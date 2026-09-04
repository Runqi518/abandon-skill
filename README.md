# Abandon Skill Anti-Slop

中文 | [English](#english)

一个跨平台、双语的去 AI 腔 Agent Skill，定位并修复可观察的模板化表达。
同一套 skill 和确定性引擎可用于 Claude Code、Codex、ChatGPT、OpenCode，
以及兼容 [Agent Skills](https://agentskills.io) 标准的其他智能体。

## 四维设计

- **场景**：通用文本自动回退，并优化小红书、PRD/技术文档、周报、Commit/PR、邮件。
- **环节**：写前 prompt-audit、写后 rewrite/report/score；写中 guard 留待阶段二。
- **溯源**：`prior`、`prompt-induced`、`translation`，仅作启发式判断。
- **漂移**：teach 写入用户配置目录，升级 skill 不会覆盖。

## 平台支持

| 平台 | 形式 | 调用方式 |
|---|---|---|
| Claude Code | 原生插件或个人 skill | `/abandon-skill:abandon-slop` 或 `/abandon-slop` |
| Codex CLI / IDE | Agent Skill | `$abandon-slop`，也支持隐式触发 |
| ChatGPT desktop | Agent Skill | 从 Skills 选择 `Abandon Skill` |
| OpenCode | Agent Skill | 根据描述自动触发，或明确要求使用 `abandon-slop` |
| 其他兼容客户端 | Agent Skills 标准目录 | 按客户端方式调用 |

规则、脚本和 references 只维护在 `skills/abandon-slop/` 一处，各平台不复制
业务规则。

## 一键安装

在仓库根目录执行：

```bash
python3 scripts/install.py --target all
```

默认创建符号链接：

```text
~/.claude/skills/abandon-slop   # Claude Code
~/.agents/skills/abandon-slop   # Codex、ChatGPT、OpenCode
```

因此在桌面仓库修改并 `git pull` 后，已安装的 skill 自动使用最新内容。若环境
不支持符号链接，可复制安装：

```bash
python3 scripts/install.py --target all --copy
```

复制安装更新时需要执行：

```bash
python3 scripts/install.py --target all --copy --force
```

只安装某个平台：

```bash
python3 scripts/install.py --target claude
python3 scripts/install.py --target codex
python3 scripts/install.py --target chatgpt
python3 scripts/install.py --target agents
python3 scripts/install.py --target opencode
python3 scripts/install.py --destination /path/to/custom/skills
```

OpenCode 已能读取 `~/.agents/skills`，因此 `--target all` 不再额外创建一份
OpenCode 副本；`--target opencode` 用于偏好其原生配置目录的用户。安装后若
客户端没有立即发现 skill，请重启对应客户端。

## Claude Code 插件模式

无需安装即可从克隆目录运行：

```bash
claude --plugin-dir "$HOME/Desktop/abandon-skill"
```

调用示例：

```text
/abandon-skill:abandon-slop 把下面这段去去 AI 味：...
/abandon-skill:abandon-slop report：哪里有 AI 味？...
/abandon-skill:abandon-slop score：这段能发吗？...
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

## 确定性引擎

检测器只依赖 Python 3：

```bash
python3 skills/abandon-slop/scripts/slop_count.py --text "值得注意的是，这项能力将赋能团队。" --genre doc-prd
python3 skills/abandon-slop/scripts/slop_count.py --file draft.md --genre weekly-report
python3 skills/abandon-slop/scripts/slop_count.py --teach-add "颗粒度对齐" --category jargon
python3 skills/abandon-slop/scripts/slop_count.py --allow-add "项目约定术语"
```

引擎是 bundled profile 和个人词表的唯一解析器。输出遵循
`skills/abandon-slop/references/spec.md`，按输入位置稳定排序。个人数据默认位于：

```text
~/.config/abandon-slop/teach-vocabulary.md
~/.config/abandon-slop/teach-allow-list.md
```

可通过 `ABANDON_SLOP_CONFIG_DIR` 修改位置。旧版
`~/.claude/config/abandon-slop/` 词表仍会读取。合并顺序为通用底盘、场景
profile、旧版个人词表、新版个人词表，allow-list 永远优先。

## 项目结构

```text
abandon-skill/
├── .claude-plugin/plugin.json       # Claude Code 插件清单
├── skills/abandon-slop/             # 唯一、可移植的标准 skill
│   ├── SKILL.md
│   ├── agents/openai.yaml           # Codex / ChatGPT 展示与策略
│   ├── scripts/slop_count.py        # 零依赖确定性引擎
│   └── references/                  # 规范、词表、溯源和场景 profiles
├── scripts/install.py               # 跨平台本地安装器
├── scripts/guard.py                 # 阶段二占位
└── shared/README.md                  # 旧布局迁移说明
```

## English

Abandon Skill is a bilingual, cross-platform Agent Skill for detecting and
rewriting observable AI-slop patterns. One canonical skill supports Claude
Code, Codex, ChatGPT, OpenCode, and other Agent Skills-compatible clients.

Install it with `python3 scripts/install.py --target all`. Claude Code can also
load the repository as a native plugin with
`claude --plugin-dir "$HOME/Desktop/abandon-skill"`. Codex invokes it as
`$abandon-slop`; compatible clients may activate it implicitly from its
description.

The deterministic engine requires only Python 3. See
`skills/abandon-slop/references/spec.md` for its output contract and
`skills/abandon-slop/references/drift.md` for persistence rules.
