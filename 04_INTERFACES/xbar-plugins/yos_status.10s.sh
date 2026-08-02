#!/bin/bash
# <xbar.title>Y-OS Mac Lock</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Manus / Y-OS</xbar.author>
# <xbar.desc>Shows active Y-OS processes requiring the Mac. Detects zombie locks.</xbar.desc>
# <xbar.refreshTime>10s</xbar.refreshTime>

LOCK_FILE="/tmp/yos_mac_lock.json"
LOCK_DIR="/tmp/yos_locks"

# --- Helper: check if a PID is alive ---
pid_alive() {
  kill -0 "$1" 2>/dev/null && echo "true" || echo "false"
}

# --- Collect all active locks ---
active=()
stale=()

# Single lock file (legacy)
if [ -f "$LOCK_FILE" ]; then
  pid=$(python3 -c "import json,sys; d=json.load(open('$LOCK_FILE')); print(d.get('pid',''))" 2>/dev/null)
  task=$(python3 -c "import json,sys; d=json.load(open('$LOCK_FILE')); print(d.get('task','Unknown task'))" 2>/dev/null)
  started=$(python3 -c "import json,sys; d=json.load(open('$LOCK_FILE')); print(d.get('started_at','?'))" 2>/dev/null)
  node=$(python3 -c "import json,sys; d=json.load(open('$LOCK_FILE')); print(d.get('node','Mac'))" 2>/dev/null)
  if [ -n "$pid" ] && [ "$(pid_alive $pid)" = "true" ]; then
    active+=("$task|$pid|$started|$node")
  elif [ -f "$LOCK_FILE" ]; then
    stale+=("$task|$pid|$started|STALE")
  fi
fi

# Multi-lock directory
if [ -d "$LOCK_DIR" ]; then
  for f in "$LOCK_DIR"/*.json; do
    [ -f "$f" ] || continue
    pid=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('pid',''))" 2>/dev/null)
    task=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('task','Unknown task'))" 2>/dev/null)
    started=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('started_at','?'))" 2>/dev/null)
    node=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('node','Mac'))" 2>/dev/null)
    if [ -n "$pid" ] && [ "$(pid_alive $pid)" = "true" ]; then
      active+=("$task|$pid|$started|$node")
    else
      stale+=("$task|$pid|$started|STALE")
    fi
  done
fi

# --- Render menu bar title ---
n_active=${#active[@]}
n_stale=${#stale[@]}

if [ $n_active -gt 0 ] && [ $n_stale -gt 0 ]; then
  echo "🔒 Y-OS ($n_active actif, ⚠️$n_stale zombie)"
elif [ $n_active -gt 0 ]; then
  echo "🔒 Y-OS ($n_active actif)"
elif [ $n_stale -gt 0 ]; then
  echo "⚠️ Y-OS ($n_stale zombie)"
else
  echo "⚫ Y-OS"
fi

echo "---"

# --- Active processes ---
if [ $n_active -gt 0 ]; then
  echo "🟢 PROCESSUS ACTIFS — Ne pas fermer le Mac"
  for entry in "${active[@]}"; do
    IFS='|' read -r task pid started node <<< "$entry"
    echo "  ▸ $task"
    echo "  --PID: $pid | Démarré: $started | Nœud: $node"
  done
  echo "---"
fi

# --- Stale/zombie locks ---
if [ $n_stale -gt 0 ]; then
  echo "⚠️ LOCKS ZOMBIES (processus mort, lock non nettoyé)"
  for entry in "${stale[@]}"; do
    IFS='|' read -r task pid started node <<< "$entry"
    echo "  ✗ $task (PID $pid — mort)"
    echo "  --Démarré: $started"
  done
  echo "  Nettoyer | bash='rm -f $LOCK_FILE $LOCK_DIR/*.json' terminal=false refresh=true"
  echo "---"
fi

# --- No activity ---
if [ $n_active -eq 0 ] && [ $n_stale -eq 0 ]; then
  echo "Aucun processus Y-OS actif"
  echo "Le Mac peut être fermé sans risque."
  echo "---"
fi

# --- Footer ---
echo "Y-OS Mac Lock v1.0"
echo "Lock file: $LOCK_FILE"
echo "Rafraîchi toutes les 10s | refresh=true"
