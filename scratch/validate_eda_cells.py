import json
import ast
import sys
from pathlib import Path

json_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/scratch/eda_cells.json")
assert json_path.exists(), f"File {json_path} does not exist!"

with open(json_path, "r", encoding="utf-8") as f:
    cells = json.load(f)

print(f"Total cells in JSON: {len(cells)}")
assert len(cells) == 17, f"Expected 17 cells, got {len(cells)}"

# 1. Validate JSON structure & AST of code cells
ast_failures = []
for i, cell in enumerate(cells):
    assert "cell_type" in cell, f"Cell {i} missing cell_type"
    assert "source" in cell, f"Cell {i} missing source"
    ctype = cell["cell_type"]
    src_text = "".join(cell["source"])

    if ctype == "code":
        # Check AST
        py_lines = []
        for line in src_text.splitlines():
            if line.strip().startswith(("!", "%")):
                py_lines.append("# " + line)
            else:
                py_lines.append(line)
        clean_code = "\n".join(py_lines)

        try:
            ast.parse(clean_code)
            print(f"  [Cell {i:2d} | code] AST Check: PASSED")
        except SyntaxError as e:
            print(f"  [Cell {i:2d} | code] AST Check: FAILED -> {e}")
            ast_failures.append((i, str(e)))
    else:
        print(f"  [Cell {i:2d} | markdown] ({len(cell['source'])} lines)")

assert not ast_failures, f"AST failures encountered: {ast_failures}"

# 2. Check no unwanted icons (✅, ⏳, 📁) in cell 3 and cell 7
banned_icons = ["✅", "⏳", "📁"]
for idx in [3, 7]:
    src = "".join(cells[idx]["source"])
    for icon in banned_icons:
        assert icon not in src, f"Banned icon {icon} found in cell {idx}!"
print("\n[CHECK] Banned icons check in Cell 3 and Cell 7: ALL PASSED (none found)")

# 3. Check 5 EDA code cells and their preceding markdown cells
eda_code_indices = [7, 9, 11, 13, 15]
required_subheaders = ["What this step does", "Why it matters", "Questions it answers"]
icon_expectations = [
    (6, "📦 Data Engine"),
    (8, "🔍 Integrity"),
    (10, "🏷️ Labels"),
    (12, "📐 Dimensions"),
    (14, "🔤 Lexicon"),
    (16, "🧹 Preprocessing"),
]

print("\n[CHECK] Verifying 5 EDA markdown + code pairs:")
for md_idx, expected_icon in icon_expectations:
    src = "".join(cells[md_idx]["source"])
    assert expected_icon in src, f"Expected {expected_icon} in cell {md_idx}"
    if md_idx < 16:
        for sub in required_subheaders:
            assert sub in src, f"Missing '{sub}' in cell {md_idx}"
        print(f"  Cell {md_idx} (markdown) -> has '{expected_icon}' and all 3 required points.")
    else:
        print(f"  Cell {md_idx} (Decision Table) -> has '{expected_icon}'.")

for code_idx in eda_code_indices:
    assert cells[code_idx]["cell_type"] == "code"
    print(f"  Cell {code_idx} (code) -> Valid code cell.")

print("\nALL VALIDATION CHECKS PASSED PERFECTLY!")
