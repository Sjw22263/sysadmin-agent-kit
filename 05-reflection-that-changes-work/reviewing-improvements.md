# Reviewing improvement proposals

**Use:** a human-and-agent review routine for proposals from bounded research. Customise with your operator before use. This is a generalised document derived from our current practice, not an active installed skill or a turnkey tested integration.

**Version:** Process inspected 21 October 2026, running Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence:** CC BY 4.0, Steve Waddington and Maxi Calder.

## Make the review findable

Use one canonical proposal queue, linked from the human's normal operational report or agenda. Give each proposal a stable ID and source report. Before a review, reconcile open IDs against the decision, experiment, watch and backlog records. The report supplies detail, not an independent second queue of pending work.

If the queue says open and a traceable decision says rejected, resolve the mismatch rather than asking again. If the reviewer cannot find a proposal or its evidence, repair the handoff before claiming the loop is closed. Do not auto-import every old report recommendation as unresolved work.

## One item at a time

Start with the oldest unresolved item unless there is a genuine priority reason to reorder it. The agent explains the problem, specific proposed change and cost briefly, then gives its recommendation and reason. Do not make the human reconstruct the argument from a long report or a neutral menu.

For each proposal establish:

- What concrete problem exists here, and what current evidence shows it?
- Does the proposal add information or a useful check, or duplicate what already happens?
- What evidence would justify trying it, and what result would justify keeping it?
- Does it change tools, authority, recurring cost, privacy, publication, governing text or another reserved matter? Which approval route applies?

The human may reject, defer, put it on a dated watch, accept for backlog, approve a bounded experiment or approve an exact change within the relevant route. Approval in principle is not approval of an unspecified implementation. A documented delegation may allow the agent to make a particular low-risk decision, but this generic document supplies no such delegation.

Record the decision immediately, including proposal ID, source, decision-maker, exact scope and reason. Reconcile the queue entry before moving on. A rejected idea is not automatically a deferred one. A deferred or watched idea needs a date or explicit trigger for reopening it. Record substantive disagreement faithfully, including evidence that later changes the result.

## Trial card

Before an approved trial starts, record:

```text
ID:
Proposal and source:
Decision-maker, approval reference and exact scope:
Problem and baseline evidence:
Hypothesis:
Specific change:
What remains unchanged:
Trials or qualifying trigger:
Success criterion:
Failure / no-signal criterion:
Evidence to collect and who checks it:
Scope of possible effects:
Recovery / rollback:
Midpoint check (for trials of three or more runs):
Final review date or trigger:
Observed outcome (complete after the trial):
Decision: keep / revise / drop / unmeasured, with reasons:
```

Use a halfway check for trials of three or more runs to see whether the experiment is generating useful evidence. Ending or materially changing an approved experiment follows the operator's authority, not this template. If a prospective trial never receives a qualifying real case, record 'not exercised', not success.

Preserve failed trials and no-signal results. A new prompt or a carefully written regression set may add no useful information. Do not turn that local result into a universal claim that prompting or regression tests are useless.

## What the evidence permits

Our five-report missing-information trial was retained after operator review, while a five-report minority-idea audit was dropped as duplicative and a three-report regression trial caught nothing and was archived. Those were practical decisions from a small local trial, not a controlled comparison proving a change in reasoning capability.

For your own trial, distinguish a new file, actual use, changed behaviour and useful outcome. If making a causal comparison, record differences in task, prompt, context, tools, model and evaluation. Without a matched control, describe what happened and what you chose, not a measured improvement you did not measure.

Prefer observable checks or a human's review of concrete output over a confidence number. Independent evidence still needs to be relevant: a separate check that never examines a failure you care about does not earn its overhead by being separate.

## Review the recurring process

Once a month, inspect the reports, queue and trial record together. How many ideas reached decisions? What changed? What was used again? What was removed? Did the benefits justify the research and review cost? Would a slower cadence produce the same useful work?

Retaining a schedule is a decision too. Do not require the process to invent a new recommendation to justify running again. Any change to the active procedure or schedule needs the applicable approval.
