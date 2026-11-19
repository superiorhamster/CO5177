# CO5177 UI development report

The redesign adapted the original static course portfolio into a Vietnamese academic dashboard. Tabular served as the design pilot, Text and Image reused the validated report patterns, and homepage work followed. The site retained the original research narrative, figures, tables, and report order. This retrospective summarizes the approved decisions and recorded checks. The [implementation plan](TUFTE_UI_IMPLEMENTATION_PLAN.md) contains the detailed phase record.

## Architecture and design decisions

| Area | Result |
| --- | --- |
| Delivery | Four physical HTML routes use shared CSS and one vanilla navigation script. No runtime font downloads or frontend framework were introduced. |
| Shared layout | [build_site.py](../scripts/build_site.py) embeds the header and footer from [pages/partials/](../pages/partials/) into marker pairs. It resolves relative paths and sets the active page in the generated HTML. Individual report TOCs live outside the generated blocks. |
| Language and typography | The site now uses static Vietnamese UI labels and retains English technical names and the English homepage quotation. The old VI/EN dictionary and storage logic were removed. Windows Chromium reproduced malformed heading accents when Georgia lacked Vietnamese glyphs and fell back within a word. The heading stack now starts with Times New Roman and uses normal letter spacing. |
| Sidebar | The persistent sidebar becomes a native modal drawer below the 80 rem desktop breakpoint when JavaScript initializes. A shared static navigation subtree supports both modes and stays in flow without JavaScript. The drawer manages keyboard focus, closing, and report-anchor navigation. |
| Report evidence | Tabular established the bordered panels and measured prose. Figures and captions are centered together. Dense charts may use a wider measure, and original-image links remain available. Semantic tables retain their structure and use local horizontal scrolling when necessary. |
| Homepage | The John Tukey quotation and attribution sit on the page background. Course summary and semester sit in a compact panel beside the existing course information on wide screens. The three project links use CSS book covers with reduced-motion support and resource statuses beneath them. |
| Print and deployment | Print restores the BK brand, removes interactive chrome, and allows wide cells to wrap. [The Pages workflow](../.github/workflows/pages.yml) builds from the checkout, stages the static site and uploads a Pages artifact. Relative paths support direct-file preview and a project-site prefix. |

## Phase outcomes

| Phase | Approved outcome |
| --- | --- |
| 1A–1C | Established the shared navy sidebar and dashboard shell, converted the site to static Vietnamese, integrated report TOCs into the mobile drawer, and validated the common layout. The foundation pass fixed the Vietnamese serif fallback, sidebar scroll styling, and oversized print table constraints. |
| 2 | Reworked Tabular into the pilot report with a clear resource panel, ordered analysis panels, numeric alignment, and centered figures. The pilot kept 15 figures and captions, 14 tables, and the existing academic text and results. |
| 3 | Validated the pilot and fixed skip-link focus by making the main landmark focusable without adding a tab stop. Recorded the evidence, keyboard, and print patterns for the other reports. |
| 4 | Rolled the report design out to Text and Image while retaining their distinct evidence widths and resource links. Standardized the three-row Notebook/PDF/YouTube panel in Tabular, added its tracked notebook download, and used the approved Colab URL. |
| 5 | Refined the homepage hero, course and team panels, and CSS academic book collection. The final hero retains the English quotation and attribution. The final books display status information beneath their covers. Tabular's status now reflects the report and local notebook download, with PDF and video pending. |
| 6 | Audited all four pages and simulated the Pages payload. Removed four hyperlinks to ignored saved-model metadata while retaining the explanatory text. The workflow audit found no defect requiring a change. |

## Verification record

### Recorded during development

- The last Phase 6 candidate resolved all 147 local references after the navigation script was included in the simulated release archive. It contained three notebook downloads and no files from `Saved_models/`.
- Exact comparisons preserved all 28 report image assets and the three report bodies apart from approved content and markup changes. Tabular's displayed 25 comparison metrics agreed with the exported CSV at report precision.
- Chromium passed direct-file, loopback-root, and simulated project-prefix checks. The responsive review covered six widths from 320 to 1440 CSS px in both themes, including a 720 px reflow proxy for a 1440 px viewport at 200% zoom. Keyboard skip focus, drawer dismissal and focus return, all 21 report TOC links, local table scrolling, and the no-JavaScript fallback passed in the recorded run.
- Chromium generated tagged A4, Letter, and A4 landscape PDFs. The four pages had 1, 14, 9, and 5 table tags for Home, Tabular, Text, and Image. Print layout checks found no table overflow or figure distortion. These checks did not include a page-by-page review of the generated PDFs.

### Verified in the documentation checkout

- The [navigation script](../pages/assets/navigation.js) is now tracked. Its earlier absence from a tracked-only simulation is historical.
- The three notebook downloads are tracked and match their corresponding source notebook bytes under `ipynb/` in this checkout. This comparison does not verify access to the Colab copies, their execution, or scientific reproducibility.
- The four pages retain the expected figure and table counts, and all 147 local references resolve to tracked files. The documented loopback preview served all four pages. The shared-layout build and check, JavaScript syntax check, and whitespace check passed against current source.

## Remaining limitations

- Live Pages configuration, GitHub Actions execution for the intended release revision, and public deployment were not verified here. The workflow targets matching changes on `main` and supports manual dispatch.
- Public Colab sharing and **Run all** still need independent verification. PDF and YouTube links remain pending for each report. The homepage completion note still labels the Text notebook as Kaggle while the Text resource panel points to Colab. [Course requirements](../requirements.md)
- Cross-browser and screen-reader coverage, page-by-page PDF review, and the validation of external resources beyond those verified in the Phase 6 record remain open.
- The [original frontend analysis](FRONTEND_ANALYSIS.md) and [legacy handoff](../AGENT.md) describe earlier states, including the old bilingual interface and incomplete Tabular report. Use the [content editing guide](CONTENT_EDITING_GUIDE.md) for current maintenance instructions.
