# Email And External Communication / 邮件与对外沟通

<!-- abandon:terms -->
mail-001|cliche|low|prior|希望这封邮件能让您一切安好
mail-002|meta|medium|prior|冒昧打扰
mail-003|vagueness|medium|prior|请您知悉
mail-004|cliche|low|prior|I hope this email finds you well
mail-005|meta|medium|prior|I am writing to inform you that
mail-006|vagueness|medium|prior|at your earliest convenience
mail-007|inflation|medium|prior|incredibly excited
<!-- /abandon:terms -->

<!-- abandon:regex -->
mail-r01|meta|medium|prior|(?:感谢|thank you for).{0,50}(?:宝贵时间|valuable time)
mail-r02|structure|medium|prior|(?:please do not hesitate|如有任何问题.{0,20}随时)
<!-- /abandon:regex -->

Established greetings, legal language, company signatures, and culturally
required honorifics are exempt. Preserve politeness while moving the request,
owner, and deadline near the top.

<!-- abandon:allow -->
您好
Dear
Regards
此致
<!-- /abandon:allow -->
