---
type: protocol
domain: Y-OS
tags: [backup, resilience, protocol]
---
# Backup Protocol
3-2-1 backup strategy: 3 copies, 2 media, 1 offsite.
- Local: [[ARC Local Server]] + [[CasaTAO Studio]] NAS
- Cloud: [[GitHub Repo Y-WORLD]] + encrypted S3
- Tested monthly via [[n8n Cognitive Automation]] automated restore drill.
