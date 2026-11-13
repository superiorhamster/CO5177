# HƯỚNG DẪN BIÊN DỊCH BÁO CÁO TRÊN OVERLEAF

Báo cáo này được cấu trúc hoàn chỉnh để nộp cho môn học **CO5177 — Nền tảng lập trình cho phân tích và trực quan dữ liệu** (Nhóm **SlightSeek**).

---

## 1. Cấu trúc thư mục báo cáo

```
report/
├── main.tex                 # File mã nguồn LaTeX chính (chứa cả 3 phần: Tabular, Image, Text)
├── refs.bib                 # Danh mục tài liệu tham khảo (BibTeX: 10 trích dẫn chuẩn)
├── hcmut.png                # Logo Đại học Bách Khoa ĐHQG-HCM
├── OVERLEAF_README.md       # Tài liệu hướng dẫn này
└── figures/                 # Toàn bộ 18 hình ảnh thực nghiệm xuất từ notebook
    ├── tab_*.png            # 7 hình cho dữ liệu bảng Adult Census Income
    ├── img_*.png            # 6 hình cho dữ liệu ảnh Intel Image Classification
    └── txt_*.png            # 4 hình cho dữ liệu văn bản VLSP 2016 Sentiment
```

---

## 2. Cách tải lên và biên dịch trên Overleaf

### Bước 1: Nén thư mục và Tải lên Overleaf
1. Sử dụng file nén `SlightSeek-report-overleaf.zip` đã được đóng gói sẵn trong thư mục dự án (hoặc nén toàn bộ nội dung bên trong thư mục `report/` thành file `.zip`).
2. Truy cập [Overleaf](https://www.overleaf.com/) và đăng nhập.
3. Chọn **New Project** $\to$ **Upload Project**.
4. Kéo thả file `SlightSeek-report-overleaf.zip` vào để Overleaf tự động giải nén.

### Bước 2: Thiết lập Compiler trên Overleaf
1. Ở góc trên bên trái màn hình giao diện soạn thảo Overleaf, bấm vào nút **Menu**.
2. Tại mục **Settings**:
   - **Compiler:** Bạn có thể để mặc định là **pdfLaTeX** (khuyên dùng vì file mã nguồn đã tích hợp sẵn gói `vntex` tương thích 100% với TeX Live của Overleaf) hoặc chuyển sang **XeLaTeX**.
   - **TeX Live version:** Chọn phiên bản mới nhất (ví dụ: `2024` hoặc `2023`).
   - **Main document:** Đảm bảo chọn đúng `main.tex`.

### Bước 3: Biên dịch và Xuất file PDF
1. Bấm nút màu xanh **Recompile** (hoặc tổ hợp phím `Ctrl + Enter` / `Cmd + Enter`).
2. Kiểm tra tài liệu hiển thị ở khung bên phải:
   - Trang bìa trang trọng với logo HCMUT, tên giảng viên hướng dẫn, thông tin nhóm SlightSeek và 2 sinh viên (MSSV: 2310139 và 2310491).
   - Mục lục tự động 3 cấp đầy đủ.
   - Phần 1: Dữ liệu Bảng (Tabular) với bảng kết quả 5 mô hình và 7 hình biểu đồ EDA / Model.
   - Phần 2: Dữ liệu Ảnh (Image) với bảng kết quả MobileNetV3 / ViT và 6 hình biểu đồ.
   - Phần 3: Dữ liệu Văn bản (Text) với bảng kết quả 4 mô hình NLP và 4 hình biểu đồ.
   - Phần 4: Kết luận đồ án và bảng phân công đóng góp 100% của từng thành viên.
   - Danh mục tài liệu tham khảo theo chuẩn IEEEtran.
3. Bấm vào biểu tượng **Download PDF** cạnh nút Recompile.
4. Đổi tên file PDF tải về thành:
   ```text
   SlightSeek-report.pdf
   ```
   theo đúng quy cách yêu cầu tại mục §6.3 của `requirements.md`.
