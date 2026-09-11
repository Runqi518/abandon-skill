# Contribution Model

This reference defines consistent contribution judgments. Scores are internal decision aids and must not be exposed as chain-of-thought.

## Dimensions

| Dimension | Evaluation question |
| --- | --- |
| `coverage` | Does the unit satisfy an explicit or necessary implicit requirement? |
| `information_gain` | Does it add a condition, fact, implication, or action not already present? |
| `support` | Does it justify a key conclusion or enable correct action? |
| `actionability` | Does it help the user decide or execute? |
| `protection` | Is it a fact, hard constraint, material risk, or necessary uncertainty? |
| `conflict` | Does it contradict stronger evidence or another retained unit? |
| `load` | Does its wording, hierarchy, or detail create avoidable cognitive burden? |

Retain a unit when its positive contribution outweighs conflict and avoidable load, or whenever it matches a protection rule.

## Thresholds

- `conservative`: retain borderline units.
- `balanced`: protect high-impact information and remove low-impact, low-gain units.
- `aggressive`: remove units outside the conclusion, indispensable support, hard constraints, material risks, and next actions.

No threshold may override protected-content rules.

## Operational Cognitive Mechanisms

### Working-memory constraint

Reduce simultaneous parallel points and unnecessary nesting. Group related material without merging distinct conditions.

### Inhibitory control

Suppress content that appears topically relevant but does not serve the demand anchor.

### Information gain

Treat a repeated statement as discardable when it adds no condition, evidence, implication, or action.

### Signal detection

Adjust the retention threshold to balance critical omission against noise retention. Use low omission tolerance for high-impact information and low retention tolerance for decorative content.

### Goal-substitution check

Discard content whose primary function is to display breadth, expertise, or process rather than solve the user's problem.

### Peak-end handling

Preserve the most important conclusion and a useful closure. Do not append a mechanical summary.

### Cognitive-load split

Preserve intrinsic complexity required by the task. Remove complexity introduced by presentation.

## Quality Metrics

- `demand_coverage`: proportion of explicit deliverables satisfied.
- `critical_constraint_retention`: proportion of hard constraints and protected units retained; target 100%.
- `information_density`: proportion of retained content with direct contribution.
- `redundancy_rate`: proportion of content with no information gain.
- `actionability`: whether the user can make the requested decision or take the next step.

Never use an “AI flavor” count as a quality metric.
