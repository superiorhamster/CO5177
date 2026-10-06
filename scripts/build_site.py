"""Render shared HTML into static pages, retaining file:// and no-JS support."""

import argparse
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"


def render_page(page: Path, templates: dict[str, str]) -> str:
    html = page.read_text(encoding="utf-8")
    # Relative URLs work both locally and beneath the GitHub Pages repo prefix.
    relative_root = Path(os.path.relpath(ROOT, page.parent)).as_posix()
    root = "" if relative_root == "." else relative_root + "/"
    assets = Path(os.path.relpath(PAGES / "assets", page.parent)).as_posix() + "/"
    for name, template in templates.items():
        pattern = re.compile(
            rf"^(?P<indent>[ \t]*)<!-- shared:{name}:start -->.*?<!-- shared:{name}:end -->",
            re.MULTILINE | re.DOTALL,
        )
        matches = list(pattern.finditer(html))
        if len(matches) != 1:
            raise ValueError(f"{page.relative_to(ROOT)} needs exactly one shared:{name} marker pair.")
        indent = matches[0].group("indent")
        body = template.strip().replace("{{root}}", root).replace("{{assets}}", assets)
        block = "\n".join(indent + line if line else "" for line in body.splitlines())
        replacement = (
            f"{indent}<!-- shared:{name}:start -->\n"
            f"{block}\n{indent}<!-- shared:{name}:end -->"
        )
        html = pattern.sub(lambda match: replacement, html, count=1)
    return html


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check for stale shared layout without writing files")
    args = parser.parse_args()
    try:
        templates = {
            name: (PAGES / "partials" / f"{name}.html").read_text(encoding="utf-8")
            for name in ("header", "footer")
        }
        pages = [ROOT / "index.html", *sorted((PAGES / "projects").rglob("*.html"))]
        # Validate every page before writing so a missing marker cannot leave a partial build.
        rendered = {page: render_page(page, templates) for page in pages}
        changed = {
            page: html for page, html in rendered.items()
            if html != page.read_text(encoding="utf-8")
        }
        if args.check:
            for page in changed:
                print(f"Shared layout is stale: {page.relative_to(ROOT)}")
            if changed:
                print("Run python3 scripts/build_site.py to update it.")
                return 1
        else:
            for page, html in changed.items():
                page.write_text(html, encoding="utf-8")
                print(f"Updated {page.relative_to(ROOT)}")
        print("Shared header and footer are up to date.")
        return 0
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
