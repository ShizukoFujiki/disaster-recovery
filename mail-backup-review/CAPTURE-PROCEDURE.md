# Mail capture procedure

Status: review checklist only. This is not a runnable script. Exact live paths,
units, destination, and credential references must be confirmed in the private
operations record before use.

1. Select a checkpoint and document the mailbox scope, exclusions, and recovery
   owner. Confirm that the encrypted destination and its independently stored
   recovery key are available.
2. Verify destination read/write access, capacity, retention, and integrity
   tooling without exposing credentials or message contents.
3. Inventory every writer and in-flight operation, including inbound polling,
   application API writes, local delivery, and outbound queue activity.
4. During an approved maintenance window, coordinate or pause writers using the
   reviewed service-specific runbook. Preserve and account for messages that
   arrive after the checkpoint. If any writer cannot be quiesced or reconciled,
   stop before capture.
5. Capture the paired mail data, processing evidence, queue state, and required
   configuration using the approved encrypted backup method. Generate a
   manifest and checksums. Do not place secrets in the manifest.
6. Verify the completed object at the destination and perform a small isolated
   restore test. A successful listing or upload alone is not proof of recovery.
7. Resume services in the recorded order, verify their health, reconcile queued
   and newly arrived messages, and record the final checkpoint boundary.
8. Keep earlier known-good backups until the restore evidence is reviewed.

Do not stop production services, upload a live capture, or change DNS or public
listeners by following this checklist alone.
