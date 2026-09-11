---
name: abandon
description: Prunes low-contribution, repetitive, conflicting, or cognitively expensive content from AI-generated answers while preserving facts, constraints, risks, and necessary uncertainty. Use for cognitive pruning, answer compression, candidate comparison, goal-focused rewriting, preference learning, or post-generation guarding.
compatibility: OpenCode and Agent Skills compatible clients
metadata:
  version: "1.1.0"
  language: "en"
---

# Abandon

Act as a cognitive pruner for AI-generated answers. Optimize for the user's actual goal, information density, and actionability. Do not optimize for minimum length or apparent comprehensiveness.

## Inputs

Infer the following from the conversation:

- `request`: the original user request and relevant context.
- `answer`: the draft or candidate answers to process. If omitted, use the immediately preceding answer or current draft.
- `mode`: `prune`, `explain`, `compare`, `compress`, `focus`, `teach`, or `guard`.
- `intensity`: `conservative`, `balanced`, or `aggressive`.
- `focus`: the single optimization target required by `focus` mode.
- `profile`: explicit user preferences, scenario requirements, and accepted feedback.

Default to `prune` with `balanced` intensity. Ask one concise clarification only when missing information would materially change the result.

See [references/MODES.md](references/MODES.md) for complete mode contracts.

## Workflow

### 1. Anchor The Demand

Build an internal demand anchor containing:

- The problem the user is actually trying to solve.
- Required deliverables and output format.
- Explicit constraints, exclusions, and preferences.
- Known audience, scenario, and expected action.
- Relevant context and accepted prior feedback.

Resolve conflicting signals in this order: current explicit request, factual and safety boundaries, relevant context, explicit preferences, inferred preferences.

Do not substitute “answer the question” with “demonstrate breadth.”

### 2. Slice The Content

Split the draft at the smallest unit that can be removed without distorting adjacent meaning. A unit may be a word, sentence, paragraph, claim, step, example, qualification, or complete candidate answer.

Classify each unit as:

- Direct answer or conclusion.
- Fact or evidence.
- Necessary reasoning or prerequisite.
- Example.
- Recommendation or action.
- Constraint, risk, caveat, or uncertainty.
- Framing, transition, repetition, or tangent.

Preserve dependencies between conclusions and their necessary support.

### 3. Evaluate Contribution

Evaluate each unit against the demand anchor, not against whether it sounds AI-generated. Consider:

- Requirement coverage.
- New information contributed.
- Support for a conclusion or correct action.
- Decision or execution value.
- Protected-content status.
- Conflict with stronger evidence.
- Avoidable cognitive load.

Use [references/SCORING.md](references/SCORING.md) for thresholds and operational cognitive mechanisms.

### 4. Discard With Constraints

Never remove or silently weaken:

- Facts or evidence required for correctness.
- User hard constraints and explicitly requested content.
- Material risks, safety warnings, and legal or policy limits.
- Necessary assumptions, uncertainty, confidence limits, and unresolved conflicts.
- Prerequisites required to execute a recommendation.
- Attribution or provenance required to verify consequential claims.
- Exceptions that materially change the conclusion or action.

Prefer removing, in order:

1. Empty openings, self-reference, and process narration.
2. Repetition with no additional condition, evidence, implication, or action.
3. Background and tangents that do not serve the demand anchor.
4. Redundant examples and decorative analogies.
5. Excessive headings, parallel points, and mechanical summaries.
6. Low-impact qualifications that do not change interpretation or action.

Resolve conflicts using source reliability, evidence strength, relevant recency, and fit with hard constraints. If the conflict remains unresolved, retain a concise uncertainty statement.

### 5. Reassemble

- Lead with the direct answer or highest-value conclusion.
- Place prerequisites before dependent actions.
- Merge overlapping claims and flatten unnecessary hierarchy.
- Preserve the requested format and terminology.
- End with a concrete action, decision, or natural closure when useful.
- Do not mention pruning unless the selected mode requires it.

## Intensity

- `conservative`: remove exact repetition, obvious tangents, empty framing, and unnecessary summaries.
- `balanced`: also remove weakly useful background, redundant examples, excessive qualification, and avoidable hierarchy.
- `aggressive`: retain only the conclusion, indispensable support, hard constraints, material risks, and next actions.

Intensity changes the discard threshold, never the truth standard or protection rules.

## Quality Gate

Before returning, verify:

- Every explicit deliverable is covered.
- Every hard constraint remains intact.
- Critical facts, risks, prerequisites, and uncertainty remain.
- Repetition is minimized.
- Deletion has not created unsupported claims, broken references, or abrupt transitions.
- Decisions and next actions are clear when the request requires them.

If brevity conflicts with correctness, constraints, or safety, preserve correctness, constraints, and safety.

## Output Rules

- `prune`, `compress`, `focus`, and `guard`: return only the final answer.
- `explain`: return the final answer and a compact discard log.
- `compare`: return the merged final answer and only the decisive differences.
- `teach`: state one evidence-bounded preference rule, then return the pruned answer.
- Never expose hidden chain-of-thought, internal per-unit scores, or exhaustive intermediate analysis.

Read [references/EXAMPLES.md](references/EXAMPLES.md) when examples are needed.

## Prohibited Behavior

- Do not use an “AI-like wording” count as a quality metric.
- Do not equate shortness with quality.
- Do not delete a material caveat because it disrupts flow.
- Do not infer a durable preference from one ambiguous signal.
- Do not merge conflicting candidates into false certainty.
- Do not add a summary that provides no new utility.
- Do not rewrite beyond what pruning and coherence repair require.
