# Google Drive backup and token refresh — October 17, 2026

## Current status — upload verified

The final upload SUCCEEDED: 47.256 GiB, 1/1 files, elapsed 5h45m14.7s.
The subsequent cryptcheck returned 0 differences and 1 matching file in 11m26.8s.
A MEMOREX USB recovery kit was copied and verified; it contains the full config,
recoverable crypt settings and instructions, without encryption of the USB itself.
Physical restore and boot/login succeeded on October 26; see [October 26 physical recovery report](RECOVERY-TEST-2026-10-26.md).
Complete application/database recovery remains unverified; recurring backups are
not configured. The earlier Windows VM plan was not used.

## Local image and earlier troubleshooting

The Seagate holds ubuntu-server-backup/ubuntu-disk.img (113 GiB) and
ubuntu-disk.img.zst (about 47.2 GiB / 50.7 GB). The compressed file passed
zstd -t, reporting 121332826112 decompressed bytes. This establishes compressed
stream integrity, not completeness of the source capture or a tested system restore.
The earlier 170 MB Clonezilla image is incomplete; see Ubuntu Server Backup Report.

Oracle remains configured with its earlier Restic test snapshot. Intermittent SSH
banner timeouts prevented uploading this disk image. Oracle was not removed.
Google Drive was selected as another destination. The user activated a 100 GB
Google One plan; rclone reported 99.702 GiB free before the image attempts.

rclone remotes:
- gdrive: Google Drive, scope drive.file.
- securebackup: crypt over gdrive:server-backup, standard filename encryption
  and directory encryption. Both crypt passwords must be stored independently.
- Configuration: /home/auroraixion/.config/rclone/rclone.conf.

A small encrypted file upload and decrypted read succeeded. Image uploads failed
at OAuth refresh: approximately 3.641 GiB in the first attempt and 7.383 GiB after
55 minutes in a later attempt. The error summary showing 100% is NOT completion.
These were earlier failed attempts; the later successful upload is recorded above.

Ubuntu rclone was updated from 1.60.1-DEV to 1.75.2 using the official installer
after selfupdate failed hash-signature verification. Windows reported 1.75.1.
A dedicated Desktop app OAuth client was created with Google Drive API enabled.
The gdrive remote was reconnected again after unauthorized_client errors.
The user later confirmed using the short shared-client authorization command in
Windows. The exact long custom-client command was required. After adding the
Google account as a test user and authorizing with that command, forced token
refresh passed and the full image upload succeeded.

## Python script used to diagnose token refresh

Repeated multiline snippets and long one-liners failed when pasted with indentation
or line breaks. Use a saved Python file instead of asking the user to paste Python
into the shell or interactive interpreter.

The script is committed as [test-rclone-refresh.py](test-rclone-refresh.py).
The current local copy is /home/devOps/test-rclone-refresh.py. Run:

```bash
sudo python3 /home/devOps/test-rclone-refresh.py
```

Review the script before running a downloaded copy as root. On another machine,
save the repository file to a trusted local path and adjust the configured path if needed.

The script:
1. Reads the local plaintext rclone configuration and checks for a refresh token.
2. Makes a timestamped backup beside it, restricted to mode 0600.
3. Marks only the gdrive access-token expiry as old to force refresh. Crypt
   passwords and client credentials retain their existing values.
4. Runs rclone about gdrive: with the exact config path and a 120-second overall
   timeout. It prints storage capacity or the normal rclone error, not config contents.
5. Starts no image upload, deletion, restore, or service change.

Validation: syntax checked and user-executed. Initial forced refresh failed;
after correcting authorization, it PASSED and reported 100 GiB capacity.
Stop other rclone jobs before running, because this test rewrites the config.
Backups contain credentials and encryption settings: never commit or share them.
The script uses configparser and expects this plaintext INI configuration;
an encrypted config requires a different procedure. A failed test leaves the
access token expired intentionally; it does not automatically restore the backup.

## Completed upload procedure (historical)

Confirm the existing encrypted test file still decrypts:

```bash
export RCLONE_CONFIG=/home/auroraixion/.config/rclone/rclone.conf
rclone cat securebackup:backup-test.txt
```

Before another image upload, resolve the client-secret exposure noted below,
confirm account access and current capacity, and arrange a terminal session that
survives a Windows SSH disconnect. Do not promise a single-file upload will resume
across separate rclone processes. Keep the original and compressed Seagate files.

The image upload command, from the image directory with the config above selected:

```bash
rclone copy ubuntu-disk.img.zst securebackup: -P
```

Require a successful final exit and remote verification before declaring the image
protected. Use cryptcheck or a downloaded decrypted hash comparison; a directory
listing alone is not integrity verification. Physical boot/login recovery has since succeeded; full application/database
restoration remains unverified.
No recurring schedule or retention policy has been configured.

## Recovery credentials and remaining work

Keep both crypt passwords, Google account recovery/MFA access, and a protected
recovery copy of rclone configuration accessible without the original server.
The configuration contains OAuth tokens and obscured encryption passwords.
Do not publish config, tokens, client secrets, or authorization command blobs.

An authorization command containing an encoded client secret was pasted into
chat. Rotate that OAuth client secret and update/reconnect rclone before relying
on unattended uploads; the rotation has not been confirmed. Review the OAuth
audience/publishing state for durable refresh authorization as well.

Official references:
- https://rclone.org/drive/
- https://rclone.org/remote_setup/
- https://rclone.org/crypt/
