# A guarded harness update

> Checked on 30 October 2026 against Hermes Agent v0.22.5 (upstream commit `bf0203a7`, 22 October 2026). Hermes has thousands of commits per month, so ask your agent to check anything Hermes-specific against your installed version.

The cutover half of an upgrade, after `upgrade-reconciliation.md` has produced a tested candidate. This is a generalised version of what our sysadmin agent does, rewritten after an October upgrade in which the preparation was thorough and the path actually run was not.

## What went wrong in October

The custom changes were applied correctly. Then:

1. **The check rejected a correct result.** The executor compared a checksum of the patch text. Git abbreviated object IDs to eight characters in the small candidate repository and ten in the large production one, so the text differed while the files did not. It treated that as corruption and started a rollback.
2. **The rollback failed on a missing directory.** Before restoring the backup it tried to save the failed state into a nested directory whose parent did not exist. The copy failed and the executor stopped before restoring anything.
3. **Services pointed at a Python environment that no longer existed.** The service definitions had the old runtime path written into them. Another agent repaired the gateway services; the web interface and dashboard needed their runtime bindings fixed as well.

In the sysadmin agent's words, "I had substantial preparation and test evidence, but it did not adequately cover the exact executor and recovery path I ultimately ran." None of the three faults was large. All three were in steps that had never been run as they were run that day.

## Before you start

- **Decide how much interruption is acceptable.** For a small estate, a short outage and a later fix is usually fine. Say so, and stop qualifying against risks you have accepted.
- **Tell the people affected** and, if other systems or agents depend on the harness, check they can tolerate the interruption.
- **Run the cutover from outside what it stops.** An agent running inside the harness gateway cannot stop that gateway and carry on. Use a separate service or shell, and decide in advance where the result will be reported, since the conversation that started it may not survive.

## Backup and rollback

- Take a consistent backup with services stopped: source, configuration, state, runtime selection and service definitions.
- **Create every recovery destination before the cutover**, and check you can write to it.
- **Exercise the rollback through the actual executor**, on disposable state, including its failed-state preservation step. A good backup is not a rollback; a tested restore is. Tests of an earlier version of the executor do not count.
- Keep the old runtime until the new services have passed a real restart.

## Apply

1. Use the harness's supported update path to the pinned target, from a clean checkout.
2. Apply the reconciled effective patch.
3. **Verify by content.** Compare the effective tree ID (`capture-effective-patch.py tree`) with the candidate's, or compare full-index patches. Never compare checksums of patch text generated with abbreviated IDs.
4. Run the configuration migration, then confirm your deliberate overrides survived.
5. Point services at a stable launcher where the harness supports one, rather than at a versioned environment path, and refresh any runtime bindings owned by other applications.

If a step fails, stop and restore. An unexplained difference is a reason to stop, but diagnose it before deciding it means lost work: in October the "difference" was formatting.

## Completion check

One check, covering:

- the installed commit is the pinned target;
- every local change in the register is present, or recorded as superseded or retired;
- services were restarted and are running from the new runtime;
- a fresh session gets the instructions your changes are meant to produce;
- one real use through each interface people actually use.

An installer exit code of 0, a version label and healthy services are not completion. Neither is an old conversation that still behaves as before.

## Afterwards

Write down what happened, including anything that failed and how it was fixed, and correct the procedure where it was wrong. Keep the corrections small. After October, our sysadmin agent recommended "a small, concrete set of corrections" and, in the same sentence, "not another elaborate framework."
