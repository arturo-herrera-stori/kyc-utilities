#!/usr/bin/env python3
"""Validate data/utilities.json against hub conventions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "utilities.json"
UTILITIES_ROOT = ROOT / "utilities"

REQUIRED_FIELDS = ("id", "title", "summary", "category", "path", "status", "updated")
ALLOWED_STATUS = frozenset({"stable", "beta"})
ALLOWED_CATEGORIES = frozenset(
    {"observability", "reference", "runbooks", "tools", "onboarding"}
)
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(messages: list[str]) -> None:
    print("Catalog validation failed:\n", file=sys.stderr)
    for msg in messages:
        print(f"  - {msg}", file=sys.stderr)
    sys.exit(1)


def normalize_path(path: str) -> tuple[str | None, str | None]:
    p = path.strip().replace("\\", "/")
    if not p.endswith("/"):
        p += "/"
    if p.startswith("/"):
        return None, f"path must be relative, got {path!r}"
    if ".." in p.split("/"):
        return None, f"path must not contain '..': {path!r}"
    if not p.startswith("utilities/"):
        return None, f"path must start with utilities/: {path!r}"
    return p, None


def entry_dir(normalized_path: str) -> Path:
    return ROOT / normalized_path.rstrip("/")


def main() -> None:
    errors: list[str] = []

    if not CATALOG_PATH.is_file():
        fail([f"missing catalog file: {CATALOG_PATH.relative_to(ROOT)}"])

    try:
        raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail([f"invalid JSON in {CATALOG_PATH.relative_to(ROOT)}: {exc}"])

    if not isinstance(raw, list):
        fail(["catalog root must be a JSON array"])

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    catalog_dirs: set[Path] = set()

    for index, item in enumerate(raw):
        label = f"entry[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue

        item_id = item.get("id")
        if isinstance(item_id, str):
            label = f'entry id={item_id!r}'

        for field in REQUIRED_FIELDS:
            if field not in item or item[field] in (None, ""):
                errors.append(f"{label} missing required field {field!r}")

        if not isinstance(item.get("id"), str):
            errors.append(f"{label} id must be a string")
        else:
            if item["id"] in seen_ids:
                errors.append(f"duplicate id {item['id']!r}")
            seen_ids.add(item["id"])
            if not ID_PATTERN.match(item["id"]):
                errors.append(
                    f"{label} id must be kebab-case alphanumeric: {item['id']!r}"
                )

        path_val = item.get("path")
        if isinstance(path_val, str):
            norm_path, path_err = normalize_path(path_val)
            if path_err:
                errors.append(f"{label} {path_err}")
            elif norm_path:
                if norm_path in seen_paths:
                    errors.append(f"duplicate path {norm_path!r}")
                seen_paths.add(norm_path)

                util_dir = entry_dir(norm_path)
                catalog_dirs.add(util_dir.resolve())
                index_file = util_dir / "index.html"
                if not index_file.is_file():
                    errors.append(
                        f"{label} expected {index_file.relative_to(ROOT)} for path {norm_path!r}"
                    )

                expected_slug = norm_path.removeprefix("utilities/").rstrip("/")
                if isinstance(item_id, str) and item_id != expected_slug:
                    errors.append(
                        f"{label} id {item_id!r} should match path slug {expected_slug!r}"
                    )
        else:
            errors.append(f"{label} path must be a string")

        status = item.get("status")
        if isinstance(status, str) and status not in ALLOWED_STATUS:
            errors.append(
                f"{label} status must be one of {sorted(ALLOWED_STATUS)}: {status!r}"
            )

        category = item.get("category")
        if isinstance(category, str) and category not in ALLOWED_CATEGORIES:
            errors.append(
                f"{label} category must be one of {sorted(ALLOWED_CATEGORIES)}: {category!r}"
            )

        updated = item.get("updated")
        if isinstance(updated, str) and not DATE_PATTERN.match(updated):
            errors.append(
                f"{label} updated must be YYYY-MM-DD: {updated!r}"
            )

    if UTILITIES_ROOT.is_dir():
        for child in sorted(UTILITIES_ROOT.iterdir()):
            if not child.is_dir():
                errors.append(
                    f"utilities/ contains non-directory {child.name!r}; use one folder per utility"
                )
                continue
            if child.resolve() not in catalog_dirs:
                errors.append(
                    f"orphan utility folder {child.relative_to(ROOT)} has no catalog entry"
                )
    else:
        errors.append("missing utilities/ directory")

    if errors:
        fail(errors)

    print(f"OK: validated {len(raw)} catalog entr{'y' if len(raw) == 1 else 'ies'}.")


if __name__ == "__main__":
    main()
