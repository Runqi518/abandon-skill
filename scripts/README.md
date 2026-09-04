# Phase Two / 阶段二

`guard.py` is a non-blocking placeholder in version 1.1. A future host-specific
hook may call its implementation before content is written to disk. Until then,
the skill must not register hooks or imply that guard mode is active.

`install.py` installs the canonical Agent Skill for Claude Code, Codex,
ChatGPT, OpenCode, or a custom Agent Skills directory. It links by default so
repository updates are immediately visible and copies only with `--copy`.
