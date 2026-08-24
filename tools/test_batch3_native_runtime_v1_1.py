#!/usr/bin/env python3
"""Deterministic integration/R-F-R test for Sourceborn Batch-3 V1.1.

V1.1 corrects the fixture vocabulary from V1 so the registry-grounded matcher
has explicit source-token overlap.  The runtime matcher is not weakened and no
IDs are invented to make the test pass.
"""
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
REPORT_PATH = GEN / "P2_BATCH3_NATIVE_RUNTIME_RFR_V1_1.json"

errors: list[str] = []
warnings: list[str] = []

# ---------------------------------------------------------------------------
# A. Compile every Batch-3 runtime module.
# ---------------------------------------------------------------------------
engine_dir = ROOT / "machine/runtime/engines"
engine_files = sorted(p for p in engine_dir.glob("*.py") if p.is_file())
compile_failures: list[str] = []
for path in engine_files:
    try:
        py_compile.compile(str(path), doraise=True)
    except Exception as exc:
        compile_failures.append(f"{path.name}:{exc}")
if compile_failures:
    errors.extend("compile:" + item for item in compile_failures)

# ---------------------------------------------------------------------------
# B. Source lock + Event decomposition.
# ---------------------------------------------------------------------------
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
if event and event.get("intent", {}).get("intent_type") != "NOT_YET_DECODED":
    errors.append("Event decomposition inferred Intent before Intent engine")
if event and event.get("observations", [{}])[0].get("value") != text:
    errors.append("Event decomposition changed source text")

# ---------------------------------------------------------------------------
# C. Controlled registry activation. Vocabulary deliberately overlaps the Event.
# ---------------------------------------------------------------------------
index = RegistryIndex()
index.add_document("fixture/human.json", {
    "containers": [
        {
            "container_id": "CON-063",
            "exact_name": "Intent Formation and Commitment",
            "definition": "commissioner intended future commitment action order and record",
        },
        {
            "container_id": "CON-080",
            "exact_name": "External Cognition, Institutions and Collective Intelligence",
            "definition": "scribe writing record dedication temple audience distributed memory",
        },
    ]
})
index.add_document("fixture/ai.json", {
    "functions": [
        {"id": "AI-17", "name": "Verification", "definition": "record dedication verification evidence checking"},
        {"id": "AI-22", "name": "Communication", "definition": "scribe record communication temple audience information"},
    ]
})
index.add_document("fixture/asi.json", {
    "governance": [
        {"id": "ASI-02", "name": "Truth Provenance Governance", "definition": "record source provenance dedication truth"},
        {"id": "ASI-08", "name": "Safety Permission Authority", "definition": "commissioner ordered authority control permission"},
    ]
})

activation = activate_event(
    event,
    index,
    min_score=0.04,
    primary_threshold=0.14,
    secondary_threshold=0.08,
    limit_per_type=8,
)
working_event = apply_activations_to_event(event, activation)
activation_refs = activation.payload.get("activation_refs", [])
activation_ids = {a.get("object_id") for a in activation_refs}
activation_domains = {a.get("object_type") for a in activation_refs}
if not activation_refs:
    errors.append("controlled registry produced no activations")
for required in {"CON-063", "CON-080", "AI-22", "ASI-08"}:
    if required not in activation_ids:
        errors.append(f"expected controlled activation missing:{required}")
if not {"HUMAN_CONTAINER", "AI_FUNCTION", "ASI_GOVERNANCE"}.issubset(activation_domains):
    errors.append(f"cross-domain activation incomplete:{sorted(activation_domains)}")
if any(str(a.get("object_id", "")).startswith(("SB-ASI-P", "SB-HFR-P")) for a in activation_refs):
    errors.append("activation engine invented atomic Human parameter ID")

# ---------------------------------------------------------------------------
# D. Actor-role separation.
# ---------------------------------------------------------------------------
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
expected_role_pairs = {
    ("ACT-COMMISSIONER", "REQUESTER"),
    ("ACT-COMMISSIONER", "CONTROLLER"),
    ("ACT-SCRIBE", "PERFORMER"),
    ("ACT-SCRIBE", "WRITER"),
    ("ACT-TEMPLE-AUDIENCE", "AUDIENCE"),
}
for expected in expected_role_pairs:
    if expected not in role_pairs:
        errors.append(f"actor-role separation missing {expected}")

# Explicit future state is source-stated by the second sentence of this fixture.
working_event["state_refs"] = [{
    "state_id": "STATE-RECORD-AVAILABLE",
    "state_role": "EXPECTED_FUTURE_STATE",
    "entity_ref": "OBJ-DEDICATION-RECORD",
    "state_payload": {"availability": "PERSISTS_AFTER_CEREMONY"},
    "source_refs": [event["source_refs"][0]["source_id"]],
    "epistemic_status": "SOURCE_STATED",
}]
working_event["object_ids"] = ["OBJ-DEDICATION-RECORD"]

# ---------------------------------------------------------------------------
# E. Same identity, multiple actor-state branches.
# ---------------------------------------------------------------------------
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
states = build_actor_state_hypotheses(
    working_event,
    working_event["actor_roles"],
    scenario_variants=scenario_variants,
)
all_states = states.payload.get("actor_state_hypotheses", [])
commissioner_states = [s for s in all_states if s.get("actor_ref") == "ACT-COMMISSIONER"]
if len(commissioner_states) < 3:
    errors.append("same actor did not receive base + two scenario states")
if any(s.get("identity_ref") != "ACT-COMMISSIONER" for s in commissioner_states):
    errors.append("actor state branching split actor identity")

# ---------------------------------------------------------------------------
# F. Relation graph + six-mode bounded combination engine.
# ---------------------------------------------------------------------------
relations = build_event_relation_graph(working_event)
if relations.payload.get("identity_merges") != 0:
    errors.append("relation graph performed identity merge")
if not relations.payload.get("relations"):
    errors.append("relation graph produced no structural edges")

pattern_priors = [{"pattern_id": "PC-SYN-RECORD-PERSISTENCE", "epistemic_status": "GENERATED_TEST_FIXTURE"}]
memory_priors = [{"memory_id": "MEM-SYN-PRIOR-001", "epistemic_status": "GENERATED_TEST_FIXTURE"}]
combos = generate_combinations(
    working_event,
    relations=relations.payload.get("relations", []),
    actor_states=all_states,
    pattern_priors=pattern_priors,
    memory_priors=memory_priors,
    max_candidates=36,
    max_candidates_per_mode=8,
)
combo_counts = combos.payload.get("counts_by_mode", {})
if combos.payload.get("cartesian_product_performed") is not False:
    errors.append("combination engine performed or claimed Cartesian generation")
if combos.payload.get("combination_count", 0) == 0:
    errors.append("combination engine produced no candidate")
if combo_counts.get("COUNTERFACTUAL", 0) == 0:
    errors.append("counterfactual actor-state combinations missing")
if combo_counts.get("CROSS_DOMAIN", 0) == 0:
    errors.append("Human+AI+ASI cross-domain combination missing")
if combo_counts.get("PATTERN_SUPPORTED", 0) == 0:
    errors.append("pattern-supported combination missing")
if combo_counts.get("NOVELTY", 0) == 0:
    errors.append("memory+current novelty combination missing")

# ---------------------------------------------------------------------------
# G. Live Intent novelty, future state and evidence predictions.
# ---------------------------------------------------------------------------
intents = generate_live_intents(
    working_event,
    working_event["actor_roles"],
    actor_states=all_states,
    combination_records=combos.payload.get("combination_records", []),
)
intent_candidates = intents.payload.get("intent_candidates", [])
if not intent_candidates:
    errors.append("live Intent engine produced no candidate")
if any(i.get("stated_motive") is not None for i in intent_candidates):
    errors.append("inferred live Intent populated stated_motive")

intents_repeat = generate_live_intents(
    working_event,
    working_event["actor_roles"],
    actor_states=all_states,
    combination_records=combos.payload.get("combination_records", []),
    existing_intents=intent_candidates,
)
if intents_repeat.payload.get("new_intent_structure_count", 0) != 0:
    errors.append("second identical structural pass inflated Intent count")

future = reconstruct_future_states(working_event, intent_candidates=intent_candidates)
future_states = future.payload.get("future_state_candidates", [])
if not future_states:
    errors.append("future-state engine produced no candidate")

predictions = generate_evidence_predictions(
    working_event,
    intent_candidates=intent_candidates,
    future_states=future_states,
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

# ---------------------------------------------------------------------------
# H. Full orchestration: untested hypotheses must remain open/low-maturity.
# ---------------------------------------------------------------------------
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
        "epistemic_status": "NEW_SYNTHETIC",
        "proof_debt": ["FIXTURE_ONLY"],
    }],
    evidence_results={},
)
required_stages = {
    "activation", "actor_roles", "actor_states", "relation_graph", "combinations",
    "live_intents", "future_states", "evidence_predictions", "rfr", "falsifiers", "maturity",
}
missing_stages = required_stages - set(run.get("stages", {}))
if missing_stages:
    errors.append(f"orchestrator missing stages:{sorted(missing_stages)}")
if run.get("writeback_boundary", {}).get("automatic_persistent_writes_performed") != 0:
    errors.append("Batch-3 performed persistent writes")
if run.get("writeback_boundary", {}).get("status") != "NOT_IMPLEMENTED_IN_BATCH3":
    errors.append("Batch-3 did not preserve explicit Batch-4 writeback boundary")

rfr_payload = run.get("stages", {}).get("rfr", {}).get("payload", {})
if rfr_payload.get("assessment_count", 0) == 0:
    errors.append("R-F-R assessed no hypotheses")
if rfr_payload.get("open_count", 0) == 0 and rfr_payload.get("weaken_or_reject_count", 0) == 0 and rfr_payload.get("fail_count", 0) == 0:
    errors.append("untested hypotheses appear to have auto-passed R-F-R")

maturities = [
    item.get("payload", {}).get("maturity")
    for item in run.get("stages", {}).get("maturity", {}).values()
    if isinstance(item, dict)
]
if "M5" in maturities:
    errors.append("untested synthetic fixture auto-promoted to M5")

# ---------------------------------------------------------------------------
# Report.
# ---------------------------------------------------------------------------
report = {
    "report_id": "P2-BATCH3-NATIVE-RUNTIME-RFR-V1-1",
    "status": "PASS" if not errors else "FAIL",
    "system_identity": "REAL_TIME_GROWING_ASI_PROTOTYPE",
    "runtime_package": "SOURCEBORN-NATIVE-RUNTIME-ENGINES-BATCH3-V1",
    "fixture_sequence_id": sequence_id,
    "supersedes_fixture_test": "P2-BATCH3-NATIVE-RUNTIME-RFR-V1",
    "checks": {
        "all_engine_files_compile": not compile_failures,
        "source_lock_pass": source.status == "COMPLETE",
        "source_text_preserved": bool(event) and event.get("observations", [{}])[0].get("value") == text,
        "Intent_not_invented_during_decomposition": bool(event) and event.get("intent", {}).get("intent_type") == "NOT_YET_DECODED",
        "registry_activation_present": bool(activation_refs),
        "Human_AI_ASI_activation_present": {"HUMAN_CONTAINER", "AI_FUNCTION", "ASI_GOVERNANCE"}.issubset(activation_domains),
        "no_atomic_Human_ID_invention": not any(str(a.get("object_id", "")).startswith(("SB-ASI-P", "SB-HFR-P")) for a in activation_refs),
        "actor_roles_separated": expected_role_pairs.issubset(role_pairs),
        "same_actor_multiple_states": len(commissioner_states) >= 3,
        "actor_identity_preserved": all(s.get("identity_ref") == "ACT-COMMISSIONER" for s in commissioner_states),
        "relation_graph_no_identity_merge": relations.payload.get("identity_merges") == 0,
        "bounded_combinations": combos.payload.get("cartesian_product_performed") is False,
        "counterfactual_combinations": combo_counts.get("COUNTERFACTUAL", 0) > 0,
        "cross_domain_combinations": combo_counts.get("CROSS_DOMAIN", 0) > 0,
        "pattern_combinations": combo_counts.get("PATTERN_SUPPORTED", 0) > 0,
        "novelty_combinations": combo_counts.get("NOVELTY", 0) > 0,
        "live_intents_present": bool(intent_candidates),
        "Intent_motive_separated": not any(i.get("stated_motive") is not None for i in intent_candidates),
        "new_wording_not_new_Intent": intents_repeat.payload.get("new_intent_structure_count", 0) == 0,
        "future_state_candidates_present": bool(future_states),
        "evidence_predictions_present": predictions.payload.get("prediction_count", 0) > 0,
        "RFR_present": rfr_payload.get("assessment_count", 0) > 0,
        "untested_hypotheses_not_auto_passed": not (rfr_payload.get("open_count", 0) == 0 and rfr_payload.get("weaken_or_reject_count", 0) == 0 and rfr_payload.get("fail_count", 0) == 0),
        "untested_synthetic_not_M5": "M5" not in maturities,
        "persistent_writeback_zero": run.get("writeback_boundary", {}).get("automatic_persistent_writes_performed") == 0,
    },
    "counts": {
        "engine_python_file_count": len(engine_files),
        "activation_count": len(activation_refs),
        "actor_role_count": len(role_pairs),
        "actor_state_count": len(all_states),
        "commissioner_state_count": len(commissioner_states),
        "relation_count": len(relations.payload.get("relations", [])),
        "combination_count": combos.payload.get("combination_count", 0),
        "combination_counts_by_mode": combo_counts,
        "live_intent_count": len(intent_candidates),
        "future_state_count": len(future_states),
        "evidence_prediction_count": predictions.payload.get("prediction_count", 0),
        "RFR_assessment_count": rfr_payload.get("assessment_count", 0),
        "persistent_write_count": run.get("writeback_boundary", {}).get("automatic_persistent_writes_performed"),
    },
    "warnings": warnings,
    "errors": errors,
}
REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(1 if errors else 0)
