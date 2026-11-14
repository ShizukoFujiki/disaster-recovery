# Mail backup and phone-access gate status

Date: 2026-11-14

This report adds evidence recorded after the November 10 preflight review. It is
sanitized; exact paths, account identifiers, archive hashes, object names and
credentials remain in protected operations records. No production cutover is
approved.

## Backup checkpoint

**A partial encrypted mail checkpoint was captured on November 8, uploaded, and
read back successfully through the existing encrypted-remote configuration.**
The archive was approximately 485 MB. Local source manifests matched before and
after capture. The remote download comparison matched the staged archive, and
remote deletions were not performed.

The known capture scope included legacy Mailbridge application/runtime data,
known inbound processing data, mail configuration and service definitions,
Postfix queue/state, local mail spool, Dovecot configuration, and installed
launch files. Known application, inbound, and Postfix writers were quiesced for
the capture and resumed successfully. A private restore verified 4,581 regular
files against the captured content manifest.

A separate isolated application test from the local checkpoint passed its stated
legacy API checks, including 405 restored original records, 857 content
comparisons and 48 attachment checks. The test used a fresh credential and
network isolation; it did not send mail or write to upstream services.

**This is not a complete recoverable production-mail backup.** The source and
writer inventory still has unresolved paths and writers. No upstream archive,
envelope, or receipt snapshot was captured. The checkpoint does not prove
protection or reconciliation of arrivals after its checkpoint boundary. The
application test restored from the local checkpoint; it was not an application
restore using an independently retrieved recovery key and the remote mail
checkpoint. Dovecot/standard-client migration and one-mailbox cutover rollback
were not tested.

## Encrypted destination and recovery material

Current read-only quota/listing checks passed: 100 GiB total, about 52 GiB free,
about 48 GiB used; the listing returned two top-level entries with names
withheld. A separate unique encrypted canary write, matching read-back, and
cleanup passed. The November 8 mail archive upload and downloaded-content
comparison also passed using the existing encrypted-remote configuration.

The cause of an earlier failed listing remains unknown.

**Historical recovery evidence is incomplete:** an October 26 report separately
records a successful restore of a prior encrypted full-disk image to another
computer and records recovery configuration on separate removable media. The
available report does not include a transcript proving that this particular
recovery configuration was used for that restore. The configuration was
recorded as unencrypted. Thus separate storage is documented, but an independent
key's use in a restore is not conclusively demonstrated. The media's current
availability/readability and restoration of the November 8 mail checkpoint using
it remain unverified. Keep the media protected and do not publish its identity or
contents.

## Retention and future arrivals

**Retention remains unverified.** No recurring capture schedule, remote retention
or lifecycle policy, or failure monitoring was established by the checkpoint.
A read-only inventory of current system-level timers on November 14 found no
Mailbridge backup job. Per-user timers and cron schedules have not been verified.

The local capture paused known writers and resumed them, but no corresponding
upstream archive/receipt snapshot or verified preservation/reconciliation of
mail arriving after the checkpoint was demonstrated. Missing or ambiguous
post-checkpoint evidence must remain a hold; it is not authorization to resend
or acknowledge a message.

## Phone-access observations

The router’s WAN IPv4 was reported to match the current public IPv4. The router
uses Automatic DHCP; ISP address stability and inbound port filtering remain
unconfirmed. Single-port forwarding is available, with no existing rules for
ports 993 or 587. IPv6 is set to Automatic/Enabled, but no prefix is present and
no IPv6 port-service exception is configured. The mail hostnames had no A/AAAA
records at the latest check; Dovecot was inactive and no 993/587 listeners were
present. No router, DNS, firewall, or live mail-service changes were made.

## Decision

Keep production capture, public listener activation, DNS changes and mailbox
cutover on hold. Remaining backup gates are: confirm current access to the
separate recovery media and demonstrate its use to restore the November 8 mail
checkpoint; define and test retention; complete the current source/writer
inventory; demonstrate post-checkpoint arrival protection and reconciliation;
and rehearse a full paired restore and one-mailbox rollback. Phone access
additionally requires ISP address/port confirmation, trusted certificate
ownership and a reviewed service plan.
