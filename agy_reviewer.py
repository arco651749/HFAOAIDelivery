"""
MetaVision AOI — AGY 獨立視覺覆核引擎 (agy_reviewer.py)
- 本機模式：以可中斷 `subprocess.Popen` 呼叫本機 `agy.exe`（沙盒唯讀 `--sandbox`，免 GOOGLE_API_KEY，直接走 Antigravity 額度）對比原圖與標註圖做視覺覆核。
- 即時取消與防洩漏：支援 `cancel_event`，當客戶關閉瀏覽器分頁（GeneratorExit）、重新上傳新圖、或遠端斷線時，於 0.2 秒內透過 Windows `taskkill /F /T /PID` 秒殺整棵 `agy.exe` 子行程樹並回收暫存檔，絕不白燒額度。
- 雲端橋接模式（未來部署於 Hugging Face Space 時）：設定環境變數 `AGY_BRIDGE_URL` + `AGY_BRIDGE_TOKEN`，雲端點按鈕後自動透過 HTTPS 將縮圖與摘要回傳至本機 `/api/agy-review` 呼叫本機 `agy.exe`；若本機關機或離線則優雅提示「AGY 覆核員離線中」，絕不影響純程式檢測。
"""

from __future__ import annotations

import asyncio
import base64
import hmac
import io
import json
import os
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from PIL import Image

BASE_DIR = Path(__file__).parent.resolve()
TMP_REVIEW_ROOT = BASE_DIR / "_agy_review_tmp"
REVIEWER_SOP_PATH = BASE_DIR / "AI_REVIEWER_SOP.md"
AGY_REVIEW_MODEL = "gemini-4-hydrogen-low"
MAX_CONCURRENT_AGY = threading.Semaphore(2)
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def _read_env_var(name: str, default: str = "") -> str:
    return (os.getenv(name) or "").strip() or default


def find_agy_binary() -> str | None:
    custom = _read_env_var("AGY_BIN")
    if custom and Path(custom).exists():
        return custom
    found = shutil.which("agy") or shutil.which("agy.exe")
    if found:
        return found
    candidates = [
        Path(os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe")),
        Path(r"D:\Users\arco0\AppData\Local\agy\bin\agy.exe"),
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


def pil_to_jpeg_bytes(img: Image.Image, max_width: int = 1024, quality: int = 86) -> bytes:
    rgb = img.convert("RGB")
    if rgb.width > max_width:
        nh = int(rgb.height * (max_width / rgb.width))
        rgb = rgb.resize((max_width, max(1, nh)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    rgb.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def _terminate_proc_tree(proc: subprocess.Popen) -> None:
    """強制終止 agy.exe 及其所有子行程（Windows 採 taskkill /F /T /PID 防孤兒行程）。"""
    if proc.poll() is not None:
        return
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
                creationflags=CREATE_NO_WINDOW,
            )
        else:
            proc.terminate()
    except Exception:
        pass
    try:
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=3)
    except Exception:
        pass


def _acquire_slot_cancellable(
    cancel_event: threading.Event | None,
    wait_limit: float = 20.0,
) -> tuple[bool, bool]:
    """回傳 (acquired, cancelled)。等待併發名額期間若觸發取消則立即放棄，不啟動 agy.exe。"""
    deadline = time.perf_counter() + wait_limit
    while time.perf_counter() < deadline:
        if cancel_event is not None and cancel_event.is_set():
            return False, True
        if MAX_CONCURRENT_AGY.acquire(timeout=0.2):
            if cancel_event is not None and cancel_event.is_set():
                MAX_CONCURRENT_AGY.release()
                return False, True
            return True, False
    return False, False


def _run_local_agy_on_files(
    work_dir: Path,
    prompt: str,
    model: str | None = None,
    timeout_sec: int = 150,
    cancel_event: threading.Event | None = None,
) -> tuple[bool, str, str]:
    agy_bin = find_agy_binary()
    if not agy_bin:
        return False, "", "🤖 本機未偵測到 `agy.exe`，AGY 視覺覆核員暫時離線，請直接參考上方純程式判定結果。"

    use_model = (model or AGY_REVIEW_MODEL).strip() or AGY_REVIEW_MODEL
    cmd = [
        agy_bin,
        "-p",
        prompt,
        "--model",
        use_model,
        "--output-format",
        "text",
        "--sandbox",
        "--disable-slash-commands",
        "--print-timeout",
        f"{timeout_sec}s",
        "--add-dir",
        str(work_dir),
    ]

    acquired, cancelled = _acquire_slot_cancellable(cancel_event, wait_limit=20.0)
    if cancelled:
        return False, use_model, "🛑 已取消本次 AGY 視覺覆核。"
    if not acquired:
        return False, use_model, "⏳ AGY 視覺覆核員目前忙碌中（已有其他覆核任務執行中），請稍後再試。"

    stdout_path = work_dir / "_agy_stdout.txt"
    stderr_path = work_dir / "_agy_stderr.txt"
    proc: subprocess.Popen | None = None
    try:
        with open(stdout_path, "wb") as f_out, open(stderr_path, "wb") as f_err:
            proc = subprocess.Popen(
                cmd,
                cwd=str(work_dir),
                stdin=subprocess.DEVNULL,
                stdout=f_out,
                stderr=f_err,
                creationflags=CREATE_NO_WINDOW,
            )
            deadline = time.perf_counter() + timeout_sec + 15
            while proc.poll() is None:
                if cancel_event is not None and cancel_event.is_set():
                    _terminate_proc_tree(proc)
                    return False, use_model, "🛑 已取消先前的 AGY 視覺覆核任務。"
                if time.perf_counter() > deadline:
                    _terminate_proc_tree(proc)
                    return False, use_model, "⏳ 本機 AGY 視覺覆核逾時，請直接參考上方純程式判定結果。"
                time.sleep(0.2)

        rc = proc.returncode
        out = stdout_path.read_text(encoding="utf-8", errors="replace").strip() if stdout_path.exists() else ""
        err = stderr_path.read_text(encoding="utf-8", errors="replace").strip() if stderr_path.exists() else ""
        if rc == 0 and out:
            return True, use_model, out
        detail = (err or out or f"exit_code={rc}")[:300]
        return False, use_model, f"⚠️ 本機 AGY 覆核執行異常（請直接參考純程式判定結果）：\n\n`{detail}`"
    except Exception as exc:
        if proc is not None:
            _terminate_proc_tree(proc)
        return False, use_model, f"⚠️ 無法啟動本機 AGY（{exc}），請直接參考純程式判定結果。"
    finally:
        if proc is not None and proc.poll() is None:
            _terminate_proc_tree(proc)
        MAX_CONCURRENT_AGY.release()


def _call_remote_bridge(
    payload: dict[str, Any],
    cancel_event: threading.Event | None = None,
) -> tuple[bool, str, str]:
    bridge_url = _read_env_var("AGY_BRIDGE_URL").rstrip("/")
    bridge_token = _read_env_var("AGY_BRIDGE_TOKEN")
    if not bridge_url:
        return False, "", ""

    endpoint = bridge_url if bridge_url.endswith("/api/agy-review") else f"{bridge_url}/api/agy-review"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "MetaVisionAOI-BridgeClient/1.0",
    }
    if bridge_token:
        headers["X-Bridge-Token"] = bridge_token

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    if cancel_event is not None and cancel_event.is_set():
        return False, "", "🛑 已取消本次遠端 AGY 覆核。"
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("ok"):
            return True, str(data.get("model", AGY_REVIEW_MODEL)), str(data.get("review_md", ""))
        return False, str(data.get("model", "")), str(data.get("error", "遠端 AGY 覆核回傳失敗"))
    except urllib.error.URLError:
        return False, "", "🤖 本機 AGY 視覺覆核員目前離線中（無法連線回主機），請直接參考上方純程式判定結果。"
    except Exception as exc:
        return False, "", f"🤖 連線至本機 AGY 覆核員失敗（{exc}），請直接參考上方純程式判定結果。"


def _execute_review_payload_locally(
    payload: dict[str, Any],
    cancel_event: threading.Event | None = None,
) -> tuple[bool, str, str]:
    mode = str(payload.get("mode") or "single")
    project_id = str(payload.get("project_id") or "unknown")
    spec_brief = str(payload.get("spec_brief") or "").strip()
    items = payload.get("images") or []
    if not items:
        return False, "", "⚠️ 未收到任何待覆核圖片。"

    TMP_REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    work_dir = TMP_REVIEW_ROOT / f"rev_{uuid.uuid4().hex[:10]}"
    work_dir.mkdir(parents=True, exist_ok=True)

    try:
        sop_copy = work_dir / "AI_REVIEWER_SOP.md"
        if REVIEWER_SOP_PATH.exists():
            sop_copy.write_text(REVIEWER_SOP_PATH.read_text(encoding="utf-8"), encoding="utf-8")

        spec_path = work_dir / "SPEC_BRIEF.md"
        if spec_brief:
            spec_path.write_text(spec_brief, encoding="utf-8")

        saved_entries: list[dict[str, str]] = []
        for idx, it in enumerate(items):
            raw = base64.b64decode(str(it["b64"]))
            tag = str(it.get("tag") or f"img_{idx+1}")
            fname = f"{idx+1:02d}_{tag}.jpg"
            p = work_dir / fname
            p.write_bytes(raw)
            saved_entries.append(
                {
                    "file": str(p),
                    "name": str(it.get("name") or fname),
                    "summary": str(it.get("summary") or ""),
                    "role": str(it.get("role") or "vis"),
                }
            )

        sop_hint = (
            f"請先用 `read_file` 讀取並嚴格遵守 `{sop_copy}` 的覆核準則、細心親切語氣、後續處理承諾與標準回覆格式，"
            if sop_copy.exists()
            else ""
        )

        if mode == "single":
            orig_f = saved_entries[0]["file"]
            vis_f = saved_entries[1]["file"] if len(saved_entries) > 1 else saved_entries[0]["file"]
            pred_summary = str(payload.get("pred_summary") or "")
            spec_hint = f"以及專案規格摘要 `{spec_path}`，" if spec_brief else ""
            prompt = (
                f"你是 MetaVision AOI 的客戶盲測視覺覆核解說員 (`aoi_reviewer`)。\n"
                f"{sop_hint}再以 `read_file` 依序仔細檢視原圖 `{orig_f}`、純程式標註結果圖 `{vis_f}`，{spec_hint}\n"
                f"本次專案為 `{project_id}`，純程式判定摘要為：`{pred_summary}`。\n"
                "請依循「模式 A：單張精細視覺覆核」格式，以親切細心的繁體中文直接回覆客戶（切勿提及任何本機暫存路徑或內部系統細節）。"
            )
            return _run_local_agy_on_files(work_dir, prompt, timeout_sec=120, cancel_event=cancel_event)

        # Batch mode
        lines = "\n".join(
            f"- 圖 {i+1}：路徑 `{e['file']}`｜檔名 `{e['name']}`｜純程式判定 `{e['summary']}`"
            for i, e in enumerate(saved_entries)
        )
        spec_hint = f"並讀取專案規格摘要 `{spec_path}`，" if spec_brief else ""
        prompt = (
            f"你是 MetaVision AOI 的客戶盲測視覺覆核解說員 (`aoi_reviewer`)。\n"
            f"{sop_hint}{spec_hint}再用 `read_file` 逐張細心檢視以下 {len(saved_entries)} 張專案 `{project_id}` 的純程式標註結果圖：\n"
            f"{lines}\n\n"
            "請依循「模式 B：整批盲測視覺覆核」格式，以親切細心的繁體中文直接回覆客戶（切勿提及任何本機暫存路徑或內部系統細節）。"
        )
        return _run_local_agy_on_files(work_dir, prompt, timeout_sec=180, cancel_event=cancel_event)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def review_single(
    project_id: str,
    orig_img: Image.Image,
    vis_img: Image.Image,
    pred_summary: str,
    spec_brief: str = "",
    cancel_event: threading.Event | None = None,
) -> str:
    payload = {
        "mode": "single",
        "project_id": project_id,
        "pred_summary": pred_summary,
        "spec_brief": spec_brief,
        "images": [
            {"tag": "orig", "role": "orig", "b64": base64.b64encode(pil_to_jpeg_bytes(orig_img)).decode("ascii")},
            {"tag": "vis", "role": "vis", "b64": base64.b64encode(pil_to_jpeg_bytes(vis_img)).decode("ascii")},
        ],
    }
    t0 = time.perf_counter()
    if _read_env_var("AGY_BRIDGE_URL"):
        ok, model_used, text = _call_remote_bridge(payload, cancel_event=cancel_event)
        source_tag = "遠端回呼本機 AGY"
    else:
        ok, model_used, text = _execute_review_payload_locally(payload, cancel_event=cancel_event)
        source_tag = "本機 AGY"
    dt = time.perf_counter() - t0
    if not ok:
        return text
    return f"#### 🤖 AGY 視覺覆核報告（{source_tag}｜模型：`{model_used}`｜耗時 `{dt:.1f}s`｜僅供覆核參考，不改原判定）\n\n{text}"


def review_batch(
    project_id: str,
    batch_items: list[dict[str, Any]],
    spec_brief: str = "",
    max_imgs: int = 12,
    cancel_event: threading.Event | None = None,
) -> str:
    selected = batch_items[:max_imgs]
    images_payload: list[dict[str, str]] = []
    for idx, it in enumerate(selected):
        vp = Path(it["vis_path"])
        if not vp.exists():
            continue
        with Image.open(vp) as im:
            images_payload.append(
                {
                    "tag": f"batch_{idx+1:02d}",
                    "name": str(it["name"]),
                    "summary": str(it["summary"]),
                    "role": "vis",
                    "b64": base64.b64encode(pil_to_jpeg_bytes(im, max_width=960, quality=82)).decode("ascii"),
                }
            )
    if not images_payload:
        return "⚠️ 找不到可覆核的批次標註圖。"

    payload = {
        "mode": "batch",
        "project_id": project_id,
        "spec_brief": spec_brief,
        "images": images_payload,
    }
    t0 = time.perf_counter()
    if _read_env_var("AGY_BRIDGE_URL"):
        ok, model_used, text = _call_remote_bridge(payload, cancel_event=cancel_event)
        source_tag = "遠端回呼本機 AGY"
    else:
        ok, model_used, text = _execute_review_payload_locally(payload, cancel_event=cancel_event)
        source_tag = "本機 AGY"
    dt = time.perf_counter() - t0
    if not ok:
        return text
    extra = f"\n\n*(註：本批共 {len(batch_items)} 張，本次 AGY 抽檢前 {len(selected)} 張。)*" if len(batch_items) > max_imgs else ""
    return f"#### 🤖 AGY 整批視覺覆核報告（{source_tag}｜模型：`{model_used}`｜耗時 `{dt:.1f}s`｜僅供覆核參考，不改 Excel 結果）\n\n{text}{extra}"


def create_agy_bridge_router() -> APIRouter:
    """供未來 Hugging Face Space 雲端站點透過安全 Token 回呼這台電腦跑 `agy.exe` 的橋接端點（含斷線自動中止）。"""
    router = APIRouter()

    @router.get("/api/agy-review/health")
    async def agy_health():
        return JSONResponse(
            {
                "agy_available": find_agy_binary() is not None,
                "bridge_enabled": bool(_read_env_var("AGY_BRIDGE_TOKEN")),
                "model": AGY_REVIEW_MODEL,
            }
        )

    @router.post("/api/agy-review")
    async def agy_bridge_review(request: Request):
        expected_token = _read_env_var("AGY_BRIDGE_TOKEN")
        if not expected_token:
            return JSONResponse(
                {"ok": False, "error": "本機尚未設定 AGY_BRIDGE_TOKEN，遠端橋接端點預設關閉。"},
                status_code=403,
            )
        got_token = (request.headers.get("x-bridge-token") or "").strip()
        if not got_token or not hmac.compare_digest(got_token, expected_token):
            return JSONResponse({"ok": False, "error": "Bridge Token 驗證失敗"}, status_code=401)

        try:
            payload = await request.json()
        except Exception:
            return JSONResponse({"ok": False, "error": "Invalid JSON"}, status_code=400)

        cancel_evt = threading.Event()
        task = asyncio.create_task(asyncio.to_thread(_execute_review_payload_locally, payload, cancel_evt))
        try:
            while not task.done():
                if await request.is_disconnected():
                    cancel_evt.set()
                    break
                await asyncio.sleep(0.3)
            ok, model_used, text = await task
        finally:
            cancel_evt.set()

        if ok:
            return JSONResponse({"ok": True, "model": model_used, "review_md": text})
        return JSONResponse({"ok": False, "model": model_used, "error": text}, status_code=503)

    return router
