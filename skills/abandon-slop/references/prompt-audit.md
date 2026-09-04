# Prompt Audit / 提示词审计

Audit instructions before generation. Report the inducing phrase, likely
effect, and a concrete replacement. Do not run output scoring when only a
prompt is supplied.

| Inducing wording | Risk | Better instruction |
|---|---|---|
| “更专业 / professional” | jargon and nominalization | Name the audience and required domain terms; prefer concrete verbs. |
| “更高级 / elevate” | inflated claims and decorative diction | Ask for precise, restrained wording with evidence. |
| “有感染力 / compelling” | rhetorical padding | Ask for one concrete scene, fact, or consequence. |
| “全面 / comprehensive” | exhaustive template structure | List the exact questions the response must answer. |
| “结构完整 / well-structured” | canned intro/body/conclusion | Specify sections by their job and omit an intro unless needed. |
| “详细 / in detail” | repetition and length inflation | Set a word budget and required evidence. |
| “像专家 / thought leadership” | authority theater | Specify expertise, audience, decision, and uncertainty policy. |
| “生动 / engaging” | metaphors and rhetorical questions | Request concrete nouns, active verbs, and no rhetorical questions. |
| “润色 / polish” | model defaults take over voice | Preserve voice; only fix the named defects. |
| “不要有 AI 味 / don't sound AI” | vague negative target | List forbidden patterns and desired voice samples. |

## Rewriting Template

```text
Task / 任务：<specific deliverable>
Audience / 读者：<who and what they know>
Purpose / 目的：<decision or action enabled>
Evidence / 依据：<facts that must be used; do not invent>
Voice / 语气：<2-3 observable traits plus a short sample>
Constraints / 约束：<length, structure, forbidden patterns>
Uncertainty / 不确定性：state unknowns plainly; do not fill gaps.
```

Return the risk list first, then the rewritten prompt in a fenced block. Keep
the original task and constraints; do not silently broaden scope.
