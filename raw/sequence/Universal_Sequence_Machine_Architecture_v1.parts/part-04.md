    ↓

══════════════════════════════════════════════════════════════════════════════
R. RESULT MULTIPLICATION → NEW SEQUENCES
══════════════════════════════════════════════════════════════════════════════

CLOSED SEQUENCE S0
    │
    ├── result becomes RESOURCE ─────────────→ create/enable S1
    ├── result becomes MEMORY ───────────────→ later reference S2
    ├── result becomes NEW ENTITY ───────────→ S3
    ├── result changes ENVIRONMENT ──────────→ modifies many later Sequences
    ├── result creates CAPABILITY ───────────→ S4
    ├── result creates RULE / LAW ───────────→ controls later Sequences
    ├── result creates PROBLEM ──────────────→ S5
    ├── result creates OPPORTUNITY ──────────→ S6
    ├── result creates COUNTER-SEQUENCE seed → S7
    ├── result remains LATENT ───────────────→ future threshold → S8
    └── result contributes to ERA TRANSITION → higher-scope Sequence
    │
    ↓
[US-51] NEXT-SEQUENCE SEED
    │
    │ MACHINE MEANING:
    │ A closed result, current reality, memory, new driver, or latent condition
    │ that can legitimately initialize a NEW Sequence instance.
    │
    │ STORE:
    │ seed_id
    │ source_closure_packet_id
    │ seed_content
    │ activation_condition
    │ possible scope
    │ possible controller/carrier
    │ inherited assumptions
    ↓
[US-52] NEW SEQUENCE INSTANCE
    │
    │ NEW sequence_id
    │ references older CLOSED sequence(s)
    │ does NOT reopen them
    │
    └──────────────────────────────→ RETURN TO:
                                     DECLARED / OBSERVED END
                                     + SCOPE / LOCK
                                     + PRIOR REALITY
                                     + UNIVERSAL SEQUENCE AGAIN

══════════════════════════════════════════════════════════════════════════════
S. NO-REOPEN RULE
══════════════════════════════════════════════════════════════════════════════

S0 = CLOSED
    ↓
NEW EVIDENCE / NEW QUESTION / NEW CONDITION
    ↓
CREATE S1
    ↓
S1.reference_sequence_ids = [S0]
    ↓
S1 MAY EXPAND / AUDIT / CHALLENGE / SUPERSEDE / REINTERPRET S0'S RESULT
    ↓
S0 REMAINS HISTORICALLY CLOSED

FORBIDDEN:
S0 CLOSED → "REOPEN S0"

══════════════════════════════════════════════════════════════════════════════
T. COMMON INPUT + UNIQUE HISTORY RULE
══════════════════════════════════════════════════════════════════════════════

COMMON INPUT
    +
COMMON RULE
    +
COMMON TEACHER / ENVIRONMENT / INFORMATION
    ↓
DOES NOT GUARANTEE COMMON RESULT
    ↓
BECAUSE EACH CARRIER MAY HAVE:
    different prior state
    different memory
    different identity
    different relationships
    different pressure
    different commitments
    different knowledge
    different capabilities
    different context
    ↓
CURRENT STATE + UNIQUE PATH HISTORY
    ↓
DIFFERENT THRESHOLD EVALUATION / PRIORITY / SELECTION
    ↓
DIFFERENT RESULT

MACHINE RULE:
Never predict identical behavior solely from identical visible input.

══════════════════════════════════════════════════════════════════════════════
U. ERA / MULTI-SCALE CLOSURE RULE
══════════════════════════════════════════════════════════════════════════════

LOCAL ACTION CLOSES
    ↓
PROMISE / TASK MAY CLOSE
    ↓
PERSON-EVENT SEQUENCE MAY CLOSE
    ↓
PROJECT / WAR / INSTITUTIONAL SEQUENCE MAY CLOSE
    ↓
DYNASTIC / CIVILIZATIONAL SEQUENCE MAY OR MAY NOT CLOSE
    ↓
ERA SEQUENCE MAY OR MAY NOT CLOSE

MACHINE RULE:
Closure is scope-bound.
A battle ending does not automatically close a war.
A war ending does not automatically close an era.
An actor terminating does not automatically close every Sequence that references them.

ERA CLOSURE, when explicitly scoped, means:
required higher-scope old-order conditions are terminal
    +
new reality can no longer be represented as continuation of the declared old-era contract
    ↓
ERA_SEQUENCE = CLOSED
    ↓
results + memory + rules + losses + surviving/new entities + new power/resource conditions
    ↓
become PRIOR REALITY for NEW ERA SEQUENCES

══════════════════════════════════════════════════════════════════════════════
V. MACHINE NODE RECORD — REQUIRED ON EVERY IMPORTANT NODE
══════════════════════════════════════════════════════════════════════════════

THIS IS NOT A SEQUENCE STAGE.
IT IS THE RECORD THE MACHINE MUST MAINTAIN FOR EACH NODE.

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
    required_attached_sequences[]

    relation_ids[]
    interacts_with[]

    controller
    carrier

    driver

    trigger
    threshold
    evaluator
    recheck_condition

    rule_ids[]
    promise_ids[]
    priority_state
    override_record_if_any

    knowledge_view_ids[]
    epistemic_status
    proof_depth

    local_effects[]
    downstream_effects[]
    event_weight_record

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

MACHINE RULE:
No important node is allowed to exist merely as an unexplained word.

══════════════════════════════════════════════════════════════════════════════
W. COMPLETE EXECUTION KERNEL — REPEATED AT EVERY NODE
══════════════════════════════════════════════════════════════════════════════

ENTER NODE
    ↓
LOAD CURRENT STATE + PRIOR REALITY + NODE CONTRACT
    ↓
IDENTIFY DRIVER
    ↓
CHECK TRIGGER
    │
    ├── NOT OCCURRED
    │      ↓
    │   WAIT FOR DECLARED EVENT
    │
    └── OCCURRED
           ↓
       EVALUATE THRESHOLD
           │
           ├── FALSE
           │      ↓
           │   WAIT FOR DECLARED RECHECK CONDITION
           │
           └── TRUE
                  ↓
              CHECK REQUIRED DEPENDENCIES
                  │
                  ├── MISSING / UNACCEPTED
                  │      ↓
                  │   OPEN ATTACHED SEQUENCE(S)
                  │      ↓
                  │   REGISTER IN LEDGER
                  │      ↓
                  │   EXECUTE
                  │      ↓
                  │   CLOSE
                  │      ↓
                  │   RETURN PACKET
                  │      ↓
                  │   RE-EVALUATE THIS NODE
                  │
                  └── READY
                         ↓
                     EXECUTE NODE TRANSITION
                         ↓
                     RECORD STATE CHANGE
                         ↓
                     RECORD ENTITY OUTCOME IF ANY
                         ↓
                     RECORD EFFECT / RESULT / EVENT WEIGHT
                         ↓
                     CAN THIS NODE'S CONTRACT COMPLETE?
                         │
                         ├── NO
                         │      ↓
                         │   IDENTIFY EXACT MISSING RESULT
                         │      ↓
                         │   OPEN NEW ATTACHED SEQUENCE
                         │      ↓
                         │   CLOSE + RETURN + RE-EVALUATE
                         │
                         └── YES
                                ↓
                            MARK NODE COMPLETE
                                ↓
                            FIRE NEXT LEGAL EDGE

NO:
"FAIL → SAME LOOP FOREVER"

YES:
ATTEMPT S1 closes
    ↓
NEW repair/investigation S2 closes
    ↓
NEW retest S3 closes
    ↓
parent node receives terminal returns
    ↓
parent node continues or closes terminally

══════════════════════════════════════════════════════════════════════════════
X. FINAL UNIVERSAL COMPRESSION
══════════════════════════════════════════════════════════════════════════════

DECLARED END / RESULT
    ↑
REVERSE-MINE REQUIRED REALITY
    ↑
LOCK SCOPE + IDENTITY + CLOSURE SCOPE
    ↑
FIND PRIOR REALITY / PROVENANCE / SEEDS
    │
    ↓
FORMATION TYPE
    ↓
ENVIRONMENT / FORMATION / EXISTENCE
    ↓
CURRENT STATE / COHERENCE / RELATIONS
    ↓
KNOWLEDGE DISTRIBUTION [IF APPLICABLE]
    ↓
DRIVER
    ↓
CONTROLLER + CARRIER
    ↓
REPRESENTED FUTURE [IF APPLICABLE]
    ↓
RULE / PROMISE / PRIORITY / CONSTRAINTS [IF APPLICABLE]
    ↓
TRIGGER
    ↓
THRESHOLD
    ↓
DEPENDENCY GRAPH
    ↓
LOCAL BARRIER
    ↓
ATTACHED SEQUENCES AS REQUIRED
    ↓
ALL REQUIRED RETURNS ACCEPTED
    ↓
AVAILABILITY
    ↓
ADMISSIBILITY
    ↓
TEST / EVIDENCE [IF REQUIRED]
    ↓
ALTERNATIVES / COUNTER-SEQUENCES
    ↓
SELECTION [IF APPLICABLE]
    ↓
ENCOUNTER / ACCESS [IF NEEDED]
    ↓
COUPLING / INTERACTION
    ↓
TRANSFORMATION [IF NEEDED]
    ↓
DYNAMICS
    ↓
INCORPORATION [IF APPLICABLE]
    ↓
EFFECT / ACTION / OUTPUT
    ↓
STATE CHANGE
    ↓
ENTITY OUTCOME
    ↓
RESULT SET
    ↓
EVENT WEIGHT / DOWNSTREAM CRITICALITY
    ↓
LATENT CONSEQUENCES / FUTURE SEEDS
    ↓
CONVERGENCE / SYNCHRONIZATION [WHERE REQUIRED]
    ↓
VERIFICATION / ACCEPTANCE
    ↓
TRACE
    ↓
MEMORY
    ↓
MEMORY VALIDATION
    ↓
COMPRESSION ↔ EXPANSION
    ↓
PATTERN / GENERALIZATION [IF MULTIPLE CASES]
    ↓
OBSERVER / WRITER SEQUENCE [IF RECORDING OCCURS]
    ↓
LAW / GUIDANCE / PROCEDURE FORMATION [IF PRODUCED]
    ↓
INHERITANCE / TRANSMISSION
    ↓
CLOSURE READINESS GATE
    ↓
SEQUENCE CLOSURE STATUS
    ↓
CLOSURE PACKET
    ↓
RETURN / ARCHIVE
    ↓
RESULT MULTIPLICATION
    ↓
NEXT-SEQUENCE SEEDS
    ↓
NEW SEQUENCE INSTANCE
    ↓
NEVER REOPEN OLD CLOSED INSTANCE
    ↓
PASS 3: END → START AGAIN
    ↓
IF NO REQUIRED UNCONNECTED DOT REMAINS:
STRUCTURALLY CLOSED

══════════════════════════════════════════════════════════════════════════════
END OF UNIVERSAL SEQUENCE MACHINE ARCHITECTURE
══════════════════════════════════════════════════════════════════════════════
