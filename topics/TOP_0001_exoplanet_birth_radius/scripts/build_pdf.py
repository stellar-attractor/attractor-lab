#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

# --- logging additions (only what's needed) ---
from datetime import datetime
import traceback

TOPIC_DIR = Path(__file__).resolve().parents[1]
TEX_DIR = TOPIC_DIR / "tex"
BUILD_DIR = TOPIC_DIR / "build"

# -----------------------------------------------------------------------------
# Unicode -> LaTeX sanitizers (pdflatex compatibility)
# -----------------------------------------------------------------------------

# Greek letters: unicode -> math macros
GREEK_UNICODE_TO_LATEX = {
    "α": r"$\alpha$",
    "β": r"$\beta$",
    "γ": r"$\gamma$",
    "δ": r"$\delta$",
    "ε": r"$\epsilon$",
    "ζ": r"$\zeta$",
    "η": r"$\eta$",
    "θ": r"$\theta$",
    "ι": r"$\iota$",
    "κ": r"$\kappa$",
    "λ": r"$\lambda$",
    "μ": r"$\mu$",
    "ν": r"$\nu$",
    "ξ": r"$\xi$",
    "ο": r"$o$",  # omicron as latin o
    "π": r"$\pi$",
    "ρ": r"$\rho$",
    "σ": r"$\sigma$",
    "τ": r"$\tau$",
    "υ": r"$\upsilon$",
    "φ": r"$\phi$",
    "χ": r"$\chi$",
    "ψ": r"$\psi$",
    "ω": r"$\omega$",
    "Α": r"$A$",
    "Β": r"$B$",
    "Γ": r"$\Gamma$",
    "Δ": r"$\Delta$",
    "Ε": r"$E$",
    "Ζ": r"$Z$",
    "Η": r"$H$",
    "Θ": r"$\Theta$",
    "Ι": r"$I$",
    "Κ": r"$K$",
    "Λ": r"$\Lambda$",
    "Μ": r"$M$",
    "Ν": r"$N$",
    "Ξ": r"$\Xi$",
    "Ο": r"$O$",
    "Π": r"$\Pi$",
    "Ρ": r"$P$",
    "Σ": r"$\Sigma$",
    "Τ": r"$T$",
    "Υ": r"$\Upsilon$",
    "Φ": r"$\Phi$",
    "Χ": r"$X$",
    "Ψ": r"$\Psi$",
    "Ω": r"$\Omega$",
}

# Unicode subscripts/superscripts commonly used in text (pdflatex can't)
SUBSCRIPT_UNICODE_TO_LATEX = {
    "₀": r"$_0$",
    "₁": r"$_1$",
    "₂": r"$_2$",
    "₃": r"$_3$",
    "₄": r"$_4$",
    "₅": r"$_5$",
    "₆": r"$_6$",
    "₇": r"$_7$",
    "₈": r"$_8$",
    "₉": r"$_9$",
    "₊": r"$_+$",
    "₋": r"$_-$",
    "₌": r"$_=$",
    "₍": r"$_($",
    "₎": r"$_)$",
    "ₐ": r"$_a$",
    "ₑ": r"$_e$",
    "ₕ": r"$_h$",
    "ₖ": r"$_k$",
    "ₗ": r"$_l$",
    "ₘ": r"$_m$",
    "ₙ": r"$_n$",
    "ₒ": r"$_o$",
    "ₚ": r"$_p$",
    "ₛ": r"$_s$",
    "ₜ": r"$_t$",
    "ₓ": r"$_x$",
}

SUPERSCRIPT_UNICODE_TO_LATEX = {
    "⁰": r"$^{0}$",
    "¹": r"$^{1}$",
    "²": r"$^{2}$",
    "³": r"$^{3}$",
    "⁴": r"$^{4}$",
    "⁵": r"$^{5}$",
    "⁶": r"$^{6}$",
    "⁷": r"$^{7}$",
    "⁸": r"$^{8}$",
    "⁹": r"$^{9}$",
    "⁺": r"$^{+}$",
    "⁻": r"$^{-}$",
    "⁼": r"$^{=}$",
    "⁽": r"$^{(}$",
    "⁾": r"$^{)}$",
    # --- extra "math italic" letters that pdflatex can't handle ---
    "𝑇": r"\ensuremath{T}",   # U+1D447 MATHEMATICAL ITALIC CAPITAL T
}


def sanitize_tex_unicode_math(tex: str) -> str:
    out = tex
    for u, repl in GREEK_UNICODE_TO_LATEX.items():
        out = out.replace(u, repl)
    for u, repl in SUBSCRIPT_UNICODE_TO_LATEX.items():
        out = out.replace(u, repl)
    for u, repl in SUPERSCRIPT_UNICODE_TO_LATEX.items():
        out = out.replace(u, repl)

    # --- extra problematic unicode (pdflatex) ---
    out = out.replace("\u2060", "")                         # WORD JOINER (invisible)
    out = out.replace("≈", r"\ensuremath{\approx}")         # U+2248
    out = out.replace("\u200b", "")                         # ZERO WIDTH SPACE
    out = out.replace("\ufeff", "")                         # BOM / ZERO WIDTH NO-BREAK SPACE
    out = out.replace("−", "-")                             # U+2212 minus -> ASCII hyphen-minus
    out = out.replace("⊙", r"\ensuremath{\odot}")           # U+2299 solar symbol

    return out


def sanitize_tex_headers(tex: str) -> str:
    """
    Sanitizes known-dangerous characters in header-ish contexts (title/author/date/section).
    Most common pdflatex killer: unescaped '#'.
    """
    tex = tex.replace("#", r"\#")
    tex = tex.replace("&", r"\&")
    return tex


def sanitize_tex_file_in_place(path: Path, *, headers: bool = False, unicode_math: bool = False) -> bool:
    if not path.exists():
        return False
    src = path.read_text(encoding="utf-8")
    dst = src
    if unicode_math:
        dst = sanitize_tex_unicode_math(dst)
    if headers:
        dst = sanitize_tex_headers(dst)
    if dst != src:
        path.write_text(dst, encoding="utf-8")
        return True
    return False


def find_body_inputs_in_template(tpl_path: Path) -> list[Path]:
    """
    Finds \\input{..._body.tex} occurrences inside the template and returns resolved paths.
    Paths are resolved relative to TEX_DIR (because we compile with cwd=TEX_DIR).
    """
    txt = tpl_path.read_text(encoding="utf-8")
    inputs = re.findall(r"\\input\{([^}]*_body\.tex)\}", txt)
    resolved: list[Path] = []
    for rel in inputs:
        resolved.append((TEX_DIR / rel).resolve())
    return resolved


# -----------------------------------------------------------------------------
# Failure logging
# -----------------------------------------------------------------------------

FAIL_LOG = BUILD_DIR / "build_pdfs_failures.log"
TAIL_N = 80


def _tail_text(path: Path, n_lines: int = 80) -> str:
    if not path.exists():
        return f"(missing: {path})"
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(lines[-n_lines:])
    except Exception as e:
        return f"(failed to read {path}: {e})"


def log_failure(
    *,
    jobname: str,
    tpl: Path,
    cmd: list[str],
    returncode: int | None,
    log_path: Path,
    pdf_path: Path,
    exc: BaseException | None = None,
) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FAIL_LOG, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 90 + "\n")
        f.write(f"FAILED: {jobname}\n")
        f.write(f"Time: {ts}\n")
        f.write(f"Template: {tpl}\n")
        f.write(f"Return code: {returncode}\n")
        f.write("Command: " + " ".join(cmd) + "\n")
        f.write(f"Expected build log: {log_path}  (exists={log_path.exists()})\n")
        f.write(f"Expected PDF      : {pdf_path}  (exists={pdf_path.exists()})\n")

        if exc is not None:
            f.write("-" * 90 + "\n")
            f.write("Python exception:\n")
            f.write("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))

        f.write("-" * 90 + "\n")
        f.write(f"TAIL of build log (last ~{TAIL_N} lines):\n")
        f.write(_tail_text(log_path, TAIL_N))
        f.write("\n")


# -----------------------------------------------------------------------------
# Build helpers
# -----------------------------------------------------------------------------

def latexmk_build(template_path: Path, jobname: str, texinputs_dir: Path) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    # TEXINPUTS must end with ":" so TeX also searches default paths
    env["TEXINPUTS"] = f"{texinputs_dir}:{env.get('TEXINPUTS', '')}"

    cmd = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-outdir={BUILD_DIR}",
        f"-jobname={jobname}",
        str(template_path),
    ]

    print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=str(TEX_DIR), env=env, check=True)


def derive_jobname_from_tpl(tpl: Path) -> str:
    # "ACA_001_RU.tpl.tex" -> "ACA_001_RU"
    name = tpl.name
    if name.endswith(".tpl.tex"):
        return name[:-len(".tpl.tex")]
    return tpl.stem


def _split_patterns(pats: list[str] | None) -> list[str]:
    if not pats:
        return []
    out: list[str] = []
    for p in pats:
        for part in p.split(","):
            part = part.strip()
            if part:
                out.append(part)
    return out


def discover_templates(*, tpl: str | None, patterns: list[str] | None) -> list[Path]:
    """
    Resolution rules:
    - if --tpl given: build only that template (exact filename inside TEX_DIR)
    - else if --pattern given: glob each pattern relative to TEX_DIR
    - else: build all *.tpl.tex in TEX_DIR
    """
    if not TEX_DIR.exists():
        raise FileNotFoundError(f"Missing TEX_DIR: {TEX_DIR}")

    if tpl:
        p = TEX_DIR / tpl
        if not p.exists():
            raise FileNotFoundError(f"Missing template: {p}")
        return [p]

    pats = _split_patterns(patterns)
    if pats:
        found: list[Path] = []
        for pat in pats:
            found.extend(sorted(TEX_DIR.glob(pat)))
        # if user passed "ACAP_*.tpl.tex" etc, ok.
        # also allow user to omit suffix and write "ACAP_*" -> we interpret literally (glob will match)
        found = [p for p in found if p.is_file()]
        # keep only tpl templates (avoid accidental matches)
        found = [p for p in found if p.name.endswith(".tpl.tex")]
        # de-dupe while preserving order
        seen: set[Path] = set()
        uniq: list[Path] = []
        for p in found:
            rp = p.resolve()
            if rp not in seen:
                seen.add(rp)
                uniq.append(rp)
        if not uniq:
            raise FileNotFoundError(f"No templates matched patterns: {pats}")
        return uniq

    # default: all templates
    all_tpls = sorted(TEX_DIR.glob("*.tpl.tex"))
    return [p.resolve() for p in all_tpls]


def build_one_template(tpl: Path, *, jobname_override: str | None, texinputs_dir: Path) -> bool:
    """
    Returns True if built successfully, False if failed (and logged).
    """
    jobname = jobname_override or derive_jobname_from_tpl(tpl)

    # 1) sanitize template headers
    changed_tpl = sanitize_tex_file_in_place(tpl, headers=True, unicode_math=False)
    if changed_tpl:
        print(f"Sanitized template headers: {tpl.name}")

    # 2) sanitize referenced body files for unicode math
    body_paths = find_body_inputs_in_template(tpl)
    print("[BODY INPUTS]")
    for bp in body_paths:
        print(" -", bp)
    if not body_paths:
        print(f"NOTE: {tpl.name} has no *_body.tex inputs (ok if intended).")

    for bp in body_paths:
        changed_body = sanitize_tex_file_in_place(bp, headers=False, unicode_math=True)
        if changed_body:
            print(f"Sanitized body unicode math: {bp}")

    # 3) Build
    try:
        latexmk_build(tpl, jobname, texinputs_dir)
        print("\n[DONE]")
        print("PDF:", (BUILD_DIR / f"{jobname}.pdf").resolve())
        return True

    except subprocess.CalledProcessError as e:
        log_path = BUILD_DIR / f"{jobname}.log"
        pdf_path = BUILD_DIR / f"{jobname}.pdf"

        cmd = [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={BUILD_DIR}",
            f"-jobname={jobname}",
            str(tpl),
        ]

        log_failure(
            jobname=jobname,
            tpl=tpl,
            cmd=cmd,
            returncode=getattr(e, "returncode", None),
            log_path=log_path,
            pdf_path=pdf_path,
            exc=None,
        )

        print(f"\n[FAILED] {jobname} (see {log_path})")
        return False

    except Exception as e:
        log_path = BUILD_DIR / f"{jobname}.log"
        pdf_path = BUILD_DIR / f"{jobname}.pdf"

        cmd = [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={BUILD_DIR}",
            f"-jobname={jobname}",
            str(tpl),
        ]

        log_failure(
            jobname=jobname,
            tpl=tpl,
            cmd=cmd,
            returncode=None,
            log_path=log_path,
            pdf_path=pdf_path,
            exc=e,
        )

        print(f"\n[FAILED (python)] {jobname} (see {FAIL_LOG})")
        return False


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Build PDFs from one template, a pattern set, or all templates in TEX_DIR."
    )
    ap.add_argument(
        "--tpl",
        default=None,
        help="Build only this template filename inside TEX_DIR (e.g. ACAP_001_EN.tpl.tex).",
    )
    ap.add_argument(
        "--pattern",
        action="append",
        default=None,
        help=(
            "Glob pattern(s) relative to TEX_DIR. Can be repeated or comma-separated.\n"
            "Examples: --pattern 'ACAP_*_EN.tpl.tex' --pattern 'ANIM_*.tpl.tex'\n"
            "          --pattern 'ACAP_*.tpl.tex,ANIM_*.tpl.tex'"
        ),
    )
    ap.add_argument(
        "--jobname",
        default=None,
        help="Override jobname (ONLY meaningful with --tpl; ignored in batch mode).",
    )
    ap.add_argument(
        "--keep-fail-log",
        action="store_true",
        help="Do not reset failures log at start.",
    )
    ap.add_argument(
        "--stop-on-fail",
        action="store_true",
        help="Stop immediately on first failed PDF (default: continue batch).",
    )
    args = ap.parse_args()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # reset failure log each run (unless asked not to)
    if not args.keep_fail_log:
        with open(FAIL_LOG, "w", encoding="utf-8") as f:
            f.write("build_pdf failures log\n")
            f.write(f"TOPIC_DIR: {TOPIC_DIR}\n")
            f.write(f"TEX_DIR  : {TEX_DIR}\n")
            f.write(f"BUILD_DIR: {BUILD_DIR}\n")
            f.write("=" * 90 + "\n")

    templates = discover_templates(tpl=args.tpl, patterns=args.pattern)
    print("[TEMPLATES]")
    for t in templates:
        print(" -", t.name)

    texinputs_dir = TEX_DIR

    failed: list[str] = []
    for tpl_path in templates:
        print("\n" + "=" * 90)
        print("BUILD:", tpl_path.name)
        print("=" * 90)

        # jobname override only makes sense for single-template build
        job_override = args.jobname if (args.tpl and len(templates) == 1) else None

        ok = build_one_template(tpl_path, jobname_override=job_override, texinputs_dir=texinputs_dir)
        if not ok:
            failed.append(derive_jobname_from_tpl(tpl_path))
            if args.stop_on_fail:
                break

    if failed:
        print("\n" + "=" * 90)
        print("[SUMMARY] FAILED:")
        for j in failed:
            print(" -", j)
        print("See:", FAIL_LOG.resolve())
        raise SystemExit(1)

    print("\n" + "=" * 90)
    print("[SUMMARY] ALL OK")
    print("PDFs in:", BUILD_DIR.resolve())


if __name__ == "__main__":
    main()