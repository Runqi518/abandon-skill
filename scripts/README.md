# Phase Two / 阶段二

`guard.py` is a non-blocking placeholder in version 1.0. A future Claude Code
hook may call its implementation before content is written to disk. Until then,
the skill must not register hooks or imply that guard mode is active.
