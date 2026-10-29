# 09: Who may change what the agent learns

Files for part nine of Guide for building an autonomous agentic system administrator: [Part 9: Who may change what the agent learns](https://onet.com.au/blog/sysadmin-agent-guide-part-9/).

| File | Use it when |
|---|---|
| `shared-and-local-skills.md` | You have more than one agent and the same procedures are drifting apart. One shared source with one owner, selective use, and small distinctly named local addendums. Includes the Hermes name-shadowing gotcha. |
| `skill-placement.md` | An agent is about to create, move or install a skill. Existing home first, one explicit category from a fixed list, and no new categories without your approval. |
| `skill-change-review.md` | Deciding who may change a skill and how: the route for a proposed change, a weekly triage of automatic proposals, and making sure every agent can find the procedure. Builds on Part 1's `hermes-self-modification.md`. |
| `skills-taxonomy.md` | The library has grown past the point where you can understand it. Principles, a five-step method, what our pilot measured, and the mistakes to avoid. |

These are generalised rewrites of our estate-authored conventions and runbooks, not upstream Hermes skills. They have not been run-tested in this generic form. Customise them with your own agents, and check real loading for each agent after any change.

The methods do not depend on Hermes. The notes about `skills.external_dirs`, name precedence, `skill_manage` and `/skills pending` are Hermes-specific. The weekly triage jobs and email format are ours, not Hermes features.

**Version:** Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence:** CC BY 4.0. Use, adapt and share with attribution to Steve Waddington and Maxi Calder.
