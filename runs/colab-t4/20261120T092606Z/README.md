# Bàn giao notebook Oxford Pets — 20/11/2026

Đã chuẩn hóa hai notebook thành 11 mục, chạy smoke test và Run all đầy đủ trên Colab T4, seed 42. Kết quả và bản tải xuống trên website đã đồng bộ trong workspace.

| Bài | Lượt chạy được bàn giao | Kết quả tốt nhất trên test |
| --- | --- | --- |
| Text | `full-20261120T161056Z`: 6 kiến trúc × Base/Augmented = 12 | PhoBERT-base-v2 Augmented: accuracy 77,81%; macro-F1 77,65%; 1.050 mẫu |
| Image | `20261120T092606Z`: MobileNetV3-Small và ViT-B/16 | ViT-B/16: accuracy 94,50%; macro-F1 94,63%; 3.000 ảnh |

Text thiếu lineage nên dùng toàn bộ tập fit đã làm sạch, không có validation, 15 epoch CNN/LSTM và 6 epoch PhoBERT. Kết quả TF-IDF + CNN thấp được giữ nguyên; tích chập theo trục từ vựng không thể hiện thứ tự từ. Thứ hạng chỉ mô tả lần chạy seed 42 này.

## Notebook, báo cáo và bằng chứng

- [Notebook Text](../../../ipynb/text/sentimentanalysis.ipynb) và [báo cáo Text](../../../pages/projects/text.html).
- [Notebook Image](../../../ipynb/image/intel_image_classification_trained.ipynb) và [báo cáo Image](../../../pages/projects/image.html).
- [Artifacts Text](text/full-retry/artifacts/full-20261120T161056Z/) gồm predictions, summary, per-class metrics, confusion matrices, history, split manifest, audit, thông tin nguồn và giải thích.
- [Artifacts Image](image/full/artifacts/full/) gồm dự đoán/metrics ba split, bảng so sánh, history, split manifest, audit, thông tin nguồn và Grad-CAM.
- [Log Text](text/full-retry/execution.log) và [log Image](image/full/execution.log); output gốc nằm cạnh notebook input trong từng thư mục full.
- Checkpoint cục bộ: `text/full-retry/selected-checkpoints.zip` và `image/full/selected-checkpoints.zip`. Các ZIP này được Git ignore, không liên kết từ website. SHA-256 nằm trong `model_files.json` của mỗi thư mục artifacts.

Text cuối dùng thư mục `full-retry`; `text/full` là lượt trước, không có bộ artifacts đầy đủ và không dùng cho website. Các thư mục smoke chỉ phục vụ kiểm tra kỹ thuật.

Notebook bàn giao bỏ các thanh tiến trình tạm thời, giữ bảng/hình và log epoch; output gốc vẫn được giữ riêng. Colab CLI không ghi `execution_count`, vì vậy trường này được giữ null. `metadata.verified_execution` gắn output với mã nguồn, log, artifacts và SHA-256; không tự tạo execution count.

Hoàn tất Text (UTC): `2026-11-20T16:40:48.724776+00:00`. Hoàn tất Image (UTC): `2026-11-20T11:09:26.600692+00:00`.

## Kiểm tra đã đạt

- Đúng 11 mục; AST và nbformat hợp lệ; 17 cell mã Text và 34 cell mã Image chạy tuần tự, không có output lỗi.
- Smoke đủ 12 cấu hình Text và hai mô hình Image; kiểm tra protocol thiếu/có lineage, lọc giao test và schema.
- Tính lại accuracy, precision/recall/F1 macro, weighted F1, support từng lớp và confusion matrix từ dự đoán; đối chiếu cùng sample_id/nhãn. Image kiểm tra cả ba split.
- Checkpoint nạp lại cho dự đoán nhất quán; embedding độc lập và pooling bỏ padding; giải thích không đổi trọng số.
- 16 tệp Text và hai checkpoint Image tải về khớp SHA-256.
- Notebook nguồn/bản tải xuống byte-equal; website dùng artifacts mới; ID không trùng, liên kết và fragment cục bộ hợp lệ.
- `python -B scripts/build_site.py --check`, `node --check pages/assets/navigation.js`, `git diff --check`.
- Xem trên desktop và mobile 390×844: bảng cuộn bằng bàn phím, không tràn trang, Escape đóng điều hướng và trả focus. Ảnh chụp nằm trong thư mục visualizations của phiên làm việc.

Chạy lại kiểm chứng từ thư mục gốc repository:

```sh
python -B scripts/validate_oxford_notebooks.py --require-executed --verify-checkpoints \
  --text-results runs/colab-t4/20261120T092606Z/text/full-retry/artifacts/full-20261120T161056Z \
  --image-results runs/colab-t4/20261120T092606Z/image/full/artifacts/full
```

Tự chạy Colab và thu artifacts ngay sau khi hoàn tất bằng `scripts/run_colab_notebook.py`; script tạo T4 riêng và giải phóng VM sau khi tải xong. Hai phiên T4 của lần bàn giao đã giải phóng.

Phạm vi hiện tại là workspace. PDF/video giữ trạng thái cũ; chưa commit, push hoặc triển khai website.
