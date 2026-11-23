"""
MetaVision AOI 多專案管理與審核工具 (manage_project.py)
用法：
  python manage_project.py list                                                # 檢視待審核申請、專案狀態看板與待處理 Hardcases
  python manage_project.py approve <客戶名稱>-<客戶專案> [自訂密碼]           # 審核通過、產生密碼、建目錄並寫入稽核日誌
  python manage_project.py reject <客戶名稱>-<客戶專案> [原因]                # 拒絕開案申請並寫入永久稽核日誌
  python manage_project.py create <客戶名稱> <客戶專案> <email> [自訂密碼]    # 由管理員直接建立新專案（不覆蓋既有專案）
"""

import json
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
REGISTRY_PATH = BASE_DIR / "projects_registry.json"
PENDING_DIR = BASE_DIR / "pending_requests"
PROJECTS_ROOT = BASE_DIR / "projects"
AUDIT_LOG_PATH = BASE_DIR / "request_audit_log.jsonl"

PENDING_DIR.mkdir(parents=True, exist_ok=True)
PROJECTS_ROOT.mkdir(parents=True, exist_ok=True)


def _sanitize_id(s: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff\-]", "", (s or "").strip())


def _load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {}


def _save_registry(reg: dict) -> None:
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def _gen_password(length: int = 10) -> str:
    alphabet = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _append_audit(event: str, data: dict) -> None:
    record = {
        "event": event,
        "logged_at": datetime.now(timezone.utc).isoformat(),
        **data,
    }
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as af:
        af.write(json.dumps(record, ensure_ascii=False) + "\n")


def _init_project_dirs(project_id: str) -> None:
    pdir = PROJECTS_ROOT / project_id
    for sub in (
        pdir / "data" / "raw" / "OK",
        pdir / "data" / "raw" / "NG",
        pdir / "data" / "raw" / "Auto",
        pdir / "ANALYST",
        pdir / "CODER" / "eval_outputs",
        pdir / "test_uploads",
    ):
        sub.mkdir(parents=True, exist_ok=True)

    state_path = pdir / "STATE.json"
    if not state_path.exists():
        state_path.write_text(
            json.dumps(
                {
                    "project_id": project_id,
                    "stage": "WAITING_UPLOAD",
                    "version": "未部署",
                    "note": "專案已開通，等待客戶上傳訓練樣本與檢測需求",
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )


def _count_pending_hardcases(project_id: str) -> int:
    q_path = PROJECTS_ROOT / project_id / "test_uploads" / "HARDCASE_QUEUE.jsonl"
    if not q_path.exists():
        return 0
    cnt = 0
    for line in q_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            if json.loads(line).get("status") == "PENDING":
                cnt += 1
        except Exception:
            pass
    return cnt


def cmd_list() -> None:
    print("=== 🆕 待審核開案申請 (pending_requests/) ===")
    pending_files = sorted(PENDING_DIR.glob("*.json"))
    if not pending_files:
        print("  (無待審核申請)")
    for pf in pending_files:
        data = json.loads(pf.read_text(encoding="utf-8"))
        print(
            f"  - {data.get('project_id')} | Email: {data.get('email')} | "
            f"聯絡人: {data.get('contact', '-')} | 申請時間: {data.get('requested_at', '')[:19]}"
        )

    print("\n=== 📊 已開通專案進度看板 (projects_registry.json) ===")
    reg = _load_registry()
    if not reg:
        print("  (尚無已開通專案)")
    for pid, info in reg.items():
        st_path = PROJECTS_ROOT / pid / "STATE.json"
        stage, ver = "UNKNOWN", "-"
        if st_path.exists():
            st = json.loads(st_path.read_text(encoding="utf-8"))
            stage = st.get("stage", "UNKNOWN")
            ver = st.get("version", "-")
        hc_pending = _count_pending_hardcases(pid)
        hc_tag = f" | ⚠️ 待處理錯判: {hc_pending}" if hc_pending > 0 else ""
        print(f"  - {pid} | 狀態: {stage} | 版本: {ver}{hc_tag} | Email: {info.get('email', '-')}")


def cmd_approve(project_id: str, custom_pw: str | None = None) -> None:
    pf = PENDING_DIR / f"{project_id}.json"
    if not pf.exists():
        print(f"❌ 找不到待審核申請：{pf}")
        sys.exit(1)

    req = json.loads(pf.read_text(encoding="utf-8"))
    reg = _load_registry()
    pw = custom_pw or _gen_password()
    reg[project_id] = {
        "password": pw,
        "client_name": req.get("client_name", ""),
        "project_title": req.get("project_title", ""),
        "email": req.get("email", ""),
        "contact": req.get("contact", ""),
        "phone_or_note": req.get("phone_or_note", ""),
        "hf_repo_id": req.get("hf_repo_id", ""),
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_registry(reg)
    _init_project_dirs(project_id)
    _append_audit("APPROVED", {"project_id": project_id, "email": req.get("email", ""), "contact": req.get("contact", "")})
    pf.unlink()

    print(f"✅ 已核准開通專案：{project_id}")
    print(f"   收件 Email：{req.get('email')}")
    print(f"   登入帳號  ：{project_id}")
    print(f"   專屬密碼  ：{pw}")
    print(f"   專案目錄  ：{PROJECTS_ROOT / project_id}")


def cmd_reject(project_id: str, reason: str = "未通過審核") -> None:
    pf = PENDING_DIR / f"{project_id}.json"
    if not pf.exists():
        print(f"❌ 找不到待審核申請：{pf}")
        sys.exit(1)

    req = json.loads(pf.read_text(encoding="utf-8"))
    _append_audit(
        "REJECTED",
        {
            "project_id": project_id,
            "email": req.get("email", ""),
            "contact": req.get("contact", ""),
            "reason": reason,
        },
    )
    pf.unlink()
    print(f"🚫 已拒絕申請：{project_id}（原因：{reason}），已永久留存於 request_audit_log.jsonl")


def cmd_create(client_name: str, project_title: str, email: str, custom_pw: str | None = None) -> None:
    c_clean = _sanitize_id(client_name)
    p_clean = _sanitize_id(project_title)
    if not c_clean or not p_clean:
        print("❌ 客戶名稱與專案名稱不可為空或僅含特殊字元。")
        sys.exit(1)

    project_id = f"{c_clean}-{p_clean}"
    reg = _load_registry()
    if project_id in reg:
        print(f"❌ 專案帳號 {project_id} 已存在，為避免誤覆蓋密碼已中止建立。")
        sys.exit(1)

    pw = custom_pw or _gen_password()
    reg[project_id] = {
        "password": pw,
        "client_name": c_clean,
        "project_title": p_clean,
        "email": email.strip(),
        "contact": "",
        "phone_or_note": "Admin created",
        "hf_repo_id": "",
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_registry(reg)
    _init_project_dirs(project_id)
    _append_audit("CREATED", {"project_id": project_id, "email": email.strip(), "source": "admin_cli"})
    print(f"✅ 已建立專案：{project_id} | 密碼：{pw} | Email：{email}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    action = sys.argv[1].lower()
    if action == "list":
        cmd_list()
    elif action == "approve" and len(sys.argv) >= 3:
        cmd_approve(sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else None)
    elif action == "reject" and len(sys.argv) >= 3:
        cmd_reject(sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else "未通過審核")
    elif action == "create" and len(sys.argv) >= 5:
        cmd_create(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) >= 6 else None)
    else:
        print(__doc__)
        sys.exit(1)
