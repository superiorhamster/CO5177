# Project handoff — CO5177 / SlightSeek

## Session Metadata

- Updated: 2026-11-05, Asia/Ho_Chi_Minh.
- Project: `/home/anhpd/Project/Group/LapTrinhAIDS/Assignment`.
- Branch: main; HEAD: 69c1f2e (finished 90% of nlp and cv, leftover: pdf and video link).
- Requested filename is AGENT.md. Read it explicitly when resuming; automatic discovery of this singular filename is not assumed.

## Current State Summary

A static Vietnamese/English GitHub Pages assignment portfolio for semester 261, academic year 2026–2027. Text and Image summarize recorded notebook results and provide online notebooks plus downloads. Tabular remains a scaffold. Separate PDF reports, YouTube videos, the combined LMS report, and independent Colab Run all checks remain pending or unverified. The commit's “90%” description is historical, not a verified completion measure.

This session reviewed six prior chats in this project (including its former Notebook subfolder), recent related parent/CV chat messages, and current source files. Active local Codex history was paginated to exhaustion; archived Codex history was empty. All six direct project chats returned no further turn cursor. The two long parent/CV chats were reviewed only for their recent ten turns. External ChatGPT history was not searched.

## Important Context

- Group: **SlightSeek**. Phạm Duy Anh, MSSV 2310139: Text and Image. Nguyễn Phan Tuấn Duy, MSSV 2310491: Tabular and Text. User supplied these details.
- Repository: https://github.com/superiorhamster/CO5177 . Expected site: https://superiorhamster.github.io/CO5177/ . Current deployment/public access was not checked.
- `requirements.md` is the checked-in course brief, not a Python dependency file. Two-person groups need Tabular, Text and one additional modality; this project chose Image.
- Historical face-mask/YOLO, garbage and football-player experiments are superseded. Current Image work uses Intel scenes, MobileNetV3-Small and ViT-B/16.
- Preserve the distinction between saved outputs and independently reproduced results. This session did not train or execute notebooks.
- Missing resources stay visibly pending. Do not invent metrics, reports, videos, personal profile links or deadlines.
- Pre-existing untracked `HCMUT_RP_template/` is user work. Its SoftEng_252 LaTeX template is not evidence of a completed CO5177 report. Leave it intact unless the next task specifically concerns it.

## Architecture Overview

Plain static HTML with local CSS and minimal JavaScript; no frontend packages, backend or database. Root index.html links to three pages under pages/projects/. Essential Vietnamese content is embedded in HTML and works without JavaScript. The language switch uses VI/EN dictionaries and translated alt text, defaults to Vietnamese, and stores the selection under co5177-language when storage is available. Color scheme follows the OS.

Shared partials are rendered into marked header/footer blocks on all four pages. Relative URLs support local files and the /CO5177/ Pages prefix. GitHub Actions builds partials and publishes only root index.html, .nojekyll and pages/. Source notebooks outside pages/ are excluded from the deployed artifact.

## Critical Files

| File | Purpose |
|---|---|
| `requirements.md` | Course brief and submission rubric |
| `README.md` | Preview, content editing and deployment instructions |
| `index.html` | Homepage, course/group information and project links |
| `pages/projects/tabular.html` | Pending Tabular content |
| `pages/projects/text.html` | VLSP sentiment report and limitations |
| `pages/projects/image.html` | Intel scene report, EDA and results |
| `pages/assets/site.css` | Shared and scoped responsive styles |
| `pages/assets/site.js` | Language behavior, VI/EN dictionaries and alt text |
| `pages/partials/header.html` | Shared header source |
| `pages/partials/footer.html` | Shared footer source |
| `scripts/build_site.py` | Render/check shared blocks |
| `.github/workflows/pages.yml` | Deployment configuration |
| `.impeccable/config.json` | Existing scoped detector exceptions |
| `ipynb/image/intel_image_classification_trained.ipynb` | Image notebook with saved outputs |
| `ipynb/text/sentimentanalysis.ipynb` | Text notebook with saved outputs |
| `ipynb/image/phan_tich_intel_image_classification.md` | Earlier code analysis; describes an older notebook version |
| `pages/notebooks/intel_image_classification_trained.ipynb` | Published Image download |
| `pages/notebooks/sentimentanalysis.ipynb` | Published Text download |
| `HCMUT_RP_template/SoftEng_252/main.tex` | Pre-existing untracked report template |

## Recorded Results

### Image

Kaggle dataset: puneet6060/intel-image-classification. Six classes: buildings, forest, glacier, mountain, sea, street. Original labeled total 17,034; cleaned total 17,006. Additional 7,301 prediction images were excluded. Removed 28 training images: 20 with conflicting labels, three test duplicates and five same-label duplicates. Exact pixel hashes do not cover all near duplicates.

Split: 11,204 train / 2,802 validation / 3,000 test, stratified validation with seed 42. Native median resolution 150×150; input 3×224×224 with ImageNet normalization. Three classifier epochs, then at most 15 full-backbone fine-tuning epochs. Validation macro-F1 selects the checkpoint; ties favor classifier; test follows selection.

| Model | Head val macro-F1 | Fine-tuned val macro-F1 | Selected FT epoch | Test accuracy | Test macro-F1 |
|---|---:|---:|---:|---:|---:|
| MobileNetV3-Small | 0.9283 | 0.9350 | 9 | 92.43% | 0.9260 |
| ViT-B/16 | 0.9339 | 0.9500 | 7 | 94.50% | 0.9463 |

Largest directional error: glacier → mountain, 58/553 for MobileNet and 51/553 for ViT. Single seed, unequal training budgets, near duplicates and crop sensitivity limit conclusions.

Online notebook: https://colab.research.google.com/drive/1pHsdOVulTgBHD1ybwBt4jTmHKW_-q3rZ . Access and Run all need rechecking.

Related sibling CV history records the user's preference to keep num_workers=2, iterator cleanup fixes, a Kaggle source migration, and switching MobileNetV3-Large to Small for speed. These concerned the sibling development notebook; inspect the actual target before applying them. Large/Small checkpoints are incompatible.

### Text

VLSP sentiment: 6,150 Vietnamese texts, 5,100 development + 1,050 test, three classes with 350 test examples each. Online notebook: https://colab.research.google.com/drive/1-S6XINpCzaYGDXTabWobxC6r2z0zODYf#scrollTo=Q3zSk1isaVGM . Dataset: https://www.kaggle.com/datasets/anhphmduy/vlsp-sentiment-dataset . Dataset version, original collection provenance and license are unconfirmed in the notebook.

| Model | Test accuracy | Test macro-F1 |
|---|---:|---:|
| PhoBERT-large | 74.00% | 0.7382 |
| TextCNN | 68.57% | 0.6844 |
| CNN+BiLSTM | 65.05% | 0.6468 |
| BiLSTM | 62.86% | 0.6256 |

Comparison is not controlled: different PhoBERT augmentation/validation and no manifest confirming identical test membership. Word2Vec models do not restore best checkpoints; PhoBERT reload logs contain LayerNorm key warnings. Validate restored weights/predictions. Potential shared embedding storage across Word2Vec runs is an inference from code, not a confirmed runtime finding. Padding is not masked in BiLSTM mean pooling, embedding lacks padding_idx, and that branch's random_split is unseeded. No saved confusion matrix or misclassified-sentence list supports a detailed error diagnosis.

## Decisions Made

- Keep the restrained academic static UI and bilingual content. Historical Tailwind/Lucide/wallpaper/Chart.js implementations were replaced; old paths and theme controls are not current architecture.
- Edit shared partial sources and run the build; do not hand-edit generated header/footer blocks.
- Update default Vietnamese HTML and matching VI/EN keys together. Translation uses textContent, so translated elements must contain plain text. Use dedicated keys instead of repurposing shared pending values.
- Use relative internal URLs. Published notebook downloads and figures belong inside pages/.
- Preserve original notebook figures and distinguish recorded evidence from new experiments.
- Existing design-detector exceptions reflect earlier scope decisions, including inherited small homepage/header/footer text. They are not blanket permission to ignore new UI issues.
- Member-table GitHub links intentionally use the group repository because personal profile URLs were not supplied. Do not describe them as verified personal profiles.

## Work Completed

Reviewed project chats and current files, checked shared layout and JavaScript syntax, and compared source/download notebook bytes. Image copies match (78 cells); Text copies match (50 cells). Created this handoff. No notebook training, publishing, committing or report authoring was performed.

## Files Modified

Only AGENT.md was added for this request. The skill scaffold was moved to this root filename. The existing untracked report-template folder was left untouched.

## Pending Work

- Tabular dataset, notebook and actual page content. Required minimum: 2,000 samples, 10 columns, missing values, categorical and numerical columns.
- Separate PDF report and Public/Unlisted YouTube video for every project; recommended video duration 5–10 minutes.
- Independent Run all in Colab, including inputs, dependencies and checkpoint restoration. A Kaggle link alone does not establish Colab compliance.
- Combined SlightSeek-report.pdf for LMS; verify GroupRegistration and put the verified landing-page URL in GroupLink. Follow LMS deadlines; none is established here.
- Confirm public accessibility of Pages and all submission resources.

## Immediate Next Steps

1. Read this file and inspect git status before editing. Preserve the untracked template. If the next request does not identify a deliverable, clarify what to continue.
2. For submission completion, identify missing Tabular inputs and available PDF/video materials. Do not infer the template is a finished report.
3. For reproduction, inspect actual notebook inputs and the limitations above. Record changed results explicitly when rerunning experiments.
4. Update both languages for content changes, rebuild partials where needed, and run the checks below. Check responsive/no-JS behavior when editing layout or language logic.

## Environment State and Validation

From the repository root:

```sh
python3 -m http.server 8000
python3 scripts/build_site.py --check
node --check pages/assets/site.js
git diff --check
```

Preview: http://localhost:8000/ . To refresh shared blocks, run python3 scripts/build_site.py, then its --check mode. Website preview needs no dependency installation.

This session passed shared-layout and JavaScript syntax checks and verified notebook-copy equality without executing cells. Earlier chats reported browser checks in both languages, desktop/mobile, themes and no-JS mode; those are historical, not fresh visual verification. Public deployment and Run all were not checked. No background server or training process was started.

The workflow runs on main for changes to index, .nojekyll, pages/, the build script or workflow, and supports workflow_dispatch. A handoff-only commit does not trigger its path filters. Pages settings must select GitHub Actions. This session did not publish.

## Assumptions Made

Current source and trained notebook outputs take precedence over old chat paths/plans. No new implementation task was selected in this session; pending items are project needs, not an instruction to perform all of them immediately. The report template's intended use is unconfirmed.

## Potential Gotchas

- README contains generic advice about pending group rows, although real group data is already filled. Inspect actual HTML before following it literally.
- Earlier image-analysis Markdown describes an output-cleared version and references sibling development files; use the trained notebook for metric claims.
- Notebook source and website copies may drift after edits. Synchronize deliberately, preserving historical evidence where needed.
- Old chats mention root image.html, docs/, Notebook/, old chart assets, YOLO and MobileNetV3-Large. These are historical, not current paths/configuration.
- No credentials are required for static preview. Do not copy credentials into this handoff.

## Related Resources: Reviewed Chat History

Exact titles and local thread IDs support retrieval. The first six are direct project chats; the last three are related parent/CV chats.

| Chat title | Thread ID | Outcome |
|---|---|---|
| Parse face mask annotations | 01a0e5ca-68ea-7fb0-ab5a-d97096682750 | Historical EDA/YOLO notebooks in former Notebook subfolder |
| Create project overview page | 01a0e6e7-f360-7313-ae74-4d7403354678 | Historical face-mask report |
| Đồng bộ và tối giản UI | 01a0fd7b-e3c6-7492-b9e1-9c0b147a7000 | Restrained consistent academic UI preference |
| Implement GitHub page requirements | 01a10f30-8303-7e62-a4e0-5ed71bf06017 | Current bilingual portfolio foundation and Intel report |
| Đẩy index.html cho GitHub Pages | 01a10f99-0a69-79d3-a027-a5262e10a34d | Root index migration and deployment fixes |
| Cập nhật EDA và tiền xử lý | 01a10ffd-7719-74f3-84c1-0caa25fe47e4 | Image EDA/preprocessing, team details, Text report, notebook links/downloads, group-repo links |
| Build image training pipeline | 01a0f1cd-5bd7-7313-a99f-b638930df4f0 | Sibling CV development, Kaggle source, Small model, two-worker fixes; recent ten turns |
| Inspect garbage classification | 01a0b452-2044-7b10-8c2f-8c65ffc49ab8 | Parent-folder experiments later switched to football players; recent ten turns |
| Clarify task request | 01a0b44f-0fc4-7ce0-a1ec-233ec678e76a | Parent-folder dataset link, no substantive implementation outcome |

Resolve conflicts by inspecting current files and retrieving the relevant messages, rather than assuming an old agent conclusion remains verified.
