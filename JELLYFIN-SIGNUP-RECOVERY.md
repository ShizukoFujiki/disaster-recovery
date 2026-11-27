# Jellyfin signup backup and recovery

## Backup destinations

- **Google Drive** holds the encrypted server image for whole-server recovery.
- **The second 500 GB MacBook** is the replacement Ubuntu server. Ubuntu Server is installed, Ethernet and SSH login work, and the expanded root filesystem has about 370 GiB free. The original storage laptop continues to host the Windows Media Archive. Test application recovery on the replacement before switching live traffic.
- **The 930 GB Windows laptop** will receive the nightly encrypted incremental backups. Confirm the destination folder, free space, and overnight availability. Cron and custom scripts will run on Ubuntu and send backups to the Windows destination.
- **Oracle** is excluded from this backup plan.

Signup backup coverage and application-level recovery still need to be verified. The existing Jellyfin restore and test copies are awaiting retention review, and the authoritative recovery copy has yet to be identified.

## Backup scope

The schedule is a nightly encrypted incremental backup with 30-day retention and an additional capture before each release. Before enabling cron, verify the first backup and an isolated restore, and confirm the script stops if the designated backup volume is unavailable. Keep credentials and environment values on the server. Capture the signup database consistently, plus the application version, migrations, and configuration required for recovery. Exclude the movie and TV libraries. Handle any outbox keys separately from the backup data.

## Before relying on the backup

1. Confirm the maintenance access route, primary and backup recovery operators, maximum acceptable data loss, and target recovery time.
2. Verify available capacity on the separate backup computer and measure the initial backup size and expected growth before enabling the schedule.
3. Restore a representative backup into a disposable environment with synthetic data and external email disabled. Verify the database, migrations, and operation state, and record elapsed time.
4. Decide whether separately protected outbox keys will be recovered or pending payloads will be quarantined and reissued by an authorized operator. Verify that a restore does not send old messages automatically.
5. Record the backup and restore evidence and identify the authoritative recovery copy before approving removal of old restore and test copies.

The isolated signup staging run still requires an approved window and a fresh disk-space check. Staging validation and backup recovery validation are separate checks.
