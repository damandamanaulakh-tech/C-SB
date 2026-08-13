# Example: Rain / Target-Layer Action Reasoning V1

<!-- SOURCEBORN-REALTIME-ASI-V1:START -->

> **Growing-Phase example semantics:** this file is a **Brain-growth event fixture**, not an answer template and not a demonstration that Sourceborn is a reasoning/prompt engine. The event activates existing IDs and may produce relation, intent, interpretation, pattern, memory, combination or new-ID candidates. A new parameter/ID is created only after the required source boundary, review and R-F-R gate. Older filenames containing `REASONING` are retained as provenance labels only. See `docs/SOURCEBORN_REALTIME_ASI_GROWING_PHASE_V1.md`.

<!-- SOURCEBORN-REALTIME-ASI-V1:END -->

## Status

`EXAMPLE / REVIEW-REQUIRED REASONING-CANDIDATE TEST`

## Source

> when i want to take my kids out, if it start raining i have no need to go; there is no rain, but how i make sure its rain to kids

The source remains immutable. This example tests a transition from understanding a condition to being asked to achieve an outcome.

## Source split

```text
ORIGINAL PLAN
I -> take kids out

CONDITIONAL RULE
IF rain -> no need to go

CURRENT WORLD STATE
no rain

REQUEST
"how do I make sure it's rain to kids?"
```

The machine must not silently decide that the user is asking to change the weather, to deceive the children, or simply to cancel the outing. Those are different candidate interpretations.

## Core difference

```text
QUESTION ABOUT REALITY
        !=
REQUEST TO ACHIEVE AN OUTCOME
```

The action request activates planning/tool/alternative/execution/effect/verification routing in addition to observation and interpretation.

## Active 3,204 source-bank regions

The source example declares `30 / 80` strong container hits, but explicitly enumerates only **28 unique container IDs**. Sourceborn preserves this discrepancy as an open R-F-R finding instead of inventing two missing containers.

```text
SEG-02 PERCEPTION / ENVIRONMENT
  CON-009 Visual Perception
  CON-013 Multisensory Integration
  CON-016 Spatial, Temporal and Environmental Mapping

SEG-03 ACTION / EXECUTION
  CON-017 Action Readiness and Affordance Detection
  CON-018 Motor Planning and Sequencing
  CON-020 Action Selection and Initiation
  CON-023 Imitation, Gesture and Tool Manipulation

SEG-04 EXECUTIVE CONTROL
  CON-030 Cognitive Flexibility
  CON-031 Executive Sequencing and Task Management
  CON-032 Conflict, Error and Performance Monitoring

SEG-06 REASONING / PLANNING / CREATION
  CON-043 Causal, Counterfactual and Predictive Reasoning
  CON-045 Problem Framing and Decomposition
  CON-046 Planning, Strategy and Future Simulation
  CON-047 Decision, Judgment and Trade-off Intelligence
  CON-048 Creativity, Imagination and Invention

SEG-07 LANGUAGE / AUDIENCE
  CON-052 Comprehension and Discourse Integration
  CON-053 Language Production
  CON-054 Pragmatics and Implied Meaning
  CON-056 Audience Adaptation

SEG-08 MOTIVATION / INTENT / MOTIVE
  CON-062 Motivation, Effort and Persistence
  CON-063 Intent Formation and Commitment
  CON-064 Motive, Needs, Values and Priority Structure

SEG-09 SOCIAL / RESPONSIBILITY / NORM
  CON-068 Agency, Ownership and Responsibility
  CON-069 Theory of Mind
  CON-071 Attachment, Belonging, Status and Group Behaviour
  CON-072 Morality and Norms

SEG-10 META / REPAIR
  CON-075 Metacognition and Self-Monitoring
  CON-077 Resilience, Failure Detection and Repair
```

```text
source-declared count    30
explicit unique refs     28
unresolved delta          2
```

Exact `SB-HFR-Pxxxx` atomic IDs are not asserted by this example.

## Additional action-mode regions

The source identifies 12 regions that become particularly relevant once the user asks the system to **do/achieve** something rather than merely interpret a situation:

```text
CON-013  multisensory integration
CON-018  motor planning
CON-023  tool manipulation
CON-030  cognitive flexibility
CON-031  task management
CON-046  planning / strategy
CON-048  creativity / invention
CON-053  language production
CON-056  audience adaptation
CON-069  theory of mind
CON-072  morality / norms
CON-077  failure detection / repair
```

These are existing source regions, not new parameters.

## Candidate discovery 1 — CHANGE TARGET LAYER

The phrase `make it rain to kids` can point to several non-equivalent change targets:

```text
DESIRED CHANGE
     │
     ├─ WORLD_STATE
     │    actual meteorological rain
     │
     ├─ SIGNAL_STATE
     │    rain-like visual/audio/tactile cues
     │
     ├─ PERCEPTION_STATE
     │    what the children perceive
     │
     ├─ BELIEF_STATE
     │    what the children believe is true
     │
     └─ BEHAVIOR_STATE
          whether the children behave as if rain changes the plan
```

Hard separation:

```text
WORLD_CHANGE
!= SIGNAL_CHANGE
!= PERCEPTION_CHANGE
!= BELIEF_CHANGE
!= BEHAVIOR_CHANGE
```

Candidate ID: `RC-TARGET-LAYER-001`.

Status: `REVIEW_REQUIRED`; no canonical promotion and no direct action authority.

## Candidate discovery 2 — INSTRUMENTAL TRIGGER != TERMINAL GOAL

The source contains:

```text
RAIN -> NO NEED TO GO
```

The machine should test whether `RAIN` is:

- the terminal end,
- a trigger/condition,
- one means/path to a different end,
- or merely part of the user's explanation.

It must not silently rewrite the end as `NO OUTING`.

```text
TRIGGER != TERMINAL_GOAL
MEANS   != END
```

Candidate ID: `RC-INSTRUMENTAL-TRIGGER-END-001`.

Status: `REVIEW_REQUIRED`.

## Actor-view / epistemic boundary

```text
CURRENT WORLD STATE
NO_RAIN

POSSIBLE REQUEST INTERPRETATIONS
- create actual rain
- create rain-like signals/experience
- change children's perception
- change children's belief
- obtain the no-outing result by another route
- other / unresolved
```

None becomes fact solely from the phrase `make it rain to kids`.

## Runtime result

```text
3,204 SOURCE BANK
      │
      ▼
28 explicitly enumerated container regions
(source text separately declares 30)
      │
      ▼
ACTION-MODE ROUTING
      │
      ├─ plan
      ├─ tools
      ├─ alternatives
      ├─ target layer
      ├─ execution
      ├─ effect
      └─ verification
      │
      ▼
RC-TARGET-LAYER-001
      +
RC-INSTRUMENTAL-TRIGGER-END-001
      │
      ▼
DOUBT / R-F-R
      │
      ▼
USER REVIEW
```

## Counting law

```text
Existing 3,204 parameters modified        0
New canonical parameters                  0
Explicitly enumerated container regions  28
Source-declared container count          30
Action-mode highlighted regions          12
New reasoning-operation candidates        2
```

The `30 vs 28` discrepancy is deliberately retained as an unresolved source-internal count finding.

## Promotion barrier

Neither candidate is a new native parameter yet. Promotion requires repeated cross-domain examples, contradiction/counter-case testing, R-F-R and explicit review.
