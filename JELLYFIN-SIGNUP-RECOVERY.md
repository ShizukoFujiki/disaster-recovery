# Jellyfin signup backup and recovery

## Backup destinations

- **Google Drive** holds the encrypted server image for whole-server recovery.
- **A separate computer** will receive the automated encrypted Jellyfin signup backups. Its identity, destination path, and available capacity still need to be confirmed.
- **Oracle** is excluded from this backup plan.

Signup backup coverage and application-level recovery still need to be verified. The existing Jellyfin restore and test copies are awaiting retention review, and the authoritative recovery copy has yet to be identified.

## Backup scope

The agreed schedule is a daily encrypted backup with 30-day retention and an additional capture before each release. Capture the signup database consistently, plus the application version, migrations, and configuration required for recovery. Exclude the movie and TV libraries. Handle any outbox keys separately from the backup data.

## Before relying on the backup

1. Confirm the maintenance access route, primary and backup recovery operators, maximum acceptable data loss, and target recovery time.
2. Verify available capacity on the separate backup computer and measure the initial backup size and expected growth before enabling the schedule.
3. Restore a representative backup into a disposable environment with synthetic data and external email disabled. Verify the database, migrations, and operation state, and record elapsed time.
4. Decide whether separately protected outbox keys will be recovered or pending payloads will be quarantined and reissued by an authorized operator. Verify that a restore does not send old messages automatically.
5. Record the backup and restore evidence and identify the authoritative recovery copy before approving removal of old restore and test copies.

The isolated signup staging run still requires an approved window and a fresh disk-space check. Staging validation and backup recovery validation are separate checks.
