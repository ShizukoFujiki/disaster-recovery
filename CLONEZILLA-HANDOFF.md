# Clonezilla backup handoff — October 15, 2026

## Current status — resume here

The user has finished writing a Clonezilla boot USB using Rufus on Windows.
Rufus reports READY. Clonezilla has not yet been booted on the server and no
full-disk image has been created or verified.

The Ubuntu server is an Intel MacBook Pro, hostname hymecymeyseh.
The user will continue with Codex in a Windows browser while operating the
MacBook's physical screen and keyboard. SSH will disconnect when Ubuntu shuts
down. Prior Ubuntu installation had internet connectivity problems; the local
Clonezilla backup does not require internet.

## Agreed destination and observed capacity

- Source: internal APPLE SSD SD0128, approximately 113 GiB, previously /dev/sdb.
  Partitions observed: 1 GiB EFI, 2 GiB /boot, and 109.9 GiB LVM member.
  Root filesystem had approximately 83 GiB used and 21 GiB available.
- Destination: external Seagate Portable Drive, 1.8 TiB, NTFS partition,
  previously /dev/sda1, connected directly to the Ubuntu server.
- User ran sudo ntfsinfo -m /dev/sda1. It reported cluster size 4096,
  488378111 total clusters, and 118272305 free clusters (24.2%).
  Free space is approximately 484 GB decimal / 451 GiB.
- A separate USB attached to Windows had 106 GB free before Rufus.
  This is the boot-media candidate, not the Seagate backup destination.

Device names can change when booted from USB. Identify drives again by model,
capacity and filesystem, not solely by /dev/sda or /dev/sdb.

The user authorized storing a full image on the Seagate for now. Save it in a new
directory without formatting the Seagate or removing its existing files.
A whole internal-disk image includes everything on that disk, including media,
credentials and any local restore-test files. Earlier selective Restic exclusions
do not apply to this whole-disk image. It does not capture other attached disks.

## Windows preparation — completed

1. Download Clonezilla Live stable, amd64, ISO from
   https://clonezilla.org/downloads.php.
   The user described the download as "3.3.3.3 amd64 iso"; exact filename/version
   has not been verified.
2. Use Rufus from https://rufus.ie/ to write it to a spare USB stick.
   Writing erases the selected boot USB. Never choose the Seagate destination.
3. Select the ISO and leave Rufus's selected defaults.
   Rufus requested a Syslinux download. The user initially encountered a download
   error, then successfully started image writing and reported READY.
   The final write mode was not confirmed.
4. Safely eject the boot USB from Windows.

Official USB creation instructions: https://clonezilla.org/liveusb.php.

## Next steps on the MacBook Pro

1. Plug the prepared Clonezilla USB into the MacBook; keep the Seagate connected.
   Use AC power and keep the lid open.
2. In the Ubuntu SSH terminal, shut down cleanly:

   ~~~bash
   sudo poweroff
   ~~~

3. After shutdown, turn on the Intel MacBook and immediately hold Option (Alt).
   Select the Clonezilla USB, commonly shown as EFI Boot.
4. Choose Clonezilla live (Default settings).
5. Choose the language and keyboard layout, then Start Clonezilla.

If the USB does not appear or boot, report the exact screen before changing
firmware or security settings. No internet or Wi-Fi setup is needed for a backup
to the directly connected drive.

## Save the image — guide carefully at each drive selection

Menu wording may vary by version. Use the save-image workflow:

1. Select device-image (work with disks/partitions using images).
2. Select local_dev for a local destination.
3. Let Clonezilla detect the attached drives; follow its scan/Enter prompts.
4. Select the NTFS partition on the approximately 1.8 TiB Seagate Portable Drive
   as the image repository. Confirm its model, size and available space.
   Do not select the internal 113 GiB SSD or the Clonezilla boot stick.
5. Select a new backup directory on the Seagate. Use Beginner mode and savedisk
   (save local disk as an image). Suggested image name:
   hymecymeyseh-ubuntu-full-2026-10-15.
6. Select the entire approximately 113 GiB APPLE SSD SD0128 as the source.
   Confirm the source and destination from the screen before final confirmation.
7. Keep the normal compression defaults. If asked about checking the source
   filesystem, report the options before choosing any repair operation.
8. Choose to check the saved image for restorability when offered.
9. Read the final summary and confirm only if it is saving the internal SSD into
   an image directory on the Seagate. Never choose disk-to-disk, restoredisk,
   or any formatting/overwrite operation.
10. Allow both image creation and verification to finish. Record the image
    directory, completion messages and verification result.
11. Shut down through Clonezilla, remove the boot USB, then start Ubuntu normally.
    Confirm its normal services return.

Do not call this backup complete until Clonezilla reports successful creation
and image verification. Verification alone is not a tested full restore.
No restore should be run against the live internal disk as a test.

A full disk image can contain secrets. Encryption has not been configured or
confirmed in this session. Keep the drive physically protected; ask about
Clonezilla encryption before writing if encrypted storage is wanted.

## Prompt to resume in Windows

"Read CLONEZILLA-HANDOFF.md in ShizukoFujiki/disaster-recovery. My Clonezilla USB
is ready. Walk me through booting my Intel MacBook Pro and saving its 113 GiB
internal SSD as an image on the 1.8 TiB Seagate, preserving the Seagate's existing
files. Check the drives shown on screen before the final save confirmation."

Existing cloud backup work remains documented in PROGRESS.md and RECOVERY.md.
This local image is an additional recovery copy; unattended production backup
and full restoration testing are still pending.
