PROMISE-MATCH
PRIORITY-CONFLICT
COMPOSITE:
    A AND B
    A OR B
    A UNLESS C
```

If no special threshold is required:

```text
threshold = ALWAYS
```

Never leave the field ambiguous.

---

# 8. DRIVER, CONTROLLER, PERFORMER, CARRIER — KEEP SEPARATE

These four roles are not synonyms.

```text
DRIVER
= why movement is being considered

CONTROLLER
= who/what authorizes, regulates or inhibits movement

PERFORMER
= who/what actually carries out the transition

CARRIER
= what carries the relevant Sequence state forward
```

Driver types:

```text
NATURAL_DYNAMICS
NEED
WANT
GOAL
EXTERNAL_DEMAND
OPPORTUNITY
CURIOSITY_UNKNOWN
DAMAGE_DEVIATION
RELATIONAL_DRIVER
PROMISE_ACTIVATION
REPRESENTED_FUTURE_DIFFERENCE
PRIOR_RESULT
```

Controller types:

```text
NONE_NATURAL
SELF
DISTRIBUTED_SELF
EXTERNAL
JOINT
META
UNKNOWN
```

Example:

```text
Pyramid Construction

Driver:
represented future monument

Controller:
project authority

Performer:
architects / quarry / transport / building workforce

Carrier:
plans + people + stone + project state

Affected Entity:
pyramid
```

---

# 9. SEQUENCE RELATION TYPES

Do not collapse every connected Sequence into one `parent/child` relation.

Use typed Sequence-to-Sequence edges.

```text
MAIN
LOCAL
RIDER
ATTACHED
PARALLEL
COUNTER
CONVERGING
NEXT
REFERENCE
OBSERVER_WRITER
```

Definitions:

```text
MAIN
= declared higher-scope Sequence being followed.

LOCAL / RIDER
= independently meaningful Sequence running alongside another.

ATTACHED
= opened because another Sequence requires a missing result.

COUNTER
= a Sequence whose result opposes, neutralizes, diverts or balances another result.

CONVERGING
= separately developed Sequence that reaches a common execution window.

NEXT
= new Sequence created after an older Sequence closes.

REFERENCE
= new Sequence that cites/expands/audits an older CLOSED Sequence.

OBSERVER_WRITER
= new recording/reconstruction Sequence built from traces of older closed events.
```

---

# 10. SUB-SEQUENCE / ATTACHED-SEQUENCE CONTRACT

Use `Sub-Sequence` as the general working word when needed, but store the precise relation type.

Every required Sub-Sequence receives:

```text
SUB_SEQUENCE_CONTRACT {
    sequence_id
    relation_type

    requesting_sequence_id
    requesting_node_or_edge

    reason
    requested_result
    return_schema

    scope
    context_snapshot

    driver
    controller
    performer
    carrier

    activation_condition
    close_condition
    acceptance_condition

    required_or_optional

    epistemic_requirement
    proof_depth

    dependencies[]
    deadline_or_time_condition

    termination_policy
}
```

Critical rule:

```text
CLOSE CONDITION
≠
ACCEPTANCE CONDITION
```

Example:

```text
SEARCH FOR WATER

Close Condition:
search finished

Return:
not found

Sequence Status:
CLOSED_SUCCESS
(as search execution)

Parent Acceptance:
FALSE
```

The parent does not advance.

It may open:

```text
BUILD
SUBSTITUTE
IMPORT
WAIT
REDUCE REQUIREMENT
ABORT
```

as new Sequences.

---

# 11. OPEN-SEQUENCE LEDGER

The Ledger is the runtime enforcement state.

```text
OPEN_SEQUENCE_LEDGER {
    sequence_id
    relation_type

    requesting_sequence_id
    requesting_node_or_edge

    required_or_optional

    controller
    performer
    carrier

    contract_id
    blocked_edge_id

    opened_at
    current_status

    required_return
    returned_packet_id
    return_acceptance

    terminal_status
}
```

Runtime statuses:

```text
OPEN
SUSPENDED
WAITING_FOR_TRIGGER
WAITING_FOR_THRESHOLD
WAITING_FOR_DEPENDENCY
WAITING_FOR_RETURN
```

Terminal statuses:

```text
CLOSED_SUCCESS
CLOSED_FAILURE
CLOSED_PARTIAL
CLOSED_UNKNOWN
CLOSED_UNAVAILABLE
CLOSED_NOT_APPLICABLE
CLOSED_ABORTED
```

Barrier query:

```text
required_open_sequences(edge_id) == 0
AND
all_required_returns_accepted(edge_id) == TRUE
```

Only then may the dependent edge fire.

---

# 12. SEED REGISTRY — SEPARATE FROM THE OPEN LEDGER

A Seed is not automatically an open Sequence.

A Seed can exist before a carrier.

```text
SEED_REGISTRY {
    seed_id

    source_sequence_id
    source_closure_packet_id

    seed_type
    seed_content

    created_at
    persistence_condition

    carrier_bound = TRUE/FALSE
    possible_carrier_types[]

    activation_trigger
    activation_threshold

    current_status:
        LATENT
        ACTIVATABLE
        ACTIVATED
        CONSUMED
        TRANSFORMED
        PERSISTENT
        EXPIRED
        UNKNOWN

    resulting_sequence_ids[]
}
```

Flow:

```text
CLOSED SEQUENCE
↓
RESULT / MEMORY / PROMISE / CONDITION
↓
SEED REGISTRY
↓
LATENT
↓
TRIGGER + THRESHOLD
↓
CARRIER FOUND OR CREATED
↓
NEW SEQUENCE ID
↓
OPEN-SEQUENCE LEDGER
```

---

# 13. ACTOR / VIEW MAP

Reality and actor knowledge must remain separate.

```text
GLOBAL REALITY
≠
ACTOR VIEW
```

Store:

```text
VIEW_STATE {
    view_id
    actor_or_system_id
    sequence_id
    time_or_state_ref

    known[]
    believed[]
    inferred[]
    unknown[]
    false_beliefs[]
    hidden_from_actor[]

    source_refs[]
    confidence[]
}
```

Action is evaluated as:

```text
GLOBAL REALITY
+
ACTOR VIEW
+
CURRENT STATE
+
UNIQUE HISTORY
+
PRIORITY
+
CAPABILITY
↓
ACTION / RESPONSE
```

Never assume identical input produces identical behavior.

---

# 14. EVENT WEIGHT / DOWNSTREAM CRITICALITY

Do not judge relevance only by local magnitude.

```text
EVENT_WEIGHT {
    event_id

    local_effect_magnitude
    affected_scope_now

    downstream_dependency_ids[]
    downstream_dependency_count

    latency

    closure_criticality
    global_scope_effect

    counterfactual_necessity:
        REQUIRED
        SUPPORTING
        INCIDENTAL
        UNKNOWN
}
```

Key falsifier:

```text
REMOVE EVENT E
↓
CAN DECLARED END STILL BE REACHED?
```

If `NO`, E is closure-critical even if it looked small locally.

This is also the reverse-depth control.

The system does not need to reverse-engineer the whole universe for every meal.

It continues backward only while older conditions materially affect closure of the declared end at the chosen resolution.

---

# 15. NODE TRUTH AND PATH TRUTH

Store two different objects.

## NODE TRUTH

```text
NODE_TRUTH {
    node_id
    applicability
    state
    owner
    borrowed_from
    evidence
    epistemic_status
}
```

## PATH TRUTH

```text
PATH_TRUTH {
    edge_id
    source
    target

    order_type
    relation_type

    trigger
    threshold

    driver
    controller
    performer
    carrier

    dependency_refs[]
    rule_refs[]
    evidence_refs[]
}
```

Dots show Node Truth.

Connected edges show Path Truth.

Both are needed.

---
