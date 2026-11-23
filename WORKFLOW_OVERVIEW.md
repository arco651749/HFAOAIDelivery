# 🔄 MetaVision AOI — 五方角色交互流程總覽 (WORKFLOW OVERVIEW)

> **參與角色**：
> - **👨‍💼 Client（客戶）**：只操作瀏覽器三分頁網頁（免裝軟體、免懂技術）
> - **🎬 Director（您 / 產品導演）**：掌握三大關鍵決策閘道，看重點報告拍板定案
> - **👔 Manager（主控 Agent / PM）**：唯一總控中樞，巡檢狀態機、**單一寫入 `STATE.json`**、自動派工、初審品質與對您彙報
> - **🔍 Analyst（`aoi_analyst` 分析師）**：看圖分析、提問、記錄討論、寫定案規格（嚴禁寫碼、嚴禁改 `STATE.json`）
> - **💻 Coder（`aoi_coder` 開發工程師）**：見 `SPEC_FROZEN` 才開工，於 `detector_dev.py` 開發驗證，過 Review 才原子覆蓋 `detector.py` 上線（嚴禁改 `STATE.json`）

---

## 一、 全生命週期交互時序圖 (Sequence Flow)

```mermaid
sequenceDiagram
    autonumber
    participant Client as 👨‍💼 客戶 (網頁)
    participant Manager as 👔 Manager (主控PM)
    participant Director as 🎬 您 (產品導演)
    participant Analyst as 🔍 Analyst (分析師)
    participant Coder as 💻 Coder (寫程式)

    %% 階段 0：開案申請與防亂玩審核
    rect rgb(245, 248, 255)
        Note over Client,Director: 階段 0：新專案申請與開通（防陌生人亂玩）
        Client->>Manager: 網頁提交開案申請（客戶名、專案名、Email）<br/>寫入 pending_requests/ + request_audit_log.jsonl
        Manager->>Director: 巡檢彙報新申請人資料
        Director-->>Manager: 【閘道 0】審核拍板：准許開通（或拒絕留痕）
        Manager->>Client: 執行 manage_project.py approve 產密建目錄 (STATE=WAITING_UPLOAD)<br/>寄送「帳號 (<客戶>-<專案>) + 專屬密碼」至 Email
    end

    %% 階段 1：樣本上傳與需求填寫
    rect rgb(240, 255, 244)
        Note over Client,Analyst: 階段 1：樣本繳交與看圖分析（嚴禁偷跑寫碼）
        Client->>Manager: 登入網頁【分頁一】上傳訓練樣本 + 填寫「檢測需求說明」<br/>寫入 data/READY.json，網頁自動寫 STATE ➔ UPLOADED
        Manager->>Analyst: 偵測 UPLOADED ➔ Manager 改 STATE ➔ ANALYZING，派工看圖分析
        Analyst->>Analyst: 實地讀圖 + 讀需求 ➔ 撰寫 ANALYST/ANALYST.md<br/>(Status: PENDING_DIRECTOR_REVIEW)
        Analyst-->>Manager: 向 Manager 回報初版規格與問題清單
        Manager->>Manager: 【初審】檢查沒寫碼、確實看過圖、保留 HTML 標記
        Manager->>Director: 彙整分析摘要與問題清單呈報
    end

    %% 階段 2：線上討論與規格定案
    rect rgb(255, 250, 235)
        Note over Client,Analyst: 階段 2：客戶線上 Q&A 討論與規格定案
        loop 直到所有疑問釐清
            Director-->>Manager: 圈選要問客戶的問題（或補充提問）
            Manager->>Analyst: 指示更新 ANALYST/ANALYST.md 提問區與檔尾紀錄<br/>(Status: WAITING_CLIENT_QA)
            Analyst-->>Manager: 回報提問區已更新
            Manager->>Client: Manager 改 STATE ➔ WAITING_CLIENT_QA<br/>通知客戶至【分頁二 Discuss】回覆問題
            Client->>Manager: 線上填寫回覆文字 + 上傳補充圖片/文件<br/>自動歸檔 attachments/ + 追加 ANALYST.md，網頁寫 STATE ➔ CLIENT_REPLIED
            Manager->>Analyst: Manager 改 STATE ➔ ANALYZING，派工消化回覆與附件
            Analyst->>Analyst: 更新 ANALYST.md 問答表與細則 (Status: PENDING_DIRECTOR_REVIEW)
            Analyst-->>Manager: 回報更新後規格與剩餘疑問
            Manager->>Director: 初審後呈報最新規格細則
        end
        Director-->>Manager: 【閘道 1】拍板定案：「允許開工！」
        Manager->>Analyst: 指示清除舊題並設 ANALYST.md ➔ SPEC_FROZEN
        Analyst-->>Manager: 回報規格已凍結
        Manager->>Manager: Manager 寫入 STATE ➔ SPEC_FROZEN
    end

    %% 階段 3：演算法開發、驗證與 Review
    rect rgb(248, 240, 255)
        Note over Manager,Coder: 階段 3：演算法開發、交叉驗證與導演 Review
        Manager->>Coder: Manager 改 STATE ➔ CODING，正式交棒開發
        Coder->>Coder: 讀取定案規格 ➔ 於 CODER/detector_dev.py 實作演算法<br/>跑交叉驗證輸出 CODER/eval_outputs/ 與 CODER/CODER.md (Status: DIRECTOR_REVIEW)
        Coder-->>Manager: 向 Manager 回報開發數據與對比圖
        Manager->>Manager: 【初審】核對規格一致、無中文路徑地雷、CPU 耗時 < 0.4s
        Manager->>Director: Manager 改 STATE ➔ DIRECTOR_REVIEW，呈報數據與視覺對比圖
        opt 導演要求微調
            Director-->>Manager: 指示修正誤判或調整參數
            Manager->>Coder: Manager 改 STATE ➔ CODING，派工調優 detector_dev.py 並更新 CODER.md
            Coder-->>Manager: 回報新版驗證結果
            Manager->>Director: Manager 改 STATE ➔ DIRECTOR_REVIEW，再次呈報 Review
        end
        Director-->>Manager: 【閘道 2】Review 通過：「准許部署上線！」
        Manager->>Coder: 指示將 detector_dev.py 原子覆蓋為 CODER/detector.py 並健康檢查
        Coder-->>Manager: 回報部署健檢通過 (CODER.md ➔ DEPLOYED)
        Manager->>Manager: Manager 更新 STATE ➔ DEPLOYED (v1.0)，分頁三自動解鎖
    end

    %% 階段 4：客戶線上盲測、錯判閉環與結案
    rect rgb(255, 242, 242)
        Note over Client,Coder: 階段 4：客戶線上盲測、錯判回饋閉環與結案封存
        Manager->>Client: 通知進入【分頁三】開始盲測驗收
        Client->>Client: 單張診斷 + 整批上傳 (Batch) 並下載 Excel 報表<br/>原圖與報表自動集中存於 test_uploads/<YYYY-MM-DD>/
        opt 客戶發現判錯並按「回報修正」
            Client->>Manager: 自動存檔 hardcase_*.png 並寫入 HARDCASE_QUEUE.jsonl (PENDING)
            Manager->>Director: 巡檢彙報錯判樣本與完整說明，決議轉 Analyst 或 Coder 調優升版 (v1.1)
        end
        Client->>Director: 驗收通過、支付尾款
        Director-->>Manager: 下達結案指令
        Manager->>Coder: 派工打包交付物並清理暫存 (CODER.md ➔ CLOSED)
        Coder-->>Manager: 回報打包驗測完成
        Manager->>Manager: Manager 寫入 STATE ➔ CLOSED（分頁三顯示已結案封存）
    end
```

---

## 二、 您的三大決策閘道（Human-in-the-Loop 精華）

平常繁瑣的收圖、讀圖、催問、寫碼、驗證、存檔都由 AI 團隊自動運作，**您（產品導演）只需要在 3 個最關鍵的時刻拍板**：

| 閘道 | 時機 | 您看什麼 | 拍板動作 |
| :--- | :--- | :--- | :--- |
| **閘道 0：准開案** | 新客戶填表申請帳號 | Manager 彙報的客戶名、專案名、Email | 說「准」（產密通知）或「拒」（寫入稽核日誌） |
| **閘道 1：准開工** | Analyst 看圖與客戶 Q&A 完成 | `ANALYST/ANALYST.md`（執行細則 + 問答紀錄） | 確認沒疑問 ➔ 下令 **`SPEC_FROZEN`** 交棒 Coder |
| **閘道 2：准上線** | Coder 完成演算法與本機驗證 | `CODER/CODER.md`（量化數據 + 對比圖） | Review 滿意 ➔ 下令 **`DEPLOYED`** 解鎖分頁三盲測 |

---

## 三、 各角色紅線、狀態命名與專屬文件速查

| 角色 | 專屬 SOP | 維護檔案 | 絕對紅線 |
| :--- | :--- | :--- | :--- |
| **👔 Manager** | [AI_MANAGER_SOP.md](./AI_MANAGER_SOP.md) | `STATE.json`（唯一內部寫入者）、`projects_registry.json`、`request_audit_log.jsonl` | 不可跳過導演三大閘道；不越權代寫演算法 |
| **🔍 Analyst** | [AI_ANALYST_SOP.md](./AI_ANALYST_SOP.md) | `ANALYST/ANALYST.md`（規格＋提問＋討論合一）、`attachments/<YYYY-MM-DD>/` | **嚴禁寫或改 `.py` 程式碼與 `STATE.json`**；一律先向 Manager 回報 |
| **💻 Coder** | [AI_CODER_SOP.md](./AI_CODER_SOP.md) | `CODER/CODER.md`、`detector_dev.py`、`detector.py`、`eval_outputs/` | **未見 `SPEC_FROZEN` 嚴禁開工**；未過 Review 嚴禁覆蓋 `detector.py`；禁用 `cv2.imread/imwrite`；一律先向 Manager 回報 |
| **👨‍💼 Client** | [CLIENT_SOP.md](./CLIENT_SOP.md) | 僅透過網頁操作 `data/`、`ANALYST/`、`test_uploads/` | 未獲審核密碼前無法進入任何專案分頁 |

---

## 四、 專案標準目錄結構

```text
d:\AntiGravity\HFAOAIDelivery\
├── app.py                       # 多專案共用三分頁入口網站 (Port 8088 / HF Space 7860)
├── manage_project.py            # 開案看板、審核核准 (approve) / 拒絕 (reject) / 手動建案 (create)
├── projects_registry.json       # 已開通專案帳密表（帳號 = <客戶名稱>-<客戶專案>）
├── request_audit_log.jsonl      # 永久申請稽核日誌 (REQUESTED / APPROVED / REJECTED / CREATED)
├── pending_requests/            # 待審核新客戶開案申請 (<客戶名稱>-<客戶專案>.json)
└── projects/
    └── <客戶名稱>-<客戶專案>/
        ├── STATE.json           # 【Manager 唯一內部寫入】單一進度事實來源 (10 種標準 stage / version)
        ├── data/                # 【訓練樣本】raw/<類別>/<YYYY-MM-DD>/ + READY.json
        ├── ANALYST/             # 【Analyst 專屬】ANALYST.md（三合一）、CLIENT_REPLIED.json、attachments/<YYYY-MM-DD>/
        ├── CODER/               # 【Coder 專屬】CODER.md、detector_dev.py、detector.py、eval_outputs/
        └── test_uploads/        # 【線上盲測】<YYYY-MM-DD>/{single,batch_HHMMSS}/ 原圖、同日根層 Excel 與 hardcase_*.png + HARDCASE_QUEUE.jsonl
```
