from __future__ import annotations

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
    out = out.replace("\u2060", "")            # WORD JOINER (invisible), e.g. "⁠."
    out = out.replace("≈", r"\ensuremath{\approx}")       # U+2248
    out = out.replace("\u200b", "")            # ZERO WIDTH SPACE
    out = out.replace("\ufeff", "")            # BOM / ZERO WIDTH NO-BREAK SPACE
    out = out.replace("−", "-")                # U+2212 minus -> ASCII hyphen-minus
    out = out.replace("⊙", r"\ensuremath{\odot}")         # U+2299 solar symbol

    return out


def sanitize_tex_headers(tex: str) -> str:
    """
    Sanitizes known-dangerous characters in header-ish contexts (title/author/date/section).
    Most common pdflatex killer: unescaped '#'.
    """
    # Escape # everywhere (safe default).
    tex = tex.replace("#", r"\#")

    # Optional: make sure raw '&' doesn't break tabular alignment if it appears in plain text.
    # If you DO want to use & in TeX intentionally, write it as \& in notebooks.
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
    Finds \input{..._body.tex} occurrences inside the template and returns resolved paths.
    Paths are resolved relative to TEX_DIR (because we compile with cwd=TEX_DIR).
    """
    txt = tpl_path.read_text(encoding="utf-8")
    inputs = re.findall(r"\\input\{([^}]*_body\.tex)\}", txt)
    resolved: list[Path] = []
    for rel in inputs:
        # rel could be "_tmp/..." or "../_tmp/..." etc. We compile with cwd=TEX_DIR.
        resolved.append((TEX_DIR / rel).resolve())
    return resolved


# -----------------------------------------------------------------------------
# Failure logging (added)
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

def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> None:
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, check=True)


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


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    if not TEX_DIR.exists():
        raise FileNotFoundError(f"Missing TEX_DIR: {TEX_DIR}")

    texinputs_dir = TEX_DIR

    templates = sorted(TEX_DIR.glob("*.tpl.tex"))
    if not templates:
        print("No templates found in:", TEX_DIR)
        return

    # reset failure log each run
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAIL_LOG, "w", encoding="utf-8") as f:
        f.write("build_pdfs failures log\n")
        f.write(f"TOPIC_DIR: {TOPIC_DIR}\n")
        f.write(f"TEX_DIR  : {TEX_DIR}\n")
        f.write(f"BUILD_DIR: {BUILD_DIR}\n")
        f.write("=" * 90 + "\n")

    print(f"Found templates: {len(templates)}")
    ok: list[str] = []
    failed: list[str] = []

    for tpl in templates:
        jobname = derive_jobname_from_tpl(tpl)

        # 1) sanitize template headers (protects \title{...} etc)
        changed_tpl = sanitize_tex_file_in_place(tpl, headers=True, unicode_math=False)
        if changed_tpl:
            print(f"Sanitized template headers: {tpl.name}")

        # 2) sanitize any referenced body files for unicode math
        body_paths = find_body_inputs_in_template(tpl)
        if not body_paths:
            print(f"NOTE: {tpl.name} has no *_body.tex inputs (ok if intended).")

        for bp in body_paths:
            changed_body = sanitize_tex_file_in_place(bp, headers=False, unicode_math=True)
            if changed_body:
                print(f"Sanitized body unicode math: {bp}")

        # 3) Build
        try:
            latexmk_build(tpl, jobname, texinputs_dir)
            ok.append(jobname)
        except subprocess.CalledProcessError as e:
            failed.append(jobname)

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

            print(f"FAILED: {jobname} (see {log_path})")

        except Exception as e:
            failed.append(jobname)

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

            print(f"FAILED (python): {jobname} (see {FAIL_LOG})")

    print("\nDone.")
    print("PDFs in:", BUILD_DIR)
    if ok:
        print("OK:", ", ".join(ok))
    if failed:
        print("FAILED:", ", ".join(failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()