# Sanitized source map

The two preflight runs examined these component categories:

| Category | Purpose |
| --- | --- |
| Mail service entrypoint | Starts the existing mailbox application. |
| Inbound polling | Schedules retrieval of new inbound items. |
| Inbound fetch and acknowledgement | Retrieves originals and records processing state. |
| Inbound edge handler | Receives upstream inbound events and coordinates delivery. |
| Service configuration and runtime state | Identifies configured writers and state that a backup plan must account for. |
| Backup destination metadata | Checks whether an existing encrypted destination can be identified and listed. |

The original mapper and code snapshots are not included. They contain private
path mappings and deployment-specific metadata. This file is a summary, not a
reproducible source-to-runtime manifest; no source hashes or host paths are
published.
