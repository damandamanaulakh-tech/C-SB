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
