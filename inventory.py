#!/usr/bin/env python3
"""Read-only recovery inventory. Outputs metadata, never file contents."""
import datetime
import json
import os
from pathlib import Path
import subprocess


def command(argv):
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=120)
        return {"exit_code": result.returncode, "output": result.stdout.strip(),
                "error": result.stderr.strip()}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"error": str(error)}


def measure(path):
    entry = {"path": str(path)}
    try:
        metadata = path.stat()
        entry.update(uid=metadata.st_uid, gid=metadata.st_gid,
                     mode=oct(metadata.st_mode & 0o7777))
        # Do not cross filesystems or dereference symlinks.
        entry["disk_usage"] = command(["du", "-sx", "--block-size=1", "--", str(path)])
    except OSError as error:
        entry["error"] = str(error)
    return entry


paths = [Path(p) for p in (
    "/etc", "/root", "/usr/local", "/opt", "/srv", "/var/lib",
    "/var/mail", "/var/spool/mail", "/var/spool/postfix",
    "/home/mediaspacedev/media-storage",
    "/home/mediaspacedev/deployments/mediaspace/shared/data",
    "/home/mediaspacedev/projects/sturdy-journey",
    "/home/mediaspacedev/.config/mediaspace", "/var/lib/jellyfin", "/etc/jellyfin",
)]
try:
    paths.extend(sorted(Path("/home").iterdir()))
except OSError:
    pass
report = {
    "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "effective_uid": os.geteuid(),
    "notes": ["Overlapping paths must not be summed.",
              "Sizes include caches and excluded media; they are not a cloud estimate.",
              "Missing or inaccessible sources require review.",
              "This is an inventory, not a backup."],
    "paths": [measure(path) for path in paths],
    "commands": {},
}
for name, argv in {
    "os": ["lsb_release", "-ds"],
    "disks": ["lsblk", "-J", "-o", "NAME,SIZE,FSTYPE,UUID,MOUNTPOINTS"],
    "mounts": ["findmnt", "--json", "--real"],
    "space": ["df", "-h"],
    "packages": ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\n"],
    "manual_packages": ["apt-mark", "showmanual"],
    "services": ["systemctl", "list-units", "--type=service", "--all", "--no-pager", "--plain"],
    "unit_files": ["systemctl", "list-unit-files", "--no-pager"],
    "timers": ["systemctl", "list-timers", "--all", "--no-pager"],
    "accounts": ["getent", "passwd"],
    "groups": ["getent", "group"],
}.items():
    report["commands"][name] = command(argv)
print(json.dumps(report, indent=2))
