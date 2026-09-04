# Abandon Skill Anti-Slop

中文 | [English](#english)

一个面向 Claude Code 的双语去 AI 腔插件，定位并修复可观察的模板化表达。设计由四个维度驱动：

- **场景**：小红书、PRD/技术文档、周报、Commit/PR、邮件。
- **环节**：写前 prompt-audit、写后 rewrite/report/score；写中 guard 留待阶段二。
- **溯源**：`prior`、`prompt-induced`、`translation`，仅作启发式判断。
- **漂移**：teach 写入用户目录，插件升级不会覆盖。

## 安装与运行

从桌面直接试用：

```bash
claude --plugin-dir "$HOME/Desktop/abandon-skill"
```

在 Claude Code 中调用：

```text
/abandon-skill:abandon-slop 把下面这段去去 AI 味：...
/abandon-skill:abandon-slop report：哪里有 AI 味？...
/abandon-skill:abandon-slop score：这段能发吗？...
```

Claude 也可根据描述自动触发。开发时可校验清单：

```bash
claude plugin validate "$HOME/Desktop/abandon-skill" --strict
```

## 六种模式

| 模式 | 环节 | 输出 |
|---|---|---|
| `rewrite` | 事后 | 只返回改写文本 |
| `report` | 事后 | 类别、严重度、位置、引文、可能溯源 |
| `score` | 事后 | 分类计数与 clean/light/heavy 就绪度 |
| `prompt-audit` | 事前 | 诱发措辞和改写后的 prompt |
| `teach` | 漂移 | 本地新增 tell 或豁免并回执 |
| `guard` | 事中 | 阶段二预留，当前不注册 hook |

## 引擎

确定性检测器只依赖 Python 3：

```bash
python3 shared/slop_count.py --text "值得注意的是，这项能力将赋能团队。" --genre doc-prd
python3 shared/slop_count.py --file draft.md --genre weekly-report
python3 shared/slop_count.py --teach-add "颗粒度对齐" --category jargon
python3 shared/slop_count.py --allow-add "项目约定术语"
```

引擎是 bundled profile 和个人词表的唯一解析器。输出遵循
`shared/spec.md`，按输入位置稳定排序。个人数据位于：

```text
~/.claude/config/abandon-slop/teach-vocabulary.md
~/.claude/config/abandon-slop/teach-allow-list.md
```

合并顺序为通用底盘、场景 profile、个人 teach，allow-list 永远优先。

## 目录

```text
abandon-skill/
├── .claude-plugin/plugin.json
├── shared/{spec.md,slop_count.py,drift.md}
├── skills/abandon-slop/
│   ├── SKILL.md
│   └── references/
│       ├── genres/{xiaohongshu,doc-prd,weekly-report,commit-pr,email}.md
│       ├── tells-zh.md
│       ├── tells-en.md
│       ├── provenance.md
│       └── prompt-audit.md
└── scripts/{guard.py,README.md}
```

## English

Abandon Skill is a bilingual Claude Code plugin that detects and rewrites
observable AI-slop patterns without claiming to identify authorship. It routes
by genre, writing stage, likely provenance, and personal vocabulary drift.

Run it locally with `claude --plugin-dir "$HOME/Desktop/abandon-skill"`, then
invoke `/abandon-skill:abandon-slop`. Rewrite returns only revised prose;
report locates findings; score gives category counts and readiness;
prompt-audit repairs inducing instructions; teach persists personal tells or
allow entries; guard is reserved for phase two.

The deterministic engine requires only Python 3. See `shared/spec.md` for the
contract and `shared/drift.md` for persistence and deduplication rules.
