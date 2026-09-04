# 中文通用底盘 / Chinese Base Tells

机器记录格式见 `spec.md`。只有标记块由引擎读取；其余文字供改写时参考。

<!-- abandon:terms -->
zh-001|meta|medium|prior|值得注意的是
zh-002|meta|low|prior|需要指出的是
zh-003|cliche|medium|prior|在当今快速发展的时代
zh-004|cliche|medium|prior|毋庸置疑
zh-005|inflation|medium|prior|至关重要
zh-006|inflation|high|prior|彻底改变
zh-007|vagueness|medium|prior|赋能
zh-008|vagueness|medium|prior|助力
zh-009|jargon|medium|prior|形成闭环
zh-010|jargon|medium|prior|抓手
zh-011|jargon|medium|prior|方法论
zh-012|rhetoric|medium|prior|不仅仅是
zh-013|rhetoric|medium|prior|更是一种
zh-014|structure|low|prior|首先
zh-015|structure|low|prior|其次
zh-016|structure|low|prior|最后
zh-017|translation|medium|translation|这意味着什么
zh-018|translation|medium|translation|让我们深入探讨
zh-019|cliche|low|prior|总而言之
zh-020|vagueness|medium|prior|持续发力
<!-- /abandon:terms -->

<!-- abandon:regex -->
zh-r01|rhetoric|high|prior|不是.{0,30}而是
zh-r02|structure|medium|prior|一方面.{0,80}另一方面
zh-r03|punctuation|medium|prior|——.{0,80}——
zh-r04|inflation|medium|prior|前所未有(?:的)?
zh-r05|vagueness|medium|prior|进一步(?:提升|加强|推动|优化)
<!-- /abandon:regex -->

## 修复配方

- 删除元话语，直接写事实。
- 把“赋能、助力、推动”改成明确的主语、动作和结果。
- 把无证据的最高级改为可核查数字，拿不出证据就删。
- 拆掉“不是 X，而是 Y”模板，保留真正需要的判断。
- 连续“首先、其次、最后”只在顺序确实重要时保留。

<!-- abandon:allow -->
<!-- /abandon:allow -->
