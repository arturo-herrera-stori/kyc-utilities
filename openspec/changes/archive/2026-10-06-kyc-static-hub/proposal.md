# Proposal

## Why

KYC engineering needs a single, stable place to publish static reference utilities (starting with the CloudWatch Log Group Atlas). Scattered HTML files and ad hoc links do not scale as more tools are added; a small hub with a clear catalog convention makes discovery and GitHub Pages publishing repeatable.

## What Changes

- Add a static **KYC Utilities Hub** landing page that lists registered utilities from a JSON catalog.
- Publish the existing **Log Group Atlas** under a stable URL slug with navigation back to the hub.
- Deploy the public site via **GitHub Pages** (GitHub Actions), shipping only site assets—not repo tooling.
- Add **CI validation** so catalog entries, folder layout, and `index.html` entry points stay aligned.
- Document how to add utilities in `README.md`.

## Capabilities

### New Capabilities

- `kyc-utilities-hub`: Static hub catalog, utility layout conventions, GitHub Pages deployment, and catalog validation.

### Modified Capabilities

- (none)

## Impact

- New top-level `index.html`, `assets/`, `data/utilities.json`, `utilities/<slug>/` layout.
- GitHub Actions: `pages.yml`, `validate-catalog.yml`.
- Public URLs under `arturo-herrera-stori.github.io/kyc-utilities/`.
- No runtime services, databases, or Hyperlane APIs.
