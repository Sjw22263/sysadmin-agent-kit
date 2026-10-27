# New agent onboarding

*Correct at Hermes Agent upstream commit `e1fdf003` (5 October 2026), checked 23 October 2026. Hermes has thousands of commits per month, so ask your agent to check the Hermes-specific points against your version.*

## Where to use this

Use this when a human has decided to add a long-lived agent and asked your sysadmin agent to bring it into the estate. It is not authority to create agents, widen anyone's permissions, expose an agent externally or change harness-wide security or model settings. Those stay with the human.

## Principles

- Start with the job the agent is for, not a generic personality.
- The agent's own identity file is the authority for its identity, specialist rules and any response templates.
- Give shared context by reference to a curated library, not by copying the sysadmin agent's memory.
- Grant only the skills and tools the remit needs.
- Access to a shared path is access, never authority to change it.
- Verify the agent can actually use its environment before calling it operational.

## Before you start

Agree and record with the human:

1. The agent's name, remit and relationship to the human.
2. Whether this is a migration of an existing persona or a new role.
3. Where its identity comes from: an existing system prompt, a brief, or both.
4. Its workspaces, tools and any external services.
5. Its authority boundary, including what always needs the human's approval.
6. Whether it needs shared storage, the request queue (`agent-mail.md`), scheduled work or external messaging.

If any of these affect access, credentials, external exposure, recurring cost or harness configuration and are not explicit, prepare a recommendation and stop for a decision.

## Procedure

### 1. Write the role brief

From verified sources: purpose and non-goals, the deliverables it owns, its source material and working directories, who it works with and when it escalates, its voice and any mandatory templates, and the minimum skills and tools. See the part 1 kit for the brief, identity and mandate templates.

### 2. Set up the identity

Give the agent its own identity file, user profile and memory.

- The user profile can share a common baseline about the human, with a short role-specific preface.
- Memory starts with a small verified set for its domain. Do not copy the sysadmin agent's operational memory or unrelated private material.
- For a migrated persona, keep any structured response templates exactly as they were. Summarising them is a regression.

> **Warning:** cloning an existing agent is the quickest route and the commonest mistake. Our first specialist migrations inherited instructions and context that belonged to the sysadmin agent, and truncated templates the specialists needed. If you clone, prune the result to the remit and read it back.

### 3. Least privilege for skills and tools

Inspect what the new profile can do. Remove inherited administrative, email, security or scheduling skills that are not part of the role, and any tool that permits action beyond the remit. Then check the opposite: the specialist skills and source access it needs to do its real work.

### 4. Shared records

- An **agent card** in the shared library (outline below): role, remit, working locations, collaboration and escalation boundary, last verified date. No secrets, prompts, raw memory or access-control detail.
- A row in the estate's agent registry, if it is long-lived.
- A one-line entry in the shared library's change log.

### 5. Connect shared context

Point the agent at, in order: the shared orientation document, its own card, the project and environment records for its remit, and the request-queue guide if it will send or receive requests. The shared library is a map. It is not a reason to load all of it into every conversation.

If it will receive requests, create its queue and a wake-gated receiver (see `agent-mail.md`), then test an empty queue (silence) and one complete round trip from the agent's own context.

> **Hermes:** a profile's scheduled jobs only run if something owns that profile's scheduler, usually a gateway service for the profile. A stored job whose next run is in the past is not running. If you start a gateway per profile so their jobs fire, disable the messaging adapters on the extra ones, or several gateways will compete for the same bot credentials and API port. We found that conflict while testing a plan, not in production; check yours the same way.

### 6. Self-review

Ask the new agent to inspect its own setup and show that it can:

- state its role, remit and limits accurately;
- read its own workspace and the shared orientation material;
- name the right source of truth for a representative task;
- use its required response template, if any;
- say which work needs escalation;
- receive, and where enabled send, one bounded request.

Treat its answers as evidence to check, not reassurance. Fix gaps within the approved scope and repeat the check.

### 7. Verify the real outcome

| Capability | Verification |
|---|---|
| Identity | A clean session reflects the role, voice and boundaries. |
| Shared references | It reads the orientation file, its card and one canonical source from its own context. |
| Workspace | It can read its sources and write only where it should. |
| Skills and tools | The enabled list matches the remit; unwanted inherited capabilities are gone. |
| Request queue | Empty-queue silence, then one delivery claimed and finished. |
| Scheduled work | The job exists, has a live scheduler owner, behaves correctly when there is nothing to do, and advances. |
| External integration | A safe, authorised end-to-end test with the real external result checked. |

> **Warning:** do not verify from the administrator's shell when the question is what the new agent can do. A port check from the host proves nothing about whether the agent, in its own runtime, can read the file. Test from the consumer's side.

### 8. Close

Report to the human: the remit and working locations, what was enabled and what was deliberately withheld, the self-review and verification evidence, and anything still open. Update the registry and shared records after the verified state is clear. A new profile that shows up in a list is not an operational agent.

## Agent card outline

```markdown
# [Agent name]

## Role

## Remit

## Canonical working locations

## Collaboration boundary
(Who it takes requests from, who it escalates to, what it never does.)

## Last verified
```

## Common failure modes

- A clone keeps powers or instructions it does not need.
- A specialist is missing the response template its work depends on.
- The shared library turns into a second project repository. Keep it an index and link the real workspaces.
- A queue exists but nothing delivers to it. Do not claim the agent can receive requests until the round trip has been tested.
- A scheduled job exists but no scheduler owns it.
- A request is mistaken for authority. A handoff from another agent is context and a request, never permission beyond the recipient's own remit.
