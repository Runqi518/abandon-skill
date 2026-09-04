# Provenance Heuristics / 溯源启发式

Labels estimate where a tell may have entered the text. They do not identify an
author or prove that AI was used. Prefer cautious wording when evidence is
weak, while machine findings use the three labels in `spec.md`.

## Model-Prior Fingerprints

| Family | Typical fingerprints | Confidence limits |
|---|---|---|
| GPT-like | `delve`, `tapestry`, `realm`, `underscore`, polished triplets, “not merely X but Y” | Common in edited human prose too. Never attribute from one match. |
| Claude-like | repeated em dashes, “It's worth noting”, balanced caveats, `nuanced`, long contrast clauses | House style and user preference can produce the same traits. |
| Generic LLM | canned openings/conclusions, exhaustive symmetry, unsupported elevation, uniformly smooth transitions | Stronger as a paragraph-level cluster than as isolated words. |

## Prompt-Induced Features

Mark `prompt-induced` when the prompt explicitly asks for traits that appear in
the output: “professional”, “comprehensive”, “engaging”, “elevate”, “有感染力”,
“高级”, “结构完整”, “面面俱到”, “文采好”. A prompt term is causal evidence only
for its feature family, not for every finding in the output.

## Translation Features

Mark `translation` for literal source-language syntax: heavy nominalization,
repeated “进行 + noun”, unnecessary pronouns, “make a contribution to”,
“under the background of”, “这意味着什么”, or English information order copied
into Chinese. Confirm against the target language's natural usage and preserve
terms of art.

## Decision Order

1. Use a rule's explicit `translation` label when present.
2. Add `prompt-induced` when prompt evidence matches the same category.
3. Otherwise use `prior` for known generation fingerprints.
4. In human-facing reports, phrase labels as “可能来源” rather than authorship.
