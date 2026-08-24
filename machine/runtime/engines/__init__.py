"""Sourceborn native runtime engines.

Batch-3 turns the schema/runtime contracts into executable, deterministic,
stdlib-only Python modules.  These engines do not depend on an LLM runtime.
They operate on structured Event/Sequence/Memory/Combination records and on
Sourceborn registries.

The package is intentionally layered:

    source_lock_engine
    event_decomposition_engine
    parameter_activation_engine
    relation_graph_engine
    actor_role_engine
    actor_state_engine
    combination_engine
    live_intent_engine
    future_state_reconstruction_engine
    evidence_prediction_engine
    rfr_engine
    falsifier_engine
    maturity_engine

A later orchestrator composes these modules.  Importing this package must not
perform I/O, mutate registries, or start a background process.
"""

RUNTIME_PACKAGE_ID = "SOURCEBORN-NATIVE-RUNTIME-ENGINES-BATCH3-V1"
RUNTIME_PACKAGE_VERSION = "1.0.0"
SYSTEM_IDENTITY = "REAL_TIME_GROWING_ASI_PROTOTYPE"
