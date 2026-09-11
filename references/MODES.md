# Mode Contracts

## prune

Return only the pruned answer. Use this as the default for general answer cleanup.

## explain

Return the pruned answer followed by a compact discard log. Paraphrase discarded units instead of reproducing long passages. Give only decision-relevant reasons.

```markdown
## Pruned Answer

<final answer>

## Discarded

| Unit | Category | Reason |
| --- | --- | --- |
| <short paraphrase> | <repetition, tangent, conflict, or avoidable load> | <decisive reason> |
```

## compare

Evaluate all candidates against one demand anchor:

1. Preserve the strongest supported parts.
2. Remove low-contribution and repeated parts.
3. Resolve conflicts only when evidence permits.
4. Retain explicit uncertainty when a conflict cannot be resolved.

```markdown
## Final Answer

<merged answer>

## Selection Notes

<decisive differences, conflicts, and reasons only>
```

## compress

Reduce length and structure without losing key conclusions, hard constraints, necessary reasoning, material risks, or actionability. Prefer deletion and sentence merging over vague paraphrasing.

## focus

Re-prune around one specified target. Keep secondary material only when it is a prerequisite, constraint, risk, or direct support for that target. Ask one concise question if the target is missing and cannot be reliably inferred.

## teach

Infer a local preference rule only from explicit retain/discard feedback. State the rule before applying it:

```text
Preference learned: <concise, testable, evidence-bounded rule>
```

Do not treat one ambiguous reaction as a durable preference.

## guard

Apply the complete pipeline silently before returning the current answer. Output only the guarded answer. A skill invocation is not a persistent runtime hook; the host application or plugin must invoke this mode after every generation if continuous guarding is required.
