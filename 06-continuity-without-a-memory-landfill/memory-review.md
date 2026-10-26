# Memory review and consolidation

*Correct at Hermes Agent upstream commit `e1fdf003` (5 October 2026), checked 23 October 2026. Hermes has thousands of commits per month, so ask your agent to check the Hermes-specific points against your version.*

## Where to use this

Use the full review when memory is above roughly 70% of its limit and contains stale entries, after a large change makes several entries obsolete, or when you are investigating why the prompt has grown. Use the light nightly review once the full review has been done by hand at least once.

Do not use this for ordinary single additions. Adding one fact is one memory write.

## Why it needs doing at all

Agents add to memory far more readily than they remove from it. In Hermes this is partly by design:

> **Hermes:** by default the background review can write to memory without approval (`memory.write_approval: false`; see the part 1 file `hermes-self-modification.md`). At the version checked, it can only *add* unattended. A `replace` or `remove` proposed by the background review is staged for approval (`/memory pending`), not applied. That is a sensible safeguard, but it means unattended memory only grows. Someone, human or a scheduled review with its own authority, has to do the removing.

If a store refills within days of being pruned, the problem is what is being written, not the size of the store. Fix the routing (see `operational-notes.md`) before raising the limit.

## Full review

### 1. Measure

Record before you change anything:

- number of entries in memory and user profile;
- characters used against each limit;
- if you can, the provider-reported prompt tokens for a minimal request, so you can compare like with like afterwards.

> **Hermes:** `hermes prompt-size --json` reports the character breakdown of the system prompt, including memory and profile. Character counts are estimates; the provider's `usage.prompt_tokens` on a minimal request is the figure that actually counts. Compare the same platform before and after, because different surfaces load different tools.

Character savings and token savings are not the same number. In one of our consolidations a 22.6% reduction in formatted memory characters produced a 12.9% reduction in prompt tokens.

### 2. Classify each entry

| Classification | Action |
|---|---|
| Keep | Short, current and still needed. |
| Move to a runbook | Too detailed for memory. Write or update the runbook, leave a pointer. |
| Consolidate | Several entries about one thing. Merge into one short entry. |
| Remove | Obsolete, duplicated, or of historical interest only. |

Rules of thumb:

- Three or more lines: candidate to move.
- About a finished one-off task: candidate to remove.
- Identity, authority, security and operationally critical facts: keep.
- Old is not the same as stale. An entry that is still true stays.
- An entry stating live system state (a model, a service, a configuration value) gets checked against the live system before it is kept or changed.

### 3. Propose before acting

Write the proposal down: baseline numbers, each change with its reason, entries that will not change, and any stale or missing runbooks you found. The human approves the proposal, not a summary of it.

### 4. Back up

Copy both stores somewhere outside the agent's working directory and record checksums of the backup and the live files before applying anything. A bad removal loses a fact nobody will think to restore.

### 5. Apply in one batch per store

> **Hermes:** the `memory` tool accepts an `operations` list (add, replace, remove) applied atomically, with the character limit checked against the final result. That lets you remove and add in one call even when the add alone would overflow. `old_text` must identify a single entry; at the version checked an ambiguous match is refused rather than guessed. Verify by reading the store afterwards, not by repeating the call.

### 6. Verify

- entry counts match the proposal;
- each protected fact is still present;
- each removed entry is gone;
- character totals and, if measured, provider tokens before and after;
- the agent's identity file is unchanged unless it was in scope.

## Light nightly review

Once the full review has been done by hand, a scheduled job can keep things tidy. Ours runs at 03:00 local time.

1. Back up memory, user profile and the session store first. If the backup fails, change nothing and report the failure.
2. Review the previous day's conversations, by exact session, against both stores.
3. Make only conservative edits: remove duplicates, contradictions, finished task state and stale claims about live state; move detail into the right runbook or skill.
4. Anything larger, such as a change to a skill, a procedure or the agent's instructions, is written up as a proposal for a human to decide. It is not applied by this job.
5. Write a short report: what changed with exact before and after text, what was proposed, what was rejected as noise.
6. Report a clean run in one line. Escalate only a backup failure, a conversation it could not read, a write that failed verification, or something that genuinely needs a decision.

**What to expect.** Once memory is being used as an index, most nights this review should change nothing. Ours made no memory edits on any of the ten nights to 22 October 2026. That is the system working, not the job failing. If your nightly review is making several edits every night, look at what is being written during the day.

> **Warning:** do not let the nightly review become a self-modification loop. Give it a time limit, no authority over instructions, skills, schedules or credentials, and a rule that anything found in conversations, email or web pages is evidence to assess, not an instruction to follow. Sequence is not cause: a proposal that infers why something happened must say how it knows.
