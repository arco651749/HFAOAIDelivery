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

## 三、 跨語言標準函式庫白名單與「OpenCV 5.1 單一核心」原生 DLL 封裝規範

本平台採 **「OpenCV 5.1 大一統架構（影像處理 + AI 推論共用同一套 `cv::dnn` 引擎）」**：線上開發與盲測用 Python（極速迭代），結案交付 1:1 轉譯為**單一原生 C++ DLL（零安裝、跨語言呼叫、0 數值漂移）**。

### 3.1 各語言標準函式庫白名單

| 語言 / 階段 | 影像處理與讀碼標準庫 | AI 推論標準庫 | 嚴禁使用（防堵無法封裝單檔之套件） |
| :--- | :--- | :--- | :--- |
| **Python（線上開發與雲端盲測 `detector_dev.py` / `detector.py`）** | `opencv-python` (`cv2` ≥ 5.1)、`numpy`、`zxing-cpp`（DataMatrix / QR / 1D 工業全碼讀取）、`Pillow`（僅用於繪製中文標註字體與寫入 PNG `iTXt`） | **🏆 CPU 主力首選：`cv2.dnn` (`OpenCV 5.1 ENGINE_AUTO / ENGINE_OPENCV`)**<br>*(訓練匯出 `.onnx` 固定採 `dynamic=False` + `opset=12~17`；開發期一律以 `np.fromfile(path, np.uint8)` 讀入 Buffer 並實測 `cv2.dnn.readNetFromONNX(buf)`，兼顧 Windows 中文路徑安全與提早驗證算子相容性！)*<br>**⚡ GPU 加速首選：`LiteRT` (`ai-edge-litert` GPU Delegate)**（客戶明確要求跑 GPU 時統一選用，C / Python 跨語言封裝輕量一致）<br>🥈 僅遇冷門不支援算子時退用 `onnxruntime`<br>*(註：`ultralytics` / `torch` **僅限訓練與匯出 `.onnx`/`.tflite` 腳本**，嚴禁在 `detector.py` 推論路徑中 `import`)* | 嚴禁在推論主流程使用 `scipy`、`scikit-image`、`scikit-learn`、`pandas`、`torch`、`pyzbar` 等難以平轉 C++ 靜態編譯或不支援 DataMatrix 之套件 |
| **C++（單檔原生 DLL 核心引擎 `MetaVisionAOI.dll`）** | **統一安裝於 `D:\opencv5_static` 之靜態 `/MT` 套件庫**：`OpenCV 5.1`（`core`、`imgproc`、`imgcodecs`、`dnn`、`geometry`、`flann`）＋ **`zxing-cpp` (`ZXing.lib`)**（DataMatrix / QR / 全條碼靜態讀碼） | **CPU 真單檔主力：同一套 `OpenCV 5.1 cv::dnn (ENGINE_AUTO / ENGINE_OPENCV)` 直接吃 Win32 `RCDATA` 內嵌 `.onnx` 記憶體指標**（免外帶額外 AI 庫）<br>**⚡ GPU 交付首選：`LiteRT` (C/C++ API + GPU Delegate)**（客戶指定跑 GPU 加速時改包 LiteRT，與 Python 端同源一致；冷門算子備援選配 `ENGINE_ORT`） | 嚴禁使用 `/MD` 動態 CRT（防客戶端缺少 `vcruntime140.dll`）、嚴禁依賴 Python/CUDA Toolkit 作為 CPU 單檔預設前提 |
| **C# / C++ / Python 客戶端呼叫層** | 客戶端自備影像來源（`OpenCvSharp` / `Bitmap` / `cv::Mat` / `numpy`），直接傳入 **連續記憶體指標（`GRAY8` / `BGR8` / `BGRA8` / `GRAY16` / `BGR16` / `FLOAT32` / `FLOAT32_3CH`）** 或 **UTF-8 圖檔路徑** | **無須安裝任何 OpenCV、AI 或 VC++ 執行環境** | 不強迫客戶端綁定特定 OpenCV 或 .NET 版本 |

### 3.2 單一原生 DLL 零安裝靜態編譯規範（Windows x64 + OpenCV 5.1）
欲達成「**客戶只拿到 1 顆 `.dll`，不用裝 OpenCV、不用裝 Python、不用裝 ONNX Runtime、連 Microsoft Visual C++ Redistributable 都不用裝**」，編譯時必須遵守：
1. **從 OpenCV 5.1 原始碼一次性靜態編譯核心模組（本機已編妥於 `D:\opencv5_static`）**：
   ```powershell
   $cmake = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
   git clone --branch 5.1.0 --depth 1 https://github.com/opencv/opencv.git D:\opencv5_src
   & $cmake -S D:\opencv5_src -B D:\opencv5_build -G "Visual Studio 17 2022" -A x64 `
     "-DCMAKE_GENERATOR_INSTANCE=C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools" `
     -DBUILD_SHARED_LIBS=OFF `
     -DBUILD_WITH_STATIC_CRT=ON `
     "-DBUILD_LIST=core,imgproc,imgcodecs,dnn" `
     -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_EXAMPLES=OFF `
     -DBUILD_opencv_apps=OFF -DBUILD_opencv_python3=OFF -DBUILD_JAVA=OFF `
     -DWITH_FFMPEG=OFF -DWITH_GSTREAMER=OFF -DWITH_MSMF=OFF -DWITH_DSHOW=OFF `
     -DCMAKE_INSTALL_PREFIX=D:\opencv5_static
   & $cmake --build D:\opencv5_build --config Release --target INSTALL --parallel
   ```
   *(註：OpenCV 5.1 靜態建置會自動連帶編出 `geometry` 與 `flann`；若單檔 DLL 需於 C++ 端直接執行 `calibrateCamera`/`findHomography`，再追加 `calib` 模組。專案 CMake 設定 `-DCMAKE_PREFIX_PATH=D:\opencv5_static` 即可同時 `find_package(OpenCV REQUIRED)` 與 `find_package(ZXing REQUIRED)`。)*
2. **MSVC 編譯器必設 `/MT`（Static CRT）與零依賴驗收**：
   - 所有專案 `CMakeLists.txt` **必須**設定 `set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded")`（防預設 `/MD` 連結 `D:\opencv5_static` 時爆 `LNK2038`）。
   - 編譯完成後**必跑** `dumpbin /dependents MetaVisionAOI.dll`，確認僅依賴 Windows 系統核心 DLL（`KERNEL32.dll` 等），**嚴禁出現 `VCRUNTIME140.dll`、`MSVCP140.dll` 或 `opencv_*.dll`**。
3. **ONNX 權重內嵌防盜（Win32 `RCDATA` 資源嵌入，嚴禁轉超大 C 陣列）**：
   - 嚴禁將 10–30 MB `.onnx` 轉為 `const unsigned char[]` C 文字陣列（會暴增破百 MB 導致 MSVC `C1060 out of heap space`）。
   - 一律透過 **Win32 Resource (`.rc` `RCDATA`)** 將 `.onnx`（可做 XOR/AES 混淆）直接打包進 `MetaVisionAOI.dll`，執行期以 `FindResourceW` / `LoadResource` / `LockResource` 取得記憶體指標與長度，直接傳入 `cv::dnn::readNetFromONNX(ptr, size)`（預設 `ENGINE_AUTO` 即啟用 OpenCV 5.1 新圖引擎）——依然 **100% 單一 `.dll`**、3 秒編完且零記憶體拷貝。

#### 3.2.1 GPU 加速專案：LiteRT (`.tflite`) 轉檔與 Windows 交付避坑規範（已實測驗證）
當客戶端明確要求 GPU 加速時，統一選用 **LiteRT (`ai-edge-litert ≥ 2.4`) + FP16 `.tflite`**（走 Windows 內建 Direct3D 12 WebGPU，**完全免裝 CUDA**，跨 NVIDIA / AMD / Intel 顯卡皆可 100% 全圖 GPU 加速；純 CPU 專案仍維持 OpenCV 5.1，實測 CPU 速度快約 36% 且可真單檔）。實作時必須遵守以下實測避坑鐵則：
1. **轉檔工具嚴禁污染主環境（必用獨立 `.venv`）**：
   - `onnx2tf` 會強制鎖定舊版 `opencv-python`（如 `4.13`）與 `numpy`，**絕對不可安裝於本機主力 `C:\Python312`**，必須建立獨立轉檔用 `.venv`（安裝 `onnx2tf` + `tensorflow` + `tf_keras`）。
2. **轉檔必加 `-tb tf_converter`（禁用預設 `flatbuffer_direct`）**：
   - `onnx2tf 2.6.x` 預設的實驗性 `flatbuffer_direct` 後端會錯誤推導 YOLO 輸出 shape 導致推論崩潰；標準指令一律為：
     ```powershell
     onnx2tf -i model.onnx -o tflite_out -tb tf_converter -n
     ```
   - 優先選用產出的 **`model_float16.tflite`**（模型體積減半、首次 Shader 編譯耗時減半，與 FP32 在 WebGPU 上精度一致，中心誤差 ≤ 0.5 px）。
   - **輸入張量格式注意**：轉出的 `.tflite` 輸入為 **NHWC `(1, H, W, 3)`**（RGB `float32` 歸一化），前處理不需再做 `HWC → CHW` 轉置。
3. **Windows GPU 交付必附 4 顆 DLL 與初始化暖機**：
   - `ai-edge-litert` 內附 `libLiteRt.dll` 與 `libLiteRtWebGpuAccelerator.dll`，但**未打包** DirectX Shader Compiler；若缺少會報 `DynamicLib.Open: dxcompiler.dll Windows Error: 87`（單純加 `PATH` 無效）。
   - Windows GPU 交付包（Python / C++ 皆同）**必須於執行檔 / DLL 同目錄隨附** Windows SDK 的 **`dxcompiler.dll` 與 `dxil.dll`**，並於 `MV_Create()` / 啟動初始化時執行 **3 次 dummy 推論暖機（warmup）**，以完成首次 WebGPU Compute Shader 編譯並拉起 GPU 時脈進入穩態（約 10 ms 級）。
   - 若遇極少數冷門算子導致 `.tflite` 轉檔或 GPU Delegate 失敗，備援切換至 **ONNX Runtime + DirectML**（同樣免裝 CUDA、直吃 `.onnx`）。

### 3.3 統一跨語言 C ABI 匯出介面 (`extern "C"`)
所有單檔 DLL 一律匯出純 C ABI（零 C++ Name Mangling、零 STL 跨邊界問題），輸入支援「記憶體連續影像指標（涵蓋 8-bit 灰階/彩色、**16-bit 工業高動態灰階與深度圖**、32-bit 浮點高度圖）」與「UTF-8 圖檔路徑」，輸出統一為 **UTF-8 JSON 字串**：

```c
// MetaVisionAOI.h — 跨語言統一 C ABI 合約（C++ / C# P/Invoke / Python ctypes 共用）
#ifdef _WIN32
  #ifdef MV_BUILDING_DLL
    #define MV_API __declspec(dllexport)
  #else
    #define MV_API __declspec(dllimport)
  #endif
#else
  #define MV_API
#endif

// 統一像素格式列舉（原生涵蓋 8-bit、16-bit 工業相機/深度圖、32-bit 浮點高度圖與 3D XYZ 點雲圖）
typedef enum MV_PixelFormat {
    MV_PIX_GRAY8       = 1,   // 8-bit  單通道灰階 (CV_8UC1,   1 byte/px)
    MV_PIX_BGR8        = 3,   // 8-bit  三通道 BGR (CV_8UC3,   3 bytes/px)
    MV_PIX_BGRA8       = 4,   // 8-bit  四通道 BGRA(CV_8UC4,   4 bytes/px，相容 C# 32bpp Bitmap)
    MV_PIX_GRAY16      = 11,  // 16-bit 單通道無號 (CV_16UC1,  2 bytes/px，Mono10/12/16 與 Depth16)
    MV_PIX_BGR16       = 13,  // 16-bit 三通道 BGR (CV_16UC3,  6 bytes/px)
    MV_PIX_FLOAT32     = 31,  // 32-bit 單通道浮點 (CV_32FC1,  4 bytes/px，3D 線雷射高度圖 / 深度圖)
    MV_PIX_FLOAT32_3CH = 33   // 32-bit 三通道浮點 (CV_32FC3, 12 bytes/px，結構光有序 XYZ 點雲圖 / HDR 浮點彩色)
} MV_PixelFormat;

extern "C" {
    // 0. 查詢 SDK 與專案模型版本（回傳靜態常數字串，免釋放）
    MV_API const char* MV_GetVersion(void);

    // 1. 建立檢測器實例（config_json 可傳 NULL 使用預設參數；失敗回傳 NULL）
    MV_API void* MV_Create(const char* config_json);

    // 2. 記憶體影像直接推論（推薦產線相機零寫碟高速呼叫）
    //    img_data: 影像資料起始指標（void* 直接相容 uint8* / uint16* / float* / C# IntPtr）
    //    pixel_format: 見 MV_PixelFormat 列舉（GRAY8/BGR8/BGRA8/GRAY16/BGR16/FLOAT32/FLOAT32_3CH）
    //    stride: 每列位元組數 bytes（傳 0 視為緊湊 width * bytes_per_pixel）
    //    回傳值：0=成功；>0=out_json_buf 空間不足（回傳所需位元組數，含結尾 '\0'）；<0=錯誤碼
    MV_API int MV_Detect(
        void* handle,
        const void* img_data,
        int width,
        int height,
        int pixel_format,
        int stride,
        char* out_json_buf,
        int buf_size
    );

    // 3. UTF-8 檔案路徑推論（支援 Windows 中文路徑，保留原位元深度如 16-bit PNG/TIFF）
    //    實作細則：內部必以 MultiByteToWideChar(CP_UTF8) + _wfopen 讀入記憶體再 cv::imdecode(buf, IMREAD_UNCHANGED)，嚴禁 cv::imread
    MV_API int MV_DetectFile(
        void* handle,
        const char* utf8_image_path,
        char* out_json_buf,
        int buf_size
    );

    // 4. 取得最近一次錯誤詳情（handle 可為 NULL 查詢建立失敗原因；回傳內部指標免釋放）
    MV_API const char* MV_GetLastError(void* handle);

    // 5. 釋放實例資源
    MV_API void MV_Destroy(void* handle);
}
```

- **產線防崩潰與執行緒紅線**：
  - **例外邊界**：所有 `extern "C"` 函式實作外層**必須包覆 `try { ... } catch (...)`**，轉寫錯誤碼與 `last_error`，嚴禁讓 C++ 例外跨 ABI 炸毀客戶端宿主程式。
  - **執行緒安全**：單一 `handle` **非執行緒安全**（多相機／多執行緒請各自呼叫 `MV_Create` 建立獨立 `handle`）。
  - **緩衝區建議**：呼叫端建議預配 `≥ 64 KB`（分割多邊形密集案建議 `≥ 256 KB`），並於 `handle` 內快取最近一次 JSON 避免緩衝區不足重呼時重複推論。
- **標準交付附帶呼叫薄封裝（隨 DLL 一併交付）**：
  - `MetaVisionAOI.dll`（唯一核心二進位檔）
  - `MetaVisionAOI.h`（C / C++ 標頭檔）
  - `MetaVisionAOI.cs`（C# P/Invoke `[DllImport("MetaVisionAOI.dll")]` 封裝類別，.NET Framework / .NET 6~9 通用）
  - `metavision_aoi.py`（Python `ctypes` 封裝模組與範例）

### 3.4 工業量測、幾何定位與讀碼標準流程（OpenCV 5.1 + ZXing-C++）
針對傳統量測、二次亞像素定位與讀碼案件，`aoi_coder` 應優先採用以下經實戰驗證之標準流程（Python 與 C++ 函式 1:1 對應，避免使用參數敏感的舊版暴力霍夫演算法）：

1. **相機校正與九點標定（Pixel ↔ Robot mm）**：
   - **特徵提取**：棋盤格用 `findChessboardCornersSB()`（抗反光且自帶亞像素）；高精工業標定板用 `findCirclesGrid()`。
   - **內參與畸變校正**：以 `calibrateCamera()` 求得 `K` 與 `distCoeffs`；產線推論於開機算一次 `initUndistortRectifyMap()`，每張圖只執行高速 `remap()`（若僅需回傳少數點座標，改用 **`undistortPoints()`** 免重採樣整張圖）。
   - **像素轉世界座標**：俯拍透視平面採 `findHomography(..., RANSAC)` ＋ `perspectiveTransform()`；遠心鏡頭／無透視採 `estimateAffine2D()`。
   - *(備註：`D:\opencv5_static` 若需在 C++ 單檔 DLL 內直接執行 `calibrateCamera`/`findHomography`，需確認已包含 OpenCV 5.1 `calib` 模組；純 `remap`/`warpAffine`/`warpPolar` 則已內建於 `imgproc`。)*
2. **強化找線（FindLine / Rake 亞像素卡尺）**：
   - **全域自動找線**：優先使用 `createLineSegmentDetector(LSD_REFINE_ADV)`（免調 Canny 雙門檻、輸出亞像素端點）。
   - **高精度矩形卡尺法（精度 `0.05 ~ 0.1 px`）**：先以 `warpAffine()` 將任意角度之矩形卡尺 ROI 轉正為水平條帶 ➔ 沿法線做 1D 高斯平滑 ＋ `Sobel` 梯度，取每列極值並做二次拋物線亞像素插值 ➔ 以 **`fitLine(..., DIST_HUBER / DIST_WELSCH)`**（或搭配 RANSAC）濾除毛邊/缺口離群點 ➔ 逆矩陣轉回原圖座標。
3. **強化找圓 / 橢圓（FindCircle / 二次精定位）**：
   - **全域初定位**：使用 `HoughCircles(..., HOUGH_GRADIENT_ALT)`（`param2` 直接對應真圓度 `0.85~0.92`）或先以 OpenCV 5.1 `cv::dnn` (YOLO) 初框目標 ROI。
   - **高精度擬合**：使用 **`fitEllipseDirect()`** 或 **`fitEllipseAMS()`**（抗斷弧、抗反光遮擋、相容透視微橢圓且不發散）。
4. **扇形 / 圓環區域檢測與找弧（Annulus / Sector / Spoke 卡尺）**：
   - **瑕疵 / 灰階 / 顏色 / 面積統計（Mask 遮罩法）**：先切出扇形外接小矩形（避免全圖運算）➔ 以 `ellipse(..., startAngle, endAngle, 255, -1)` 畫外扇形，再以 `circle(..., r_in, 0, -1)` 挖空內圓得到圓環扇形 `mask`（做瑕疵邊緣檢測前將 `mask` 內縮 `erode` 2～3 px 防止邊界誤報）。
   - **扇形找圓弧 (`Spoke`) / 測圓度 / 抓缺口 / 環形 OCR（極座標攤平法）**：以 **`warpPolar(..., WARP_POLAR_LINEAR)`** 將圓展開為極座標圖（X 軸=半徑 $r$、Y 軸=角度 $\theta$），直接矩形切片 `polar[start_deg:end_deg, r_in:r_out]`（跨 0°/360° 時將 `polar` 上下垂直拼接兩份即可無縫裁切）；沿每一列找 1D 亞像素邊緣後轉回直角座標 $(c_x + r\cos\theta,\; c_y + r\sin\theta)$ 做圓/橢圓擬合，可精準避開鍵槽、缺口與局部反光。
5. **工業全碼讀取（DataMatrix ECC200 / QR / 1D / 雷雕 DPM）**：
   - 統一使用 **`zxing-cpp`**（Python `import zxingcpp`；C++ 靜態連結 `D:\opencv5_static\lib\ZXing.lib`）。
   - 大圖小碼或雷雕 DPM 必走三段式：**OpenCV 5.1（YOLO 或梯度密集區）切出碼區 ROI ➔ `imgproc` 強化（CLAHE 對比增強 / 反相 / 形態學閉運算連接點陣）➔ `zxing-cpp` 毫秒級解碼並輸出字串與四角點座標**。

### 3.5 傳統機器視覺演算法理論地圖（按需查閱 `REFERENCE/NI_VISION_CONCEPT/`，以 OpenCV 5.1 實作）
當遇到複雜光照、週期性紋理、重疊粒子、固定圖樣比對或精密座標系跟隨等傳統 CV 難題時，**切忌盲目硬套 YOLO 或粗糙的 `Canny + findContours`**。`aoi_coder` 可按需唯讀查閱專案內建之 [REFERENCE/NI_VISION_CONCEPT/README.md](./REFERENCE/NI_VISION_CONCEPT/README.md)（399 頁原廠概念手冊 22 章 Markdown 版）借鏡經典數學模型與邊界心法，**並嚴守 3.1 白名單以 OpenCV 5.1 / `zxing-cpp` 實作（嚴禁引入 `nivision.dll`）**：

| 實務演算法難題 | 按需查閱章節（`REFERENCE/NI_VISION_CONCEPT/`） | OpenCV 5.1 對應實作核心 |
| :--- | :--- | :--- |
| **光照不均、低對比、週期性背景紋理** | `Chapter_04_Image_Analysis.md`（直方圖/Line Profile）<br>`Chapter_05_Image_Processing.md`（LUT/濾波/灰階形態學）<br>`Chapter_07_Frequency_Domain_Analysis.md`（FFT 頻域濾波） | `cv2.createCLAHE`、`cv2.morphologyEx`（`TOPHAT`/`BLACKHAT` 去不均勻背景）、`cv2.dft` 陷波濾波去週期紋理 |
| **影像分割、二值化與重疊粒子分離** | `Chapter_08_Image_Segmentation.md`（全域/局部/形態學分割）<br>`Chapter_09_Binary_Morphology.md`（結構元素/連通性/填洞/骨架） | `cv2.threshold(OTSU)`、`cv2.adaptiveThreshold`、`cv2.distanceTransform` ＋ `cv2.watershed` 分離黏連目標 |
| **瑕疵/粒子幾何特徵篩選與分類** | `Chapter_10_Particle_Measurements.md`（面積/圓度/長寬比/慣性矩）<br>`Chapter_16_Binary_Particle_Classification.md` | `cv2.connectedComponentsWithStats`、`cv2.moments`、`cv2.minAreaRect`（計算真圓度、矩形度、主軸角） |
| **畸變校正、座標系跟隨 (Fixture) 與量測** | `Chapter_03_System_Setup_and_Calibration.md`<br>`Chapter_11_Edge_Detection.md`<br>`Chapter_14_Dimensional_Measurements.md` | `findChessboardCornersSB` / `remap`、先找基準點建立相對座標轉換矩陣，再對齊量測 ROI 做 1D 亞像素卡尺 |
| **模板匹配 vs 幾何輪廓匹配** | `Chapter_12_Pattern_Matching.md`（灰階 NCC 金字塔）<br>`Chapter_13_Geometric_Matching.md`（抗旋轉/縮放/遮擋） | 影像金字塔 + `cv2.matchTemplate(TM_CCOEFF_NORMED)`，或梯度邊緣方向特徵匹配（權衡見 [Pattern_Matching_vs_Geometric_Matching.md](./REFERENCE/wiki/comparisons/Pattern_Matching_vs_Geometric_Matching.md)） |
| **抗亮度干擾之色彩檢測與色差判別** | `Chapter_15_Color_Inspection.md`（色彩空間/色彩光譜比對） | `cv2.cvtColor(BGR2HSV / BGR2Lab)` 分離亮度與色度通道、Lab $\Delta E$ 色差或色相直方圖比對 |
| **印刷/標籤/固定結構瑕疵（黃金樣板比對）** | `Chapter_17_Golden_Template_Comparison.md`（對齊＋邊緣寬容帶＋亮暗瑕疵雙閾值） | `warpAffine` / `findTransformECC` 精準對齊 ➔ 樣板邊緣膨脹建立忽略帶（防亞像素位移誤報）➔ 正負差值分離亮/暗瑕疵 |
| **字元/條碼前處理與讀碼增強** | `Chapter_18_Optical_Character_Recognition.md`<br>`Chapter_19_Instrument_Readers.md` | 借鏡字元切割與條碼對比強化心法；讀碼實作統一用 `zxing-cpp`，OCR 採輕量 ONNX 模型（濾波核直接用 OpenCV `Sobel`/`Scharr`/`getStructuringElement`，勿依賴轉檔直排的 `Appendix_A_Kernels.md`） |

- **進階權衡速查（唯讀）**：二值化選型見 [REFERENCE/wiki/comparisons/Thresholding_Methods_Comparison.md](./REFERENCE/wiki/comparisons/Thresholding_Methods_Comparison.md)；模板 vs 幾何匹配見 [REFERENCE/wiki/comparisons/Pattern_Matching_vs_Geometric_Matching.md](./REFERENCE/wiki/comparisons/Pattern_Matching_vs_Geometric_Matching.md)；六大任務分流與「規則快篩 ➔ AI 精判」兩段式架構見 [REFERENCE/wiki/syntheses/Pragmatic_Industrial_Vision_Toolbox.md](./REFERENCE/wiki/syntheses/Pragmatic_Industrial_Vision_Toolbox.md)。
- **上游殘留防呆**：`REFERENCE/wiki/` 與 `NI_VISION_CONCEPT/README.md` 內若出現 `[[...]]` 雙括號、`VDMAPI`、`../index.md` 或非白名單工具（NI VDM / TensorRT / WeChatQRCode / Anomalib / Open3D），**一律忽略斷鏈，僅借鏡數學與架構思維並映射回 3.1 標準棧（OpenCV 5.1 + `zxing-cpp` + ONNX `cv::dnn`）**。

### 3.6 無損 PNG Metadata 統一資料結構（`MetaVisionAOI/1.0`）
為確保**永不破壞原始影像像素**（方便未來重訓、換演算法回放與無損縮放檢視），歸檔與交付用 PNG 一律保留 100% 無損原圖，並將 **ROI（輸入區／YOLO 真值標註）**、**Overlay（演算法輸出疊圖）**、**相機校正 (`calibration`)** 與 **深度／點雲連結 (`depth_assets`)** 寫入 PNG 標準 **`iTXt` Chunk**（UTF-8 原生支援繁體中文，嚴禁使用僅支援 Latin-1 的 `tEXt`）：

- **Chunk Keyword**：`MetaVisionAOI`（UTF-8 JSON；大資料量可啟用 `iTXt` zlib 壓縮）。
- **寫入與防抹除鐵則**：
  - **Replace-or-Insert 原子寫入**：更新同一張 PNG 時，**必須先剔除所有既有同名 `MetaVisionAOI` Chunk**，再於 `IEND` 前寫入唯一一份（含 Big-Endian 長度與 CRC32），並經 `.tmp` Atomic Rename 覆蓋防斷電損檔（嚴禁重複 append 造成雙份 Chunk）。
  - **Python**：使用 `PIL.PngImagePlugin.PngInfo().add_itxt("MetaVisionAOI", json_str, zip=...)`；**注意 `cv2.imencode` / `cv::imwrite` 及未帶 `pnginfo` 的 `PIL.Image.save` 會靜默抹除 `iTXt`**，任何重存皆須顯式搬移原 `MetaVisionAOI` Chunk。
  - **C++**：因 `D:\opencv5_static` 預設不安裝 3rdparty `png.h`，統一以 ~80 行純 C++ 直接解析／替換 PNG Chunk（零 header 依賴、免重編解碼像素、`< 1ms`）。
  - 網頁/瀏覽器即時預覽圖僅在記憶體副本上渲染標註，不覆蓋無損原圖。
- **統一座標、角度與矩陣方向約定（嚴格防漂移）**：
  - 座標原點為原圖左上角 `(0, 0)`、單位 `px`（浮點數支援亞像素）；角度單位 `deg`（`0°` = 3 點鐘 `+X`，順時針為正）。
  - **`calibration` 方向鎖死**：`homography` = **Pixel `(u,v,1)` → World `(X,Y,1)`**；`hand_eye_4x4` = **Camera → Robot Base (`T_base_cam`)**；`dist` = OpenCV 順序 `[k1,k2,p1,p2,k3...]`；`pose_3d_mm` 標明歐拉角順序（預設 `ZYX` deg）。
- **兩用統一幾何基元 (`geom`)**（`rois[]` 與 `overlays[]` 100% 共用，且兩邊皆含 `label` 與 `class_id` 以無縫互通 YOLO 標註）：
  - `point`：`{ "type": "point", "x", "y" }`
  - `line`：`{ "type": "line", "x1", "y1", "x2", "y2" }`
  - `rect`：`{ "type": "rect", "cx", "cy", "w", "h" }`（直接對齊 YOLO Detect）
  - `rrect`：`{ "type": "rrect", "cx", "cy", "w", "h", "angle" }`（`w` 沿 `angle` 主軸、`h` 垂直 `angle + 90°`，`angle ∈ [0, 360)` 支援有方向 Rake 卡尺與 YOLO OBB）
  - `circle`：`{ "type": "circle", "cx", "cy", "r" }`
  - `ellipse`：`{ "type": "ellipse", "cx", "cy", "rx", "ry", "angle" }`（`rx`/`ry` 明定為**半軸長**非直徑，`rx` 沿 `angle` 主軸；從 `cv::fitEllipse` 轉換必除以 2）
  - `sector`：`{ "type": "sector", "cx", "cy", "r_in", "r_out", "start_deg", "end_deg" }`（圓環／扇形／Spoke 卡尺；**順時針掃描且嚴格 `end_deg > start_deg`、`0 < end - start <= 360`**，跨 0° 寫 `350~370` 或 `-10~10` 防 `cv::ellipse` 畫反；`r_in=0` 為實心扇形，`0~360` 為整圈圓環）
  - `polygon`：`{ "type": "polygon", "points": [[x,y], ...], "closed": true }`（多邊形 / 折線 / YOLO Seg）
- **標準 JSON Schema 範例（`MetaVisionAOI/1.0`）**：
  ```json
  {
    "schema": "MetaVisionAOI/1.0",
    "project_id": "TestClient-SpoolAOI",
    "version": "v1.0",
    "timestamp": "2026-11-24T08:37:00+08:00",
    "image": { "w": 1280, "h": 720 },
    "classes": ["大黑軸", "小黑軸", "小白軸", "綠墊", "棧板"],
    "summary": { "verdict": "OK", "elapsed_ms": 58.6, "counts": { "大黑軸": 6, "綠墊": 1 }, "note": "大黑軸:6, 綠墊:1" },
    "calibration": {
      "model": "pinhole",
      "K": [[1120.5, 0.0, 640.0], [0.0, 1120.5, 360.0], [0.0, 0.0, 1.0]],
      "dist": [-0.082, 0.115, 0.0, 0.0, 0.0],
      "pixel_to_mm": null,
      "homography": null,
      "hand_eye_4x4": null,
      "euler_order": "ZYX",
      "unit": "mm"
    },
    "depth_assets": {
      "depth": { "file": "20261119_001-Depth.png", "format": "uint16_png", "scale_mm": 0.1, "invalid_value": 0, "min_mm": 300.0, "max_mm": 2000.0, "aligned_to_rgb": true },
      "pointcloud": { "file": "20261119_001.ply", "format": "ply", "unit": "mm", "frame": "camera" }
    },
    "rois": [
      {
        "id": "roi_pallet",
        "label": "取料棧板區",
        "class_id": null,
        "op": "include",
        "geom": { "type": "rect", "cx": 645.0, "cy": 402.5, "w": 810.0, "h": 595.0 },
        "style": { "color": "#FFFF00", "width": 2, "dash": true, "visible": true },
        "meta": {}
      }
    ],
    "overlays": [
      {
        "id": "det_01",
        "label": "大黑軸",
        "class_id": 0,
        "layer": "detect",
        "status": "OK",
        "score": 0.994,
        "text": "#1 大黑軸 (412,219) 0.99",
        "geom": { "type": "rect", "cx": 412.4, "cy": 218.7, "w": 148.0, "h": 146.0 },
        "style": { "color": "#00E5FF", "width": 2, "fill_alpha": 0.0, "font_size": 14, "visible": true },
        "meta": { "pose_3d_mm": [125.4, -38.2, 612.0, 0.0, 0.0, 15.2] }
      }
    ]
  }
  ```
  - `rois[].op` 合法值：`"include"`（檢測區）、`"exclude"`（遮罩挖除區）、`"caliper"`（卡尺掃描區，方向如 `in_to_out`/`left_to_right` 與極性如 `dark_to_light` 放 `rois[].meta`）、`"gt"`（YOLO 訓練真值標註）。
  - `depth_assets.*.file` 一律填寫**相對於本 RGB PNG 所在目錄之相對路徑且強制使用正斜線 `/`**（確保跨平台與整包搬移不斷鏈）；純 2D 案時 `calibration` 與 `depth_assets` 填 `null` 即可。

---

## 四、 標準作業步驟

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
1. 依客戶選擇的交付方案（參見 [AOI_Delivery_Playbook.md](./AOI_Delivery_Playbook.md) 階段 4）：
   - **方案 A（Windows 離線綠色版）**：封裝 `CODER/detector.py` + 精簡純檢測介面 + 一鍵啟動 `.bat` + 環境健檢腳本。
   - **方案 B（產線機台 Watchdog）**：封裝資料夾監聽、`.tmp` Atomic Rename 防搶讀、Heartbeat 心跳與 FIFO 清理。
   - **方案 C（乾淨雲端 Space）**：建立全新無 Git 歷史的 Space 上傳最終版。
   - **方案 D（單一原生 C++ DLL SDK — 零安裝跨語言）**：依第三節規範以統一靜態庫 `D:\opencv5_static`（`OpenCV 5.1` + `ZXing.lib` + `/MT`）搭配 `ENGINE_AUTO / ENGINE_OPENCV` 與 Win32 `RCDATA` 內嵌 `.onnx` 權重編譯出單一 `MetaVisionAOI.dll`，附送 `MetaVisionAOI.h` / `MetaVisionAOI.cs` / `metavision_aoi.py`，並以與 Python 版一致的測試圖驗證推論數值與座標一致（且必跑 `dumpbin /dependents` 確認 0 外部 DLL 依賴）。
2. 清理開發期暫存圖與敏感測試資料（絕不打包 `projects_registry.json` 或其他客戶資料）。
3. 驗測交付包正常運作後，將 `CODER/CODER.md` 標頭更新為 `- **Status**: \`CLOSED\``，向 Manager 回報結案完成。
