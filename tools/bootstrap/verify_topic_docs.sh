#!/usr/bin/env bash
set -euo pipefail

# Verifies: for each notebooks/<KIND>_<NNN>_<LANG>.ipynb there is tex/<KIND>_<NNN>_<LANG>.tpl.tex
#
# Usage:
#   tools/bootstrap/verify_topic_docs.sh topics/TOP_0001_exoplanet_birth_radius

TOPIC_DIR="${1:-}"
if [[ -z "${TOPIC_DIR}" ]]; then
  echo "ERROR: Provide topic directory."
  echo "Example: tools/bootstrap/verify_topic_docs.sh topics/TOP_0001_exoplanet_birth_radius"
  exit 1
fi

NOTEBOOKS_DIR="${TOPIC_DIR}/notebooks"
TEX_DIR="${TOPIC_DIR}/tex"

if [[ ! -d "${NOTEBOOKS_DIR}" ]]; then
  echo "ERROR: Missing notebooks dir: ${NOTEBOOKS_DIR}"
  exit 1
fi
if [[ ! -d "${TEX_DIR}" ]]; then
  echo "ERROR: Missing tex dir: ${TEX_DIR}"
  exit 1
fi

missing=0

while IFS= read -r nb; do
  base="$(basename "${nb}" .ipynb)"
  tpl="${TEX_DIR}/${base}.tpl.tex"
  if [[ ! -f "${tpl}" ]]; then
    echo "MISSING tpl: ${tpl}  (for ${nb})"
    missing=$((missing+1))
  fi
done < <(find "${NOTEBOOKS_DIR}" -maxdepth 1 -type f -name "*.ipynb" | sort)

if [[ "${missing}" -eq 0 ]]; then
  echo "OK: all notebooks have matching templates."
else
  echo "FAIL: ${missing} template(s) missing."
  exit 2
fi