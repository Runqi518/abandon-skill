# Genre Profiles / 场景 Profiles

Choose exactly one profile. Explicit user choice wins. Otherwise infer from
the strongest path or content signal; if confidence is low, use no profile.

| Profile | Path signals | Content signals |
|---|---|---|
| `xiaohongshu` | `xiaohongshu`, `xhs`, `notes/` | 种草、同款、姐妹们、emoji-heavy product notes |
| `doc-prd` | `docs/`, `prd`, `design`, `rfc` | 背景、目标、非目标、验收标准、API、architecture |
| `weekly-report` | `weekly`, `status`, `周报` | 本周进展、下周计划、blocker, status update |
| `commit-pr` | `.git/`, PR/MR template | fix, feat, scope, testing, risk, reviewers |
| `email` | `.eml`, `mail`, `email` | subject, 收件人, Hi, Dear, Regards |

Each profile may define `terms`, `regex`, and `allow` blocks from
`../spec.md`. Genre rules merge after the language base. Profile allow
entries override both base and genre tells. Keep bilingual entries together.

Profiles should contain only genre-specific evidence. General-purpose rules
belong in `tells-zh.md` or `tells-en.md`.
