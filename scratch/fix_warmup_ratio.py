import json
import ast
import shutil
from pathlib import Path

nb_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/ipynb/text/sentimentanalysis.ipynb")
pub_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/pages/notebooks/sentimentanalysis.ipynb")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Find cell 52 (or cell with TrainingArguments)
target_idx = None
for idx, cell in enumerate(nb['cells']):
    src = "".join(cell.get('source', ''))
    if "training_args = TrainingArguments(" in src:
        target_idx = idx
        break

print(f"Found TrainingArguments in cell {target_idx}")

new_cell_source = """import numpy as np
import inspect
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    TrainerCallback
)
from sklearn.metrics import accuracy_score, f1_score


# Load model local
model = AutoModelForSequenceClassification.from_pretrained(
    "./phobert-base-v2-local",
    num_labels=3
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="macro"),
    }

# Xác định tham số tương thích đa phiên bản transformers (v4.x và v5.x)
train_args_params = inspect.signature(TrainingArguments.__init__).parameters
eval_strat_key = "eval_strategy" if "eval_strategy" in train_args_params else "evaluation_strategy"
eval_kwargs = {eval_strat_key: "epoch"}

training_args = TrainingArguments(
    output_dir="./phobert_base_v2_sentiment",
    learning_rate=2e-5,

    # Với PhoBERT v2 base (135M params) trên T4 có thể dùng batch size 16 mượt mà
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    gradient_accumulation_steps=2,

    num_train_epochs=6,
    weight_decay=0.01,
    warmup_steps=100,                   # Sử dụng warmup_steps thay cho warmup_ratio để tương thích mọi phiên bản transformers
    lr_scheduler_type="cosine",

    save_strategy="epoch",              # vẫn save theo epoch
    load_best_model_at_end=True,
    save_total_limit=2,   
    metric_for_best_model="f1",         # save/best theo f1
    greater_is_better=True,
    fp16=torch.cuda.is_available(),     # Bật fp16 khi có GPU
    report_to="none",
    **eval_kwargs
)

trainer_params = inspect.signature(Trainer.__init__).parameters
tokenizer_kwargs = {"processing_class": tokenizer} if "processing_class" in trainer_params else {"tokenizer": tokenizer}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_split,
    eval_dataset=val_split,
    compute_metrics=compute_metrics,
    callbacks=[
        EarlyStoppingCallback(early_stopping_patience=2)
    ],
    **tokenizer_kwargs
)

trainer.train()
trainer.evaluate(tokenized_test)"""

nb['cells'][target_idx]['source'] = [l for l in new_cell_source.splitlines(keepends=True)]

# Also clear the old warning in outputs of cell 52
for out in nb['cells'][target_idx].get('outputs', []):
    if 'text' in out:
        out_is_list = isinstance(out['text'], list)
        out_txt = "".join(out['text']) if out_is_list else str(out['text'])
        out_txt = out_txt.replace("warmup_ratio is deprecated and will be removed in v5.2. Use `warmup_steps` instead.\n", "")
        if out_is_list:
            out['text'] = [l for l in out_txt.splitlines(keepends=True)]
        else:
            out['text'] = out_txt

# Validate AST
errors = []
for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = cell.get('source', '')
        text = "".join(source) if isinstance(source, list) else str(source)
        code_lines = [l for l in text.splitlines(keepends=True) if not l.strip().startswith(('!', '%'))]
        try:
            ast.parse("".join(code_lines))
        except SyntaxError as e:
            errors.append((idx, str(e)))

if errors:
    print(f"❌ Syntax errors: {errors}")
    raise SystemExit(1)
else:
    print("✅ 100% of code cells passed AST syntax check!")

# Save to source notebook
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f"Saved to {nb_path}")

# Sync to published copy
shutil.copyfile(nb_path, pub_path)
print(f"Synced to {pub_path}")
