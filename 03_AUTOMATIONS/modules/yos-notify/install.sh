#!/bin/bash
# yOS-Notify Installer
# Installs the module globally and creates the CLI command

set -e

YOS_DIR="${HOME}/.yos"
MODULE_DIR="${YOS_DIR}/modules/yos_notify"
BIN_DIR="${HOME}/.local/bin"

echo "=== Installing yOS-Notify ==="

# Create directories
mkdir -p "$MODULE_DIR" "$BIN_DIR" "${YOS_DIR}/config"

# Copy module
cp "$(dirname "$0")/yos_notify.py" "$MODULE_DIR/"

# Create __init__.py for Python import
cat > "$MODULE_DIR/__init__.py" << 'EOF'
from .yos_notify import notify, send_pushover, send_telegram, load_config, save_config
__all__ = ["notify", "send_pushover", "send_telegram", "load_config", "save_config"]
EOF

# Create CLI executable
cat > "$BIN_DIR/yos-notify" << EOF
#!/usr/bin/env python3
import sys
sys.path.insert(0, '${YOS_DIR}/modules')
from yos_notify.yos_notify import main
main()
EOF
chmod +x "$BIN_DIR/yos-notify"

# Install requests if needed
python3 -c "import requests" 2>/dev/null || pip3 install requests -q

echo ""
echo "✅ yOS-Notify installed:"
echo "   CLI:    yos-notify 'Title' 'Message' [--channel pushover|telegram|both] [--device ios|macos|android|n100|all]"
echo "   Python: from yos_notify.yos_notify import notify"
echo ""
echo "Next step: configure credentials"
echo "   yos-notify --setup"
echo ""
echo "Or set environment variables:"
echo "   export PUSHOVER_APP_TOKEN=..."
echo "   export PUSHOVER_USER_KEY=..."
echo "   export TELEGRAM_BOT_TOKEN=..."
echo "   export TELEGRAM_CHAT_ID=..."
