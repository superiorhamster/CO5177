# Kịch bản thuyết trình notebook · SlightSeek

Mỗi kịch bản dài khoảng 5 phút, tính cả thời gian chỉ vào bảng và chuyển cell. Mở notebook có output trước khi quay. Dòng *Màn hình* là chỉ dẫn thao tác.

- [Kịch bản notebook Text](#text)
- [Kịch bản notebook Image](#image)

## Text

[Mở notebook phân loại cảm xúc tiếng Việt](../ipynb/text/sentimentanalysis_pipeline_comparison.ipynb)

### 0:00–0:30 · Bài toán và dữ liệu

*Màn hình — Bắt đầu ở tiêu đề notebook, rồi mở bảng đếm nhãn ở mục `1. Nạp dữ liệu và kiểm tra schema`.*

Em chào thầy cô và các bạn. Em đại diện nhóm SlightSeek trình bày notebook phân loại cảm xúc tiếng Việt trên VLSP phiên bản 5. Mỗi văn bản thuộc một trong ba nhãn, tiêu cực, trung lập hoặc tích cực. Nhóm chạy ba pipeline trên dữ liệu gốc và dữ liệu tăng cường. Cả sáu cấu hình dùng chung 1.050 câu test, với 350 câu cho mỗi nhãn.

### 0:30–1:25 · EDA và làm sạch

*Màn hình — Chỉ đường phân phối ở mục `2. Độ dài văn bản gốc`, rồi dừng vài giây ở cột giao test trong bảng audit bên dưới cell `normalize_text`.*

Hình này cho thấy phân phối độ dài của từng nhãn. Tại mốc 95% trên trục dọc, lớp trung lập có độ dài khoảng 416 ký tự. Ở đuôi phân phối, câu dài nhất có hơn 13 nghìn ký tự. Vì vậy, nhóm đo lại độ dài sau khi tách từ và mã hóa token trước khi nhận xét về giới hạn đầu vào.

Ở cell này, nhóm chuẩn Unicode và đưa những cách viết như “ko” về “không”, đồng thời giữ dấu tiếng Việt và nghĩa phủ định. Sau chuẩn hóa, nhóm phát hiện 34 dòng Base và 48 dòng Augmented có nội dung giao với test. Nhóm loại các dòng đó khỏi dữ liệu phát triển để giảm rò rỉ dữ liệu. Khóa văn bản chuẩn hóa giúp phát hiện cả những dòng chỉ khác cách viết.

### 1:25–2:10 · Tập fit và kiểm tra tokenizer

*Màn hình — Mở `Phân bố nhãn và audit dữ liệu`. Sau đó nhảy đến `Kiểm tra ngưỡng đầu vào theo tokenizer` ở mục 6.3.*

Sau lọc, Base còn 5.022 câu và Augmented còn 9.934 câu để fit. Phiên bản dữ liệu này thiếu thông tin nối mẫu tăng cường về câu gốc. Notebook chạy với siêu tham số và số epoch cố định cho từng nhánh, rồi chấm trên tập test đã giữ riêng.

Ở hình tokenizer, đường mốc 256 áp dụng cho hai cách đếm. Với PyVi, 18 câu Base vượt 256 từ. Với PhoBERT, 22 câu vượt 256 token BPE, tính cả token đặc biệt. Cả hai tỷ lệ đều dưới nửa phần trăm trên Base fit. Các câu vượt mốc có thể mất phần cuối khi đưa vào mô hình.

### 2:10–3:25 · Ba pipeline và cách huấn luyện

*Màn hình — Quay lại mục `6.1`. Lần lượt chỉ cell TF-IDF, phần `CBOWGRU` ở `6.2` và cell `Trainer` ở `6.3`.*

Nhánh đầu dùng PyVi để tách từ, rồi dùng TF-IDF cho từ đơn và cụm hai từ như “không tốt”. Notebook giữ ma trận TF-IDF ở dạng thưa với kiểu float32 để tiết kiệm bộ nhớ, giảm chiều bằng TruncatedSVD rồi fit LinearSVC. Từ vựng, IDF và phép giảm chiều đều học riêng từ từng tập fit.

Nhánh thứ hai đưa chuỗi vector Word2Vec CBOW vào GRU. DataLoader gom tối đa 64 câu một batch. Notebook truyền độ dài thật để GRU bỏ qua phần đệm, rồi dùng trạng thái ẩn cuối để phân loại. GRU nhận trực tiếp chiều của vector CBOW.

Nhánh thứ ba tách từ bằng RDRSegmenter rồi mã hóa BPE. PhoBERT đệm theo câu dài nhất trong từng batch. Cả Base và Augmented đều bắt đầu từ cùng trọng số PhoBERT pretrained và fine-tune trong ba epoch.

### 3:25–4:40 · Đọc bảng và ma trận nhầm lẫn

*Màn hình — Mục `7. Xuất bằng chứng và đọc kết quả`. Chỉ bảng tổng hợp, rồi dừng ở ma trận PhoBERT Augmented, hàng `neutral`, cột `negative`.*

Macro‑F1 lấy trung bình F1 của ba nhãn với trọng số bằng nhau. Trong bảng test, PhoBERT Augmented có Macro‑F1 cao nhất, 77,93%, và Accuracy 78,19%. So với Base, Macro‑F1 của cấu hình này tăng 0,65 điểm phần trăm. Cùng phép so sánh đó, CBOW cộng GRU tăng 1,28 điểm và nhánh TF-IDF giảm khoảng 1,61 điểm.

Ở bảng từng lớp của PhoBERT Augmented, trung lập có F1 thấp nhất, 70,41%. Trên ma trận, hàng là nhãn thật và cột là nhãn dự đoán. Có 72 trong số 350 câu trung lập bị dự đoán thành tiêu cực. Một dạng lỗi khác là đảo thẳng từ tiêu cực sang tích cực hoặc ngược lại. PhoBERT Augmented mắc lỗi này ở 4,86% số câu có nhãn thật thuộc hai cực.

### 4:40–5:00 · Kết luận

*Màn hình — Giữ ma trận nhầm lẫn và dòng thông báo nơi lưu kết quả.*

Trong lần chạy trên Colab T4, PhoBERT Augmented dẫn đầu sáu cấu hình. Notebook lưu dự đoán và chỉ số từng lớp để nhóm có thể xem lại các lỗi trung lập. Em cảm ơn thầy cô và các bạn đã theo dõi.

## Image

[Mở notebook phân loại ảnh cảnh Intel](../ipynb/image/intel_image_classification_trained.ipynb)

### 0:00–0:30 · Bài toán và dữ liệu

*Màn hình — Bắt đầu ở tiêu đề, rồi mở lưới ảnh mẫu ở mục `3. EDA trên ảnh gốc`.*

Em chào thầy cô và các bạn. Em đại diện nhóm SlightSeek trình bày notebook phân loại ảnh cảnh trên bộ Intel phiên bản 2. Mỗi ảnh thuộc một trong sáu lớp. Nhóm so sánh MobileNetV3-Small và ViT-B/16 bằng cùng dữ liệu. Trên lưới ảnh mẫu, glacier và mountain đều có thể chứa núi hoặc tuyết. Em sẽ quay lại cặp này khi đọc kết quả test.

### 0:30–1:25 · EDA và audit ảnh

*Màn hình — Mục `3.2. Kích thước, màu và chất lượng ảnh`. Chỉ cột `median`, rồi dừng vài giây ở một ảnh cực trị.*

Bảng kích thước cho thấy cạnh ngắn trung vị là 150 pixel. Trong tập train gốc có 26 ảnh với cạnh ngắn dưới 128 pixel. Nhóm đưa ảnh về 224 nhân 224 để khớp đầu vào của mô hình pretrained. Khi phóng lớn ảnh nhỏ, lượng chi tiết từ ảnh gốc vẫn giữ nguyên. Biểu đồ tỷ lệ khung hình cho thấy vì sao bước crop cần được kiểm tra cùng nội dung ảnh.

Ở các đồ thị chất lượng, brightness đo độ sáng trung bình, contrast đo mức phân tán của giá trị xám, còn Laplacian variance cho biết mức biến thiên tại các cạnh. Chẳng hạn, một cảnh có nhiều mặt biển phẳng có thể cho chỉ số cạnh thấp. Nhóm xem các ảnh cực trị để đọc các chỉ số trong ngữ cảnh của từng cảnh.

### 1:25–2:20 · Làm sạch, chia tập và DataLoader

*Màn hình — Chỉ bảng lý do loại ảnh ở `4.2`, sau đó mở hình trong `Xuất EDA và kiểm tra transform` ở mục 5.*

Nhóm dùng hash pixel để phát hiện ảnh trùng chính xác. Từ tập train gốc, nhóm loại 28 ảnh, gồm ba ảnh trùng test, 20 ảnh trong nhóm mâu thuẫn nhãn và năm bản sao cùng nhãn. Sau đó, nhóm chia theo tỷ lệ từng lớp thành 11.204 ảnh train và 2.802 ảnh validation, đồng thời giữ 3.000 ảnh test gốc. Notebook kiểm tra các tập đã chia có đủ sáu lớp và không có hash pixel giao nhau.

`SceneDataset` đọc ảnh RGB và dùng transform của từng tập. Khi train, mỗi batch có 16 ảnh. Notebook crop ngẫu nhiên, lật ngang và đổi màu nhẹ. Validation và test dùng resize, crop giữa và chuẩn hóa ImageNet. Trên hình, hãy nhìn phần cảnh còn lại sau khi crop. Hình minh họa dùng cùng transform với DataLoader và dùng seed cố định để tái tạo ví dụ.

### 2:20–3:25 · Huấn luyện và chọn checkpoint

*Màn hình — Mở `6.5. Điều phối hai giai đoạn và chọn checkpoint cuối`. Sau đó chỉ bảng và đường học ViT ở mục `8.3`.*

Hai mô hình bắt đầu từ trọng số ImageNet. MobileNet trích đặc trưng bằng các lớp tích chập. ViT chia ảnh thành các patch 16 nhân 16 rồi xử lý chuỗi patch. Cả hai có đầu phân loại sáu lớp.

Trong ba epoch đầu, nhóm khóa backbone và chỉ huấn luyện classifier. Sau đó, nhóm mở toàn bộ backbone để fine-tune với learning rate nhỏ. Notebook cho phép tối đa 15 epoch fine-tuning và dừng sớm khi bốn epoch liên tiếp không cải thiện Macro‑F1 trên validation. Trong lần chạy Colab T4 này, MobileNet nạp lại checkpoint đã lưu ở epoch fine-tuning thứ 9. Với ViT, bảng cho thấy Macro‑F1 trên validation tăng từ 93,39% sau giai đoạn classifier lên 95,00% tại checkpoint được chọn ở epoch fine-tuning thứ 7.

### 3:25–4:40 · Đánh giá trên test và đọc lỗi

*Màn hình — Mở `8.4. Câu hỏi 2 — đánh giá ViT trên ảnh chưa thấy`. Chỉ dòng `test`, rồi cuộn đến ma trận nhầm lẫn và lưới ảnh sai.*

Trên cùng 3.000 ảnh test, MobileNet đạt 92,53% Macro‑F1. ViT đạt 94,63% Macro‑F1, 94,50% Accuracy và 94,65% Balanced Accuracy. Balanced Accuracy lấy trung bình Recall của sáu lớp. Ở dòng test của ViT, Top‑2 đạt 99,37%, tức nhãn thật xuất hiện trong hai dự đoán có điểm cao nhất ở 99,37% số ảnh. Bảng bên dưới cho biết Precision, Recall và F1 của từng lớp. Chẳng hạn, ViT nhận đúng 89,15% ảnh thật sự thuộc lớp glacier.

Trong ma trận, hàng biểu diễn nhãn thật và cột biểu diễn dự đoán. Ở hàng glacier, ViT xếp nhầm 50 trong số 553 ảnh sang mountain. Ta có thể xem lưới ảnh dự đoán sai để kiểm tra các dấu hiệu như núi và tuyết mà hai lớp cùng có.

### 4:40–5:00 · Kết luận

*Màn hình — Mở mục `10. Kiểm tra nhất quán của từng bài đã chạy` và giữ hai dòng kết quả.*

ViT đạt Macro‑F1 cao nhất trong lần chạy với seed 42. Notebook kiểm tra tính nhất quán giữa checkpoint và kết quả của cả hai mô hình. Em cảm ơn thầy cô và các bạn đã theo dõi.
