---
name: abandon-slop
description: Detects and removes AI slop in Chinese or English writing using genre, writing stage, provenance, and personal vocabulary drift. Use when the user says 去去AI味、去 AI 味、humanize、less AI、哪里有AI味、flag the slop、AI味重吗、能发吗, asks whether a prompt will produce AI-like prose, or teaches phrases to flag or allow.
compatibility: Works with Agent Skills clients including Claude Code, Codex, ChatGPT, and OpenCode; Python 3 enables deterministic scoring and teach persistence.
metadata:
  display-name: Abandon Skill
  display-name-zh: 摒弃 AI 腔
  version: "1.1.0"
---

# Abandon Skill / 摒弃 AI 腔

Remove detectable generation habits without flattening the author's voice.
Treat provenance as a hypothesis, never proof that a model wrote the text.

## Locate Resources

Set `SKILL_ROOT` to the directory containing this `SKILL.md`. Resolve every
resource relative to it; do not assume a particular host or working directory:

- Contract: `references/spec.md`
- Engine: `scripts/slop_count.py`
- Drift rules: `references/drift.md`
- General rules: `references/tells-zh.md` and `references/tells-en.md`
- Genres: `references/genres/README.md`
- Provenance: `references/provenance.md`
- Prompt audit: `references/prompt-audit.md`

Read `references/spec.md` first. Load only references required by the selected
mode, detected language, and one genre. Do not load every profile.

## Select One Mode

| Mode | Stage | Trigger examples | Output |
|---|---|---|---|
| `rewrite` (default) | after | 去去AI味, less AI, humanize | Rewritten text only |
| `report` | after | 哪里有AI味, flag the slop | Located findings |
| `score` | after | AI味重吗, 能发吗 | Counts and readiness |
| `prompt-audit` | before | 这个 prompt 会不会写出 AI 味 | Risks and rewritten prompt |
| `teach` | drift | 这个词也是 slop, 这个词别再标 | Persist and confirm |
| `guard` | during | Hook, no phrase required | Phase two; report unavailable |

Explicit mode words win. If the request asks to change prose, use `rewrite`.
If it asks only for diagnosis, do not rewrite. If ambiguous, default to
`rewrite`; do not ask a routing question.

## Determine Input, Language, And Genre

1. Use text in the message, an attached file, or the path the user names.
2. Honor an explicitly named genre.
3. Otherwise apply `references/genres/README.md`; choose no genre when unsure.
4. Let the engine detect language. Mixed content loads both language bases.
5. Preserve Markdown, links, code, names, numbers, quotations, and required
   templates unless the user asks otherwise.

For `report`, `score`, and pre-rewrite diagnosis, run:

```bash
python3 "<SKILL_ROOT>/scripts/slop_count.py" --file INPUT [--genre GENRE]
```

For prompt-aware provenance, save the prompt separately and append
`--prompt-file PROMPT`. The JSON is stable and authoritative for deterministic
matches. Add a semantic finding only when you can quote exact text and map it
to a category in `references/spec.md`.

If the host cannot execute Python, `rewrite`, `report`, and `prompt-audit` may
continue from the loaded references. Do not fabricate deterministic counts:
state that `score` requires Python 3. `teach` requires local file and Python
access; explain that limitation instead of pretending persistence succeeded.

## Rewrite

1. Run the detector; inspect clusters, not isolated common words.
2. Read the selected language base's repair recipes and selected genre profile.
3. Remove throat-clearing, canned transitions, unsupported elevation, false
   symmetry, repetitive conclusions, and abstract verbs.
4. Restore an actor, action, object, evidence, limit, or date where supplied.
   Never invent facts to make vague prose sound concrete.
5. Vary sentence shape only where it improves natural rhythm. Preserve useful
   repetition, domain terms, intentional voice, and genre conventions.
6. Re-run the detector. Remaining matches are acceptable only when quoted,
   required, or more natural than the alternative.
7. Return only the rewritten text. No preface, score, changelog, apology, or
   fenced block unless the input itself is code-fenced.

## Report

Return findings in source order. Each item must contain:

```text
[severity] category · paragraph/line · provenance
“exact quote”
Why it reads as slop; concise repair direction.
```

Use Chinese labels for Chinese requests and English labels for English
requests. Include deterministic and justified semantic findings. Do not claim
authorship. If there are none, say the text has no material slop findings.

## Score

Run the engine and return:

```text
就绪度/Readiness: clean | light | heavy
类别/Category: count
一句结论/One-line verdict: 是否可直接发布及首要修改点
```

Use the engine's readiness exactly. Do not present a fake probability that AI
wrote the text. “Clean” means no material style signal, not guaranteed human
authorship or factual quality.

## Prompt Audit

Load only `references/prompt-audit.md` and `provenance.md`.

1. Quote every inducing phrase.
2. Name its likely category and effect.
3. Preserve the prompt's task, facts, audience, and hard constraints.
4. Replace vague style adjectives with observable requirements.
5. Return the short risk list, then the rewritten prompt in a fenced block.
6. Do not generate the requested deliverable unless separately asked.

## Teach

Interpret “这个词也是 slop / flag this phrase” as a tell and “这个词别再标 /
allow this phrase” as an exemption. If the exact phrase is unclear, ask for it.
Otherwise call exactly one engine mutation:

```bash
python3 "<SKILL_ROOT>/scripts/slop_count.py" --teach-add "PHRASE"
python3 "<SKILL_ROOT>/scripts/slop_count.py" --allow-add "PHRASE"
```

Optional tell metadata: `--category`, `--severity`, `--provenance`. Use defaults
unless the user clearly supplies them. For “forget/remove”, use
`--teach-remove` or `--allow-remove`. Never edit bundled vocabulary. Return a
one-line confirmation with action, phrase, and destination from engine JSON.

## Guard

Guard is reserved for phase two. Do not create or enable hooks. If invoked,
say that guard is not implemented and offer `score` on the current text.

## Quality Bar

- An uncommon word is not slop by itself; context and clustering matter.
- Genre exemptions and personal allow-list always win.
- Keep meaning, commitments, facts, uncertainty, and authorial stance intact.
- Do not make every sentence short, casual, or quirky merely to evade tells.
- Never replace one cliché with another or fabricate anecdotes and metrics.
