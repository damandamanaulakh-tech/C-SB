#!/usr/bin/env python3
"""Build a deterministic provenance manifest for a GitHub release.

The script intentionally inventories and classifies release assets without
promoting any asset into canonical Sourceborn structures. Promotion remains a
separate review/R-F-R decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "raw/release-assets/backend-docs/MANIFEST.json"
DEFAULT_REPORT = REPO_ROOT / "docs/RELEASE_ASSET_INGESTION_REPORT.md"

# Explicitly blocked from canonical ingestion unless a later human decision
# changes the policy. This preserves the current build constraint.
QUARANTINE_PATTERNS = (
    "grok",
)

OFF_PROJECT_PATTERNS = (
    "resume",
    "cv_",
    "curriculum_vitae",
    "birthday",
    "stock",
    "ashstock",
    "ash08",
)

RESEARCH_PATTERNS = (
    "riemann",
    "rh_",
    "silence_on_the_mirror",
    "silence.on.the.mirror",
    "one_dot",
    "one.dot",
    "hollo",
    "holo_",
    "mirror_structure",
)


def _contains_any(name: str, patterns: tuple[str, ...]) -> bool:
    return any(p in name for p in patterns)


def classify_asset(name: str, content_type: str) -> tuple[str, str, int]:
    """Return (route, rationale, priority), where 1 is highest priority."""
    n = name.lower().replace(" ", "_")
    ct = (content_type or "").lower()

    if _contains_any(n, QUARANTINE_PATTERNS):
        return "quarantine", "explicitly blocked model-derived material", 99
    if _contains_any(n, OFF_PROJECT_PATTERNS):
        return "off-project", "filename indicates unrelated/personal/cross-project material", 90
    if _contains_any(n, RESEARCH_PATTERNS):
        return "research", "research corpus; preserve separately from Sourceborn core", 70

    if ct.startswith("image/") or n.endswith((".svg", ".png", ".jpg", ".jpeg", ".webp")):
        return "visuals", "visual/diagram asset", 60

    if any(x in n for x in ("test", "audit", "review", "flaw", "scorecard", "rfr", "adversarial", "verification")):
        return "tests-audits", "test/review/audit evidence", 30

    if any(x in n for x in ("bhagavad", "gita", "mahabharata", "wisdom", "holy_book", "holy-book")):
        return "wisdom", "wisdom/holy-book source material", 40

    if any(x in n for x in ("universal_sequence", "the_sequences", "sequence_machine", "sequence_map", "sequence_to_sequence", "reverse_walk")):
        return "sequence", "Universal Sequence / sequence-machine source", 20

    if any(x in n for x in ("parameter", "subparameter", "human_native", "human_container", "ai_readable_11338", "table.csv", "table.2.csv", "table.3.csv")):
        return "parameters", "parameter/container bank or structured table", 10

    if any(x in n for x in ("engine", "definition_engine", "raw_definition", "definer", "orchestrator_reusable", "orchestrat")):
        return "engines", "engine/definition/orchestration material", 8

    if any(x in n for x in ("asi-brain", "asi_brain", "asi_core", "asi-core", "asi_unified", "asi_engines", "asi-engine", "asi_worldwide", "asi_registry", "asi_catalog", "asi_node")):
        return "asi", "ASI registry/catalog/brain/engine material", 5

    if any(x in n for x in ("sourceborn", "sb_urr", "sb-urr", "urr_", "urr-", "urr.", "core_spec", "core_backbone", "clean_core", "sourceborn_master", "sourceborn_handoff")):
        return "sourceborn-core", "Sourceborn/URR/core specification material", 6

    if any(x in n for x in ("render", "deploy", "deployment", "site_control", "project_plan", "handoff", "the_plan", "workstream", "pending_task")):
        return "operations", "deployment/project-control/handoff material", 50

    return "unclassified", "no deterministic route matched; manual review required", 80


def api_json(url: str, token: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "c-sb-release-asset-inventory",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {exc.code} for {url}: {body}") from exc


def fetch_release(repository: str, tag: str, token: str) -> dict[str, Any]:
    quoted_tag = urllib.parse.quote(tag, safe="")
    url = f"https://api.github.com/repos/{repository}/releases/tags/{quoted_tag}"
    data = api_json(url, token)
    if not isinstance(data, dict):
        raise RuntimeError("release response was not an object")
    return data


def fetch_assets(repository: str, release_id: int, token: str) -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{repository}/releases/{release_id}/assets"
            f"?per_page=100&page={page}"
        )
        batch = api_json(url, token)
        if not isinstance(batch, list):
            raise RuntimeError(f"asset page {page} was not a list")
        assets.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return assets


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def repository_digest_index(excluded: set[Path]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        resolved = path.resolve()
        if resolved in excluded:
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            digest = sha256_file(path)
        except OSError as exc:
            print(f"warning: could not hash {rel}: {exc}", file=sys.stderr)
            continue
        index[digest].append(rel)
    return dict(index)


def sanitize_filename(name: str) -> str:
    # Keep source filenames recognizable while making proposed paths portable.
    cleaned = re.sub(r"[^A-Za-z0-9._()\-]+", "_", name).strip("._")
    return cleaned or "unnamed_asset"


def build_manifest(repository: str, tag: str, token: str, output: Path, report: Path) -> dict[str, Any]:
    release = fetch_release(repository, tag, token)
    release_id = int(release["id"])
    assets = fetch_assets(repository, release_id, token)

    digest_index = repository_digest_index({output.resolve(), report.resolve()})

    # GitHub's asset digest is currently sha256:<hex>. Assets without a digest
    # remain distinct and are never guessed to be duplicates.
    by_digest: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for asset in assets:
        digest = asset.get("digest") or ""
        if digest.startswith("sha256:"):
            by_digest[digest[7:]].append(asset)

    primary_by_asset_id: dict[int, int] = {}
    duplicate_groups: list[dict[str, Any]] = []
    for digest, group in sorted(by_digest.items()):
        ordered = sorted(group, key=lambda a: (str(a.get("name", "")).lower(), int(a.get("id", 0))))
        primary_id = int(ordered[0]["id"])
        for asset in ordered:
            primary_by_asset_id[int(asset["id"])] = primary_id
        if len(ordered) > 1:
            duplicate_groups.append(
                {
                    "sha256": digest,
                    "primary_asset_id": primary_id,
                    "asset_ids": [int(a["id"]) for a in ordered],
                    "names": [a.get("name") for a in ordered],
                }
            )

    records: list[dict[str, Any]] = []
    route_counts: Counter[str] = Counter()
    priority_counts: Counter[int] = Counter()
    exact_repo_match_count = 0

    for asset in sorted(assets, key=lambda a: (str(a.get("name", "")).lower(), int(a.get("id", 0)))):
        asset_id = int(asset["id"])
        name = str(asset.get("name") or "")
        content_type = str(asset.get("content_type") or "")
        route, rationale, priority = classify_asset(name, content_type)
        route_counts[route] += 1
        priority_counts[priority] += 1

        digest_value = str(asset.get("digest") or "")
        sha256 = digest_value[7:] if digest_value.startswith("sha256:") else None
        repo_matches = digest_index.get(sha256 or "", [])
        if repo_matches:
            exact_repo_match_count += 1

        primary_id = primary_by_asset_id.get(asset_id, asset_id)
        duplicate_of = primary_id if primary_id != asset_id else None

        records.append(
            {
                "asset_id": asset_id,
                "name": name,
                "content_type": content_type,
                "size": int(asset.get("size") or 0),
                "state": asset.get("state"),
                "sha256": sha256,
                "digest_primary": duplicate_of is None,
                "duplicate_of_asset_id": duplicate_of,
                "repo_sha256_matches": repo_matches,
                "route": route,
                "route_rationale": rationale,
                "review_priority": priority,
                "proposed_intake_path": f"raw/release-assets/backend-docs/{route}/{sanitize_filename(name)}",
                "created_at": asset.get("created_at"),
                "updated_at": asset.get("updated_at"),
                "api_url": asset.get("url"),
                "download_url": asset.get("browser_download_url"),
            }
        )

    unique_digests = len(by_digest)
    duplicate_asset_count = sum(max(0, len(group) - 1) for group in by_digest.values())
    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": repository,
        "release": {
            "id": release_id,
            "tag_name": release.get("tag_name"),
            "name": release.get("name"),
            "target_commitish": release.get("target_commitish"),
            "published_at": release.get("published_at"),
            "html_url": release.get("html_url"),
        },
        "policy": {
            "upstream_release_is_immutable_source_custody": True,
            "automatic_canonical_promotion": False,
            "quarantine_terms": list(QUARANTINE_PATTERNS),
            "promotion_rule": "review + provenance check + Sourceborn R-F-R before canonical adoption",
        },
        "summary": {
            "asset_count": len(records),
            "assets_with_sha256": sum(1 for r in records if r["sha256"]),
            "unique_sha256_payloads": unique_digests,
            "duplicate_asset_count": duplicate_asset_count,
            "duplicate_group_count": len(duplicate_groups),
            "exact_repo_match_count": exact_repo_match_count,
            "route_counts": dict(sorted(route_counts.items())),
        },
        "duplicate_groups": duplicate_groups,
        "assets": records,
    }
    return manifest


def write_report(manifest: dict[str, Any], path: Path) -> None:
    summary = manifest["summary"]
    assets = manifest["assets"]
    routes = summary["route_counts"]
    duplicate_groups = manifest["duplicate_groups"]

    high_priority = [a for a in assets if a["review_priority"] <= 10 and not a["repo_sha256_matches"] and a["digest_primary"]]
    high_priority.sort(key=lambda a: (a["review_priority"], a["route"], a["name"].lower()))

    lines = [
        "# Release Asset Ingestion Report",
        "",
        f"Release: **{manifest['release']['name']}** (`{manifest['release']['tag_name']}`)",
        "",
        "This report is generated from GitHub release metadata plus exact SHA-256 hashing of the checked-out repository. It does **not** make release assets canonical automatically.",
        "",
        "## Inventory",
        "",
        f"- Total assets: **{summary['asset_count']}**",
        f"- Assets with SHA-256 metadata: **{summary['assets_with_sha256']}**",
        f"- Unique SHA-256 payloads: **{summary['unique_sha256_payloads']}**",
        f"- Duplicate asset records: **{summary['duplicate_asset_count']}** across **{summary['duplicate_group_count']}** digest groups",
        f"- Assets already byte-for-byte represented in the repository: **{summary['exact_repo_match_count']}**",
        "",
        "## Routing",
        "",
        "| Route | Assets |",
        "|---|---:|",
    ]
    for route, count in sorted(routes.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{route}` | {count} |")

    lines += [
        "",
        "## Duplicate groups",
        "",
    ]
    if duplicate_groups:
        for group in duplicate_groups:
            names = ", ".join(f"`{name}`" for name in group["names"])
            lines.append(f"- `{group['sha256'][:16]}…`: {names}")
    else:
        lines.append("No digest duplicates found.")

    lines += [
        "",
        "## Highest-priority unique assets not already present exactly",
        "",
        "These are routing candidates only. Their contents still require semantic reconciliation before promotion.",
        "",
        "| Priority | Route | Asset | Size |",
        "|---:|---|---|---:|",
    ]
    for asset in high_priority[:120]:
        safe_name = asset["name"].replace("|", "\\|")
        lines.append(f"| {asset['review_priority']} | `{asset['route']}` | `{safe_name}` | {asset['size']} |")
    if len(high_priority) > 120:
        lines.append(f"\n_...and {len(high_priority) - 120} more high-priority candidates; see `MANIFEST.json`._")

    lines += [
        "",
        "## Promotion rule",
        "",
        "1. Preserve the release as upstream custody.",
        "2. Do not copy exact SHA-256 matches already present in the repository.",
        "3. Deduplicate release variants by digest for ingestion purposes while retaining all alias records in the manifest.",
        "4. Review high-priority ASI, engine, parameter, Sourceborn/URR and sequence material first.",
        "5. Keep `quarantine`, `research`, and `off-project` material out of canonical structures unless explicitly reclassified.",
        "6. Promote only after provenance reconciliation and the repository's normal R-F-R process.",
        "",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_manifest(manifest: dict[str, Any], expected_count: int | None) -> None:
    assets = manifest.get("assets") or []
    ids = [a["asset_id"] for a in assets]
    if len(ids) != len(set(ids)):
        raise RuntimeError("manifest contains duplicate asset IDs")
    if expected_count is not None and len(assets) != expected_count:
        raise RuntimeError(f"expected {expected_count} release assets, found {len(assets)}")
    if manifest["summary"]["asset_count"] != len(assets):
        raise RuntimeError("summary asset_count does not match asset records")
    for asset in assets:
        if not asset["name"]:
            raise RuntimeError(f"asset {asset['asset_id']} has an empty name")
        if not asset["route"]:
            raise RuntimeError(f"asset {asset['asset_id']} has no route")
        if asset["duplicate_of_asset_id"] == asset["asset_id"]:
            raise RuntimeError(f"asset {asset['asset_id']} self-references as duplicate")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", "damandamanaulakh-tech/C-SB"))
    parser.add_argument("--release-tag", default="Docs")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--expected-count", type=int, default=383)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    manifest = build_manifest(args.repository, args.release_tag, token, args.output, args.report)
    validate_manifest(manifest, args.expected_count)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(manifest, args.report)

    print(json.dumps(manifest["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
