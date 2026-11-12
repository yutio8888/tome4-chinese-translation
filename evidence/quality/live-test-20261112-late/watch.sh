#!/bin/bash
# Host-side read-only observer; not a hard limit. Wakes host if any session >= WARN_MB image b64, or all reports exist, or timeout.
WARN_MB=${WARN_MB:-15}; MAX_S=${MAX_S:-7000}; T=$HOME/tome-live/testers; D=$(dirname $0); end=$((SECONDS+MAX_S))
while [ $SECONDS -lt $end ]; do
  out=$(python3 $D/stats.py); n=0
  for k in ${ACTIVE:-d6a2 d6b2}; do [ -s $T/$k/REPORT.md ] && n=$((n+1)); done
  hit=$(echo "$out" | awk -v w=$WARN_MB '{for(i=1;i<=NF;i++) if($i ~ /^image_b64_MB=/){split($i,a,"="); if(a[2]+0>=w) print $1}}')
  if [ -n "$hit" ] || [ $n -eq $(echo ${ACTIVE:-d6a2 d6b2} | wc -w) ]; then echo "TRIGGER warn=[$hit] reports=$n"; echo "$out"; exit 0; fi
  sleep 60
done
echo "TIMEOUT"; python3 $D/stats.py
