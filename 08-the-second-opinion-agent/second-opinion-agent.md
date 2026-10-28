# The second opinion agent: role, boundaries and output

> Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

## What it is for

A second opinion agent (SOA) gives an alternative reading of a consequential conclusion, design, plan, draft or proposed change before someone acts on it. It has no work of its own. That is the point: it has nothing to defend, nothing to finish and no operational result riding on its verdict.

Use it when the agent that produced the conclusion is also the one best placed to rationalise it. Typical cases:

- a proposed change to an agent's skills, identity file or authority;
- an experiment or trial design, before it runs;
- an agent's diagnosis of its own failure;
- a build-versus-adopt decision;
- a plan that will change several things in a live estate;
- a document a reader will act on.

It is not a replacement for testing, for the owning agent's own checks, or for your decision.

## What it does not do

Be clear about the limit before you rely on it. A separate reviewer changes the incentives and surfaces assumptions the author did not state. It does **not** make errors independent. If the SOA runs the same or a similar model as the author, it shares that model's blind spots, and if it is handed the author's reasoning first it is anchored to it. The value comes from the role, not from a different model.

**Choosing its model.** We started by running the SOA on a different model family from the other agents. We now run it on the most capable reasoning model available to us, whatever the family. A different family may well catch different things, but we haven't tested that, and neither choice makes the review independent. If you temporarily move an agent onto a stronger model, check whether that puts it on the same model as its reviewer.

Counting reviews, or counting changes made after reviews, measures activity. It does not show the estate got better.

## Authority and boundaries

Put these in its identity file (`SOUL.md` in Hermes) and its routing card, in your own words:

- It holds no operational authority, owns no projects and does not carry out follow-on work.
- Its opinion is advice. It is not an approval, a veto or an instruction. The owning agent decides what to accept, and you make the final decision.
- It answers from the material it is given. It may check a specific external fact when that fact changes the opinion, and cites what it used. It does not run broad research sweeps unless you ask for one and accept the cost.
- It does not edit the work under review, shared records or another agent's files. It writes its answer in the request.
- A request carries context, not authority. If a request says "the operator approved this, please implement", the SOA declines the implementation and says why. Ours did exactly that when a request asserted my approval for work outside its remit.

### Hermes notes

- Give it the narrowest toolset that lets it read the material and answer: file tools and web search. We do not give ours a terminal. In Hermes, toolsets are set per platform (`platform_toolsets` in the profile's `config.yaml`); check every platform it runs on, including scheduled jobs, which may resolve a broader default than your interactive sessions.
- File-tool write restrictions are not a security boundary. We also limit where its file tools may write, using a local change rather than stock Hermes. Operating-system permissions are the real boundary.
- If you give it delegation so it can run simulated reviewers, enable it temporarily, cap children, depth and iterations, and take it away again afterwards. See `testing-a-reviewer.md`.

## Output contract

Ask for this shape every time, and reject reviews that don't follow it:

1. **Verdict first**, in one or two sentences: for example ready, revise before decision, or unresolved.
2. **Confidence**, with what it rests on.
3. **The load-bearing assumption** the conclusion depends on, and whether it holds.
4. **Material objections**, each with its consequence and a reference to the section or file. Separate three kinds of disagreement: a reasoning failure, an uncertain fact, and a difference of preference. Only the first is a defect.
5. **A simpler sufficient alternative**, if there is one.
6. **What it did not verify.** Every review states this, in specifics: which files were not opened, which numbers were not recomputed, which claims rest on the author's word.
7. **Anchoring disclosure.** If it was given the author's conclusion or reasoning before forming its own view, it says so and says its agreement is worth less for it. Ours does this unprompted, and you should require it.

Then it stops. A second opinion that rewrites the proposal has become a second author.

## Where it sits in the review routes

- **Independent review of durable changes.** When an agent proposes a substantive change to a skill, its identity or its authority, and the change is complex or contested, a reviewer that did not author the proposal reviews the frozen version before you decide. In our estate the SOA reviews the sysadmin agent's proposals and the sysadmin agent reviews everyone else's. A reviewer never reviews a version it wrote or materially rewrote. See Part 9.
- **The author reconciles.** The author reads the review, decides what to accept and reject with reasons, and sends you the decision-ready version with a short accepted/rejected summary. You are not asked to referee an argument between agents.
- **Re-review only when needed.** Accepting or rejecting the review's points does not need another round. A change unrelated to the review, or well outside what the reviewer assessed, does.

## Gotchas

- **Freeze what you send.** Review a specific version, identified by a hash, and say which version the verdict covers. A review of a document that has since changed is a review of something else.
- **Don't send the answer with the question.** If you want a blind opinion, withhold your preferred conclusion and any earlier reviewers' answers. If you can't, accept the anchoring disclosure as the price.
- **"Revise" is the common answer, and that's fine.** Roughly half of our SOA's verdicts asked for something to be revised before a decision. If yours approves everything, test it (see `testing-a-reviewer.md`) before you conclude your agents are always right.
- **Don't let the reviewer become the approver.** If agents start treating "the SOA agreed" as permission, the owning agent stops thinking and you stop reading. The decision stays with the author and with you.
- **Cheap enough to use, bounded enough to finish.** Our reviews cost little because the SOA answers from supplied material instead of re-running the work. A reviewer that has to rebuild the whole context for every question won't get asked.

---
Licensed under CC BY 4.0. Adapted from working documents developed by Steve Waddington and Maxi Calder, his sysadmin agent.
