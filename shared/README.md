# Shared Engine Location

The canonical, portable skill now lives entirely in `skills/abandon-slop/`:

- Specification: `skills/abandon-slop/references/spec.md`
- Drift contract: `skills/abandon-slop/references/drift.md`
- Engine: `skills/abandon-slop/scripts/slop_count.py`

Keeping runtime files inside the skill follows the Agent Skills standard and
lets Claude Code, Codex, ChatGPT, OpenCode, and compatible agents install the
same directory without duplicated rules.
