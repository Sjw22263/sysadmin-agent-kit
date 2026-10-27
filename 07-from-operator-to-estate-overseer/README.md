# 07: From operator to estate overseer

Files for part seven of Guide for building an autonomous agentic system administrator: [Part 7: From operator to estate overseer](https://onet.com.au/blog/sysadmin-agent-guide-part-7/).

| File | Use it when |
|---|---|
| `new-agent-onboarding.md` | Bringing a new long-lived agent into an estate that already has one: role first, least privilege, shared context by reference, a self-review and real verification before it is called operational. Includes an agent card outline. |
| `agent-mail.md` | Agents need to hand work to each other. A plain-file request queue, one inbox per agent, a status line as the only workflow state, wake-gated receivers and automatic return of outcomes to the sender. |
| `delivery-template.md` | The template for one request. Copy it into the recipient's queue. |
| `estate-rationalisation.md` | The estate has grown by accretion and you want the most capable agent to simplify it: audit everything, register overlaps, plan one row per component, test the plan against live state, implement in batches. Includes the six controls we added after it went wrong. |

These are generalised rewrites of our estate-authored runbooks and skills, not upstream Hermes skills. They have not been run-tested in this generic form. Customise them with your own agents, and exercise every route (a delivery, a wake, a return, a retirement) end to end before you rely on it.

The methods do not depend on Hermes. The notes about profiles, gateways and scheduled jobs are Hermes-specific.

**Version:** Checked on 23 October 2026 against Hermes Agent upstream commit `e1fdf003` (5 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

**Licence:** CC BY 4.0. Use, adapt and share with attribution to Steve Waddington and Maxi Calder.
