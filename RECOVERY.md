# Access recovery from a replacement computer

## Current protection level

The disk image has a verified encrypted Google Drive copy and a separate MEMOREX
USB recovery kit. Physical restoration to sehysekaccam succeeded: boot, login,
SSH and limited data checks passed. Full application/database recovery remains
unverified. See [October 26 physical recovery report](RECOVERY-TEST-2026-10-26.md) for the current handoff.

The original [VM recovery plan](VM-RECOVERY-HANDOFF.md) remains an alternative,
not the procedure used in the completed physical test.

The Oracle instructions below concern the earlier devOps-only Restic test snapshot,
not the disk image. They do not establish complete server recovery.

## Keep these independently accessible

GitHub contains instructions, not the encryption password or private SSH key.
Keep the Restic password and a recovery copy of the SSH private key in an
independently accessible password manager or encrypted offline storage. Record
the Oracle account login, MFA recovery method, and GitHub recovery method there
too. Do not depend solely on the lost Ubuntu server or Windows machine for MFA.
Do not upload private keys, passwords, .env files, or live inventory reports here.

## Recover the earlier Oracle test snapshot

1. Sign into GitHub from a trusted replacement computer and read this repository.
2. Retrieve the repository password and SSH key from independent storage. Their
   independent storage has not yet been confirmed or tested.
3. Sign into Oracle and confirm backup-instance and backup-data still exist.
   Confirm the current public IP; recorded IP is 129.159.187.123.
4. On a trusted Linux recovery computer install OpenSSH and Restic (the version
   used for the test was 0.18.1). Save the recovered SSH key as
   ~/oracle-recovery.key and restrict permissions:

```bash
chmod 600 ~/oracle-recovery.key
```

Verify the SSH host fingerprint through an independent trusted Oracle console
channel before accepting a new host key. A trusted fingerprint was not recorded
in this documentation. Then check the destination disk:

```bash
ssh -i ~/oracle-recovery.key opc@129.159.187.123 'findmnt -T /backup/restic'
```

The backup login permits SFTP only; use the administrator login opc for this
read-only mount check. It must show the separate backup filesystem mounted at /backup, not the root
filesystem. Recorded UUID: d57c8986-a51b-4bfb-82f3-f7c6754b88df.

Set these variables in the recovery terminal. Replace the IP if Oracle changed it:

```bash
export RESTIC_REPOSITORY=sftp:backup@129.159.187.123:/backup/restic
export BACKUP_SSH="ssh -i $HOME/oracle-recovery.key backup@129.159.187.123 -s sftp"
```

List available snapshots, supplying the repository password interactively:

```bash
restic -o sftp.command="$BACKUP_SSH" snapshots
```

Restore into a new empty directory, never / or existing production paths:

```bash
restic -o sftp.command="$BACKUP_SSH" restore 043ab3af --target ~/recovered-files
```

The test snapshot restores the original /home/devOps path below the target, so
files will be under ~/recovered-files/home/devOps. Snapshot 043ab3af was the only
completed backup recorded when this guide was written. Use the listing to choose
an appropriate newer snapshot if production backups are configured later.

Do not run restic init against the existing repository. Lost repository passwords
cannot be reconstructed from these instructions. If both the SSH key and access
to Oracle are lost, these instructions alone cannot restore remote access.

## Still required

- Confirm independently stored password, private key, and account recovery access.
- Record a verified SSH host fingerprint independently.
- Configure full backup scope, application consistency, mount enforcement,
  scheduling, retention, monitoring and an independent second destination.
- Validate repository data and perform an isolated application recovery.
