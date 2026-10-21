# Owning the maintenance: verify before retry

> Checked against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## Where to use this

Give this to the agent as a standing procedure, or adapt it into a skill, for any operation that changes something outside the agent and can end ambiguously: a timeout after the request was sent, an unclear error, a success message with no evidence behind it, or a job that may have done part of its work.

It governs what happens after an ambiguous result. It does not grant authority for the operation itself or anything broader.

## Why

An agent's natural response to a failed call is to try again. For a read that is harmless. For anything that changes state, the failure message and the real effect are two separate pieces of evidence, and the first says little about the second. A retry after a timeout can send the email twice, create a second record, run a migration twice or publish a duplicate.

Ours: a nightly job that copies backups to a second device reported failure because its sender timed out waiting for the far end to finish verifying. The far end had not failed. It finished verifying and published the new backup three minutes after the sender gave up. Read naively, that was a failed backup and a reason to run it again. Checked properly, it was a successful backup and a deadline shorter than that successful run took. We did not establish why that verification ran slower than usual, and did not need to: the repair was to extend that one deadline. The retry, run as a test of the repair, found the generation already present and did not create a second one, because the job checks for the generation before writing it.

## Procedure

1. **Do not retry from the response alone.** Treat the tool's response and the real-world effect as separate evidence.
2. **Check the real state, read-only.** Use the narrowest reliable evidence of the intended outcome: read the object back, look it up by a stable identifier, check a status endpoint, find the sent-message record, compare a content hash, check the service from the consumer's side.
3. **Classify the outcome:**
   - **TRUE:** the intended change exists and is complete. Record success. Do not retry.
   - **FALSE:** reliable evidence shows the change did not happen. Retry at most once, if the original authority still applies, reusing the same idempotency key or operation identifier where the target supports one. Then check again.
   - **UNKNOWN:** the state cannot be established, may be stale, or is partly complete. Stop. Do not retry blindly. Contain it and report it, or resolve it under the agent's mandate.
4. **After any retry, check the effect again.** A second success message is not proof that only one change happened.

## Limits

- One retry, at most, under this procedure.
- Do not invent an idempotency key after the target has already processed a request without one and then assume it will deduplicate the earlier call.
- Never use a retry to widen the scope, change the target or get around an approval.
- If the target is eventually consistent, wait only within an agreed observation window. If the window ends without an answer, the result is UNKNOWN, not FALSE.

## What counts as evidence

Evidence has to test the intended outcome, not a proxy for it:

| Weaker | Stronger |
|---|---|
| HTTP 200 from the send call | A sent-message record with the right recipient and operation ID |
| The upload process exited 0 | The remote file's hash matches |
| The process is running | The service answers a real request from its consumer's side |
| A search by approximate time or text | A lookup by the stable idempotency key |
| An empty or stale read | (Not evidence of absence. Classify as UNKNOWN.) |

If no authoritative check exists, the state is UNKNOWN.

## Closing the incident

Close only when one of these is true:

- the intended effect is confirmed and there is no duplicate;
- its absence is confirmed and the operation is deliberately left undone;
- partial or unknown state is contained, with the remaining risk and the next action recorded;
- resolution is blocked and the exact help or decision needed has been stated.

## Design for it in your own jobs

The best time to apply this is when the job is written. Give each run a stable identity (a dated generation name, an operation ID) and publish only after verification.

A stable name plus "check whether it already exists" is a start, not a guarantee. Two runs can both pass a non-atomic existence check and both write. Make the duplicate impossible at the target or in the sequencing: an idempotency key the target enforces, an atomic create-if-absent or rename-into-place, or a lock that genuinely serialises runs. Then a retry is cheap rather than dangerous. It does not make the outcome check optional: still read the result back, and still check that only one copy exists.

## Common mistakes

- Retrying because the error "looks transient" after the request was sent.
- Treating a second success as evidence that only one change happened.
- Treating an empty or stale read as proof of absence.
- Checking an implementation detail rather than the outcome the consumer sees.
- Wrapping every tool in a generic retry helper when each needs its own postcondition.
