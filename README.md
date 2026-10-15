# Recovery preparation

Status updated October 15, 2026: Oracle backup storage and an encrypted Restic
repository have been created. A test backup of /home/devOps and an isolated file
restore comparison succeeded. Production application backups are not configured.
See [PROGRESS.md](PROGRESS.md) for the session record and remaining work.
See [RECOVERY.md](RECOVERY.md) for accessing the test backup from a replacement
computer. Keep this documentation repository private; store recovery secrets
separately in an independently accessible password manager or offline storage.

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
databases; torrent and download-client state; mail state; relevant home directories;
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
- Test upload and project-file restore comparison completed; isolated application
  restoration remains outstanding.

Use Oracle only as the first backup destination: free-account inactivity and VM
reclamation remain limitations. A file restore test can run in a separate local
directory; full application recovery needs an isolated compatible VM, which can
be in the cloud. Do not start restored production mail or network identities.
