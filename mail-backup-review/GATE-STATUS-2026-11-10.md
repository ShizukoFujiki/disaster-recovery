# Mail backup readiness: DevOps gate status

Date: 2026-11-10

This is a sanitized status report based on the two read-only preflights and the
November 7 live metadata review. Exact source paths and identity details remain
in the protected operations record. No production capture or cutover is approved.

## 1. Encrypted destination: listing, capacity, and write access

**Current read-only status: listing and quota pass; write access remains untested.**
The first preflight did not identify a usable destination configuration. The
follow-up listing failed and its preflight withheld raw diagnostics, so the cause
of that earlier failure is unknown. A later sanitized check succeeded using a
temporary copy of the existing configuration: the remote listing returned two
top-level entries (names withheld), and reported 100 GiB total, about 52 GiB free,
and about 48 GiB used. Any OAuth refresh occurred only in the temporary copy.

No remote write/canary test has been performed, so write access is not confirmed.
Do not infer it from an earlier upload or token-refresh test.

Next: after review, perform a separately authorized, uniquely named encrypted
canary write/read/delete and verify cleanup. Record the result without publishing
object names or credentials.

## 2. Independent recovery key

**Status: unverified.** The preflight detected encrypted-remote configuration
material on the server, but did not establish that the recovery key is stored
independently or that it can restore this destination. No restore using an
independently retrieved key has been demonstrated.

Next: verify the key is available through a separate protected recovery channel,
then test it against a small isolated restore. Never put key material in this
repository.

## 3. Retention

**Status: unverified.** No current remote retention/version policy or lifecycle
behavior was confirmed. Define and test retention before capture; preserve a
known-good copy until a restore has passed.

## 4. Live mail data and writers

**Status: partially mapped from metadata observed on November 7; not a current
complete path/writer inventory.** The review identified these categories:

- Active legacy mailbox application data, written by the application service.
- Inbound originals and local processing evidence, with a periodic inbound job
  and an application worker. The worker was idle at observation; the periodic
  job was still enabled.
- Mail service configuration, service units/overrides, account mappings, and
  locally modified deployed code.
- Postfix queue/state and local system mail, with Postfix active.
- Upstream originals, envelopes, and receipts, whose remote retention and
  acknowledgment boundary remain unverified.

The exact inbound spool location was not fully confirmed from service arguments.
Dovecot was inactive; the isolated pilot is not the authoritative live mailbox.
Refresh the private path map and inspect all writer arguments before capture.

## 5. Messages arriving during capture

**Status: no verified capture barrier or reconciliation procedure.** Upstream
retention during a pause is unknown. A future capture must coordinate application
writes, the inbound timer and in-flight worker, local delivery, and queue writers.
Define a checkpoint boundary, preserve arrivals after it upstream, resume writers
in a recorded order, and reconcile message/receipt/journal state before declaring
success. Missing or ambiguous evidence must block resend or acknowledgment.

## 6. Rollback rehearsal

**Status: no full-mail rollback rehearsal.** An isolated restore of the legacy
application from a local checkpoint was tested, but it did not validate a complete
mail backup, the encrypted remote destination, inbound receipts, outbound queue,
or a one-mailbox cutover rollback. It is not sufficient rollback evidence.

## Decision

Keep production capture and cutover on hold. Required next evidence is: a
successful current remote listing/quota check; confirmed canary write/read and
cleanup; independent-key restore; defined retention; refreshed private source and
writer inventory; an arrival reconciliation plan; and a rehearsed isolated restore
and rollback.