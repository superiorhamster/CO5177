# Bàn giao Text v2 — Colab T4 Run All & Website Sync (21/11/2026)

Thực hiện theo giao thức Oxford Pets 11 mục, quy trình EDA v2 (tách EDA CPU và huấn luyện T4 với tiền xử lý theo embedder: TF-IDF 20k word+emoticon, CBOW 10k PyVi max 300, PhoBERT 256). Toàn bộ 12 lượt chạy (6 kiến trúc × Base/Augmented) trên Colab T4 hoàn tất thành công, artifacts và checkpoint đã được kiểm toán và tích hợp vào notebook gốc cũng như website báo cáo.

## 1. Thông tin phiên chạy (Session Metadata)
- **Run ID**: `20261121T123956Z`
- **Thời gian hoàn tất**: 21/11/2026 (UTC: 2026-11-21T13:15:38Z; GMT+7: 21/11/2026 20:15:38)
- **Môi trường**: Google Colab T4 (GPU: Tesla T4, Python 3.13.16, PyTorch 2.14.1+cu130, Transformers 4.57.6, scikit-learn 1.6.1, Gensim 4.4.0)
- **Colab Session**: `vlsp-v2-full-t4`, VM đã giải phóng (`vm_released: true`, driver status `passed`)
- **Seed**: `42`
- **Fit Mode**: `fixed_configuration` (15 epoch CNN/LSTM, 6 epoch PhoBERT; không chia validation ngẫu nhiên từ Augmented vì thiếu lineage)
- **Quy mô dữ liệu**:
  - Base fit: 5.042 dòng (gốc: 5.100 dòng, loại 48 trùng và 23 giao test)
  - Augmented fit: 9.978 dòng (gốc: 10.149 dòng, loại 161 trùng, 33 giao test và 2 mâu thuẫn nhãn)
  - Test: đúng 1.050 mẫu độc lập (giữ nguyên gốc)
- **Preprocessing Policy**: `vlsp-eda-v2` (`runs/vlsp-eda-20261121/complete/artifacts/preprocessing_policy.json`)

## 2. Bảng tổng hợp kết quả thực nghiệm (12 lượt chạy trên 1.050 mẫu Test)

| Kiến trúc | Tập | Accuracy (%) | Precision macro (%) | Recall macro (%) | Macro-F1 (%) | Weighted F1 (%) | Tham số | Train (s) |
|---|---|---|---|---|---|---|---|---|
| **PhoBERT-base-v2** | **Base** | **78,10** | **77,94** | **78,10** | **77,91** | **77,91** | 135.000.579 | 417,1 |
| PhoBERT-base-v2 | Augmented | 77,81 | 77,75 | 77,81 | 77,77 | 77,77 | 135.000.579 | 831,1 |
| TF-IDF + LinearSVC | Base | 71,05 | 71,14 | 71,05 | 71,08 | 71,08 | 60.003 | 1,1 |
| TF-IDF + LinearSVC | Augmented | 70,95 | 70,92 | 70,95 | 70,94 | 70,94 | 60.003 | 1,8 |
| BiLSTM | Base | 68,76 | 69,02 | 68,76 | 68,77 | 68,77 | 3.879.779 | 31,5 |
| CNN+BiLSTM | Base | 68,48 | 68,80 | 68,48 | 68,57 | 68,57 | 3.894.243 | 37,7 |
| TextCNN | Augmented | 68,29 | 68,45 | 68,29 | 68,31 | 68,31 | 4.481.203 | 91,4 |
| TextCNN | Base | 67,90 | 69,10 | 67,90 | 67,92 | 67,92 | 4.122.003 | 47,4 |
| BiLSTM | Augmented | 67,62 | 68,05 | 67,62 | 67,72 | 67,72 | 4.238.979 | 61,3 |
| CNN+BiLSTM | Augmented | 65,33 | 68,25 | 65,33 | 64,89 | 64,89 | 4.253.443 | 75,3 |
| TF-IDF + 1D-CNN | Base | 33,33 | 11,11 | 33,33 | 16,67 | 16,67 | 50.307 | 133,3 |
| TF-IDF + 1D-CNN | Augmented | 33,33 | 11,11 | 33,33 | 16,67 | 16,67 | 50.307 | 270,8 |

*Ghi chú*: Kết quả TF-IDF + 1D-CNN đạt F1 16,67% là hoàn toàn dự kiến và được ghi rõ trong báo cáo vì phép tích chập dọc theo trục đặc trưng từ vựng không biểu diễn thứ tự tuần tự của từ.

## 3. Ảnh hưởng của tập tăng cường (Augmented Delta)

| Kiến trúc | Base F1 (%) | Augmented F1 (%) | Δ (điểm %) |
|---|---|---|---|
| TextCNN | 67,92 | 68,31 | +0,39 |
| TF-IDF + 1D-CNN | 16,67 | 16,67 | 0,00 |
| PhoBERT-base-v2 | 77,91 | 77,77 | -0,14 |
| TF-IDF + LinearSVC | 71,08 | 70,94 | -0,14 |
| BiLSTM | 68,77 | 67,72 | -1,05 |
| CNN+BiLSTM | 68,57 | 64,89 | -3,68 |

## 4. Đối chiếu với pipeline trước ngày 20/11/2026 (`20261120T161056Z`)

| Mô hình | Tập | F1 cũ (%) | F1 mới (%) | Chênh lệch (điểm %) |
|---|---|---|---|---|
| TF-IDF + LinearSVC | Base | 71,46 | 71,08 | -0,38 |
| TF-IDF + LinearSVC | Augmented | 71,43 | 70,94 | -0,49 |
| TF-IDF + 1D-CNN | Base | 16,67 | 16,67 | 0,00 |
| TF-IDF + 1D-CNN | Augmented | 16,67 | 16,67 | 0,00 |
| TextCNN | Base | 68,52 | 67,92 | -0,60 |
| TextCNN | Augmented | 69,20 | 68,31 | -0,89 |
| BiLSTM | Base | 68,08 | 68,77 | +0,69 |
| BiLSTM | Augmented | 68,37 | 67,72 | -0,65 |
| CNN+BiLSTM | Base | 67,41 | 68,57 | +1,16 |
| CNN+BiLSTM | Augmented | 64,80 | 64,89 | +0,09 |
| PhoBERT-base-v2 | Base | 77,59 | 77,91 | +0,32 |
| PhoBERT-base-v2 | Augmented | 77,65 | 77,77 | +0,12 |

## 5. Tệp tin và bằng chứng trong thư mục chạy

- `sentimentanalysis.ipynb`: Notebook nguồn dispatch.
- `sentimentanalysis_output.ipynb`: Notebook output gốc Colab (17 code cell, 0 error output).
- `execution.log`: Log chi tiết quá trình chạy Colab qua CLI.
- `launcher.log` & `launcher_pid.txt`: Log và PID của launcher detached.
- `driver.json`: Trạng thái thực thi (`passed`, `vm_released: true`).
- `selected-checkpoints.zip`: Lưu trữ 16 checkpoints (1,1 GB, Git ignored), khớp chính xác mã băm SHA-256 trong `model_files.json`.
- `artifacts/full-20261121T123956Z/`: Toàn bộ kết quả đầu ra (CSV, JSON, PNG) của 12 lượt chạy.

## 6. Trạng thái đồng bộ Website và Notebook

1. **Notebook thực thi đã kiểm chứng**:
   - `ipynb/text/sentimentanalysis.ipynb` đã được ghi nhận metadata `verified_execution` (run_id: `20261121T123956Z`, status: `passed`).
   - `pages/notebooks/sentimentanalysis.ipynb` khớp byte 100% với `ipynb/text/sentimentanalysis.ipynb` (1.826.345 bytes).
   - `pages/notebooks/sentimentanalysis_eda.ipynb` khớp byte 100% với `ipynb/text/sentimentanalysis_eda.ipynb` (668.022 bytes).
2. **Báo cáo Website**:
   - `pages/projects/text.html` cập nhật đầy đủ kết quả v2, bảng xử lý embedder-specific, 9 hình ảnh EDA CPU, 12 mô hình và đường học, phân tích lỗi, bảng đối chiếu pipeline cũ/mới và liên kết tải artifacts.
   - Tài nguyên đính kèm: `pages/assets/vlsp-sentiment/oxford/20261121T123956Z/` và `pages/assets/vlsp-sentiment/eda-v2/20261121T123956Z/`.
   - Giữ nguyên các tài nguyên PDF và YouTube ở trạng thái chờ liên kết.

## 7. Các lệnh kiểm chứng độc lập đã đạt

```sh
# Kiểm tra toàn bộ notebook, AST, outputs, recalculate metrics từ CSV và verify SHA-256 checkpoints
python -B scripts/validate_oxford_notebooks.py --require-executed --verify-checkpoints \
  --text-results runs/vlsp-eda-20261121/train-full/artifacts \
  --eda-results runs/vlsp-eda-20261121/complete/artifacts

# Kiểm tra tính toàn vẹn layout tĩnh và header/footer
python -B scripts/build_site.py --check

# Kiểm tra cú pháp JavaScript điều hướng
node --check pages/assets/navigation.js

# Kiểm tra diff Git không có lỗi định dạng/khoảng trắng
git diff --check
```
