---
title: MetaVision AOI
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🔍 MetaVision AOI — 多專案視覺檢測協作與遠端 MCP 平台

- **Web Portal (`/`)**：多專案帳密隔離、三分頁協作（樣本上傳 → 需求討論 → 線上盲測與 Excel 報表）。
- **Remote MCP (`/mcp`)**：標準 MCP Streamable HTTP (`2025-03-26`)，支援外部 AI Agent 透過 `Authorization: Bearer <project_id>:<password>` 安全呼叫專案推論與協作。
- **AGY 獨立視覺覆核 (`aoi_reviewer`)**：本機直跑或透過 `AGY_BRIDGE_URL` + `AGY_BRIDGE_TOKEN` 安全回呼本機 `agy.exe` 執行唯讀目視覆核。

### Hugging Face Space Secrets 設定（部署上雲時於 Space Settings 填寫）
- `HF_TOKEN`：用於同步專案樣本與盲測紀錄至 Private Dataset
- `AGY_BRIDGE_URL`：本機回呼位址（例如 `https://www.metavisionsystems.com`）
- `AGY_BRIDGE_TOKEN`：與本機一致的遠端橋接密鑰
