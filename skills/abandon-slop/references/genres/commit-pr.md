# Commit And PR Descriptions / 提交与合并请求

<!-- abandon:terms -->
pr-001|vagueness|medium|prior|various improvements
pr-002|vagueness|medium|prior|minor fixes
pr-003|meta|medium|prior|this PR aims to
pr-004|inflation|medium|prior|significantly enhances
pr-005|vagueness|medium|prior|优化相关逻辑
pr-006|vagueness|medium|prior|修复一些问题
<!-- /abandon:terms -->

<!-- abandon:regex -->
pr-r01|structure|medium|prior|(?:key changes|主要改动)[：:]?\s*(?:\n[-*].*){4,}
pr-r02|meta|low|prior|(?:in this (?:commit|pull request)|在本次(?:提交|改动)中)
<!-- /abandon:regex -->

Conventional Commit types, repository vocabulary, issue IDs, test commands,
and required PR-template headings are exempt. Rewrite around behavior, reason,
tests, and risk; do not turn a one-line fix into release marketing.

<!-- abandon:allow -->
feat:
fix:
BREAKING CHANGE
<!-- /abandon:allow -->
