# Windows VM recovery test handoff — October 17, 2026

## Resume here

The user plans to continue on October 18 using another Windows computer with
VMware or VirtualBox. The objective is to download/decrypt the Google Drive image,
restore it to a new disposable VM disk, and test boot and representative services
without affecting the original Ubuntu server. No VM restore has been attempted yet.
Guide one step at a time. Identify every disk and mount before any write.
Prefer saved scripts over multiline Python pasted into terminals.

Suggested resume prompt:

> Read VM-RECOVERY-HANDOFF.md in ShizukoFujiki/disaster-recovery. The encrypted
> image upload and cryptcheck passed, and I have the MEMOREX recovery USB. Help me
> test recovery on another Windows computer using VMware or VirtualBox. Start by
> checking available storage and creating an isolated VM. Do not overwrite any
> physical disk or start restored production services on the network.

## What completed

- The Seagate contains ubuntu-server-backup/ubuntu-disk.img and ubuntu-disk.img.zst.
- Raw image size reported by zstd verification: 121332826112 bytes (113 GiB).
- Compressed file is about 50.7 GB / 47.2 GiB.
- zstd -t succeeded on the compressed file. The original image creation command
  and source-capture consistency have not been established in this session.
- The older 170 MB Clonezilla image is incomplete and is NOT the recovery source.
- Google One 100 GB plan activated. Oracle resources were retained; the earlier
  Oracle Restic test snapshot is separate from this disk-image backup.
- rclone crypt remote securebackup: wraps gdrive:server-backup. Files and
  directory names are encrypted. The cloud object is ubuntu-disk.img.zst when
  viewed through the crypt remote.
- Ubuntu rclone updated to 1.75.2. A dedicated Desktop OAuth client was configured.
- OAuth failures were traced to authorization using the short shared-client
  command instead of the exact long command generated with the custom client.
  The Google account was added as a test user, authorization repeated with the
  long command, and the saved Python forced-refresh test PASSED.
- Final upload: 47.256 GiB transferred, 1/1 files, elapsed 5h45m14.7s.
- rclone cryptcheck ubuntu-disk.img.zst securebackup: -P completed at
  2026/10/17 18:43:32 in the supplied terminal log:
  0 differences found; 1 matching files; Checks 1/1; elapsed 11m26.8s.
  This verifies the uploaded encrypted copy against the local compressed file.
  It is NOT proof of bootability or application consistency.
- MEMOREX 128 USB recovery kit was copied and verified after correcting the
  helper script's USB-detection tree handling. User reported SUCCESS.
  Exact timestamped directory path was not supplied. Safe unmount was advised;
  completion of unmount was not confirmed.

## Credentials are on the USB, not in GitHub

Find server-recovery-<timestamp>/ on MEMOREX 128:
- rclone.conf: full Google authorization and crypt configuration.
- encryption-keys.conf: same securebackup section, including password/password2.
- RECOVERY-INSTRUCTIONS.txt: basic recovery directions.

The passwords are stored as original reversible rclone-obscured values, not as
human-readable password text. The full configuration is sufficient for rclone
decryption. Do not run obscure on these existing values again.
This USB kit is NOT encrypted; FAT does not enforce Unix permissions.
Keep it physically secure and separately from the original server.

The image predates the rclone setup. Do not expect the image to contain this
configuration or the encryption keys. Independent Google login/MFA access is
also needed if OAuth must be renewed. Existing production Ubuntu config is
/home/auroraixion/.config/rclone/rclone.conf.

Never commit rclone.conf, encryption-keys.conf, config backups, tokens, OAuth
secrets, or authorization blobs. No credentials are included in this handoff.

## Preparation on the Windows recovery computer

1. Confirm available host disk space, RAM, virtualization support, hypervisor and
   internet access. Use an Ubuntu amd64 live ISO from the official Ubuntu site.
2. Create a disposable VM with a NEW empty virtual disk of at least 128 GiB
   (137438953472 bytes). Check actual byte capacity; never assume a drive labeled
   128 GB decimal is large enough for a 121332826112-byte image.
3. Plan persistent staging storage with at least 55 GB free for the compressed
   download, plus the target virtual disk and host overhead. A 200 GiB or larger
   host free-space budget is a useful starting point, not an exact requirement.
   If also retaining the decompressed image, budget another 113 GiB.
   Thin provisioned virtual disks can grow; host free capacity must cover growth.
4. Boot the VM in Try Ubuntu/live mode. The recorded source disk included EFI,
   so use UEFI initially; confirm the image partition table before restoration.
5. Use network access only in the live environment for tools/download.
   Enable USB passthrough for MEMOREX, or copy the kit securely into the live VM.
   Never attach a host physical disk as the VM's raw restoration target.
6. Provide a separate persistent staging disk or carefully arranged host-shared
   folder for the download. Live-session RAM/tmp storage is not suitable for a
   51 GB file. Avoid FAT32 staging for the image (4 GB per-file limit).
   The MEMOREX FAT USB is for credentials, not this image.
7. Inspect lsblk and df in the live VM. Clearly distinguish live ISO, staging
   storage, USB recovery kit, and the empty virtual disk intended for restoration.

## Download and verify in the live VM

Install current rclone and zstd using supported installation methods.
Copy USB rclone.conf into a private directory in the live user's home.
Do not overwrite another configuration; restrict its permissions.

After setting the real persistent staging path, commands are:

```bash
chmod 600 "$HOME/recovery-rclone.conf"
export RCLONE_CONFIG="$HOME/recovery-rclone.conf"
rclone lsl securebackup:
```

Use the kit's existing complete configuration; do not create new crypt passwords.
For example, if persistent staging is mounted at /mnt/recovery-staging:

```bash
rclone copy securebackup:ubuntu-disk.img.zst /mnt/recovery-staging/ -P
zstd -t --progress /mnt/recovery-staging/ubuntu-disk.img.zst
rclone cryptcheck /mnt/recovery-staging/ubuntu-disk.img.zst securebackup: -P
```

Confirm all return successfully. cryptcheck compares the decrypted local file
against encrypted cloud checksums. A listing alone is not verification.

If authentication fails, reconnect gdrive with the same dedicated Desktop OAuth
client. Use the EXACT long authorization command supplied by rclone on a machine
with a browser; paste its result only at config_token>. Select No for Shared Drive.
The short shared-client authorize command caused earlier refresh failures.
Do not change securebackup passwords. Use a disposable copy of the config for
diagnostics; the committed refresh helper is hardcoded to the original server path.
Testing-mode OAuth can have limited refresh-token lifetime; review audience/
publishing status for durable access. OAuth secret rotation remains unconfirmed.

## Restore to the empty VM disk — guided step required

This is a raw .img.zst image, not a Clonezilla image directory or a VM disk file.
After verification, disconnect the VM network adapter at the hypervisor.
Ensure staging remains accessible locally.

Inspect the image partition table (decompress to staging if capacity allows) and
confirm it is a complete raw disk image before choosing a restoration method.
Record the image's exact size and the target disk's model, byte size, and partitions.
The target must be the newly created EMPTY VIRTUAL DISK, unmounted.

The intended operation is to decompress the image onto that target disk, either
from a decompressed staging file or by a checked pipeline with failure propagation.
Do NOT provide a guessed /dev/sda or /dev/sdb write command. Resolve the device
from the actual VM inventory and review the exact destructive command first.
Never write over the live server, Windows physical disks, the USB, or staging disk.

After successful writing and flush, power off, disconnect the live ISO, USB and
unneeded staging devices, keep networking disconnected, and boot the restored VM.
Firmware, virtual storage drivers, or bootloader repair may be needed; a boot
failure is a diagnostic finding, not permission to modify production systems.

## Validate and record results

- Does the restored system boot, and can an existing Linux user log in?
- Are expected files, user directories, application configuration and data present?
- Inspect MediaSpace, Jellyfin and mail data with services isolated.
- Keep the restored VM offline: production mail, cloudflared, Tailscale and other
  credentials/identities may automatically start. Do not bridge it onto production
  networks. Network testing requires separately disabling duplicate identities.
- Record commands, boot issues, representative file/application checks, and errors.
- Distinguish successful download, image write, boot, and application recovery.
- Keep the original Seagate images and verified Drive copy throughout testing.

No recurring backups, retention schedule, or full application restore are configured
or verified by the completed upload. This image does not include changes after capture.
