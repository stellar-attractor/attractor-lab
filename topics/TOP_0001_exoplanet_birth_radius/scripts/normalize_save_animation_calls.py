#!/usr/bin/env python3
"""
Normalize save_animation() calls in selected ANIM notebooks.

Goal:
- Use ONE style everywhere:
    save_animation(<anim_obj>, anim_base("<NOTEBOOK>_<slug>"))
  where anim_base() already prefixes NOTEBOOK in bootstrap:
    ANIM_DIR / f"{NOTEBOOK}_{slug(name)}"

So here we pass ONLY the "name" part (without NOTEBOOK prefix),
and anim_base() will add NOTEBOOK automatically.

This script:
- Finds save_animation(anim, <path-expr>)
- Extracts a stable "name" from common patterns:
    1) ANIM_DIR / "SOME_NAME"
    2) ANIM_DIR / f"..."
    3) anim_outpath("SOME_NAME", ext=...) or anim_outpath(...).with_suffix("")
    4) out = anim_outpath("SOME_NAME", ...); save_animation(anim, out)
- Rewrites into:
    save_animation(anim, anim_base("SOME_NAME"))
- Keeps everything else unchanged.

Usage:
  python normalize_save_animation_calls.py /path/to/ANIM_001_EN.ipynb /path/to/ANIM_002_EN.ipynb /path/to/ANIM_003_EN.ipynb
"""

from __future__ import annotations

import re
import sys
import shutil
from pathlib import Path

import nbformat


# ----------------------------
# Helpers
# ----------------------------
RE_SAVE = re.compile(
    r"""
    save_animation
    \(
        \s*(?P<anim>[^,]+?)\s*,          # 1st arg: animation object expr
        \s*(?P<path>[^)]+?)\s*           # 2nd arg: path expr (until ')')
    \)
    """,
    re.VERBOSE,
)

RE_ANIMDIR_STR = re.compile(
    r"""ANIM_DIR\s*/\s*["'](?P<name>[^"']+)["']"""
)

RE_ANIMDIR_FSTR = re.compile(
    r"""ANIM_DIR\s*/\s*f["'](?P<fstr>[^"']+)["']"""
)

RE_ANIM_OUTPATH = re.compile(
    r"""anim_outpath\s*\(\s*["'](?P<name>[^"']+)["'](?:\s*,[^)]*)?\)"""
)

RE_WITH_SUFFIX_EMPTY = re.compile(
    r"""\.with_suffix\(\s*["']\s*["']\s*\)\s*$"""
)

# out = anim_outpath("X", ...); save_animation(anim, out)
RE_ASSIGN_OUT = re.compile(
    r"""^\s*(?P<var>[A-Za-z_]\w*)\s*=\s*(?P<rhs>.+?)\s*$"""
)


def extract_name_from_path_expr(path_expr: str) -> str | None:
    """
    Try to infer the intended base name from the second argument.
    Returns None if we cannot infer safely.
    """
    s = path_expr.strip()

    # Case: anim_outpath("NAME", ...) or anim_outpath("NAME", ...).with_suffix("")
    m = RE_ANIM_OUTPATH.search(s)
    if m:
        return m.group("name")

    # Case: (anim_outpath("NAME", ...).with_suffix(""))
    # (We already catch anim_outpath above; the suffix wrapper is fine.)
    # Case: ANIM_DIR / "NAME"
    m = RE_ANIMDIR_STR.search(s)
    if m:
        return m.group("name")

    # Case: ANIM_DIR / f"..."
    # We CANNOT safely evaluate f-strings; but we can preserve as literal template.
    m = RE_ANIMDIR_FSTR.search(s)
    if m:
        # Keep original f-string body as "raw" name.
        # Example: f"{NOTEBOOK}_migration_{MODE}" -> "{NOTEBOOK}_migration_{MODE}"
        # But we DO NOT want NOTEBOOK here. We'll strip leading "{NOTEBOOK}_" if present.
        body = m.group("fstr")
        body = re.sub(r"^\{NOTEBOOK\}_", "", body)
        return body

    # Case: Path(...) or something else - skip
    return None


def rewrite_save_call(line: str) -> str:
    """
    Rewrite a single line if it contains save_animation(...).
    Otherwise return unchanged.
    """
    m = RE_SAVE.search(line)
    if not m:
        return line

    anim_expr = m.group("anim").strip()
    path_expr = m.group("path").strip()

    name = extract_name_from_path_expr(path_expr)
    if not name:
        # If cannot infer, leave it unchanged
        return line

    # Strip leading NOTEBOOK prefix if user already included it in the name
    name = re.sub(r"^\{?NOTEBOOK\}?_+", "", name)
    name = re.sub(r"^ANIM_[0-9A-Z]+_+", "", name) if name.startswith("ANIM_") else name  # keep conservative

    new_call = f'save_animation({anim_expr}, anim_base("{name}"))'
    return RE_SAVE.sub(new_call, line, count=1)


def normalize_cell_source(source: str) -> str:
    """
    Normalize all save_animation(...) occurrences inside a cell source.
    Also supports pattern:
        out = anim_outpath("NAME", ext="mp4")
        save_animation(anim, out)
    by leaving the out assignment, but rewriting the call using the same NAME.
    """
    lines = source.splitlines()

    # First pass: collect simple `var = anim_outpath("NAME"... )` bindings per cell
    var_to_name: dict[str, str] = {}
    for ln in lines:
        m = RE_ASSIGN_OUT.match(ln)
        if not m:
            continue
        var = m.group("var")
        rhs = m.group("rhs").strip()
        mm = RE_ANIM_OUTPATH.search(rhs)
        if mm:
            var_to_name[var] = mm.group("name")

    # Second pass: rewrite save_animation calls line-by-line
    out_lines: list[str] = []
    for ln in lines:
        m = RE_SAVE.search(ln)
        if not m:
            out_lines.append(ln)
            continue

        anim_expr = m.group("anim").strip()
        path_expr = m.group("path").strip()

        # If second arg is a known var that maps to an anim_outpath() earlier in the cell
        if path_expr in var_to_name:
            name = var_to_name[path_expr]
            name = re.sub(r"^\{?NOTEBOOK\}?_+", "", name)
            new_call = f'save_animation({anim_expr}, anim_base("{name}"))'
            out_lines.append(RE_SAVE.sub(new_call, ln, count=1))
            continue

        # Otherwise use generic extraction
        out_lines.append(rewrite_save_call(ln))

    return "\n".join(out_lines) + ("\n" if source.endswith("\n") else "")


def process_notebook(path: Path, *, make_backup: bool = True) -> None:
    nb = nbformat.read(path, as_version=4)
    changed = False

    for cell in nb.cells:
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        if "save_animation" not in src:
            continue

        new_src = normalize_cell_source(src)
        if new_src != src:
            cell["source"] = new_src
            changed = True

    if not changed:
        print(f"[SKIP] {path.name}: no changes needed")
        return

    if make_backup:
        bak = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, bak)
        print(f"[BACKUP] {bak.name}")

    nbformat.write(nb, path)
    print(f"[OK] {path.name}: rewritten")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Pass one or more .ipynb paths.")
        return 2

    for p in argv[1:]:
        path = Path(p).expanduser().resolve()
        if not path.exists() or path.suffix != ".ipynb":
            print(f"[ERR] Not an ipynb: {path}")
            continue
        process_notebook(path, make_backup=True)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))