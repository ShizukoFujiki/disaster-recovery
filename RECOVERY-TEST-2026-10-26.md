# Recovery and laptop assessment report — October 26, 2026

## Outcome

The encrypted Google Drive disk image was recovered onto a separate physical
MacBook Pro. The user confirmed download/restoration completed, the machine booted,
and an existing account could log in. Subsequent reports confirm Ubuntu is running
on MacBookPro8,1 with a Samsung 250 GB SSD, distinct from the original server's
MacBookPro11,1 hardware. The restored hostname was changed to sehysekaccam.

This establishes cloud-image recovery, physical boot, login, SSH access and limited
data-readability checks. It does NOT establish complete application recovery,
database consistency, current production data, failover readiness or long-term
hardware reliability. The exact download/decompression/write command transcript
was not supplied; do not invent an audited restore command sequence.

## Plan change and equipment

The initial Windows/VirtualBox proposal was superseded by a direct restore to an
older MacBook Pro that had Linux Mint. The user authorized replacing Mint because
the laptop had nothing to preserve. VirtualBox was not used for this recovery.

Two laptops are available locally: this 250 GB machine and another reported 500 GB
machine. The wider goal is to assess up to ten laptops for media storage, network
shares, a secondary MediaSpace instance or spare hardware.

The agreed direction is to finish appropriate checks, assess the 500 GB laptop,
choose roles, and install fresh Ubuntu for permanent secondary-server use rather
than retain a production clone indefinitely. No fresh installation or permanent
role assignment has happened. No migration or ongoing synchronization was configured.

## Backup source and USB identification

- Recovery source: ubuntu-disk.img.zst, about 50.7 GB / 47.2 GiB compressed,
  121332826112 bytes / 113 GiB decompressed.
- Original and compressed copies remain on the Seagate; encrypted copy is on
  Google Drive through the securebackup rclone crypt remote.
- Earlier upload and cryptcheck succeeded: 1 matching file, 0 differences.
- The older approximately 170 MB Clonezilla directory is incomplete and was not
  the restore source.
- MEMOREX 128 is the separate FAT recovery-key USB. Its top level contained
  server-recovery-20261017T190806944371 and ordinary stored files; it was not
  identified as the boot stick. Its recovery configuration is unencrypted.
- The second stick was approximately 29.3 GiB, label RESCUE1302, and booted
  SystemRescue 13.02 x86_64 successfully.
- Initial SystemRescue disk inventory: Samsung SSD target /dev/sda, RESCUE1302
  boot USB /dev/sdb. Device names are observations from that boot, not reusable
  target selections for another machine.
- SystemRescue had Ethernet and rclone, zstd and sshd available. SSH listening
  was confirmed, but early remote probes timed out. The user subsequently
  completed recovery; the network-probe issue was not fully diagnosed.

## Restored-system findings

Evidence: user-provided terminal output plus reports transferred to the original
server and reviewed on October 26.

- Hardware MacBookPro8,1; Intel Core i7-2620M, two cores/four threads.
- Approximately 8 GB installed memory (7.2 GiB available to the restored OS);
  about 6.3 GiB available during assessment.
- Ubuntu 26.04.1 LTS, kernel 7.0.0-38-generic.
- Successful boot, existing-user authentication, Ethernet and SSH.
- systemctl reported running and zero failed system units at collection time.
- Expected user directories, Jellyfin configuration/state, mail directory and
  MediaSpace production/development data paths were present and readable.
- MediaSpace production media.json, profiles.json and site-settings.json parsed
  as JSON. Development media.json and site-settings.json also parsed; development
  profiles.json was absent and may be optional.
- JSON parsing proves syntax/readability, not catalog accuracy, file completeness,
  linked media availability or functional application behavior.
- SQLite/database consistency and protocol/UI/application workflows were not tested.
- External Seagate libraries and Windows media are not included merely because
  the internal disk image was restored. Their absence is not by itself a failed restore.

## Copied services and identity

Tailscale, Cloudflare Tunnel and Postfix were stopped and confirmed inactive.
They remained ENABLED at boot in both reports. A reboot can start them again.
Docker/containerd/Dovecot units were absent in the captured system; Docker stop
errors were therefore consistent with missing units.

Other copied workloads were still active: Jellyfin, Samba, MediaSpace production
and development user services, Mailbridge server and user timers. Mailbridge inbound
and MediaSpace reporting timers were listed. No comprehensive persistent test-mode
isolation was applied; do not claim the restored system was fully isolated.

Hostname was changed from hymecymeyseh to sehysekaccam and confirmed in the later
report. Hostname change alone does not replace copied machine ID, SSH host keys,
Tailscale identity, tunnel credentials or other application identities.
Copied services must not be treated as an independently configured secondary server.

Poweroff was recommended via sudo poweroff on sehysekaccam. The user has not
confirmed shutdown completion. Keep the original server running. Before a later
online boot, account for copied services that remain enabled.

## Disk layout

Samsung SSD 850 EVO 250GB, 232.9 GiB actual capacity. Restoring the smaller image
retained approximately 1 GiB EFI, 2 GiB /boot, and a 109.9 GiB LVM partition.
Root filesystem: approximately 108 GiB, 82 GiB used, 22 GiB available.

Approximately 120 GiB lies outside the restored partition layout.
fdisk reported GPT PMBR size mismatch and backup GPT not at device end, consistent
with copying a smaller whole disk onto a larger SSD. The inspection was read-only;
no GPT repair, partition expansion, pvresize, LV growth or filesystem growth ran.
A fresh installation can establish the desired layout after roles are selected.

## SSD health and short self-test

smartmontools was installed on sehysekaccam for diagnostic queries; package
installation may enable its normal monitoring service. The read-only query
script did not start a self-test. A short self-test was subsequently started
explicitly by the user.

Recorded findings:
- SMART overall-health self-assessment PASSED.
- 4181 power-on hours at collection.
- Zero reallocated sectors/reserved-block use, program failures, erase failures,
  runtime bad blocks, uncorrectable errors and CRC errors in reported counters.
- Extended comprehensive error log: No Errors Logged.
- Current SSD temperature approximately 33–34 C.
- Short offline self-test: Completed without error, 00% remaining, no failing LBA.

Limitations:
- Self-test/selective-log checksum warnings and SCT diagnostic version/field
  anomalies were reported. Their cause is unresolved; no claim of a perfectly
  healthy drive or exact remaining lifespan is made.
- No extended self-test, sustained read/write/load test, memory test or extended
  stability observation was performed.
- No destructive disk testing, repairs, firmware update or formatting was done.
- The SSD is a reasonable candidate for continued evaluation, not certified
  reliable solely on these results.

## Cooling, battery and Wi-Fi

One CPU package reading was 60 C; battery thermal reading 33.8 C.
These are point-in-time readings, not a cooling stress assessment.
Battery reported 727 cycles, charge_full 5154000 versus design 5770000
(approximately 89% of design); charge percentage and status were not fully
consistent. Physical swelling/condition and runtime remain unassessed.

Wi-Fi hardware is PRESENT: Broadcom BCM4331 802.11a/b/g/n, wl driver bound.
NetworkManager still marked it unavailable. The earlier suspicion that Wi-Fi
had been removed was not supported by hardware enumeration. Radio/driver operation
remains undiagnosed. Ethernet was functional.

## Scripts and local evidence

Scripts created on the original server and transferred using SCP:
- /home/devOps/recovery-check.py: read-only recovery inventory.
- /home/devOps/assess-sehysekaccam.py: model/hostname-guarded read-only assessment.
- /home/devOps/check-sehysekaccam-ssd.py: model/hostname guard, optional
  smartmontools installation, read-only SMART and kernel-warning collection.

The hardware-guarded scripts rejected the original server during validation.
Report paths on the original server:
- /home/devOps/recovery-macbook-report.log
- /home/devOps/sehysekaccam-assessment.log
- /home/devOps/sehysekaccam-ssd-health.log

The report files contain infrastructure metadata and potentially hardware serials.
They are retained locally; raw logs, serials, credentials, tokens, and recovery-key
configuration are not published with this summary. The final short-test result
was supplied in chat and is summarized above.

## Next session handoff

1. Confirm sehysekaccam shutdown if that was performed. Do not assume it is off.
2. Assess the 500 GB laptop: model/CPU/RAM, disk health, network, temperatures,
   battery physical condition and stability. Do not assume it matches this hardware.
3. Do not restore the whole production image onto every candidate solely to assess
   hardware. Use a generic inventory/live environment appropriate to each machine.
4. Compare the laptops and choose primary media-storage, network-share, application
   or spare roles. Measure the Windows media collection before planning storage.
5. Keep Windows media originals until copied data is verified. A network share
   alone is not a backup.
6. Fresh Ubuntu for permanent use remains the agreed direction after evaluation.
   Give each server independent identities and deliberately selected services.
7. If retaining the clone temporarily, persistently isolate copied workloads before
   further online boot; plan application-specific consistency/recovery checks.
8. Preserve Seagate images, Google Drive copy and the MEMOREX recovery kit.
9. Recurring backup scheduling, retention, monitoring/outage email setup, OAuth
   secret rotation and long-term OAuth publishing review remain separate work.

No changes were made to the original server's production services as part of
these assessment scripts. No production cutover was attempted.
