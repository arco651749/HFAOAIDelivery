# 🚀 LiteRT-LM + Gemma 4 E2B Windows 本機推論實戰指南

> **實測日期**：2026-11-27  
> **實測環境**：Windows 11 x64 + Python 3.12 + NVIDIA GeForce RTX 2060 with Max-Q Design (6 GB VRAM)  
> **核心特色**：**100% 斷網離線、完全免裝 CUDA**（底層走 WebGPU over Direct3D 12）、支援 **Text + Vision（看圖多模態）**，峰值僅吃 **1.89 GB VRAM**，可與 AOI 主檢模型和平共存於入門級 6 GB 顯卡。

---

## 一、 步驟 1：建立獨立隔離虛擬環境並安裝 LiteRT-LM

為避免任何套件版本衝突（尤其保護主力 `C:\Python312` 內的 `opencv-python 5.1`），建議一律在獨立 `.venv` 安裝：

```powershell
mkdir D:\litert_lm_demo
cd D:\litert_lm_demo

# 1. 建立並啟用虛擬環境
C:\Python312\python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. 安裝官方 Windows Wheel（2026-11 實測版本為 0.20.0，約 28 MB）
pip install -U litert-lm litert-lm-api huggingface_hub
```

安裝完成後會一併取得：
- Python 套件：`import litert_lm`
- 命令列工具：`litert-lm`（內建 `run`、`benchmark`、`serve`、`describe` 子指令）

---

## 二、 步驟 2：下載官方 Gemma 4 E2B 模型（`.litertlm`）

- **官方 Repo**：`litert-community/gemma-4-E2B-it-litert-lm`（**Apache-2.0 授權、免申請 Gated 權限**）
- **模型檔案**：`gemma-4-E2B-it.litertlm`（約 **2.41 GiB / 2.59 GB**）

> ⚠️ **Windows 下載避坑**：`huggingface_hub` 若預設啟用 `hf-xet` 可能在部分 Windows 環境停在 0 bytes 不動，下載前務必設定 `HF_HUB_DISABLE_XET=1`。

```powershell
$env:HF_HUB_DISABLE_XET = "1"
python -c "from huggingface_hub import hf_hub_download; print(hf_hub_download('litert-community/gemma-4-E2B-it-litert-lm', 'gemma-4-E2B-it.litertlm', local_dir='./models'))"
```

下載完成後可用 CLI 檢視模型支援的能力與後端：

```powershell
litert-lm describe .\models\gemma-4-E2B-it.litertlm
```

實測回報規格：
- **Input Modalities**：`Text` / `Vision` / `Audio` 全支援
- **Backends**：Text `CPU / GPU`、Vision `CPU / GPU`、Audio `CPU`
- **Max Context**：`4096`（支援 Dynamic Context）、Vision Token Budget：`[70, 140, 280]`

---

## 三、 步驟 3：CLI 快速試玩與本機 OpenAI API 服務

```powershell
# 1. 互動式聊天（指定 GPU）
litert-lm run .\models\gemma-4-E2B-it.litertlm --backend gpu

# 2. 啟動本機 OpenAI-compatible API Server（可供任何 Agent / 前端直接呼叫）
litert-lm serve .\models\gemma-4-E2B-it.litertlm --backend gpu
```

---

## 四、 步驟 4：Python 完整最小範例（文字 + 看圖多模態 + 熱快取）

以下為經實測驗證可執行的標準寫法（重點已標註在註解中）：

```python
import os
import time
import litert_lm

MODEL_PATH = r".\models\gemma-4-E2B-it.litertlm"
CACHE_DIR = r".\cache"
IMAGE_PATH = r".\test_sample.jpg"

# ⚠️ 必做：cache_dir 必須預先建立，否則會拋 INVALID_ARGUMENT
# 開啟 cache_dir 後，GPU 第二次載入可從 20.8s 大幅縮短至 ~3.0s！
os.makedirs(CACHE_DIR, exist_ok=True)

# ⚠️ 必做：Backend 需傳入實例 Backend.GPU() / Backend.CPU()（類別傳法已棄用）
engine = litert_lm.Engine(
    model_path=MODEL_PATH,
    backend=litert_lm.Backend.GPU(),        # 無顯卡工控機改用 Backend.CPU()
    vision_backend=litert_lm.Backend.GPU(), # 看圖編碼器同步上 GPU
    cache_dir=CACHE_DIR,
    max_num_tokens=2048,
    enable_benchmark=True,
)


def extract_text(msg) -> str:
    if isinstance(msg, str):
        return msg
    c = getattr(msg, "content", msg)
    if isinstance(c, list):
        return "".join(getattr(item, "text", "") or "" for item in c)
    return str(c)


# --- 1. 純文字串流推論 ---
with engine.create_conversation(max_output_tokens=256) as conv:
    t0 = time.perf_counter()
    for chunk in conv.send_message_async("請用 3 句繁體中文簡述 AOI 視覺檢測的主要用途。"):
        print(extract_text(chunk), end="", flush=True)
    print(f"\n[TEXT] 總耗時: {time.perf_counter() - t0:.2f}s")
    print("[BENCH]", conv.get_benchmark_info())

# --- 2. 看圖多模態推論（用 ImageBytes 避開 Windows 中文路徑問題）---
if os.path.exists(IMAGE_PATH):
    with open(IMAGE_PATH, "rb") as f:
        img_bytes = f.read()

    with engine.create_conversation(max_output_tokens=256) as conv:
        msg = litert_lm.Contents([
            litert_lm.Content.ImageBytes(img_bytes),
            litert_lm.Content.Text("請用繁體中文簡述這張工業產線圖片裡看到了什麼物體？"),
        ])
        t0 = time.perf_counter()
        for chunk in conv.send_message_async(msg):
            print(extract_text(chunk), end="", flush=True)
        print(f"\n[VISION] 總耗時: {time.perf_counter() - t0:.2f}s")

# 釋放引擎與 VRAM（實測可乾淨釋放回 ~13 MiB，無洩漏）
engine.close()
```

---

## 五、 實測效能與 VRAM 數據總表（RTX 2060 Max-Q 6 GB）

| 指標 | 純 CPU (XNNPACK) | GPU 冷啟動（首次編譯） | GPU 熱快取（`cache_dir`） |
| :--- | :---: | :---: | :---: |
| **引擎載入時間** | 13.15 s | 20.78 s | **3.06 s** |
| **文字生成速度（Decode）** | **20.0 tok/s** | 42.6 tok/s | **62.2 tok/s** |
| **看圖 Prefill 速度** (295 tok) | 178.6 tok/s | 1,359.7 tok/s | **2,318.3 tok/s** |
| **看圖首字延遲（Engine / Wall）** | 1.70 s / 7.07 s | 0.23 s / 3.05 s | **0.14 s / 1.76 s** |
| **看圖生成速度（Decode）** | 20.6 tok/s | 58.9 tok/s | **66.8 tok/s**（256 tok 共 **5.55 s**） |
| **6 GB 顯卡 VRAM 峰值** | 0 MiB | **1,940 MiB (~1.89 GiB)** | **1,940 MiB (~1.89 GiB)** |

---

## 六、 實測踩坑清單與產線定位建議

### ⚠️ 必記避坑點
1. **下載模型加 `HF_HUB_DISABLE_XET=1`**：避免 Windows 上 `hf-xet` 卡在 0 bytes；正式交付給客戶直接分發單一 `.litertlm` 檔即可完全離線。
2. **務必啟用並預先建立 `cache_dir`**：可把 GPU 載入時間從 20.8 秒壓到 **3.0 秒**；若資料夾未事先建立會報 `INVALID_ARGUMENT`。
3. **含中文路徑圖片必用 `Content.ImageBytes(bytes)`**：不要直接傳中文路徑字串給 C++ 層，避免 Windows codepage 讀檔失敗。
4. **Windows 精簡版產線機 GPU 備援 DLL**：本機新驅動（Driver 617.42）開箱即跑通 WebGPU D3D12；若客戶端精簡版 Windows 報缺 `dxcompiler.dll`（Error 87），從 Windows SDK 複製 `dxcompiler.dll` 與 `dxil.dll` 放到執行檔同目錄即可。

### 🎯 產線導入定位建議
- **❌ 不適合**：取代 OpenCV 5.1 / LiteRT YOLO 做像素級 AOI 定位、微米量測或極小繁中字 OCR（2B 模型對小字繁中會有輕微認錯字，且深度光學知識較籠統）。
- **✅ 非常適合**：高度保密／**100% 斷網工廠**的本地 AI 輔助模組——例如**異常畫面自然語言解說、交班報表自動摘要、操作員離線問答、疑似 NG 畫面二次語意分流**（僅佔 1.89 GB VRAM，可與 AOI 主檢模型安全共存於同一張入門級 6 GB 顯卡）。
