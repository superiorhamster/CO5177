import ast
import json
from pathlib import Path

cells = []

def add_md(content):
    lines = [l + "\n" for l in content.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    })

def add_code(code_str):
    # Strictly validate code syntax using ast.parse
    ast.parse(code_str)
    lines = [l + "\n" for l in code_str.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    })

# ==============================================================================
# Cell 1: Section Header Markdown
# ==============================================================================
add_md("""## ⚙️ Architecture & 🧪 Experiments: Trích xuất Đặc trưng TF-IDF & Các Mô hình Baseline

Phần này xây dựng hệ thống các mô hình cơ sở (baselines) dựa trên phương pháp trích xuất đặc trưng thống kê n-gram truyền thống **TF-IDF (Term Frequency - Inverse Document Frequency)**.

Các mô hình baseline này thiết lập ngưỡng chuẩn (benchmark) định lượng để đối sánh với các kiến trúc mạng nơ-ron sâu (TextCNN, BiLSTM, CNN+BiLSTM) và mô hình ngôn ngữ ngữ cảnh hóa tiền huấn luyện (PhoBERT-large) ở các phần tiếp theo:
1. **⚙️ Architecture: Trích xuất Đặc trưng TF-IDF**: Xây dựng không gian biểu diễn thống kê 5,000 chiều từ unigram và bigram với kỹ thuật làm mượt dưới tuyến tính (`sublinear_tf=True`).
2. **🧪 Experiments: Baseline 1 - LinearSVC (Calibrated)**: Mô hình phân loại tuyến tính cổ điển với biên phân chia cực đại và hiệu chỉnh xác suất `CalibratedClassifierCV`.
3. **⚙️ Architecture & 🧪 Experiments: Baseline 2 - TFIDF_CNN_Model (1D-CNN)**: Mạng nơ-ron tích chập 1 chiều trích xuất tổ hợp đặc trưng cục bộ trên vector TF-IDF, huấn luyện trong 15 epochs.""")

# ==============================================================================
# Cell 2: TF-IDF Markdown Explanation
# ==============================================================================
add_md("""### ⚙️ Architecture: Trích xuất Đặc trưng TF-IDF (N-gram Range 1-2)

- **Nội dung thực hiện (What this step does)**:
  - Khởi tạo bộ trích xuất đặc trưng `TfidfVectorizer` với cấu hình chuẩn: `max_features=5000`, `ngram_range=(1, 2)` (kết hợp cả từ đơn và cụm 2 từ liền kề), và `sublinear_tf=True` (áp dụng thang đo tần suất logarit $1 + \\log(\\text{tf})$).
  - Khớp từ vựng trên dữ liệu huấn luyện `train_df['Data']` và chuyển đổi cả tập huấn luyện (`X_train_tfidf`) lẫn kiểm thử (`X_test_tfidf`).
  - Đồng bộ hóa nhãn cảm xúc về thang số `[0, 1, 2]` tương ứng với `[Negative: 0, Neutral: 1, Positive: 2]`.

- **Ý nghĩa & Lý do lựa chọn (Why it matters)**:
  - `ngram_range=(1, 2)` đóng vai trò tối quan trọng trong phân tích cảm xúc tiếng Việt: nó bảo toàn các cụm từ phủ định và tăng cấp độ cảm xúc (ví dụ: *không thích*, *rất tốt*, *quá tệ*, *hài lòng*), khắc phục hạn chế mất mát ngữ cảnh của mô hình Bag-of-Words thuần túy.
  - `sublinear_tf=True` giúp triệt tiêu hiện tượng từ lặp nhiều lần trong các bài đánh giá dài áp đảo trọng số của toàn văn bản.
  - Tạo không gian đặc trưng thưa 5,000 chiều có kiểm soát, tối ưu hóa tốc độ huấn luyện mà vẫn giữ trọn vẹn các tín hiệu từ vựng phân biệt.

- **Câu hỏi nghiên cứu được giải quyết (Questions it answers)**:
  - Không gian đặc trưng TF-IDF trích xuất có độ thưa (sparsity) bao nhiêu phần trăm?
  - Kích thước ma trận đặc trưng của tập train và test sau khi trích xuất đạt bao nhiêu?
  - Phân phối nhãn sau khi đồng bộ hóa có cân bằng trên cả tập train và tập test không?""")

# ==============================================================================
# Cell 3: TF-IDF Feature Extraction Code
# ==============================================================================
tfidf_code = '''# ==============================================================================
# ⚙️ Architecture: Trích xuất Đặc trưng N-gram TF-IDF
# ==============================================================================
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Khởi tạo TF-IDF Vectorizer theo cấu hình chuẩn
tfidf_vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True
)

# 2. Fit trên tập train và transform trên tập train & test
# Sử dụng văn bản đã được tiền xử lý và làm sạch: train_df['Data'] và test_df['Data']
X_train_tfidf = tfidf_vectorizer.fit_transform(train_df['Data'])
X_test_tfidf = tfidf_vectorizer.transform(test_df['Data'])

# 3. Đồng bộ hóa nhãn về thang [0, 1, 2] (0: Negative, 1: Neutral, 2: Positive)
if train_df['Class'].min() < 0:
    y_train_tfidf = (train_df['Class'] + 1).values.astype(np.int64)
    y_test_tfidf = (test_df['Class'] + 1).values.astype(np.int64)
else:
    y_train_tfidf = train_df['Class'].values.astype(np.int64)
    y_test_tfidf = test_df['Class'].values.astype(np.int64)

# 4. Đo lường thống kê không gian đặc trưng
feature_names = tfidf_vectorizer.get_feature_names_out()
sparsity = 100.0 * (1.0 - X_train_tfidf.nnz / (X_train_tfidf.shape[0] * X_train_tfidf.shape[1]))

print("=" * 65)
print("⚙️ KẾT QUẢ TRÍCH XUẤT ĐẶC TRƯNG TF-IDF (N-GRAM 1-2)")
print("=" * 65)
print(f"Kích thước ma trận Train (X_train_tfidf) : {X_train_tfidf.shape[0]:,} mẫu x {X_train_tfidf.shape[1]:,} chiều")
print(f"Kích thước ma trận Test  (X_test_tfidf)  : {X_test_tfidf.shape[0]:,} mẫu x {X_test_tfidf.shape[1]:,} chiều")
print(f"Tổng số n-grams trong từ vựng            : {len(feature_names):,} (Unigrams + Bigrams)")
print(f"Độ thưa của ma trận train (Sparsity)     : {sparsity:.2f}%")
print(f"Phân phối nhãn Train [Lớp 0, 1, 2]       : {np.bincount(y_train_tfidf).tolist()}")
print(f"Phân phối nhãn Test  [Lớp 0, 1, 2]       : {np.bincount(y_test_tfidf).tolist()}")
print(f"10 đặc trưng đầu tiên trong từ vựng      : {list(feature_names[:10])}")
print("=" * 65)
'''
add_code(tfidf_code)

# ==============================================================================
# Cell 4: LinearSVC Markdown Explanation
# ==============================================================================
add_md("""### 🧪 Experiments: Baseline 1 - Phân loại Tuyến tính Hỗ trợ Vector (TF-IDF + LinearSVC)

- **Nội dung thực hiện (What this step does)**:
  - Huấn luyện mô hình Support Vector Classifier tuyến tính `LinearSVC(C=1.0, random_state=42, max_iter=2000)` kết hợp bộ chuẩn hóa xác suất `CalibratedClassifierCV(LinearSVC(...))` trên toàn bộ ma trận đặc trưng `X_train_tfidf`.
  - Dự đoán nhãn phân loại trên tập kiểm thử độc lập `X_test_tfidf`.
  - Thu thập đầy đủ các chỉ số hiệu năng chuẩn: Accuracy, Macro Precision/Recall/F1, Weighted Precision/Recall/F1 và xuất báo cáo chi tiết theo từng lớp cảm xúc.
  - Lưu kết quả vào biến dùng chung `results["TF-IDF + LinearSVC"]` và lưu cặp nhãn `(y_true, y_pred)` vào `all_predictions["TF-IDF + LinearSVC"]` phục vụ trực quan hóa ma trận nhầm lẫn tổng hợp.

- **Ý nghĩa & Lý do lựa chọn (Why it matters)**:
  - Linear SVM là chuẩn mực (gold standard) của học máy truyền thống trong không gian văn bản thưa nhiều chiều: nguyên lý biên phân chia cực đại (maximum-margin hyperplane) giúp mô hình chống hiện tượng overfitting hiệu quả ngay cả khi số lượng đặc trưng ($D=5,000$) tương đương quy mô mẫu huấn luyện ($N=5,100$).
  - `CalibratedClassifierCV` sử dụng kỹ thuật hồi quy sigmoid Platt scaling để chuyển đổi điểm khoảng cách lề thành xác suất phân loại tin cậy mà không làm biến dạng ranh giới quyết định.

- **Câu hỏi nghiên cứu được giải quyết (Questions it answers)**:
  - Một mô hình phân loại tuyến tính thuần túy với đặc trưng n-gram TF-IDF có thể đạt độ chính xác và Macro F1 bao nhiêu trên tập test VLSP 2016?
  - F1-score của lớp Neutral có chênh lệch đáng kể so với hai lớp phân cực Positive và Negative hay không?
  - Tốc độ huấn luyện và suy luận của LinearSVC so với các mạng nơ-ron sâu chênh lệch ra sao?""")

# ==============================================================================
# Cell 5: LinearSVC Baseline Code
# ==============================================================================
svc_code = '''# ==============================================================================
# 🧪 Experiments: Baseline 1 - TF-IDF + LinearSVC (Calibrated)
# ==============================================================================
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report

# 1. Khởi tạo mô hình LinearSVC và bao bọc bằng CalibratedClassifierCV
base_svc = LinearSVC(C=1.0, random_state=42, max_iter=2000)
calibrated_svc = CalibratedClassifierCV(base_svc)

# 2. Huấn luyện mô hình trên ma trận đặc trưng TF-IDF
print("Đang huấn luyện mô hình TF-IDF + LinearSVC (Calibrated)...")
calibrated_svc.fit(X_train_tfidf, y_train_tfidf)

# 3. Dự đoán trên tập kiểm thử (Test Set)
y_pred_svc = calibrated_svc.predict(X_test_tfidf)

# 4. Tính toán bộ chỉ số đánh giá toàn diện
svc_metrics = {
    "accuracy": accuracy_score(y_test_tfidf, y_pred_svc),
    "precision_macro": precision_score(y_test_tfidf, y_pred_svc, average="macro", zero_division=0),
    "recall_macro": recall_score(y_test_tfidf, y_pred_svc, average="macro", zero_division=0),
    "f1_macro": f1_score(y_test_tfidf, y_pred_svc, average="macro", zero_division=0),
    "precision_weighted": precision_score(y_test_tfidf, y_pred_svc, average="weighted", zero_division=0),
    "recall_weighted": recall_score(y_test_tfidf, y_pred_svc, average="weighted", zero_division=0),
    "f1_weighted": f1_score(y_test_tfidf, y_pred_svc, average="weighted", zero_division=0),
}

# 5. Lưu trữ kết quả đồng bộ cho bảng so sánh tổng hợp
if "results" not in globals():
    results = {}
results["TF-IDF + LinearSVC"] = svc_metrics

if "all_predictions" not in globals():
    all_predictions = {}
all_predictions["TF-IDF + LinearSVC"] = (y_test_tfidf, y_pred_svc)

# 6. Hiển thị báo cáo kết quả
print("=" * 65)
print("🧪 KẾT QUẢ ĐÁNH GIÁ BASELINE 1: TF-IDF + LinearSVC")
print("=" * 65)
for metric_name, val in svc_metrics.items():
    print(f"  {metric_name:<22}: {val * 100:.2f}%")
print("-" * 65)
print("\\nBáo cáo phân loại chi tiết (Classification Report):")
print(classification_report(
    y_test_tfidf,
    y_pred_svc,
    target_names=['Negative (-1)', 'Neutral (0)', 'Positive (1)'],
    digits=4
))
print("=" * 65)
'''
add_code(svc_code)

# ==============================================================================
# Cell 6: 1D-CNN Architecture Markdown Explanation
# ==============================================================================
add_md("""### ⚙️ Architecture: Baseline 2 - Mạng Nơ-ron TF-IDF + 1D-CNN (TFIDF_CNN_Model)

- **Nội dung thực hiện (What this step does)**:
  - Thiết kế kiến trúc mạng nơ-ron tích chập 1 chiều `TFIDF_CNN_Model` kế thừa từ `nn.Module` trong PyTorch, nhận tensor đầu vào có kích thước `(batch_size, 1, 5000)`.
  - Luồng xử lý đặc trưng tuần tự:
    $$\\mathbf{X} \\in \\mathbb{R}^{B \\times 1 \\times 5000} \\xrightarrow{\\text{Conv1d}} \\mathbb{R}^{B \\times 64 \\times 5000} \\xrightarrow{\\text{BatchNorm1d}} \\xrightarrow{\\text{ReLU}} \\xrightarrow{\\text{AdaptiveMaxPool1d}(1)} \\mathbb{R}^{B \\times 64 \\times 1} \\xrightarrow{\\text{Flatten}} \\mathbb{R}^{B \\times 64} \\xrightarrow{\\text{Linear}} \\mathbb{R}^{B \\times 3}$$
  - Chuyển đổi ma trận thưa TF-IDF sang dense PyTorch tensor dạng float32 và đóng gói thành `DataLoader` với `batch_size=64`.

- **Ý nghĩa & Lý do lựa chọn (Why it matters)**:
  - `TFIDF_CNN_Model` đóng vai trò kiến trúc chuyển tiếp đặc biệt giữa phương pháp trích xuất đặc trưng truyền thống và học sâu: thay vì chiếu từ vựng qua Word2Vec hay Transformer, mô hình dùng bộ lọc tích chập quét qua dải tần số đặc trưng n-gram để phát hiện các tổ hợp mẫu tần suất cục bộ mang tính phân loại.
  - Lớp `BatchNorm1d` ổn định phân phối trung gian, tăng tốc độ hội tụ và giảm độ nhạy với việc khởi tạo trọng số.
  - `AdaptiveMaxPool1d(1)` thực hiện nén cực đại toàn cục (global max pooling), trích xuất tín hiệu kích hoạt mạnh nhất dọc theo toàn bộ 5,000 đặc trưng bất kể vị trí.

- **Câu hỏi nghiên cứu được giải quyết (Questions it answers)**:
  - Kiến trúc nơ-ron tích chập 1 chiều hoạt động thế nào trên dữ liệu TF-IDF đầu vào dạng `(batch_size, 1, 5000)`?
  - Chi phí bộ nhớ RAM và GPU khi chuyển đổi ma trận thưa sang dense tensor có nằm trong ngưỡng an toàn không?""")

# ==============================================================================
# Cell 7: 1D-CNN Model Architecture & DataLoader Code
# ==============================================================================
cnn_arch_code = '''# ==============================================================================
# ⚙️ Architecture: Định nghĩa Mô hình TFIDF_CNN_Model (PyTorch)
# ==============================================================================
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# 1. Định nghĩa Module PyTorch TFIDF_CNN_Model
class TFIDF_CNN_Model(nn.Module):
    """
    Kiến trúc mạng 1D-CNN trích xuất đặc trưng trên vector TF-IDF:
    - Input Shape : (batch_size, 1, 5000)
    - Conv1d      : in_channels=1, out_channels=64, kernel_size=5, padding=2
    - BatchNorm1d : 64 features
    - ReLU        : Kích hoạt phi tuyến tính
    - MaxPool     : AdaptiveMaxPool1d(1) -> Global Max Pooling
    - Flatten     : Nén về (batch_size, 64)
    - Linear      : Lớp tuyến tính ánh xạ ra 3 lớp cảm xúc
    """
    def __init__(self, input_dim=5000, num_classes=3, num_filters=64, kernel_size=5):
        super(TFIDF_CNN_Model, self).__init__()
        self.conv1d = nn.Conv1d(
            in_channels=1,
            out_channels=num_filters,
            kernel_size=kernel_size,
            padding=kernel_size // 2
        )
        self.bn1d = nn.BatchNorm1d(num_filters)
        self.relu = nn.ReLU()
        self.maxpool = nn.AdaptiveMaxPool1d(output_size=1)
        self.fc = nn.Linear(num_filters, num_classes)

    def forward(self, x):
        # Đảm bảo tensor có số chiều (batch_size, 1, 5000)
        if x.dim() == 2:
            x = x.unsqueeze(1)
        
        # Conv1d -> BatchNorm1d -> ReLU -> MaxPool -> Linear
        out = self.conv1d(x)
        out = self.bn1d(out)
        out = self.relu(out)
        out = self.maxpool(out)
        out = torch.flatten(out, start_dim=1)
        out = self.fc(out)
        return out

# 2. Xác định thiết bị tính toán (CUDA GPU / CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"⚙️ Thiết bị thực thi: {device}")

# 3. Chuyển đổi dữ liệu TF-IDF sang PyTorch Float Tensor kích thước (N, 1, 5000)
X_train_dense = torch.tensor(X_train_tfidf.toarray(), dtype=torch.float32).unsqueeze(1)
y_train_tensor = torch.tensor(y_train_tfidf, dtype=torch.long)

X_test_dense = torch.tensor(X_test_tfidf.toarray(), dtype=torch.float32).unsqueeze(1)
y_test_tensor = torch.tensor(y_test_tfidf, dtype=torch.long)

# 4. Đóng gói vào PyTorch TensorDataset & DataLoader
batch_size_cnn = 64
train_tfidf_dataset = TensorDataset(X_train_dense, y_train_tensor)
test_tfidf_dataset = TensorDataset(X_test_dense, y_test_tensor)

train_tfidf_loader = DataLoader(train_tfidf_dataset, batch_size=batch_size_cnn, shuffle=True)
test_tfidf_loader = DataLoader(test_tfidf_dataset, batch_size=batch_size_cnn, shuffle=False)

print("=" * 65)
print(f"Tensor X_train_dense Shape : {tuple(X_train_dense.shape)} (batch_size, channels, length)")
print(f"Tensor X_test_dense Shape  : {tuple(X_test_dense.shape)}")
print(f"Số lượng batches Train     : {len(train_tfidf_loader)} (batch_size={batch_size_cnn})")
print(f"Số lượng batches Test      : {len(test_tfidf_loader)}")
print("=" * 65)
'''
add_code(cnn_arch_code)

# ==============================================================================
# Cell 8: 1D-CNN Training & Evaluation Markdown Explanation
# ==============================================================================
add_md("""### 🧪 Experiments: Huấn luyện và Đánh giá TF-IDF + 1D-CNN (15 Epochs)

- **Nội dung thực hiện (What this step does)**:
  - Khởi tạo `TFIDF_CNN_Model`, hàm mất mát `nn.CrossEntropyLoss()` và thuật toán tối ưu `optim.Adam(..., lr=0.001, weight_decay=1e-5)`.
  - Tiến hành huấn luyện lặp qua đúng **15 epochs** trên tập huấn luyện, theo dõi hàm mất mát trung bình và độ chính xác huấn luyện theo từng epoch.
  - Chuyển mô hình sang chế độ đánh giá (`model.eval()`), dự đoán toàn bộ tập kiểm thử `test_tfidf_loader` với `torch.no_grad()`.
  - Thu thập đầy đủ các chỉ số hiệu năng (Accuracy, Macro/Weighted Precision, Recall, F1) và lưu vào `results["TF-IDF + 1D-CNN"]` cùng `all_predictions["TF-IDF + 1D-CNN"]`.

- **Ý nghĩa & Lý do lựa chọn (Why it matters)**:
  - 15 epochs là thời lượng huấn luyện chuẩn xác, vừa đủ để mạng 1D-CNN hội tụ tối ưu trên không gian 5,000 đặc trưng mà không rơi vào tình trạng quá khớp (overfitting) nhờ có L2 Regularization (`weight_decay=1e-5`) và Batch Normalization.
  - Việc đánh giá toàn diện theo cùng một thang đo với LinearSVC và các mô hình tiếp theo đảm bảo tính khách quan và nhất quán trong phân tích thực nghiệm so sánh.

- **Câu hỏi nghiên cứu được giải quyết (Questions it answers)**:
  - TF-IDF + 1D-CNN có vượt qua được đường cơ sở LinearSVC về Macro F1 không?
  - Tốc độ hội tụ của mô hình trong 15 epochs diễn ra như thế nào qua từng chu kỳ huấn luyện?
  - Khả năng phân loại của mô hình trên lớp Neutral và các lớp phân cực đạt kết quả ra sao?""")

# ==============================================================================
# Cell 9: 1D-CNN Training & Evaluation Code
# ==============================================================================
cnn_train_code = '''# ==============================================================================
# 🧪 Experiments: Huấn luyện và Đánh giá TFIDF_CNN_Model (15 Epochs)
# ==============================================================================
# 1. Khởi tạo mô hình, đưa lên thiết bị tính toán
tfidf_cnn_model = TFIDF_CNN_Model(input_dim=5000, num_classes=3, num_filters=64, kernel_size=5)
tfidf_cnn_model = tfidf_cnn_model.to(device)

# 2. Cấu hình Loss Function và Adam Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(tfidf_cnn_model.parameters(), lr=0.001, weight_decay=1e-5)

# 3. Vòng lặp huấn luyện trong 15 epochs
epochs = 15
print("=" * 65)
print(f"🧪 BẮT ĐẦU HUẤN LUYỆN TFIDF_CNN_Model TRONG {epochs} EPOCHS TRÊN {device}")
print("=" * 65)

for epoch in range(epochs):
    tfidf_cnn_model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_x, batch_y in train_tfidf_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad()
        outputs = tfidf_cnn_model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * batch_x.size(0)
        _, preds = torch.max(outputs, 1)
        total += batch_y.size(0)
        correct += (preds == batch_y).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    print(f"Epoch [{epoch + 1:02d}/{epochs:02d}] - Train Loss: {epoch_loss:.4f} - Train Accuracy: {epoch_acc * 100:.2f}%")

# 4. Đánh giá trên tập kiểm thử (Test Set)
tfidf_cnn_model.eval()
all_preds_cnn = []
all_trues_cnn = []

with torch.no_grad():
    for batch_x, batch_y in test_tfidf_loader:
        batch_x = batch_x.to(device)
        outputs = tfidf_cnn_model(batch_x)
        preds = torch.argmax(outputs, dim=1).cpu().numpy()
        
        all_preds_cnn.extend(preds.tolist())
        all_trues_cnn.extend(batch_y.numpy().tolist())

all_preds_cnn = np.array(all_preds_cnn)
all_trues_cnn = np.array(all_trues_cnn)

# 5. Tính toán các chỉ số đánh giá toàn diện
tfidf_cnn_metrics = {
    "accuracy": accuracy_score(all_trues_cnn, all_preds_cnn),
    "precision_macro": precision_score(all_trues_cnn, all_preds_cnn, average="macro", zero_division=0),
    "recall_macro": recall_score(all_trues_cnn, all_preds_cnn, average="macro", zero_division=0),
    "f1_macro": f1_score(all_trues_cnn, all_preds_cnn, average="macro", zero_division=0),
    "precision_weighted": precision_score(all_trues_cnn, all_preds_cnn, average="weighted", zero_division=0),
    "recall_weighted": recall_score(all_trues_cnn, all_preds_cnn, average="weighted", zero_division=0),
    "f1_weighted": f1_score(all_trues_cnn, all_preds_cnn, average="weighted", zero_division=0),
}

# 6. Đăng ký kết quả vào dictionary chung
if "results" not in globals():
    results = {}
results["TF-IDF + 1D-CNN"] = tfidf_cnn_metrics

if "all_predictions" not in globals():
    all_predictions = {}
all_predictions["TF-IDF + 1D-CNN"] = (all_trues_cnn, all_preds_cnn)

# 7. Hiển thị báo cáo kết quả
print("\\n" + "=" * 65)
print("🧪 KẾT QUẢ ĐÁNH GIÁ BASELINE 2: TF-IDF + 1D-CNN")
print("=" * 65)
for metric_name, val in tfidf_cnn_metrics.items():
    print(f"  {metric_name:<22}: {val * 100:.2f}%")
print("-" * 65)
print("\\nBáo cáo phân loại chi tiết (Classification Report):")
print(classification_report(
    all_trues_cnn,
    all_preds_cnn,
    target_names=['Negative (-1)', 'Neutral (0)', 'Positive (1)'],
    digits=4
))
print("=" * 65)
'''
add_code(cnn_train_code)

# ==============================================================================
# Save to scratch/tfidf_cells.json
# ==============================================================================
out_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/scratch/tfidf_cells.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cells, f, ensure_ascii=False, indent=2)

print(f"Successfully created {len(cells)} cells in {out_path}")
