#!/bin/bash
# DWPose polling — vérifie toutes les 3 minutes si le rig est terminé
# Lance en background: nohup bash dwpose_poll.sh &

START=$(date +%s)
MAX_WAIT=900  # 15 minutes
POLL_INTERVAL=180  # 3 minutes
LOG=/home/ubuntu/eya_pipeline/dwpose_poll.log
RESULT_FLAG=/home/ubuntu/eya_pipeline/dwpose_done.flag

echo "[$(date)] DWPose polling started" | tee -a $LOG

while true; do
  NOW=$(date +%s)
  ELAPSED=$((NOW - START))
  
  if [ $ELAPSED -ge $MAX_WAIT ]; then
    echo "[$(date)] TIMEOUT after ${ELAPSED}s — DWPose did not complete" | tee -a $LOG
    break
  fi
  
  # Check if new .stretch file appeared in Downloads (newer than start)
  LATEST=$(ls -t /home/ubuntu/Downloads/*.stretch 2>/dev/null | head -1)
  if [ -n "$LATEST" ]; then
    FILE_TIME=$(stat -c %Y "$LATEST" 2>/dev/null)
    if [ "$FILE_TIME" -gt "$START" ]; then
      echo "[$(date)] DONE — New .stretch file detected: $LATEST" | tee -a $LOG
      cp "$LATEST" /home/ubuntu/eya_pipeline/output/eya_dwpose.stretch
      touch $RESULT_FLAG
      echo "DWPose .stretch saved to output/" | tee -a $LOG
      break
    fi
  fi
  
  echo "[$(date)] Still building... (${ELAPSED}s elapsed)" | tee -a $LOG
  sleep $POLL_INTERVAL
done
