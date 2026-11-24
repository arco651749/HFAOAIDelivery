"""
MetaVision AOI Remote MCP Server (Streamable HTTP / JSON-RPC 2.0)
- 掛載於 FastAPI `/mcp`，與 Gradio 入口網站共用同一埠口 (8088) 與 Cloudflare Tunnel (`https://www.metavisionsystems.com/mcp`)。
- 權限嚴格隔離：所有專案操作皆須透過 HTTP Header `Authorization: Bearer <專案帳號>:<密碼>`（或參數 `project_id` + `password`）驗證 `projects_registry.json`，僅限讀寫授權之單一專案，絕不外洩跨專案資料或內部管理權限。
"""

from __future__ import annotations

import base64
import hmac
import io
import ipaddress
import json
import socket
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from PIL import Image

MCP_PROTOCOL_VERSION = "2025-03-26"
SUPPORTED_PROTOCOLS = {"2025-03-26", "2024-11-05"}
SERVER_INFO = {
    "name": "metavision-aoi-mcp",
    "version": "1.0.0",
}

MAX_IMAGE_BYTES = 15 * 1024 * 1024  # 15 MB

TOOLS_SCHEMA: list[dict[str, Any]] = [
    {
        "name": "aoi_request_project",
        "description": (
            "免登入申請開通新的 MetaVision AOI 專案帳號。"
            "提交後將進入人工審核（閘道 0），核准後系統會將專屬帳號與密碼寄送至聯絡 Email。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "client_name": {"type": "string", "description": "客戶公司或名稱（必填，例如 TestClient）"},
                "project_name": {"type": "string", "description": "專案名稱（必填，例如 SpoolAOI）"},
                "email": {"type": "string", "description": "聯絡 Email（必填，用於接收開通帳密與進度通知）"},
                "contact_name": {"type": "string", "description": "聯絡人姓名（選填）"},
                "note": {"type": "string", "description": "專案簡述或聯絡電話（選填）"},
            },
            "required": ["client_name", "project_name", "email"],
        },
    },
    {
        "name": "aoi_get_status",
        "description": (
            "查詢已開通 AOI 專案的即時狀態（STAGE、部署版本、最新備註與待確認問題狀態）。"
            "需於 HTTP Header 帶入 `Authorization: Bearer <project_id>:<password>`，或在參數傳入 project_id 與 password。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "專案帳號（若已透過 Authorization Header 提供可省略）"},
                "password": {"type": "string", "description": "專案密碼（若已透過 Authorization Header 提供可省略）"},
            },
        },
    },
    {
        "name": "aoi_upload_sample",
        "description": (
            "上傳單張訓練樣本圖片（Base64）至專案分頁一，並可選附帶檢測需求說明與標記上傳完畢（觸發分析師開始看圖）。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "圖片檔名（含副檔名，例如 大黑軸-1.png）"},
                "image_base64": {"type": "string", "description": "圖片 Base64 編碼（支援純 Base64 或 data:image/... 前綴）"},
                "category": {
                    "type": "string",
                    "enum": ["Auto", "OK", "NG"],
                    "default": "Auto",
                    "description": "樣本分類：Auto（多類別/依檔名）、OK（良品）、NG（瑕疵）",
                },
                "mark_ready": {
                    "type": "boolean",
                    "default": False,
                    "description": "是否同時標記「已全部上傳完畢，通知分析師」（需一併提供 requirements）",
                },
                "requirements": {
                    "type": "string",
                    "description": "白話檢測需求說明（當 mark_ready=true 時必填）",
                },
                "project_id": {"type": "string", "description": "專案帳號（Header 未提供時填寫）"},
                "password": {"type": "string", "description": "專案密碼（Header 未提供時填寫）"},
            },
            "required": ["filename", "image_base64"],
        },
    },
    {
        "name": "aoi_get_discuss",
        "description": "讀取分頁二（Discuss）中分析師發布的待確認問題與歷史問答紀錄。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "專案帳號（Header 未提供時填寫）"},
                "password": {"type": "string", "description": "專案密碼（Header 未提供時填寫）"},
            },
        },
    },
    {
        "name": "aoi_reply_discuss",
        "description": "在分頁二（Discuss）回覆分析師的開工前確認問題，可選擇夾帶 Base64 補充圖片或文件附件。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reply_text": {"type": "string", "description": "客戶回覆文字內容"},
                "attachments": {
                    "type": "array",
                    "description": "選填補充附件清單",
                    "items": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string"},
                            "data_base64": {"type": "string"},
                        },
                        "required": ["filename", "data_base64"],
                    },
                },
                "project_id": {"type": "string", "description": "專案帳號（Header 未提供時填寫）"},
                "password": {"type": "string", "description": "專案密碼（Header 未提供時填寫）"},
            },
            "required": ["reply_text"],
        },
    },
    {
        "name": "aoi_detect_image",
        "description": (
            "呼叫已部署（DEPLOYED）之專案 AOI 演算法進行單張影像推論，"
            "回傳結構化檢測結果（類別、數量、座標、推論耗時與狀態摘要），並可選擇回傳標註視覺圖。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_base64": {"type": "string", "description": "待測圖片 Base64 編碼（與 image_url 二擇一）"},
                "image_url": {"type": "string", "description": "公開可存取的圖片 HTTP/HTTPS URL（與 image_base64 二擇一）"},
                "filename": {"type": "string", "default": "mcp_input.png", "description": "圖片檔名標籤（選填）"},
                "return_annotated_image": {
                    "type": "boolean",
                    "default": False,
                    "description": "是否同時回傳 JPEG Base64 標註結果圖（預設 false 以節省 Token）",
                },
                "project_id": {"type": "string", "description": "專案帳號（Header 未提供時填寫）"},
                "password": {"type": "string", "description": "專案密碼（Header 未提供時填寫）"},
            },
        },
    },
    {
        "name": "aoi_report_misjudgment",
        "description": "回報單張盲測判錯樣本，自動歸檔圖片並寫入 HARDCASE_QUEUE.jsonl 進入模型強化修正流程。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_base64": {"type": "string", "description": "判錯原圖 Base64 編碼"},
                "predicted_label": {"type": "string", "description": "模型原先判定的結果摘要"},
                "feedback_text": {"type": "string", "description": "正確結果與詳細說明（例如：應為大黑軸 6 顆＋綠墊 1）"},
                "project_id": {"type": "string", "description": "專案帳號（Header 未提供時填寫）"},
                "password": {"type": "string", "description": "專案密碼（Header 未提供時填寫）"},
            },
            "required": ["image_base64", "feedback_text"],
        },
    },
]


def _cors_headers(session_id: str | None = None) -> dict[str, str]:
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Mcp-Session-Id, X-Project-Id, X-Project-Password",
        "Access-Control-Expose-Headers": "Mcp-Session-Id",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    return headers


def _extract_credentials(request: Request, args: dict[str, Any]) -> tuple[str, str]:
    """支援 Bearer <project_id>:<password>、X-Project-Id/X-Project-Password 與工具參數。"""
    auth = (request.headers.get("authorization") or "").strip()
    if auth.lower().startswith("bearer "):
        token = auth[7:].strip()
        if ":" in token:
            pid, pw = token.split(":", 1)
            return pid.strip(), pw.strip()

    hdr_pid = (request.headers.get("x-project-id") or "").strip()
    hdr_pw = (request.headers.get("x-project-password") or "").strip()
    if hdr_pid and hdr_pw:
        return hdr_pid, hdr_pw

    return str(args.get("project_id") or "").strip(), str(args.get("password") or "").strip()


def _decode_base64_payload(b64_str: str) -> bytes:
    s = (b64_str or "").strip()
    if "," in s and s[:40].lower().startswith("data:"):
        s = s.split(",", 1)[1]
    raw = base64.b64decode(s, validate=False)
    if not raw or len(raw) > MAX_IMAGE_BYTES:
        raise ValueError(f"檔案大小無效或超過 {MAX_IMAGE_BYTES // (1024 * 1024)} MB 上限")
    return raw


def _fetch_public_image_url(url: str) -> bytes:
    parsed = urllib.parse.urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("image_url 僅允許公開 http:// 或 https:// 網址")

    # SSRF 防護：阻擋回環位址、區域內網與雲端中繼資料 IP
    try:
        infos = socket.getaddrinfo(parsed.hostname, None)
    except Exception as exc:
        raise ValueError(f"無法解析網址主機：{exc}") from exc

    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise ValueError("安全限制：不允許抓取內網或本機位址圖片")

    req = urllib.request.Request(url.strip(), headers={"User-Agent": "MetaVisionAOI-MCP/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read(MAX_IMAGE_BYTES + 1)
    if not data or len(data) > MAX_IMAGE_BYTES:
        raise ValueError(f"下載圖片失敗或超過 {MAX_IMAGE_BYTES // (1024 * 1024)} MB 上限")
    return data


def _bytes_to_bgr(raw: bytes) -> np.ndarray:
    arr = np.frombuffer(raw, dtype=np.uint8)
    img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError("圖片解碼失敗，請確認為有效 PNG / JPG / BMP / WebP 影像")
    return img_bgr


def create_mcp_router(app_mod: Any) -> APIRouter:
    """建立掛載於 `/mcp` 的 Remote MCP Streamable HTTP Router，複用 app.py 核心狀態與推論快取。"""
    router = APIRouter()

    def _authenticate(request: Request, args: dict[str, Any]) -> str:
        pid, pw = _extract_credentials(request, args)
        if not pid or not pw:
            raise PermissionError(
                "缺少專案驗證資訊。請在 HTTP Header 帶入 `Authorization: Bearer <專案帳號>:<密碼>`，"
                "或在參數中提供 `project_id` 與 `password`。"
            )
        reg = app_mod._load_registry()
        info = reg.get(pid)
        expected = str((info or {}).get("password") or "")
        if not info or not expected or not hmac.compare_digest(pw, expected):
            raise PermissionError("專案帳號或密碼驗證失敗，請確認憑證是否正確。")
        return pid

    def _call_tool(request: Request, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        # 1. 免登入：線上申請開案
        if tool_name == "aoi_request_project":
            msg = app_mod.handle_project_request(
                args.get("client_name", ""),
                args.get("project_name", ""),
                args.get("contact_name", ""),
                args.get("email", ""),
                args.get("note", ""),
            )
            ok = msg.startswith("📩")
            return {
                "content": [{"type": "text", "text": json.dumps({"ok": ok, "message": msg}, ensure_ascii=False)}],
                "isError": not ok,
            }

        # 以下皆需專案帳密驗證（單一專案隔離）
        pid = _authenticate(request, args)

        if tool_name == "aoi_get_status":
            st = app_mod._read_state(pid)
            stage = st.get("stage", "WAITING_UPLOAD")
            q_md, _ = app_mod._load_discuss_views(pid)
            payload = {
                "project_id": pid,
                "stage": stage,
                "stage_label": app_mod.STAGE_LABELS.get(stage, stage),
                "version": st.get("version", "未部署"),
                "note": st.get("note", ""),
                "updated_at": st.get("updated_at", ""),
                "blind_test_ready": stage == "DEPLOYED",
                "questions_preview": q_md[:500],
            }
            return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}

        if tool_name == "aoi_upload_sample":
            fname = Path(str(args.get("filename") or "sample.png")).name
            if Path(fname).suffix.lower() not in app_mod.ALLOWED_EXTS:
                raise ValueError(f"不支援的副檔名：{fname}（僅支援 PNG/JPG/BMP/WebP/TIFF）")
            cat = str(args.get("category") or "Auto")
            if cat not in {"Auto", "OK", "NG"}:
                raise ValueError("category 僅允許 Auto / OK / NG")

            raw = _decode_base64_payload(str(args.get("image_base64") or ""))
            _ = _bytes_to_bgr(raw)  # 驗證確實為有效影像

            paths = app_mod._project_paths(pid)
            today = app_mod._today_str()
            save_dir = paths["data"] / "raw" / cat / today
            save_dir.mkdir(parents=True, exist_ok=True)
            out_path = save_dir / fname
            if out_path.exists():
                out_path = save_dir / f"{out_path.stem}_{datetime.now().strftime('%H%M%S_%f')[:10]}{out_path.suffix}"
            out_path.write_bytes(raw)

            ready_msg = ""
            if bool(args.get("mark_ready", False)):
                req_text = str(args.get("requirements") or "").strip()
                ready_msg = app_mod.notify_ready(pid, req_text)
                if ready_msg.startswith("⚠️"):
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(
                                    {"ok": False, "saved_file": out_path.name, "message": ready_msg},
                                    ensure_ascii=False,
                                ),
                            }
                        ],
                        "isError": True,
                    }

            payload = {
                "ok": True,
                "project_id": pid,
                "category": cat,
                "saved_path": f"data/raw/{cat}/{today}/{out_path.name}",
                "ready_status": ready_msg or "已儲存樣本（尚未標記上傳完畢）",
            }
            return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}

        if tool_name == "aoi_get_discuss":
            q_md, log_md = app_mod._load_discuss_views(pid)
            payload = {
                "project_id": pid,
                "questions_md": q_md,
                "discuss_log_md": log_md,
            }
            return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}

        if tool_name == "aoi_reply_discuss":
            reply_text = str(args.get("reply_text") or "").strip()
            attachments = args.get("attachments") or []
            temp_files: list[str] = []
            paths = app_mod._project_paths(pid)
            today = app_mod._today_str()
            tmp_dir = paths["analyst"] / "attachments" / today / "_mcp_tmp"
            try:
                if attachments:
                    tmp_dir.mkdir(parents=True, exist_ok=True)
                    for idx, att in enumerate(attachments):
                        att_name = Path(str(att.get("filename") or f"att_{idx}.bin")).name
                        att_bytes = _decode_base64_payload(str(att.get("data_base64") or ""))
                        tmp_p = tmp_dir / att_name
                        tmp_p.write_bytes(att_bytes)
                        temp_files.append(str(tmp_p))
                status_msg, q_md, _ = app_mod.submit_client_reply(pid, reply_text, temp_files or None)
            finally:
                for p_str in temp_files:
                    try:
                        Path(p_str).unlink(missing_ok=True)
                    except Exception:
                        pass
                try:
                    if tmp_dir.exists() and not any(tmp_dir.iterdir()):
                        tmp_dir.rmdir()
                except Exception:
                    pass

            ok = status_msg.startswith("✅")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            {"ok": ok, "message": status_msg, "questions_md": q_md},
                            ensure_ascii=False,
                        ),
                    }
                ],
                "isError": not ok,
            }

        if tool_name == "aoi_detect_image":
            st = app_mod._read_state(pid)
            stage = st.get("stage", "WAITING_UPLOAD")
            if stage == "CLOSED":
                raise RuntimeError("此專案已驗收結案封存，線上推論已關閉。")
            if stage != "DEPLOYED":
                raise RuntimeError(f"演算法尚未部署上線（目前狀態：{stage} — {st.get('note', '')}）。")

            b64_in = args.get("image_base64")
            url_in = args.get("image_url")
            if b64_in:
                raw = _decode_base64_payload(str(b64_in))
            elif url_in:
                raw = _fetch_public_image_url(str(url_in))
            else:
                raise ValueError("請提供 `image_base64` 或 `image_url` 其中之一。")

            img_bgr = _bytes_to_bgr(raw)
            h, w = img_bgr.shape[:2]

            # 歸檔原圖（不破壞原圖）
            paths = app_mod._project_paths(pid)
            today = app_mod._today_str()
            ts = datetime.now().strftime("%H%M%S_%f")[:10]
            fname = Path(str(args.get("filename") or f"mcp_{ts}.png")).name
            save_dir = paths["test_uploads"] / today / "mcp"
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = save_dir / f"{ts}_{fname}"
            if save_path.suffix.lower() not in app_mod.ALLOWED_EXTS:
                save_path = save_path.with_suffix(".png")
            ok_enc, enc_buf = cv2.imencode(".png", img_bgr)
            if ok_enc:
                enc_buf.tofile(str(save_path))

            res = app_mod._run_detector_engine(pid, img_bgr)
            headers = list(res.get("headers") or [])
            row_values = list(res.get("row_values") or [])
            fields = {}
            if len(headers) == len(row_values) + 1:
                for k, v in zip(headers[1:], row_values):
                    fields[k] = v

            payload = {
                "project_id": pid,
                "version": st.get("version", "v1.0"),
                "filename": fname,
                "image": {"w": int(w), "h": int(h)},
                "summary_label": str(res.get("summary_label", "")),
                "headers": headers,
                "row_values": row_values,
                "fields": fields,
                "status_md": str(res.get("status_md", "")),
                "archived_path": f"test_uploads/{today}/mcp/{save_path.name}",
            }
            content: list[dict[str, Any]] = [
                {"type": "text", "text": json.dumps(payload, ensure_ascii=False)}
            ]

            if bool(args.get("return_annotated_image", False)) and res.get("vis_bgr") is not None:
                ok_jpg, jpg_buf = cv2.imencode(".jpg", res["vis_bgr"], [int(cv2.IMWRITE_JPEG_QUALITY), 88])
                if ok_jpg:
                    content.append(
                        {
                            "type": "image",
                            "data": base64.b64encode(jpg_buf.tobytes()).decode("ascii"),
                            "mimeType": "image/jpeg",
                        }
                    )
            return {"content": content}

        if tool_name == "aoi_report_misjudgment":
            raw = _decode_base64_payload(str(args.get("image_base64") or ""))
            pil_img = Image.open(io.BytesIO(raw)).convert("RGB")
            msg = app_mod.report_misjudgment(
                pid,
                pil_img,
                str(args.get("predicted_label") or ""),
                str(args.get("feedback_text") or ""),
            )
            ok = not msg.startswith("⚠️ 請先") and not msg.startswith("⚠️ 目前沒有")
            return {
                "content": [{"type": "text", "text": json.dumps({"ok": ok, "message": msg}, ensure_ascii=False)}],
                "isError": not ok,
            }

        raise KeyError(f"未知的工具名稱：{tool_name}")

    @router.options("/mcp")
    async def mcp_options():
        return Response(status_code=204, headers=_cors_headers())

    @router.get("/mcp")
    async def mcp_info():
        return JSONResponse(
            {
                "service": "MetaVision AOI Remote MCP Server",
                "serverInfo": SERVER_INFO,
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "transport": "Streamable HTTP (JSON-RPC 2.0 via POST /mcp)",
                "auth": "HTTP Header `Authorization: Bearer <project_id>:<password>` (or tool arguments)",
                "tools": [t["name"] for t in TOOLS_SCHEMA],
                "docs_url": "https://www.metavisionsystems.com",
            },
            headers=_cors_headers(),
        )

    @router.delete("/mcp")
    async def mcp_delete():
        return Response(status_code=204, headers=_cors_headers())

    @router.post("/mcp")
    async def mcp_rpc(request: Request):
        session_id = request.headers.get("mcp-session-id") or str(uuid.uuid4())
        try:
            body = await request.json()
        except Exception:
            return JSONResponse(
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error: invalid JSON"}},
                status_code=400,
                headers=_cors_headers(session_id),
            )

        if not isinstance(body, dict):
            return JSONResponse(
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}},
                status_code=400,
                headers=_cors_headers(session_id),
            )

        req_id = body.get("id")
        method = str(body.get("method") or "")
        params = body.get("params") or {}

        # Notifications (no id) -> 202 Accepted per MCP Streamable HTTP spec
        if req_id is None and method.startswith("notifications/"):
            return Response(status_code=202, headers=_cors_headers(session_id))

        if method == "initialize":
            client_proto = str(params.get("protocolVersion") or MCP_PROTOCOL_VERSION)
            negotiated = client_proto if client_proto in SUPPORTED_PROTOCOLS else MCP_PROTOCOL_VERSION
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": negotiated,
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": SERVER_INFO,
                        "instructions": (
                            "MetaVision AOI Remote MCP Server。"
                            "請於 HTTP Header 帶入 `Authorization: Bearer <project_id>:<password>` 驗證專案權限；"
                            "若尚未開通專案可免登入呼叫 `aoi_request_project`。"
                        ),
                    },
                },
                headers=_cors_headers(session_id),
            )

        if method == "ping":
            return JSONResponse({"jsonrpc": "2.0", "id": req_id, "result": {}}, headers=_cors_headers(session_id))

        if method == "tools/list":
            return JSONResponse(
                {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_SCHEMA}},
                headers=_cors_headers(session_id),
            )

        if method == "tools/call":
            tool_name = str(params.get("name") or "")
            tool_args = params.get("arguments") or {}
            if not isinstance(tool_args, dict):
                return JSONResponse(
                    {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32602, "message": "Invalid params: arguments must be an object"},
                    },
                    headers=_cors_headers(session_id),
                )
            try:
                result = _call_tool(request, tool_name, tool_args)
                return JSONResponse(
                    {"jsonrpc": "2.0", "id": req_id, "result": result},
                    headers=_cors_headers(session_id),
                )
            except KeyError as exc:
                return JSONResponse(
                    {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": str(exc)}},
                    headers=_cors_headers(session_id),
                )
            except Exception as exc:
                return JSONResponse(
                    {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False),
                                }
                            ],
                            "isError": True,
                        },
                    },
                    headers=_cors_headers(session_id),
                )

        return JSONResponse(
            {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}},
            headers=_cors_headers(session_id),
        )

    return router
