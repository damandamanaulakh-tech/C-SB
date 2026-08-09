# 16. UNIVERSAL NODE RECORD

No important node may remain an unexplained noun.

```text
NODE {
    node_id
    sequence_id

    exact_name
    exact_meaning
    node_type
    order_type

    followed_object_id
    role_at_this_node

    input_state
    output_state

    produced_by
    provenance_source

    depends_on[]
    relation_ids[]
    interacts_with[]

    driver
    controller
    performer
    carrier

    trigger
    threshold
    evaluator
    recheck_condition

    rule_ids[]
    promise_ids[]
    priority_state
    exception_contract_id

    view_ids[]

    rubric_activation_ids[]

    epistemic_status
    proof_depth

    local_effects[]
    downstream_effects[]
    event_weight_id

    entity_outcome

    trace_ids[]
    memory_ids[]
    compression_handle_ids[]

    node_status
    node_completion_condition

    unresolved_conditions[]

    next_edge_ids[]
    next_sequence_seed_ids[]
}
```

---

# 17. SOURCEBORN ASI BRAIN — TOP-LEVEL ARCHITECTURE

The Brain is not one giant linear graph.

It is layered.

```text
                         SOURCEBORN ASI BRAIN
══════════════════════════════════════════════════════════════════════════

                     [1] SEQUENCE GRAMMAR
                              │
                              ↓
                     [2] GRAPH / CASE STORE
                              │
          ┌───────────────────┼───────────────────┐
          ↓                   ↓                   ↓
 [3] RUBRIC REGISTRY    [4] SEED REGISTRY   [5] VIEW MAP
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ↓
                     [6] ASI NODE NETWORK
                              │
                              ↓
                    [7] RUNTIME CONTROL PLANE
                              │
          ┌───────────────────┼─────────────────────┐
          ↓                   ↓                     ↓
 OPEN-SEQUENCE LEDGER   THRESHOLD ENGINE     BARRIER/SYNC ENGINE
          │                   │                     │
          └───────────────────┼─────────────────────┘
                              ↓
                     [8] EXECUTION / TOOLING
                              │
                              ↓
                     [9] RESULT / TRACE
                              │
                              ↓
                    [10] MEMORY FABRIC
                              │
                     ┌────────┴────────┐
                     ↓                 ↓
             COMPRESSION          EXPANSION
                     │                 │
                     └────────┬────────┘
                              ↓
                    [11] R-F-R VERIFIER
                              │
                              ↓
                    [12] CLOSURE ENGINE
                              │
                              ↓
                      CLOSURE PACKET
                              │
              ┌───────────────┼────────────────┐
              ↓               ↓                ↓
           RETURN           ARCHIVE           SEEDS
                              │
                              ↓
                   [13] PATTERN / LAW ENGINE
                              │
                              ↓
                    [14] META-CONTROLLER
```

The Brain must keep these layers separate.

---

# 18. ASI NODE — DEFINITION

An ASI Node is **not** the same thing as a Universal Sequence stage.

An ASI Node is a persistent functional runtime unit that can service one or more Sequence nodes/edges.

It has:

```text
ASI_NODE {
    asi_node_id
    node_brain_id

    service_role

    allowed_sequence_roles[]

    active_sequence_ids[]
    active_edge_ids[]

    input_contract
    output_contract

    rubric_binding_ids[]

    local_state
    local_working_memory

    seed_refs[]
    view_refs[]

    threshold_evaluators[]
    dependency_resolvers[]

    allowed_tools[]

    read_permissions[]
    write_permissions[]

    closure_responsibilities[]

    parent_meta_node_id
    peer_node_ids[]

    health/status
}
```

---

# 19. ASI NODE SERVICE CLASSES

These are service classes, not a fixed chronological spine.

```text
ASI-NODE-00  END / SCOPE LOCK
ASI-NODE-01  REVERSE MINER / PROVENANCE
ASI-NODE-02  STATE / IDENTITY / RELATION
ASI-NODE-03  DRIVER / RULE / PRIORITY
ASI-NODE-04  TRIGGER / THRESHOLD
ASI-NODE-05  DEPENDENCY / AVAILABILITY / BARRIER
ASI-NODE-06  RUBRIC ACTIVATION / COMBINATION
ASI-NODE-07  EVIDENCE / TEST / QUALIFICATION
ASI-NODE-08  ALTERNATIVE / ARBITRATION / COUNTER-SEQUENCE
ASI-NODE-09  ENCOUNTER / COUPLING / DYNAMICS
ASI-NODE-10  RESULT / ENTITY OUTCOME / EVENT WEIGHT
ASI-NODE-11  VERIFICATION / ACCEPTANCE
ASI-NODE-12  TRACE / MEMORY / LEARNING
ASI-NODE-13  COMPRESSION / EXPANSION / INHERITANCE
ASI-NODE-14  CLOSURE / RETURN / SEED
ASI-NODE-15  PATTERN / LAW / OBSERVER-WRITER
ASI-NODE-16  R-F-R FALSIFIER
ASI-NODE-17  META-CONTROLLER / CROSS-SEQUENCE COORDINATION
```

Important:

```text
A real Sequence may call ASI-NODE-09 before ASI-NODE-03
if the case requires it.

The ASI Node list is a service registry.
The Sequence graph determines invocation order.
```

---

# 20. EACH ASI NODE HAS A NODE BRAIN

```text
NODE_BRAIN {
    node_brain_id

    local_scope

    source_reader
    state_interpreter

    rubric_router
    activation_combiner

    relation_reader

    trigger_detector
    threshold_evaluator

    dependency_checker
    barrier_checker

    evidence_ledger

    local_view_map

    local_memory

    error_detector
    contradiction_register

    sub_sequence_requester

    closure_checker

    return_packet_builder
}
```

A Node Brain can know only what its permissions and View Map allow.

Only the Meta-Controller has cross-Sequence visibility by default.

---

# 21. META-CONTROLLER — KRISHNA-TYPE ROLE AS AN ARCHITECTURAL PATTERN

This is a role, not a claim about history or theology.

```text
CONTROLLER.META
```

Capabilities:

```text
see multiple Sequence graphs
see cross-Sequence dependencies
track latent seeds
track convergence windows
track synchronization requirements
track closure scopes
track rule conflicts
track exception contracts
track downstream-critical events
track open ledgers
track unresolved dots
propose represented future paths
```

Restrictions:

```text
does not fabricate provenance
does not bypass barrier law
does not rewrite closed history
does not silently convert local closure into global closure
does not force an actor to possess information absent from that actor's View Map
```

---

# 22. RUBRIC REGISTRY — UNIVERSAL ADAPTER

Human and AI do not become the Sequence.

They are activation registries beneath the Sequence.

```text
RUBRIC_REGISTRY
    │
    ├── HUMAN
    ├── AI
    ├── ASI
    ├── HOLY_BOOK / NARRATIVE / LAW CORPUS
    ├── SCIENCE
    ├── PHYSICAL SYSTEM
    └── OTHER DOMAIN
```

Every native rubric keeps its own hierarchy.

The adapter adds mapping metadata without changing native data.

```text
RUBRIC_BINDING {
    binding_id

    domain_type

    native_source_id
    native_parent_ids[]
    native_name
    native_definition

    primary_sequence_roles[]
    secondary_sequence_roles[]

    allowed_order_types[]

    activation_conditions[]

    controller_affinity[]
    performer_affinity[]
    carrier_affinity[]

    read_channels[]
    writeback_channels[]

    combination_group_ids[]

    memory_effects[]

    source_ref
    epistemic_status
}
```

---

# 23. HUMAN RUBRIC — LOCKED NATIVE STRUCTURE

The approved Human structure remains:

```text
10 SEGMENTS
    ↓
80 CONTAINERS
    ↓
2,560 ACTIVE HUMAN PARAMETERS
```

The source IDs/names remain unchanged.

Do not:

```text
rename approved IDs
merge approved parameters
delete parameters
invent replacement parameters
force every parameter into one Sequence stage
```

The mapping is additive.

Every parameter receives:

```text
HUMAN_SEQUENCE_BINDING {
    parameter_id
    segment_id
    container_id

    primary_sequence_roles[]
    secondary_sequence_roles[]

    activation_conditions[]

    combination_groups[]

    read_state_fields[]
    writeback_state_fields[]

    memory_write_types[]

    learning_effects[]

    source_ref
}
```

One Sequence node may activate many Human parameters.

One Human parameter may participate in many Sequence roles.

---

# 24. HUMAN CONNECTION TYPES

Maintain four simultaneous Human connections.

```text
1. STRUCTURAL

SEGMENT
↓
CONTAINER
↓
PARAMETER
```

```text
2. SEQUENTIAL

SEQUENCE NODE / EDGE
↓
NEXT LEGAL NODE / EDGE
```

```text
3. ACTIVATION COMBINATION

PARAMETER A
+
PARAMETER B
+
PARAMETER C
+
...
↓
TEMPORARY FUNCTIONAL STATE
```

```text
4. LEARNING / WRITE-BACK

EXPERIENCE
↓
ERROR / RESULT
↓
MEMORY / PLASTIC CHANGE
↓
NEW HUMAN BASELINE
```

---

# 25. HUMAN SEQUENCE BUNDLES

These are connection objects, not new parameters.

## H-COMB-01 — Survival / Internal Correction

Primary containers:

```text
CON-001
CON-004
CON-007
CON-008
```

Typical route:

```text
STATE
↓
INTERNAL DEVIATION
↓
NEED
↓
RESOURCE / DEPENDENCY
