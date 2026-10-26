# Recovery preparation

## October 26, 2026 — current handoff

The Google Drive image was restored directly to a physical MacBookPro8,1 using
SystemRescue rather than a Windows VM. The user confirmed boot and existing-user
login; SSH, data-readability checks and a short SSD self-test followed. The restored
hostname is sehysekaccam. Basic recovery PASSED; complete application/database
recovery and long-term hardware reliability remain unverified.

See [October 26 physical recovery report](RECOVERY-TEST-2026-10-26.md) for evidence, limitations and next steps.
Tailscale, Cloudflare Tunnel and Postfix were stopped but remain enabled at boot;
other copied application services/timers ran. Hostname change did not create fully
independent identities. Shutdown was advised but has not been confirmed.

Next: assess the other 500 GB laptop, compare candidates and choose roles.
Fresh Ubuntu for permanent secondary-server use is the agreed direction after
assessment; no reinstall, cutover or synchronization has been performed.
Preserve existing backups, recovery USB and Windows media originals.


Earlier status, October 15, 2026: Oracle backup storage and an encrypted Restic
repository have been created. A test backup of /home/devOps and an isolated file
restore comparison succeeded. Production application backups are not configured.
See [PROGRESS.md](PROGRESS.md) for the session record and remaining work.
See [RECOVERY.md](RECOVERY.md) for accessing the test backup from a replacement
computer. Keep this documentation repository private; store recovery secrets
separately in an independently accessible password manager or offline storage.

## Current local image backup handoff

The original Clonezilla attempt failed to capture the main Ubuntu logical volume;
see [Ubuntu Server Backup Report](Ubuntu%20Server%20Backup%20Report).
A separate ubuntu-disk.img and compressed ubuntu-disk.img.zst now exist on the
Seagate. Boot/login recovery on separate physical hardware has now succeeded; source capture
consistency and complete application recovery remain to be validated.
The compressed stream passed zstd verification. Current cloud backup history
is in [GOOGLE-DRIVE-BACKUP.md](GOOGLE-DRIVE-BACKUP.md).
[CLONEZILLA-HANDOFF.md](CLONEZILLA-HANDOFF.md) describes the earlier boot procedure.

## Collect the inventory

Run from an administrator terminal on the actual Ubuntu host:

```bash
umask 077
sudo python3 /home/devOps/projects/disaster-recovery/inventory.py > "$HOME/recovery-inventory.json"
```

The script only reads metadata and runs inventory commands. It does not mount
disks, stop services, install packages, read environment files, or upload data.
The report contains account names, paths, and disk identifiers: keep it private
and do not commit it to the public repository. Execution may take several minutes.
Review command errors and inaccessible paths; a partial inventory is not complete.

## Current scope

Based on the repository's October 13 recovery proposal, include MediaSpace media,
catalog, configuration, source and unpublished work; Jellyfin configuration and
databases; mail state; relevant home directories;
and system reconstruction information. Exclude Jellyfin movie/video library files.
This exclusion must be checked against actual library paths, including other disks.

Inventory sizes overlap and include disposable files. They cannot be added together
or treated as the final encrypted repository size. Database and cross-file capture
consistency must be designed after inspecting application state.

## Remaining prerequisites

- Administrator inventory and access to protected application state.
- Oracle account and VM created; backup volume attached (see progress record).
- Independent recovery credentials and an encryption password kept off-server.
- Reviewed backup source/exclusion list and version retention within available disk.
- Test upload and project-file restore comparison completed; complete application
  restoration remains outstanding.

Use Oracle only as the first backup destination: free-account inactivity and VM
reclamation remain limitations. A file restore test can run in a separate local
directory; full application recovery needs an isolated compatible VM, which can
be in the cloud. Do not start restored production mail or network identities.

## Back up your own account

See [USER-BACKUPS.md](USER-BACKUPS.md) for user-owned backups, destination
setup prerequisites, and restore verification. Each user backs up their own home;
an administrator separately covers protected system and service data.
Torrent/download state is outside the current scope because it is not configured.
