#!/usr/bin/env python3
"""Integration/R-F-R test for Sourceborn Batch-3 native runtime engines."""
from __future__ import annotations

from pathlib import Path
import json
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from machine.runtime.engines.actor_role_engine import infer_actor_roles
from machine.runtime.engines.actor_state_engine import build_actor_state_hypotheses
from machine.runtime.engines.combination_engine import generate_combinations
from machine.runtime.engines.event_decomposition_engine import decompose_source
from machine.runtime.engines.evidence_prediction_engine import generate_evidence_predictions
from machine.runtime.engines.future_state_reconstruction_engine import reconstruct_future_states
from machine.runtime.engines.live_intent_engine import generate_live_intents
from machine.runtime.engines.native_runtime_pipeline import run_event_pipeline
from machine.runtime.engines.parameter_activation_engine import activate_event, apply_activations_to_event
from machine.runtime.engines.relation_graph_engine import build_event_relation_graph
from machine.runtime.engines.runtime_core import RegistryIndex
from machine.runtime.engines.source_lock_engine import lock_text_source

GEN = ROOT / "generated/tests"
GEN.mkdir(parents=True, exist_ok=True)
REPORT_PATH = GEN / "P2_BATCH3_NATIVE_RUNTIME_RFR_V1.json"

errors: list[str] = []
warnings: list[str] = []

# 0. All Batch-3 engine files must at least compile before structural testing.
engine_dir = ROOT / "machine/runtime/engines"
engine_files = sorted(p for p in engine_dir.glob("*.py") if p.name != "__pycache__")
compile_failures = []
for path in engine_files:
    try:
        py_compile.compile(str(path), doraise=True)
    except Exception as exc:
        compile_failures.append(f"{path.name}:{exc}")
if compile_failures:
    errors.extend("compile:" + item for item in compile_failures)

# 1. Controlled source. It is a test fixture, not historical evidence.
text = (
    "The commissioner ordered the scribe to record the dedication for the temple audience. "
    "The record was intended to remain available after the ceremony."
)
sequence_id = "SYN-BATCH3-RUNTIME-001"
source = lock_text_source(
    text,
    source_type="GENERATED_TEST_FIXTURE",
    locator="fixture://batch3/native-runtime-001",
    scope={"sequence_id": sequence_id, "test": True},
    metadata={"fixture": True, "historical_claim": False},
)
decomposition = decompose_source(source.payload, sequence_id=sequence_id, strategy="WHOLE")
events = decomposition.payload.get("events", [])
if len(events) != 1:
    errors.append(f"expected exactly one Event, got {len(events)}")
event = events[0] if events else {}

# 2. Small controlled registry index. IDs are existing-style source IDs, but this
# fixture does not assert that these definitions replace the repo's native files.
index = RegistryIndex()
index.add_document("fixture/human.json", {
    "containers": [
        {"container_id": "CON-063", "exact_name": "Intent Formation and Commitment", "definition": "Immediate intention, future intention, action commitment, implementation intention."},
        {"container_id": "CON-080", "exact_name": "External Cognition, Institutions and Collective Intelligence", "definition": "Writing, records, organisations, procedures, distributed memory."},
    ]
})
index.add_document("fixture/ai.json", {
    "functions": [
        {"id": "AI-17", "name": "Verification", "definition": "Evidence checking, validation, acceptance and verification."},
        {"id": "AI-22", "name": "Communication", "definition": "Represent, communicate, write and transmit information."},
    ]
})
index.add_document("fixture/asi.json", {
    "governance": [
        {"id": "ASI-02", "name": "Truth Provenance Governance", "definition": "Source, truth, evidence and provenance governance."},
        {"id": "ASI-08", "name": "Safety Permission Authority", "definition": "Permission, authority and safe execution governance."},
    ]
})

activation = activate_event(event, index, min_score=0.05, primary_threshold=0.16, secondary_threshold=0.08)
working_event = apply_activations_to_event(event, activation)
if not activation.payload.get("activation_refs"):
    errors.append("controlled registry produced no activations")
if any(a.get("object_id", "").startswith("SB-ASI-P") for a in activation.payload.get("activation_refs", [])):
    errors.append("activation engine invented atomic Human parameter ID")

# 3. Explicit actor roles preserve operational separation.
actor_hints = [
    {"actor_ref": "ACT-COMMISSIONER", "role": "REQUESTER", "actor_type": "HUMAN", "epistemic_status": "SOURCE_STATED", "supporting_evidence_refs": ["OBS-ORDER"]},
    {"actor_ref": "ACT-COMMISSIONER", "role": "CONTROLLER", "actor_type": "HUMAN", "epistemic_status": "INFERRED", "supporting_evidence_refs": ["OBS-ORDER"]},
    {"actor_ref": "ACT-SCRIBE", "role": "PERFORMER", "actor_type": "HUMAN", "epistemic_status": "SOURCE_STATED", "supporting_evidence_refs": ["OBS-SCRIBE"]},
    {"actor_ref": "ACT-SCRIBE", "role": "WRITER", "actor_type": "HUMAN", "epistemic_status": "SOURCE_STATED", "supporting_evidence_refs": ["OBS-SCRIBE"]},
    {"actor_ref": "ACT-TEMPLE-AUDIENCE", "role": "AUDIENCE", "actor_type": "GROUP", "epistemic_status": "SOURCE_STATED", "supporting_evidence_refs": ["OBS-AUDIENCE"]},
]
roles = infer_actor_roles(working_event, actor_hints=actor_hints, lexical_hypotheses=False)
working_event["actor_roles"] = roles.payload.get("actor_role_assignments", [])
role_pairs = {(a.get("actor_ref"), a.get("role")) for a in working_event["actor_roles"]}
for expected in [
    ("ACT-COMMISSIONER", "REQUESTER"),
    ("ACT-COMMISSIONER", "CONTROLLER"),
    ("ACT-SCRIBE", "PERFORMER"),
    ("ACT-SCRIBE", "WRITER"),
    ("ACT-TEMPLE-AUDIENCE", "AUDIENCE"),
]:
    if expected not in role_pairs:
        errors.append(f"actor-role separation missing {expected}")

# Add an explicit future-state structure so Live Intent has a desired difference
# without inventing it from prose.
working_event["state_refs"] = [{
    "state_id": "STATE-RECORD-AVAILABLE",
    "state_role": "EXPECTED_FUTURE_STATE",
    "entity_ref": "OBJ-DEDICATION-RECORD",
    "state_payload": {"availability": "PERSISTS_AFTER_CEREMONY"},
    "source_refs": [event["source_refs"][0]["source_id"]],
    "epistemic_status": "SOURCE_STATED",
}]
working_event["object_ids"] = ["OBJ-DEDICATION-RECORD"]

# 4. Same commissioner, two alternative state hypotheses. Identity must not split.
scenario_variants = {
    "ACT-COMMISSIONER": [
        {
            "label": "SECURE_AUTHORITY",
            "dimensions": [{"dimension": "BELONGING_STATUS_GROUP", "value": "SECURE", "epistemic_status": "NEW_SYNTHETIC"}],
            "epistemic_status": "NEW_SYNTHETIC",
        },
        {
            "label": "THREATENED_AUTHORITY",
            "dimensions": [
                {"dimension": "BELONGING_STATUS_GROUP", "value": "THREATENED", "epistemic_status": "NEW_SYNTHETIC"},
                {"dimension": "THREAT_LOSS", "value": "ELEVATED", "epistemic_status": "NEW_SYNTHETIC"},
            ],
            "epistemic_status": "NEW_SYNTHETIC",
        },
    ]
}
states = build_actor_state_hypotheses(working_event, working_event["actor_roles"], scenario_variants=scenario_variants)
commissioner_states = [s for s in states.payload.get("actor_state_hypotheses", []) if s.get("actor_ref") == "ACT-COMMISSIONER"]
if len(commissioner_states) < 3:
    errors.append("same-actor multi-state search space was not generated")
if any(s.get("identity_ref") != "ACT-COMMISSIONER" for s in commissioner_states):
    errors.append("actor state variants split identity")

# 5. Relation graph and bounded combinations.
relations = build_event_relation_graph(working_event)
if relations.payload.get("identity_merges") != 0:
    errors.append("relation graph performed identity merge")

pattern_priors = [{"pattern_id": "PC-SYN-RECORD-PERSISTENCE", "epistemic_status": "GENERATED_TEST_FIXTURE"}]
memory_priors = [{"memory_id": "MEM-SYN-PRIOR-001", "epistemic_status": "GENERATED_TEST_FIXTURE"}]
combos = generate_combinations(
    working_event,
    relations=relations.payload.get("relations", []),
    actor_states=states.payload.get("actor_state_hypotheses", []),
    pattern_priors=pattern_priors,
    memory_priors=memory_priors,
    max_candidates=30,
    max_candidates_per_mode=8,
)
if combos.payload.get("cartesian_product_performed") is not False:
    errors.append("combination engine did not preserve bounded generation law")
if combos.payload.get("combination_count", 0) == 0:
    errors.append("combination engine produced no candidates")
if combos.payload.get("counts_by_mode", {}).get("COUNTERFACTUAL", 0) == 0:
    errors.append("actor-state counterfactual combination not produced")
if combos.payload.get("counts_by_mode", {}).get("CROSS_DOMAIN", 0) == 0:
    warnings.append("controlled lexical activation did not create a cross-domain pair; this is not a hard failure")

# 6. Live Intent + future state + evidence.
intents = generate_live_intents(
    working_event,
    working_event["actor_roles"],
    actor_states=states.payload.get("actor_state_hypotheses", []),
    combination_records=combos.payload.get("combination_records", []),
)
intent_candidates = intents.payload.get("intent_candidates", [])
if not intent_candidates:
    errors.append("live Intent engine produced no candidates")
if any(i.get("stated_motive") is not None for i in intent_candidates):
    errors.append("live Intent engine conflated inferred Intent with stated motive")

# Re-run novelty against its own first result. Same structural Intents should not
# count as new merely because a second run can render different surrounding text.
intents_second = generate_live_intents(
    working_event,
    working_event["actor_roles"],
    actor_states=states.payload.get("actor_state_hypotheses", []),
    combination_records=combos.payload.get("combination_records", []),
    existing_intents=intent_candidates,
)
if intents_second.payload.get("new_intent_structure_count", 0) != 0:
    errors.append("new wording/execution pass inflated existing Intent structures")

future = reconstruct_future_states(working_event, intent_candidates=intent_candidates)
if future.payload.get("future_state_count", 0) == 0:
    errors.append("future-state reconstruction produced no candidates")

predictions = generate_evidence_predictions(
    working_event,
    intent_candidates=intent_candidates,
    future_states=future.payload.get("future_state_candidates", []),
    combination_records=combos.payload.get("combination_records", []),
    domain_predictions=[{
        "hypothesis_ref": intent_candidates[0]["intent_id"] if intent_candidates else "NONE",
        "test_type": "DOMAIN_SPECIFIC_TEST",
        "domain": "SYNTHETIC_RECORD_FIXTURE",
        "expected_observation": {"record_persists_after_ceremony": True},
        "failure_implication": "Weakens the record-persistence Intent branch.",
        "source_independence_required": True,
        "priority": "HIGH",
    }],
)
if predictions.payload.get("prediction_count", 0) == 0:
    errors.append("evidence prediction engine produced no tests")

# 7. Full orchestrated event pass. We deliberately do not manufacture evidence
# results here; R-F-R should preserve UNKNOWN/open proof debt rather than auto-pass.
run = run_event_pipeline(
    working_event,
    registry_index=index,
    actor_hints=actor_hints,
    scenario_variants=scenario_variants,
    pattern_priors=pattern_priors,
    memory_priors=memory_priors,
    domain_future_templates=[{
        "state_payload": {"availability": "PERSISTS_AFTER_CEREMONY"},
        "entity_ref": "OBJ-DEDICATION-RECORD",
        "future_role": "SYNTHETIC_PERSISTENCE_TEST",
        "epistemic_status": "GENERATED_TEST_FIXTURE",
        "proof_debt": ["FIXTURE_ONLY"],
    }],
    domain_evidence_predictions=[],
    evidence_results={},
)
required_stages = {
    "activation", "actor_roles", "actor_states", "relation_graph", "combinations",
    "live_intents", "future_states", "evidence_predictions", "rfr", "falsifiers", "maturity",
}
if required_stages - set(run.get("stages", {})):
    errors.append(f"orchestrator missing stages: {sorted(required_stages - set(run.get('stages', {})))}")
if run.get("writeback_boundary", {}).get("automatic_persistent_writes_performed") != 0:
    errors.append("Batch-3 crossed into persistent writeback before Batch-4")
if run.get("writeback_boundary", {}).get("status") != "NOT_IMPLEMENTED_IN_BATCH3":
    errors.append("Batch-3 writeback boundary not explicit")

# R-F-R should not auto-pass hypotheses when no tests were supplied.
rfr_payload = run.get("stages", {}).get("rfr", {}).get("payload", {})
if rfr_payload.get("assessment_count", 0) == 0:
    errors.append("R-F-R assessed no hypotheses")
if rfr_payload.get("open_count", 0) == 0 and rfr_payload.get("weaken_or_reject_count", 0) == 0 and rfr_payload.get("fail_count", 0) == 0:
    errors.append("R-F-R appears to auto-pass all untested hypotheses")

maturities = [
    item.get("payload", {}).get("maturity")
    for item in run.get("stages", {}).get("maturity", {}).values()
    if isinstance(item, dict)
]
if "M5" in maturities:
    errors.append("untested synthetic fixture auto-matured to M5")

report = {
    "report_id": "P2-BATCH3-NATIVE-RUNTIME-RFR-V1",
    "status": "PASS" if not errors else "FAIL",
    "system_identity": "REAL_TIME_GROWING_ASI_PROTOTYPE",
    "runtime_package": "SOURCEBORN-NATIVE-RUNTIME-ENGINES-BATCH3-V1",
    "fixture_sequence_id": sequence_id,
    "checks": {
        "engine_python_files_compiled": len(compile_failures) == 0,
        "source_locked": source.status == "COMPLETE",
        "one_event_decomposed": len(events) == 1,
        "existing_registry_activations_present": bool(activation.payload.get("activation_refs")),
        "atomic_human_ids_not_invented": not any(a.get("object_id", "").startswith("SB-ASI-P") for a in activation.payload.get("activation_refs", [])),
        "actor_roles_separated": len(role_pairs) >= 5,
        "same_actor_multiple_states": len(commissioner_states) >= 3,
        "actor_identity_preserved": all(s.get("identity_ref") == "ACT-COMMISSIONER" for s in commissioner_states),
        "no_identity_merge": relations.payload.get("identity_merges") == 0,
        "bounded_combinations": combos.payload.get("cartesian_product_performed") is False,
        "counterfactual_combination_present": combos.payload.get("counts_by_mode", {}).get("COUNTERFACTUAL", 0) > 0,
        "live_intents_present": bool(intent_candidates),
        "new_wording_not_new_intent": intents_second.payload.get("new_intent_structure_count", 0) == 0,
        "future_states_present": future.payload.get("future_state_count", 0) > 0,
        "evidence_predictions_present": predictions.payload.get("prediction_count", 0) > 0,
        "rfr_present": rfr_payload.get("assessment_count", 0) > 0,
        "no_untested_M5": "M5" not in maturities,
        "no_persistent_writeback_in_batch3": run.get("writeback_boundary", {}).get("automatic_persistent_writes_performed") == 0,
    },
    "counts": {
        "compiled_engine_files": len(engine_files),
        "activation_count": activation.payload.get("activation_count", 0),
        "actor_role_count": len(role_pairs),
        "actor_state_count": states.payload.get("state_variant_count", 0),
        "relation_count": len(relations.payload.get("relations", [])),
        "combination_count": combos.payload.get("combination_count", 0),
        "live_intent_count": len(intent_candidates),
        "future_state_count": future.payload.get("future_state_count", 0),
        "evidence_prediction_count": predictions.payload.get("prediction_count", 0),
        "rfr_assessment_count": rfr_payload.get("assessment_count", 0),
    },
    "warnings": warnings,
    "errors": errors,
}
REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(1 if errors else 0)
