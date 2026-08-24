#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "generated/tests/P2_BATCH3_DIAGNOSTIC_V1.json"
REPORT.parent.mkdir(parents=True, exist_ok=True)

cmd = [sys.executable, "tools/test_batch3_native_runtime_v1_1.py"]
proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)

def tail(text: str, max_chars: int = 30000) -> str:
    if len(text) <= max_chars:
        return text
    return "...[truncated]...\n" + text[-max_chars:]

payload = {
    "report_id": "P2-BATCH3-DIAGNOSTIC-V1",
    "status": "PASS" if proc.returncode == 0 else "FAIL",
    "command": cmd,
    "returncode": proc.returncode,
    "stdout": tail(proc.stdout),
    "stderr": tail(proc.stderr),
    "native_report_exists": (ROOT / "generated/tests/P2_BATCH3_NATIVE_RUNTIME_RFR_V1_1.json").exists(),
}
REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(json.dumps(payload, indent=2))
# Intentionally return zero so the workflow can commit this diagnostic.
sys.exit(0)
