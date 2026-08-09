# P2-AI Review 01 — Capability Family Crosswalk

Status: `REVIEW FINDINGS ONLY — NO ADOPTION`

Source: `raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md`

The 74-family map is useful as a **Human-container crosswalk**, but it must not become the AI-native hierarchy as-is.

## Lock

```text
AI NATIVE RUBRIC
≠
HUMAN CONTAINER CROSSWALK
```

Human `CON-xxx` links describe functional resemblance. They do not prove that an AI capability has the same mechanism, state model, learning rule, ownership, embodiment or failure mode as the Human container.

## Structural findings

### A. Composite/outcome families should not be mistaken for primitives

Flag for layer review:

- `AI-CAP-001` General intelligence composite and cross-domain performance — aggregate/composite.
- `AI-CAP-072` Research productivity and R&D acceleration — system outcome/productivity effect.

These may remain registry objects, but their type should be `COMPOSITE/OUTCOME`, not automatically `NATIVE_PRIMITIVE_CAPABILITY`.

### B. Governance/evaluation/runtime-policy families need their own layer

Flag for classification review:

- `AI-CAP-057` Scalable oversight and weak-to-strong supervision.
- `AI-CAP-060` Refusal, classifier, and fallback management.
- `AI-CAP-063` Benchmark integrity and cheating resistance.
- `AI-CAP-065` Transparency and external disclosure.
- `AI-CAP-066` Response-length and verbosity control.

These may be real AI system capabilities, but they are not necessarily cognitive primitives. Keep `CAPABILITY_LAYER` explicit.

### C. Training-time and runtime adaptation must remain separate

Potential cluster:

- `AI-CAP-045` Learning from feedback and few-shot adaptation.
- `AI-CAP-046` Continual and lifelong learning.
- `AI-CAP-073` Model training, optimization, and meta-learning.

Phase-1 already locked the distinction between runtime context/memory/config writes and actual model-weight training. The AI-native rubric must preserve that boundary.

### D. Failure/recovery families overlap and require precise boundaries

Potential overlap cluster:

- `AI-CAP-009` Debugging, diagnosis, and error correction.
- `AI-CAP-026` Self-correction and iterative refinement.
- `AI-CAP-052` Failure detection and recovery.
- `AI-CAP-068` Production reliability, recovery, and quality assurance.

Do not merge automatically. Phase-2 must define whether these represent:

```text
DETECTION
DIAGNOSIS
LOCAL CORRECTION
RECOVERY
RETRY / RE-SEQUENCE
SYSTEM RELIABILITY / QA
```

### E. Safety/control families overlap but act at different points

Potential cluster:

- `AI-CAP-023` Safety refusal and harm avoidance.
- `AI-CAP-053` Security, adversarial robustness, and attack resistance.
- `AI-CAP-055` Alignment with external rules and policies.
- `AI-CAP-060` Refusal, classifier, and fallback management.
- `AI-CAP-062` Destructive-action control and execution safety.

These should be separated by Sequence role: input threat detection, rule/constraint qualification, decision inhibition, tool/action barrier, and post-action verification/recovery.

### F. `AI-CAP-067` is over-bundled

`Self-report, model-welfare, and simulated affect` contains at least three distinct concepts:

```text
SELF-REPORT / REPORTABILITY
MODEL-WELFARE EVALUATION CONSTRUCT
SIMULATED AFFECT / AFFECTIVE REPRESENTATION
```

Hold for split review. No assumption should be made that simulated affect implies subjective experience.

### G. Several primary-container cells are syntactically mixed mappings

Require normalization before machine adoption:

- `AI-CAP-007`: primary cell begins `CON-007` but text says code functions map primarily to `CON-048 + CON-035`.
- `AI-CAP-012`: primary cell mixes `CON-012` with an arrow to `CON-039`.
- `AI-CAP-062`: primary cell contains `CON-006 + CON-029` rather than one clearly typed primary relation.
- `AI-CAP-072`: primary cell begins `CON-006` but points to `CON-047 + CON-078`.

The source row is preserved unchanged. The future machine crosswalk should parse these as review issues, not silently choose one interpretation.

### H. Biological analogies must remain analogies

Mappings into Human biological/body containers such as `CON-006`, `CON-007`, `CON-012`, `CON-015`, etc. can be useful functional analogies, but must carry a relation type such as:

```text
FUNCTIONAL_ANALOGY
```

rather than:

```text
MECHANISTIC_IDENTITY
```

## Proposed AI-native layer classes for Phase-2 review

These are classification buckets for review, not approved AI parameters:

```text
CORE_REASONING
KNOWLEDGE_RETRIEVAL
MEMORY_STATE
PERCEPTION_GROUNDING
LANGUAGE_COMMUNICATION
PLANNING_CONTROL
TOOL_EXECUTION
SOCIAL_MODELING
VALUE_RISK_SAFETY
SELF_MONITORING
LEARNING_ADAPTATION
TRAINING_OPTIMIZATION
SECURITY_ROBUSTNESS
EVALUATION_OVERSIGHT
SYSTEM_RELIABILITY
POLICY_OUTPUT_CONTROL
COMPOSITE_OUTCOME
```

## Next review operation

For each `AI-CAP-001..074`, Phase-2 must assign:

```text
native_candidate_status:
    ACCEPT / RENAME / SPLIT / MERGE / MOVE / OMIT / HOLD

capability_layer
exact_definition
runtime_or_training
state_owned_by
controller_role
performer_role
memory_read/write
primary_sequence_roles
secondary_sequence_roles
human_crosswalk_relation_type
known_overlap_ids
source/evidence
```

No item is approved by this review.
