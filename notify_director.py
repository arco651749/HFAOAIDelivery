"""
MetaVision AOI 導演 Telegram 即時推播工具 (notify_director.py)
自動從本專案目錄之 AGENTS.md 讀取 TELEGRAM_BOT_TOKEN 與 TELEGRAM_CHAT_ID（絕不將 Token 寫死於程式碼中）。
用法：
  python notify_director.py "欲推播給導演的訊息內容"
  python notify_director.py --sync-chat-id   # 僅從 getUpdates 同步導演 Chat ID 並寫回 AGENTS.md
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
AGENTS_MD = BASE_DIR / "AGENTS.md"


def _read_config() -> tuple[str, str]:
    if not AGENTS_MD.exists():
        raise FileNotFoundError(f"找不到 {AGENTS_MD}，請先確認專案專屬 AGENTS.md 是否存在。")
    txt = AGENTS_MD.read_text(encoding="utf-8")
    m_tok = re.search(r"TELEGRAM_BOT_TOKEN\*\*:\s*`([^`]+)`", txt)
    m_cid = re.search(r"TELEGRAM_CHAT_ID\*\*:\s*`([^`]+)`", txt)
    token = m_tok.group(1).strip() if m_tok else ""
    chat_id = m_cid.group(1).strip() if m_cid else ""
    return token, chat_id


def _save_chat_id(chat_id: str) -> None:
    txt = AGENTS_MD.read_text(encoding="utf-8")
    new_txt = re.sub(
        r"(TELEGRAM_CHAT_ID\*\*:\s*`)[^`]+(`)",
        rf"\g<1>{chat_id}\g<2>",
        txt,
    )
    AGENTS_MD.write_text(new_txt, encoding="utf-8")


def _fetch_chat_id(token: str) -> str | None:
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode("utf-8"))
    for upd in reversed(data.get("result", [])):
        msg = upd.get("message") or upd.get("edited_message") or {}
        chat = msg.get("chat") or {}
        if "id" in chat:
            return str(chat["id"])
    return None


def send_telegram(message: str) -> dict:
    token, chat_id = _read_config()
    if not token:
        raise RuntimeError("AGENTS.md 中缺少 TELEGRAM_BOT_TOKEN。")

    if not chat_id or chat_id == "PENDING_FIRST_MESSAGE":
        fetched = _fetch_chat_id(token)
        if not fetched:
            raise RuntimeError(
                "尚未取得導演的 Telegram Chat ID。請先在手機點開 https://t.me/HFAOAIDelivery_bot 按 Start 或傳送任意訊息後重試。"
            )
        chat_id = fetched
        _save_chat_id(chat_id)
        print(f"✅ 已自動取得並儲存 TELEGRAM_CHAT_ID: {chat_id}")

    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        method="POST",
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
    if not resp.get("ok"):
        raise RuntimeError(f"Telegram API 回傳錯誤：{resp}")
    return resp


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    if sys.argv[1] == "--sync-chat-id":
        tok, _ = _read_config()
        cid = _fetch_chat_id(tok)
        if cid:
            _save_chat_id(cid)
            print(f"✅ 已同步 TELEGRAM_CHAT_ID = {cid}")
        else:
            print("⚠️ 尚未收到訊息，請先對 @HFAOAIDelivery_bot 按 Start 或傳送一句 hi。")
            sys.exit(1)
    else:
        text = " ".join(sys.argv[1:])
        res = send_telegram(text)
        print(f"✅ Telegram 推播已送出 (message_id={res['result']['message_id']})")
