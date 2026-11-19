# CO5177 Premium Academic Dashboard Implementation Plan

## 1. Executive design summary and constraints

**Option B is approved as the design direction. Phase 1A is approved. Phase 1B and later require explicit approval.**

Use a persistent navy left sidebar across all four pages and an ivory/white dashboard canvas with subtle blue accents, restrained panels, and clear hierarchy for routes, titles, resources and scientific evidence. Pilot the report layout on Tabular, then roll it out to Text and Image. Tufte informs typography, tables and captions. Academic Project informs institutional identity and resource placement.

Preserve every original academic section, numerical result, figure, table, link, resource state and behavior, except the approved removal of bilingual mode. Keep the exact university logo in each sidebar and print header. Retain static HTML/CSS, vanilla JavaScript, Python partial rendering and GitHub Pages. The existing plan filename is retained for continuity.

## 2. Verified current architecture and page inventory

| Route | Current sections in order | Baseline counts |
| --- | --- | --- |
| [Homepage](../index.html) | Header, introduction and course record, three project cards, team and contributions, completion notice, footer | 1 logo, 3 SVGs, 1 table (3 rows, 4 header and 8 data cells), 13 links |
| [Tabular](../pages/projects/tabular.html) | Breadcrumb, introduction, resources, dataset, global quality, split, Train EDA and feature selection, preprocessing, training/evaluation, conclusions/source, TOC/team/scope, project navigation, footer | 15 figures/captions, 16 images with logo, 14 tables (93 rows, 132 header and 225 data cells), 44 links, 115 code nodes |
| [Text](../pages/projects/text.html) | Breadcrumb, introduction, resources, dataset/EDA, preparation, modeling/test, conclusions/reproducibility, TOC/team/requirements, project navigation, footer | 4 figures/captions, 5 images with logo, 9 tables (53 rows, 85 header and 160 data cells), 25 links, 1 code node |
| [Image](../pages/projects/image.html) | Breadcrumb, introduction, resources, dataset/EDA, preparation, modeling/error analysis, conclusions/reproducibility, TOC/team/requirements, project navigation, footer | 9 figures/captions, 10 images with logo, 5 tables (29 rows, 45 header and 69 data cells), 27 links, 2 code nodes |

The following describes the pre-1A baseline. All routes are physical files. Shared [CSS](../pages/assets/site.css) provides responsive layouts, system themes, focus, reduced motion and print. The former deferred script (`pages/assets/site.js`) updates opted-in text, ARIA labels, alt text and metadata, document language and button state. It stores the preference under `co5177-language` with Vietnamese fallback if storage fails. Native links handle routes, fragments, original images and notebook downloads. The [Python renderer](../scripts/build_site.py) embeds header/footer blocks with page-relative paths. The [workflow](../.github/workflows/pages.yml) regenerates those blocks and stages `index.html`, `.nojekyll` and all of `pages/`.

**Existing issues, separate from the redesign**

- The homepage originally marked Tabular pending. Phase 5 now records the existing report and local notebook download, with PDF and video still pending. The separate Text notebook provider wording remains a content decision.
- The static Vietnamese H1 “Dữ liệu nhiều để làm gì.” differs from the Vietnamese dictionary “Từ dữ liệu đến hiểu biết.” The static lecturer label was "Giảng viên hướng"; the dictionary used "Giảng viên". Three Text error-example explanations and the conclusion used double quotes in HTML and single quotes in the dictionary. Phase 1A retains all static values, including this punctuation and these labels. Academic claims, resource statuses, and facts are unchanged.
- Tabular has eight text translation bindings, largely for chrome. On EN, its unbound report, title and metadata remain Vietnamese while document language changes. Keep the existing static wording. A single Vietnamese document language resolves the former EN mismatch.
- The mobile TOC follows the article. Tabular borrows `.image-report` and has inline CSS for its grid, table width and focus. The shared-layout check reproduced the Tabular drift documented in [FRONTEND_ANALYSIS.md](FRONTEND_ANALYSIS.md). JavaScript syntax passed.
- The local KNN and SVM artifacts total 47,439,711 bytes. The workflow includes them if present in its checkout. The ignore rules alone do not establish what is tracked or deployed.

## 3. Tufte CSS, Academic Project, and skill findings

| Local source | Design implications |
| --- | --- |
| [Tufte README](../../.ui-references/tufte-css/README.md), [demo](../../.ui-references/tufte-css/index.html), [CSS](../../.ui-references/tufte-css/tufte.css) | Borrow only typographic clarity, data integrity, legible scientific plates and captions near evidence. Do not adopt the book/article layout or margin-note architecture as the primary UI. |
| [Academic Project README](../../.ui-references/academic-project/README.md), [HTML](../../.ui-references/academic-project/index.html) | Borrow university identity, project hierarchy and resource-action clarity as design inspiration. Keep the existing CO5177 page structure and dependencies. |
| [ui-ux-pro-max](../../.agents/skills/ui-ux-pro-max/SKILL.md) | Apply contrast, focus, reflow, keyboard order and readable type guidance. |
| [design-system](../../.agents/skills/design-system/SKILL.md) | Use primitive palette/scale values, semantic roles, and component aliases where needed. Implement directly in CSS. |
| [ui-styling](../../.agents/skills/ui-styling/SKILL.md) | Apply responsive and accessibility-first guidance with native HTML controls. Keep the existing vanilla stack. |

## 4. Component preservation matrix

Before implementation, capture an ordered manifest for the academic article and a per-page manifest for the surrounding interface. Capture literal text, mathematical notation, headings, lists, code, media attributes, names, accessible relationships, routes, and resource states. The matrix identifies inventory boundaries for the comparison.

| Component | Exact source location | Existing purpose or behavior | Proposed visual treatment | Preserve | Verification |
| --- | --- | --- | --- | --- | --- |
| Document head | All four pages, `head` | Metadata, favicon, shared assets and language bindings | Keep existing load order | All title/meta values, bindings, refs | Compare static Vietnamese metadata and requests |
| Skip, masthead, logo, nav and language | All four pages before `#main`, `pages/partials/header.html`, `.skip-link`, `.brand`, `.main-nav`, `.language-switch` | Main-content jump, home/projects/team/source navigation and VI/EN | Persistent sidebar branding and navigation, visible focus | Existing destinations and exact logo. Remove bilingual controls and state. | Tab and activate every control, confirm all logo URLs |
| Homepage opening and facts | `index.html` lines 41–91, `.hero`, `.course-sheet` | Intro, course name, CTA, semester, course/institution facts | Dashboard overview header and restrained information panel | All original labels, facts and links | Compare static Vietnamese DOM |
| Project cards | `index.html#projects`, three `.project-card` nodes | Routes, SVGs, labels, arrows, summaries and statuses | Three premium dashboard project cards | Order, whole-card click, text, icons and links | Compare and activate all three targets |
| Team and submission | `index.html#team`, `.completion-note` | Group/member/contribution details and status notice | Dashboard team table and status panel | Every row, label, link, icon and status | Compare cells and test mobile flow |
| Breadcrumb and report masthead | All reports `.breadcrumb`, `.project-hero`, `#project-title` | Home return, project identity, summary and state | Dashboard report title and metadata strip | All text, symbols where present, links and states | Compare headings and navigation |
| Resources | All reports `#resources` | Notebook links, existing downloads, pending PDF/video labels | Compact dashboard resource panel | Exact targets, rel, target and download attrs, pending text | Compare URL strings and test local downloads |
| Tabular dataset and quality | `tabular.html#dataset`, `#eda-cleaning`, `#preparation` | Inputs, target, class distribution, missingness, duplicates, negative checks and split | Prose paired with evidence plates | Every feature, count, formula and split | Compare ordered headings, text, tables and figures |
| Tabular Train EDA and preprocessing | `tabular.html#eda`, `#preprocessing` | Imputation, imbalance, univariate distributions, 3 × IQR, relationships, target relevance, encodings, three input branches and SMOTENC | Wider distribution plots and table grid | Every subsection, label, measured value and figure | Compare each cell, caption and asset |
| Tabular models and conclusions | `tabular.html#analysis`, `#conclusions`, `.report-source-note` | Five model configurations, test results, reuse, CSV and reports, evidence | Wide evaluation blocks and source note | All model data and results, six CSV/TXT links, conclusions | Verify all 14 tables and 15 figures across report |
| Text dataset and prep | `text.html#dataset`, `#eda`, `#preparation` | Length/checks, vocabulary, cleaning, representations and splits | Reading measure with full evidence width | Ordered prose, code, labels, figures and links | Compare ordered nodes in static Vietnamese |
| Text models and conclusions | `text.html#analysis`, `#results`, `#conclusions`, `.report-source-note` | Architecture, 12 runs, augmentation gain, class errors/examples, limitations, next steps and sources | Wide benchmark/error tables and inline source note | All results, examples, interpretation and claims | Verify 9 tables, 4 figures and deep links |
| Image dataset and prep | `image.html#dataset`, `#eda`, `#eda-decisions-title`, `#preparation` | EDA, size/color/quality, cleaning, leakage, class counts and transforms | Wide figures, captions and wrapped method cells | Every evidence and procedure block | Compare values, alt text and captions |
| Image models and conclusions | `image.html#analysis`, `#conclusions`, `.report-source-note` | Two-stage transfer learning, test results, class F1, errors, limitations, extensions and reproducibility | Full article width for matrices and error panels | All metrics, source assets, captions and prose | Verify 5 tables, 9 figures and all destinations |
| TOC, team and requirements | All reports `.project-sidebar`, first `.sidebar-block`, `.group-block`, `.requirements-block` | Anchors, group details and scope/requirements | Move the existing TOC into the shared sidebar and its mobile drawer. Keep group and requirements in the content flow. | All labels and fragment targets, team items, scope and requirements | Follow every anchor, compare sidebar text |
| Evidence and technical components | All reports `.report-figure`, `figcaption`, `.figure-image-link`, `.table-wrap`, `.report-table`, lists, code and notes | Original images and links, captions, scrollable tables and narrative context | Wide plates, ruled tables and readable notes | Exact bytes, alt/loading attributes, row/cell/spans, labels, code and sequence | Compare hashes and ordered element/attribute manifests |
| Footer | Report `.project-footer-nav`, all `.site-footer`, `pages/partials/footer.html` | Next/all-project links, semester and source | Compact dashboard footer | Destinations, labels and source order | Test every footer link and compare text |
| Interaction and print | `pages/assets/site.js` and responsive/print rules in `pages/assets/site.css` | Baseline language persistence, no-JS fallback, theme, reduced motion and print | Reflow and white-paper reading layout | Preserve behavior except bilingual mode and keep access to all content | Keyboard, no-JS and PDF preview checks |

## 5. Mandatory bk.png branding

The exact [bk.png](../pages/assets/bk.png) is a 256 × 258 RGBA image (41,016 bytes). Keep its bytes, color, transparency and aspect ratio. In the shared sidebar branding block use `{{assets}}bk.png`, which generates `pages/assets/bk.png` at home and `../assets/bk.png` in all three reports. Reserve native-ratio dimensions. Set the displayed width around 44 px desktop, 36 px mobile and 32–36 px print, with automatic height. Align to the course label. Use a restrained light backing only where needed in dark mode. Give the mark alt text using the existing source name “Đại học Bách Khoa - ĐHQG-HCM.” Ensure the brand link's accessible name contains both course and institution, accounting for the existing parent aria-label. Keep favicon links. Review all four desktop sidebars, opened mobile drawers, in-flow no-JS sidebars and print headers for the original mark. Reuse the same brand node for print.

## 6. Typography and color tokens

Checking the Unicode cmap in all five bundled ET Book TTFs found that they lack Ă, Đ, Ơ, ư, the U+1EA0–U+1EF9 precomposed range, and tested combining accents U+0300, U+0301, U+0303, U+0309 and U+0323. Webfont binary parity and browser shaping remain unverified. Use `"Segoe UI", system-ui, sans-serif` as the primary UI and body font. Reserve `Georgia, "Times New Roman", "Noto Serif", serif` for selective large headings if Vietnamese shaping is verified. Use `"Segoe UI", system-ui, sans-serif` for controls/tables and `ui-monospace, Consolas, "Liberation Mono", monospace` for code. Test Vietnamese stacked accents in regular, italic and bold. If consistent platform rendering requires bundling, evaluate a verified Vietnamese-capable Noto Serif or Source Serif 4 distribution with its corresponding SIL OFL notice as a separate approval.

- H1 2–3.2 rem at 1.15–1.22, H2 1.55–2.1 rem at 1.25, H3 1.125–1.35 rem at 1.35.
- Prose approximately 1–1.0625 rem at 1.6–1.7 with a comfortable max measure where appropriate, but dashboard panels and evidence can use the full content width. Narrow view approximately 1 rem at 1.6. Paragraph gap 0.85–1 em.
- Captions and navigation 0.875–1 rem at 1.45–1.55. Tables 0.875–0.9375 rem at 1.45 with lining/tabular numerals. Code 0.9 em with safe wrapping of long identifiers. Spacing scale 4, 8, 12, 16, 24, 32, 48, 64 px.

| Semantic role | Light | Dark |
| --- | --- | --- |
| Page | #F8F5ED | #151A22 |
| Surface | #FFFFFF | #202732 |
| Ink | #23262B | #F2EFE8 |
| Muted | #505560 | #C2C7CF |
| Accent | #203B61 | #B8D2FA |
| Surface tint | #ECE8DE | #2E394A |
| Rule | #D5CCBB | #455166 |
| Focus | #315A8F | #9CC8FF |
| Figure paper | #FFFFFF | #FFFFFF |

Map the current blue, blue-soft, line and teal variables to semantic accent, tint, rule and focus roles during migration. Decorative rules may remain subtle. Functional boundaries, text and focus colors must pass contrast checks on their actual backgrounds.

## 7. Homepage design specification

Use the same persistent left sidebar as the reports. In the content area, provide a dashboard overview heading, existing course introduction, CTA and semester information, with a course-information panel alongside where space allows. Stack in source order on narrow screens. Use the verified course name “Nền tảng lập trình cho phân tích và trực quan dữ liệu,” faculty “Khoa Khoa học và Kỹ thuật Máy tính,” lecturer “TS. Lê Thành Sách,” and the existing semester details without rewriting them. Keep three linked project cards, all SVGs, types, descriptions, arrows and status elements. Use premium but restrained cards with light borders, modest radius, accessible hover/focus and the existing whole-card link. Leave the team table and completion notice in sequence, using restrained dashboard panels. Keep the footer and all anchors.

## 8. Shared dashboard shell and report layouts

- Use a two-track desktop grid with a sticky navy sidebar approximately 240 to 280 px wide and a flexible `minmax(0, 1fr)` canvas. Phase 1A uses 80 rem so the existing inner report layout keeps sufficient canvas width and stacks the site navigation at 1024 px. Recheck the breakpoint during 1C after the 1B TOC migration. Keep document scrolling for the canvas and let a tall sidebar scroll independently. The shared primary group adds Overview, Tabular, Text and Image. Preserve Projects, Team and GitHub links and use Vietnamese labels. Give the current primary route `aria-current="page"` and an indicator distinguishable without color.
- Each page owns the sidebar and canvas wrappers. Place the existing generated header marker pair inside the sidebar for the shared brand and primary navigation. In 1B, move each report's existing TOC into that same sidebar as a page-owned sibling outside the marker pair. This keeps route-specific anchors safe when the renderer replaces the generated block. The homepage has no report TOC. Keep group and requirements/scope panels together after the report article in the canvas. Keep the shared footer after existing project navigation. Use one persistent navigation column.
- Use a compact report title and resource panel followed by ordered analysis panels. Limit prose measure where useful and allow dense evidence to use the full available canvas. Keep captions, original-image links and interpretations adjacent to the evidence. Use existing content for all panels. The dashboard mockup supplies composition ideas only.
- **Tabular.** Keep all seven numbered sections and the source note. Preserve global checks, Train-only analysis and Test reporting with wide panels for feature dictionaries, distributions, associations and comparisons.
- **Text.** Keep EDA, preparation, benchmarks, augmentation, class errors, examples and reproducibility. Preserve `#eda` and `#results` and support long cell text.
- **Image.** Keep the sequence from EDA through processing decisions and transforms to class/error analysis. Use maximum available evidence width for dense scientific plates.

## 9. Figures, charts, captions, statistical tables, and sidenotes

- **Standard figures.** Center the figure and its attached caption horizontally within the panel. Use a readable maximum width and scale down to fit on narrow screens. Keep the intrinsic aspect ratio, original asset, alt text, loading attributes and original-image link. Preserve unused space where it helps keep the figure at a reasonable size.
- **Wide or detail-heavy figures.** Use a larger centered width when label legibility requires it, such as Tabular's target relevance and confusion matrices. Keep proportional scaling and avoid enlargement beyond intrinsic size solely to fill the panel. Retain original-image links for close inspection.
- **Rollout.** Apply this centered sizing policy in the Tabular pilot (Phase 2) and to Text and Image in Phase 4, choosing their wider figures individually. Review desktop, mobile and print for image and caption alignment.
- **Multi-panel figures.** Keep any composite image intact. Allow existing adjacent figure pairs to sit side by side only where DOM order, caption identity, and near-text context remain intact. Stack in that order on mobile.
- **Tables.** Keep native table structure, captions, labels, headers/scopes, rows, spans and all original cells. Align numeric values by type with tabular digits, and wrap explanatory cells. Use a bounded `.table-wrap` with keyboard scrolling, focus indicators and accessible region labels wherever needed. Start with existing per-table minimum widths (420–840 px, including Tabular's 620 px and Text splits' 760 px), then check each at narrow widths. Allow scroll only within the evidence region. In print remove clipping, wrap text and repeat header rows where supported. Use landscape if necessary to fit dense tables.
- **Sidenotes.** Keep current notes inline in the pilot. Prefer compact callouts within the dashboard; do not add a Tufte-style margin-note column or invent tooltips. Keep interpretive and reproducibility notes directly in the reading flow.

## 10. Navigation, responsiveness, accessibility, Vietnamese UI, and print

In 1A, keep small-screen navigation in flow without scripting. In 1B, at tablet/mobile widths progressively enhance the same sidebar subtree into a native modal dialog drawer. Render it before `#main` in ordinary document flow by default. Show the labeled toggle only after initialization succeeds. If dialog support or JavaScript is unavailable, the in-flow navigation remains usable. The drawer reuses a single sidebar subtree with its original logo and report TOC.

Plan a small vanilla controller for expanded state, initial focus, close button, Escape, backdrop dismissal and return focus. Use modal focus containment and background inertness while open. For a same-page TOC link, dismiss the drawer without swallowing native fragment/history behavior, then focus the destination heading instead of the trigger. Restore the sidebar to its static location when switching to desktop and before printing if the drawer is open. Keep the skip link before navigation and preserve its target. Maintain visible focus, readable zoom/reflow, scroll margins and approximately 44 px targets where feasible. Respect reduced motion and system themes.

The site is Vietnamese-only starting in 1A. Keep `lang="vi"` on all pages. Remove the VI/EN control and its ARIA state, dictionaries, all translation bindings, dynamic translation and metadata updates, and reads/writes of `co5177-language`. Remove the script asset and references if it contains only translation behavior. Preserve the static Vietnamese text, labels, metadata and alt text when dictionary values differ, and note the discrepancies without updating facts or statuses. Existing English technical terms, citations and code remain. Use static Vietnamese labels for future drawer controls.

For A4 and Letter, revert the shell to document flow and present the original shared brand as a print header on white. Hide interactive navigation while preserving the brand, resource link text and all academic evidence. Clear sticky/fixed positioning, overflow clipping and dark backgrounds. Allow table pagination and test landscape for dense evidence.

## 11. CSS integration strategy and collisions

| Approach | Assessment |
| --- | --- |
| Scope a complete Tufte stylesheet | Still creates a second cascade and requires rewriting global selectors and float-based layout. |
| Extract selected upstream rules | Viable for a proven case, with selector review and MIT notice for substantial copied portions. |
| Adapt current `pages/assets/site.css` | Recommended. Independently implement sidebar/dashboard shell, palette, UI typography, evidence panels and responsive navigation using existing static components. |

The reference's global font sizing, body width/padding, article/paragraph/list widths, heading/anchor styles, image defaults, negative-margin notes, full-width classes and checkbox rules conflict with CO5177's `.container`, `.project-layout`, paragraph measure, table/figure wrappers, responsive controls, and theme/print overrides. Its font URLs also assume its own directory tree. Within CO5177, resolve `th, td` nowrap versus prose cells, `.project-hero h1` specificity, report-specific table widths, `:is(.image-report, .text-report)` scoping and Tabular inline overrides. Add shared dashboard shell hooks incrementally and preserve existing report-specific selectors until parity is established. Keep legacy report selectors through the pilot, then migrate and retire them after parity. Collapse the old inner report/sidebar grid as each TOC migrates. Review desktop, mobile and print overrides for the single dashboard shell. Place print overrides last and verify the card link's overlay does not obscure focus or other actions.

## 12. File-by-file changes and phased implementation

Run future checks from `CO5177/` after approval. Preview locally with `python -B -m http.server 8000`. Regenerate shared blocks with `python -B scripts/build_site.py` when partials change, then run `python -B scripts/build_site.py --check` and syntax-check the JavaScript if present. Use `git diff --check` in the approved repository context.

| Phase | Exact files and dependencies | Expected outcome, risk, and acceptance gate |
| --- | --- | --- |
| 1. Foundations | Checkpoints 1A, 1B and 1C below. | Ship and review each checkpoint independently before proceeding. |
| 2. Tabular pilot | `pages/projects/tabular.html`, `pages/assets/site.css`. Depends on 1C. | Apply dashboard report panels only. Verify all 15 figures, 14 tables, fragments and six exports. TOC integration is already handled in 1B. |
| 3. Pilot validation | Review Phase 1 and 2 changes. | Check visual and Vietnamese content parity, keyboard, no-JS, themes and print. |
| 4. Report rollout | `pages/projects/text.html`, `pages/projects/image.html`, `pages/assets/site.css`. Depends on pilot gate. | Same dashboard conventions with per-table sizing and centered figures sized by detail and intrinsic dimensions. Check all paper sections and report counts, downloads, labels and anchors before removing legacy CSS. |
| 5. Homepage refinement | `index.html`, `pages/assets/site.css`, and header/footer partials only if shared markup needs adjustment. Regenerate all four shared blocks if a partial changes. | Dashboard overview, premium project cards and team/notice panels. Compare static Vietnamese presentation, all three SVGs, team cells, states and links. |
| 6. Regression and deployment readiness | Audit four pages, `pages/assets/site.css`, any Phase 1B script, `scripts/build_site.py`, `.github/workflows/pages.yml`, `.nojekyll` and referenced assets. | Pass build/syntax/content checks, repository-prefix and direct-file tests. Inspect local payload paths and sizes. Publishing requires separate authorization. |

### Phase 1 checkpoints

| Checkpoint | Changes and dependencies | Verification and stop condition |
| --- | --- | --- |
| 1A. Shell and Vietnamese-only cleanup | `index.html`, all three `pages/projects/*.html`, `pages/partials/header.html`, `pages/partials/footer.html` for obsolete bindings, `pages/assets/site.css`, obsolete `pages/assets/site.js` and `scripts/build_site.py`. Use a 248 px desktop sidebar and in-flow small-screen navigation. | Compare pre/post content, TOCs and links, build/check, verify static route state, logo and print rules. Run visual checks when available. Leave the report layouts and TOCs in place. Stop here in this execution. |
| 1B. Mobile and TOC integration | Four page shells, shared header/CSS and a small vanilla drawer controller. Depends on approved 1A. | Move existing TOCs outside generated blocks into the sidebar. Verify no duplicates, fallback, focus, Escape/backdrop, history and breakpoint transitions. |
| 1C. Foundation validation | Review all Phase 1 files and original assets. Depends on approved 1B. | Full visual and responsive review, keyboard, Vietnamese metadata, no-JS, themes, print, build, content and deployment paths before Phase 2. |

Use exact repo-relative routes and controlled template placeholders in the renderer to emit one active primary route per page. Preserve `{{root}}`/`{{assets}}`, marker pairs, `--check` and the workflow. Verify root, repo-prefix and direct-file paths. Run syntax checks for any retained/new JavaScript. Preserve images, notebooks, metrics, models and exports.

### Phase 3 handoff to Phase 4

- Use the Tabular panel hierarchy, reviewed Vietnamese serif headings, and centered figure and caption units as presentation references. Set widths for each report's evidence. Keep dense figures wider where warranted, and stack figure pairs in their original order on small screens and in print.
- Check that a keyboard-activated skip link transfers focus to the main landmark and that the next Tab enters the main content, including with JavaScript disabled. Tabular uses `tabindex="-1"` on `#main` for this.
- Retain the named, focusable table scroll regions and visible focus indicators on narrow screens. In print, allow tables to wrap within the page and keep each caption attached to its figure. Check the generated PDF as well as the browser print layout.
- Four existing Tabular references under `Saved_models/` resolve locally but point to files excluded from the tracked checkout. Track deployment verification separately from the report presentation rollout.

### Phase 4 rollout decisions

- Use the Image panel as the shared resource convention. Title it “Tài liệu bài tập” and list Notebook, PDF report, and YouTube in that order. Keep the report-specific notebook description, group Colab and local download actions together, and only show a download when the corresponding `.ipynb` exists in `pages/notebooks/`. Show a pending status for PDF and YouTube until their URLs are verified.
- Tabular now uses the [approved Colab URL](https://colab.research.google.com/drive/1reO265UJqaPSxTSr7VqSmSk0Sc14C2Yo?usp=sharing) and links to its tracked local notebook. PDF report and YouTube remain pending. Keep the current Text and Image Colab links.

Text and Image share the approved Tabular panel, caption, and print styles. Each report keeps its existing evidence order, table widths, and resource states. Class-distribution charts use the standard centered measure. Dense Text comparisons and confusion matrices and Image grids, learning curves, and confusion matrices use the wider centered measure. Each figure keeps its original dimensions and remains linked to the source asset. Numeric columns use end alignment with the original table headers and values, and the main landmark receives skip-link focus without adding a tab stop.

### Phase 5 homepage refinement and validation

The homepage hero uses the approved English heading with a language marker for assistive technology. The responsive serif quote sits directly on the page background, with the attribution immediately beneath it:

> “The greatest value of a picture is when it forces us to notice what we never expected to see.”
>
> — John Tukey

The approved hero refinement removes the Vietnamese translation. A compact bordered panel below the attribution contains the course description and semester. The separate **Khám phá các bài tập lớn** button keeps its `#projects` destination and uses a text-only label. The existing course-information panel stays to the right when space allows and stacks below the hero on narrow screens. The homepage uses the approved dashboard tokens for project cards, the team panel, and the completion notice. Team table text can wrap on narrow screens, and the skip link focuses the main landmark. Existing course details, statuses, three project icons and links, member cells, and completion copy were preserved.

Build, navigation script syntax, whitespace, and local link and fragment checks passed. Chromium verified the homepage at 320, 375, 720, 768, 1024, and 1440 px in both themes. The skip link, project CTA, drawer keyboard focus, no-JS navigation, whole-card link targets, accessible quote heading, and tagged A4 output with the member table passed. Cross-browser and screen-reader testing and page-by-page PDF review remain open.

The three project links are presented as an academic book collection in navy, slate-blue, and muted teal. CSS provides a 5.5-degree perspective, a shaded spine, and a 15 px paper edge. The covers retain the original project titles, descriptions, SVGs and destinations. Statuses sit beneath the covers and are associated with the full-surface links via `aria-describedby`. Tabular's label and completion note reflect its report and tracked notebook download, with PDF and video still pending. Public access to the Colab notebook remains unverified. Each book keeps its visible keyboard focus outline. The hover lift requires a hover-capable device and no reduced-motion preference. On wide screens align the covers and status rows, and stack the books in their original order at narrow widths. Print uses flat covers with their status labels below.

Book collection validation passed in Chromium at seven widths from 320 to 1440 px in both themes. Wide-screen cover heights match, and the status labels sit outside the covers at every tested width. The cover and paper edge resolve to the same link, keyboard order remains Tabular, Text, and Image, and the layout works without JavaScript. The accessibility tree exposes the linked Tabular description, reduced-motion mode suppresses the hover lift, and cover text contrast is at least 6.5:1. The homepage matched its pre-refinement content after accounting for the wrappers, status associations, and approved Tabular status edits. All three report HTML files matched their original hashes.

## 13. Licensing, attribution, and deployment compatibility

- **Tufte CSS code.** The local README and LICENSE identify MIT. If substantial code is reused, preserve its copyright and permission notice. The recommended CSS is independently authored from the design ideas.
- **ET Book.** The local font tree has no separate license notice located in this review. Confirm exact redistribution terms and provenance before bundling any face. The theme's code license is insufficient evidence for every asset. Verify the actual build and license notice of any approved fallback font.
- **Academic Project.** README and footer identify CC BY-SA 4.0 and request a backlink when borrowing source. Its structured-data license is template paper metadata. Before direct reuse, confirm scope, attribution, license link, changes notice and share-alike for any distributed adaptation. Verify third-party code, fonts and media separately. This plan uses design inspiration with zero imported assets or source.
- **CO5177 assets.** Retain the approved institutional mark in the existing site and preserve research credits and asset links. Verify rights separately for new redistribution contexts.
- **Deployment.** Preserve relative paths, offline/direct-file render and the existing Pages artifact structure. The pilot adds zero font bytes and network dependencies. Any approved local WOFF2 would live under `pages/assets/` with CSS-relative URLs and matching notice. Report its compressed footprint. Confirm which saved artifacts ship from a tracked checkout before proposing any payload policy change.

## 14. Verification and measurable acceptance criteria

1. Compare complete semantic manifests against current HTML and rendered Vietnamese and no-JS states. Require zero missing or changed academic text, sequence, values, formulas, code, captions, links or assets. Record shell wrapping, TOC relocation, approved branding metadata and added dashboard navigation as explicit structural differences.
2. Match all Section 2 figure, caption, table, row and header/data cell counts. Preserve every legacy anchor and count the new primary shortcuts separately. Compare alt strings, caption association, dimensions, image hints, URL/target/rel/download attrs and artifact hashes. Only the logo's approved accessibility metadata may change. Keep all local targets and fragment links valid.
3. Review 320, 375, 768, 1024 and 1440 px, both themes, and 200% zoom. Require no document-wide horizontal scrolling or clipped controls/figures/captions. Wide table scrolling stays local. Inspect regular, italic and bold Vietnamese stacked accents.
4. Keyboard-test skip, sidebar, TOC and, starting in 1B, the drawer, resource links, scroll regions, original-figure links and footer. Require one current primary route per page, one TOC per report, no duplicate IDs and a usable no-JS sidebar. Starting in 1B, verify drawer dismissal, anchor focus, focus return and resizing while open. Require visible and unobscured focus, understandable names, valid TOC fragments and working browser history. Verify absence of translation controls, bindings and language storage. Target 4.5:1 for normal text and 3:1 for large text and essential UI boundaries. Verify reduced-motion behavior.
5. Check A4 and Letter print and landscape for wide tables. Require logo, all academic evidence and captions, intact cells and legible results. No scroll clipping or missing evidence.
6. Require a green shared layout check and syntax check of any retained/new JS, image byte parity, and parity of root, repo-prefix and direct-file relative paths. Confirm the same artifact layout locally without publishing. No new runtime dependencies.

## 15. Dashboard-specific design acceptance and unresolved decisions

- The site must visibly read as a **premium academic dashboard**, not a magazine, paper or SaaS marketing landing page. Use clean cards/panels with disciplined spacing, restrained shadows, navy sidebar and subtle blue accents.
- **No fabricated metrics or visualizations.** Homepage uses only existing content and verified project statuses; the generated mockup is inspiration for composition only and is not a source of facts, university imagery, project screenshots or new resource links.
- The sidebar must be consistent across four pages; starting in 1B on reports, the nested TOC must contain all original section links, be usable with keyboard and on mobile, and not consume a second permanent column.
- Existing `bk.png` is mandatory in the sidebar on all four pages **and in print header**. No recreated logo or substitution from the illustrative mockups.
- Produce before/after screenshots at desktop and mobile sizes during implementation; compare visual hierarchy, navigation clarity, legibility of dense scientific tables/figures, and both color schemes.
- The Phase 1B mobile drawer needs a small JavaScript enhancement after approval. The in-flow no-JS navigation is the required fallback.
- Keep the 6-phase rollout. The pilot cannot be approved solely on syntax/build checks: review the actual visual result and full functional parity first.

## 16. Risks, mitigations, open decisions, and unverified assumptions

| Risk or open decision | Mitigation |
| --- | --- |
| ET Book glyph gaps, local serif variation and unverified webfont license | Use a reliable sans-serif UI stack with selective serif display headings; do not make serif prose the default. Test target platforms. Approve a licensed Vietnamese-capable bundled face separately if needed. |
| Wide scientific evidence and print fragmentation | Keep full original image links, local table scrolling and a landscape fallback. Review the densest tables and figures individually. |
| Navigation / reading order | Integrate existing TOC into the single sidebar without duplicating IDs or controls. Keep native anchors and original report content order; test drawer focus and responsive width. |
| Content states and mixed language | Preserve exact current claims and output. Review stale statuses, static/dictionary discrepancies and the local notebook action as discrete decisions. |
| Generated markup and build drift | Reproduce the prior Tabular drift, then verify route substitutions and footer parity during regeneration. Compare semantic and generated diffs separately. |
| Drawer, breakpoint and print | Verify dialog support and fallback, final breakpoint, hash-link focus, resize transitions and print when the drawer is open. |
| Deployment and runtime verification | Browser rendering, real assistive technology, print output, external resource access, Colab Run all, and published Pages are unverified. Tracked artifact membership has not been established. |

## 17. Phase 6 regression and deployment readiness

Validation completed on 2026-11-20. No site source, assets, workflow, Git index, or remote deployment changed during this phase.

| Check | Result |
| --- | --- |
| Build and source hygiene | The Python shared-layout check, JavaScript syntax check and `git diff --check` passed. Git reported existing line-ending conversion notices. The workflow packages `index.html`, `.nojekyll`, and `pages/`, with no symlinks or hardlinks found in the working candidate. |
| Content and figure parity | The three report HTML files and all 28 report image assets matched the approved checkpoints. The exact BK logo was preserved. The homepage retains its approved quote, three linked SVG books, and two-member table. Tabular's 25 displayed model metrics match the exported CSV at report precision. |
| Local links and assets | All 151 local references resolved in the worktree. Fragment targets and project-prefix URLs passed. Chromium loaded all four pages through direct files, loopback root paths and a simulated `/CO5177/` prefix. All three tracked notebook files parsed as JSON and were served by the candidate payload. |
| Responsive and visual | Chromium passed at 320, 375, 720, 768, 1024 and 1440 CSS px in both themes. The 720 px pass is a reflow proxy for a 1440 px window at 200% zoom. Mobile light and desktop dark screenshots were spot-checked on all four pages. Figures stayed proportional with captions attached. Wide tables scrolled locally. |
| Accessibility and navigation | Keyboard skip focus, first Tab inside main, drawer initial focus, Escape and backdrop focus return, resize restoration, no-JS navigation, all 21 report TOC links and native history, and keyboard scrolling of wide tables passed. Homepage book edges retained their link targets. The audit used Chromium and does not establish screen-reader or cross-engine conformance. |
| Print | Chromium generated tagged A4, Letter, and A4 landscape PDFs for all four pages. Every version retained the logo in the print layout and had the expected table-tag count of 1, 14, 9, and 5 for home, Tabular, Text, and Image. Print geometry found no table overflow or figure distortion. PDF pagination review remains a manual follow-up. |
| External links | The project repository, UCI Adult dataset and PhoBERT repository were readable. The two Kaggle dataset landing titles resolved, but their contents were unavailable to the checker. The two member profile requests and all three Colab requests were inconclusive. Public notebook access and Run all remain unverified. |

### Initial deployment blockers and proposed fixes

1. **Track the navigation script.** All four pages reference `pages/assets/navigation.js`, which is present locally but untracked. The tracked-only simulation returned 404 for it. Include it in the approved release commit so the narrow-screen drawer is available.
2. **Resolve the four broken Tabular references in the packaged site.** The candidate package returned 404 for `Saved_models/model_metadata.json`, `preprocessing_metadata.json`, `mlp_config.json`, and `README.md`. They exist locally under an ignored directory. After reviewing the four files for publication, approve an explicit allowlist or relocation into a tracked public metadata directory. Keep the binary model files excluded unless separately approved.
3. **Confirm the release commit and Pages settings.** The local branch is `Duy` and the worktree contains uncommitted changes. The workflow's automatic trigger targets `main`. Verify the approved candidate is in the intended revision, confirm GitHub Actions is the Pages publishing source and verify the `github-pages` environment. Repository setting and existing public site requests were inconclusive. [GitHub Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [custom workflow requirements](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
4. **Confirm the pre-existing Tabular notebook edit.** The working download has 53 cells, compared with 78 at HEAD, and the code-cell sequence differs. The working file is valid notebook JSON. Confirm it is the version intended for release and verify Run all and its relationship to the published results before representing it as reproduced.

The worktree-based package contained 46 tracked files totaling 15,553,859 bytes. Simulating the addition of the navigation script produced 47 files totaling 15,557,772 bytes. Copying all local files would include the ignored model directory and produce 61 files totaling 64,251,252 bytes. These are uncompressed local measurements. No Actions artifact was uploaded.

**Submission follow-up.** All three reports still show pending PDF and YouTube entries. The course requires these resources and a notebook that passes Run all. The homepage also retains the previously noted Text notebook provider mismatch. Confirm these assets, permissions and copy separately. [Course requirements](../requirements.md)

### Final readiness fixes and release gate

- Removed the four broken `Saved_models/` hyperlinks from the Tabular report. Their descriptive text remains. Restoring just the four anchor wrappers reproduced the approved Tabular HTML hash. The page still contains 15 figures and captions, 14 tables, and all six CSV and text export links.
- Audited the workflow YAML, `main` push and manual dispatch triggers, checkout behavior, hosted-runner Python availability, permissions, environment and deployment output, staging paths, and upload/deploy artifact names. The upload and deploy actions agree on the default `github-pages` name. The hosted workflow uses the existing standard-library Python renderer and raw static artifact. The upload action excludes hidden paths such as `.nojekyll` from its tar, which is expected for this custom workflow. No workflow defect was found in the local audit. [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [Pages upload action](https://github.com/actions/upload-pages-artifact/blob/v4/action.yml).
- Built a temporary checkout simulation using the working versions of Git-tracked inputs only. The renderer built successfully and passed its check. The simulated upload contained 45 files and covered 147 local references across the four pages. The only missing target was `pages/assets/navigation.js`, referenced once per page and intentionally left untracked for the user to add.
- A second temporary simulation included the unchanged navigation script. All 147 references, including links and assets resolved under the site root and `/CO5177/` prefix, passed. The archive contained 46 files with 15,557,438 bytes of uncompressed file content, three valid notebook downloads, and no saved-model files, symlinks, hardlinks, or Git LFS pointers.

The candidate passes local build and package checks once the user tracks the navigation script and includes the intended changes in the release revision. Branches and deployment strategy are unchanged. Live GitHub Actions execution and the repository's Pages configuration remain unverified. The notebook-version, Colab access and Run all, and pending PDF and video follow-ups above remain open. No commit, merge, push, deployment, or upload was performed.
