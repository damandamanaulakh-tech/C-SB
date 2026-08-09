#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json"
OUT = ROOT / "generated/registry_views"
OUT.mkdir(parents=True, exist_ok=True)

containers = json.loads(SRC.read_text(encoding="utf-8"))["records"]

locals_ = [
    (1, "Activation Trigger", "defines the minimum evidence, state, goal, or event conditions required to activate this element", "TRIGGER_THRESHOLD_ENTRY"),
    (2, "Input Normalisation", "converts heterogeneous source and engine signals into a comparable operational representation without erasing provenance", "REPRESENTATION_AND_SOURCE_PRESERVATION"),
    (3, "Cross-Engine Synthesis", "combines relevant engine outputs, segment state, and source evidence while preserving contradictions and uncertainty", "MULTI_ENGINE_COMBINATION_WITH_CONTRADICTION_PRESERVATION"),
    (4, "State and Confidence Update", "updates the active state vector, confidence, proof debt, and priority after processing new information", "STATE_CHANGE_PLUS_EPISTEMIC_UPDATE"),
    (5, "Failure and Contradiction Response", "detects conflict, drift, overload, unsupported inference, or unsafe continuation and selects repair, checkpoint, or stop", "BLOCK_REPAIR_INVESTIGATION_OR_STOP"),
    (6, "Validated Commit and Feed-Forward", "commits approved output to action, memory, or downstream containers with rollback and lineage retained", "VERIFIED_OUTPUT_RETURN_MEMORY_OR_NEXT_EDGE"),
]

records = []
for container_id, segment_id, element_code, container_name, weight_class in containers:
    cnum = int(container_id.split("-")[-1])
    start = 2593 + (cnum - 161) * 6
    for local_no, name, clause, sequence_role in locals_:
        pid_num = start + local_no - 1
        records.append({
            "sequence": pid_num,
            "parameter_id": f"SB-ASI-P{pid_num:04d}",
            "system": "Sourceborn",
            "segment_id": segment_id,
            "container_id": container_id,
            "container_name": container_name,
            "element_code": element_code,
            "local_number": local_no,
            "operational_subparameter": name,
            "full_functional_wording": f"In ‘{container_name}’, {name.lower()} {clause}. It must preserve Point Zero, source lineage, engine identity, uncertainty, and the distinction between user-authorized evidence and externally verified evidence.",
            "sequence_role": sequence_role,
            "input_class": "State; evidence; memory; engine output; user command",
            "output_class": "Updated state; decision object; action instruction; memory candidate; verification result",
            "failure_gate": "Contradiction / proof debt / unsafe action / unresolved authority / termination condition",
            "memory_rule": "Write only validated outcome; retain rejected alternatives and source lineage",
            "weight_class": weight_class,
            "approval_status": "APPROVED BY USER",
            "evidence_status": "USER EVIDENT",
            "activation_status": "ACTIVE FOR TESTING",
            "external_verification_boundary": "SEPARATE LEDGER",
            "source": "ASI_Brain_Engine_Combined_Corpus_v1.xlsx#07 New Sub-Parameters"
        })

assert len(records) == 480
assert records[0]["parameter_id"] == "SB-ASI-P2593"
assert records[-1]["parameter_id"] == "SB-ASI-P3072"

payload = {
    "registry_id": "OPERATIONAL-SUBPARAMETERS-2593-3072-V1",
    "status": "GENERATED_FROM_APPROVED_SOURCE_PATTERN",
    "source_container_registry": str(SRC.relative_to(ROOT)),
    "record_count": len(records),
    "records": records,
}
(OUT / "operational_subparameters_2593_3072_v1.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

md = ["# Operational Sub-Parameters SB-ASI-P2593..SB-ASI-P3072", "", "Generated from the approved CON-161..CON-240 source pattern.", ""]
for r in records:
    md.append(f"- **{r['parameter_id']}** → `{r['container_id']}` / {r['operational_subparameter']} / {r['sequence_role']}")
(OUT / "OPERATIONAL_SUBPARAMETERS_2593_3072_V1.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"Generated {len(records)} operational sub-parameters: {records[0]['parameter_id']}..{records[-1]['parameter_id']}")
