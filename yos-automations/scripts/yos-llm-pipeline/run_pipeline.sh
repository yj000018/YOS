#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# LLM Distillation Pipeline Runner
# Called by yOS scheduler (cron or Manus schedule)
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/pipeline.log"
PYTHON="python3.11"

echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Pipeline run started" >> "$LOG_FILE"

cd "$SCRIPT_DIR"

# Load environment if .env exists
if [ -f "${SCRIPT_DIR}/.env" ]; then
    export $(grep -v '^#' "${SCRIPT_DIR}/.env" | xargs)
fi

# Run pipeline
$PYTHON llm_distillation_pipeline.py "$@" 2>&1 | tee -a "$LOG_FILE"

echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Pipeline run finished" >> "$LOG_FILE"
