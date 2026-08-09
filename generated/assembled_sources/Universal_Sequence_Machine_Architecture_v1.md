# UNIVERSAL SEQUENCE — MACHINE EXECUTION ARROW ARCHITECTURE
## Consolidated working state from the Sequence source conversation

> This document is intentionally written as an executable arrow grammar, not as a prose list.
> Every named object below is placed where it acts.
> Human and AI parameter registries are NOT mapped here.
> "Closure" is reserved for a Sequence contract. Entity persistence/termination is separate.

══════════════════════════════════════════════════════════════════════════════
A. ABSOLUTE SEQUENCE RULE
══════════════════════════════════════════════════════════════════════════════

DIFFERENCE
    +
RELATIONSHIP
    +
ORDER
    ↓
SEQUENCE EXISTS

MACHINE MEANING:
A Sequence may be temporal, causal, dependency-based, logical, constructional,
discovery-based, decision-based, execution-based, mathematical, social, physical,
biological, informational, or mixed.

ORDER does NOT automatically mean clock-time.

EXAMPLES OF ORDER TYPES THE MACHINE MUST DISTINGUISH:
TEMPORAL        = A happened before B.
CAUSAL          = A contributed to producing B.
DEPENDENCY      = B cannot execute unless A is available/accepted.
LOGICAL         = B follows from A under a rule of inference.
CONSTRUCTION    = B must be assembled after required parts/states exist.
DISCOVERY       = B became known after evidence/process A.
CONTROL         = A authorizes, inhibits, or redirects B.
REPRESENTATION  = a present model of a possible future constrains present action.

RULE:
Never convert one order type into another without an explicit relation edge.

══════════════════════════════════════════════════════════════════════════════
B. THREE-PASS SEQUENCE VALIDATION — THE OUTER ENVELOPE
══════════════════════════════════════════════════════════════════════════════

                     DECLARED / OBSERVED END
                              │
                              │
                              │ PASS 1 — REVERSE
                              │ "What had to exist, happen, persist, or close
                              │  for this exact end/result to be possible?"
                              ↑
                              │
                    EARLIEST JUSTIFIED PRIOR REALITY
                              │
                              │
                              │ PASS 2 — FORWARD
                              │ "If every required prior condition actually
                              │  exists, can the graph legally produce END?"
                              ↓
                              │
                     DECLARED / OBSERVED END
                              │
                              │
                              │ PASS 3 — REVERSE AGAIN
                              │ "Does every result have a producer?
                              │  Does every producer have provenance?
                              │  Does every edge have a legal firing condition?
                              │  Are all required attached sequences terminal?
                              │  Are identity changes and borrowed operations
                              │  explained?"
                              ↑
                              │
                    EARLIEST JUSTIFIED PRIOR REALITY
                              │
                              ↓
                    STRUCTURAL CLOSURE DECISION

IF ANY REQUIRED LINK CANNOT BE EXPLAINED:
    ↓
UNCONNECTED DOT
    ↓
CREATE A NEW INVESTIGATION / RECOVERY ATTACHED SEQUENCE
    ↓
THAT SEQUENCE RUNS THE SAME UNIVERSAL GRAMMAR
    ↓
IT CLOSES
    ↓
ITS CLOSURE PACKET RETURNS
    ↓
RUN THE AFFECTED PASS AGAIN

IMPORTANT:
The "declared end" is the analysis target.
It is NOT automatically the chronological beginning of reality.

══════════════════════════════════════════════════════════════════════════════
C. PRE-RUN MACHINE LOCK
══════════════════════════════════════════════════════════════════════════════

DECLARED / OBSERVED END
    ↓
[US-00] SEQUENCE SCOPE + CLOSURE SCOPE
    │
    │ MACHINE MEANING:
    │ Define exactly what this Sequence instance is required to explain,
    │ produce, verify, or close.
    │
    │ STORE:
    │ - sequence_id
    │ - sequence_name
    │ - declared_end_or_target
    │ - closure_scope
    │ - included_systems
    │ - excluded_systems
    │ - resolution_level
    │ - causal_horizon
    │ - epistemic_floor_rule
    │
    │ CLOSURE SCOPE MUST BE EXPLICIT:
    │ action / promise / task / person-event / project / war / institution /
    │ dynasty / era / scientific question / physical event / mathematical proof /
    │ other declared scope.
    │
    │ MACHINE RULE:
    │ A lower-scope closure never silently means a higher-scope closure.
    ↓
[US-01] FOLLOWED OBJECT / IDENTITY / BOUNDARY
    │
    │ MACHINE MEANING:
    │ Declare what the machine is following through this Sequence.
    │
    │ TYPE MAY BE:
    │ entity / event / relation / condition / rule / information / capability /
    │ abstract object / system / process.
    │
    │ STORE:
    │ - followed_object_id
    │ - followed_object_type
    │ - identity_continuity_criteria
    │ - boundary_type
    │ - current_role
    │
    │ BOUNDARY TYPE:
    │ intrinsic / emergent / operational / observer-declared / unbounded /
    │ abstract.
    │
    │ MACHINE RULE:
    │ Identity is not identical to current physical state, function, role,
    │ purpose, or use.
    ↓
[US-02] FORMATION-TYPE ROUTER
    │
    │ MACHINE MEANING:
    │ Select the formation regime that tells the machine which later routes
    │ are potentially applicable. This does NOT force every regime to use
    │ every node.
    │
    ├── FUNDAMENTAL / FORMATION-NOT-APPLICABLE
    ├── SPONTANEOUS PHYSICAL FORMATION
    ├── BIOLOGICAL FORMATION
    ├── AGENT-DESIGNED FORMATION
    ├── SOCIAL / CULTURAL EMERGENCE
    ├── INFORMATIONAL / COMPUTATIONAL FORMATION
    ├── PURE MATHEMATICAL / ABSTRACT FORMATION
    ├── HYBRID
    └── UNKNOWN / UNRESOLVED
    │
    │ MACHINE RULE:
    │ "Universal" means the grammar can represent the case without forcing
    │ false semantics. It does NOT mean every route must be populated.

══════════════════════════════════════════════════════════════════════════════
D. FORWARD UNIVERSAL SEQUENCE SPINE
══════════════════════════════════════════════════════════════════════════════

[US-03] PRIOR REALITY
    │
    │ MACHINE MEANING:
    │ The complete set of already-existing conditions that are allowed to be
    │ treated as input reality at the declared causal horizon.
    │
    │ MAY INCLUDE:
    │ physical conditions
    │ previously closed Sequence results
    │ existing entities
    │ relationships
    │ resources
    │ environments
    │ stored rules
    │ memories
    │ institutions
    │ unknown-but-declared conditions
    │
    │ STORE:
    │ - prior_state_snapshot
    │ - source_sequence_ids
    │ - unresolved_prior_conditions
    │ - epistemic_status for every claimed predecessor
    │
    │ EPISTEMIC STATUS:
    │ KNOWN / SUPPORTED / INFERRED / SPECULATIVE / UNKNOWN / CONTRADICTORY
    ↓
[US-04] PROVENANCE / ORIGIN
    │
    │ MACHINE MEANING:
    │ For every object, state, relation, capability, rule, or dependency that
    │ will be used later, record where it came from.
    │
    │ PROVENANCE MAY BE:
    │ prior closed Sequence
    │ formation process
    │ physical source
    │ biological source
    │ informational source
    │ social source
    │ technical source
    │ mathematical derivation
    │ unknown source
    │
    │ MACHINE RULE:
    │ "Used later" + "no origin" = UNCONNECTED DOT unless explicitly UNKNOWN.
    ↓
[US-05] SEQUENCE SEED / LATENT PRECONDITION
    │
    │ MACHINE MEANING:
    │ A condition, relation, stored commitment, resource arrangement, capability,
    │ or possibility that can exist before the later Sequence carrier or visible
    │ event exists.
    │
    │ A SEED IS NOT AN OPEN SEQUENCE.
    │ A SEED IS NOT AUTOMATICALLY INTENT.
    │
    │ STORE:
    │ - seed_id
    │ - created_by_sequence_id or unknown
    │ - seed_type
    │ - persistence_condition
    │ - possible_carrier_types
    │ - activation_threshold
    │ - consumed/transformed/persistent status
    │
    │ EXAMPLES OF MACHINE INTERPRETATION:
    │ - a stored promise = future-action seed
    │ - a physical configuration that matters decades later = latent seed
    │ - a design possibility before a specific builder = formation seed
    │
    │ MACHINE RULE:
    │ Do not attribute a seed's origin to the later carrier merely because
    │ the carrier executes it.
    ↓
[US-06] ENVIRONMENT / HOST / SUBSTRATE / CONDITIONS
    │
    │ MACHINE MEANING:
    │ Declare the larger reality in which the followed object can exist,
    │ interact, persist, form, or execute.
    │
    │ STORE:
    │ - host_system
    │ - substrate
    │ - environmental_conditions
    │ - external_constraints
    │ - location / domain
    │ - time conditions if relevant
    │
    │ MACHINE RULE:
    │ Environment may itself be the result of older closed Sequences.
    │ The environment is not assumed passive; it can be modified by the Sequence.
    ↓
[US-07] FORMATION / EMERGENCE / INSTANTIATION
    │
    │ MACHINE MEANING:
    │ Explain how the followed object/state/relation became sufficiently real
    │ to participate in the current Sequence.
    │
    │ POSSIBLE MODES:
    │ already present in scope
    │ assembled
    │ grown
    │ inherited
    │ transformed
    │ generated
    │ designed then instantiated
    │ socially emerged
    │ mathematically defined/derived
    │ unknown
    │
    │ STORE:
    │ - formation_mode
    │ - formation_sequence_ids
    │ - formation_inputs
    │ - formation_result
    │
    │ MACHINE RULE:
    │ EXISTENCE is itself normally the result of a prior formation Sequence.
    ↓
[US-08] EXISTENCE STATUS + ROLE
    │
    │ MACHINE MEANING:
    │ Record the current degree and form of existence without assuming a
    │ simple yes/no.
    │
    │ EXISTENCE STATUS MAY BE:
    │ represented
    │ proposed
    │ initiated
    │ partially instantiated
    │ functionally instantiated
    │ materially instantiated
    │ completed
    │ modified
    │ degraded
    │ remnant
    │ absent
    │ unknown
    │ abstract-only
    │
    │ ROLE:
    │ The function/position the object currently plays in this Sequence.
    │ Same object may change role while identity persists.
    ↓
[US-09] CURRENT STATE
    │
    │ MACHINE MEANING:
    │ Snapshot of all properties relevant to the next legal transition.
    │
    │ STORE:
    │ - state variables
    │ - current capabilities
    │ - current deficits/deviations
    │ - current resources
    │ - current restrictions
    │ - current unresolved conditions
    │
    │ MACHINE RULE:
    │ STATE answers "what is true now?"
    │ It does NOT answer "why move now?"
    ↓
[US-10] ENTITY COHERENCE / PERSISTENCE
    │
    │ MACHINE MEANING:
    │ Determine whether the followed identity-bearing object remains coherent
    │ enough to be treated as the same object.
    │
    │ STATES:
    │ persisting / unstable / degraded / repairing / transforming / unknown /
    │ not-applicable
    │
    │ MACHINE RULE:
    │ ENTITY COHERENCE is NOT SEQUENCE CLOSURE.
    │ A phenomenon/entity may continue after the Sequence about it closes.
    ↓
[US-11] RELATION MAP
    │
    │ MACHINE MEANING:
    │ Record every relation that can change the path or meaning of the Sequence.
    │
    │ RELATIONS MAY INCLUDE:
    │ object ↔ environment
    │ object ↔ resource
    │ object ↔ other object
    │ object ↔ rule
    │ object ↔ information
    │ object ↔ controller
    │ Sequence ↔ Sequence
    │ state ↔ state
    │
    │ STORE:
    │ - relation_id
    │ - relation_type
    │ - from
    │ - to
    │ - direction
    │ - start condition
    │ - current validity
    │ - evidence/provenance
    ↓
[US-12] KNOWLEDGE DISTRIBUTION / VIEW MAP
    │
    │ APPLIES WHEN:
    │ one or more participants/observers/controllers can hold information.
    │
    │ MACHINE MEANING:
    │ Separate global recorded reality from what each participant actually knows,
    │ believes, observes, infers, or is told.
    │
    │ STORE PER PARTICIPANT:
    │ - known facts
    │ - believed facts
    │ - unknown facts
    │ - false/misleading inputs
    │ - confidence
    │ - source
    │ - hidden information
    │
    │ MACHINE RULE:
    │ GLOBAL REALITY ≠ ACTOR VIEW.
    │ Never infer that all participants have access to the same map.
    │
    │ UNIQUE-HISTORY MODULATION:
    │ Same input + same formal rule does not imply same response.
    │ Response may differ because current state, prior history, relationships,
    │ pressure, identity, commitments, memory, and knowledge differ.
    ↓
[US-13] DRIVER ORIGIN
    │
    │ MACHINE MEANING:
    │ Record why a transition is even being considered.
    │
    │ DRIVER TYPES:
    │ NATURAL / CONSTRAINT DYNAMICS
    │ NEED
    │ WANT
    │ GOAL
    │ EXTERNAL DEMAND
    │ OPPORTUNITY
    │ CURIOSITY / UNKNOWN
    │ DAMAGE / DEVIATION
    │ RELATIONAL DRIVER
    │ PROMISE / STORED-COMMITMENT ACTIVATION
    │ REPRESENTED FUTURE DIFFERENCE
    │ PRIOR RESULT
    │
    │ MACHINE RULE:
    │ Requirement is NOT universal.
    │ Natural dynamics can proceed with no need/want/goal.
    ↓
[US-14] CONTROLLER + SEQUENCE CARRIER
    │
    │ MACHINE MEANING:
    │ Distinguish "what drives" from "what controls" and from "what carries".
    │
    │ CONTROLLER TYPES:
    │ NONE / NATURAL DYNAMICS
    │ SELF
    │ DISTRIBUTED SELF
    │ EXTERNAL
    │ JOINT
    │ META-CONTROLLER
    │ UNKNOWN
    │
    │ SEQUENCE CARRIER:
    │ The entity/person/system through which an already-existing seed,
    │ commitment, capability, or relation is executed.
    │
    │ MACHINE RULE:
    │ DRIVER ≠ CONTROLLER ≠ CARRIER.
    ↓
[US-15] REPRESENTED FUTURE STATE / REPRESENTED FUTURE SEQUENCE
    │
    │ CONDITIONAL:
    │ only when a system can represent a not-yet-existing state/path.
    │
    │ MACHINE MEANING:
    │ A present representation of a possible future can constrain current
    │ transitions without claiming literal backward causation.
    │
    │ DISTINGUISH:
    │ DESIRED FUTURE STATE
    │     = the target condition.
    │ REPRESENTED FUTURE SEQUENCE
    │     = the modeled path required to reach that target.
    │
    │ STORE:
    │ - target_state
    │ - represented_path
    │ - owner/controller
    │ - confidence
    │ - assumptions
    │
    │ IF NOT APPLICABLE:
    │ route directly onward.
    ↓
[US-16] RULE / PROMISE / PRIORITY / CONSTRAINT MAP
    │
    │ MACHINE MEANING:
    │ Record all controls that can permit, prohibit, delay, prioritize,
    │ or redirect a transition.
    │
    │ RULE:
    │ a general condition governing allowed/forbidden transitions.
    │
    │ PROMISE / FUTURE-ACTION COMMITMENT:
    │ a closed prior Sequence result that stores:
    │ creator / owner / target / intended result / activation condition /
    │ persistence / close condition.
    │ When the condition later fires, a NEW Sequence is created.
    │
    │ PRIORITY:
    │ ranking/arbitration used when multiple valid drivers/rules/goals conflict.
    │
    │ RULE OVERRIDE:
    │ a recorded local exception. It MUST contain:
    │ - normal rule
    │ - higher controlling condition
    │ - reason
    │ - controller
    │ - allowed scope
    │ - exact permitted deviation
    │ - alternatives considered
    │ - cost/consequence
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
