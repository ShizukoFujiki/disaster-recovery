# Mail backup review

These public materials summarize two read-only preflight checks, a later
partial encrypted Mailbridge checkpoint, and the remaining capture/restore
controls. See [GATE-STATUS-2026-11-14.md](GATE-STATUS-2026-11-14.md) for the
latest sanitized gate status.

## Files

- [GATE-STATUS-2026-11-10.md](GATE-STATUS-2026-11-10.md) — status at the time
  of the preflight and remote-canary checks.
- [GATE-STATUS-2026-11-14.md](GATE-STATUS-2026-11-14.md) — adds verified
  November 8 checkpoint, historical recovery-kit restore evidence, current
  phone-access observations, and remaining gates.
- reports/preflight-kg5vzidm-summary.md — first preflight result and blockers.
- reports/preflight-mn8ef7pr-summary.md — follow-up preflight result and blockers.
- SOURCE-MAP.md — sanitized description of the component categories examined.
- BACKUP-PLAN.md — scope and prerequisites; draft, not an approved recurring job.
- CAPTURE-PROCEDURE.md — controlled capture checklist; not an executable runner.
- RESTORE-PROCEDURE.md — isolated recovery checklist; not yet validated as a
  complete independent-key production-mail restore.

The original JSON reports and source mapper were withheld because they contain
private filesystem paths, account identifiers, service configuration details,
runtime metadata, and code provenance. The sanitized summaries retain results
and blockers only. No credentials, tokens, message content, key material, raw
inventories, archive hashes, server addresses, or private paths are included.

## Current conclusion

The preflights themselves did not create a backup. A later, partial encrypted
mail checkpoint was captured, uploaded, and read back successfully. A private
local restore and isolated legacy-application check also passed their stated
scope. Historical recovery records document a prior encrypted disk-image restore
using recovery material stored separately on removable media; that material was
reported unencrypted. The current kit has not been revalidated, and the November
8 mail checkpoint has not been restored using it.

Retention, complete source coverage, upstream receipt recovery,
post-checkpoint arrival protection, and a full mail cutover rollback remain
unverified. Keep production capture, DNS/public-listener changes and mailbox
cutover on hold until the remaining gates in the latest status report are
verified.
