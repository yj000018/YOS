# yOS-Notify

## Description
Universal push notification module for the yOS ecosystem. It allows Manus, scripts, and apps to send instant push notifications to Yannick's devices (iOS, macOS, Android, Ubuntu/N100) via Pushover (native push) and Telegram.

## Capabilities
- **Dual-channel delivery**: Send to Pushover, Telegram, or both simultaneously.
- **Device targeting**: Target specific devices (e.g., only iPhone, only Mac) via Pushover.
- **Priority management**: Support for silent, normal, high, and emergency priority levels.
- **Sound customization**: Trigger specific notification sounds on iOS/macOS.

## Usage — CLI
The module is installed globally at `/home/ubuntu/.local/bin/yos-notify`.

```bash
# Basic usage (uses default channel)
yos-notify "Pipeline Done" "DWPose completed successfully"

# Specify channel
yos-notify "Alert" "Disk full" --channel pushover
yos-notify "Info" "Server started" --channel telegram
yos-notify "Critical" "System down" --channel both

# Target specific device (Pushover only)
yos-notify "Mac Alert" "Build failed" --channel pushover --device macos
```

## Usage — Python
```python
import sys
import os
sys.path.insert(0, os.path.expanduser("~/.yos/modules"))
from yos_notify import notify

# Send notification
notify(
    title="yOS Update",
    message="New module installed",
    channel="pushover",  # 'pushover', 'telegram', 'both', or None for default
    device="ios",        # 'all', 'ios', 'macos', 'android', 'n100'
    priority=1           # -2 (silent) to 2 (emergency)
)
```

## Configuration
Configuration is stored in `~/.yos/config/notify.json`.
Tokens can also be provided via environment variables:
- `PUSHOVER_APP_TOKEN`
- `PUSHOVER_USER_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

To reconfigure interactively:
```bash
yos-notify --setup
```

## Best Practices
1. **Long-running tasks**: Always use `yos-notify` at the end of long-running tasks (e.g., video rendering, DWPose rigging, large downloads) so the user doesn't have to wait and watch the terminal.
2. **Errors**: Send high-priority notifications for critical failures in automated pipelines.
3. **Channel selection**: Use `pushover` for high-signal alerts (native OS integration). Use `telegram` for logs, status updates, or lower-priority information.
