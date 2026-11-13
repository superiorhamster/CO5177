import json
import ast
import shutil
from pathlib import Path

# Load original notebook
nb_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/ipynb/text/sentimentanalysis.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Original cell count: {len(nb['cells'])}")

# Helper to create markdown cell
def create_md_cell(content):
    lines = [l + "\n" for l in content.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    }

# Helper to create code cell
def create_code_cell(code):
    lines = [l + "\n" for l in code.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    }

# 1. Update Cell 0: Academic Title & Course Info
cell_0_content = """# Phân tích Cảm xúc Văn bản Tiếng Việt: Word2Vec và PhoBERT-large
**Môn học:** CO5177 — Nền tảng lập trình cho phân tích và trực quan dữ liệu  
**Học kỳ:** 261 | **Năm học:** 2026–2027  
**Giảng viên hướng dẫn:** TS. Lê Thành Sách  
**Nhóm sinh viên thực hiện:** SlightSeek  

---
*Notebook thực nghiệm so sánh các kiến trúc Deep Learning truyền thống (TextCNN, BiLSTM, CNN+BiLSTM kết hợp Word2Vec CBOW 400d) và mô hình ngôn ngữ ngữ cảnh hóa tiền huấn luyện (PhoBERT-large) trên bộ dữ liệu VLSP 2016.*"""

nb['cells'][0]['source'] = [l + "\n" for l in cell_0_content.split("\n")]
nb['cells'][0]['source'][-1] = nb['cells'][0]['source'][-1].rstrip("\n")

# 2. Update Cell 2 & 3: Environment setup and dependencies
# Cell 2: Colab package install
cell_2_code = """# Cài đặt các thư viện cần thiết khi chạy trên Google Colab / Kaggle
!pip install -q pyvi gensim datasets transformers accelerate kagglehub"""
nb['cells'][2]['source'] = [cell_2_code]

# Cell 3: Data directory resolver (supports Colab auto-download via kagglehub, Kaggle inputs, and local folder)
cell_3_code = """import os
import sys
from pathlib import Path

def resolve_dataset_dir():
    \"\"\"
    Tự động phát hiện môi trường thực thi và đường dẫn dữ liệu:
    1. Kiểm tra môi trường Kaggle (/kaggle/input/...)
    2. Kiểm tra thư mục cục bộ (./data, .)
    3. Tải tự động qua kagglehub nếu chạy trên Google Colab hoặc máy mới
    \"\"\"
    # 1. Kaggle paths
    kaggle_paths = [
        Path('/kaggle/input/datasets/anhphmduy/vlsp-sentiment-dataset'),
        Path('/kaggle/input/vlsp-sentiment-dataset'),
    ]
    for p in kaggle_paths:
        if p.exists() and (p / 'vlsp_sentiment_train.csv').exists():
            print(f"✅ Phát hiện dữ liệu tại đường dẫn Kaggle: {p}")
            return p

    # 2. Local relative paths
    local_paths = [
        Path('./data'),
        Path('.'),
        Path('../data'),
    ]
    for p in local_paths:
        if p.exists() and (p / 'vlsp_sentiment_train.csv').exists():
            print(f"✅ Phát hiện dữ liệu tại đường dẫn cục bộ: {p.resolve()}")
            return p.resolve()

    # 3. Google Colab / Remote download via kagglehub
    print("⏳ Đang tải bộ dữ liệu 'anhphmduy/vlsp-sentiment-dataset' từ Kaggle Hub...")
    try:
        import kagglehub
        path = kagglehub.dataset_download("anhphmduy/vlsp-sentiment-dataset")
        print(f"✅ Đã tải dữ liệu thành công về: {path}")
        return Path(path)
    except Exception as e:
        raise RuntimeError(
            f"Không thể tải tự động bộ dữ liệu: {e}. "
            "Vui lòng tải thủ công từ https://www.kaggle.com/datasets/anhphmduy/vlsp-sentiment-dataset "
            "và đặt vào thư mục './data'."
        )

DATA_DIR = resolve_dataset_dir()
print(f"📁 Thư mục dữ liệu: {DATA_DIR}")"""
nb['cells'][3]['source'] = [l + "\n" for l in cell_3_code.split("\n")]
nb['cells'][3]['source'][-1] = nb['cells'][3]['source'][-1].rstrip("\n")

# 3. Update Cell 4: Seed setup & Device initialization
cell_4_src = "".join(nb['cells'][4]['source'])
seed_code = """
# Thiết lập hạt giống ngẫu nhiên để đảm bảo tính tái lập (Reproducibility)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)
np.random.seed(42)
"""
if "manual_seed" not in cell_4_src:
    cell_4_src = cell_4_src.strip() + seed_code
    nb['cells'][4]['source'] = [l + "\n" for l in cell_4_src.split("\n")]
    nb['cells'][4]['source'][-1] = nb['cells'][4]['source'][-1].rstrip("\n")

# 4. Update Cell 7: Load CSVs via DATA_DIR
cell_7_code = """train_df = pd.read_csv(DATA_DIR / 'vlsp_sentiment_train.csv', sep='\\t')
test_df = pd.read_csv(DATA_DIR / 'vlsp_sentiment_test.csv', sep='\\t')
# Xem kích thước và 5 dòng đầu tiên của dữ liệu
print(f"Kích thước tập Train: {train_df.shape}")
print(f"Kích thước tập Test : {test_df.shape}")
print("\\n5 dòng đầu tập Train:")
display(train_df.head())
print("\\n5 dòng đầu tập Test:")
display(test_df.head())"""
nb['cells'][7]['source'] = [l + "\n" for l in cell_7_code.split("\n")]
nb['cells'][7]['source'][-1] = nb['cells'][7]['source'][-1].rstrip("\n")

# 5. Insert Decision Table between Cell 16 and Cell 17
decision_table_content = """### Bảng Quyết định Tiền xử lý từ Kết quả Khám phá Dữ liệu (EDA)

Dựa trên các đặc trưng và hiện tượng phát hiện được trong quá trình EDA, nhóm thiết lập các quyết định kỹ thuật tương ứng cho các giai đoạn tiền xử lý và xây dựng mô hình:

| Hiện tượng phát hiện từ EDA | Bằng chứng định lượng | Quyết định tiền xử lý & Thiết kế mô hình |
|---|---|---|
| **Cân bằng lớp hoàn hảo** | Tập train: đúng 1.700 mẫu/lớp (-1, 0, 1); Test: 350 mẫu/lớp | Không áp dụng kỹ thuật oversampling/class-weighting ở giai đoạn nạp ban đầu. Dùng Macro F1 làm thước đo đánh giá chính. |
| **Lượng lớn Teencode & Viết tắt** | Hàng loạt biến thể: *ko, đc, sp, wa, thik, mik, bthg...* | Xây dựng từ điển quy chuẩn 30+ từ ghép/từ viết tắt về dạng chuẩn tiếng Việt trước khi tách từ. |
| **Ký tự cảm xúc (Emoticons)** | Tần suất cao: `:)`, `:((`, `:D`, `^^`, `t.t` | Ánh xạ emoticon thành từ biểu cảm (`cười`, `buồn`, `khóc`, `vui`) trước khi lọc bỏ dấu câu đặc biệt. |
| **Phân phối độ dài lệch phải** | Đa số câu < 150 từ; 99% câu < 250 từ; cá biệt > 300 từ | Thiết lập `MAX_SEQUENCE_LENGTH = 300` cho nhánh Word2Vec và `max_length = 256` cho nhánh PhoBERT (vừa bao phủ 99% ngữ cảnh vừa tối ưu bộ nhớ GPU). |
| **Từ vựng phân tán & từ hiếm** | Phân phối Zipf điển hình; nhiều từ sai chính tả hoặc xuất hiện 1 lần | Nhánh W2V: Giới hạn `MAX_VOCAB_SIZE = 10000`, khởi tạo embedding out-of-vocab ngẫu nhiên theo phân phối chuẩn. Nhánh PhoBERT: Tận dụng Byte-Pair Encoding (BPE) 64K subwords. |
"""
table_cell = create_md_cell(decision_table_content)

# We will construct new cell list carefully
new_cells = []
for i, cell in enumerate(nb['cells']):
    new_cells.append(cell)
    if i == 16:
        new_cells.append(table_cell)

nb['cells'] = new_cells
print(f"Cell count after inserting decision table: {len(nb['cells'])}")

# Update indexes after insertion:
# Let's locate cells by their content rather than hardcoded indexes!
def find_cell_index_by_substring(cells, sub):
    for i, c in enumerate(cells):
        src = "".join(c.get('source', []))
        if sub in src:
            return i
    return -1

# 6. Update Cell 20 (cleaning): local file export
idx_clean = find_cell_index_by_substring(nb['cells'], "replace_dict = {")
print(f"Found cleaning code at cell {idx_clean}")
clean_src = "".join(nb['cells'][idx_clean]['source'])
clean_src = clean_src.replace("train_df.to_csv('vlsp_sentiment_train_cleaned.csv')", "train_df.to_csv('./vlsp_sentiment_train_cleaned.csv', index=False)")
clean_src = clean_src.replace("test_df.to_csv('vlsp_sentiment_test_cleaned.csv')", "test_df.to_csv('./vlsp_sentiment_test_cleaned.csv', index=False)")
nb['cells'][idx_clean]['source'] = [l + "\n" for l in clean_src.split("\n")]
nb['cells'][idx_clean]['source'][-1] = nb['cells'][idx_clean]['source'][-1].rstrip("\n")

# 7. Update Cell 24 (preprocessing & dataloader): add seed to random_split
idx_prep = find_cell_index_by_substring(nb['cells'], "torch.utils.data.random_split(train_dataset, [train_size, val_size])")
print(f"Found DataLoader random_split at cell {idx_prep}")
prep_src = "".join(nb['cells'][idx_prep]['source'])
old_split = "train_dataset, val_dataset = torch.utils.data.random_split(train_dataset, [train_size, val_size])"
new_split = "# Phân tách train/validation 80/20 với seed cố định để đảm bảo tính tái lập\ntrain_dataset, val_dataset = torch.utils.data.random_split(\n    train_dataset, [train_size, val_size],\n    generator=torch.Generator().manual_seed(42)\n)"
prep_src = prep_src.replace(old_split, new_split)
nb['cells'][idx_prep]['source'] = [l + "\n" for l in prep_src.split("\n")]
nb['cells'][idx_prep]['source'][-1] = nb['cells'][idx_prep]['source'][-1].rstrip("\n")

# 8. Update Cell 27 (Word2Vec loading): use DATA_DIR
idx_w2v = find_cell_index_by_substring(nb['cells'], "KeyedVectors.load_word2vec_format(")
print(f"Found W2V loading at cell {idx_w2v}")
w2v_src = "".join(nb['cells'][idx_w2v]['source'])
old_w2v_load = "KeyedVectors.load_word2vec_format('/kaggle/input/datasets/anhphmduy/vlsp-sentiment-dataset/vi-model-CBOW.bin', binary=True)"
new_w2v_load = "KeyedVectors.load_word2vec_format(str(DATA_DIR / 'vi-model-CBOW.bin'), binary=True)"
w2v_src = w2v_src.replace(old_w2v_load, new_w2v_load)
nb['cells'][idx_w2v]['source'] = [l + "\n" for l in w2v_src.split("\n")]
nb['cells'][idx_w2v]['source'][-1] = nb['cells'][idx_w2v]['source'][-1].rstrip("\n")

# 9. Update Cell 40 (PhoBERT dataset loading): use DATA_DIR
idx_bert_df = find_cell_index_by_substring(nb['cells'], "bert_train_df = pd.read_csv('/kaggle/input/")
print(f"Found PhoBERT dataset loading at cell {idx_bert_df}")
bert_df_code = """# Nạp dữ liệu huấn luyện tăng cường (Augmented v2) và dữ liệu kiểm thử
bert_train_df = pd.read_csv(DATA_DIR / 'vlsp_sentiment_train_augmented_v2.csv', sep='\\t')
# Kiểm tra file test cleaned từ thư mục hiện tại hoặc DATA_DIR
test_cleaned_path = Path('./vlsp_sentiment_test_cleaned.csv')
if not test_cleaned_path.exists():
    test_cleaned_path = DATA_DIR / 'vlsp_sentiment_test_cleaned.csv'

bert_test_df = pd.read_csv(test_cleaned_path)
bert_test_df = bert_test_df[['Class', 'Data']]

print("=== TRAIN SET (Augmented v2) ===")
print(f"Shape: {bert_train_df.shape}")
display(bert_train_df.head())

print("\\n=== TEST SET ===")
print(f"Shape: {bert_test_df.shape}")
display(bert_test_df.head())"""
nb['cells'][idx_bert_df]['source'] = [l + "\n" for l in bert_df_code.split("\n")]
nb['cells'][idx_bert_df]['source'][-1] = nb['cells'][idx_bert_df]['source'][-1].rstrip("\n")

# 10. Update Cell 41 (PhoBERT download): local directory ./phobert-large-local
idx_bert_dl = find_cell_index_by_substring(nb['cells'], "local_dir=\"/kaggle/working/phobert-large-local\"")
print(f"Found PhoBERT download at cell {idx_bert_dl}")
bert_dl_src = "".join(nb['cells'][idx_bert_dl]['source'])
bert_dl_src = bert_dl_src.replace('local_dir="/kaggle/working/phobert-large-local"', 'local_dir="./phobert-large-local"')
nb['cells'][idx_bert_dl]['source'] = [l + "\n" for l in bert_dl_src.split("\n")]
nb['cells'][idx_bert_dl]['source'][-1] = nb['cells'][idx_bert_dl]['source'][-1].rstrip("\n")

# 11. Update Cell 43 (PhoBERT model loading): from ./phobert-large-local
idx_bert_load = find_cell_index_by_substring(nb['cells'], "\"/kaggle/working/phobert-large-local\"")
print(f"Found PhoBERT model loading at cell {idx_bert_load}")
bert_load_src = "".join(nb['cells'][idx_bert_load]['source'])
bert_load_src = bert_load_src.replace('"/kaggle/working/phobert-large-local"', '"./phobert-large-local"')
nb['cells'][idx_bert_load]['source'] = [l + "\n" for l in bert_load_src.split("\n")]
nb['cells'][idx_bert_load]['source'][-1] = nb['cells'][idx_bert_load]['source'][-1].rstrip("\n")

# 12. Add Confusion Matrix, Error Analysis, and Section 4 at the end
cm_md_content = """## Trực quan hóa Ma trận Nhầm lẫn (Confusion Matrix)

Nhằm so sánh toàn diện khả năng nhận diện trên từng lớp cảm xúc riêng biệt (`Negative: -1`, `Neutral: 0`, `Positive: 1`), ma trận nhầm lẫn của cả 4 mô hình được tổng hợp dưới dạng lưới heatmap trực quan."""

cm_code_content = """# Trực quan hóa Confusion Matrix cho cả 4 mô hình
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(14, 11))
model_keys = ["TextCNN", "BiLSTM", "CNN+BiLSTM", "PhoBERT-large"]
class_names = ['Negative (-1)', 'Neutral (0)', 'Positive (1)']

all_predictions = {}

# 1. Thu thập dự đoán từ các mô hình PyTorch W2V nếu có trong session
torch_model_pairs = [("TextCNN", 'cnn_model'), ("BiLSTM", 'lstm_model'), ("CNN+BiLSTM", 'cnn_lstm_model')]
for name, var_name in torch_model_pairs:
    if var_name in globals():
        mod = globals()[var_name]
        mod.eval()
        preds, trues = [], []
        with torch.no_grad():
            for x, y in test_loader:
                x = x.to(device)
                out = mod(x)
                preds.extend(torch.argmax(out, dim=1).cpu().numpy())
                trues.extend(y.numpy())
        all_predictions[name] = (trues, preds)

# 2. Thu thập dự đoán từ PhoBERT Trainer
if 'trainer' in globals() and 'tokenized_test' in globals():
    hf_preds = trainer.predict(tokenized_test)
    all_predictions["PhoBERT-large"] = (hf_preds.label_ids, np.argmax(hf_preds.predictions, axis=-1))

# 3. Vẽ biểu đồ nhiệt Confusion Matrix
for idx, name in enumerate(model_keys):
    ax = axes[idx // 2, idx % 2]
    if name in all_predictions:
        y_true, y_pred = all_predictions[name]
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                    xticklabels=class_names, yticklabels=class_names, ax=ax)
    else:
        ax.text(0.5, 0.5, f"Chạy 'Run All' để hiển thị\\nConfusion Matrix ({name})",
                ha='center', va='center', fontsize=12, color='gray')
    ax.set_title(f"Confusion Matrix: {name}", fontsize=13, fontweight='bold')
    ax.set_xlabel("Nhãn dự đoán (Predicted)")
    ax.set_ylabel("Nhãn thực tế (True)")

plt.suptitle("So sánh Ma trận Nhầm lẫn trên Tập Kiểm thử VLSP 2016", fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()"""

err_md_content = """## Phân tích Lỗi Định tính (Error Analysis)

Để hiểu rõ tại sao lớp **Trung lập (Neutral)** luôn đạt F1-score thấp nhất trên tất cả các mô hình, ta trích xuất và phân tích định tính các mẫu thực tế mà PhoBERT-large dự đoán sai."""

err_code_content = """# Phân tích lỗi định tính: Các trường hợp PhoBERT dự đoán sai
label_names_display = {0: 'Negative (-1)', 1: 'Neutral (0)', 2: 'Positive (1)'}

if "PhoBERT-large" in all_predictions:
    y_true_phobert, y_pred_phobert = all_predictions["PhoBERT-large"]
    error_indices = [i for i, (t, p) in enumerate(zip(y_true_phobert, y_pred_phobert)) if t != p]
    print(f"Tổng số mẫu dự đoán sai trên Test Set ({len(y_true_phobert)} mẫu): {len(error_indices)} mẫu "
          f"(Tỉ lệ lỗi: {len(error_indices)/len(y_true_phobert)*100:.2f}%)\\n")

    test_raw_df = pd.read_csv(DATA_DIR / 'vlsp_sentiment_test.csv', sep='\\t')
    error_records = []
    for idx in error_indices:
        error_records.append({
            'Index': idx,
            'Original_Text': test_raw_df.iloc[idx]['Data'],
            'True_Class': label_names_display[y_true_phobert[idx]],
            'Predicted_Class': label_names_display[y_pred_phobert[idx]],
        })

    error_df = pd.DataFrame(error_records)
    print("=== 6 VÍ DỤ ĐIỂN HÌNH VỀ DỰ ĐOÁN SAI CỦA PHOBERT (ĐẶC BIỆT LỚP NEUTRAL) ===")
    for i, row in error_df.head(6).iterrows():
        print(f"\\n[Mẫu #{row['Index']}]")
        print(f"  Văn bản gốc   : \\\"{row['Original_Text']}\\\"")
        print(f"  Nhãn thực tế  : {row['True_Class']}")
        print(f"  Nhãn dự đoán  : {row['Predicted_Class']}")
else:
    print("Chạy 'Run All' để hiển thị danh sách các mẫu dự đoán sai của mô hình.")"""

sec4_content = """## 4. Tổng kết và Mở rộng

### 4.1. Nhận xét và Kết luận Thực nghiệm
1. **Sức mạnh vượt trội của Pre-trained Language Model**: PhoBERT-large đạt **Accuracy 70.86%** và **Macro F1 70.82%**, vượt trội rõ rệt (+5.43% Accuracy, +5.57% Macro F1) so với mô hình Word2Vec tốt nhất (TextCNN: 65.43% Accuracy, 65.25% Macro F1). Kết quả này khẳng định ưu thế của cơ chế Self-Attention đa tầng trong việc nắm bắt sắc thái từ vựng theo ngữ cảnh so với static embedding (Word2Vec CBOW).
2. **So sánh các kiến trúc mạng nơ-ron truyền thống**:
   - **TextCNN** đạt hiệu quả cao nhất trong nhóm W2V nhờ các bộ lọc n-gram (filter sizes 3, 4, 5) bắt trúng các cụm từ thể hiện thái độ ngắn ("rất thích", "không hài lòng", "tạm được").
   - **BiLSTM** và **CNN+BiLSTM** có độ phức tạp tham số cao hơn nhưng không cải thiện được kết quả trên tập kiểm thử (đạt lần lượt 62.48% và 63.81% Macro F1), cho thấy dấu hiệu overfitting trên tập train kích thước khiêm tốn (5.100 mẫu).
3. **Thách thức cốt lõi ở lớp Trung lập (Neutral)**: Cả 4 mô hình đều đạt điểm F1 thấp nhất ở lớp Trung lập (~63.2% ở PhoBERT và ~57.1% ở TextCNN). Nguyên nhân chủ yếu xuất phát từ:
   - Các câu chứa cả khen lẫn chê ("máy dùng mượt nhưng pin hơi yếu").
   - Các câu trần thuật thuần túy về thông số kĩ thuật hoặc hỏi đáp thiếu từ ngữ biểu cảm rõ ràng.

### 4.2. Hạn chế và Đánh giá Rủi ro (Limitations & Leakage Analysis)
1. **Ranh giới tập từ vựng Word2Vec**: Toàn bộ 5.100 mẫu tập train ban đầu được dùng để xây dựng bảng từ vựng (vocabulary) trước khi phân tách 20% validation. Dù toàn bộ 5.100 mẫu này là dev set hợp lệ (không chứa tập test), đây vẫn là một rò rỉ nhẹ về thông tin tần suất từ ngữ giữa train và val.
2. **Dữ liệu tăng cường (Data Augmentation) chưa chia nhóm theo nguồn**: Tập tăng cường `augmented_v2` gồm 10.200 mẫu sinh từ bản dịch vòng và biến thể. Khi phân tách ngẫu nhiên train/validation, một số câu phái sinh có thể nằm ở tập huấn luyện trong khi câu gốc nằm ở tập kiểm định.
3. **Cắt cụt độ dài văn bản**: Giới hạn độ dài 256 subwords (PhoBERT) và 300 words (W2V) đã loại bỏ phần đuôi của một số ít đánh giá rất dài (> 350 từ), có thể làm mất đi các kết luận cảm xúc ở cuối bài đánh giá.

### 4.3. Hướng Mở rộng Tiếp theo (Future Work)
1. **Kiểm chứng K-Fold Cross Validation**: Phân tách dữ liệu theo `GroupKFold` (nhóm theo mã câu gốc) để triệt tiêu hoàn toàn rủi ro rò rỉ dữ liệu tăng cường giữa các fold.
2. **Thử nghiệm các kiến trúc Transformer Tiếng Việt mới**: So sánh chi phí tính toán và hiệu năng giữa PhoBERT-base, ViDeBERTa, và mô hình sinh (LLM prompting/LoRA) trên bài toán phân loại cảm xúc 3 lớp.
3. **Phân tích cảm xúc theo khía cạnh (Aspect-Based Sentiment Analysis - ABSA)**: Mở rộng bài toán từ phân loại toàn câu sang bóc tách cảm xúc cụ thể cho từng khía cạnh (chất lượng sản phẩm, giá cả, dịch vụ vận chuyển, thái độ phục vụ)."""

nb['cells'].append(create_md_cell(cm_md_content))
nb['cells'].append(create_code_cell(cm_code_content))
nb['cells'].append(create_md_cell(err_md_content))
nb['cells'].append(create_code_cell(err_code_content))
nb['cells'].append(create_md_cell(sec4_content))

print(f"Final cell count: {len(nb['cells'])}")

# Save updated notebook
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Saved to", nb_path)
