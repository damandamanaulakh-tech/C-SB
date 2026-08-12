#!/usr/bin/env python3
"""Inspect candidate Human-2560 release workbooks without committing binaries."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "raw/release-assets/backend-docs/MANIFEST.json"
DEFAULT_OUTPUT = ROOT / "raw/release-assets/backend-docs/HUMAN_SOURCE_INSPECTION.json"
DEFAULT_REPORT = ROOT / "docs/HUMAN_SOURCE_WORKBOOK_INSPECTION.md"

CANDIDATE_NAMES = (
    "ASI_Brain_Engine_Combined_Corpus_v1.xlsx",
    "Brain.+.Engine.Combined.Corpus.xlsx",
    "ASI-Brain.xlsx",
    "ASI-Brain_Task2_Approved_v0_1.xlsx",
    "ASI-Brain_Core_Engine_Combined_v0_4.xlsx",
    "ASI-Brain_Merged_APPROVED_EVIDENT_v0_3.xlsx",
    "ASI-Brain_Task3_Review_v0_2.xlsx",
)

EXPECTED_COLUMNS = (
    "row_id", "verified", "condensed_meaning", "bucket_256", "bucket_title",
    "sub_bucket_128", "category_64", "category_name", "reasoning_function",
    "actor_view", "phenomenological_qualia", "decision_function",
    "values_ethics", "bias_pattern", "memory_orientation", "system_mapping",
    "function_equation", "human_eval_relevance", "source",
    "verification_source", "schema_note",
)

ID_RE = re.compile(r"^H(?:00[1-9]|0[1-9]\d|[1-9]\d{2}|[12]\d{3}|25[0-5]\d|2560)$")


def download(url: str, token: str, path: Path) -> None:
    headers = {
        "Accept": "application/octet-stream",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "c-sb-human-source-inspector",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as response, path.open("wb") as out:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            out.write(block)


def norm(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def inspect_workbook(path: Path) -> dict[str, Any]:
    wb = load_workbook(path, read_only=True, data_only=True)
    result: dict[str, Any] = {"sheets": []}
    all_ids: set[str] = set()
    for ws in wb.worksheets:
        sheet: dict[str, Any] = {
            "name": ws.title,
            "max_row": ws.max_row,
            "max_column": ws.max_column,
            "first_rows": [],
            "header_matches": [],
            "id_count": 0,
            "id_samples": [],
            "sentinel_rows": {},
        }
        header_best = {"row": None, "matched": []}
        id_values: set[str] = set()
        sentinel_targets = {"H001", "H080", "H081", "H160", "H161", "H256", "H257", "H512", "H513", "H640", "H641", "H1280", "H1281", "H1920", "H1921", "H2560"}

        for r_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
            vals = [norm(v) for v in row]
            if r_idx <= 8:
                sheet["first_rows"].append(vals[:30])
            if r_idx <= 25:
                lower = {v.lower() for v in vals if v}
                matched = [c for c in EXPECTED_COLUMNS if c.lower() in lower]
                if len(matched) > len(header_best["matched"]):
                    header_best = {"row": r_idx, "matched": matched}
            for v in vals:
                if ID_RE.match(v):
                    id_values.add(v)
                    all_ids.add(v)
                    if v in sentinel_targets and v not in sheet["sentinel_rows"]:
                        sheet["sentinel_rows"][v] = {"row": r_idx, "values": vals[:40]}
            if len(sheet["id_samples"]) < 12:
                row_ids = [v for v in vals if ID_RE.match(v)]
                for rid in row_ids:
                    if rid not in sheet["id_samples"]:
                        sheet["id_samples"].append(rid)
                        if len(sheet["id_samples"]) >= 12:
                            break
        sheet["id_count"] = len(id_values)
        sheet["id_range"] = [min(id_values), max(id_values)] if id_values else []
        sheet["header_matches"] = header_best
        result["sheets"].append(sheet)
    wb.close()
    result["workbook_unique_h_ids"] = len(all_ids)
    result["workbook_h_id_range"] = [min(all_ids), max(all_ids)] if all_ids else []
    result["has_all_h001_h2560"] = len(all_ids) == 2560 and all(f"H{i:03d}" if i < 1000 else f"H{i}" for i in range(1, 2561)) <= all_ids
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    by_name = {a["name"]: a for a in manifest["assets"]}
    token = os.environ.get("GITHUB_TOKEN", "")
    inspections = []

    with tempfile.TemporaryDirectory(prefix="csb-human-source-") as td:
        tmp = Path(td)
        for name in CANDIDATE_NAMES:
            asset = by_name.get(name)
            if not asset:
                continue
            path = tmp / f"{asset['asset_id']}.xlsx"
            print(f"Inspecting {name}...")
            download(asset["api_url"], token, path)
            inspected = inspect_workbook(path)
            inspected.update({
                "asset_id": asset["asset_id"],
                "name": name,
                "sha256": asset.get("sha256"),
                "size": asset.get("size"),
            })
            inspections.append(inspected)

    payload = {"schema_version": 1, "candidates": inspections}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Human-2560 Source Workbook Inspection",
        "",
        "Release binaries are downloaded only inside CI and are not committed. This report records workbook structure needed for an exact, hash-guarded reconstruction.",
        "",
    ]
    for item in inspections:
        lines += [
            f"## `{item['name']}`",
            "",
            f"- Asset: `{item['asset_id']}`",
            f"- SHA-256: `{item['sha256']}`",
            f"- Size: `{item['size']}` bytes",
            f"- Unique Human IDs across workbook: **{item['workbook_unique_h_ids']}**",
            f"- Human ID range: `{item['workbook_h_id_range']}`",
            f"- Exact H001..H2560 set present: **{item['has_all_h001_h2560']}**",
            "",
            "| Sheet | Rows | Cols | H IDs | Best header row | Expected columns matched |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for sheet in item["sheets"]:
            hb = sheet["header_matches"]
            lines.append(
                f"| `{sheet['name']}` | {sheet['max_row']} | {sheet['max_column']} | {sheet['id_count']} | "
                f"{hb.get('row') or ''} | {len(hb.get('matched') or [])}/{len(EXPECTED_COLUMNS)} |"
            )
        lines += ["", "### Candidate headers / first rows", ""]
        for sheet in item["sheets"]:
            if not sheet["id_count"] and not sheet["header_matches"].get("matched"):
                continue
            lines.append(f"**{sheet['name']}**")
            for idx, row in enumerate(sheet["first_rows"], start=1):
                compact = " | ".join(x for x in row if x)
                if compact:
                    lines.append(f"- row {idx}: `{compact[:1500]}`")
            if sheet["sentinel_rows"]:
                lines.append("- sentinel IDs located: " + ", ".join(sorted(sheet["sentinel_rows"])))
            lines.append("")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"inspected": len(inspections)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
