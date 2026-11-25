"""
MetaVision AOI — 零 Token 消耗自動巡檢推播器 (patrol_notifier.py)
- 純 Python 掃描（0 LLM Token 消耗！），由 Windows 工作排程於每日 09:00~18:00 每 30 分鐘執行一次。
- 偵測以下四種新事件並透過 notify_director.py 推播至導演 Telegram（含去重記憶 `_patrol_seen.json`，同一事件絕不重複洗版）：
  1. 新客戶申請開案 (`pending_requests/*.json`) -> 閘道 0
  2. 客戶剛上傳訓練樣本 (`STATE.json == UPLOADED`)
  3. 客戶剛於討論區回覆 (`STATE.json == CLIENT_REPLIED`)
  4. 客戶剛回報盲測錯判 (`HARDCASE_QUEUE.jsonl` 新增 `PENDING` 項目)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
PENDING_DIR = BASE_DIR / "pending_requests"
PROJECTS_ROOT = BASE_DIR / "projects"
SEEN_PATH = BASE_DIR / "_patrol_seen.json"

sys.path.insert(0, str(BASE_DIR))
from notify_director import send_telegram  # noqa: E402


def _load_seen() -> dict[str, list[str]]:
    if SEEN_PATH.exists():
        try:
            return json.loads(SEEN_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"pending": [], "states": [], "hardcases": []}


def _save_seen(seen: dict[str, list[str]]) -> None:
    SEEN_PATH.write_text(json.dumps(seen, indent=2, ensure_ascii=False), encoding="utf-8")


def run_patrol() -> int:
    seen = _load_seen()
    seen_pending = set(seen.get("pending", []))
    seen_states = set(seen.get("states", []))
    seen_hc = set(seen.get("hardcases", []))
    alerts: list[str] = []

    # 1. 新客戶開案申請 (pending_requests/)
    if PENDING_DIR.exists():
        for f in sorted(PENDING_DIR.glob("*.json")):
            key = f"{f.name}:{int(f.stat().st_mtime)}"
            if key in seen_pending:
                continue
            try:
                req = json.loads(f.read_text(encoding="utf-8"))
                pid = req.get("project_id", f.stem)
                client = req.get("client_name", "")
                proj = req.get("project_name", "")
                email = req.get("email", "")
                note = (req.get("note") or "").strip()
                alerts.append(
                    f"🆕【閘道 0 新開案申請】客戶 {client} / 專案 {proj} ({pid})\n"
                    f"Email：{email}" + (f"\n備註：{note}" if note else "") + "\n請回 Antigravity 審核 approve/reject！"
                )
                seen_pending.add(key)
            except Exception:
                continue

    # 2. 各專案狀態異動 (UPLOADED / CLIENT_REPLIED) 與新錯判回饋 (HARDCASE_QUEUE.jsonl)
    if PROJECTS_ROOT.exists():
        for pdir in sorted(p for p in PROJECTS_ROOT.iterdir() if p.is_dir()):
            pid = pdir.name
            st_file = pdir / "STATE.json"
            if st_file.exists():
                try:
                    st = json.loads(st_file.read_text(encoding="utf-8"))
                    stage = st.get("stage", "")
                    updated = st.get("updated_at", "")
                    if stage in {"UPLOADED", "CLIENT_REPLIED"}:
                        s_key = f"{pid}:{stage}:{updated}"
                        if s_key not in seen_states:
                            if stage == "UPLOADED":
                                alerts.append(
                                    f"📤【新樣本上傳】專案 {pid} 客戶已上傳訓練樣本，請回 Antigravity 派發 aoi_analyst 看圖分析！"
                                )
                            else:
                                alerts.append(
                                    f"💬【客戶回覆討論】專案 {pid} 客戶已於分頁二回覆問題，請回 Antigravity 派發 aoi_analyst 整理規格！"
                                )
                            seen_states.add(s_key)
                except Exception:
                    pass

            hc_file = pdir / "test_uploads" / "HARDCASE_QUEUE.jsonl"
            if hc_file.exists():
                try:
                    for line in hc_file.read_text(encoding="utf-8").splitlines():
                        if not line.strip():
                            continue
                        rec = json.loads(line)
                        if rec.get("status") != "PENDING":
                            continue
                        hc_id = str(rec.get("id") or rec.get("reported_at") or "")
                        hc_key = f"{pid}:{hc_id}"
                        if hc_key not in seen_hc:
                            fb = str(rec.get("client_feedback") or "")[:120]
                            alerts.append(
                                f"⚠️【盲測錯判回饋】專案 {pid} 收到新錯判回報：{fb}\n請回 Antigravity 檢視並派發修版升版！"
                            )
                            seen_hc.add(hc_key)
                except Exception:
                    pass

    sent_count = 0
    for msg in alerts:
        try:
            send_telegram(msg)
            sent_count += 1
        except Exception as exc:
            print(f"Telegram push failed: {exc}", file=sys.stderr)

    _save_seen(
        {
            "pending": sorted(seen_pending),
            "states": sorted(seen_states),
            "hardcases": sorted(seen_hc),
        }
    )
    print(f"Patrol done: {len(alerts)} new alert(s), {sent_count} sent.")
    return sent_count


if __name__ == "__main__":
    run_patrol()
