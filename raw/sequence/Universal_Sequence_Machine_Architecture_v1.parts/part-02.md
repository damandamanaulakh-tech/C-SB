    │ - closure condition
    │
    │ MACHINE RULE:
    │ An override does not delete the normal rule.
    ↓

══════════════════════════════════════════════════════════════════════════════
E. UNIVERSAL EDGE FIRING LAW — APPLIES BETWEEN EVERY EXECUTABLE NODE
══════════════════════════════════════════════════════════════════════════════

SOURCE NODE / STATE
    ↓
TRIGGER / ACTIVATION EVENT
    │
    │ MACHINE MEANING:
    │ Something changed, arrived, was observed, became due, or was returned.
    ↓
THRESHOLD EVALUATION
    │
    │ MACHINE MEANING:
    │ The explicit condition that must be true before this edge may fire.
    │
    │ THRESHOLD TYPES:
    │ VALUE
    │ RANGE
    │ TIME
    │ EVENT
    │ COUNT / QUORUM
    │ CONFIDENCE / PROOF
    │ STATE
    │ ABSENCE
    │ PROMISE MATCH
    │ PRIORITY CONFLICT RESOLUTION
    │ COMPOSITE: A AND B / A OR B / A UNLESS C / other declared logic
    │
    │ REQUIRED FIELDS:
    │ - activation_event
    │ - threshold_condition
    │ - evaluator
    │ - evaluation_time
    │ - recheck_condition
    │ - status
    │
    ├── THRESHOLD FALSE
    │      ↓
    │   EDGE DOES NOT FIRE
    │      ↓
    │   WAIT ONLY FOR DECLARED RECHECK CONDITION
    │
    └── THRESHOLD TRUE
           ↓
       CHECK REQUIRED DEPENDENCIES
           ↓
       EDGE MAY FIRE ONLY IF LOCAL BARRIER IS CLEARED

MACHINE RULE:
TRIGGER ≠ THRESHOLD.
A condition may exist for years and never activate until the declared trigger
and threshold relationship is satisfied.

══════════════════════════════════════════════════════════════════════════════
F. DEPENDENCY AND ATTACHED-SEQUENCE ENGINE
══════════════════════════════════════════════════════════════════════════════

[US-17] DEPENDENCY GRAPH
    │
    │ MACHINE MEANING:
    │ Enumerate everything that MUST / MAY / ALTERNATIVELY be true before the
    │ next transition can legally execute.
    │
    │ DEPENDENCY TYPES:
    │ resource
    │ condition
    │ capability
    │ information
    │ infrastructure
    │ other entity
    │ permission
    │ location
    │ timing
    │ prior closed Sequence result
    │ validated memory
    │ other declared type
    │
    │ STORE EACH DEPENDENCY AS:
    │ - dependency_id
    │ - required / optional
    │ - alternatives
    │ - acceptance_condition
    │ - provenance
    │ - availability_status
    │ - epistemic_status
    ↓
[US-18] LOCAL DEPENDENCY BARRIER
    │
    │ QUESTION:
    │ Are all dependencies required for THIS EDGE accepted and terminal?
    │
    ├── YES
    │      ↓
    │   CONTINUE
    │
    └── NO
           ↓
       SUSPEND ONLY THE DEPENDENT EDGE
           ↓
       CREATE ATTACHED SEQUENCE(S)
           ↓
       EACH ATTACHED SEQUENCE RUNS THIS ENTIRE UNIVERSAL GRAMMAR
           ↓
       EACH ATTACHED SEQUENCE CLOSES
           ↓
       CLOSURE PACKET RETURNS
           ↓
       DEPENDENCY ACCEPTANCE RE-EVALUATED

ATTACHED SEQUENCE — MACHINE MEANING:
A complete separately identified Sequence opened because another Sequence
requires a result that does not yet exist or is not yet accepted.

ATTACHED SEQUENCE IS NOT:
- an unfinished loop inside the same Sequence
- automatically younger than the Main Sequence
- automatically less important
- automatically later in absolute time

ATTACHED SEQUENCE CONTRACT MUST STORE:
- attached_sequence_id
- requesting_sequence_id
- requesting_node_or_edge
- reason
- requested_result
- return_schema
- scope
- context_snapshot
- controller
- carrier if known
- activation_condition
- close_condition
- acceptance_condition
- required_or_optional
- epistemic_requirement
- proof_depth
- dependencies
- deadline / time condition
- termination_policy

CRITICAL MACHINE RULE:
CLOSE CONDITION ≠ ACCEPTANCE CONDITION.

EXAMPLE OF LOGIC:
SEARCH SEQUENCE closes SUCCESS because the search finished.
SEARCH RESULT = NOT FOUND.
PARENT acceptance = FALSE.
Therefore the parent opens a DIFFERENT attached Sequence
(build / substitute / reduce requirement / wait / abort, as contracted).

NO ENDLESS IN-PLACE LOOP.

══════════════════════════════════════════════════════════════════════════════
G. OPEN-SEQUENCE LEDGER — ALWAYS ACTIVE CONTROL STATE
══════════════════════════════════════════════════════════════════════════════

EVERY OPEN OR SUSPENDED SEQUENCE
    ↓
REGISTER IN OPEN-SEQUENCE LEDGER
    │
    │ RECORD:
    │ - sequence_id
    │ - relation_to_other_sequence
    │ - requesting_sequence_id
    │ - requesting_node_or_edge
    │ - required_or_optional
    │ - controller
    │ - current_status
    │ - contract_id
    │ - blocked_edge
    │ - opened_at
    │ - required_return
    │ - terminal_status when closed
    │
    │ STATUS DURING EXECUTION:
    │ OPEN
    │ SUSPENDED
    │ WAITING_FOR_TRIGGER
    │ WAITING_FOR_DEPENDENCY
    │ WAITING_FOR_RETURN
    │
    │ FINAL STATUS:
    │ CLOSED_SUCCESS
    │ CLOSED_FAILURE
    │ CLOSED_PARTIAL
    │ CLOSED_UNKNOWN
    │ CLOSED_UNAVAILABLE
    │ CLOSED_NOT_APPLICABLE
    │ CLOSED_ABORTED
    │
    │ BARRIER RULE:
    │ No dependent edge may cross while a REQUIRED attached Sequence
    │ for that edge is non-terminal or its return is unaccepted.
    │
    │ Independent branches may continue.

══════════════════════════════════════════════════════════════════════════════
H. RESOURCE / EVIDENCE / EXECUTION PREPARATION
══════════════════════════════════════════════════════════════════════════════

[US-19] AVAILABILITY
    │
    │ MACHINE MEANING:
    │ A dependency may exist but still be inaccessible now.
    │
    │ CHECK:
    │ exists?
    │ reachable?
    │ controllable/usable?
    │ timely?
    │ sufficient quantity/capacity?
    │
    ├── AVAILABLE
    │      ↓
    │   CONTINUE
    │
    └── NOT AVAILABLE
           ↓
       OPEN ATTACHED SEQUENCE
           │
           ├── LOCATE
           ├── OBTAIN / IMPORT
           ├── CREATE / BUILD
           ├── REPAIR
           ├── SUBSTITUTE
           ├── ADAPT
           ├── WAIT FOR DECLARED EVENT
           ├── REDUCE REQUIREMENT
           └── ABORT / CLOSE FAILURE if contract permits
           ↓
       CLOSE ATTACHED SEQUENCE
           ↓
       RETURN
           ↓
       RECHECK AVAILABILITY
    ↓
[US-20] ADMISSIBILITY / QUALIFICATION
    │
    │ MACHINE MEANING:
    │ Determine whether the available input/state/dependency is legitimate for
    │ the next transition.
    │
    │ CHECK:
    │ physically possible
    │ compatible
    │ valid
    │ safe where safety is part of the contract
    │ sufficient
    │ relevant
    │ authorized
    │ correct identity/version
    │ within scope
    │
    ├── QUALIFIED
    │      ↓
    │   CONTINUE
    │
    └── NOT QUALIFIED
           ↓
       ATTACHED SEQUENCE:
       modify / repair / condition / replace / investigate / obtain evidence
           ↓
       CLOSE
           ↓
       RETURN
           ↓
       RE-QUALIFY
    ↓
[US-21] TEST / EVIDENCE
    │
    │ MACHINE MEANING:
    │ If the contract requires proof, observation, simulation, trial,
    │ comparison, consistency checking, or evidence collection, execute it here.
    │
    │ TEST MODE:
    │ observation
    │ experiment
    │ simulation
    │ formal proof / derivation
    │ trial
    │ cross-check
    │ comparison with validated memory
    │
    ├── TEST NOT REQUIRED BY CONTRACT
    │      ↓
    │   CONTINUE
    │
    └── TEST REQUIRED
           ↓
       CREATE/EXECUTE TEST SEQUENCE
           ↓
       TEST SEQUENCE CLOSES WITH RESULT
           │
           ├── ACCEPTED PASS
           │      ↓
           │   CONTINUE
           │
           └── FAIL / UNKNOWN / UNAVAILABLE
                  ↓
              CURRENT TEST ATTEMPT REMAINS HISTORICALLY CLOSED
                  ↓
              OPEN NEW REPAIR / MODIFICATION / INVESTIGATION /
              RETEST SEQUENCE
                  ↓
              CLOSE
                  ↓
              RETURN
                  ↓
              RE-EVALUATE

══════════════════════════════════════════════════════════════════════════════
I. ALTERNATIVES, COUNTER-SEQUENCES, SELECTION
══════════════════════════════════════════════════════════════════════════════

[US-22] ALTERNATIVE PATH GENERATION
    │
    │ MACHINE MEANING:
    │ Enumerate multiple legally possible continuations without collapsing them
    │ prematurely.
    │
    │ STORE:
    │ - path_id
    │ - predicted result
    │ - required dependencies
    │ - risk/cost if part of contract
    │ - reversibility if part of contract
    │ - rule compatibility
    │ - evidence confidence
    ↓
[US-23] COUNTER-SEQUENCE DETECTION
    │
    │ MACHINE MEANING:
    │ Detect a separately identified Sequence whose result can negate, block,
    │ degrade, divert, balance, neutralize, or oppose a required result of
    │ another Sequence.
    │
    │ STORE:
    │ - counter_sequence_id
    │ - opposed_sequence_id
    │ - relation_type
    │ - exact result being opposed
    │ - activation condition
    │ - controller/carrier if any
    │ - expected interaction point
    │
    │ MACHINE RULE:
    │ "Counter" describes relation, not moral value.
    │ The Counter-Sequence must have its own contract and closure.
    ↓
[US-24] PRIORITY / ARBITRATION / SELECTION
    │
    │ MACHINE MEANING:
    │ If more than one admissible path/control exists, determine which path
    │ governs the next transition.
    │
    │ IF NO SELECTING CONTROLLER EXISTS:
    │ resolution is produced by declared physical/logical/structural constraints.
    │
    │ IF SELECTING CONTROLLER EXISTS:
    │ compare according to explicit priority/rule/goal/contract fields.
    │
    │ OUTPUT:
    │ selected_path_id
    │ selection_reason
    │ rejected/held alternatives retained in memory
    ↓

══════════════════════════════════════════════════════════════════════════════
J. ENCOUNTER → COUPLING → DYNAMICS
══════════════════════════════════════════════════════════════════════════════

[US-25] ENCOUNTER / ACCESS
    │
    │ CONDITIONAL:
    │ Use only when the required relation does not already exist.
    │
    │ MACHINE MEANING:
    │ Bring required objects/states/information/resources into a relation in
    │ which interaction can become possible.
    │
    │ SPECIALIZATIONS:
    │ encounter / contact / access / acquisition / retrieval / approach
    ↓
[US-26] COUPLING / INTERACTION
    │
    │ MACHINE MEANING:
    │ The involved states now causally, logically, physically, biologically,
    │ informationally, socially, or computationally affect one another.
    │
    │ MACHINE RULE:
    │ COUPLING is broader than ingestion/intake.
    │ Ingestion, reception, binding, connection, contact, and communication
    │ are domain-specific forms.
    ↓
[US-27] TRANSFORMATION / CONDITIONING
    │
    │ CONDITIONAL:
    │ only if an object/input/state must be altered before/during use.
    │
    │ MACHINE MEANING:
    │ Change form, representation, condition, structure, encoding, or state
    │ to make the next dynamics possible.
    │
    │ SPECIALIZATIONS:
    │ conditioning
    │ conversion
    │ reaction
    │ shaping
    │ preparation
    │ encoding
    │ translation
    │ cleaning
    │ restructuring
    │
    │ IF TRANSFORMATION IS NONTRIVIAL:
    │ open an Attached Sequence; close it; return transformed result.
    ↓
[US-28] DYNAMICS / PROCESS / PROPAGATION
    │
    │ MACHINE MEANING:
    │ The actual state-evolution mechanism.
    │
    │ POSSIBLE TYPES:
    │ physical propagation
    │ motion
    │ reaction
    │ metabolism
    │ regulation
    │ computation
    │ reasoning
    │ assembly
    │ decay
    │ transfer
    │ exchange
    │ mathematical iteration
    │ social process
    │ other declared mechanism
    │
    │ MACHINE RULE:
    │ "Processing" is only one subtype of Dynamics.
    ↓
[US-29] INCORPORATION / INTEGRATION
    │
    │ CONDITIONAL:
    │ only when some input/result becomes part of a receiving system's state.
    │
    │ MACHINE MEANING:
    │ Update the receiving state so the incorporated material/information/
    │ capability/relationship is now represented as part of current reality.
    │
    │ DO NOT duplicate "assimilation" and "integration" as separate universal
    │ stages unless the domain defines two distinct transitions.
    ↓
[US-30] EFFECT / ACTION / OUTPUT
    │
    │ MACHINE MEANING:
    │ Record what the active dynamics causes beyond the immediately updated state.
    │
    │ UNIVERSAL PARENT = EFFECT.
    │
    │ SUBTYPES:
    │ passive physical effect
    │ emitted material/energy
    │ information output
    │ behavioral action
    │ deliberate action
    │ environmental alteration
    │ product creation
    │ resource consumption/creation
    │
    │ MACHINE RULE:
    │ Do not force "Action" onto non-agentic systems.
    ↓

══════════════════════════════════════════════════════════════════════════════
K. RESULT, EVENT WEIGHT, LATENT CONSEQUENCE
══════════════════════════════════════════════════════════════════════════════

[US-31] STATE CHANGE
    │
    │ MACHINE MEANING:
    │ Store exactly how reality after the transition differs from reality before it.
    │
    │ RECORD SEPARATELY:
    │ followed-object change
    │ other-entity change
    │ environment change
    │ relation change
    │ information change
    │ capability change
    │ rule/constraint change
    ↓
[US-32] ENTITY OUTCOME
