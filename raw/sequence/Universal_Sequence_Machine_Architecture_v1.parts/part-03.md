    │
    │ MACHINE MEANING:
    │ Final identity/lifecycle state of each affected entity at this point.
    │
    │ ALLOWED VALUES:
    │ PERSISTS
    │ MODIFIED
    │ DEGRADED
    │ REPAIRED
    │ TRANSFORMED
    │ SPLIT
    │ MERGED
    │ CONSUMED / INCORPORATED
    │ TERMINATED
    │ NEW_ENTITY_INSTANTIATED
    │ ABSENT
    │ UNKNOWN
    │ NOT_APPLICABLE
    │
    │ IF TRANSFORMED:
    │ explicitly evaluate identity continuity.
    │
    │ MACHINE RULE:
    │ ENTITY OUTCOME ≠ SEQUENCE CLOSURE.
    ↓
[US-33] RESULT SET
    │
    │ MACHINE MEANING:
    │ A transition/Sequence may generate many results simultaneously.
    │
    │ RECORD:
    │ primary_result
    │ side_results
    │ failed_results
    │ new_conditions
    │ new_entities
    │ new_resources
    │ new_capabilities
    │ new_relations
    │ new_knowledge
    │ new_problems
    │ new_rule_candidates
    │ new_sequence_seeds
    ↓
[US-34] EVENT WEIGHT / DOWNSTREAM CRITICALITY
    │
    │ MACHINE MEANING:
    │ Do NOT judge importance only from immediate visible magnitude.
    │ Evaluate whether an event/result becomes critical to later closure.
    │
    │ REQUIRED FIELDS:
    │ - local_effect_magnitude
    │ - affected_scope_now
    │ - downstream_dependency_count
    │ - downstream_dependency_ids
    │ - time_to_activation / latency
    │ - closure_criticality
    │ - counterfactual_necessity_status
    │ - global_scope_effect
    │
    │ CLOSURE CRITICALITY TEST:
    │ "If this event/result is removed from the reconstructed graph,
    │  does the declared end still remain reachable?"
    │
    │ IMPORTANT:
    │ A locally tiny event can have LOW immediate magnitude but HIGH
    │ closure criticality many years later.
    ↓
[US-35] LATENT CONSEQUENCE / EARLY PRECONDITIONING
    │
    │ MACHINE MEANING:
    │ A result can close locally now yet remain stored as a future-active
    │ condition. It does not keep the old Sequence open.
    │
    │ FLOW:
    │ RESULT CREATED
    │     ↓
    │ CREATING SEQUENCE CLOSES
    │     ↓
    │ RESULT PERSISTS AS STATE / RELATION / MEMORY / CONDITION
    │     ↓
    │ TIME + OTHER SEQUENCES PASS
    │     ↓
    │ NEW TRIGGER OCCURS
    │     ↓
    │ DECLARED THRESHOLD BECOMES TRUE
    │     ↓
    │ NEW SEQUENCE OPENS USING THE OLD CLOSED RESULT
    │
    │ EARLY PRECONDITIONING:
    │ A controller intentionally changes a present state because the change is
    │ expected to matter at a later threshold.
    │ This is recorded as an intentional Sequence now + latent result later,
    │ not as an unexplained future event.
    ↓

══════════════════════════════════════════════════════════════════════════════
L. PARALLELISM, CONVERGENCE, SYNCHRONIZATION — CAN OCCUR AT ANY STAGE
══════════════════════════════════════════════════════════════════════════════

GLOBAL / MAIN SEQUENCE
    │
    ├──────── LOCAL / ATTACHED / RIDER SEQUENCE A ────────┐
    ├──────── LOCAL / ATTACHED / RIDER SEQUENCE B ────────┤
    ├──────── LOCAL / ATTACHED / RIDER SEQUENCE C ────────┤
    └──────── EXTERNAL / COUNTER SEQUENCE D ──────────────┤
                                                          ↓
                                                CONVERGENCE WINDOW
                                                          │
                                                          │ MACHINE MEANING:
                                                          │ Multiple sequences,
                                                          │ possibly started at
                                                          │ radically different
                                                          │ times, reach a shared
                                                          │ interaction/execution
                                                          │ region.
                                                          ↓
                                                SYNCHRONIZATION GATE
                                                          │
                                                          │ Required sequences/
                                                          │ states terminal and
                                                          │ accepted?
                                                ┌─────────┴─────────┐
                                                │                   │
                                               NO                  YES
                                                │                   │
                                      BLOCK ONLY DEPENDENT         ↓
                                      TRANSITION                   JOINT EVENT /
                                                                  EXECUTION

SEQUENCE RELATION TYPES THE MACHINE MUST DISTINGUISH:
MAIN / GLOBAL SEQUENCE
    = declared higher-scope Sequence being followed.

LOCAL / CHARACTER / RIDER SEQUENCE
    = an independently meaningful Sequence that runs alongside and intersects
      the Main Sequence but is not merely a task created by a blocked edge.

ATTACHED SEQUENCE
    = created because another Sequence requires a missing result.

NEXT SEQUENCE
    = new Sequence created after a closed result becomes new prior reality.

REFERENCE SEQUENCE
    = new analysis/action Sequence that cites or expands an older CLOSED Sequence
      without reopening it.

COUNTER-SEQUENCE
    = separately identified Sequence whose result opposes/blocks/balances another.

MACHINE RULE:
Do not collapse all these relations into the word "sub-sequence."

══════════════════════════════════════════════════════════════════════════════
M. VERIFICATION, TRACE, MEMORY
══════════════════════════════════════════════════════════════════════════════

[US-36] VERIFICATION / ACCEPTANCE
    │
    │ MACHINE MEANING:
    │ Compare produced result against the specific contract of this Sequence.
    │
    │ RESULT:
    │ SUCCESS
    │ PARTIAL
    │ FAILURE
    │ UNKNOWN
    │ UNAVAILABLE
    │ NOT_APPLICABLE
    │
    │ MACHINE RULE:
    │ Execution completion and result acceptance are different.
    │ A Sequence may close FAILURE while the execution itself was validly completed.
    ↓
[US-37] TRACE
    │
    │ MACHINE MEANING:
    │ Record what persists from the path even when no remembering agent exists.
    │
    │ TRACE TYPES:
    │ physical
    │ dynamical/path-dependent
    │ biological
    │ behavioral
    │ informational
    │ symbolic
    │ technical
    │ institutional
    │ environmental
    │ narrative
    ↓
[US-38] MEMORY
    │
    │ MACHINE MEANING:
    │ Retained path dependence, knowledge, capability, rule, record, or structure
    │ that allows a later Sequence to be influenced by a prior closed path.
    │
    │ MEMORY TYPES:
    │ fact/result memory
    │ path memory
    │ failure memory
    │ context memory
    │ rule memory
    │ procedural/skill memory
    │ physical trace memory
    │ external record
    │ narrative memory
    │ institutional memory
    │ technical memory
    │
    │ MACHINE RULE:
    │ Memory does not require a conscious rememberer.
    ↓
[US-39] MEMORY TRUST / VALIDATION
    │
    │ MACHINE MEANING:
    │ Determine whether the retained memory may be reused under the current scope.
    │
    │ CHECK:
    │ provenance
    │ source quality
    │ confidence
    │ context match
    │ age/version
    │ contradictions
    │ manipulation/contamination
    │ recoverability
    │ scope limitations
    │
    ├── VALID / QUALIFIED
    │      ↓
    │   MAY REUSE
    │
    └── UNRESOLVED
           ↓
       OPEN NEW VALIDATION / RECONSTRUCTION SEQUENCE
           ↓
       CLOSE
           ↓
       RETURN
           ↓
       RE-EVALUATE MEMORY

══════════════════════════════════════════════════════════════════════════════
N. COMPRESSION ↔ EXPANSION
══════════════════════════════════════════════════════════════════════════════

[US-40] COMPRESSION
    │
    │ MACHINE MEANING:
    │ Convert a large closed path into a smaller reusable representation while
    │ explicitly declaring what information is preserved or lost.
    │
    │ COMPRESSED HANDLE MAY BE:
    │ name
    │ rule
    │ procedure
    │ skill
    │ formula
    │ model
    │ narrative
    │ institution
    │ standard
    │ shortcut
    │ validated-path reference
    │
    │ MUST STORE:
    │ - source_sequence_ids
    │ - preserved_invariants
    │ - discarded_or_unavailable_detail
    │ - valid_scope
    │ - assumptions
    │ - known_exceptions
    │ - epistemic_status
    │ - recoverability_grade
    │
    │ RECOVERABILITY GRADE:
    │ LOSSLESS
    │ PARTIAL
    │ LOSSY
    │ IRREVERSIBLE
    │ CURRENTLY_UNRECOVERABLE
    │ CONTEXT_DEPENDENT
    │
    ↕
[US-41] EXPANSION / RECONSTRUCTION
    │
    │ MACHINE MEANING:
    │ Reconstruct as much of the compressed path as evidence/context permits.
    │
    │ MACHINE RULE:
    │ Expansion must NEVER invent missing detail merely to make the graph complete.
    │ Missing detail remains UNKNOWN and may open an investigation Sequence.
    │
    ↓

══════════════════════════════════════════════════════════════════════════════
O. PATTERN, OBSERVER/WRITER, NARRATIVE, LAW
══════════════════════════════════════════════════════════════════════════════

MULTIPLE CLOSED SEQUENCES / CASES
    ↓
[US-42] COMPARISON / PATTERN EXTRACTION
    │
    │ MACHINE MEANING:
    │ Compare CLOSED cases to determine which relations repeat and which are
    │ case-specific.
    │
    │ STORE:
    │ repeated relations
    │ exceptions
    │ context conditions
    │ failed generalizations
    │ confidence
    ↓
[US-43] GENERALIZATION / RULE CANDIDATE
    │
    │ MACHINE MEANING:
    │ Create a candidate reusable rule ONLY from what survived case comparison.
    │
    │ MACHINE RULE:
    │ A candidate rule is not automatically universal or permanent.
    ↓
[US-44] OBSERVER / WRITER / RECORDER SEQUENCE
    │
    │ CONDITIONAL:
    │ Applies when later agents/systems reconstruct and record earlier events.
    │
    │ IMPORTANT:
    │ EVENT SEQUENCE closes first.
    │ RECORDING is a NEW Sequence.
    │
    │ FLOW:
    │ CLOSED EVENT TRACES / MEMORIES
    │     ↓
    │ OBSERVER COLLECTS
    │     ↓
    │ SELECTS
    │     ↓
    │ ORDERS
    │     ↓
    │ COMPARES
    │     ↓
    │ INTERPRETS / REASONS
    │     ↓
    │ RECORDS
    │     ↓
    │ NARRATIVE MEMORY
    │
    │ MACHINE RULE:
    │ WHAT HAPPENED
    │ ≠ WHAT WAS RECORDED
    │ ≠ WHAT A LATER READER INTERPRETS.
    ↓
[US-45] LAW / GUIDANCE / PROCEDURE FORMATION
    │
    │ CONDITIONAL:
    │ Applies when closed cases are transformed into future controls.
    │
    │ FLOW:
    │ CLOSED EVENTS
    │     ↓
    │ CONSEQUENCES
    │     ↓
    │ COMPARISON
    │     ↓
    │ PATTERN
    │     ↓
    │ ABSTRACTION
    │     ↓
    │ COMPROMISE / AGREEMENT / RESTRICTION / PERMISSION /
    │ FUTURE-ACTION CONDITION
    │     ↓
    │ LAW / GUIDANCE / PROCEDURE / STANDARD
    │
    │ MACHINE MEANING:
    │ A law/guidance object is a newly created control object produced from
    │ earlier closed Sequences. It then becomes Prior Reality for later Sequences.
    ↓

══════════════════════════════════════════════════════════════════════════════
P. INHERITANCE / TRANSMISSION
══════════════════════════════════════════════════════════════════════════════

[US-46] INHERITANCE
    │
    │ MACHINE MEANING:
    │ Transfer usable results of a CLOSED Sequence into another Sequence or
    │ future reality without requiring the original execution to remain open.
    │
    │ INHERITANCE TYPES:
    │ physical
    │ biological
    │ individual memory
    │ social
    │ cultural
    │ technical
    │ institutional
    │ informational
    │ structural
    │ mathematical/abstract
    │ path memory
    │
    │ MACHINE RULE:
    │ Higher layers may inherit lower-layer constraints without replacing them.
    ↓

══════════════════════════════════════════════════════════════════════════════
Q. CLOSURE
══════════════════════════════════════════════════════════════════════════════

[US-47] CLOSURE READINESS GATE
    │
    │ MACHINE MEANING:
    │ A Sequence may become terminal only when every requirement of its own
    │ contract is explicitly resolved or explicitly recorded as terminal failure/
    │ unknown/unavailable under that contract.
    │
    │ CHECK ALL:
    │ 1. declared Sequence contract reached a terminal condition
    │ 2. declared closure scope is clear
    │ 3. required result set recorded
    │ 4. verification/acceptance status recorded where applicable
    │ 5. entity outcome recorded separately
    │ 6. every REQUIRED attached Sequence is terminal
    │ 7. every required return is accepted or terminally rejected
    │ 8. required traces/memory recorded
    │ 9. unresolved conditions explicitly recorded
    │ 10. epistemic status of unresolved/unknown links recorded
    │ 11. next-sequence seeds identified
    │
    ├── NOT READY
    │      ↓
    │   DO NOT CLOSE
    │      ↓
    │   IDENTIFY EXACT BLOCKED CONTRACT ITEM
    │      ↓
    │   OPEN REQUIRED ATTACHED SEQUENCE OR CLOSE FAILURE/UNKNOWN IF CONTRACT ALLOWS
    │
    └── READY
           ↓
[US-48] SEQUENCE CLOSURE STATUS
    │
    │ CLOSED_SUCCESS
    │ CLOSED_FAILURE
    │ CLOSED_PARTIAL
    │ CLOSED_UNKNOWN
    │ CLOSED_UNAVAILABLE
    │ CLOSED_NOT_APPLICABLE
    │ CLOSED_ABORTED
    │
    │ MACHINE RULE:
    │ Once CLOSED, this Sequence instance is immutable historical execution.
    │ New evidence NEVER reopens it.
    ↓
[US-49] CLOSURE PACKET
    │
    │ MUST CONTAIN:
    │ sequence_id
    │ sequence_name
    │ closure_scope
    │ closure_status
    │ declared_end_or_target
    │ starting_reality
    │ final_reality
    │ result_set
    │ entity_outcomes
    │ important effects
    │ event_weight_records
    │ attached_sequence_ids + their terminal statuses
    │ verification_status
    │ trace_ids
    │ memory_ids
    │ narrative_memory_ids if any
    │ compression_handles
    │ unresolved_conditions
    │ epistemic_status_summary
    │ inherited_outputs
    │ next_sequence_seeds
    │ prior_sequence_references
    │ controller
    │ carrier(s)
    │
    │ MACHINE RULE:
    │ Closure Packet is the permanent return object.
    ↓
[US-50] RETURN / ARCHIVE ROUTER
    │
    ├── REQUESTING SEQUENCE EXISTS
    │      ↓
    │   RETURN CLOSURE PACKET
    │      ↓
    │   REQUESTING NODE/EDGE RE-EVALUATES
    │
    └── NO REQUESTING SEQUENCE
           ↓
       ROOT SEQUENCE RESULT
           ↓
       ARCHIVE + MEMORY + ENVIRONMENT + INHERITANCE
