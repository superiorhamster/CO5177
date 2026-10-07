# CO5177 assignment portfolio

A static Vietnamese/English GitHub Pages portfolio for Semester 261, academic year 2026–2027. It includes a group landing page and separate Tabular, Text, and Image project pages based on [the course requirements](requirements.md).

Group **SlightSeek** has two members: Phạm Duy Anh (2310139; Text and Image) and Nguyễn Phan Tuấn Duy (2310491; Tabular and Text). The Image page includes recorded results, a [Colab notebook](https://colab.research.google.com/drive/1pHsdOVulTgBHD1ybwBt4jTmHKW_-q3rZ), and an unchanged [notebook download](pages/notebooks/intel_image_classification_trained.ipynb); Colab Run all has not been independently rechecked. The Text page summarizes the supplied sentiment-analysis notebook (four models, EDA, preprocessing, and comparison limits) with a [Kaggle notebook](https://www.kaggle.com/code/anhphmduy/sentimentanalysis) and an unchanged [notebook download](pages/notebooks/sentimentanalysis.ipynb). Text Run all has not been rechecked. Tabular content/notebook, plus PDF reports and videos for each project, are **pending**. The website is not yet a completed assignment submission; dataset requirements and suggested methods remain guidance unless supported by recorded results.

## Preview locally

No dependencies are required. The checked-in HTML already contains the shared header/footer, so it works directly. From the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. You can also open `index.html` directly. All site assets are local; no fonts, analytics, or other third-party resources are fetched. JavaScript enables the language switch; the default Vietnamese content remains readable without it.

## Update content

- Homepage: `index.html`; project pages: `pages/projects/{tabular,text,image}.html`.
- Shared appearance: `pages/assets/site.css`; translations and language behavior: `pages/assets/site.js`.
- Shared header and footer: edit `pages/partials/header.html` and `pages/partials/footer.html`, then run `python3 scripts/build_site.py`. The script updates the marked blocks in all four pages, resolving `{{root}}` to the repository root and `{{assets}}` to `pages/assets/`, using relative paths for each page. Do not edit those generated blocks directly. Run `python3 scripts/build_site.py --check` to check whether they are current. GitHub Actions runs the build automatically before publishing; the rendered layout remains available when JavaScript is disabled or HTML is opened directly.
- Replace pending group details with the registered group name and real members, MSSVs, contributions, and optional verified GitHub URLs. Keep the details consistent on all four pages. The single pending row in the homepage table is an empty-state marker; replace it with one row per actual member.
- Edit both the default Vietnamese HTML and the matching keys in the `vi` and `en` dictionaries in `site.js`. Language switching uses `textContent`, so translated elements must contain plain text. Use new keys where repeated pending values become distinct real content; do not repurpose the shared `pending` key for a specific person or dataset.
- Document official Vietnamese names as provided. Use meaningful English translations for descriptions and controls. Update each page’s title and description in its HTML and corresponding translation keys.
- Replace the language-neutral project type heading with the actual project title once selected; update both languages. Add real problem statements, dataset sources, methods, figures, metrics, and conclusions to the project sections. Clearly distinguish completed work from planned work.

The switch defaults to Vietnamese and remembers the selection in browser storage under `co5177-language`. If storage is unavailable, switching still works on the current page. Light/dark appearance follows the operating system.

## Add notebook, PDF, and video links

Each project contains three `.resource-item` blocks. Replace its non-clickable `.resource-pending` span with a real anchor, for example:

```html
<a class="text-link" href="https://github.com/superiorhamster/CO5177/blob/main/notebooks/tabular.ipynb">
  <span data-i18n="open-notebook">Mở notebook</span>
</a>
```

This is a **format example**, not an existing notebook. Add `open-notebook` to both translation dictionaries and use the actual URL. Do not add a link until the resource exists.

- Notebook: an actual GitHub `.ipynb` URL and/or Google Colab URL. Independently verify **Run all** completes in Colab.
- Report: add the real PDF under `pages/reports/`, then use `../reports/actual-filename.pdf` from a project page, or supply a publicly accessible external URL.
- Video: an actual YouTube URL, Public or Unlisted; 5–10 minutes is recommended.

Keep internal URLs relative. Leading `/` URLs bypass the repository prefix and will break assets or navigation at `/CO5177/`. Add real members’ GitHub links only when provided; no placeholder profile URLs.

## Publish on GitHub Pages

1. In [repository Pages settings](https://github.com/superiorhamster/CO5177/settings/pages), select **GitHub Actions** under **Build and deployment → Source**.
2. Push the site and `.github/workflows/pages.yml` to `main`. The workflow also supports a manual run from the Actions tab.
3. Confirm **Deploy assignment portfolio** succeeds and use the `github-pages` environment URL. The expected project-site address is `https://superiorhamster.github.io/CO5177/`; treat it as live only after checking the deployment.

The workflow packages **root `index.html`, `.nojekyll`, and `pages/`** into a temporary website directory, with `index.html` at the artifact root. The requirements document, README, repository internals, and future notebooks outside `pages/` are not included in the website artifact. GitHub Pages settings must be enabled before the first workflow run. See [GitHub’s custom workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Before submitting

- Check all four pages at mobile and desktop widths, in both languages and color schemes. Check keyboard focus, navigation, and language persistence across pages.
- Verify all actual links, including YouTube access and PDF downloads. Confirm notebooks run successfully in Colab.
- Confirm group information matches `GroupRegistration`; add the verified landing-page URL to `GroupLink` before the LMS registration deadline.
- Add a notebook, separate PDF report, and video for **each** project. Conclusions and chart captions must agree with the actual report metrics.
- Submit the combined `<groupname>-report.pdf` to LMS. It does not replace the landing page or each project’s resources. No submission date is assumed; follow the lecturer’s LMS announcements.
