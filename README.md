# CO5177 assignment portfolio

A Vietnamese static website for the CO5177 course portfolio, semester 261 of the 2026–2027 academic year. Group **SlightSeek** presents three reports: [Tabular](pages/projects/tabular.html), [Text](pages/projects/text.html), and [Image](pages/projects/image.html).

Phạm Duy Anh (2310139) contributed to Text and Image. Nguyễn Phan Tuấn Duy (2310491) contributed to Tabular and Text. Each report links to a Colab notebook and a local notebook download. The report pages mark PDF and YouTube resources as pending. See the [course requirements](requirements.md) for the submission checklist and LMS requirements.

## Local development

From the repository root, open [index.html](index.html) directly or use Python to serve the site:

```sh
python -B -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/`. Preview uses the checked-in HTML, local CSS, and vanilla JavaScript. Python 3.9 or later runs the build script using its standard library. Node.js is only needed for the JavaScript syntax check below. JavaScript enhances mobile navigation. The static sidebar and report contents remain accessible with JavaScript disabled.

| Path | Purpose |
| --- | --- |
| [index.html](index.html) | Homepage, course and team information, and project links |
| [pages/projects/](pages/projects/) | Report HTML and per-report tables of contents |
| [pages/partials/](pages/partials/) | Shared header and footer sources |
| [pages/assets/site.css](pages/assets/site.css) and [navigation.js](pages/assets/navigation.js) | Layout, themes, print styles, and mobile drawer behavior |
| [pages/notebooks/](pages/notebooks/) and [ipynb/](ipynb/) | Website downloads and repository notebook sources, respectively |
| [scripts/build_site.py](scripts/build_site.py) | Expands the shared marker blocks in the homepage and reports |
| [Pages workflow](.github/workflows/pages.yml) | Builds and packages the static site on GitHub Actions |

After changing either shared partial, regenerate the embedded header and footer. Use the read-only check to catch stale generated markup. Report bodies and report TOCs are maintained in their respective HTML files.

```sh
python -B scripts/build_site.py
python -B scripts/build_site.py --check
node --check pages/assets/navigation.js
git diff --check
```

## GitHub Pages

The workflow rebuilds shared markup and stages root `index.html`, `.nojekyll`, and `pages/`. The upload action archives the static payload with hidden files excluded. A clean checkout supplies only files tracked in the selected revision, so check new assets and notebook downloads with `git ls-files`. Keep site URLs relative for direct-file preview and the `/CO5177/` project prefix. The workflow runs on matching pushes to `main` and supports manual dispatch. Release owners manage the intended revision, Pages publishing source, and deployment approval. [Workflow source](.github/workflows/pages.yml)

## Documentation

- [Content editing guide](docs/CONTENT_EDITING_GUIDE.md) for report sections, resources, shared UI, and the contributor checklist.
- [UI development report](docs/UI_DEVELOPMENT_REPORT.md) for design history, verified outcomes, and open risks.
- [Implementation plan](docs/TUFTE_UI_IMPLEMENTATION_PLAN.md) for approved decisions and detailed phase validation.
- [AGENTS.md](AGENTS.md) for the current agent handoff.
- [Original frontend analysis](docs/FRONTEND_ANALYSIS.md) and [legacy handoff](AGENT.md) for historical context. Use current source and the guides for active instructions.
