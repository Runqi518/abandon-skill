# Abandon Skill Specification

This file is the single source of truth for categories, severity, thresholds,
language routing, provenance labels, and machine output.

## Categories

| ID | 中文 | English | Meaning |
|---|---|---|---|
| `cliche` | 陈词滥调 | cliché | Stock phrases that substitute familiarity for information. |
| `inflation` | 夸大拔高 | inflation | Unsupported superlatives, sweeping claims, or grand framing. |
| `vagueness` | 模糊空转 | vagueness | Claims without an actor, action, object, evidence, or deadline. |
| `meta` | 元话语 | meta discourse | Narration about explaining, noting, or structuring instead of content. |
| `structure` | 模板结构 | templated structure | Repetitive headings, triplets, canned openings, and canned conclusions. |
| `rhetoric` | 修辞堆叠 | rhetorical padding | Contrast frames, rhetorical questions, and decorative transitions. |
| `jargon` | 黑话 | jargon | Abstract business or technical nouns with no operational meaning. |
| `translation` | 翻译腔 | translationese | Source-language syntax or literal collocations unnatural in the target. |
| `punctuation` | 标点指纹 | punctuation fingerprint | Repeated em dashes, scare quotes, or colon-heavy fragments. |

## Severity

| Level | Weight | Rule |
|---|---:|---|
| `low` | 1 | Mild tell; report only when repeated or co-occurring. |
| `medium` | 2 | Noticeable generic phrasing; rewrite unless context justifies it. |
| `high` | 3 | Strong template/fingerprint or a cluster that damages credibility. |

Literal and regex records define their own severity. A paragraph containing
three or more distinct non-exempt tell IDs receives one additional `high`
`structure` finding named `paragraph-cooccurrence`. Duplicate matches with the
same rule, paragraph, and exact span are emitted once.

## Language Routing

Count CJK Unified Ideographs among letters and digits:

- ratio greater than `0.30`: load Chinese rules;
- ratio from `0.10` through `0.30`: mixed, load Chinese and English rules;
- ratio below `0.10`: load English rules.

The selected genre profile always loads and may contain both languages.

## Merge Order

1. General language base.
2. One selected genre profile.
3. Personal `teach-vocabulary.md`.
4. Personal `teach-allow-list.md`, which always wins.

Rules are deduplicated by normalized literal or regex pattern. Later metadata
replaces earlier metadata. Allow entries suppress literal and regex findings
whose matched text is fully covered by the allow entry.

## Provenance Labels

- `prior`: a known model-family or generic generation fingerprint.
- `prompt-induced`: wording plausibly elicited by the supplied prompt.
- `translation`: a cross-language transfer pattern.

Every finding has at least one label. If a rule carries `translation`, retain
it. If `--prompt-file` contains a matching inducement family, prepend
`prompt-induced`; otherwise use the rule's declared provenance, normally
`prior`. These labels are hypotheses, never proof of model authorship.

## Rule Blocks

Markdown reference files expose machine-readable pipe-separated blocks:

```text
<!-- abandon:terms -->
id|category|severity|provenance|literal
<!-- /abandon:terms -->
```

Regex blocks use the same fields and Python regular-expression syntax between
`abandon:regex` markers. Allow blocks contain one literal per line between
`abandon:allow` markers. Blank lines and lines beginning with `#` are ignored.
The five fields may not contain `|`.

## Stable JSON Schema

The engine emits UTF-8 JSON with sorted keys, deterministic finding order, and
the following shape. Line and paragraph numbers are one-based; offsets are
zero-based Unicode code-point offsets in the original input.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["schema_version", "language", "genre", "summary", "readiness", "findings"],
  "properties": {
    "schema_version": {"const": "1.0"},
    "language": {"enum": ["zh", "en", "mixed"]},
    "genre": {"type": ["string", "null"]},
    "summary": {
      "type": "object",
      "additionalProperties": {"type": "integer", "minimum": 0}
    },
    "readiness": {"enum": ["clean", "light", "heavy"]},
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["rule_id", "category", "severity", "paragraph", "line", "quote", "start", "end", "provenance", "source"],
        "properties": {
          "rule_id": {"type": "string"},
          "category": {"type": "string"},
          "severity": {"enum": ["low", "medium", "high"]},
          "paragraph": {"type": "integer", "minimum": 1},
          "line": {"type": "integer", "minimum": 1},
          "quote": {"type": "string"},
          "start": {"type": "integer", "minimum": 0},
          "end": {"type": "integer", "minimum": 0},
          "provenance": {"type": "array", "items": {"enum": ["prior", "prompt-induced", "translation"]}},
          "source": {"type": "string"}
        }
      }
    }
  }
}
```

Readiness uses weighted findings after exemptions: `clean` for 0-2 points,
`light` for 3-8, and `heavy` for 9 or more. The co-occurrence finding counts
as three points.
