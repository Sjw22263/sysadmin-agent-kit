# Reviewing changes to what the agent has learned

> Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

Part 1 (`hermes-self-modification.md`) covers the switches: how Hermes agents change their own skills and memory, and why we run with skill writes approval-gated and memory writes open. This file is what happens after you flip the switch: the route a proposed change follows, how proposals reach you, and how to make sure every agent can find the route.

## Skills need review, memories are the agent's

Our rule came from a question I put to the sysadmin agent: "Skills need review, memories are yours. Agree or not?" Skills are procedures an agent will follow on your systems and, if shared, other agents will follow too, so a change needs someone to read it.

Memory is left open for a different reason. An agent has to carry context from one session to the next, or each conversation starts with rediscovering and re-explaining everything, and gating every memory write gets in the way of that. Open memory only works once the agent knows what to keep. Out of the box, agents are poor at it: our early memory filled with trivia while important durable facts were lost. What fixed it was explicit guidance in the skills about what belongs in memory, and runbooks for detail (see Part 6, `operational-notes.md`), so memory holds short facts and pointers. Put that guidance in place before you leave memory open. You may draw the line differently, but draw it deliberately.

## The route for a skill change

Classify a change by what it does, not by which file it is in. A change is substantive if it can alter when a skill triggers, what it means, what authority it implies, how a decision is made, what is produced or how it is verified. A typo fix that cannot change any of those is ordinary maintenance.

For a substantive change:

1. **Exact proposal.** The author presents the exact before-and-after text, the target, the intended effect and its recommendation. A paraphrase is not a proposal.
2. **Your decision on the route.** If it is straightforward, you approve the exact change directly. If it is complex, uncertain or someone has a serious objection, it goes to independent review first.
3. **Independent review, when used.** A reviewer that did not write the proposal reviews the frozen version. In our estate the second opinion agent reviews the sysadmin agent's proposals and the sysadmin agent reviews everyone else's (see Part 8).
4. **The author reconciles.** The author decides what review advice to accept, with reasons, and sends you the decision-ready version with a short accepted/rejected summary. Advice is neither an instruction nor a veto.
5. **Your final decision** on that exact version.
6. **Apply and verify.** Apply only the approved version, confirm nothing else changed, and check the changed behaviour in a fresh session.

Changes to an agent's identity file or authority always need your explicit approval before they take effect. For changes prompted by a mistake, first establish that the instruction was actually missing or defective. If the agent simply didn't follow a sound rule, fix the execution, not the rules (see *Corrections Consolidate*, linked from the Part 9 post).

## Automatic proposals: a weekly triage

With `skills.write_approval: true`, Hermes's background review still proposes skill changes; they wait as pending records instead of going live. Those need someone to look at them, or the queue just grows.

Each of our agents runs a weekly job that reviews every unresolved pending record for its own skills, and emails me the result from its own mailbox. For each record it answers three questions with evidence:

1. **Is a durable skill change necessary,** or is this already handled by an existing procedure, an ordinary record or a correction in the conversation where it arose?
2. **Will it materially improve the work?** What concrete outcome gets better, or what failure does it prevent?
3. **Will it make the work easier or simpler,** once you count the extra instruction and maintenance?

More rules are not automatically better, and the recommendation has to say so when a change adds complexity.

The email lists every pending ID separately:

```text
## 1. <skill name>.<pending id>
- Why needed: <what the change does, and whether and why it is needed>
- Where used: <which agent, in what task>
- Recommendation: <approve / reject / revise / defer, with reasons>
```

Rules that keep it honest:

- Every unresolved item reappears every week until you approve or reject it, including items the agent recommends rejecting.
- No scheduled job approves, rejects, applies or archives a pending record. Only you do.
- An empty queue says so in one line.
- A stale proposal (written against a version of the skill that has since changed) is recommended for revision, not approved as a paraphrase.

### Hermes notes

- Review pending changes with `/skills pending`, `/skills diff <id>`, `/skills approve <id>` and `/skills reject <id>`.
- The gate stages changes made through `skill_manage`. It does not stop an agent editing a skill file with ordinary file tools or a shell. Approval interfaces and successful writes are not evidence that the right change is active; verification is.
- Background review and the curator are separate mechanisms. See Part 1 for the curator's archiving behaviour.
- The weekly triage jobs, the email format and the review routing are ours, not Hermes features.

## Make the route discoverable

We had all of this written down and still had an agent fail to follow it. When the sysadmin agent checked, it found nothing in that agent's live instructions or task context that told it to read the procedure. That is a routing failure, not the agent's. The fix was not to load the whole procedure into every agent's context. In my words: "The desired outcome is just that the agent knows where to find the information if they need it."

So the procedure lives in one canonical file every agent can read, and each agent's identity file carries a short conditional pointer:

```text
Before proposing, reviewing or applying a change to governing instructions,
skills, reusable agent methods or consequential runtime controls, read
<path to the canonical procedure>. This is an on-demand reference, not
automatically loaded context, and grants no additional authority.
```

Test it from the agent's side: start a fresh session and ask the agent how it would propose a change to one of its skills. If it can't find the procedure, the pointer isn't where it looks.

## Checklist

- [ ] Decide which stores need review and which are the agent's own.
- [ ] Write the change route down once, in a place every agent can read.
- [ ] Put a conditional pointer to it in every agent's identity file, and test it from a fresh session.
- [ ] Set up a regular triage of pending automatic proposals that keeps every unresolved item visible until you decide.
- [ ] Keep the reviewer of a proposal separate from its author.
- [ ] Verify applied changes in a fresh session.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
