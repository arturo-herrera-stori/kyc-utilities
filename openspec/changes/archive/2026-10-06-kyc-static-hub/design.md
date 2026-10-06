# Design

## Context

See `proposal.md` (Why). The repo hosts self-contained static HTML utilities. The first utility is the Log Group Atlas (formerly a standalone HTML file). Publishing targets GitHub Pages on `arturo-herrera-stori/kyc-utilities`.

## Goals / Non-Goals

**Goals:**

- Catalog-driven hub (`data/utilities.json` + client-side render).
- One folder per utility under `utilities/<slug>/`.
- Pages deploy via Actions with a minimal `_site` artifact (no `.cursor`, `openspec`, or workflows in the public bundle).
- CI script (`scripts/validate_catalog.py`) enforcing catalog ↔ filesystem alignment.

**Non-Goals:**

- Server-side rendering, auth, or dynamic backends.
- Validating external links (e.g., AWS console URLs).
- Shared CSS across all utilities (utilities may remain self-contained).

## Decisions

1. **JSON catalog + lightweight JS hub**  
   - *Why:* Adding a utility is one JSON object plus a folder; no build step required.  
   - *Alternative:* Hand-edited HTML cards — rejected for poor scalability.

2. **Slug equals catalog `id`**  
   - *Why:* Validator and humans can spot mismatches; paths are predictable.  
   - *Alternative:* Decouple id from folder name — rejected as error-prone.

3. **`_site` staging in Pages workflow**  
   - *Why:* Avoid exposing repo metadata paths on the public site.  
   - *Alternative:* Publish entire repo root — rejected.

4. **Python validator in CI**  
   - *Why:* Readable rules, no extra npm deps, Python 3 available on `ubuntu-latest`.  
   - *Alternative:* Shell + `jq` — acceptable but harder to extend.

## Risks / Trade-offs

- **[Risk] Hub requires HTTP for local preview** → Document `python3 -m http.server` in README; GitHub Pages is the primary target.
- **[Risk] New category needs validator update** → Document in README; extend `ALLOWED_CATEGORIES` when adding categories.
- **[Risk] Catalog and atlas content drift** → Atlas updates are manual; hub only links and describes utilities.

## Migration Plan

1. Land hub structure and move atlas to `utilities/log-group-atlas/index.html`.
2. Enable GitHub Pages source: GitHub Actions.
3. Verify hub and atlas URLs after first deploy.

Rollback: revert `main`; Pages republishes previous artifact.
