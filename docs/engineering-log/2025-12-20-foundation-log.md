# Engineering Log — 2025-12-20
## Attractor Lab: Foundation Day

This document captures the architectural and organizational decisions
made during the initial setup of Attractor Lab.

### Key outcomes
- Repository identity and scope finalized.
- GitHub organization-level workflow established.
- Core Python package (`lulab`) introduced.
- Separation between science (topics), formats, and tooling defined.

### Rationale
The project is designed to scale across many scientific topics while
maintaining a single source of truth for data, code, and narrative assets.

### Notes
This log intentionally focuses on decisions and structure, not implementation details.

---

## Notebook → LaTeX → PDF pipeline (TOP_0001)

Implemented a reproducible pipeline where Jupyter notebooks act as the
single source of truth for narrative text and formulas.

### Key elements
- LaTeX content is authored directly in notebook cells.
- Cells are tagged (`tex:<name>`) and exported into standalone `.tex` snippets.
- Topic-local build scripts export snippets and compile PDFs in one step.
- Core LaTeX preamble and macros are centralized under `lulab/tex`.
- LaTeX build is isolated per topic (`build/` directory, gitignored).

### Rationale
This approach avoids duplication between notebooks and LaTeX sources,
keeps scientific narration close to exploratory analysis,
and enables fully reproducible media-ready PDFs.

The solution is editor-agnostic (works in Windsurf) and does not rely on
LaTeX relative paths, ensuring long-term maintainability.