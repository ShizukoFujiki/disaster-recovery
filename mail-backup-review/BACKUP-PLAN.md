# Mail backup plan

Status: draft. No complete current mail backup or full live mail restore has
been demonstrated by the two preflight reports.

## Required scope

Before capture, privately identify the authoritative locations and owners for:

- Mailbox messages, metadata, identities, folders, and read state.
- Retained inbound originals, delivery envelopes, acknowledgements, and
  de-duplication or ownership journals.
- The accepted outbound queue and its delivery state.
- Mail service configuration, account mappings, service definitions, and the
  deployed application revision, including reviewed local changes.
- Encryption and recovery material, stored separately from both the source
  server and this public repository.

Do not assume that repository defaults describe the live system. Record exact
sources, exclusions, writers, and consistency requirements in a private,
access-controlled operations record before scheduling capture.

## Required controls

1. Confirm the source list and exclusions with the service owner.
2. Verify the encrypted destination can be read and written, has sufficient
   capacity, and can be recovered with independently stored key material.
3. Confirm retention and protect messages accepted after the selected checkpoint.
4. Coordinate every application, inbound-worker, and mail-queue writer. Use a
   consistent snapshot or a reviewed maintenance pause; do not copy a live,
   changing set and call it coherent.
5. Produce an encrypted backup with a manifest and integrity checks. Preserve
   prior known-good backups until a separate restore has passed review.
6. Resume only the services that were paused and reconcile arrivals and queue
   state before declaring the capture complete.
7. Record the backup identifier, verification outcome, exclusions, and recovery
   duration without publishing private paths or secrets.

## Current gates

Remote destination access, recovery-key independence, upstream retention,
post-checkpoint arrival protection, complete writer coordination, and
crash-safe service recovery remain unverified. The preflight space check is not
a backup. Do not start production capture or cutover until these gates and a
rollback plan are approved.
