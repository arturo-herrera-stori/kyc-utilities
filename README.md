# KYC Utilities Hub

Central hub for **static** KYC engineering utilities, published with [GitHub Pages](https://arturo-herrera-stori.github.io/kyc-utilities/).

## Live site

- **Hub:** https://arturo-herrera-stori.github.io/kyc-utilities/
- **Log Group Atlas:** https://arturo-herrera-stori.github.io/kyc-utilities/utilities/log-group-atlas/

After the first deploy, enable **Settings → Pages → Build and deployment → Source: GitHub Actions** if it is not already selected.

## Add a utility

1. Create `utilities/<slug>/index.html` (self-contained static page or small site).
2. Add an entry to `data/utilities.json`:

```json
{
  "id": "my-utility",
  "title": "Human title",
  "summary": "One line for the hub card.",
  "category": "observability",
  "path": "utilities/my-utility/",
  "status": "stable",
  "updated": "YYYY-MM-DD"
}
```

3. Merge to `main` — the Pages workflow redeploys automatically.

**Categories:** `observability`, `reference`, `runbooks`, `tools`, `onboarding` (extend the list in `scripts/validate_catalog.py` if you add a new one).

**Slugs:** use `kebab-case`. The catalog `id` must match the folder name (`utilities/<id>/index.html`).

**CI:** the [Validate catalog](.github/workflows/validate-catalog.yml) workflow runs on pushes and PRs to `main`. It checks JSON shape, unique ids, paths, `index.html` files, and orphan folders under `utilities/`. Run locally:

```bash
python3 scripts/validate_catalog.py
```

Optional: add a link back to the hub at the top of each utility (`../../` from one level under `utilities/`).

## Layout

```
index.html              Hub landing
data/utilities.json     Catalog (source of truth for cards)
assets/                 Hub CSS/JS
utilities/<slug>/       One folder per utility
```

## Local preview

Static files only — serve the repo root over HTTP (fetch needs a server, not `file://`):

```bash
python3 -m http.server 8080
# open http://localhost:8080/
```
