# Spec Delta

## Purpose

Central static hub for KYC engineering utilities with a machine-readable catalog, predictable URLs, GitHub Pages publishing, and CI guards against broken catalog entries.

## ADDED Requirements

### Requirement: Hub lists registered utilities

The system SHALL render a hub landing page that loads utility metadata from `data/utilities.json` and displays each entry as a navigable card grouped by category.

#### Scenario: Catalog loads successfully

- **WHEN** a visitor opens the hub root URL
- **THEN** the page fetches `data/utilities.json` and shows one card per catalog entry with title and summary

#### Scenario: Filter narrows visible utilities

- **WHEN** a visitor types text into the hub search control
- **THEN** only utilities whose title, summary, category, or id match the filter remain visible

### Requirement: Utility entry layout

Each published utility SHALL live at `utilities/<id>/index.html`, where `<id>` matches the catalog entry `id` and `path` is `utilities/<id>/`.

#### Scenario: Stable utility URL

- **WHEN** a catalog entry has `id` `log-group-atlas` and `path` `utilities/log-group-atlas/`
- **THEN** the utility is reachable at that path with `index.html` as the entry document

#### Scenario: Return navigation to hub

- **WHEN** a visitor views a utility under `utilities/`
- **THEN** the page provides a link back to the hub root

### Requirement: GitHub Pages deployment

The repository SHALL deploy the public site to GitHub Pages on pushes to `main` using a GitHub Actions workflow that publishes only hub site content (hub root, assets, catalog, and utilities trees).

#### Scenario: Deploy on main push

- **WHEN** changes merge to the `main` branch
- **THEN** the Pages workflow runs and updates the published site artifact

### Requirement: Catalog validation in CI

The repository SHALL run an automated check on pushes and pull requests to `main` that validates `data/utilities.json` and the `utilities/` directory layout.

#### Scenario: Valid catalog passes

- **WHEN** every catalog entry has required fields, unique ids, matching slugs, an existing `index.html`, and no orphan folders under `utilities/`
- **THEN** the validation job succeeds

#### Scenario: Broken path fails

- **WHEN** a catalog entry references a path without `index.html` or a folder exists under `utilities/` without a catalog entry
- **THEN** the validation job fails
