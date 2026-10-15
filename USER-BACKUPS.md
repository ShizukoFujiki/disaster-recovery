# Back up your own server account

Status: instructions prepared October 15, 2026. No new user repository, SSH
account, or schedule has been configured by this guide. Only devOps has a
confirmed test snapshot. Finish destination setup before running a backup.

## Where to get these instructions

Read this file in the private ShizukoFujiki/disaster-recovery GitHub repository.
GitHub access is separate from your Linux account. Ask the repository owner for
access, or have the administrator copy this document to ~/backup-instructions.md
in your account. Do not make other users' home directories readable to distribute
these instructions. A local file under /home/devOps is not accessible to everyone.

## Responsibility and scope

Each user runs backups as themselves and supplies their own encryption password.
An administrator separately backs up protected system and service-owned state.
A home-directory backup alone is not a complete server recovery backup.

| Account | Preserve in its home directory |
| --- | --- |
| mediaspacedev | MediaSpace source, unpublished work, uploads, media-storage, media-dev-storage, production shared data, development data, configuration and required releases |
| maildev | Projects, configuration and any mail data owned by this account |
| seodev | Projects, unpublished work, configuration and history |
| jellyfindev | Projects, scripts and user-owned settings; the administrator handles Jellyfin's protected service data |
| auroraixion | Personal files, projects, configuration and history |
| devOps | Recovery tools, documentation and account settings; exclude restore-test |
| winscpuser | Any files actually stored in this account |

Do not exclude MediaSpace uploads by file extension. Exclude Jellyfin movie and
television video libraries by their verified paths. Torrent/download software is
not configured on this server and is outside the current scope. Review nested
mounts, links, caches and old restore copies before finalizing exclusions.

## 1. Work as the account being backed up

Sign in normally as that user. An administrator can instead open its login shell,
for example:

```bash
sudo -iu mediaspacedev
```

Then run these commands without sudo:

```bash
whoami
printf '%s\n' "$HOME"
restic version
```

If Restic is unavailable, ask the administrator to install it. Do not change
ownership of other accounts' files to make a backup succeed.

## 2. Make a separate SSH key

Check whether this dedicated key already exists:

```bash
ls -l ~/.ssh/oracle-backup-ed25519*
```

If it does not exist, create it (do not overwrite an existing key):

```bash
install -d -m 700 ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/oracle-backup-ed25519 -C "$(whoami)-oracle-backup"
```

Choose a passphrase for interactive use. Unattended access needs a separately
reviewed credential arrangement; an interactive setup is not yet a scheduled job.
Give the administrator only the public key:

```bash
cat ~/.ssh/oracle-backup-ed25519.pub
```

Keep the private key and future Restic password in independent recovery storage.
Do not put them in GitHub, chat, this guide, or another user's account.

## 3. Administrator prepares this user's destination

This is a one-time Oracle administration task. The administrator must:

1. Give the user a dedicated remote account and directory on the backup volume,
   with their public key installed. Restrict filesystem access so users cannot
   read, modify or delete each other's repositories. Separate encryption
   passwords alone do not prevent deletion through shared SSH access.
2. Leave the existing devOps repository /backup/restic intact. Other users get
   separate repositories; do not initialize inside /backup/restic.
3. Confirm the repository is on the mounted /backup filesystem with UUID
   d57c8986-a51b-4bfb-82f3-f7c6754b88df. Enforce a mount check before every
   repository write, and deny the backup account writes to the underlying boot
   disk mount directory if the data volume is absent. A one-time check is not
   enough. This enforcement is still to be implemented and verified.
4. Check shared free capacity. The original backup volume has approximately
   93 GiB usable; separate repositories do not deduplicate across accounts.
5. Supply the user with an exact repository URL, remote login, verified SSH host
   fingerprint and confirmed exclusions. Recorded Oracle IP: 129.159.187.123;
   verify it is still current.

Do not give every user the existing backup login/private key. Do not continue
with uploads until the administrator confirms these destination requirements.

## 4. Connect and initialize once

After destination preparation, the administrator supplies a complete SSH config
entry for the alias oracle-account-backup, including the assigned HostName,
User, IdentityFile, IdentitiesOnly yes and connection timeout. Verify its host
fingerprint against the trusted Oracle console before accepting it. Never disable
host-key checking to get past a mismatch.

Set the exact repository URL supplied by the administrator in your terminal:

```bash
read -r -p 'Your assigned Restic repository URL: ' RESTIC_REPOSITORY
export RESTIC_REPOSITORY
```

Its format is sftp:oracle-account-backup:/absolute/assigned/repository. Do not use
that example literally and do not point it at the devOps repository.

For a NEW, EMPTY repository only:

```bash
restic init
```

Choose your own encryption password and store it off-server. If a repository
already exists, use restic snapshots; do not initialize again or delete it.

## 5. Review and run a backup

Start with a non-writing preview of your own home:

```bash
restic backup --dry-run --one-file-system --exclude "$HOME/restore-test" "$HOME"
```

This includes hidden files. The filesystem option skips nested filesystems;
review those separately. Restic preserves symlinks rather than following their
targets, so required data outside your home needs explicit coverage.

Before the real run, agree how running applications produce a consistent capture.
For MediaSpace, identify and capture both development and production mutable
state. A live file copy alone is not proof of application consistency. Do not
leave applications stopped during a long network upload. Jellyfin and Postfix
service-owned data belong in the separate administrator backup.

Once destination enforcement, exclusions, capacity and application capture have
been reviewed, run:

```bash
restic backup --one-file-system --exclude "$HOME/restore-test" "$HOME"
```

Treat permission errors, changed/unreadable-file warnings and any nonzero exit
status as requiring investigation. Record the snapshot ID and actual stored size.
Do not schedule or prune yet.

## 6. Verify recovery

List snapshots and check the repository:

```bash
restic snapshots
restic check
```

Select the snapshot ID from that successful run and restore into a NEW directory:

```bash
read -r -p 'Snapshot ID to test: ' SNAPSHOT_ID
RESTORE_TARGET=$(mktemp -d /tmp/account-restore.XXXXXXXX)
restic restore "$SNAPSHOT_ID" --target "$RESTORE_TARGET"
printf 'Restored files are under %s\n' "$RESTORE_TARGET"
```

Check available space first; a full restore must fit. If it will not fit, restore
selected representative files or use another isolated machine. Compare files
and validate application data. A repository check alone does not validate a
working application. Never restore over / or live production paths for testing.
Never activate duplicate production mail or network identities in a restore test.

After a successful manual backup and restore, configure a user-owned schedule,
noninteractive protected credentials, failure reporting, retention based on real
capacity, and a second independent destination. These remain pending.

## References

- [Restic repository and SFTP setup](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)
- [Restic backup behavior and exclusions](https://restic.readthedocs.io/en/stable/040_backup.html)
- [Server recovery instructions](RECOVERY.md)
