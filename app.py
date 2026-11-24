"""
MetaVision AOI 多專案協作與驗收平台 (Gradio)
- 帳號即專案：登入帳號即為 `<客戶名稱>-<客戶專案>`，單一入口服務所有客戶、資料 100% 專案隔離。
- 防亂玩機制：查無帳號時可填寫客戶名稱、專案名稱與聯絡 Email 線上申請開案，審核後發送專屬密碼。
- 三分頁協作：
  1. 分頁一：訓練樣本上傳區 (OK/NG/Auto + ZIP 串流解壓保留子目錄 + 檢測需求說明 + READY.json)
  2. 分頁二：需求討論與問答確認區 (統一讀寫 ANALYST/ANALYST.md 公開區段 + 附件歸檔 + CLIENT_REPLIED.json)
  3. 分頁三：線上盲測驗收區 (STATE.json 未上線/結案鎖定 + mtime 快取熱插拔 CODER/detector.py + Excel 報表 + HARDCASE_QUEUE.jsonl)
"""

import importlib.util
import json
import os
import re
import sys
import threading
import time
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import cv2
import gradio as gr
import numpy as np
import openpyxl
import uvicorn
from fastapi import FastAPI
from huggingface_hub import HfApi
from PIL import Image

from agy_reviewer import create_agy_bridge_router, review_batch, review_single
from mcp_server import create_mcp_router

# === 全域路徑與設定 ===
BASE_DIR = Path(__file__).parent.resolve()
PROJECTS_ROOT = BASE_DIR / "projects"
PENDING_DIR = BASE_DIR / "pending_requests"
REGISTRY_PATH = BASE_DIR / "projects_registry.json"
AUDIT_LOG_PATH = BASE_DIR / "request_audit_log.jsonl"

PROJECTS_ROOT.mkdir(parents=True, exist_ok=True)
PENDING_DIR.mkdir(parents=True, exist_ok=True)

HF_TOKEN = os.getenv("HF_TOKEN", "")
SERVER_PORT = int(os.getenv("PORT", "7860" if os.getenv("SPACE_ID") else "8088"))

ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff"}

# 全系統統一 10 種狀態（與 AI_MANAGER_SOP.md 100% 對齊）
STAGE_LABELS = {
    "WAITING_UPLOAD": "等待客戶上傳訓練樣本與需求",
    "UPLOADED": "客戶已上傳樣本，等待分析師看圖評估",
    "ANALYZING": "分析師正在看圖與撰寫規格草案",
    "WAITING_CLIENT_QA": "開工前需求確認中（請至分頁二回覆問題）",
    "CLIENT_REPLIED": "客戶已回覆問題，等待分析師整理定案",
    "SPEC_FROZEN": "規格已定案，準備交棒工程師開發",
    "CODING": "演算法工程師開發與交叉驗證中",
    "DIRECTOR_REVIEW": "開發完成，等待產品導演 Review 驗收",
    "DEPLOYED": "演算法已部署上線，開放線上盲測",
    "CLOSED": "專案已驗收結案封存",
}

# 依 (project_id, mtime_ns) 快取已載入的 CODER/detector.py，避免整批測試重複載入模型
_DETECTOR_CACHE: dict[str, tuple[int, object]] = {}

# 追蹤各專案正在執行之 AGY 視覺覆核任務（供重傳、登出或斷線時秒殺舊 agy.exe，零浪費額度）
_ACTIVE_AGY_LOCK = threading.Lock()
_ACTIVE_AGY_CANCELS: dict[tuple[str, str], threading.Event] = {}


def _cancel_agy_slot(project_id: str | None, mode: str | None = None) -> None:
    if not project_id:
        return
    with _ACTIVE_AGY_LOCK:
        modes = (mode,) if mode else ("single", "batch")
        for m in modes:
            evt = _ACTIVE_AGY_CANCELS.pop((project_id, m), None)
            if evt is not None:
                evt.set()


def _register_agy_slot(project_id: str, mode: str) -> threading.Event:
    evt = threading.Event()
    with _ACTIVE_AGY_LOCK:
        old = _ACTIVE_AGY_CANCELS.get((project_id, mode))
        if old is not None:
            old.set()
        _ACTIVE_AGY_CANCELS[(project_id, mode)] = evt
    return evt


def _today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _load_registry() -> dict:
    if REGISTRY_PATH.exists():
        try:
            return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _read_bgr_unicode(path: Path) -> np.ndarray | None:
    """Windows 中文路徑安全讀圖（嚴禁直接使用 cv2.imread）。"""
    try:
        data = np.fromfile(str(path), dtype=np.uint8)
        if data.size == 0:
            return None
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception:
        return None


def _project_paths(project_id: str) -> dict[str, Path]:
    pdir = PROJECTS_ROOT / project_id
    paths = {
        "root": pdir,
        "state": pdir / "STATE.json",
        "data": pdir / "data",
        "analyst": pdir / "ANALYST",
        "coder": pdir / "CODER",
        "detector": pdir / "CODER" / "detector.py",
        "test_uploads": pdir / "test_uploads",
        "hardcase_queue": pdir / "test_uploads" / "HARDCASE_QUEUE.jsonl",
    }
    for sub in (
        paths["data"] / "raw" / "OK",
        paths["data"] / "raw" / "NG",
        paths["data"] / "raw" / "Auto",
        paths["analyst"],
        paths["coder"] / "eval_outputs",
        paths["test_uploads"],
    ):
        sub.mkdir(parents=True, exist_ok=True)
    return paths


def _get_project_hf(project_id: str) -> tuple[HfApi | None, str]:
    reg = _load_registry()
    hf_repo = reg.get(project_id, {}).get("hf_repo_id", "").strip()
    if not HF_TOKEN or not hf_repo:
        return None, ""
    return HfApi(token=HF_TOKEN), hf_repo


def _read_state(project_id: str) -> dict:
    paths = _project_paths(project_id)
    if paths["state"].exists():
        try:
            return json.loads(paths["state"].read_text(encoding="utf-8"))
        except Exception:
            pass
    default_state = {
        "project_id": project_id,
        "stage": "WAITING_UPLOAD",
        "version": "未部署",
        "note": STAGE_LABELS["WAITING_UPLOAD"],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    paths["state"].write_text(json.dumps(default_state, indent=2, ensure_ascii=False), encoding="utf-8")
    return default_state


def _update_state(project_id: str, stage: str, note: str | None = None, version: str | None = None) -> dict:
    paths = _project_paths(project_id)
    st = _read_state(project_id)
    st["project_id"] = project_id
    st["stage"] = stage
    st["note"] = note if note is not None else STAGE_LABELS.get(stage, stage)
    if version is not None:
        st["version"] = version
    st["updated_at"] = datetime.now(timezone.utc).isoformat()
    paths["state"].write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
    return st


def _is_valid_image_name(name: str) -> bool:
    p = Path(name)
    if any(part.startswith("__MACOSX") or part.startswith(".") for part in p.parts):
        return False
    if p.name in {"Thumbs.db", ".DS_Store"}:
        return False
    return p.suffix.lower() in ALLOWED_EXTS


def _safe_zip_filename(raw_member_name: str) -> str:
    """保留 ZIP 內子資料夾資訊（轉成 <子目錄>_<檔名>）並防止路徑穿越與同名覆蓋。"""
    parts = [p for p in Path(raw_member_name).parts if p not in ("", ".", "..", "/", "\\")]
    if len(parts) <= 1:
        return Path(raw_member_name).name
    prefix = "_".join(parts[:-1])
    safe_prefix = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", prefix)
    return f"{safe_prefix}_{parts[-1]}"


def _extract_images_from_files(files, dest_dir: Path) -> list[Path]:
    saved: list[Path] = []
    if not files:
        return saved
    for f in files:
        src_path = Path(f.name if hasattr(f, "name") else str(f))
        if src_path.suffix.lower() == ".zip":
            with zipfile.ZipFile(src_path, "r") as zf:
                for info in zf.infolist():
                    if info.is_dir() or not _is_valid_image_name(info.filename):
                        continue
                    safe_name = _safe_zip_filename(info.filename)
                    target = dest_dir / safe_name
                    with zf.open(info, "r") as src, open(target, "wb") as dst:
                        while chunk := src.read(65536):
                            dst.write(chunk)
                    saved.append(target)
        elif _is_valid_image_name(src_path.name):
            target = dest_dir / src_path.name
            target.write_bytes(src_path.read_bytes())
            saved.append(target)
    return saved


# === 登入與新專案開通申請 ===
def _sanitize_id(s: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff\-]", "", (s or "").strip())


def handle_login(project_id: str, password: str):
    pid = (project_id or "").strip()
    pw = (password or "").strip()
    if not pid or not pw:
        return (
            None,
            "⚠️ 請輸入「專案帳號（`<客戶名稱>-<客戶專案>`）」與「專屬密碼」。",
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            "",
            "",
            "",
        )

    reg = _load_registry()
    if pid not in reg:
        return (
            None,
            f"❌ 查無專案帳號 **`{pid}`**！\n\n若為首次合作或新專案，請在右側 **「🆕 尚未開通專案？線上申請帳號」** 填寫客戶名稱、專案名稱與聯絡 Email，我們審核後會將專屬密碼寄送至您的信箱。",
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            "",
            "",
            "",
        )

    if reg[pid].get("password") != pw:
        return (
            None,
            "❌ 密碼錯誤，請確認信箱中收到的專屬密碼，或聯繫 MetaVision 窗口重新發送。",
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            "",
            "",
            "",
        )

    hf_repo = reg[pid].get("hf_repo_id", "").strip()
    header_md = (
        f"# 🔍 MetaVision AOI 全自動視覺檢測與驗收平台\n"
        f"- **當前專案帳號**：`{pid}`　|　**聯絡信箱**：`{reg[pid].get('email', '-')}`　|　"
        f"**圖庫模式**：`{hf_repo or '本機專案隔離模式 (Local)'}`"
    )
    q_md, log_md = _load_discuss_views(pid)
    banner_md = _get_blind_test_banner(pid)
    return (
        pid,
        "",
        gr.update(visible=False),
        gr.update(visible=True),
        header_md,
        q_md,
        log_md,
        banner_md,
    )


def handle_logout(project_id: str | None = None):
    _cancel_agy_slot(project_id)
    return (
        None,
        "已登出。請重新輸入專案帳號與密碼。",
        gr.update(visible=True),
        gr.update(visible=False),
    )


def handle_project_request(client_name: str, project_title: str, contact_name: str, email: str, note: str) -> str:
    c_clean = _sanitize_id(client_name)
    p_clean = _sanitize_id(project_title)
    email_clean = (email or "").strip()

    if not c_clean or not p_clean:
        return "⚠️ 請填寫有效的「客戶名稱」與「專案名稱」（建議使用英數字或中文，不含特殊符號）。"
    if not email_clean or "@" not in email_clean:
        return "⚠️ 請填寫有效的「聯絡 Email」，我們將把專屬開通密碼寄送到此信箱。"

    project_id = f"{c_clean}-{p_clean}"
    reg = _load_registry()
    if project_id in reg:
        return f"⚠️ 專案帳號 **`{project_id}`** 已經開通！請直接使用既有密碼於左側登入，或聯繫窗口補寄密碼。"

    req_file = PENDING_DIR / f"{project_id}.json"
    if req_file.exists():
        return f"⚠️ 專案帳號 **`{project_id}`** 已有待審核申請正在處理中，請勿重複提交；若有異動請直接聯繫 MetaVision 窗口。"

    payload = {
        "status": "PENDING_APPROVAL",
        "project_id": project_id,
        "client_name": c_clean,
        "project_title": p_clean,
        "contact": (contact_name or "").strip(),
        "email": email_clean,
        "phone_or_note": (note or "").strip(),
        "requested_at": datetime.now(timezone.utc).isoformat(),
    }
    req_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as af:
        af.write(json.dumps({"event": "REQUESTED", **payload}, ensure_ascii=False) + "\n")

    return (
        f"✅ 已收到您的開案申請！\n\n"
        f"- **預定專案帳號**：`{project_id}`\n"
        f"- **收件信箱**：`{email_clean}`\n\n"
        f"我們審核開通後，會立即將 **專屬密碼** 寄送至您的 Email，屆時即可返回左側登入使用。"
    )


# === 分頁一：訓練樣本上傳 ===
def upload_samples(project_id: str | None, label_choice: str, files) -> str:
    if not project_id:
        return "⚠️ 請先登入專案帳號。"
    if not files:
        return "⚠️ 請先選擇或拖拉圖片 / ZIP 壓縮檔。"

    if "Auto" in label_choice:
        category = "Auto"
    elif "OK" in label_choice:
        category = "OK"
    else:
        category = "NG"

    paths = _project_paths(project_id)
    today = _today_str()
    dest_dir = paths["data"] / "raw" / category / today
    dest_dir.mkdir(parents=True, exist_ok=True)
    saved = _extract_images_from_files(files, dest_dir)
    if not saved:
        return "⚠️ 未偵測到有效圖片（支援 PNG / JPG / BMP / WEBP / TIF 或 ZIP）。"

    sync_msg = f"已儲存於本機專案目錄 `projects/{project_id}/data/raw/{category}/{today}/`"
    api, hf_repo = _get_project_hf(project_id)
    if api and hf_repo:
        try:
            api.upload_folder(
                folder_path=str(dest_dir),
                path_in_repo=f"raw/{category}/{today}",
                repo_id=hf_repo,
                repo_type="dataset",
                commit_message=f"Batch upload {len(saved)} {category} samples ({today})",
            )
            sync_msg = f"已批次同步至 HF 私密圖庫 `{hf_repo}` (`raw/{category}/{today}/`)"
        except Exception as e:
            sync_msg = f"本機已儲存，但 HF 同步失敗：{e}"

    return f"✅ 成功接收 **{len(saved)}** 張 **{category}** 樣本圖。\n\n- 狀態：{sync_msg}"


def notify_ready(project_id: str | None, requirements_text: str) -> str:
    if not project_id:
        return "⚠️ 請先登入專案帳號。"
    req_clean = (requirements_text or "").strip()
    if not req_clean:
        return "⚠️ 請先在「📝 檢測需求說明」填寫您想檢測的內容，再通知分析師。"

    paths = _project_paths(project_id)
    ok_count = sum(1 for p in (paths["data"] / "raw" / "OK").rglob("*") if p.is_file())
    ng_count = sum(1 for p in (paths["data"] / "raw" / "NG").rglob("*") if p.is_file())
    auto_count = sum(1 for p in (paths["data"] / "raw" / "Auto").rglob("*") if p.is_file())
    if ok_count + ng_count + auto_count == 0:
        return "⚠️ 目前尚未偵測到任何已上傳的樣本圖片，請先按「⬆️ 開始上傳樣本」成功接收圖片後再通知分析師。"

    api, hf_repo = _get_project_hf(project_id)
    payload = {
        "status": "READY",
        "project_id": project_id,
        "repo_id": hf_repo or "(local-only)",
        "client_requirements": req_clean,
        "local_ok_count": ok_count,
        "local_ng_count": ng_count,
        "local_auto_count": auto_count,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    ready_path = paths["data"] / "READY.json"
    ready_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # 狀態守門員：僅在開案上傳階段改為 UPLOADED，絕不降級覆蓋已開發/已上線之專案狀態
    cur_stage = _read_state(project_id).get("stage", "WAITING_UPLOAD")
    if cur_stage in {"WAITING_UPLOAD", "UPLOADED"}:
        _update_state(
            project_id,
            "UPLOADED",
            note=f"客戶已上傳樣本（OK:{ok_count}/NG:{ng_count}/Auto:{auto_count}）並提交檢測需求",
        )

    if api and hf_repo:
        try:
            api.upload_file(
                path_or_fileobj=str(ready_path),
                path_in_repo="READY.json",
                repo_id=hf_repo,
                repo_type="dataset",
                commit_message="Mark dataset READY for training with client requirements",
            )
            return f"📩 已寫入 `READY.json`（含檢測需求說明）並通知分析師！（OK {ok_count} 張 / NG {ng_count} 張 / Auto {auto_count} 張）"
        except Exception as e:
            return f"⚠️ 本機已產生 `READY.json`，但上傳 HF 失敗：{e}"

    return f"📩 已在本機產生 `READY.json`（含檢測需求說明）並通知分析師！（OK {ok_count} 張 / NG {ng_count} 張 / Auto {auto_count} 張）"


# === 分頁二：需求討論與問答確認 (統一讀寫 ANALYST/ANALYST.md) ===
Q_START = "<!-- CLIENT_QUESTIONS_START -->"
Q_END = "<!-- CLIENT_QUESTIONS_END -->"
LOG_START = "<!-- DISCUSS_LOG_START -->"

ANALYST_MD_TEMPLATE = f"""# 🔍 專案分析與規格確認書 (ANALYST)

- **Status**: `WAITING_UPLOAD`

## 1. 影像觀察與執行細則（內部規格）
（待客戶上傳樣本後，由分析師看圖撰寫）

## 2. 給客戶的待確認問題
{Q_START}
（目前尚無待確認問題。樣本上傳並通知分析師後，系統將於此處顯示開工前確認問題。）
{Q_END}

## 3. 客戶討論紀錄 (Q&A LOG)
{LOG_START}
（尚無歷史討論紀錄。）
"""


def _load_discuss_views(project_id: str | None) -> tuple[str, str]:
    """僅讀取 ANALYST.md 公開區段（不主動建立假檔案，避免誤導巡檢）。"""
    if not project_id:
        return "（尚未登入專案）", "（尚無紀錄）"
    paths = _project_paths(project_id)
    md_path = paths["analyst"] / "ANALYST.md"
    if not md_path.exists():
        return (
            "（目前尚無待確認問題。樣本上傳並通知分析師後，系統將於此處顯示開工前確認問題。）",
            "（尚無歷史討論紀錄。）",
        )

    content = md_path.read_text(encoding="utf-8")
    if Q_START in content and Q_END in content:
        q_md = content.split(Q_START, 1)[1].split(Q_END, 1)[0].strip()
    else:
        q_md = "（目前尚無待確認問題。）"

    if LOG_START in content:
        log_md = content.split(LOG_START, 1)[1].strip()
    else:
        log_md = "（尚無歷史討論紀錄。）"

    return q_md or "（目前尚無待確認問題。）", log_md or "（尚無歷史討論紀錄。）"


def submit_client_reply(project_id: str | None, reply_text: str, attachments) -> tuple[str, str, str]:
    if not project_id:
        return "⚠️ 請先登入專案帳號。", "", ""
    text = (reply_text or "").strip()
    if not text and not attachments:
        q_md, log_md = _load_discuss_views(project_id)
        return "⚠️ 請至少輸入回覆文字，或上傳圖片/文件附件。", q_md, log_md

    paths = _project_paths(project_id)
    today = _today_str()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_file = datetime.now().strftime("%H%M%S")
    attach_dir = paths["analyst"] / "attachments" / today
    attach_dir.mkdir(parents=True, exist_ok=True)

    saved_names: list[str] = []
    if attachments:
        for f in attachments:
            src = Path(f.name if hasattr(f, "name") else str(f))
            safe_name = f"{ts_file}_{src.name}"
            dst = attach_dir / safe_name
            dst.write_bytes(src.read_bytes())
            saved_names.append(f"attachments/{today}/{safe_name}")

    md_path = paths["analyst"] / "ANALYST.md"
    if not md_path.exists():
        md_path.write_text(ANALYST_MD_TEMPLATE, encoding="utf-8")
    content = md_path.read_text(encoding="utf-8")
    if LOG_START not in content:
        content = content.rstrip() + f"\n\n## 3. 客戶討論紀錄 (Q&A LOG)\n{LOG_START}\n"

    content = content.replace("（尚無歷史討論紀錄。）", "").rstrip()

    entry_lines = [
        f"\n\n### 👨‍💼 客戶回覆（{ts}）",
        text if text else "（僅上傳附件）",
    ]
    if saved_names:
        entry_lines.append("**📎 附件檔案**：")
        for rel in saved_names:
            entry_lines.append(f"- `{rel}`")
    entry_lines.append("\n---")

    md_path.write_text(content + "\n".join(entry_lines) + "\n", encoding="utf-8")

    reply_flag = paths["analyst"] / "CLIENT_REPLIED.json"
    reply_flag.write_text(
        json.dumps(
            {
                "status": "CLIENT_REPLIED",
                "project_id": project_id,
                "replied_at": datetime.now(timezone.utc).isoformat(),
                "reply_text": text,
                "attachments": saved_names,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # 狀態守門員：僅在需求分析/問答階段切為 CLIENT_REPLIED，避免把已 DEPLOYED 的分頁三鎖死！
    cur_stage = _read_state(project_id).get("stage", "WAITING_UPLOAD")
    if cur_stage in {"WAITING_CLIENT_QA", "CLIENT_REPLIED", "ANALYZING"}:
        _update_state(
            project_id,
            "CLIENT_REPLIED",
            note=f"客戶已於討論區回覆（附件 {len(saved_names)} 件），等待分析師整理",
        )

    api, hf_repo = _get_project_hf(project_id)
    sync_note = f"已記錄至本機 `projects/{project_id}/ANALYST/ANALYST.md`"
    if api and hf_repo:
        try:
            api.upload_folder(
                folder_path=str(paths["analyst"]),
                path_in_repo="ANALYST",
                repo_id=hf_repo,
                repo_type="dataset",
                commit_message=f"Client discuss reply ({today} {ts_file})",
            )
            sync_note = "已同步寫入本機與 HF 圖庫 `ANALYST/`"
        except Exception as e:
            sync_note = f"本機已記錄，但 HF 同步失敗：{e}"

    q_md, log_md = _load_discuss_views(project_id)
    return f"✅ 已送出回覆並通知分析師！（附件 {len(saved_names)} 件；{sync_note}）", q_md, log_md


# === 分頁三：線上盲測驗收 ===
def _get_blind_test_banner(project_id: str | None) -> str:
    if not project_id:
        return "（請先登入專案帳號）"
    st = _read_state(project_id)
    stage = st.get("stage", "WAITING_UPLOAD")
    ver = st.get("version", "未部署")
    note = st.get("note", "")
    updated = st.get("updated_at", "")[:19].replace("T", " ")
    if stage == "DEPLOYED":
        return f"### ✅ 線上盲測已開放　|　部署版本：`{ver}`　|　更新時間：`{updated} UTC`"
    if stage == "CLOSED":
        return f"### 📦 專案已驗收結案封存　|　最終版本：`{ver}`　|　結案時間：`{updated} UTC`\n- 線上盲測已關閉，若需重新開啟或追加訓練請聯繫 MetaVision 窗口。"
    return (
        f"### ⏳ 盲測區暫未開放（演算法開發中）\n"
        f"- **目前專案進度**：`{stage}`（{note}）\n"
        f"- 待工程師開發完成並通過審核上線後，點擊「🔄 刷新部署狀態」即可開始盲測。"
    )


def _load_project_detector(project_id: str):
    """依 (project_id, mtime_ns) 快取載入 CODER/detector.py，兼顧熱重載與批次推論效能。"""
    paths = _project_paths(project_id)
    det_path = paths["detector"]
    if not det_path.exists():
        _DETECTOR_CACHE.pop(project_id, None)
        return None

    mtime_ns = det_path.stat().st_mtime_ns
    cached = _DETECTOR_CACHE.get(project_id)
    if cached is not None and cached[0] == mtime_ns:
        return cached[1]

    spec = importlib.util.spec_from_file_location(f"detector_{project_id}_{mtime_ns}", str(det_path))
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _DETECTOR_CACHE[project_id] = (mtime_ns, mod)
    return mod


def detect_defects_baseline(img_bgr: np.ndarray) -> tuple[np.ndarray, str, int, float]:
    t0 = time.perf_counter()
    vis = img_bgr.copy()
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 60, 160)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = gray.shape
    min_area = max(120, int(h * w * 0.0005))
    max_area = int(h * w * 0.25)

    boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area <= area <= max_area:
            x, y, bw, bh = cv2.boundingRect(cnt)
            boxes.append((x, y, bw, bh))
            cv2.rectangle(vis, (x, y), (x + bw, y + bh), (0, 0, 255), 2)
            cv2.putText(vis, "Defect?", (x, max(15, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    elapsed = time.perf_counter() - t0
    verdict = "NG" if boxes else "OK"
    return vis, verdict, len(boxes), elapsed


def _run_detector_engine(project_id: str, img_bgr: np.ndarray) -> dict:
    mod = _load_project_detector(project_id)
    if mod is not None and hasattr(mod, "detect_image"):
        res = mod.detect_image(img_bgr)
        headers = getattr(mod, "REPORT_HEADERS", ["檔名", "辨識結果", "數值/分數", "耗時(秒)"])
        res.setdefault("headers", headers)
        return res

    vis_bgr, verdict, count, elapsed = detect_defects_baseline(img_bgr)
    if verdict == "NG":
        status_md = f"### 🔴 判定：NG（檢出 {count} 處疑似異常，耗時 {elapsed:.3f} 秒）"
    else:
        status_md = f"### 🟢 判定：OK（良品，耗時 {elapsed:.3f} 秒）"
    return {
        "vis_bgr": vis_bgr,
        "status_md": status_md,
        "summary_label": verdict,
        "row_values": [verdict, count, round(elapsed, 4)],
        "headers": ["檔名", "判定結果", "異常區域數", "耗時(秒)"],
    }


def run_single_test(project_id: str | None, image: Image.Image | None):
    # 只要使用者清空圖片或重新上傳新圖，立刻秒殺上一張還在跑的 AGY 覆核
    _cancel_agy_slot(project_id, "single")
    if not project_id:
        return None, "⚠️ 請先登入專案帳號。", None, None, "", ""
    if image is None:
        return None, "⚠️ 請先上傳一張測試圖片。", None, None, "", ""

    st = _read_state(project_id)
    stage = st.get("stage", "WAITING_UPLOAD")
    if stage == "CLOSED":
        return None, "📦 **此專案已驗收結案封存**，線上盲測已關閉。", None, None, "", ""
    if stage != "DEPLOYED":
        return (
            None,
            f"⏳ **演算法尚未部署上線**（目前進度：`{stage}` — {st.get('note', '')}），請等待工程師完成開發並上線後再進行盲測。",
            None,
            None,
            "",
            "",
        )

    paths = _project_paths(project_id)
    today = _today_str()
    ts = datetime.now().strftime("%H%M%S_%f")[:10]
    save_dir = paths["test_uploads"] / today / "single"
    save_dir.mkdir(parents=True, exist_ok=True)
    image.save(save_dir / f"single_{ts}.png")

    img_rgb = np.array(image.convert("RGB"))
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    res = _run_detector_engine(project_id, img_bgr)
    vis_rgb = cv2.cvtColor(res["vis_bgr"], cv2.COLOR_BGR2RGB)
    ver = st.get("version", "v1.0")
    ver_tag = f"\n\n*(版本：`{ver}`)*"

    return (
        Image.fromarray(vis_rgb),
        res["status_md"] + ver_tag,
        image,
        Image.fromarray(vis_rgb),
        str(res.get("summary_label", "")),
        _spinner_md("AGY 單張視覺覆核啟動中", 0.0),
    )


def _read_spec_brief(project_id: str, max_chars: int = 2200) -> str:
    md_path = _project_paths(project_id)["analyst"] / "ANALYST.md"
    if not md_path.exists():
        return ""
    try:
        return md_path.read_text(encoding="utf-8")[:max_chars]
    except Exception:
        return ""


def _spinner_md(title: str, elapsed_sec: float) -> str:
    return (
        '<div style="display:flex;align-items:center;gap:12px;padding:12px 16px;'
        'border-radius:10px;border:1px solid #38bdf8;background:rgba(56,189,248,0.12);margin:6px 0;">'
        '<svg width="28" height="28" viewBox="0 0 24 24" style="flex-shrink:0;">'
        '<circle cx="12" cy="12" r="9" fill="none" stroke="#bae6fd" stroke-width="3"/>'
        '<path d="M12 3a9 9 0 0 1 9 9" fill="none" stroke="#0284c7" stroke-width="3" stroke-linecap="round">'
        '<animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.9s" repeatCount="indefinite"/>'
        '</path></svg>'
        f'<div><b>🤖 {title}</b><br>'
        f'<span style="font-size:0.92em;opacity:0.88;">AGY 視覺覆核員 (<code>aoi_reviewer</code>) 正在本機沙盒細心看圖分析中，已耗時 <b>{elapsed_sec:.0f} 秒</b>（純程式結果已顯示，請稍候）...</span>'
        '</div></div>'
    )


def _yield_with_spinner(project_id: str, mode: str, title: str, fn, *args):
    cancel_evt = _register_agy_slot(project_id, mode)
    box: dict[str, str] = {}

    def _worker():
        try:
            box["result"] = fn(*args, cancel_event=cancel_evt)
        except Exception as exc:
            box["result"] = f"⚠️ AGY 視覺覆核執行異常（請直接參考純程式判定結果）：`{exc}`"

    t0 = time.perf_counter()
    th = threading.Thread(target=_worker, daemon=True)
    th.start()
    try:
        yield _spinner_md(title, 0.0)
        while th.is_alive():
            if cancel_evt.is_set():
                return
            th.join(timeout=1.0)
            if th.is_alive() and not cancel_evt.is_set():
                yield _spinner_md(title, time.perf_counter() - t0)
        if not cancel_evt.is_set():
            yield box.get("result", "⚠️ 未取得 AGY 回覆，請稍後重試。")
    finally:
        # 瀏覽器關閉分頁、F5 重整、斷線或被新任務取代時，GeneratorExit 立即觸發秒殺 agy.exe！
        cancel_evt.set()
        with _ACTIVE_AGY_LOCK:
            if _ACTIVE_AGY_CANCELS.get((project_id, mode)) is cancel_evt:
                _ACTIVE_AGY_CANCELS.pop((project_id, mode), None)


def run_single_ai_review(
    project_id: str | None,
    orig_img: Image.Image | None,
    vis_img: Image.Image | None,
    pred_summary: str,
):
    if not project_id:
        yield "⚠️ 請先登入專案帳號。"
        return
    if orig_img is None or vis_img is None:
        yield "⚠️ 請先於上方拖入一張圖片並完成純程式檢測後，再執行 AGY 視覺覆核。"
        return
    yield from _yield_with_spinner(
        project_id,
        "single",
        "AGY 單張視覺覆核進行中",
        review_single,
        project_id,
        orig_img,
        vis_img,
        pred_summary,
        _read_spec_brief(project_id),
    )


def run_single_ai_review_auto(
    project_id: str | None,
    orig_img: Image.Image | None,
    vis_img: Image.Image | None,
    pred_summary: str,
):
    if not project_id or orig_img is None or vis_img is None:
        yield ""
        return
    yield from _yield_with_spinner(
        project_id,
        "single",
        "AGY 單張視覺覆核進行中",
        review_single,
        project_id,
        orig_img,
        vis_img,
        pred_summary,
        _read_spec_brief(project_id),
    )


def run_batch_ai_review(project_id: str | None, batch_items: list[dict] | None):
    if not project_id:
        yield "⚠️ 請先登入專案帳號。"
        return
    if not batch_items:
        yield "⚠️ 請先執行「🚀 開始整批掃描」產生盲測標註圖後，再進行 AGY 整批覆核。"
        return
    yield from _yield_with_spinner(
        project_id,
        "batch",
        f"AGY 整批視覺覆核進行中（共 {min(len(batch_items), 12)} 張）",
        review_batch,
        project_id,
        batch_items,
        _read_spec_brief(project_id),
    )


def run_batch_ai_review_auto(project_id: str | None, batch_items: list[dict] | None):
    if not project_id or not batch_items:
        yield ""
        return
    yield from _yield_with_spinner(
        project_id,
        "batch",
        f"AGY 整批視覺覆核進行中（共 {min(len(batch_items), 12)} 張）",
        review_batch,
        project_id,
        batch_items,
        _read_spec_brief(project_id),
    )


def report_misjudgment(
    project_id: str | None,
    orig_img: Image.Image | None,
    last_pred: str,
    correct_label: str,
) -> str:
    if not project_id:
        return "⚠️ 請先登入專案帳號。"
    if orig_img is None:
        return "⚠️ 目前沒有可回報的測試圖片。"

    paths = _project_paths(project_id)
    st = _read_state(project_id)
    raw_label = (correct_label or "未填寫說明").strip() or "未填寫說明"
    safe_label = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in raw_label)[:24]
    today = _today_str()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = paths["test_uploads"] / today
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"hardcase_{safe_label}_{ts}.png"
    orig_img.save(out_path)

    # 寫入結構化佇列 HARDCASE_QUEUE.jsonl（保留完整未截斷說明與模型版本，供 Manager 巡檢防重複）
    hc_record = {
        "id": f"hc_{ts}",
        "project_id": project_id,
        "image_path": f"test_uploads/{today}/{out_path.name}",
        "model_version": st.get("version", "unknown"),
        "model_prediction": last_pred or "",
        "client_feedback": raw_label,
        "reported_at": datetime.now(timezone.utc).isoformat(),
        "status": "PENDING",
    }
    with open(paths["hardcase_queue"], "a", encoding="utf-8") as qf:
        qf.write(json.dumps(hc_record, ensure_ascii=False) + "\n")

    api, hf_repo = _get_project_hf(project_id)
    if api and hf_repo:
        try:
            api.upload_file(
                path_or_fileobj=str(out_path),
                path_in_repo=f"test_uploads/{today}/{out_path.name}",
                repo_id=hf_repo,
                repo_type="dataset",
                commit_message=f"Feedback hard case ({today}): {out_path.name}",
            )
            api.upload_file(
                path_or_fileobj=str(paths["hardcase_queue"]),
                path_in_repo="test_uploads/HARDCASE_QUEUE.jsonl",
                repo_id=hf_repo,
                repo_type="dataset",
                commit_message=f"Update HARDCASE_QUEUE ({today})",
            )
            return f"⚠️ 已將錯判圖與完整說明回報至雲端 `test_uploads/{today}/{out_path.name}`（說明：`{raw_label}`）！"
        except Exception as e:
            return f"⚠️ 本機已記錄錯判圖與佇列，但上傳 HF 失敗：{e}"

    return f"⚠️ 已記錄錯判圖與完整說明至本機 `projects/{project_id}/test_uploads/{today}/{out_path.name}`（說明：`{raw_label}`）。"


def run_batch_test(project_id: str | None, files):
    # 只要使用者重新執行整批掃描，立刻秒殺上一批還在跑的 AGY 覆核
    _cancel_agy_slot(project_id, "batch")
    if not project_id:
        return [], None, "⚠️ 請先登入專案帳號。", [], [], ""
    if not files:
        return [], None, "⚠️ 請先上傳多張圖片或 `.zip` 壓縮檔。", [], [], ""

    st = _read_state(project_id)
    stage = st.get("stage", "WAITING_UPLOAD")
    if stage == "CLOSED":
        return [], None, "📦 **此專案已驗收結案封存**，線上盲測已關閉。", [], [], ""
    if stage != "DEPLOYED":
        return (
            [],
            None,
            f"⏳ **演算法尚未部署上線**（目前進度：`{stage}` — {st.get('note', '')}），請等待工程師完成開發並上線後再進行整批盲測。",
            [],
            [],
            "",
        )

    paths = _project_paths(project_id)
    today = _today_str()
    batch_ts = datetime.now().strftime("%H%M%S")
    day_dir = paths["test_uploads"] / today
    batch_dir = day_dir / f"batch_{batch_ts}"
    vis_dir = batch_dir / "vis"
    vis_dir.mkdir(parents=True, exist_ok=True)

    imgs = _extract_images_from_files(files, batch_dir)
    if not imgs:
        return [], None, "⚠️ 未找到有效圖片。", [], [], ""

    rows = []
    headers = ["檔名", "辨識結果", "數值/分數", "耗時(秒)"]
    label_counter: Counter = Counter()
    gallery_items: list[tuple[str, str]] = []
    batch_meta: list[dict] = []

    for idx, p in enumerate(imgs):
        img_bgr = _read_bgr_unicode(p)
        if img_bgr is None:
            continue
        res = _run_detector_engine(project_id, img_bgr)
        headers = res["headers"]
        rows.append([p.name] + list(res["row_values"]))
        s_label = str(res.get("summary_label", str(res["row_values"][0])))
        label_counter[s_label] += 1

        # 另存標註預覽圖至 batch_*/vis/（原圖保持 100% 乾淨無損）
        vis_path = vis_dir / f"{idx:03d}_{p.stem}_vis.jpg"
        ok_enc, enc_buf = cv2.imencode(".jpg", res["vis_bgr"], [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        if ok_enc:
            enc_buf.tofile(str(vis_path))
            gallery_items.append((str(vis_path), f"{p.name} | {s_label}"))
            batch_meta.append({"name": p.name, "vis_path": str(vis_path), "summary": s_label})

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "AOI_Batch_Report"
    ws.append(headers)
    for r in rows:
        ws.append(r)

    report_path = day_dir / f"AOI_Report_{today}_{batch_ts}.xlsx"
    wb.save(report_path)

    dist_str = " / ".join(f"{k}: {v} 張" for k, v in label_counter.items())
    summary = f"✅ 整批掃描完成（版本：`{st.get('version', 'v1.0')}`）：共 **{len(rows)}** 張（{dist_str}）"
    ai_hint = _spinner_md(f"AGY 整批視覺覆核啟動中（共 {min(len(batch_meta), 12)} 張）", 0.0)
    return gr.update(value=rows, headers=headers), str(report_path), summary, gallery_items, batch_meta, ai_hint


HELP_GUIDE_MD = """
### 🚀 MetaVision AOI 五步驟合作與測試流程

| 步驟 | 操作位置 | 您需要做的事 | 系統與團隊會做什麼 |
| :---: | :--- | :--- | :--- |
| **1. 申請開案** | 首頁右側「線上申請帳號」 | 填寫 **客戶名稱、專案名稱、聯絡 Email** 並送出申請 | 審核開通後產生專屬帳號（`<客戶名稱>-<客戶專案>`）與獨立密碼，寄送至您的信箱（資料 100% 獨立隔離） |
| **2. 上傳樣本** | 登入 ➔ **分頁一：訓練樣本上傳區** | 選擇樣本分類（多類別或依檔名分類請選 **Auto**；良品/瑕疵請選 **OK / NG**），拖入圖片或 `.zip` 壓縮檔，**填寫白話「檢測需求說明」** 後點「**開始上傳樣本**」➔「**我已全部上傳完畢，通知分析師**」 | 系統自動解壓歸檔並觸發系統分析師逐張檢視影像特徵（光源、反光、尺度、瑕疵邊界） |
| **3. 需求確認** | **分頁二：需求討論與問答確認區 (Discuss)** | 收到通知後點「**重新整理**」檢視分析師提出的開工前確認問題，於下方文字框回覆（可夾帶補充圖片/PDF/Excel/ZIP），點「**送出回覆並通知分析師**」 | 確認所有判定規則、座標與 Excel 報表欄位後定案規格，立即交由演算法工程師訓練與驗證模型 |
| **4. 線上盲測** | **分頁三：線上盲測驗收區** | 收到演算法上線通知後點「**刷新部署狀態**」解鎖：<br>• **模式 A（單張診斷）**：拖入單張圖即時看標註框、座標與耗時<br>• **模式 B（整批盲測）**：上傳多張圖或 `.zip` 一鍵掃描並下載 **Excel 報表 (`.xlsx`)** | 演算法部署於雲端即時推論；所有盲測圖與報表皆依日期獨立存檔於您的專屬空間 |
| **5. 錯判回饋 & 交付** | **分頁三 ➔ 模式 A 下方** | 若發現單張判錯，填寫正確結果與說明並點「**⚠️ 這張判錯了，回報修正**」 | 錯判圖與說明自動進入強化修正佇列，升版（`v1.1` / `v1.2`）後通知複測；驗收滿意即可選擇離線綠色版、產線 Watchdog 或獨立雲端交付 |

---

### 💡 常見問題與小提醒 (FAQ)
- **📦 怎麼整理 `.zip` 上傳最方便？**：可直接把各類別資料夾打包成單一 `.zip`（例如 `大黑軸/`、`小黑軸/`、`綠墊/`），分頁一選 **Auto** 上傳，系統會自動保留子資料夾與檔名作為分類依據。
- **⏳ 為什麼分頁三顯示「暫未開放」？**：在樣本剛上傳或模型訓練審查期間，分頁三會暫時鎖定以防誤測空殼模型；待版本上線（`DEPLOYED`）後按「🔄 刷新部署狀態」即可解鎖。
- **🔒 我的產線圖片會被別的客戶看到嗎？**：不會。每個專案皆有獨立帳號密碼與獨立目錄隔離，任何人都無法跨專案存取您的圖檔與報表。
"""


MCP_GUIDE_MD = """
### 🤖 Remote MCP 接入說明（讓外部 AI Agent 直接操控 MetaVision AOI）

本平台原生提供標準 **Remote MCP (Streamable HTTP / JSON-RPC 2.0)** 端點，讓支援 MCP 的外部 AI Agent（如 Antigravity、Claude、Cursor、企業自動化 Agent）無須操作網頁即可直接呼叫您的專屬 AOI 模型與協作流程。

- **🌐 Remote MCP 端點網址**：`https://www.metavisionsystems.com/mcp`
- **📡 傳輸協定**：`Streamable HTTP`（JSON-RPC 2.0 via `POST /mcp`；`GET /mcp` 可查看服務狀態）
- **🔑 認證方式（與網頁登入同一組帳密，單一專案 100% 隔離）**：
  - **推薦（HTTP Header）**：`Authorization: Bearer <專案帳號>:<專屬密碼>`（例如 `Bearer TestClient-SpoolAOI:你的密碼`）
  - **備用（工具參數）**：若客戶端不便設定 Header，亦可直接於工具呼叫參數傳入 `project_id` 與 `password`

---

#### 📋 MCP 客戶端設定範例（直接複製貼上即可使用）
```json
{
  "mcpServers": {
    "metavision-aoi": {
      "url": "https://www.metavisionsystems.com/mcp",
      "headers": {
        "Authorization": "Bearer <客戶名稱>-<客戶專案>:<您的專屬密碼>"
      }
    }
  }
}
```

---

#### 🛠️ 開放給外部 AI Agent 的 7 支標準 MCP Tools

| Tool 名稱 | 權限 | 功能說明 |
| :--- | :---: | :--- |
| `aoi_request_project` | 免登入 | 線上申請開通新專案（進入人工審核，開通後寄發帳密至 Email） |
| `aoi_get_status` | 需帳密 | 查詢專案即時進度（`stage`）、部署版本（`version`）與是否有待回覆問題 |
| `aoi_upload_sample` | 需帳密 | 上傳 Base64 訓練樣本圖（`Auto` / `OK` / `NG`），可一併帶入需求說明通知分析師 |
| `aoi_get_discuss` | 需帳密 | 讀取分頁二分析師發布的待確認問題與歷史 Q&A 紀錄 |
| `aoi_reply_discuss` | 需帳密 | 替客戶回覆分頁二規格確認問題（支援夾帶 Base64 補充圖片或文件附件） |
| `aoi_detect_image` | 需帳密 | 呼叫已上線（`DEPLOYED`）之專案演算法進行單張推論（支援 `image_base64` 或公開 `image_url`），回傳結構化 JSON 類別、數量、座標與耗時（設 `return_annotated_image: true` 可同步取得標註圖） |
| `aoi_report_misjudgment` | 需帳密 | 回報盲測判錯原圖與正確說明，自動寫入錯判修正佇列觸發下一輪升版 |

---

#### ⚡ 一行指令快速測試連通性 (`curl`)
```bash
# 1. 查詢服務資訊與可用工具列表
curl -s https://www.metavisionsystems.com/mcp

# 2. 透過 MCP JSON-RPC 查詢專案狀態（替換為您的帳密）
curl -s -X POST https://www.metavisionsystems.com/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TestClient-SpoolAOI:YOUR_PASSWORD" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"aoi_get_status","arguments":{}}}'
```
"""


# === Gradio 介面 ===
with gr.Blocks(title="MetaVision AOI 全自動視覺檢測平台") as demo:
    current_project = gr.State(None)

    with gr.Accordion("📖 平台使用說明與 AOI 合作流程 (Help — 點此展開 / 收合)", open=False):
        gr.Markdown(HELP_GUIDE_MD)

    with gr.Accordion("🤖 Remote MCP 接入指南（給外部 AI Agent 連線使用 — 點此展開 / 收合）", open=False):
        gr.Markdown(MCP_GUIDE_MD)

    # --- 登入與新專案申請畫面 ---
    with gr.Column(visible=True) as auth_panel:
        gr.Markdown(
            """
            # 🔐 MetaVision AOI 客戶專案登入入口
            每個專案皆有獨立的專屬帳號（格式：**`<客戶名稱>-<客戶專案>`**）與加密密碼，確保您的產線影像資料 100% 獨立隔離。
            """
        )
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🔑 已有專案帳號？請由此登入")
                login_user = gr.Textbox(
                    label="專案帳號（<客戶名稱>-<客戶專案>）",
                    placeholder="例如：TestClient-PartsAOI",
                )
                login_pw = gr.Textbox(label="專屬密碼", type="password", placeholder="請輸入信箱收到的密碼")
                btn_login = gr.Button("🔓 登入專案", variant="primary")
                login_msg = gr.Markdown()

            with gr.Column():
                gr.Markdown("### 🆕 尚未開通專案？線上申請帳號")
                gr.Markdown("若查無您的專案帳號，請填寫以下資訊，審核開通後我們將把**專屬密碼寄送至您的 Email**。")
                req_client = gr.Textbox(label="客戶名稱（必填）", placeholder="例如：TestClient")
                req_project = gr.Textbox(label="客戶專案名稱（必填）", placeholder="例如：PartsAOI")
                req_contact = gr.Textbox(label="聯絡人姓名", placeholder="例如：王小明")
                req_email = gr.Textbox(label="聯絡 Email（必填，用於接收密碼）", placeholder="name@company.com")
                req_note = gr.Textbox(label="電話或專案簡述（選填）", placeholder="例如：0912-345-678 / 4種零件辨識")
                btn_req = gr.Button("📩 提交開案申請", variant="secondary")
                req_msg = gr.Markdown()

        btn_req.click(
            handle_project_request,
            inputs=[req_client, req_project, req_contact, req_email, req_note],
            outputs=req_msg,
        )

    # --- 專案主操作區（登入成功後顯示） ---
    with gr.Column(visible=False) as main_panel:
        with gr.Row():
            project_header = gr.Markdown()
            btn_logout = gr.Button("🚪 登出", scale=0)

        with gr.Tabs():
            with gr.Tab("📤 分頁一：訓練樣本上傳區"):
                gr.Markdown("請選擇圖片類別後，直接拖拉多張圖片或 `.zip` 壓縮檔至此。")
                sample_label = gr.Radio(
                    choices=[
                        "📦 依檔名自動分類 / 多類別樣本 (Auto)",
                        "🟢 正常良品 (OK)",
                        "🔴 瑕疵不良品 (NG)",
                    ],
                    value="📦 依檔名自動分類 / 多類別樣本 (Auto)",
                    label="樣本分類",
                )
                sample_files = gr.File(
                    label="拖拉上傳圖片或 .zip 壓縮檔（支援整批）",
                    file_count="multiple",
                    file_types=["image", ".zip"],
                )
                client_req = gr.Textbox(
                    label="📝 檢測需求說明（必填：請用白話說明您想檢測或辨識什麼）",
                    placeholder="例如：這批有 4 種零件（緣墊、大黑軸、小白、小黑軸），請幫我辨識盲測圖中是哪一種零件並標示位置與報表...",
                    lines=4,
                )
                with gr.Row():
                    btn_upload = gr.Button("⬆️ 開始上傳樣本", variant="primary")
                    btn_ready = gr.Button("✅ 我已全部上傳完畢，通知分析師", variant="secondary")
                upload_status = gr.Markdown()

                btn_upload.click(
                    upload_samples,
                    inputs=[current_project, sample_label, sample_files],
                    outputs=upload_status,
                )
                btn_ready.click(
                    notify_ready,
                    inputs=[current_project, client_req],
                    outputs=upload_status,
                )

            with gr.Tab("💬 分頁二：需求討論與問答確認區 (Discuss)"):
                gr.Markdown("分析師看完樣本後若有需要確認的細節，會顯示在下方；您可以直接文字回覆並附上圖片或文件，所有紀錄皆會自動存檔留存。")
                btn_refresh_discuss = gr.Button("🔄 重新整理最新問題與紀錄")
                gr.Markdown("### ❓ 目前待確認問題")
                discuss_questions = gr.Markdown()
                gr.Markdown("---")
                client_reply_box = gr.Textbox(
                    label="✍️ 客戶回覆內容",
                    placeholder="請逐條回覆上方問題，或補充現場拍攝條件、允收標準...",
                    lines=4,
                )
                client_reply_files = gr.File(
                    label="📎 補充圖片或文件附件（可選，支援圖片 / PDF / Word / Excel / ZIP）",
                    file_count="multiple",
                )
                btn_send_reply = gr.Button("📨 送出回覆並通知分析師", variant="primary")
                reply_status = gr.Markdown()
                gr.Markdown("### 📜 歷史討論紀錄 (Q&A LOG)")
                discuss_log_view = gr.Markdown()

                btn_refresh_discuss.click(
                    _load_discuss_views,
                    inputs=[current_project],
                    outputs=[discuss_questions, discuss_log_view],
                )
                btn_send_reply.click(
                    submit_client_reply,
                    inputs=[current_project, client_reply_box, client_reply_files],
                    outputs=[reply_status, discuss_questions, discuss_log_view],
                )

            with gr.Tab("🧪 分頁三：線上盲測驗收區"):
                with gr.Row():
                    blind_banner = gr.Markdown()
                    btn_refresh_state = gr.Button("🔄 刷新部署狀態", scale=0)
                btn_refresh_state.click(
                    _get_blind_test_banner,
                    inputs=[current_project],
                    outputs=blind_banner,
                )

                with gr.Tabs():
                    with gr.Tab("🔍 模式 A：單張精細診斷"):
                        with gr.Row():
                            test_input = gr.Image(type="pil", label="拖入單張盲測圖片")
                            test_output = gr.Image(type="pil", label="AOI 檢測標註結果")
                        test_status = gr.Markdown("請上傳圖片進行檢測。")
                        cached_orig = gr.State()
                        cached_vis = gr.State()
                        cached_pred = gr.State("")

                        with gr.Row():
                            btn_single_ai = gr.Button("🤖 請 AGY 視覺覆核這張（抓疑似漏檢／誤判，不改原判定）", variant="secondary")
                        single_ai_review = gr.Markdown()

                        test_input.change(
                            run_single_test,
                            inputs=[current_project, test_input],
                            outputs=[test_output, test_status, cached_orig, cached_vis, cached_pred, single_ai_review],
                        ).then(
                            run_single_ai_review_auto,
                            inputs=[current_project, cached_orig, cached_vis, cached_pred],
                            outputs=single_ai_review,
                        )
                        btn_single_ai.click(
                            run_single_ai_review,
                            inputs=[current_project, cached_orig, cached_vis, cached_pred],
                            outputs=single_ai_review,
                        )

                        with gr.Row():
                            fb_label = gr.Textbox(
                                label="若此張判錯，請填寫正確結果與說明（例如：應為 大黑軸 9 顆 / 左上反光不是刮痕）",
                                placeholder="例如：應為 大黑軸 / 應為 NG",
                            )
                            btn_feedback = gr.Button("⚠️ 這張判錯了，回報修正", variant="stop")
                        fb_status = gr.Markdown()
                        btn_feedback.click(
                            report_misjudgment,
                            inputs=[current_project, cached_orig, cached_pred, fb_label],
                            outputs=fb_status,
                        )

                    with gr.Tab("📦 模式 B：整批極速盲測"):
                        batch_files = gr.File(
                            label="一次上傳多張盲測圖或 .zip 壓縮檔",
                            file_count="multiple",
                            file_types=["image", ".zip"],
                        )
                        with gr.Row():
                            btn_batch = gr.Button("🚀 開始整批掃描", variant="primary")
                            btn_batch_ai = gr.Button("🤖 請 AGY 視覺覆核整批結果（自動揪出疑似錯判圖）", variant="secondary")
                        batch_summary = gr.Markdown()
                        batch_ai_review = gr.Markdown()
                        cached_batch_items = gr.State([])
                        batch_gallery = gr.Gallery(
                            label="🖼️ 整批盲測標註視覺相簿（點擊可放大檢視每張框選）",
                            columns=3,
                            height="auto",
                            object_fit="contain",
                        )
                        batch_table = gr.Dataframe(
                            headers=["檔名", "辨識結果", "數值/分數", "耗時(秒)"],
                            interactive=False,
                        )
                        batch_excel = gr.File(label="📥 下載完整盲測報告 (.xlsx)")

                        btn_batch.click(
                            run_batch_test,
                            inputs=[current_project, batch_files],
                            outputs=[batch_table, batch_excel, batch_summary, batch_gallery, cached_batch_items, batch_ai_review],
                        ).then(
                            run_batch_ai_review_auto,
                            inputs=[current_project, cached_batch_items],
                            outputs=batch_ai_review,
                        )
                        btn_batch_ai.click(
                            run_batch_ai_review,
                            inputs=[current_project, cached_batch_items],
                            outputs=batch_ai_review,
                        )

    btn_login.click(
        handle_login,
        inputs=[login_user, login_pw],
        outputs=[
            current_project,
            login_msg,
            auth_panel,
            main_panel,
            project_header,
            discuss_questions,
            discuss_log_view,
            blind_banner,
        ],
    )
    btn_logout.click(
        handle_logout,
        inputs=[current_project],
        outputs=[current_project, login_msg, auth_panel, main_panel],
    )

# === FastAPI + Remote MCP (/mcp) + AGY Bridge (/api/agy-review) + Gradio 單一入口整合 ===
fastapi_app = FastAPI(title="MetaVision AOI Portal & Remote MCP")
fastapi_app.include_router(create_mcp_router(sys.modules[__name__]))
fastapi_app.include_router(create_agy_bridge_router())
fastapi_app = gr.mount_gradio_app(fastapi_app, demo, path="/")


if __name__ == "__main__":
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=SERVER_PORT,
        log_level="info",
    )
