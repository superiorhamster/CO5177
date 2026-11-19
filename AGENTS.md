# CO5177 agent instructions

- Start with the [README](README.md) and [content editing guide](docs/CONTENT_EDITING_GUIDE.md). Use the [development report](docs/UI_DEVELOPMENT_REPORT.md) and [implementation plan](docs/TUFTE_UI_IMPLEMENTATION_PLAN.md) for decision history. [AGENT.md](AGENT.md) is an older handoff.
- Inspect `git status --short` and the affected source before editing. Preserve unrelated work. Keep changes within the requested scope.
- Maintain the static Vietnamese UI and the existing accessibility and print behavior. Preserve academic claims, numerical results, captions, anchors, and resource statuses unless the user authorizes the specific change.
- Edit reports in `pages/projects/` and the homepage in `index.html`. Edit shared header/footer markup in `pages/partials/` and run `python -B scripts/build_site.py`. Preserve both marker pairs on each page and keep report TOCs outside the generated blocks.
- Use relative site URLs. Check that new assets under `pages/` are tracked for release. Keep ignored `Saved_models/` files out of published links and artifacts. Preserve the exact BK logo and the no-JavaScript navigation fallback.
- Before handing back work, run `python -B scripts/build_site.py --check`, `node --check pages/assets/navigation.js`, and `git diff --check`. Check affected links, anchors and rendered behavior. State which checks ran and which remain open.
- Treat saved notebook outputs as recorded evidence. Verify resource access and Colab **Run all** independently before claiming either works. Keep PDF and video placeholders until their actual URLs are verified.
- Branch changes, commits, pushes, merges and deployment require explicit authorization.
