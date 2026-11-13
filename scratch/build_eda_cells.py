import json
import ast
from pathlib import Path

# Load original notebook to get exact base metadata
nb_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/ipynb/text/sentimentanalysis.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    orig_nb = json.load(f)

def to_source_lines(text):
    lines = text.strip("\n").split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]] if lines else []

def make_md_cell(content):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": to_source_lines(content)
    }

def make_code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": to_source_lines(code)
    }

# Cell 0: Title and Academic metadata
cell_0 = orig_nb["cells"][0]

# Cell 1: Imports markdown
cell_1 = orig_nb["cells"][1]

# Cell 2: Colab package install
cell_2 = orig_nb["cells"][2]

# Cell 3: Data Engine resolver (replace ✅, ⏳, 📁 with [📦 Data Engine])
cell_3_code = '''import os
import sys
from pathlib import Path

def resolve_dataset_dir():
    """
    Tự động phát hiện môi trường thực thi và đường dẫn dữ liệu:
    1. Kiểm tra môi trường Kaggle (/kaggle/input/...)
    2. Kiểm tra thư mục cục bộ (./data, .)
    3. Tải tự động qua kagglehub nếu chạy trên Google Colab hoặc máy mới
    """
    # 1. Kaggle paths
    kaggle_paths = [
        Path('/kaggle/input/datasets/anhphmduy/vlsp-sentiment-dataset'),
        Path('/kaggle/input/vlsp-sentiment-dataset'),
    ]
    for p in kaggle_paths:
        if p.exists() and (p / 'vlsp_sentiment_train.csv').exists():
            print(f"[📦 Data Engine] Phát hiện dữ liệu tại đường dẫn Kaggle: {p}")
            return p

    # 2. Local relative paths
    local_paths = [
        Path('./data'),
        Path('.'),
        Path('../data'),
    ]
    for p in local_paths:
        if p.exists() and (p / 'vlsp_sentiment_train.csv').exists():
            print(f"[📦 Data Engine] Phát hiện dữ liệu tại đường dẫn cục bộ: {p.resolve()}")
            return p.resolve()

    # 3. Google Colab / Remote download via kagglehub
    print("[📦 Data Engine] Đang tải bộ dữ liệu 'anhphmduy/vlsp-sentiment-dataset' từ Kaggle Hub...")
    try:
        import kagglehub
        path = kagglehub.dataset_download("anhphmduy/vlsp-sentiment-dataset")
        print(f"[📦 Data Engine] Đã tải dữ liệu thành công về: {path}")
        return Path(path)
    except Exception as e:
        raise RuntimeError(
            f"[📦 Data Engine] Không thể tải tự động bộ dữ liệu: {e}. "
            "Vui lòng tải thủ công từ https://www.kaggle.com/datasets/anhphmduy/vlsp-sentiment-dataset "
            "và đặt vào thư mục './data'."
        )

DATA_DIR = resolve_dataset_dir()
print(f"[📦 Data Engine] Thư mục dữ liệu: {DATA_DIR}")'''
cell_3 = make_code_cell(cell_3_code)

# Cell 4: Imports & Reproducibility seeds
cell_4 = orig_nb["cells"][4]

# Cell 5: EDA Section header
cell_5_content = """## EDA — Khám phá và Phân tích Dữ liệu (Exploratory Data Analysis)"""
cell_5 = make_md_cell(cell_5_content)

# EDA Step 1: 📦 Data Engine Markdown
cell_6_content = """### 📦 Data Engine: Truy xuất và Tải Dữ liệu (Data Loading & Path Resolving)

- **What this step does:** Nạp các tập dữ liệu huấn luyện (`vlsp_sentiment_train.csv`) và kiểm thử (`vlsp_sentiment_test.csv`) thông qua đối tượng đường dẫn an toàn `DATA_DIR`, hiển thị kích thước ma trận (`shape`) và 5 bản ghi mẫu đầu tiên của từng phân vùng dữ liệu.
- **Why it matters:** Đảm bảo luồng đọc dữ liệu định dạng phân cách bằng tab (`\\t`) và bảng mã ký tự tiếng Việt (UTF-8) hoạt động ổn định và nhất quán trên đa môi trường (Kaggle, Colab, Local); xác nhận tính toàn vẹn của tệp dữ liệu thô trước khi thực hiện các phân tích sâu hơn.
- **Questions it answers:**
  - Dữ liệu thô có được tải thành công từ đúng phân vùng lưu trữ vào DataFrame hay không?
  - Kích thước tập Train và tập Test là bao nhiêu (số dòng, số cột)?
  - Cấu trúc mẫu ban đầu của các cột `Class` (nhãn) và `Data` (văn bản) trông như thế nào?

> *Ghi chú:* Tệp `vlsp_sentiment_train_augmented.csv` (dữ liệu tăng cường) được cung cấp sẵn trong kho dữ liệu sẽ không sử dụng ở giai đoạn này mà được bảo lưu dành riêng cho phần thực nghiệm nâng cao với PhoBERT-large."""
cell_6 = make_md_cell(cell_6_content)

# EDA Step 1 Code: 📦 Data Engine loading
cell_7_code = """train_df = pd.read_csv(DATA_DIR / 'vlsp_sentiment_train.csv', sep='\\t')
test_df = pd.read_csv(DATA_DIR / 'vlsp_sentiment_test.csv', sep='\\t')

# Xem kích thước và 5 dòng đầu tiên của dữ liệu
print(f"[📦 Data Engine] Kích thước tập Train: {train_df.shape}")
print(f"[📦 Data Engine] Kích thước tập Test : {test_df.shape}")
print("\\n[📦 Data Engine] 5 dòng đầu tập Train:")
display(train_df.head())
print("\\n[📦 Data Engine] 5 dòng đầu tập Test:")
display(test_df.head())"""
cell_7 = make_code_cell(cell_7_code)

# EDA Step 2: 🔍 Integrity Markdown
cell_8_content = """### 🔍 Integrity: Kiểm tra Tính Toàn vẹn và Giá trị Thiếu (Missing Values & Dtypes)

- **What this step does:** Kiểm tra cấu trúc kiểu dữ liệu (`dtypes`) của từng trường thông tin, kiểm tra tính đầy đủ và phát hiện các giá trị khuyết thiếu (`null` / `NaN`) trên cả tập huấn luyện và kiểm thử.
- **Why it matters:** Đảm bảo dữ liệu đầu vào sạch về mặt cấu trúc (structural integrity). Dữ liệu văn bản chứa `NaN` hoặc sai lệch kiểu dữ liệu sẽ gây lỗi runtime nghiêm trọng trong pipeline chuẩn hóa xâu ký tự và vector hóa; kiểm tra sớm giúp xác định xem có cần áp dụng thao tác loại bỏ (`dropna`) hay không.
- **Questions it answers:**
  - Tập dữ liệu có chứa bản ghi nào bị rỗng hoặc mất mát thông tin (`NaN`) không?
  - Kiểu dữ liệu của các cột đã đúng chuẩn mong đợi (`int64` cho nhãn `Class`, `object`/chuỗi cho văn bản `Data`) chưa?
  - Bộ dữ liệu có sẵn sàng cho phân tích sâu mà không cần can thiệp xử lý giá trị rỗng không?"""
cell_8 = make_md_cell(cell_8_content)

# EDA Step 2 Code: 🔍 Integrity checks
cell_9_code = """print("[🔍 Integrity] === TRAIN SET SCHEMA ===")
print(f"Shape: {train_df.shape}")
print("Data types:\\n", train_df.dtypes)
print("\\n[🔍 Integrity] === TEST SET SCHEMA ===")
print(f"Shape: {test_df.shape}")
print("Data types:\\n", test_df.dtypes)

# Kiểm tra missing values
print("\\n[🔍 Integrity] Missing values (Train):")
print(train_df.isnull().sum())

print("\\n[🔍 Integrity] Missing values (Test):")
print(test_df.isnull().sum())"""
cell_9 = make_code_cell(cell_9_code)

# EDA Step 3: 🏷️ Labels Markdown
cell_10_content = """### 🏷️ Labels: Phân tích Phân phối và Cân bằng Lớp (Class Distribution)

- **What this step does:** Thống kê số lượng quan sát tuyệt đối và tỷ lệ phần trăm phân bố của từng lớp nhãn cảm xúc (-1: Tiêu cực, 0: Trung lập, 1: Tích cực) trên cả tập Train và Test; trực quan hóa so sánh bằng biểu đồ cột (bar plot).
- **Why it matters:** Đánh giá mức độ cân bằng lớp (class balance) là yếu tố quyết định chiến lược xây dựng mô hình: xác định có cần kỹ thuật bù mẫu (oversampling/SMOTE), điều chỉnh trọng số hàm mất mát (class-weighted cross entropy), cũng như khẳng định tính phù hợp của độ đo Macro F1 và Accuracy.
- **Questions it answers:**
  - Tỷ lệ phân bố giữa ba lớp nhãn (-1, 0, 1) trong tập huấn luyện có cân bằng không?
  - Phân phối nhãn ở tập kiểm thử (Test) có đồng nhất với tập huấn luyện (Train) không?
  - Kết luận về sự cân bằng dữ liệu: Có cần can thiệp xử lý mất cân bằng lớp ở giai đoạn tiền xử lý không?"""
cell_10 = make_md_cell(cell_10_content)

# EDA Step 3 Code: 🏷️ Labels
cell_11_code = """# Đếm số lượng từng class
print("[🏷️ Labels] Class distribution (Train):")
print(train_df['Class'].value_counts())
print("\\n[🏷️ Labels] Tỷ lệ phần trăm (Train):")
print(train_df['Class'].value_counts(normalize=True))

# Trực quan hóa đối sánh Train vs Test
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

train_df['Class'].value_counts().sort_index().plot(
    kind='bar', ax=axes[0], color=['#e74c3c', '#95a5a6', '#2ecc71']
)
axes[0].set_title('Train - Class Distribution')
axes[0].set_xlabel('Class (-1: Negative, 0: Neutral, 1: Positive)')
axes[0].set_ylabel('Count')

test_df['Class'].value_counts().sort_index().plot(
    kind='bar', ax=axes[1], color=['#e74c3c', '#95a5a6', '#2ecc71']
)
axes[1].set_title('Test - Class Distribution')
axes[1].set_xlabel('Class (-1: Negative, 0: Neutral, 1: Positive)')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.show()

# Thống kê định lượng tỷ lệ mẫu
total_train = len(train_df)
print("[🏷️ Labels] Chi tiết phân bố tập Train:")
for cls, cnt in train_df['Class'].value_counts().sort_index().items():
    print(f"  Class {cls:2d}: {cnt:5d} mẫu ({cnt / total_train * 100:.2f}%)")

total_test = len(test_df)
print("\\n[🏷️ Labels] Chi tiết phân bố tập Test:")
for cls, cnt in test_df['Class'].value_counts().sort_index().items():
    print(f"  Class {cls:2d}: {cnt:5d} mẫu ({cnt / total_test * 100:.2f}%)")"""
cell_11 = make_code_cell(cell_11_code)

# EDA Step 4: 📐 Dimensions Markdown
cell_12_content = """### 📐 Dimensions: Khảo sát Phân phối Độ dài Văn bản (Text & Sequence Length)

- **What this step does:** Đo lường độ dài văn bản theo số lượng ký tự (`char_length`) và số lượng từ đơn (`word_count`) cho từng bản ghi; tính toán các chỉ số thống kê mô tả (mean, median, std, min, max, phân vị); trực quan hóa phân phối qua biểu đồ Histogram và Boxplot theo từng lớp; dò quét các mẫu ngoại lai (câu cực ngắn < 10 ký tự hoặc câu cực dài > 500 ký tự).
- **Why it matters:** Phân phối độ dài chuỗi cung cấp căn cứ định lượng then chốt để thiết lập siêu tham số cắt cụt chuỗi (`MAX_SEQUENCE_LENGTH` cho mô hình Word2Vec CBOW và `max_length` cho PhoBERT Tokenizer). Ngưỡng tối ưu phải vừa bao quát đại đa số ngữ cảnh (>99% câu) vừa tiết kiệm bộ nhớ tính toán GPU.
- **Questions it answers:**
  - Phân phối độ dài câu có dạng lệch phải (right-skewed) điển hình của ngôn ngữ tự nhiên không?
  - Độ dài câu trung bình, trung vị và khoảng tứ phân vị (IQR) là bao nhiêu?
  - Giữa các lớp cảm xúc (-1, 0, 1), độ dài văn bản có sự chênh lệch đáng kể nào không?
  - Có bao nhiêu quan sát ngoại lai (rất ngắn < 10 ký tự hoặc rất dài > 500 ký tự) và nên thiết lập ngưỡng cắt cụt (truncation) ở giá trị nào để bao phủ trên 95%-99% dữ liệu?"""
cell_12 = make_md_cell(cell_12_content)

# EDA Step 4 Code: 📐 Dimensions
cell_13_code = """# Tính độ dài theo ký tự và từ
train_df['char_length'] = train_df['Data'].str.len()
train_df['word_count']  = train_df['Data'].str.split().str.len()

test_df['char_length'] = test_df['Data'].str.len()
test_df['word_count']  = test_df['Data'].str.split().str.len()

# Thống kê mô tả
print("[📐 Dimensions] === Thống kê độ dài văn bản (Train Set) ===")
print(train_df[['char_length', 'word_count']].describe())

# Trực quan hóa phân phối độ dài theo class
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

for i, col in enumerate(['char_length', 'word_count']):
    # Histogram phân phối tổng
    train_df[col].hist(bins=50, ax=axes[0][i], color='steelblue', alpha=0.7, edgecolor='black')
    axes[0][i].set_title(f'Phân phối tổng thể {col}')
    axes[0][i].set_xlabel(col)
    axes[0][i].set_ylabel('Tần số')

    # Boxplot theo từng Class
    train_df.boxplot(column=col, by='Class', ax=axes[1][i])
    axes[1][i].set_title(f'{col} phân rã theo nhãn cảm xúc')
    axes[1][i].set_xlabel('Class')
    axes[1][i].set_ylabel(col)

plt.suptitle('')  # Xóa tiêu đề mặc định của boxplot
plt.tight_layout()
plt.show()

# Phát hiện các mẫu ngoại lai (outliers)
short_samples = train_df[train_df['char_length'] < 10]
long_samples = train_df[train_df['char_length'] > 500]
print(f"[📐 Dimensions] Số mẫu rất ngắn (< 10 ký tự): {len(short_samples)}")
if len(short_samples) > 0:
    print("  Ví dụ mẫu rất ngắn:", short_samples['Data'].values[:5])

print(f"\\n[📐 Dimensions] Số mẫu rất dài (> 500 ký tự): {len(long_samples)} ({len(long_samples)/len(train_df)*100:.2f}%)")
print(f"[📐 Dimensions] 99th percentile word count: {train_df['word_count'].quantile(0.99):.1f} từ")"""
cell_13 = make_code_cell(cell_13_code)

# EDA Step 5: 🔤 Lexicon Markdown
cell_14_content = """### 🔤 Lexicon: Phân tích Tần suất Từ vựng và Teencode (Vocabulary & Teencode Analysis)

- **What this step does:** Khảo sát quy mô tập từ vựng thô (tổng số lượng tokens và số lượng tokens phân biệt); trích xuất Top 20 từ có tần số xuất hiện cao nhất toàn tập dữ liệu và Top 15 từ đặc trưng cho từng lớp nhãn cảm xúc (-1, 0, 1).
- **Why it matters:** Dữ liệu đánh giá người dùng trên mạng xã hội chứa tỷ lệ rất cao teencode, tiếng lóng, từ viết tắt, ký tự kéo dài, emoticon, và stopwords. Phân tích từ vựng giúp định hình cấu trúc từ điển chuẩn hóa (dictionary mapping) và quy tắc làm sạch dữ liệu trong pipeline tiền xử lý (Preprocessing).
- **Questions it answers:**
  - Quy mô từ vựng thô là bao nhiêu tokens và mật độ từ hiếm (sparse vocabulary) như thế nào?
  - Những từ nào mang tính biểu cảm đặc thù cho từng lớp nhãn (ví dụ: *khen, thích, tốt* ở lớp Tích cực vs *lỗi, chán, tệ* ở lớp Tiêu cực)?
  - Những từ viết tắt, teencode phổ biến nào (như *ko, đc, sp, wa, mik*) xuất hiện với tần suất cao cần được chuẩn hóa trước khi vector hóa?"""
cell_14 = make_md_cell(cell_14_content)

# EDA Step 5 Code: 🔤 Lexicon
cell_15_code = """from collections import Counter
import re

# Tokenize cơ bản theo khoảng trắng để khảo sát từ vựng thô
all_words = ' '.join(train_df['Data']).lower().split()
word_freq = Counter(all_words)

print(f"[🔤 Lexicon] Tổng số tokens (Tokens count) : {len(all_words):,}")
print(f"[🔤 Lexicon] Số từ phân biệt (Unique tokens): {len(word_freq):,}")
print(f"\\n[🔤 Lexicon] Top 20 từ xuất hiện nhiều nhất:\\n{word_freq.most_common(20)}")

# Top từ phổ biến phân rã theo từng lớp cảm xúc
label_mapping = {-1: 'Tiêu cực (Negative)', 0: 'Trung lập (Neutral)', 1: 'Tích cực (Positive)'}
for cls in sorted(train_df['Class'].unique()):
    texts = ' '.join(train_df[train_df['Class'] == cls]['Data']).lower().split()
    freq  = Counter(texts)
    print(f"\\n[🔤 Lexicon] --- Class {cls} ({label_mapping.get(cls, cls)}) — Top 15 words ---")
    print(freq.most_common(15))"""
cell_15 = make_code_cell(cell_15_code)

# EDA to Preprocessing Decision Table Markdown: 🧹 Preprocessing
cell_16_content = """### 🧹 Preprocessing — Bảng Quyết định Tiền xử lý từ Kết quả Khám phá Dữ liệu (EDA)

Dựa trên các bằng chứng định lượng phát hiện được trong quá trình khám phá dữ liệu (EDA), nhóm thiết lập các quyết định kỹ thuật và nguyên lý thiết kế cho toàn bộ pipeline tiền xử lý và mô hình hóa tiếp theo:

| Hiện tượng phát hiện từ EDA | Bằng chứng định lượng | Quyết định tiền xử lý & Thiết kế mô hình |
|---|---|---|
| 🏷️ **Cân bằng lớp hoàn hảo** | Tập train: đúng 1.700 mẫu/lớp (-1, 0, 1); Test: đúng 350 mẫu/lớp | Không áp dụng kỹ thuật oversampling hay class-weighting ở pha nạp ban đầu. Sử dụng **Macro F1** song hành cùng **Accuracy** làm thước đo đánh giá chính. |
| 🔤 **Lượng lớn Teencode & Viết tắt** | Hàng loạt biến thể mạng xã hội: *ko, đc, sp, wa, thik, mik, bthg...* | Xây dựng từ điển quy chuẩn 30+ từ ghép/từ viết tắt về dạng chuẩn tiếng Việt trước khi tiến hành tách từ (word segmentation). |
| 🔤 **Ký tự cảm xúc (Emoticons)** | Tần suất xuất hiện cao: `:)`, `:((`, `:D`, `^^`, `t.t` | Ánh xạ emoticon thành từ biểu cảm tiếng Việt (`cười`, `buồn`, `khóc`, `vui`) trước khi lọc bỏ dấu câu đặc biệt. |
| 📐 **Phân phối độ dài lệch phải** | Đa số câu < 150 từ; 99% câu < 250 từ; chỉ một số ít ngoại lai > 300 từ | Thiết lập `MAX_SEQUENCE_LENGTH = 300` cho nhánh Word2Vec và `max_length = 256` cho nhánh PhoBERT (vừa bao phủ 99% ngữ cảnh vừa tối ưu hóa bộ nhớ GPU). |
| 🔤 **Từ vựng phân tán & từ hiếm** | Phân phối Zipf điển hình; nhiều từ sai chính tả hoặc xuất hiện 1 lần | Nhánh W2V: Giới hạn `MAX_VOCAB_SIZE = 10000`, khởi tạo vector OOV ngẫu nhiên theo phân phối chuẩn. Nhánh PhoBERT: Tận dụng Byte-Pair Encoding (BPE) 64K subwords để triệt tiêu bài toán OOV. |"""
cell_16 = make_md_cell(cell_16_content)

restructured_cells = [
    cell_0,
    cell_1,
    cell_2,
    cell_3,
    cell_4,
    cell_5,
    cell_6,
    cell_7,
    cell_8,
    cell_9,
    cell_10,
    cell_11,
    cell_12,
    cell_13,
    cell_14,
    cell_15,
    cell_16,
]

out_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/scratch/eda_cells.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(restructured_cells, f, ensure_ascii=False, indent=1)

print(f"SUCCESS: Wrote {len(restructured_cells)} restructured cells to {out_path}")
