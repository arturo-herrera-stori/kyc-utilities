# Tasks

## 1. Hub structure and catalog

- [x] 1.1 Add hub landing (`index.html`, `assets/hub.css`, `assets/hub.js`) and verify `python3 -m http.server` serves the catalog cards from `data/utilities.json`
- [x] 1.2 Add initial catalog entry for log-group-atlas and verify filter/search updates the visible card count

## 2. Utilities and atlas migration

- [x] 2.1 Move Log Group Atlas to `utilities/log-group-atlas/index.html` and verify hub link and back link to hub resolve correctly
- [x] 2.2 Remove duplicate root-level atlas HTML and verify only the slug path remains

## 3. GitHub Pages

- [x] 3.1 Add Pages workflow building `_site` from hub assets only and verify workflow file lists `index.html`, `assets`, `data`, `utilities`
- [x] 3.2 Document live URLs and Pages setup in `README.md`

## 4. Catalog CI

- [x] 4.1 Add `scripts/validate_catalog.py` and `validate-catalog.yml` and verify `python3 scripts/validate_catalog.py` exits 0 on current repo
- [x] 4.2 Document local validation and CI behavior in `README.md`

## 5. Integration

- [x] 5.1 Push to `main` on `arturo-herrera-stori/kyc-utilities` and verify GitHub Actions runs deploy and validate workflows
