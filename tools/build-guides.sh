#!/usr/bin/env bash
set -euo pipefail
support_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
guide_python="${GUIDES_PYTHON:-python3}"
guide_venv="$support_root/.venv-guides"
if [[ ! -x "$guide_venv/bin/python" ]]; then
  "$guide_python" -m venv "$guide_venv"
fi
"$guide_venv/bin/python" -m pip install --disable-pip-version-check -r "$support_root/tools/requirements.txt"
"$guide_venv/bin/python" "$support_root/tools/build_guides.py" "$@"
