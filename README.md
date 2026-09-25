# Website Báo Cáo Đồ Án Môn Học: Nền Tảng Lập Trình Cho Phân Tích & Trực Quan Dữ Liệu
> **Trường Đại học Bách Khoa - ĐHQG-HCM**  
> **Khoa Khoa học & Kỹ thuật Máy tính**  
> **Giảng viên phụ trách:** TS. Lê Thành Sách  
> **Học kỳ:** HK261 • Năm học 2026 - 2027  
> **Nhóm thực hiện:** `G6`  

---

## 📌 Giới Thiệu
Trang web học thuật (Academic Portfolio / Course Showcase) chuẩn Responsive, hiện đại và sạch sẽ, được xây dựng theo kiến trúc trang tĩnh (Static Multi-page Site) tối ưu 100% để triển khai trực tiếp trên **GitHub Pages** không cần build step phức tạp.

Website phục vụ trình bày toàn bộ kết quả thực nghiệm của 3 bài tập lớn con:
1. **Dữ liệu Dạng Bảng (Tabular Data):** Dự báo rủi ro tín dụng với LightGBM & SHAP (`tabular.html`).
2. **Dữ liệu Văn bản (Text / NLP):** Phân loại cảm xúc đa lớp tiếng Việt với PhoBERT & VnCoreNLP (`text.html`).
3. **Dữ liệu Hình ảnh (Computer Vision):** Nhận dạng bệnh học lá cây với Vision Transformer & Grad-CAM (`image.html`).

---

## 📂 Cấu Trúc Thư Mục
```text
.
├── index.html                   # Landing page tổng quan, thông tin nhóm, mục lục bài con
├── tabular.html                 # Trang báo cáo chi tiết bài tập dữ liệu dạng bảng
├── text.html                    # Trang báo cáo chi tiết bài tập dữ liệu văn bản
├── image.html                   # Trang báo cáo chi tiết bài tập dữ liệu hình ảnh
├── assets/
│   ├── css/
│   │   └── style.css            # Tùy biến Dark mode, scrollbar, responsive video, print styles
│   ├── js/
│   │   ├── main.js              # Xử lý Dark/Light mode (localStorage) & Mobile Drawer
│   │   └── charts.js            # Khởi tạo biểu đồ tương tác Chart.js (tự đổi màu theo theme)
│   ├── images/
│   │   ├── bk-logo.svg          # Logo Trường ĐH Bách Khoa TP.HCM (HCMUT)
│   │   └── cse-logo.svg         # Logo Khoa KH&KT Máy tính (CSE)
│   └── reports/
│       └── README.md            # Nơi đặt các tệp báo cáo PDF ([groupname]-report.pdf, ...)
└── README.md                    # Tài liệu hướng dẫn sử dụng và triển khai
```

---

## 🚀 Hướng Dẫn Triển Khai Lên GitHub Pages (Trong 2 Phút)

### Bước 1: Đẩy mã nguồn lên GitHub Repository
```bash
git init
git add .
git commit -m "feat: complete academic showcase website for GitHub Pages"
git branch -M main
git remote add origin https://github.com/[YOUR_USERNAME]/[REPO_NAME].git
git push -u origin main
```

### Bước 2: Kích hoạt GitHub Pages trên Repository
1. Mở trang Repository của bạn trên GitHub (`https://github.com/[YOUR_USERNAME]/[REPO_NAME]`).
2. Vào tab **Settings** &rarr; Chọn mục **Pages** ở thanh điều hướng bên trái.
3. Tại phần **Build and deployment**:
   - **Source:** Chọn `Deploy from a branch`.
   - **Branch:** Chọn `main` và thư mục `/(root)`.
4. Bấm **Save**. 
5. Đợi khoảng 1-2 phút, trang web của bạn sẽ hoạt động tại địa chỉ:
   ```text
   https://[YOUR_USERNAME].github.io/[REPO_NAME]/
   ```

---

## 🔍 Hướng Dẫn Thay Thế Dữ Liệu Thực Tế (Placeholders Checklist)

Tìm kiếm nhanh trong mã nguồn các từ khóa sau để thay thế bằng thông tin chính thức của nhóm:

| Placeholder | Ý Nghĩa / Vị trí thay thế | Ví dụ thực tế |
| :--- | :--- | :--- |
| `[GROUP_NAME]` | Tên nhóm đồ án | `Group 08 - DataHawks` |
| `[HỌ VÀ TÊN 1..4]` | Họ và tên sinh viên | `Nguyễn Văn A` |
| `[MSSV_1..4]` | Mã số sinh viên | `2210123` |
| `[GITHUB_USER_1..4]`| Username GitHub của từng thành viên | `nguyenvana-bk` |
| `[YOUR_USERNAME]` | Username GitHub chứa repository đồ án | `bachkhoa-data-team` |
| `[REPO_NAME]` | Tên repository GitHub | `assignment-data-analysis` |
| `[YOUR_COLAB_NOTEBOOK_ID]` | ID hoặc Link Notebook trên Google Colab | `1xYz...` |
| `[YOUTUBE_VIDEO_ID]` | Mã định danh video thuyết trình YouTube | `dQw4w9WgXcQ` |
| `[groupname]-report.pdf` | Tệp báo cáo PDF đồ án nộp kèm | Đặt file vào `assets/reports/` |

---

## 💻 Xem Thử Nghiệm Tại Máy Cục Bộ (Local Preview)

Do sử dụng thuần HTML5/Tailwind CDN/Vanilla JS, bạn có thể xem trang web ngay lập tức mà không cần cài đặt Node.js hay bất kỳ build tool nào:
- **Cách 1:** Nhấp đúp chuột trực tiếp vào tệp `index.html` để mở trong trình duyệt Chrome / Firefox / Safari.
- **Cách 2 (Khuyến nghị với Local Server):**
  ```bash
  # Chạy máy chủ tĩnh đơn giản với Python 3:
  python3 -m http.server 8080
  # Mở trình duyệt và truy cập: http://localhost:8080
  ```

---

## ✨ Điểm Nổi Bật Đáp Ứng Rubric Môn Học
- **Kiến trúc Multi-page:** Điều hướng mượt mà, phân tách rõ ràng từng bài toán không bị dồn nén mất mục lục.
- **Dark / Light Mode:** Tự động phát hiện cài đặt hệ điều hành và lưu tùy chọn vào `localStorage`. Biểu đồ tương tác Chart.js tự động chuyển màu đường lưới và nhãn trục theo theme.
- **Resource Bar Chuẩn Mực:** Cung cấp đầy đủ các nút truy cập nhanh: Colab (Badge SVG nổi bật), GitHub Notebook, Báo cáo PDF phân mục và Video thuyết trình 16:9.
- **Rubric 10 Sáng tạo:** Có đầy đủ bảng so sánh chỉ số định lượng (Accuracy, F1, AUC, Latency), biểu đồ trực quan, phân tích mẫu lỗi (Failure Mode Analysis) và giải thích mô hình bằng XAI (SHAP & Grad-CAM).
