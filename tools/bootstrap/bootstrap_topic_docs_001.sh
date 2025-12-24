#!/usr/bin/env bash
set -euo pipefail

# Create a full "001" doc-set for a topic:
# - notebooks/<KIND>_<NNN>_<LANG>.ipynb
# - tex/<KIND>_<NNN>_<LANG>.tpl.tex
#
# Usage:
#   tools/bootstrap/bootstrap_topic_docs_001.sh topics/TOP_0001_exoplanet_birth_radius
#
# Notes:
# - Uses global preambles: core/tex/preamble_ru.tex and core/tex/preamble_en.tex
# - Templates include: \input{../_tmp/<KIND>_<NNN>_<LANG>_body.tex}

TOPIC_DIR="${1:-}"
if [[ -z "${TOPIC_DIR}" ]]; then
  echo "ERROR: Provide topic directory."
  echo "Example: tools/bootstrap/bootstrap_topic_docs_001.sh topics/TOP_0001_exoplanet_birth_radius"
  exit 1
fi

if [[ ! -d "${TOPIC_DIR}" ]]; then
  echo "ERROR: Topic dir not found: ${TOPIC_DIR}"
  exit 1
fi

NOTEBOOKS_DIR="${TOPIC_DIR}/notebooks"
TEX_DIR="${TOPIC_DIR}/tex"
TMP_DIR="${TEX_DIR}/_tmp"
BUILD_DIR="${TOPIC_DIR}/build"

mkdir -p "${NOTEBOOKS_DIR}" "${TEX_DIR}" "${TMP_DIR}" "${BUILD_DIR}"

KINDS=(
  "ACA"
  "ACAP"
  "AZ"
  "AA"
  "CHR"
  "MIN"
  "TERM"
  "NOTE"
  "TOP"
  "MISC"
)

create_ipynb () {
  local out="$1"
  local title="$2"
  cat > "${out}" <<EOF
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# ${title}\\n",
        "\\n",
        "_Draft._\\n"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
EOF
}

create_tpl () {
  local out="$1"
  local lang="$2"
  local kind="$3"
  local num="$4"
  local title="$5"

  local preamble
  if [[ "${lang}" == "RU" ]]; then
    preamble="\\input{../../../core/tex/preamble_ru.tex}"
  else
    preamble="\\input{../../../core/tex/preamble_en.tex}"
  fi

  cat > "${out}" <<EOF
\\documentclass[11pt]{article}

% Global preamble (single source of truth)
${preamble}

\\title{${title}}
\\author{Attractor Lab}
\\date{\\today}

\\begin{document}
\\maketitle

% Auto-generated body from notebooks (do not edit by hand)
\\input{../_tmp/${kind}_${num}_${lang}_body.tex}

\\end{document}
EOF
}

for kind in "${KINDS[@]}"; do
  if [[ "${kind}" == "TOP" ]]; then
    num="000"
  else
    num="001"
  fi

  for lang in RU EN; do
    ipynb="${NOTEBOOKS_DIR}/${kind}_${num}_${lang}.ipynb"
    tpl="${TEX_DIR}/${kind}_${num}_${lang}.tpl.tex"

    if [[ ! -f "${ipynb}" ]]; then
      create_ipynb "${ipynb}" "${kind} ${num} (${lang})"
      echo "Created: ${ipynb}"
    else
      echo "Skip (exists): ${ipynb}"
    fi

    if [[ ! -f "${tpl}" ]]; then
      create_tpl "${tpl}" "${lang}" "${kind}" "${num}" "${kind} ${num} (${lang})"
      echo "Created: ${tpl}"
    else
      echo "Skip (exists): ${tpl}"
    fi
  done
done

echo "OK: bootstrap completed for ${TOPIC_DIR}"