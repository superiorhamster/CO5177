import json
import ast
import shutil
from pathlib import Path

nb_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/ipynb/text/sentimentanalysis.ipynb")
pub_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/pages/notebooks/sentimentanalysis.ipynb")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total cells in notebook: {len(nb['cells'])}")

for idx, cell in enumerate(nb['cells']):
    # Handle source replacement
    source = cell.get('source', '')
    is_list = isinstance(source, list)
    text = "".join(source) if is_list else str(source)
    
    # Specific targeted replacements
    if "PhoBERT-large" in text or "phobert-large" in text or "phobert_large" in text:
        text = text.replace("vinai/phobert-large", "vinai/phobert-base-v2")
        text = text.replace("./phobert-large-local", "./phobert-base-v2-local")
        text = text.replace("/kaggle/working/phobert-large-local", "./phobert-base-v2-local")
        text = text.replace("phobert-large-local", "phobert-base-v2-local")
        text = text.replace("./phobert_large_sentiment", "./phobert_base_v2_sentiment")
        text = text.replace("PhoBERT-large", "PhoBERT-base-v2")
        text = text.replace("PHOBERT-LARGE", "PHOBERT-BASE-V2")
        text = text.replace("370M tham số", "135M tham số (thế hệ 2)")
        
        # Specific tuning for cell 52 (training args)
        if idx == 52:
            text = text.replace("per_device_train_batch_size=8", "per_device_train_batch_size=16")
            text = text.replace("per_device_eval_batch_size=16", "per_device_eval_batch_size=32")
            text = text.replace("gradient_accumulation_steps=4", "gradient_accumulation_steps=2")
            text = text.replace("learning_rate=1.5e-5", "learning_rate=2e-5")
            text = text.replace("# Với PhoBERT-large trên T4 nên giảm batch", "# Với PhoBERT v2 base (135M params) trên T4 có thể dùng batch size 16 mượt mà")
            
        if is_list:
            cell['source'] = [l for l in text.splitlines(keepends=True)]
        else:
            cell['source'] = text
        print(f"Updated cell {idx}")

    # Also clean up any string output that referenced phobert-large
    for out in cell.get('outputs', []):
        if 'text' in out:
            out_is_list = isinstance(out['text'], list)
            out_txt = "".join(out['text']) if out_is_list else str(out['text'])
            if "phobert-large" in out_txt or "PhoBERT-large" in out_txt:
                out_txt = out_txt.replace("phobert-large", "phobert-base-v2")
                out_txt = out_txt.replace("PhoBERT-large", "PhoBERT-base-v2")
                if out_is_list:
                    out['text'] = [l for l in out_txt.splitlines(keepends=True)]
                else:
                    out['text'] = out_txt

# Validate AST syntax on all code cells
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
    print("✅ 100% of code cells passed AST syntax check cleanly!")

# Save to source notebook
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f"Saved to {nb_path}")

# Sync to published copy
shutil.copyfile(nb_path, pub_path)
print(f"Synced to {pub_path}")
