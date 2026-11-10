# Mail restore procedure

Status: proposed isolation procedure. A complete live-mail restore has not yet
been verified. Do not restore over production paths.

1. Select a verified backup and matching manifest. Retrieve the recovery key
   through an independent protected channel; never store it in this repository.
2. Prepare a separate restore target with outbound delivery disabled and no
   credentials that can acknowledge or modify upstream messages.
3. Restore into a new, empty location. Preserve ownership, permissions, account
   mappings, and the relationship between mailbox data, inbound originals,
   processing receipts/journals, and queued outbound messages.
4. Verify checksums, expected objects, message identity, MIME content, account
   isolation, folder/read state, and consistency between messages and their
   processing records.
5. Start only isolated services. Confirm that no message is delivered externally
   and no upstream acknowledgement or resend occurs during validation.
6. Compare the restored checkpoint with the latest known accepted arrival.
   Missing or ambiguous post-checkpoint evidence is a stop condition, not
   permission to resend or mark a message processed.
7. Document recovery time, verified scope, exclusions, and remaining gaps.
   Review the result before planning any production cutover.
8. For an approved live recovery, use a separate maintenance plan with a tested
   reverse path. Keep the original source and known-good backup intact until
   the restored service is accepted.

The prior isolated legacy-application restore did not validate complete mailbox,
inbound-receipt, outbound-queue, or independent off-host recovery.
