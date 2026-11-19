# CO5177 content editing guide

Use [requirements.md](../requirements.md) for submission rules and the [development report](UI_DEVELOPMENT_REPORT.md) for the rationale behind the layout. Run commands from the CO5177 repository root.

## 1. Find the report and its evidence

| Report | Page | Figure and result files | Notebook source | Website notebook download |
| --- | --- | --- | --- | --- |
| Tabular | [tabular.html](../pages/projects/tabular.html) | [Adult_Census_Income_Results/](../pages/assets/Adult_Census_Income_Results/) | [Adult_Census_Income_Modeling_Updated.ipynb](../ipynb/tabular/Adult_Census_Income_Modeling_Updated.ipynb) | [Adult_Census_Income_Modeling_Updated.ipynb](../pages/notebooks/Adult_Census_Income_Modeling_Updated.ipynb) |
| Text | [text.html](../pages/projects/text.html) | [vlsp-sentiment/](../pages/assets/vlsp-sentiment/) | [sentimentanalysis.ipynb](../ipynb/text/sentimentanalysis.ipynb) | [sentimentanalysis.ipynb](../pages/notebooks/sentimentanalysis.ipynb) |
| Image | [image.html](../pages/projects/image.html) | [intel-image/](../pages/assets/intel-image/) | [intel_image_classification_trained.ipynb](../ipynb/image/intel_image_classification_trained.ipynb) | [intel_image_classification_trained.ipynb](../pages/notebooks/intel_image_classification_trained.ipynb) |

The Tabular figure folders are `EDA_result/` and `Model_result/`. The latter also contains [test_metrics.csv](../pages/assets/Adult_Census_Income_Results/Model_result/test_metrics.csv) and five text classification reports. The Tabular Colab output description mentions `Saved_models/`, which is ignored by Git and excluded from published links. The Text file `ipynb/text/sentimentanalysis_CO5177.ipynb` is separate from the source/download pair above.

## 2. Update the homepage or a report section

1. Run `git status --short` and edit the smallest relevant block. Update course, team, and card copy in [index.html](../index.html). Report sidebars contain their own group, scope, or requirements panels. Synchronize related facts when an authorized change affects both.
2. In the report, locate `<main id="main">`, then the relevant section by ID. Tabular has `#dataset`, `#eda-cleaning`, `#preparation`, `#eda`, `#preprocessing`, `#analysis`, and `#conclusions`. Text and Image use `#dataset`, `#preparation`, `#analysis`, and `#conclusions`, with nested anchors such as `#eda` and Text's `#results`. Each page has `#resources`.
3. Preserve the section order and existing IDs. If you add a section entry to the report TOC, edit the report's `.report-toc` and link to the real ID in the same file. Its position outside the generated header markers lets it survive a shared layout rebuild.
4. Check the evidence behind changed numerical claims. When authorized results change, reconcile the report prose, table, chart captions and downloadable metrics. Keep recorded outputs and independently reproduced runs clearly distinguished.

## 3. Add a figure or table

### Figures

1. Place the original image in the corresponding tracked asset directory above. Keep the filename case consistent. From a report, point both the figure link and image at `../assets/<directory>/<filename>`.
2. Follow the report's `figure.report-figure` pattern. The example uses an existing Tabular image. Provide actual intrinsic dimensions, meaningful alt text, and a concise adjacent caption. Keep the link to the full-size image.
3. Use the standard centered measure first. For a genuinely dense figure, follow `.tabular-figure-wide` in Tabular or `.report-figure-wide` in Text and Image. Keep aspect ratio and verify that a figure and its caption stay together at narrow widths and in print.

```html
<figure class="report-figure tabular-figure-reading">
  <a class="figure-image-link"
     href="../assets/Adult_Census_Income_Results/EDA_result/income_full.png"
     aria-label="Mở hình Phân phối thu nhập trước khi lọc">
    <img src="../assets/Adult_Census_Income_Results/EDA_result/income_full.png"
         width="1102" height="618" loading="lazy" decoding="async"
         alt="Phân phối thu nhập trước khi lọc" />
  </a>
  <figcaption>
    <strong>Phân phối thu nhập trước khi lọc</strong>
    <span>Số lượng và tỷ lệ của hai lớp trên toàn bộ dữ liệu Adult.</span>
  </figcaption>
</figure>
```

### Tables

1. Keep a native `table` inside `.table-wrap.report-table`. Use a meaningful `caption` or the existing adjacent heading, and `thead` and `tbody` with `th scope="col"` and `th scope="row"` as applicable.
2. Follow the existing focusable scroll region pattern. Use `tabindex="0"`, `role="region"` and either a descriptive `aria-label` or `aria-labelledby` pointing to an existing heading. For numeric columns, use `.tabular-number` in Tabular and `.report-number` in Text and Image on the relevant headers and data cells.
3. Check that values agree with the source, horizontal scroll stays within the table region, arrow keys move it when focused, and print keeps all columns readable. Use landscape preview for a dense table if needed.

## 4. Edit Notebook, PDF report or YouTube links

1. Open the report's `#resources` section. Keep the Notebook, PDF report, and YouTube rows in that order.
2. For Notebook, keep the report-specific description. In `.resource-actions`, update the Colab destination only when an approved replacement exists. Keep the separate local download anchor with its `download` attribute and a path under `../notebooks/`. Confirm the correct file exists and is included in the release revision. Compare it with its corresponding file under `ipynb/` before changing either copy. Public Colab access and **Run all** require separate verification.
3. For PDF, replace the row's `.resource-pending` with an `a.text-link` once you have an approved, accessible PDF. Use a verified external URL or place the real PDF under `pages/` and link to it relatively. If the team chooses a new `pages/reports/` directory, create it when the first actual PDF is available.
4. For YouTube, replace the pending label with an `a.text-link` to the verified Public or Unlisted video. The course recommends 5–10 minutes. Leave pending labels in place for resources that are still unavailable.
5. Update the homepage status copy only when the new availability is verified and the change is authorized. Keep unrelated statuses and links intact. [Course requirements](../requirements.md)

## 5. Maintain shared UI and generated blocks

- Edit [header.html](../pages/partials/header.html) for the shared BK brand and primary navigation, and [footer.html](../pages/partials/footer.html) for the semester label and source link. Keep one start/end marker pair for each partial on each page. The renderer replaces only the marked blocks, so maintain report-specific navigation and content in the page.
- The renderer resolves `{{root}}`, `{{assets}}`, and `{{current:...}}` into page-relative paths and the appropriate static `aria-current="page"`. After a partial edit, run `python -B scripts/build_site.py` and review the generated HTML diff. [Build script](../scripts/build_site.py)
- Edit [site.css](../pages/assets/site.css) for scoped layout or print changes. The sidebar turns into a drawer below the desktop breakpoint when [navigation.js](../pages/assets/navigation.js) initializes. Preserve the in-flow no-JavaScript fallback, keyboard focus, and original BK logo. Keep the CSS and JavaScript breakpoint aligned if it ever changes.
- Use relative site URLs. GitHub Actions builds from the selected checkout and stages the site files from that revision. An ignored or untracked file can work locally and be missing from the hosted artifact. [Pages workflow](../.github/workflows/pages.yml)

## 6. Checklist before review

- [ ] Read the diff for approved changes only. Confirm claims, labels, resource statuses, and figures still agree with their evidence.
- [ ] Run the checks below. If a partial changed, run the renderer first.
- [ ] Test edited links, report fragments, source-image links, notebook downloads and pending status labels. Verify the exact case of new filenames and that release assets appear in `git ls-files`.
- [ ] Preview on narrow and wide screens in light and dark mode. Test keyboard focus, mobile drawer dismissal, the no-JavaScript sidebar, and print preview when the change affects those areas.
- [ ] Record completed checks and unresolved evidence. For an approved release, verify the intended revision, the GitHub Actions Pages source, and public access to required resources. Follow the course requirements for GroupRegistration, GroupLink, and the combined LMS PDF.

```sh
python -B scripts/build_site.py --check
node --check pages/assets/navigation.js
git diff --check
```
