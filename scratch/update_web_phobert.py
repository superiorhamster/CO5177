from pathlib import Path

# Files to update
text_html_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/pages/projects/text.html")
index_html_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/index.html")
site_js_path = Path("/home/anhpd/Project/Group/LapTrinhAIDS/Assignment/pages/assets/site.js")

# 1. Update text.html
with open(text_html_path, "r", encoding="utf-8") as f:
    text_html = f.read()

text_html_updated = text_html.replace("vinai/phobert-large", "vinai/phobert-base-v2")
text_html_updated = text_html_updated.replace("PhoBERT-large", "PhoBERT-base-v2")
text_html_updated = text_html_updated.replace("phobert-large", "phobert-base-v2")

with open(text_html_path, "w", encoding="utf-8") as f:
    f.write(text_html_updated)
print("Updated text.html")

# 2. Update index.html
with open(index_html_path, "r", encoding="utf-8") as f:
    index_html = f.read()

index_html_updated = index_html.replace("PhoBERT-large", "PhoBERT-base-v2")
index_html_updated = index_html_updated.replace("phobert-large", "phobert-base-v2")

with open(index_html_path, "w", encoding="utf-8") as f:
    f.write(index_html_updated)
print("Updated index.html")

# 3. Update site.js
with open(site_js_path, "r", encoding="utf-8") as f:
    site_js = f.read()

site_js_updated = site_js.replace("vinai/phobert-large", "vinai/phobert-base-v2")
site_js_updated = site_js_updated.replace("PhoBERT-large", "PhoBERT-base-v2")
site_js_updated = site_js_updated.replace("phobert-large", "phobert-base-v2")

with open(site_js_path, "w", encoding="utf-8") as f:
    f.write(site_js_updated)
print("Updated site.js")
