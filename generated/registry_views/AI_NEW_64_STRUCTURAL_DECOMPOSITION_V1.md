# AI-NEW-001..064 Structural Decomposition V1

Source IDs/names/levels are preserved. Structural and ownership fields are additive.

- Records: 64
- runtime_form_counts: `{"CONTROL": 14, "EVIDENCE_CONTROL": 7, "FILTER": 19, "MECHANISM": 19, "META_CONTROL": 3, "STATE": 1, "STATE_OR_MECHANISM_MIXED": 1}`
- atomicity_counts: `{"ATOMIC_AT_APPROVED_SOURCE_SCOPE": 53, "COMPOSITE_CANDIDATE": 11}`
- ownership_counts: `{"AI_EVIDENCE_MECHANISM_WITH_ASI_PROVENANCE_GOVERNANCE": 7, "AI_FILTER_WITH_ASI_ACCEPTANCE_INTERFACE": 19, "AI_PRIMARY": 6, "AI_PRIMARY_WITH_ASI_GOVERNANCE_INTERFACE": 13, "AI_RUNTIME_STATE_OR_MECHANISM_UNDER_EXPLICIT_CALL_CONTRACT": 1, "AI_RUNTIME_STATE_UNDER_ASI_POLICY": 1, "SHARED_AI_ASI_CONTROL": 14, "SHARED_AI_ASI_META_CONTROL": 3}`
- engine_binding_counts: `{"ENGINE_BINDING_OPEN_NO_EXACT_SOURCE_RELATION": 64}`
- governance_patch_count: `7`

## Composite candidates

- **AI-NEW-002 Context compression and semantic retention** → CONTEXT_COMPRESSION, SEMANTIC_RETENTION
- **AI-NEW-009 Cache invalidation and freshness control** → CACHE_INVALIDATION, FRESHNESS_CONTROL
- **AI-NEW-011 Tool selection and authorization** → TOOL_SELECTION, TOOL_AUTHORIZATION
- **AI-NEW-014 Tool retry and recovery policy** → TOOL_RETRY_POLICY, TOOL_RECOVERY_POLICY
- **AI-NEW-026 Agent interruption and rollback** → AGENT_INTERRUPTION, ROLLBACK
- **AI-NEW-029 File-transfer and marker verification** → FILE_TRANSFER_CONTROL, MARKER_VERIFICATION
- **AI-NEW-052 Record-integrity and custody ledger** → RECORD_INTEGRITY, CUSTODY_LEDGER
- **AI-NEW-055 Latency and time-to-first-token monitoring** → LATENCY_MONITORING, TIME_TO_FIRST_TOKEN_MONITORING
- **AI-NEW-058 API-error interpretation and recovery** → API_ERROR_INTERPRETATION, RECOVERY
- **AI-NEW-063 Versioned parameter and evidence updating** → VERSIONED_PARAMETER_UPDATE, VERSIONED_EVIDENCE_UPDATE
- **AI-NEW-064 Production rollback and recovery** → PRODUCTION_ROLLBACK, RECOVERY

## Engine binding

Direct Engine IDs are emitted only when an exact AI-NEW reference is found in a source-derived Engine relationship registry. Name similarity is not used.
