# Backup setup progress

## October 17, 2026 — current handoff

Google Drive is configured as an additional encrypted destination, but both image
upload attempts failed during OAuth refresh. No complete offsite image is verified.
A saved Python script now replaces fragile pasted Python snippets:

```bash
sudo python3 /home/devOps/test-rclone-refresh.py
```

The script is syntax-checked; its execution result is still pending. It backs up
the config, expires the access token and tests refresh without starting an upload.
See [GOOGLE-DRIVE-BACKUP.md](GOOGLE-DRIVE-BACKUP.md) and
[test-rclone-refresh.py](test-rclone-refresh.py) for exact behavior, remaining
authorization work, and current local image status. Preserve existing Oracle
resources and both Seagate image files.

## October 15, 2026 — historical record

This record is based on terminal output and Oracle console observations supplied
by the user. This workspace does not provide direct access to the live servers.
Contains infrastructure details: keep private. No passwords or private keys recorded.

## Destination established

- Oracle region: Ashburn; availability domain AD-1. Confirm home-region eligibility
  before further resource changes. User observed Always Free on the new volume.
- Instance: backup-instance, Oracle Linux 9, VM.Standard.E2.1.Micro.
- Public IP: 129.159.187.123; administrator SSH login: opc.
- VCN: backup-network, public subnet, internet gateway and default route.
- Boot volume: console reports 47 GB; guest reports 46.6G, root 29.5G and
  /var/oled 15G. Root had approximately 25G available.
- Guest memory approximately 498 MiB, with approximately 497 MiB swap.
- SSH previously stalled during banner exchange. A normal power transition took
  roughly 10–15 minutes; connection subsequently recovered. Cause not diagnosed.
- Added 100 GB block volume backup-data, attached to the instance.
- New disk /dev/sdb had no signatures with wipefs -n before formatting.
- Created ext4 filesystem, label backup-data, UUID
  d57c8986-a51b-4bfb-82f3-f7c6754b88df; mounted at /backup, about 93G available.
- Backed up /etc/fstab to /etc/fstab.before-backup and added:

```text
UUID=d57c8986-a51b-4bfb-82f3-f7c6754b88df /backup ext4 defaults,nofail 0 2
```

- findmnt --verify reported zero errors; one existing swap-file warning.
- Reloaded systemd. Automatic mounting after a reboot has not been tested.
- Created non-sudo account backup; /backup mode 711 and /backup/restic mode 700,
  owned by backup:backup. Copied opc authorized_keys to backup's .ssh directory,
  set directory mode 700 and file mode 600, and applied restorecon.
- Confirmed SFTP as backup and findmnt shows /backup/restic on /dev/sdb.

## Encrypted repository and tests

- Restic 0.18.1 installed on Ubuntu using auroraixion's sudo privileges.
  devOps does not have sudo; no additional administrators were granted.
- SSH key used on Ubuntu: /home/devOps/ssh-key-2026-10-15.key.
- Repository: sftp:backup@129.159.187.123:/backup/restic.
- Repository ID prefix: e17c13dc2e; repository format version 2.
- Password entered interactively; off-server storage was requested but not verified.
- A repeated init failed because the repository already existed; no overwrite.
- Clipboard truncation caused the first backup to cover all /home/devOps,
  rather than just the project. Snapshot 043ab3af: 6191 files, 596.660 MiB
  processed, 239.104 MiB stored. This may include SSH keys and other hidden data.
- Another truncated command restored that snapshot to /, its original location:
  reported 2740 restored files/directories, 15.354 MiB, and 6181 skipped.
  Existing files may have been replaced. Impact has not been audited.
- Subsequently restored the snapshot separately into /home/devOps/restore-test:
  8921 files/directories, 596.660 MiB.
- Recursive diff of projects/disaster-recovery against its restored copy produced
  no output. This validates that subset, not all restored data or application recovery.
- Test restore remains on Ubuntu. Avoid including it in future backup sources.

Short commands that worked in Ubuntu's devOps shell (variables are session-only):

```bash
export RESTIC_REPOSITORY=sftp:backup@129.159.187.123:/backup/restic
export BACKUP_SSH="ssh -i $HOME/ssh-key-2026-10-15.key backup@129.159.187.123 -s sftp"
restic -o sftp.command="$BACKUP_SSH" restore 043ab3af --target ~/restore-test
```

Do not run init again. RESTIC_SFTP_COMMAND was suggested incorrectly earlier;
use the explicit sftp.command option above. Do not restore to / for testing.

## Source findings and unresolved scope

- Ubuntu host hymecymeyseh: root filesystem 108G, 83G used, 21G available before
  test restore. No complete privileged inventory report was validated this session.
- A 129 KB October 13 inventory was found under auroraixion with a newline in
  its filename. Rename/validation status became unclear; user chose short manual
  commands instead. /home/devOps/recovery-inventory.json was empty.
- /home about 62G; /var about 12G; /srv about 4.5M; /opt effectively empty.
- MediaSpace home about 40G: media-storage 6.6G, media-dev-storage 4.4G,
  projects 3G, deployments 10G, plus imports, restore tests and tooling.
- Deployment current release: 20261013T120557272858Z-5d6a45bb (829M);
  previous: 20261011T011349405759Z-f175ad25 (829M). Proposed backup selection
  retains both, but older-release exclusions are not finalized. No originals deleted.
- Preserve /home/mediaspacedev/deployments/mediaspace/shared/data entirely:
  media.json, profiles.json, site-settings.json, experience, imports and prior copies.
- Development /home/mediaspacedev/projects/sturdy-journey/data has a separate
  media.json, imports and settings. Preserve source and unpublished work too.
- Live processes run from both current deployment and sturdy-journey.
  Consistent capture method has not been designed; no services stopped.
- Other homes: maildev 5.3G, seodev 7.5G, jellyfindev 2.7G, auroraixion 5.8G.
  Much is .codex data; do not exclude wholesale without identifying history/settings.
- Jellyfin /etc/jellyfin and /var/lib/jellyfin are mode 700, owned by jellyfin.
  Inspected with sudo; permissions left unchanged. Active state about 2.8G;
  several old failed-restore copies and user restore-test directories also exist.
- Library definitions reference /mnt/jellyfin-media/Movies and Television plus
  Windows-style paths. That mount directory appeared empty from this shell;
  user says substantial linked media exists. Actual paths/mount namespace remain
  unresolved. User requested deferral. Do not assume those media are absent.
- Preserve Jellyfin settings/database; exclude movie/video files only after paths
  are established. Preserve torrent/download-client state; location not found yet.
- Postfix runs. /var/mail is small; home_mailbox, virtual_mailbox_base,
  mailbox_transport and mailbox_command are empty; virtual_transport is virtual.
  doveconf unavailable. Actual mail storage and mail application state unresolved.
- Other running services include cloudflared, Samba, Tailscale, cron and SSH;
  reconstruction configuration and credentials need encrypted coverage.

## Resume here

1. Check Ubuntu free space after the test restore; keep restore copy out of backups.
2. Review accidental restore-to-original-path impact where practical.
3. Finalize sources/exclusions, mail/download state, and application consistency.
4. Configure privileged source access without granting devOps unrestricted sudo.
5. Add an enforced remote mount/UUID check before every backup so an absent
   /backup disk cannot redirect writes to the boot disk. Not implemented yet.
6. Configure protected credentials, off-server recovery instructions, retention and
   unattended jobs. No schedule or production backup is configured yet.
7. Run production backup, repository integrity verification, representative restores,
   and isolated application recovery. Never activate restored production mail or
   duplicate network identities during testing.

Oracle is the first destination, not the only planned recovery copy. Account/VM
reclamation remains a reason to arrange an independent copy.

## Next session agreement

Paused at the user's request on October 15, 2026; resume tomorrow.
Add a second independent cloud backup provider alongside Oracle, retaining Oracle.
No second provider has been selected or configured. At the next session compare
current storage, retrieval and minimum charges, Restic support, and recovery access
before choosing. Continue the pending production backup and restore work above.
Documentation is published in the private ShizukoFujiki/disaster-recovery GitHub
repository; passwords and private keys are not included.
