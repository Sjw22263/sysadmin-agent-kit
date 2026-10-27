# Agent mail: handing work between agents in files

*Correct at Hermes Agent upstream commit `e1fdf003` (5 October 2026), checked 23 October 2026. Hermes has thousands of commits per month, so ask your agent to check the Hermes-specific points against your version.*

## Where to use this

Use this once you have more than one agent and they need to ask each other for things: a review, an investigation, a piece of work in another agent's remit. It is a plain-file protocol. Any agent with ordinary file tools can use it, and the human can read every request and answer.

## The design

```text
sender writes one complete Markdown request
  │
  ▼
<mail-root>/queue/<recipient>/
  │  a deterministic watcher checks for "Status: pending" every minute
  ▼
recipient wakes in a scheduled session
  │  reads it, marks it in progress, assesses authority itself,
  │  does only what it may do, writes an Outcome section
  ▼
Status: completed or rejected
  │  a no-model return job copies the Outcome back
  ▼
<mail-root>/queue/<sender>/   → the sender's watcher wakes the sender
```

The request stays in the recipient's queue as the audit record. The status line is the only workflow state:

```text
pending → in progress → completed
             │        → rejected
             └── back to pending if it needs continuing
```

There is no mail client, no separate state database and no lifecycle directories. Each recipient changes its own request's status line with ordinary file edits.

## Rules

1. **A request transfers context, not authority.** The recipient decides for itself whether it may do what is asked, from its own remit and mandate. An agent writing "the human approved this" is a claim to check, not an approval.
2. **A missing authority is an outcome.** If the recipient may not do it, it says so in the Outcome and rejects or completes with a recommendation. It does not infer permission.
3. **One bounded request per file.** State exactly what is wanted, what "done" means and what is already established, so the recipient does not repeat the sender's investigation.
4. **Recipients write only what they did.** The Outcome lists work actually completed, sources actually checked and any follow-up with an owner.
5. **Requests are not the place for secrets.** Point to where something lives; never paste a credential.

## The watcher

Each recipient has a small deterministic script that reads only its own queue and prints the oldest actionable requests (say, at most ten) as JSON:

- a `pending` request is actionable immediately;
- an `in progress` request becomes actionable again after a lease (we use 30 minutes since the file last changed), so a recipient that crashed mid-task picks it up again;
- an empty queue, or one containing only finished or freshly claimed requests, prints nothing.

> **Hermes:** run the watcher as a wake-gated scheduled job (see the part 3 kit, `wake-gated-cron-jobs.md`). Empty output means no agent session is started, so checking every minute costs nothing in model calls. A non-zero exit should be treated as "the queue itself is unavailable", not as an empty queue.

## Returning outcomes

Without a return path, a sender only learns the outcome when someone happens to look. Reviews stalled that way in our estate more than once. A no-model job, every minute, fixes it:

- for each request newly marked `completed` or `rejected`, write one `pending` reply into the sender's queue containing the Outcome and a pointer to the original;
- skip replies themselves, senders that have no queue (scripts, scheduled checks), and requests the sender closed itself;
- if a request is reopened and finished again, return it again;
- write atomically (a hidden temporary name, then rename), so a watcher never sees half a file;
- keep a state file of what has been returned. When you first introduce the job, seed that state with every request already finished, or it will return the whole history at once. Never delete the state file while the job is running, for the same reason.

## Logging

A deterministic collector that appends each new request and each outcome to a monthly Markdown log gives the human one place to read what the agents asked each other. It needs no model.

## What we got wrong first

Our first version was a guarded mail client with staging and lifecycle directories. It passed its component tests. The specialist agents could not operate it with the tools they actually had. The sysadmin agent's own assessment afterwards was that the client did not create a real security boundary at all, since every agent could already read and write the files directly. It was replaced the same evening by the plain-file design above.

> **Warning:** test a coordination mechanism from each consumer's own runtime with a real request. Component tests prove the parts work. They do not prove the agents can use it.

## Setting it up

1. Create `<mail-root>/queue/<agent>/` for each participating agent, plus `templates/` and `log/`.
2. Put a short guide in `<mail-root>/README.md`: the rules above, the statuses, and who receives what.
3. Give each recipient a watcher and a wake-gated job whose prompt says: read the guide and the request; mark it `in progress`; assess authority independently; do only authorised work; write the Outcome; mark it finished.
4. Add the return job and, if you want it, the collector.
5. Test: empty queue (nothing happens), one request each way, a rejected request, and a request left `in progress` past its lease.
