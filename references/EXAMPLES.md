# Examples

These examples test demand alignment, conflict handling, constraint retention, and cognitive-load reduction. They are not command-execution tutorials.

## Example 1: Turn A Broad Analysis Into A Decision

### Input

```text
Request: Should we delay the public launch by two weeks? Give the product lead a decision and the decisive reasons.

Draft:
Launching products is always a complex cross-functional effort involving engineering, design, marketing, sales, support, and leadership. Many famous companies have delayed launches, while others have succeeded by moving quickly. In our case, checkout fails for 4.8% of mobile users, the incident team estimates eight days to fix it, and marketing can move the campaign at no additional cost if notified by Friday. The team has worked hard and morale matters. A launch also creates learning opportunities. Overall, there are arguments on both sides, and the decision should be made carefully.

Mode: prune
Intensity: balanced
```

### Output

```text
Delay the public launch by two weeks. The current mobile checkout failure rate of 4.8% directly threatens conversion and trust, the fix is expected within eight days, and marketing can move the campaign at no added cost if notified by Friday.
```

### Why This Is Better

It preserves the decision, evidence, timing, and cost constraint. It removes generic launch commentary, weak analogies, morale as an unsupported deciding factor, and a noncommittal conclusion.

## Example 2: Preserve Uncertainty Instead Of Inventing Certainty

### Input

```text
Request: Summarize whether the onboarding redesign improved activation.

Draft:
The redesign was clearly successful. Dashboard A reports activation rising from 41% to 49%. Dashboard B reports activation falling from 44% to 42%. The difference may come from cohort definitions, but we do not yet know. The new screens also look cleaner and several teammates prefer them. Therefore, the redesign improved activation by eight percentage points.

Mode: aggressive
```

### Output

```text
The impact on activation is unresolved. Dashboard A shows an increase from 41% to 49%, while Dashboard B shows a decline from 44% to 42%. Reconcile the cohort definitions before making a success claim.
```

### Why This Is Better

Aggressive pruning removes visual-preference commentary and the unsupported success claim, but retains the conflicting evidence and the action needed to resolve it.

## Example 3: Compare Candidates Without Averaging Away The Trade-off

### Input

```text
Request: Recommend a rollout plan that limits customer harm while producing useful evidence within one month.

Candidate A: Release to 100% of customers next Monday. This produces results fastest and avoids operational complexity.

Candidate B: Run a four-week internal test. This minimizes customer risk, but internal behavior may not predict customer behavior.

Candidate C: Release to 5% of eligible customers for one week, review support tickets and the primary success metric, then increase to 25% only if predefined guardrails hold.

Mode: compare
```

### Output

```markdown
## Final Answer

Start with 5% of eligible customers for one week. Review the primary success metric and support-ticket rate, then expand to 25% only if predefined guardrails hold. This produces customer evidence within the month while limiting initial exposure.

## Selection Notes

Candidate C best satisfies both constraints. Candidate A maximizes speed but not harm reduction; Candidate B minimizes exposure but may not produce representative customer evidence.
```

### Why This Is Better

The result selects against explicit criteria instead of combining incompatible plans or treating all candidates as equally useful.

## Example 4: Focus On The User's Decision, Not Every Available Detail

### Input

```text
Request: Rewrite this for a CFO deciding whether to renew the vendor contract.
Focus: financial decision

Draft:
The vendor was founded in 2017 and refreshed its brand identity last year. Its interface uses a modern navigation system, and the account team responds quickly. Annual cost will rise from $240,000 to $310,000. Usage has fallen 18% year over year. Replacing it would require an estimated $90,000 migration and three months of work. The current contract renews automatically in 21 days unless notice is sent. The vendor also sponsors a well-known industry conference.

Mode: focus
Intensity: balanced
```

### Output

```text
Do not allow the contract to auto-renew without renegotiation. Annual cost is increasing from $240,000 to $310,000 while usage is down 18%. Replacement would cost about $90,000 and take three months, so use the 21-day notice deadline to seek lower pricing or a short extension while evaluating alternatives.
```

### Why This Is Better

It keeps cost, usage, switching cost, timing, and a decision path. Company history, branding, interface style, responsiveness, and sponsorship do not materially support the CFO's decision as stated.

## Example 5: Learn A Bounded Preference

### Input

```text
User feedback: In weekly project updates, keep blockers and owner names. Remove motivational language and completed-task detail unless it changes the launch date.

Draft: The team made fantastic progress and completed twelve cleanup tasks. Ana is waiting for Legal to approve the data-retention wording by Thursday. If approval slips past Thursday, the launch moves by one week. Everyone remains energized and committed.

Mode: teach
```

### Output

```text
Preference learned: For weekly project updates, retain blockers, owners, and schedule impact; omit motivational language and completed work that does not affect timing.

Blocker: Ana is waiting for Legal to approve the data-retention wording by Thursday. A later approval will delay launch by one week.
```

### Why This Is Better

The learned rule is limited to weekly project updates and reflects explicit feedback rather than inventing a universal preference.

## Example 6: Do Not Prune A Material Compliance Constraint

### Input

```text
Request: Make this customer message as short as possible.

Draft: We can delete your account immediately. Financial transaction records must still be retained for seven years under the applicable regulation, so account deletion does not remove those records. You may contact privacy@example.com to request deletion.

Mode: compress
Intensity: aggressive
```

### Output

```text
Request account deletion at privacy@example.com. Your account can be deleted immediately, but legally required transaction records will be retained for seven years.
```

### Why This Is Better

The message is shorter, but the retention obligation remains because removing it would create a materially misleading promise.
