#!/usr/bin/env python3
"""Build a conservative merge plan from release metadata + content profiles.

This is the policy layer. It does not trust a single keyword mention as a
canonicality decision and never promotes a release payload automatically.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "raw/release-assets/backend-docs/MANIFEST.json"
DEFAULT_CONTENT = ROOT / "raw/release-assets/backend-docs/CONTENT_INDEX.json"
DEFAULT_OUTPUT = ROOT / "raw/release-assets/backend-docs/MERGE_PLAN.json"
DEFAULT_REPORT = ROOT / "docs/RELEASE_ASSET_MERGE_PLAN.md"

PROMOTION_TARGETS = {
    "sourceborn-core": ["brain/", "machine/", "phase2/", "docs/"],
    "asi": ["registries/asi/", "machine/", "phase2/asi/", "phase2/sources/"],
    "engines": ["machine/", "phase2/sources/", "brain/12-optional-tool-rag/"],
    "parameters": ["registries/human/", "registries/ai/", "registries/asi/", "machine/parameters/"],
    "sequence": ["raw/sequence/", "machine/v2/", "phase2/v2/", "docs/"],
    "wisdom": ["raw/wisdom/", "phase2/wisdom/", "registries/wisdom/"],
    "tests-audits": ["phase2/tests/", "phase2/reviews/", "phase2/rfr/", "generated/tests/"],
    "operations": ["docs/ops/", "docs/deployment/"],
    "visuals": ["raw/visuals/", "docs/visuals/"],
    "archives-transcripts": ["raw/release-assets/backend-docs/archives-transcripts/"],
    "model-evidence": ["raw/release-assets/backend-docs/model-evidence/"],
    "reference": ["raw/release-assets/backend-docs/reference/"],
    "research": ["raw/research/"],
    "off-project": [],
    "quarantine": [],
}

CANONICAL_CANDIDATE_ROUTES = {
    "sourceborn-core", "asi", "engines", "parameters", "sequence",
    "wisdom", "tests-audits", "operations", "visuals",
}


def profile_hits(profile: dict[str, Any]) -> Counter[str]:
    body = profile.get("profile") or {}
    candidates = (
        body.get("keyword_hits"),
        body.get("keyword_hits_in_headers"),
        body.get("keyword_hits_sample"),
    )
    hits: Counter[str] = Counter()
    for candidate in candidates:
        if isinstance(candidate, dict):
            for key, value in candidate.items():
                try:
                    hits[str(key).lower()] += int(value)
                except (TypeError, ValueError):
                    pass
    return hits


def final_route(asset: dict[str, Any], profile: dict[str, Any]) -> tuple[str, str, list[str]]:
    current = asset.get("route", "unclassified")
    name = str(asset.get("name", "")).lower().replace(" ", "_")
    hits = profile_hits(profile)
    flags: list[str] = []

    if hits["grok"]:
        flags.append("contains_grok_reference")

    # Explicit filename policy wins. A mere content mention does not.
    if "grok" in name:
        return "quarantine", "explicit Grok-specific filename", flags

    if current != "unclassified":
        return current, "deterministic filename route retained", flags

    if any(x in name for x in ("conversation", "transcript", "chat", "archive", "memory", "pasted")):
        return "archives-transcripts", "conversation/archive filename signal", flags
    if any(x in name for x in ("claude", "gemini", "gpt", "lovable", "deepseek", "model_")):
        return "model-evidence", "model-output/reference filename signal", flags
    if any(x in name for x in ("riemann", "silence_on_the_mirror", "one_dot", "hollo", "holo_")):
        return "research", "research-family filename signal", flags
    if any(x in name for x in ("ard", "rgl", "met_")):
        return "research", "ARD/RGL research/reference filename signal", flags

    # Strong content signals. Thresholds use actual extracted keyword counts,
    # not JSON-string presence counts.
    if hits["stock"] >= 8:
        return "off-project", "strong stock-domain content signal", flags
    if hits["sourceborn"] >= 8 or hits["urr"] >= 8:
        return "sourceborn-core", "strong Sourceborn/URR content signal", flags
    if hits["asi"] >= 8 and (hits["brain"] + hits["node"] + hits["registry"] >= 4):
        return "asi", "strong ASI architecture/registry content signal", flags
    if hits["engine"] >= 10 or hits["definition"] >= 6:
        return "engines", "strong engine/definition content signal", flags
    if hits["parameter"] >= 10:
        return "parameters", "strong parameter content signal", flags
    if hits["sequence"] >= 10:
        return "sequence", "strong sequence content signal", flags
    if hits["wisdom"] >= 8:
        return "wisdom", "strong wisdom content signal", flags
    if hits["audit"] + hits["test"] + hits["verification"] >= 12:
        return "tests-audits", "strong testing/audit content signal", flags
    if hits["riemann"] >= 8 or hits["mirror"] >= 8:
        return "research", "strong RH/Riemann/Mirror content signal", flags

    # Strong Grok presence in a generic file becomes model evidence, not
    # quarantine, unless the filename itself says Grok.
    if hits["grok"] >= 8:
        return "model-evidence", "strong model-reference content; Grok sections must be excluded from canonical promotion", flags

    return "reference", "generic source/reference material pending semantic reconciliation", flags


def action_for(route: str, asset: dict[str, Any]) -> tuple[str, bool]:
    if asset.get("repo_sha256_matches"):
        return "skip-exact-existing", False
    if not asset.get("digest_primary"):
        return "skip-release-duplicate", False
    if route == "quarantine":
        return "quarantine-pointer-only", False
    if route == "off-project":
        return "keep-out-of-c-sb-core", False
    if route in {"research", "model-evidence", "archives-transcripts", "reference"}:
        return "preserve-pointer-and-review", False
    if route in CANONICAL_CANDIDATE_ROUTES:
        return "semantic-reconcile-candidate", True
    return "preserve-pointer-and-review", False


def build_plan(manifest: dict[str, Any], content: dict[str, Any]) -> dict[str, Any]:
    profiles = {int(p["asset_id"]): p for p in content["profiles"]}
    # Duplicate release records reuse the profile of their digest primary.
    primary_by_id = {int(a["asset_id"]): int(a.get("duplicate_of_asset_id") or a["asset_id"]) for a in manifest["assets"]}

    decisions = []
    route_counts: Counter[str] = Counter()
    action_counts: Counter[str] = Counter()
    candidate_count = 0

    for asset in manifest["assets"]:
        asset_id = int(asset["asset_id"])
        primary_id = primary_by_id[asset_id]
        profile = profiles.get(primary_id, {})
        route, reason, flags = final_route(asset, profile)
        action, candidate = action_for(route, asset)
        route_counts[route] += 1
        action_counts[action] += 1
        candidate_count += int(candidate)
        decisions.append({
            "asset_id": asset_id,
            "name": asset["name"],
            "sha256": asset.get("sha256"),
            "size": asset.get("size"),
            "route": route,
            "route_reason": reason,
            "flags": flags,
            "action": action,
            "canonical_reconciliation_candidate": candidate,
            "repo_sha256_matches": asset.get("repo_sha256_matches", []),
            "duplicate_of_asset_id": asset.get("duplicate_of_asset_id"),
            "release_download_url": asset.get("download_url"),
            "promotion_targets_after_review": PROMOTION_TARGETS.get(route, []),
        })

    return {
        "schema_version": 1,
        "repository": manifest["repository"],
        "release": manifest["release"],
        "policy": {
            "release_payloads_are_source_evidence_not_automatic_truth": True,
            "exact_repo_matches_are_not_reimported": True,
            "release_duplicates_are_not_reimported": True,
            "grok_filename_assets_are_quarantined": True,
            "grok_mentions_in_mixed_files_do_not_quarantine_entire_file": True,
            "canonical_promotion_requires_semantic_reconciliation_and_rfr": True,
        },
        "summary": {
            "asset_count": len(decisions),
            "route_counts": dict(sorted(route_counts.items())),
            "action_counts": dict(sorted(action_counts.items())),
            "canonical_reconciliation_candidate_count": candidate_count,
        },
        "decisions": decisions,
    }


def write_report(plan: dict[str, Any], path: Path) -> None:
    summary = plan["summary"]
    decisions = plan["decisions"]
    candidates = [d for d in decisions if d["canonical_reconciliation_candidate"]]
    candidates.sort(key=lambda d: (d["route"], str(d["name"]).lower()))

    lines = [
        "# Backend Docs Release Merge Plan",
        "",
        "This is the conservative policy decision layer built from the 383-asset release manifest plus structural content profiling.",
        "",
        f"- Release records: **{summary['asset_count']}**",
        f"- Canonical reconciliation candidates: **{summary['canonical_reconciliation_candidate_count']}**",
        "- Exact byte matches already in the repo are skipped.",
        "- Release digest duplicates are skipped for import while all alias records remain in provenance.",
        "- Grok-specific filenames are quarantined; a mixed file is **not** quarantined merely because it mentions Grok.",
        "",
        "## Actions",
        "",
        "| Action | Assets |",
        "|---|---:|",
    ]
    for action, count in sorted(summary["action_counts"].items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{action}` | {count} |")

    lines += ["", "## Final routes", "", "| Route | Assets |", "|---|---:|"]
    for route, count in sorted(summary["route_counts"].items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{route}` | {count} |")

    lines += [
        "",
        "## Canonical reconciliation queue",
        "",
        "These assets are **candidates**, not automatic replacements. The first landing zone is provenance/raw custody; only reconciled concepts/records move into canonical registries, machine contracts, brain stages, tests or docs.",
        "",
        "| Route | Asset | Post-review targets | Flags |",
        "|---|---|---|---|",
    ]
    for d in candidates:
        targets = ", ".join(f"`{x}`" for x in d["promotion_targets_after_review"])
        flags = ", ".join(d["flags"])
        name = str(d["name"]).replace("|", "\\|")
        lines.append(f"| `{d['route']}` | `{name}` | {targets} | {flags} |")

    lines += [
        "",
        "## Safety boundary",
        "",
        "`quarantine`, `off-project`, `research`, `model-evidence`, `archives-transcripts`, and generic `reference` assets stay outside canonical Sourceborn structures unless a later explicit review promotes a specific claim/record with provenance.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--content-index", type=Path, default=DEFAULT_CONTENT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    content = json.loads(args.content_index.read_text(encoding="utf-8"))
    plan = build_plan(manifest, content)

    if plan["summary"]["asset_count"] != 383:
        raise RuntimeError(f"expected 383 decisions, found {plan['summary']['asset_count']}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(plan, args.report)
    print(json.dumps(plan["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
