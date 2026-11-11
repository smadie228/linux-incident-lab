#!/usr/bin/env bash
# Read-only учебная диагностика без sudo
set -u
PORT="${1:-8080}"
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || (( PORT < 1 || PORT > 65535 )); then
  echo "Использование: bash diagnose.sh 8080" >&2
  exit 1
fi
echo "=== Linux Incident Lab ==="
date -Is
uname -sr
echo
echo "1) HTTP"
if command -v curl >/dev/null 2>&1; then
  curl --silent --show-error --output /dev/null \
    --write-out "HTTP %{http_code}; time %{time_total}s\n" \
    --max-time 2 "http://127.0.0.1:$PORT/health"
  echo "curl exit code: $?"
else
  echo "curl не установлен"
fi
echo
echo "2) TCP listeners"
if command -v ss >/dev/null 2>&1; then ss -lnt; fi
echo
echo "3) Memory"
if command -v free >/dev/null 2>&1; then free -h; fi
echo
echo "4) Disk"
if command -v df >/dev/null 2>&1; then df -h .; fi
echo
echo "Сравни результаты с учебным инцидентом в docs/."
