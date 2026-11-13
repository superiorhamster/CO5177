import json
import ast
import shutil
from pathlib import Path

nb_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/ipynb/text/sentimentanalysis.ipynb")
pub_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/pages/notebooks/sentimentanalysis.ipynb")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Find cell 24
target_idx = None
for idx, cell in enumerate(nb['cells']):
    src = "".join(cell.get('source', ''))
    if "def pad_sequences(sequences, maxlen):" in src:
        target_idx = idx
        break

print(f"Found pad_sequences in cell {target_idx}")
src_text = "".join(nb['cells'][target_idx]['source'])

old_pad_func = """def pad_sequences(sequences, maxlen):
    padded = np.zeros((len(sequences), maxlen), dtype=int)
    for i, seq in enumerate(sequences):
        if len(seq) > maxlen:
            padded[i, :] = seq[:maxlen] 
        else:
            padded[i, -len(seq):] = seq 
    return padded"""

new_pad_func = """def pad_sequences(sequences, maxlen):
    \"\"\"Cắt hoặc thêm 0 (pre-padding) để các chuỗi có độ dài bằng nhau.
    Xử lý an toàn trường hợp chuỗi rỗng len(seq) == 0 để tránh lỗi slice broadcast.\"\"\"
    padded = np.zeros((len(sequences), maxlen), dtype=int)
    for i, seq in enumerate(sequences):
        if len(seq) == 0:
            continue  # Chuỗi rỗng giữ nguyên toàn bộ 0 (pad token)
        elif len(seq) > maxlen:
            padded[i, :] = seq[:maxlen] 
        else:
            padded[i, -len(seq):] = seq 
    return padded"""

if old_pad_func in src_text:
    src_text = src_text.replace(old_pad_func, new_pad_func)
    nb['cells'][target_idx]['source'] = [l for l in src_text.splitlines(keepends=True)]
    print("Successfully replaced pad_sequences function.")
else:
    print("Warning: old_pad_func string did not match exactly, doing regex/line replacement.")
    lines = src_text.splitlines(keepends=True)
    new_lines = []
    in_pad = False
    for line in lines:
        if "def pad_sequences" in line:
            in_pad = True
            new_lines.append(new_pad_func + "\n")
        elif in_pad:
            if line.strip().startswith("return padded"):
                in_pad = False
        else:
            new_lines.append(line)
    nb['cells'][target_idx]['source'] = new_lines

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
