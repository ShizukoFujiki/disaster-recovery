# Server recovery runbook

This is the offline-chat procedure for recovering the Ubuntu server. Keep a
printed or offline copy with the recovery kit. This runbook distinguishes steps
that have been tested from work still required. Do not treat the server as fully
recoverable until the completion gates at the end pass.

## Current recovery capability (reviewed October 30, 2026)

- A compressed full-disk image of the Ubuntu server was uploaded to Google Drive
  using rclone crypt. `rclone cryptcheck` reported one matching file and zero
  differences. The image was downloaded and restored to a spare MacBook using
  SystemRescue; the restored Ubuntu system booted and accepted the original login.
- The rclone configuration and crypt recovery values were copied to a USB kit.
  Treat that USB as sensitive: it contains access material. The exact disk-image
  restore command and checksum transcript were not captured in this repository.
  Do not improvise a destructive whole-disk restore from this guide; see the
  image restore stop point below.
- Oracle Restic repository `sftp:backup@129.159.187.123:/backup/restic` contains
  a test snapshot of `/home/devOps` (prefix `043ab3af`). Restoring it to a
  separate directory and comparing the repository project succeeded. This is
  not a production backup of the whole server.
- No recurring production backup schedule is installed. MediaSpace, Jellyfin,
  mail, other user homes and complete system state are not confirmed protected
  by Restic. There is no validated application-level recovery test.

## Before an incident

Keep these items in at least two separately protected places, one offsite:

1. This runbook and the private GitHub repository URL.
2. Google account recovery method and MFA recovery codes.
3. Oracle account recovery method and MFA recovery codes.
4. The rclone configuration/crypt recovery material for the image.
5. The Restic repository password and the SSH private key authorized for the
   Oracle `backup` account, if the Restic repository is to be used.
6. A verified copy of the Oracle SSH host key fingerprint. It is not recorded
   yet; obtain it from the Oracle console through a separate trusted channel.

Never put passwords, private keys, OAuth tokens, rclone config, MFA codes, or
live inventory reports in GitHub or chat. If the USB kit stores keys beside the
encrypted data, possession of the kit may be enough to decrypt it. Protect it
accordingly; consider storing the decryption secret separately.

## A. Recover files from the existing Oracle Restic test snapshot

Use a trusted Linux computer with internet access. These steps recover only the
test snapshot's `devOps` home files, not a working server.

1. Obtain the Restic password and SSH key from the independent recovery store.
   Save the key as `~/oracle-recovery.key` and restrict access:

   ```bash
   chmod 600 ~/oracle-recovery.key
   ```

2. Confirm the current Oracle instance address in the Oracle console. The
   recorded address is `129.159.187.123`. Verify its SSH host fingerprint using
   a trusted Oracle console channel before accepting it. Do not bypass a
   fingerprint mismatch.

3. Confirm the repository disk is mounted on Oracle:

   ```bash
   ssh -i ~/oracle-recovery.key backup@129.159.187.123 'findmnt -T /backup/restic'
   ```

   It must show the separate `/backup` filesystem. Expected filesystem UUID:
   `d57c8986-a51b-4bfb-82f3-f7c6754b88df`. Stop if the disk is absent or the
   result is unclear.

4. Set the repository and SFTP transport in the recovery terminal:

   ```bash
   export RESTIC_REPOSITORY='sftp:backup@129.159.187.123:/backup/restic'
   export BACKUP_SSH="ssh -i $HOME/oracle-recovery.key backup@129.159.187.123 -s sftp"
   ```

5. List snapshots. Enter the Restic password when prompted; never put it on the
   command line:

   ```bash
   restic -o sftp.command="$BACKUP_SSH" snapshots
   ```

6. Restore into a new, empty directory, never over `/` or a live home directory:

   ```bash
   mkdir -m 700 "$HOME/recovered-devops"
   restic -o sftp.command="$BACKUP_SSH" restore 043ab3af \
     --target "$HOME/recovered-devops"
   ```

   Files from the recorded test snapshot appear below
   `~/recovered-devops/home/devOps`. Choose a newer snapshot from `snapshots` if
   a later production snapshot has been created. Do not run `restic init` on
   this existing repository. The test snapshot is not proof that other users or
   applications can be recovered.

## B. Restore the full disk image

The full image was successfully restored once using SystemRescue, but this
repository does not contain the exact restore transcript, image byte count,
verified checksum, or verified target-disk identification from that operation.
This is a **stop point for whole-disk restoration**: an incorrect target device
will erase the wrong disk. Do not run `dd`, `partclone`, or a disk restore
command based only on a guessed device name.

For a future image restore, first add a peer-reviewed appendix here that records:

- Exact object path and expected downloaded size from Google Drive.
- Image format and compression chain, plus tested decompression/restore command.
- A cryptographic checksum of the downloaded image and the verified value.
- How to identify the target disk by model, size and serial; target must be the
  intended replacement disk and large enough for the image.
- What existing data on the target will be erased, and a final visual device
  confirmation before writing.
- First-boot checks, including network identity and any duplicated SSH/Tailscale
  credentials when a cloned image is used.

Until this appendix exists, use the known SystemRescue procedure only with
hands-on operator confirmation and verified device details. Do not infer a
command from the fact that a prior restore succeeded.

## C. After restoring an image

1. Keep the original server disconnected or powered off while validating the
   restored copy, to avoid duplicate host identities on the network.
2. Confirm the machine boots, local login works, root filesystem mounts, and
   `hostname`, `hostnamectl`, `ip address`, and `lsblk` show the expected
   replacement machine and disks.
3. Check critical services and application data before exposing the machine to
   users. A booting disk image does not establish that every application or
   database is healthy.
4. Check DNS/tunnel, SSH, Samba, mail, Jellyfin and MediaSpace individually.
   Restore or reissue unique SSH and Tailscale identities before running a
   cloned system alongside the source server.
5. Record failures and the exact recovery actions in this repository, excluding
   secrets and private inventory data.

## Full recovery completion gates

The network is not fully protected until all of these are true:

- A root-controlled, reviewed source list covers critical system configuration,
  each agreed user home, MediaSpace production and development data, Jellyfin
  state, and actual mail storage. Known restore-test directories and bulky
  re-downloadable media are excluded only by verified path.
- Application data is captured consistently (database-aware snapshots or a
  bounded, restart-safe service pause); a live copy alone is not assumed
  consistent.
- A regular encrypted backup schedule runs with alerts on failure, locking,
  retention, protected credentials, and a destination mount/UUID guard.
- At least one restore of representative files and an isolated application
  recovery test succeed.
- The offsite recovery kit has been tested from a different computer, including
  account/MFA recovery and access to all encryption material.
- A second independent destination exists if losing the Google/Oracle account
  is part of the threat model.

Current known blocker: production scope and application-consistent backup,
automation, and isolated restore validation remain unfinished. The Oracle
volume has about 93 GiB usable; earlier source estimates were about 63 GiB for
homes alone, so measure deduplicated Restic size and available space before
committing the complete scope. Keep the existing test snapshot until a verified
replacement recovery path is in place.
