#!/bin/bash
# Y-OS ChatGPT Cookie Refresh Pipeline
# Version: 1.0 (2026-07-30)
# Stored: /home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh (CC — persistent)
#
# PIPELINE:
#   1. SSH to Mac → copy extractor script → launch via Terminal GUI (Keychain access)
#   2. Wait for extraction → transfer cookies JSON to CC
#   3. Run ChatGPT ingestion → update master_ledger.csv
#
# USAGE (from CC or Manus sandbox via SSH):
#   bash /home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh
#   bash /home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh --full   # full rebuild
#   bash /home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh --dry    # dry run only
#
# PREREQUISITES:
#   - bore tunnel active on Mac (port 22847) — check: nc -zv bore.pub 22847
#   - SSH key: ~/.ssh/manus_mac (or password fallback: 4 spaces)
#   - pycryptodome installed on Mac: pip3 install pycryptodome
#   - Chrome open on Mac with chatgpt.com session active

set -e

MAC_HOST="bore.pub"
MAC_PORT="22847"
MAC_USER="yannickjolliet"
MAC_SSH_KEY="$HOME/.ssh/manus_mac"
MAC_EXTRACTOR="/tmp/yos_extract_cookies.py"
MAC_OUTPUT="/Users/yannickjolliet/chatgpt_cookies_fresh.json"
CC_COOKIES="$HOME/yos/ledger/chatgpt_cookies_fresh.json"
CC_LEDGER_SCRIPT="$HOME/yos/ledger/ingest_chatgpt_cookies.py"
CC_EXTRACTOR="$HOME/yos/tools/extract_mac_chrome_cookies.py"

MODE="${1:-}"

echo "═══════════════════════════════════════════"
echo " Y-OS ChatGPT Cookie Refresh Pipeline"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════"

# ── Step 1: Check bore tunnel ──────────────────
echo "[1/4] Checking Mac SSH tunnel..."
if ! nc -zv -w 5 "$MAC_HOST" "$MAC_PORT" 2>/dev/null; then
    echo "ERROR: bore tunnel not reachable at $MAC_HOST:$MAC_PORT"
    echo "→ Start bore on Mac: bore local 22 --to bore.pub"
    exit 1
fi
echo "  ✓ Tunnel active"

# ── Step 2: Copy extractor to Mac + launch via Terminal GUI ──
echo "[2/4] Deploying extractor to Mac..."
scp -i "$MAC_SSH_KEY" -o StrictHostKeyChecking=no -P "$MAC_PORT" \
    "$CC_EXTRACTOR" "$MAC_USER@$MAC_HOST:$MAC_EXTRACTOR" 2>/dev/null || \
    cat "$CC_EXTRACTOR" | ssh -i "$MAC_SSH_KEY" -o StrictHostKeyChecking=no -p "$MAC_PORT" \
    "$MAC_USER@$MAC_HOST" "cat > $MAC_EXTRACTOR"
echo "  ✓ Extractor deployed"

echo "[3/4] Launching extraction via Terminal GUI (Keychain access)..."
ssh -i "$MAC_SSH_KEY" -o StrictHostKeyChecking=no -p "$MAC_PORT" "$MAC_USER@$MAC_HOST" \
    "rm -f /tmp/yos_extract_out.txt; \
     osascript -e 'tell application \"Terminal\" to do script \
     \"python3 $MAC_EXTRACTOR > /tmp/yos_extract_out.txt 2>&1; echo DONE >> /tmp/yos_extract_out.txt\"'"

# Wait for extraction (max 30s)
echo "  Waiting for extraction..."
for i in $(seq 1 30); do
    sleep 1
    DONE=$(ssh -i "$MAC_SSH_KEY" -o StrictHostKeyChecking=no -p "$MAC_PORT" "$MAC_USER@$MAC_HOST" \
        "grep -c DONE /tmp/yos_extract_out.txt 2>/dev/null || echo 0")
    if [ "$DONE" -gt 0 ]; then
        echo "  ✓ Extraction complete (${i}s)"
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "ERROR: Extraction timed out. Output:"
        ssh -i "$MAC_SSH_KEY" -o StrictHostKeyChecking=no -p "$MAC_PORT" "$MAC_USER@$MAC_HOST" \
            "cat /tmp/yos_extract_out.txt"
        exit 1
    fi
done

# Transfer cookies to CC
ssh -i "$MAC_SSH_KEY" -o StrictHostKeyChecking=no -p "$MAC_PORT" "$MAC_USER@$MAC_HOST" \
    "cat $MAC_OUTPUT" > "$CC_COOKIES"
COOKIE_SIZE=$(wc -c < "$CC_COOKIES")
echo "  ✓ Cookies transferred (${COOKIE_SIZE} bytes)"

# ── Step 4: Run ingestion ──────────────────────
echo "[4/4] Running ChatGPT ingestion..."
cd "$HOME/yos/ledger"

if [ "$MODE" = "--dry" ]; then
    python3 "$CC_LEDGER_SCRIPT" --cookies "$CC_COOKIES" --dry-run
elif [ "$MODE" = "--full" ]; then
    python3 "$CC_LEDGER_SCRIPT" --cookies "$CC_COOKIES" --full
else
    python3 "$CC_LEDGER_SCRIPT" --cookies "$CC_COOKIES"
fi

echo ""
echo "═══════════════════════════════════════════"
echo " Pipeline complete ✓"
echo "═══════════════════════════════════════════"
