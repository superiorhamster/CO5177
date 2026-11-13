import json
import ast
import shutil
from pathlib import Path

# Paths
current_nb_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/ipynb/text/sentimentanalysis.ipynb")
published_nb_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/pages/notebooks/sentimentanalysis.ipynb")

# 1. Load sub-module cell lists
with open("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/scratch/eda_cells.json", "r", encoding="utf-8") as f:
    eda_cells = json.load(f)

with open("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/scratch/tfidf_cells.json", "r", encoding="utf-8") as f:
    tfidf_cells = json.load(f)

with open("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/scratch/eval_cells.json", "r", encoding="utf-8") as f:
    eval_cells = json.load(f)

# 2. Load current notebook for middle blocks (preprocessing & models)
with open(current_nb_path, "r", encoding="utf-8") as f:
    current_nb = json.load(f)

# Middle Block A: Data Preprocessing (Cells 18 to 24 of current_nb)
prep_cells = current_nb['cells'][18:25]

# Middle Block B: W2V data prep, W2V models, PhoBERT (Cells 25 to 46 of current_nb)
model_cells = current_nb['cells'][25:46]

print(f"EDA cells count         : {len(eda_cells)}")
print(f"Preprocessing cells count: {len(prep_cells)}")
print(f"TF-IDF cells count      : {len(tfidf_cells)}")
print(f"W2V & PhoBERT cells count: {len(model_cells)}")
print(f"Eval cells count        : {len(eval_cells)}")

# 3. Assemble complete cell list
final_cells = eda_cells + prep_cells + tfidf_cells + model_cells + eval_cells
print(f"Total merged cells count: {len(final_cells)}")

# 4. AST Syntax Check on ALL code cells
errors = []
for idx, cell in enumerate(final_cells):
    if cell['cell_type'] == 'code':
        source = cell.get('source', '')
        if isinstance(source, list):
            text = "".join(source)
        else:
            text = str(source)
        
        # Filter IPython magic lines starting with ! or %
        lines = text.splitlines(keepends=True)
        code_lines = [l for l in lines if not l.strip().startswith(('!', '%'))]
        clean_code = "".join(code_lines)
        
        try:
            ast.parse(clean_code)
        except SyntaxError as e:
            errors.append((idx, str(e)))

if errors:
    print(f"❌ Syntax errors found: {errors}")
    raise SystemExit(1)
else:
    print("✅ 100% of code cells passed AST syntax check!")

# 5. Check for unhandled /kaggle/ paths
hardcoded_paths = []
for idx, cell in enumerate(final_cells):
    source = cell.get('source', '')
    if isinstance(source, list):
        text = "".join(source)
    else:
        text = str(source)
    if '/kaggle/' in text and 'resolve_dataset_dir' not in text:
        hardcoded_paths.append(idx)

if hardcoded_paths:
    print(f"⚠️ Warning: Unhandled Kaggle paths in cells: {hardcoded_paths}")
    raise SystemExit(1)
else:
    print("✅ Zero unhandled Kaggle paths found!")

# 6. Save updated notebook
current_nb['cells'] = final_cells
with open(current_nb_path, "w", encoding="utf-8") as f:
    json.dump(current_nb, f, ensure_ascii=False, indent=1)
print(f"Saved merged notebook to {current_nb_path}")

# 7. Copy to published path
shutil.copyfile(current_nb_path, published_nb_path)
print(f"Synchronized to {published_nb_path}")
