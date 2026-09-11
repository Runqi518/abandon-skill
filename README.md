# Abandon Skill

Abandon 是 AI 输出后的认知剪枝器。它围绕用户真实目标删除低贡献、冲突、重复或增加认知负担的内容，同时保护事实、硬约束、重大风险和必要不确定性。

除本说明文档外，Skill 的运行指令、参考资料、模板和脚本全部使用英文。

## 目录结构

```text
abandon/
├── SKILL.md
├── README.md
├── assets/
│   └── REQUEST_TEMPLATE.md
├── references/
│   ├── EXAMPLES.md
│   ├── MODES.md
│   └── SCORING.md
└── scripts/
    └── validate.py
```

`SKILL.md` 是运行入口。其余文件按需加载，避免 Skill 激活时占用过多上下文。

## 安装

将整个 `abandon` 文件夹复制到以下任一位置：

```text
# OpenCode 项目级
.opencode/skills/abandon/

# OpenCode 全局
~/.config/opencode/skills/abandon/

# Agent Skills 兼容目录
.agents/skills/abandon/
```

安装后重启客户端。

## 使用方式

```text
Use abandon to prune the previous answer with balanced intensity.
```

```text
Use abandon in focus mode. Optimize for helping an executive make a go/no-go decision.
```

```text
Use abandon in compare mode to combine these three candidate answers.
```

## 模式

| 模式 | 用途 |
| --- | --- |
| `prune` | 删除低价值内容并输出最终答案 |
| `explain` | 输出答案及舍弃原因 |
| `compare` | 比较候选答案并融合最优部分 |
| `compress` | 在保护关键约束的前提下压缩 |
| `focus` | 围绕一个指定目标重新剪枝 |
| `teach` | 从明确反馈中学习当前偏好 |
| `guard` | 对当前生成结果静默执行剪枝 |
