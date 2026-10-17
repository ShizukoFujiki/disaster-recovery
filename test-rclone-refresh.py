#!/usr/bin/env python3
import configparser
import datetime
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    if os.geteuid() != 0:
        print("Run this script with sudo.")
        return 1
    path = Path("/home/auroraixion/.config/rclone/rclone.conf")
    try:
        config = configparser.RawConfigParser()
        with path.open() as source:
            config.read_file(source)
        token = json.loads(config["gdrive"]["token"])
        if not token.get("refresh_token"):
            print("No refresh token is configured. Google authorization must be reconnected.")
            return 1
        token["expiry"] = "2000-01-01T00:00:00Z"
        config["gdrive"]["token"] = json.dumps(token)
        output = io.StringIO()
        config.write(output)
        stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
        backup = path.with_name(path.name + ".before-refresh-test-" + stamp)
        shutil.copy2(path, backup)
        os.chmod(backup, 0o600)
        with path.open("w") as destination:
            destination.write(output.getvalue())
        print("Configuration backed up. Testing Google token refresh...", flush=True)
        result = subprocess.run(
            ["rclone", "--config", str(path), "about", "gdrive:",
             "--contimeout", "15s", "--timeout", "30s", "--retries", "1"],
            timeout=120,
        )
        if result.returncode == 0:
            print("SUCCESS: Google token refresh worked. No backup upload was started.")
        else:
            print("FAILED: Token refresh did not succeed. Do not restart the upload yet.")
            print("Configuration backup: " + str(backup))
        return result.returncode
    except subprocess.TimeoutExpired:
        print("The refresh test timed out. No backup upload was started.")
        return 1
    except Exception as error:
        print("Stopped safely; error type: " + type(error).__name__)
        print("Do not paste configuration contents or credentials into chat.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
