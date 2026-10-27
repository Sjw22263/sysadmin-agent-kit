# Estate rationalisation

*Correct at Hermes Agent upstream commit `e1fdf003` (5 October 2026), checked 23 October 2026. Hermes has thousands of commits per month, so ask your agent to check the Hermes-specific points against your version.*

## Where to use this

Use this when the estate (every system, service, agent, schedule, script, backup, security control and operational document under the agent's remit) has grown by accretion and you want the agent to simplify it. Also after a major change such as a new agent, a new model or provider, or suspected drift from the last baseline.

Do not use it for routine maintenance or for fixing one broken thing.

## The brief

Give the job to your most capable agent and model, and be explicit about why. Ours was told that the extra capacity of the stronger model was for better planning and judgement, not for doing more of the routine work itself. The governing duty we later wrote into its mandate was to remove complexity rather than add it.

The aim is fewer components, fewer paths and fewer things to break. A proposal that adds machinery to solve a problem is usually the wrong proposal.

## Stage 1: Audit

Inventory every component. Skip nothing because it is "obviously fine"; that is how the next audit starts from an incomplete baseline. Each entry needs an identifier, purpose, location, owner and status. Keep supporting evidence in its own folder.

## Stage 2: Overlap register

For every component in the audit, record what it overlaps with, whether the overlap is harmful, benign, deliberate defence in depth or an incomplete migration, whether one supersedes the other, and a recommended disposition: keep both, pick one, consolidate, retire, or close after review. "No problematic overlap" is still a finding and still gets a line.

## Stage 3: Plan

One row per audited component: disposition (retain, simplify, consolidate, repair, retire, close after review), the specific change, the reason, the risk and what sign-off it needs (none, human review, human approval, approval for a destructive step). Group the rows into batches small enough to verify one at a time.

Above the rows, write down the **capability invariants**: outcomes for people and agents that cut across components ("agent X can read the shared library", "the human gets a morning report"). A plan in which every row looks reasonable can still remove an invariant. Any row that would weaken one is a decision for the human, not a line item.

## Stage 4: Cold validation

This is the stage that matters. The plan is built on assumptions formed during the audit, and plans are persuasive stories. Before any change:

1. Re-read the plan as if someone else wrote it.
2. For each change, ask what would make it wrong or dangerous.
3. Test each material assumption against the live system: configuration, running services, credential files, actual traffic, disk, backup contents.
4. Record every assumption that failed and revise the plan.
5. Produce the sign-off list: only the items that genuinely need the human, each with the specific question.

Our first validation pass caught six material errors before anything was changed: a port marked for closure was still serving live traffic; enabling a gateway per agent profile would have made them compete for shared credentials; a backup the plan proposed to create already partly existed under another name; credential residue contradicted the record of a purge; a remote access assumption was wrong in a way that turned out to be low risk; and a queue correctly identified as unused still needed checking before retirement.

## Stage 5: Implement

- Implement only what the human approved.
- One batch at a time; verify each before starting the next.
- Keep rollback explicit.
- New discoveries go on a follow-up list. Do not widen the batch.
- A batch that creates a file or directory is not done until that path exists.
- Where live configuration contradicts a runbook, flag it. Correct the documentation only when live evidence is unambiguous and no approval is needed; never resolve the discrepancy silently in either direction.

## Stage 6: Delegation, once the estate is clean

Only after rationalisation, decide which class of work goes where, cheapest suitable first:

1. Deterministic scripts with no model at all, for mechanical checks with fixed output.
2. A cheap model for bounded research, synthesis and implementation with explicit inputs and acceptance criteria.
3. A mid-tier model for routine work needing better tool judgement.
4. The strongest model for goals, governance, security and access exceptions, destructive decisions, integration and final acceptance.

Delegation moves execution, not accountability. The overseeing agent stays responsible for scope, review and the truth of the final claim.

- Pin the model and provider on every scheduled job that uses a model, so nothing silently runs on a default.
- Give routine jobs an exception path: a material problem goes into the overseeing agent's request queue (see `agent-mail.md`), where the stronger model assesses it. The handoff carries context, not authority.
- Smoke-test both the delegated path and the exception path, and check which model actually ran in the runtime logs rather than trusting configured labels.

> **Warning:** fallback is an authority route. If the main session's model is unavailable, the fallback model inherits the main session's authority. A cheap fallback behind a high-authority session is a quiet escalation. Review the fallback chain whenever you change delegation, and either make the fallback capable enough or record that the human accepted the risk.

## The six controls we added after it went wrong

Our first programme closed as verified with a serious error in it. The human and the agent had agreed to give another agent narrow access to the shared library and request queue. During rationalisation, half an hour later, the overseeing agent replaced that outcome with its own assertion that the other agent should have no access, recorded that assertion as the human's decision, retired the working trial arrangement before the agreed replacement existed, and verified the programme against its own corrupted plan. Eleven records ended up repeating the false decision, and were then treated as corroborating each other.

1. **Decision provenance.** Any decision about access, retirement, replacement, credentials, security boundaries or agent capability records the intended outcome, the chosen mechanism, its status (proposed, accepted, implementing, verified), the human's exact instruction or message, dependencies, and acceptance evidence. Never write "the human decided" without a message that says so. If there is none, label it an inference and stop.
2. **Successor before retirement.** Do not call anything replaced until its successor passes the required tests from the consumer's own environment. Encode it in the plan: "Do not retire A until B passes [tests]." An archive check is not a successor test.
3. **Capability invariants above component rows** (see Stage 3).
4. **A specific question overrides grouped approval.** If the human asks a specific question inside a batch approval, or the approval conflicts with a recent agreed design, that item stays open. Answer the question and surface the conflict. Unrelated items may proceed.
5. **Consumer-perspective acceptance.** Close the programme with real tasks performed from each affected agent's or person's own context, not the administrator's shell.
6. **Source-diverse review.** Five documents that copy one unsupported claim are one source. For material decisions compare the human's instruction, the intended capability, the implementation, the consumer's actual experience and the current documentation. Disagreement blocks closure.

The part 1 mandate template already carries the first two as duties. If you start from it, these controls are the procedure that makes those duties checkable.

## Closing

Write the review the mandate requires without asking permission to write it; reviewing is not a change. Present conclusions and only the items that need a decision. Reconcile the documentation with the live estate (plan status, index, runbooks) as part of closure, not later.
