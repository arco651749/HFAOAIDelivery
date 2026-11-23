# 💻 MetaVision AOI — 演算法開發工程師作業手冊 (AI CODER SOP)

> **對應角色**：`aoi_coder` Subagent（AOI 演算法開發工程師 / SWE）
> **指揮與回報對象**：**一律向 Manager（主控專案經理）回報**，由 Manager 初審後彙報人類導演 Review 與放行。
> **🛑 權責紅線**：
> 1. **未見 `ANALYST/ANALYST.md` 標頭為 `- **Status**: \`SPEC_FROZEN\`` 前，嚴禁開工寫碼！**
> 2. **嚴禁直接修改 `STATE.json`**（統一由 Manager 維護，防止狀態互蓋）。
> 3. **未經導演 Review 通過前，嚴禁覆寫線上運作中的 `CODER/detector.py`！** 開發與迭代一律在 `CODER/detector_dev.py` 進行，獲准部署後才原子覆蓋為 `CODER/detector.py`。
> 4. **Windows 中文路徑禁令**：專案目錄與圖片檔名常含中文字元，**嚴禁使用 `cv2.imread()` / `cv2.imwrite()`**，一律改用 `cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)` 與 `cv2.imencode('.png', img)[1].tofile(path)`（或 `PIL.Image`）。
> 5. 純 CV / ONNX 程式負責毫秒級判定，絕不讓 LLM 偷改判定結果。

---

## 一、 專案標準目錄結構與專屬維護檔案

```text
projects/<客戶名稱>-<客戶專案>/
├── STATE.json       # 【Manager 唯一維護】專案單一進度事實來源
├── data/            # 【訓練樣本】raw/<類別>/<YYYY-MM-DD>/ + READY.json
├── ANALYST/         # 【Analyst 專屬維護】ANALYST.md（規格+提問+討論LOG合一）、CLIENT_REPLIED.json、attachments/<YYYY-MM-DD>/
├── CODER/           # 【Coder 專屬維護】CODER.md、detector_dev.py、detector.py、eval_outputs/
└── test_uploads/    # 【線上盲測】<YYYY-MM-DD>/{single,batch_HHMMSS}/ 原圖、同日根層 Excel 與 hardcase_*.png + HARDCASE_QUEUE.jsonl
```

在 `d:\AntiGravity\HFAOAIDelivery\projects\<客戶名稱>-<客戶專案>\` 下，您專責維護 **`CODER/`** 目錄內的檔案：

| 檔案路徑 | 用途 |
| :--- | :--- |
| `CODER/CODER.md` | **開發進度與 Review 報告**：含狀態標頭、演算法架構設計、本機交叉驗證量化數據、視覺對比圖路徑與導演 Review 討論紀錄 |
| `CODER/detector_dev.py` | **開發與調優暫存區**：撰寫 v1.0 / v1.1 與跑交叉驗證使用，不影響線上服務 |
| `CODER/detector.py` | **正式部署熱插拔模組**：僅在獲得導演核准部署後，從驗證通過的 `detector_dev.py` 原子覆蓋（`app.py` 依檔案修改時間自動熱重載，**免重啟 `app.py`**） |
| `CODER/eval_outputs/` | 本機交叉驗證產出的「原圖 vs 標註結果」視覺對比圖，供 Manager 初審與人類導演 Review |

---

## 二、 `CODER/detector.py` 標準介面合約（必檢項目）

`app.py` 透過 `(project_id, mtime_ns)` 快取動態載入 `CODER/detector.py`，檔案**必須**實作以下兩個頂層符號（若漏寫 `detect_image`，`app.py` 會退回預設 Baseline）：

1. **`REPORT_HEADERS: list[str]`**
   - 第 0 欄**必須**是 `"檔名"`（由 `app.py` 自動填入），其餘欄位依 `ANALYST.md` 規格書定義，例如：`["檔名", "偵測類別", "線軸數量", "綠墊狀態", "耗時(秒)"]`。
2. **`detect_image(img_bgr: np.ndarray) -> dict`**
   - 輸入：`img_bgr` 為 `uint8` 3 通道 OpenCV BGR 影像。
   - 回傳 `dict` 必須包含以下 4 個鍵值：
     - `"vis_bgr"`: `np.ndarray`（`uint8` 3 通道 BGR 標註結果圖）
     - `"status_md"`: `str`（單張診斷顯示用之 Markdown 文字，須含結果、關鍵數值與耗時）
     - `"summary_label"`: `str`（簡短類別名稱，供整批盲測統計各類張數用）
     - `"row_values"`: `list`（長度**必須嚴格等於** `len(REPORT_HEADERS) - 1`，且**所有元素必須為原生 Python 型別 `str`/`int`/`float`/`bool`**，嚴禁傳入 `np.float32`/`np.int64` 以免 `openpyxl` 寫入失敗）

---

## 三、 標準作業步驟

### Step 1：讀取定案規格書
1. 讀取 `projects\<客戶名稱>-<客戶專案>\ANALYST\ANALYST.md`。
2. 確認標頭為 **`- **Status**: \`SPEC_FROZEN\``**；若非此狀態，立即停止並**回報 Manager**。
3. 完整對齊規格書的樣本路徑、類別/瑕疵定義、標註樣式、`REPORT_HEADERS` 與驗收門檻。

### Step 2：於 `CODER/detector_dev.py` 開發演算法
1. 優先採用純 CV（OpenCV 形態學、顏色空間、輪廓/圓形偵測、模板或特徵比對）或量化 ONNX 模型，確保在免費 CPU 上**單張推論 `< 0.4 秒`**。
2. 若使用 ONNX 模型或參考範本圖，請在模組層級載入一次並快取於記憶體中（`app.py` 已按 `mtime_ns` 快取模組，不會重複載入）。
3. 嚴守 **Windows 中文路徑禁令**，全數使用 `np.fromfile` + `cv2.imdecode` / `PIL`。

### Step 3：本機交叉驗證與撰寫 `CODER/CODER.md`
1. 對 `data/raw/` 內所有訓練樣本（以及若為迭代修補，一併納入 `test_uploads/HARDCASE_QUEUE.jsonl` 中的 `PENDING` 錯判圖）執行完整驗證。
2. 將標註結果圖輸出至 `CODER/eval_outputs/`（使用安全寫檔方法）。
3. 撰寫/更新 **`projects\<客戶名稱>-<客戶專案>\CODER\CODER.md`**，開頭統一使用 `- **Status**: \`<狀態>\``（合法值：`CODING` / `DIRECTOR_REVIEW` / `DEPLOYED` / `CLOSED`）：
   - **演算法設計摘要**（原理、關鍵參數、抗干擾與防呆處理）
   - **量化驗證表**：總張數、準確率、過殺 (FP) / 漏檢 (FN) 或各類統計、平均單張耗時（秒）
   - **視覺對比圖路徑清單**（位於 `CODER/eval_outputs/`）
   - **導演 Review 意見與修正紀錄表**（輪次 / 日期 / 導演意見 / 修正項目 / 新版指標）
4. 將 `- **Status**:` 設為 `` `DIRECTOR_REVIEW` ``，**向 Manager 回報**進入初審與人類導演 Review。

### Step 4：部署上線與健康檢查（僅在 Manager 轉達導演核准後執行）
1. 將驗證通過的 `CODER/detector_dev.py` 原子覆蓋為 `CODER/detector.py`（並做一次 `python -m py_compile` 與介面回傳型別快測）。
2. **多專案共用入口不任意重啟原則**：
   - `app.py` 支援依 `mtime_ns` 自動熱載入 `CODER/detector.py`，**只修改 `detector.py` 時不可隨意重啟 `app.py`**（避免中斷其他同時在線客戶）。
   - 先檢查 `curl.exe -s -I --max-time 5 http://localhost:8088`；**僅當 `app.py` 尚未啟動或修改了 `app.py` 本身時**，才於工作區根目錄啟動：
     ```powershell
     python d:\AntiGravity\HFAOAIDelivery\app.py
     ```
   - 確認 `http://localhost:8088` 與 `https://www.metavisionsystems.com` 均回應 `200 OK`。
3. 將 `CODER/CODER.md` 標頭更新為 `- **Status**: \`DEPLOYED\``，**向 Manager 回報**由 Manager 更新 `STATE.json`（`DEPLOYED` 與版本號如 `v1.0`）並通知客戶盲測。

### Step 5：結案打包與交付（收到 Manager 轉達結案指令時執行）
1. 依客戶選擇的交付方案（參見 [AOI_Delivery_Playbook.md](./AOI_Delivery_Playbook.md) 第四節）：
   - **方案 A（Windows 離線綠色版）**：封裝 `CODER/detector.py` + 精簡純檢測介面 + 一鍵啟動 `.bat` + 環境健檢腳本。
   - **方案 B（產線機台 Watchdog）**：封裝資料夾監聽、`.tmp` Atomic Rename 防搶讀、Heartbeat 心跳與 FIFO 清理。
   - **方案 C（乾淨雲端 Space）**：建立全新無 Git 歷史的 Space 上傳最終版。
2. 清理開發期暫存圖與敏感測試資料（絕不打包 `projects_registry.json` 或其他客戶資料）。
3. 驗測交付包正常運作後，將 `CODER/CODER.md` 標頭更新為 `- **Status**: \`CLOSED\``，向 Manager 回報結案完成。
