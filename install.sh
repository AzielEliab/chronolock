#!/usr/bin/env bash
# ChronoLock one-click install. Counted download via this project's Worker.
# Usage: curl -fsSL https://chronolock-download-tracker.vibelock.workers.dev/install.sh | bash
set -euo pipefail

HOST="${CHRONOLOCK_HOME_HOST:-https://chronolock-download-tracker.vibelock.workers.dev}"
ASSET="${CHRONOLOCK_HOME_ASSET:-chronolock-0.1.0.tar.gz}"
WORKDIR="${CHRONOLOCK_HOME:-$HOME/chronolock}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "Downloading counted tarball from ${HOST}/download (User-Agent Mozilla/5.0)…"
curl -fsSL -A 'Mozilla/5.0' "${HOST}/download?asset=${ASSET}" -o "${ASSET}"

tar -xzf "${ASSET}"
DIR="$(find . -maxdepth 1 -type d -name 'chronolock-*' | head -n 1)"
if [ -n "${DIR}" ]; then
  cd "${DIR}"
fi

python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

echo
echo "Installed ChronoLock."
echo "Run:  chronolock ui"
echo "Then open http://127.0.0.1:8851  (loopback only)"
echo "Author: Aziel Eliab."
