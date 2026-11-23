# Bàn giao Text v3 Raincloud Six — Colab T4 Run All & Website Sync (22/11/2026)

Thực hiện theo giao thức Oxford Pets 11 mục, quy trình Raincloud Six: huấn luyện 3 nhóm kiến trúc cốt lõi (Linear baseline TF-IDF + SVD + LinearSVC, Recurrent CBOW + GRU, Transformer PhoBERT-base-v2) trên cả hai tập Base và Augmented (tổng cộng 6 lượt chạy), đánh giá trên đúng 1.050 mẫu kiểm thử VLSP chuẩn độc lập. Toàn bộ 6 lượt chạy trên Google Colab T4 đã hoàn tất 100% không lỗi, giải phóng VM (`vm_released: true`), artifacts và checkpoints đã được kiểm toán toàn diện và tích hợp vào notebook gốc cũng như website báo cáo.

---

## 1. Thông tin phiên chạy (Session Metadata)

- **Run ID**: `20261121T174533Z`
- **Thời gian hoàn tất**: 22/11/2026 (UTC: 2026-11-21T17:58:53Z; GMT+7: 22/11/2026 00:58:53)
- **Môi trường**: Google Colab T4 (GPU: Tesla T4, Python 3.13.16, PyTorch 2.14.1+cu130, Transformers 4.57.6, scikit-learn 1.6.1, Gensim 4.4.0)
- **Colab Session**: `raincloud-six-full-t4`, VM đã giải phóng (`vm_released: true`, driver status `passed`)
- **Seed**: `42`
- **Fit Mode**: `fixed_configuration` (4 epoch CBOW+GRU, 3 epoch PhoBERT; không chia validation ngẫu nhiên từ Augmented vì thiếu lineage)
- **Quy mô dữ liệu**:
  - Base fit: 5.042 dòng (gốc: 5.100 dòng, loại 48 trùng và 23 giao test)
  - Augmented fit: 9.978 dòng (gốc: 10.149 dòng, loại 161 trùng, 33 giao test và 2 mâu thuẫn nhãn)
  - Test: đúng 1.050 mẫu độc lập (giữ nguyên gốc)
- **Preprocessing Policy**: `vlsp-eda-v3-six-raincloud` (`runs/raincloud-six-20261121/eda-artifacts/preprocessing_policy.json`)

---

## 2. Bảng tổng hợp kết quả thực nghiệm (6 lượt chạy trên 1.050 mẫu Test)

| Kiến trúc | Tập | Accuracy (%) | Precision macro (%) | Recall macro (%) | Macro-F1 (%) | Weighted F1 (%) | Tham số | Train (s) | Inference (s) |
|---|---|---|---|---|---|---|---|---|---|
| **PhoBERT-base-v2** | **Augmented** | **77,43** | **77,30** | **77,43** | **77,25** | **77,25** | 135.000.579 | 410,2 | 4,67 |
| PhoBERT-base-v2 | Base | 76,29 | 76,08 | 76,29 | 75,99 | 75,99 | 135.000.579 | 198,4 | 4,69 |
| TF-IDF + SVD + LinearSVC | Augmented | 67,62 | 67,79 | 67,62 | 67,66 | 67,66 | 903 | 11,6 | 0,08 |
| TF-IDF + SVD + LinearSVC | Base | 66,76 | 67,02 | 66,76 | 66,85 | 66,85 | 903 | 7,6 | 0,10 |
| CBOW + GRU | Base | 64,86 | 64,74 | 64,86 | 64,74 | 64,74 | 3.730.467 | 13,6 | 0,17 |
| CBOW + GRU | Augmented | 62,86 | 66,13 | 62,86 | 62,88 | 62,88 | 4.089.667 | 16,8 | 0,16 |

---

## 3. Ảnh hưởng của tập tăng cường (Augmented Delta)

| Kiến trúc | Base F1 (%) | Augmented F1 (%) | Δ (điểm %) |
|---|---|---|---|
| PhoBERT-base-v2 | 75,99 | 77,25 | **+1,25** |
| TF-IDF + SVD + LinearSVC | 66,85 | 67,66 | **+0,81** |
| CBOW + GRU | 64,74 | 62,88 | **-1,86** |

---

## 4. Xử lý kỹ thuật: Khắc phục sự cố SVD(300) trên Colab Python 3.13

- **Hiện tượng**: Thuật toán mặc định `TruncatedSVD(n_components=300, algorithm='randomized')` gây crash khởi động lại kernel (`Kernel restarting before the code finished`) tại Cell 12 do xung đột đa luồng và tràn bộ nhớ trên môi trường Python 3.13.16 / Colab T4.
- **Giải pháp xử lý**:
  1. Giải phóng triệt để tiến trình Java JVM nền của `py_vncorenlp` (`pkill -f VnCoreNLP`) và thu dọn bộ nhớ (`release_memory()`).
  2. Chuyển sang thuật toán `algorithm='arpack'` có tính tất định cao và kiểm soát luồng thông qua `with threadpool_limits(limits=2):`.
  3. Kết quả: Quá trình fit SVD hoàn thành mượt mà trong ~7-11 giây, không gây tràn bộ nhớ hay gián đoạn kernel.

---

## 5. Tệp tin và bằng chứng trong thư mục chạy

- `sentimentanalysis.ipynb`: Notebook nguồn đã nạp giao thức Raincloud Six.
- `sentimentanalysis_output.ipynb`: Notebook output gốc Colab (17 code cell, 0 error output).
- `execution.log`: Toàn bộ nhật ký chạy Colab qua headless driver.
- `launcher.log` & `launcher_pid.txt`: Log và PID của phiên chạy detached.
- `driver.json`: Trạng thái thực thi (`passed`, `vm_released: true`).
- `selected-checkpoints.zip`: Lưu trữ 8 mô hình đã lưu (1,1 GB, Git ignored), khớp chính xác mã băm SHA-256 (`3feba1cf8d46c1dafdb7abac973eb4dccc3aa83da413bec8c61abf00a110007d`).
- `artifacts/full-20261121T174533Z/`: Toàn bộ kết quả đầu ra (CSV, JSON, PNG) của 6 lượt chạy.

---

## 6. Trạng thái đồng bộ Website và Notebook

1. **Notebook thực thi đã kiểm chứng**:
   - `ipynb/text/sentimentanalysis.ipynb` đã được ghi nhận metadata `verified_execution` (run_id: `20261121T174533Z`, status: `passed`).
   - `pages/notebooks/sentimentanalysis.ipynb` khớp byte 100% với `ipynb/text/sentimentanalysis.ipynb`.
   - `pages/notebooks/sentimentanalysis_eda.ipynb` khớp byte 100% với `ipynb/text/sentimentanalysis_eda.ipynb`.
2. **Báo cáo Website**:
   - `pages/projects/text.html` cập nhật đầy đủ kết quả v3 Raincloud Six, bảng xử lý embedder-specific, các biểu đồ phân phối và đường học, phân tích lỗi, và liên kết tải artifacts.
   - Tài nguyên đính kèm: `pages/assets/vlsp-sentiment/oxford/20261121T174533Z/` và `pages/assets/vlsp-sentiment/eda-v2/20261121T174533Z/`.
   - Giữ nguyên các tài nguyên PDF và YouTube ở trạng thái chờ liên kết.

---

## 7. Các lệnh kiểm chứng độc lập đã đạt

```sh
# Kiểm tra toàn bộ notebook, AST, outputs, recalculate metrics từ CSV và verify SHA-256 checkpoints
python -B scripts/validate_oxford_notebooks.py --require-executed --verify-checkpoints \
  --text-results runs/raincloud-six-20261121/train-full/artifacts \
  --eda-results runs/raincloud-six-20261121/eda-artifacts

# Kiểm tra tính toàn vẹn layout tĩnh và header/footer
python -B scripts/build_site.py --check

# Kiểm tra cú pháp JavaScript điều hướng
node --check pages/assets/navigation.js

# Kiểm tra diff Git không có lỗi định dạng/khoảng trắng
git diff --check
```
