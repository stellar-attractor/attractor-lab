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

---

## 2025-12-22 04:01 — TOP_0001 foundation stabilized

**Context**  
The first complete end-to-end pass for topic TOP_0001 (Exoplanet Birth Radius) has been completed — from repository structure to fully reproducible PDF generation with figures and scripts.

**What was done**
- Finalized the core architecture of the `attractor-lab` repository:
  - clear separation between `core/` (reusable code) and `topics/` (content packages);
  - single source of truth for Python code, TeX content, and notebooks.
- Implemented a full data pipeline for TOP_0001:
  - downloading real datasets (SWEET-Cat + NASA Exoplanet Archive);
  - normalization and merging at the host-star level;
  - saving a reproducible processed CSV snapshot.
- Added a complete set of diagnostic and scientifically relevant figures:
  - FIG_001–FIG_007 (metallicity distribution, distance bias, stellar parameters, planet properties).
- Stabilized CHR PDF generation:
  - TeX snippet export from notebooks;
  - centralized LaTeX preamble resolved via `TEXINPUTS`;
  - clean, reproducible build of `CHR.pdf` including all figures.
- Established Git data policy:
  - `data/raw/`, `sources/papers/`, and `figures/` are excluded from version control;
  - only code, TeX sources, notebooks, and processed data are tracked.

**Result**
- The first topic-pack is fully reproducible from scratch:
  `fetch data → build figures → export TeX → build PDF`.
- The repository is ready for public sharing and long-term scaling.
- TOP_0001 now serves as a reference implementation for future topics.

**Notes**
- Distance fields (`sy_dist`, `Distance`) are correctly interpreted as
  *star → Earth* distances, not *planet → star* separations.
- The next step is the scientific interpretation of FIG_002–FIG_007
  and their transformation into the final “Celestial Chronicles” script.

---

## 2025-12-22 04:23 — RU/EN split for TeX + bilingual figure pipeline

**Context**  
We reached the point where language becomes part of the content. To avoid mixing Russian and English versions inside the same artifacts, we introduced a clean RU/EN separation for LaTeX sources and figure generation.

**What was done**
- Introduced topic-level, language-specific LaTeX preambles:
  - `topics/TOP_0001_exoplanet_birth_radius/tex/preamble_en.tex`
  - `topics/TOP_0001_exoplanet_birth_radius/tex/preamble_ru.tex`
- Deprecated the old core preamble by renaming:
  - `core/src/lulab/tex/preamble.tex` → `core/src/lulab/tex/preamble_LEGACY.tex`
- Updated plotting code to support localization:
  - `core/src/lulab/viz/plots.py` now accepts `lang="en"|"ru"` and renders titles/labels accordingly.
- Updated figure builder to produce two language variants:
  - `figures/en/` and `figures/ru/` (both ignored by git as generated artifacts).
- Updated PDF build script to compile both languages from topic `tex/` entrypoints:
  - build targets moved from a single `CHR.tex` to separate RU/EN entrypoints.

**Result**
- The topic can now generate fully consistent bilingual deliverables:
  - English PDF uses English text, English captions, and `figures/en/`.
  - Russian PDF uses Russian text, Russian captions, and `figures/ru/`.
- `core/` remains language-agnostic; language decisions live inside `topics/`.

**Notes / next**
- Ensure consistent naming conventions for entrypoint files (`CHR_EN.tex` / `CHR_RU.tex`) to avoid case-sensitivity issues on CI/Linux.
- Next: finalize `birth_radius_*` TeX snippets for both languages and start writing the full CHR script (EN first, then RU adaptation).
----

2025-12-22 10:35 — Milestone: ipynb-first publishing pipeline (RU/EN) + stable LaTeX templates
	•	Switched the CHR workflow to an ipynb-as-source-of-truth approach: CHR.ipynb was replaced by CHR_RU.ipynb and CHR_EN.ipynb.
	•	Introduced non-destructive LaTeX templating: CHR_RU.tpl.tex / CHR_EN.tpl.tex are now the only hand-maintained TeX entrypoints; build scripts no longer overwrite template files.
	•	Added an explicit intermediate build layer via _tmp/:
	•	notebook export produces _tmp/CHR_*_body.tex (and related intermediates),
	•	templates \input{../_tmp/CHR_*_body.tex} to compile PDFs reproducibly.
	•	Implemented / added core helpers for notebook→markdown→tex export (core/src/lulab/tex/...) and updated topic scripts accordingly.
	•	Updated .gitignore to keep the repo public-friendly (exclude build artifacts and bulky inputs while keeping reproducibility).
	•	Cleaned legacy artifacts (CHR_RU.tex, CHR_EN.tex, old CHR.ipynb) to avoid ambiguity and enforce the one-way source flow.

Result: reproducible RU+EN PDF builds from editable notebooks, with templates stable and generation isolated to _tmp/ + build/.