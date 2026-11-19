# CO5177 frontend analysis

This offline review covers the course homepage, the three project reports, their shared frontend, and the GitHub Pages build. The active Tabular page received a closer review. Findings reflect the current files under `CO5177/`.

## Architecture

| Source | Role |
| --- | --- |
| [index.html](../index.html) | Course information, project cards, team details, and submission status. |
| [Tabular](../pages/projects/tabular.html), [Text](../pages/projects/text.html), [Image](../pages/projects/image.html) | Standalone HTML reports with resource links, methodology, results, and section navigation. |
| [site.css](../pages/assets/site.css) | Shared theme, layout, typography, responsive breakpoints, report components, and print rules. |
| [site.js](../pages/assets/site.js) | Vietnamese and English dictionaries, language controls, and preference persistence. |
| [Header](../pages/partials/header.html), [footer](../pages/partials/footer.html), [build script](../scripts/build_site.py) | Python copies the partials into marked HTML blocks and substitutes page-relative paths. |
| [Pages workflow](../.github/workflows/pages.yml) | Rebuilds the shared layout and deploys `index.html`, `.nojekyll`, and the entire `pages/` tree. |

Each route is a physical HTML file. The site uses native navigation and renders content directly from HTML. The deferred shared script updates translated text, accessible labels, image alt text, and metadata where markup opts in. The language preference uses `localStorage` with a fallback to Vietnamese. CSS handles the system color scheme, reduced motion, and printing.

The desktop project layout pairs an article with a contents sidebar. At 700 px or below, the sidebar follows the article in the single-column layout. That order makes section links harder to discover on long reports. The shared skip link, semantic headings, and native fragment navigation provide a baseline for keyboard access.

## Tabular report

The Adult Census Income page links to Colab and gives readers the dataset description, global data-quality checks, data split, train-only exploration and feature selection, preprocessing, evaluation, and conclusions. It compares DummyClassifier, XGBoost, MLP, KNN, and SVM and links directly to the exported test metrics and per-model classification reports. The local notebook exists in the deployment tree.

The page has 14 tables and 15 report figures. Figures declare dimensions, descriptive alternative text, lazy loading, and asynchronous decoding. Scrollable tables use focusable regions with accessible labels. Tabular inherits styles through the `image-report` class and uses a small inline style block for its grid, table widths, and focus outline. Shared report styles are therefore coupled to a page-specific class name.

## Findings and priorities

| Priority | Finding | Suggested change |
| --- | --- | --- |
| High | The [homepage](../index.html#projects) marks Tabular as pending even though the report, Colab link, and local notebook exist. The homepage completion note and both dictionaries repeat the old status and identify the Text notebook as Kaggle, while the [Text resource section](../pages/projects/text.html#resources) links to Colab. | Update the Vietnamese homepage copy and both dictionaries together. Track report availability, PDF/video availability, and notebook execution status separately in the copy. |
| High | Selecting EN switches the document language and shared controls, but the Tabular title, narrative, captions, table labels, and metadata remain Vietnamese. The page has eight text translation bindings, primarily for shared interface elements. This leaves a language mismatch for assistive technology. | Translate the Tabular report and metadata or mark the Vietnamese content with explicit language attributes while English chrome is active. |
| Medium | The Tabular [resource section](../pages/projects/tabular.html#resources) links to Colab only. The [local notebook](../pages/notebooks/Adult_Census_Income_Modeling_Updated.ipynb) already ships with the site. Text and Image offer both links and display their pending PDF and video states. | Link the local Tabular notebook and make resource status consistent across reports. |
| Medium | The shared-layout check fails for Tabular. Comparing against fresh template output showed whitespace and line wrapping differences in the generated header and footer. The workflow already regenerates both blocks before deployment. | Regenerate the checked-in blocks and run the read-only check before committing changes to shared markup. |
| Medium | Deployment includes all files under `pages/`, including saved model artifacts. The KNN and SVM files alone total about 47.4 MB on disk. These files add deployment weight even when readers only request the reports. | Verify which artifacts readers are expected to download and scope the deployment payload accordingly. |
| Low | Tabular uses an Image-specific class to inherit common report rules. The mobile contents navigation appears after the report body. | Consider a shared report class when changing report styles and place section navigation near the top on narrow screens. |

## Verification

- `node --check pages/assets/site.js` passed.
- `python -B scripts/build_site.py --check` flagged only `pages/projects/tabular.html`. A read-only comparison isolated the generated layout differences.
- Static parsing of the four pages found no duplicate IDs, missing local `href` or `src` targets, or broken fragments pointing into those pages.
- External links, live Pages deployment, notebook execution, and browser rendering were outside this offline verification. The accessibility and responsive observations come from markup and CSS inspection.
