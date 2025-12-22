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

---

## Data → Figure → PDF pipeline validated (TOP_0001)

Validated a full end-to-end pipeline using a synthetic dataset:

- Topic-local processed data stored under `data/processed/`.
- Reusable loaders and plotting functions added to `lulab`.
- Topic-level figure build script generates reproducible figures (FIG_001).
- Figures are excluded from version control and treated as build artifacts.
- Generated figures are embedded into LaTeX and compiled into PDF deliverables.

This confirms that the project infrastructure supports reproducible,
data-driven narrative content, with a clean separation between
source-of-truth (data + code) and generated artifacts.

---

## Transition to real scientific data (TOP_0001)

The project has successfully transitioned from synthetic test data to a real,
publicly available scientific dataset, validating the full research-to-media
pipeline on an actual peer-reviewed study.

### Data sources
- SWEET-Cat catalog (homogeneous stellar parameters; SWFlag = 1)
- NASA Exoplanet Archive (planetary systems table, default_flag = 1)
- Reference paper: Teixeira, Adibekyan, Bossini et al. (2025),
  “Where in the Milky Way do exoplanets preferentially form?” (arXiv:2501.11660)

### Implemented workflow
- Automated download of raw catalogs into `data/raw/` (gitignored).
- Robust merging of SWEET-Cat and NEA datasets using Gaia DR3 source identifiers,
  with a hostname-based fallback for unmatched cases.
- Construction of a reproducible processed snapshot
  (`data/processed/sample_planets_real.csv`, 1522 rows).
- Clear separation between:
  - raw data (local, ignored),
  - processed data (versioned),
  - generated artifacts (figures, PDFs; ignored).

### Visualization
- FIG_001 updated to use real host-star metallicity data ([Fe/H]).
- Figures are generated deterministically from processed data and excluded from git.

### Outcome
This milestone confirms that the project infrastructure supports:
- reproducible scientific data processing,
- transparent provenance of results,
- seamless integration of real astrophysical data into narrative
  and media-ready LaTeX deliverables.

TOP_0001 is no longer a demonstration topic but a fully grounded
research-backed content unit.