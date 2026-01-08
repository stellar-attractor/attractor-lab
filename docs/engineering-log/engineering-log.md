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

---

## 2025-12-24 04:23

Stabilized the full documentation pipeline for Topic TOP_0001.

Key results:
- ipynb declared as the single source of truth for all narrative content
- automated export: ipynb → sanitized LaTeX body → PDF
- unified bilingual structure (RU / EN) across all document types:
  CHR, MIN, ACA, ACAP, AZ, TERM, NOTE, TOP, MISC
- LaTeX sanitization integrated directly into export_bodies_from_ipynb.py
  (Unicode symbols, emojis, math edge cases)
- all document types successfully build to PDF without manual fixes

Outcome:
The system is now ready for scalable content production across multiple topics
with minimal maintenance overhead.

---
## 2025-12-25 13:34

Context

Work on topic TOP_0001_exoplanet_birth_radius focused on consolidating the computational pipeline for stellar age estimation, Galactic Chemical Evolution (GCE) inversion, and reconstruction of stellar birth radii. The main goal was to separate computational logic from narrative notebooks and to ensure full reproducibility of all figures used in articles and scripts.

Key changes and decisions

1. Separation of concerns (code vs narrative)
	•	All executable cells responsible for data processing and figure generation were moved into ACAP_001_EN.ipynb (Practikum).
	•	Narrative notebooks (AZ_001_EN.ipynb, AZ_001_RU.ipynb) now only reference precomputed figures via relative paths.
	•	This prevents accidental recomputation, keeps narrative notebooks lightweight, and improves long-term maintainability.


2. Unified figure export mechanism
	•	Introduced a single helper interface: save_fig("Figure_N")
	•	All figures are exported in a consistent format and location:
  topics/TOP_0001_exoplanet_birth_radius/figures/en/Figure_N.png

  	•	Figures are now reusable across notebooks and documents without code duplication.


3. Stellar age reconstruction pipeline
	•	Implemented grid-based stellar age estimation using MIST isochrones.
	•	Multiple fitting strategies were explored (MCMC, emcee, grid minimization).
	•	Final choice: deterministic grid-based interpolation, due to:
	•	robustness,
	•	speed,
	•	absence of external sampler dependencies (e.g. pymultinest),
	•	sufficient accuracy for population-level analysis.
	•	Results saved as: data/processed/sweetcat_ages_grid.csv

  4. Birth-radius reconstruction
	•	Implemented two GCE models:
	•	Toy GCE model (didactic, pipeline validation).
	•	Realistic GCE model (Minchev+2018-like).
	•	Reconstruction explicitly treats metallicity as a tracer of the birth environment, not as a causal variable.
	•	Outputs saved as:
  data/processed/sweetcat_rbirth_toy.csv
  data/processed/sweetcat_rbirth_gce.csv

  5. Figures produced and validated
	•	Figure 1: log g – T_{\rm eff} diagram (SWEET-Cat + HARPS-GTO).
	•	Figure 2: \[Fe/H\] distributions.
	•	Figures 5–7: comparison of toy vs realistic GCE, r_{\rm birth} vs age, and r_{\rm birth} vs metallicity.
	•	All figures are now reproducible from a clean checkout using ACAP only.

Technical notes
	•	Absolute paths were fully removed; all file access is relative to project root.
	•	Intermediate CSV products are committed to ensure reproducibility and to avoid long recomputation cycles.
	•	Some age outliers were clipped (0.1–13.5 Gyr) to avoid non-physical artifacts of the grid method.


Known limitations / next steps
	•	Ages for HARPS-GTO single stars are not yet computed; required for full reproduction of multi-panel figures similar to Figure 9 in the reference paper.
	•	Planet-mass–dependent analysis (HMPH vs LMPH) is planned but not yet implemented.
	•	Possible future improvement: document processed data products with a dedicated data/processed/README.md.

Status

Pipeline stable.
All current figures reproducible.
Repository state committed and clean.

---
## 2025-12-26 13:11

Engineering Log — Animation & Reproducibility Phase

Topic: Galactic Birth Radius of Exoplanet Host Stars
git Notebook(s): ACAP_001_EN, ANIM_001_EN, ANIM_001_RU
Date: 2025-12-26

Scope

This phase focused on transitioning from static, paper-style figures to reproducible, video-ready animations, while simultaneously validating the practical reproducibility of published results on Galactic birth radii of exoplanet host stars.

⸻

Practical exercises (ACAP_001_EN)

In the practical notebook ACAP_001_EN, we reconstructed key elements of the analysis presented in the reference paper:
	•	Reproduced stellar sample selections using SWEET-Cat and HARPS-GTO datasets.
	•	Implemented grid-based stellar age estimation (MIST-based interpolation) as a lightweight, transparent alternative to full Bayesian fitting.
	•	Explored toy and Minchev-like Galactic Chemical Evolution (GCE) prescriptions to reconstruct stellar birth radii.
	•	Compared reconstructed distributions against published figures and assessed qualitative agreement.

A key outcome was the recognition that exact visual reproduction of published plots is non-trivial, even when using identical data sources and nominally the same methodology. Small, often undocumented choices (binning, filtering, implicit priors, clipping, normalization) materially affect the final appearance, while preserving the underlying physical trends. This observation was explicitly documented in the practical notes as a methodological caveat.

⸻

Animation pipeline

A dedicated animation workflow was developed in separate notebooks (ANIM_001_EN, ANIM_001_RU), deliberately decoupled from the analytical notebooks.

Implemented features include:
	•	Two histogram animation modes:
	•	Strict reveal (scientifically neutral, monotonic buildup)
	•	Equalizer-style reveal (temporally smoothed stochastic jitter converging to the exact final distribution)
	•	Global export switches:
	•	mp4 / gif output
	•	light / dark visual themes
	•	Consistent axis handling (fixed limits, zero-based Y axes) to avoid misleading visual artifacts during animation.
	•	Combined log g–T_eff scatter animations with controlled reveal order:
	•	left-to-right (screen space)
	•	randomized reveal

All animation outputs are written to dedicated, git-ignored directories to keep the repository clean and reproducible.

⸻

Key results and insights
	•	The qualitative scientific conclusions of the reference paper (metallicity dependence, inner-disk preference for giant planet hosts, time evolution of formation efficiency) were reproducible.
	•	Exact visual agreement with published figures was not guaranteed without additional, implicit methodological information.
	•	For communication and outreach purposes, controlled, well-documented visual storytelling (animations with known behavior) is preferable to attempting pixel-perfect reproduction.
	•	Separating analysis (ACAP) from presentation (ANIM) significantly improved clarity, maintainability, and creative flexibility.

⸻

Next steps
	•	Animate formation efficiency vs. birth radius (Figures 8–9 analogs) with error bars and staged reveal.
	•	Integrate animations into short-form video pipelines (16:9 and 9:16 variants).
	•	Optionally formalize the practical notebook as a standalone reproducibility case study.

---
## 2025-12-27 12:44

Вот аккуратная запись для engineering log — в ней зафиксировано что именно сделали, какие решения приняли и почему.

⸻

Engineering Log — 2025-12-27

Topic: Galactic Chemical Evolution — Figure 2 (Age–Metallicity–Radius)

Goal

Reproduce a paper-style, low-cost visualization of Galactic Chemical Evolution using observational data, suitable for outreach and explanatory content (no heavy modeling).

What was implemented
	1.	APOGEE × Gaia EDR3 cross-match
	•	Used APOGEE DR17 allStar catalog (III/286).
	•	Cross-matched with Gaia EDR3 via CDS TAP/ADQL to obtain parallaxes.
	•	Computed galactocentric cylindrical radius R_{\rm gal} using astropy (Galactocentric frame, R_0=8.2 kpc, Z_0=20.8 pc).
	•	Built a clean working dataset m with:
	•	[Fe/H]
	•	R_gal
	•	Derived a global metallicity gradient:
d[\mathrm{Fe/H}]/dR \approx -0.025 \ \mathrm{dex/kpc}
	2.	MDF by radial bins (panel b)
	•	Constructed metallicity distribution functions for several radial bins (6–8, 8–10, 10–12 kpc).
	•	Rotated MDF by 90° so that [Fe/H] is on the Y-axis, matching the reference paper style.
	•	Ensured consistent [Fe/H] limits across all panels.
	3.	R vs [Fe/H] relation (panel c)
	•	Scatter plot of [Fe/H] vs R_gal using APOGEE × Gaia sample.
	•	Added global linear fit and displayed numerical slope directly on the figure.
	•	Added a reference vertical line at Sun’s inferred birth radius (~5 kpc) for narrative context.
	4.	Age vs [Fe/H] (panel a) — lightweight solution
	•	Abandoned heavy astroNN age pipeline (too slow for interactive work).
	•	Switched to Boulet et al. (2024) asteroseismically calibrated APOGEE ages.
	•	Built df_age with:
	•	Age [Gyr]
	•	[Fe/H]
	•	Plotted Age–Metallicity relation with:
	•	large scatter cloud
	•	binned median trend line (0.5 Gyr bins)
	5.	Final multi-panel figure
	•	Assembled three panels on a single figure:
	•	(a) Age vs [Fe/H]
	•	(b) MDF (rotated)
	•	(c) R vs [Fe/H]
	•	Unified:
	•	[Fe/H] axis limits and ticks
	•	paper-style layout (sharey=True)
	•	minimal duplicated labels
	•	Added export utility:
	•	automatic save to figures/en
	•	publication-ready DPI and bounding box

Key engineering decisions
	•	Decoupled age and radius datasets:
	•	Ages from a calibrated subsample (Boulet+2024).
	•	Radial trends from the full APOGEE × Gaia sample.
	•	Scientifically standard and explicitly documented.
	•	Avoided heavy modeling:
	•	Focused on “cheap but powerful” observables.
	•	Suitable for fast iteration and outreach visualization.
	•	Cached/one-shot philosophy:
	•	No repeated long downloads.
	•	Ready for reuse in figures, videos, and scripts.

Result

A clean, paper-style Figure 2 reproducing key GCE trends:
	•	weak age–metallicity relation,
	•	radial metallicity gradient,
	•	shifting MDF with galactocentric radius,

ready for:
	•	scientific explanation,
	•	outreach videos,
	•	further annotation and storytelling.

----
## 2025-12-29 15:48

### ISM metallicity proxy & Galactic context

- Built large APOGEE DR17 × Gaia DR3 cross-match (~10^5 stars) via VizieR + CDS XMatch
- Constructed present-day radial metallicity gradient [Fe/H](R)
- Implemented binned medians, q16–q84 envelopes, and bin counts
- Identified strong inner-disk incompleteness and justified extrapolation
- Overlaid metallicity profile on schematic Galactic cross-section
- Interpreted shallow gradient (≈ −0.05 dex/kpc) as migration-flattened ISM proxy
- Prepared data export for animation pipeline (ANIM_001_EN.ipynb)

## 2025-12-30 14:48

ACAP_001_EN — Engineering log

Implemented a robust APOGEE × Gaia DR3 pipeline to construct an ISM metallicity proxy across the Galactic disk.
Built face-on Milky Way visualizations illustrating:
– differential rotation,
– radial stellar migration,
– inside-out disk growth,
– and spiral density waves as a rotating pattern distinct from stellar orbits.

Produced several original animations suitable for outreach and explanatory videos.

All animations are illustrative but grounded in real survey data and physically motivated parametrizations.

## 2025-12-31 11:45

Summary

This session focused on building a coherent visual and physical narrative that links:
	•	Galactic-scale stellar migration and spiral density waves
	•	Disk-scale accretion physics around a black hole

We deliberately separated conceptual regimes (galactic disk vs. accretion disk) and implemented each as a standalone toy model with internally consistent dynamics.

⸻

1. Galactic Disk: Stars & Density Waves

Implemented a face-on Milky Way disk model with:
	•	Stellar component
	•	Real-data proxy from APOGEE × Gaia (ISM metallicity tracer)
	•	Differential rotation (flat rotation curve)
	•	Radial migration with stochastic inward/outward components
	•	Age-based evolution (animation starts at ~7–9 Gyr to avoid artificial early rings)
	•	Spiral density waves
	•	Treated explicitly as a pattern, not material arms
	•	Rigid pattern speed distinct from stellar angular velocity
	•	Logarithmic spiral geometry
	•	Stars brighten temporarily while crossing arms (arm membership via phase distance)

Result:
	•	Clear visualization of stars entering and exiting spiral arms
	•	Correct physical intuition: stars do not co-rotate with arms
	•	Density waves propagate through matter rather than dragging it

Artifacts such as early dense rings were mitigated by shifting the animation start time rather than forcing initial conditions.

⸻

2. Accretion Disk Around a Black Hole (New Module)

Developed a separate physical object for black hole accretion, not derived from the galactic model.

Architecture
	•	BlackHole object
	•	Gravitational radius (visual)
	•	ISCO as inner disk boundary
	•	AccretionDisk object
	•	Thousands of tracer particles
	•	Softened Keplerian rotation:
\Omega(R) \propto R^{-3/2}
	•	Viscous-like inward drift, increasing toward ISCO
	•	No spiral arms (explicitly removed)

Disk Physics (Illustrative, but consistent)
	•	Differential shear dominates morphology
	•	Continuous inward mass transport
	•	Inner disk brighter and hotter
	•	Outer disk more diffuse
	•	Density fluctuations emerge naturally from shear + inflow
	•	No galactic-scale wave patterns applied

Visual Enhancements
	•	Dark theme applied globally
	•	Temperature-weighted brightness
	•	Doppler-like asymmetry (approaching side brighter)
	•	Particle birth/death near outer/inner radii
	•	Final frame hold for visual inspection

Result:
	•	Clear visual distinction between galactic disks and accretion disks
	•	Animation now reads correctly as a black hole system, not a galaxy

⸻

3. Key Methodological Decisions
	•	Spiral arms are density waves, not streams of stars
	•	Accretion disks require Keplerian shear, not flat rotation
	•	Early-time artifacts are addressed by time windowing, not parameter hacking
	•	Visual realism prioritized after conceptual correctness

⸻

4. Outputs
	•	ANIM_005_stars_cross_spiral_arms — Galactic density-wave interaction
	•	ANIM_BH_001_accretion_disk_density_wave — Black hole accretion disk toy model

Both animations are suitable for:
	•	Scientific outreach
	•	Conceptual explanation
	•	Further refinement into higher-fidelity simulations

⸻

Next Steps (Deferred)
	•	Relativistic lensing (GR)
	•	Inclined disk projection
	•	Light-travel-time effects
	•	Quantitative comparison with observed pattern speeds

These are intentionally postponed to keep the current models clean and interpretable.

⸻

Conclusion:
The project now contains two physically distinct, visually coherent disk simulations that clearly communicate why galaxies and accretion disks look similar — and why they are fundamentally different.

-----
# Engineering log — Practicum 1 (draft completion)
## Date: 2026-01-02 16:21

Data preparation & consistency
	•	Loaded and cleaned SWEET-Cat stellar parameters with quality filtering (SWFlag = 1).
	•	Implemented robust handling of column-name variability across intermediate CSVs (age, fit flags, birth radius).
	•	Introduced explicit physical age cuts for disk stars to suppress isochrone edge effects.
	•	Ensured consistent merging between stellar ages and metallicities using name-based cross-matching.

Stellar age estimation
	•	Implemented grid-based isochrone fitting using MIST_Isochrone from the isochrones package.
	•	Estimated stellar ages via χ² minimization in $(\log T_{\rm eff}, \log g)$ space.
	•	Applied evolutionary phase (EEP) filtering to suppress unphysical solutions.
	•	Produced a clean, reusable age catalogue for downstream analysis.

Galactic chemical evolution (GCE) models
	•	Implemented a toy GCE model with time-dependent ISM enrichment and metallicity gradient.
	•	Implemented a realistic Minchev-like GCE model with:
	•	logarithmic ISM enrichment at the solar radius,
	•	time-dependent radial metallicity gradient.
	•	Inverted the GCE relations to reconstruct stellar birth radii from age and metallicity.
	•	Clipped reconstructed radii to physically plausible disk ranges.

Analysis & visualization
	•	Constructed publication-style figures for:
	•	metallicity distributions,
	•	stellar age distributions,
	•	age–metallicity relation,
	•	birth radius distributions (toy vs realistic GCE),
	•	birth radius vs age,
	•	birth radius vs metallicity.
	•	Implemented KDE-based mode estimation for birth-radius distributions.
	•	Standardized binning and axis ranges for direct comparison between models.
	•	Identified and mitigated edge-driven artifacts (“walls”) in age and radius distributions.

Scientific validation
	•	Verified that reconstructed birth radii correlate with metallicity in the physically expected sense.
	•	Confirmed broad birth-radius distributions at fixed age, consistent with radial migration.
	•	Demonstrated that age alone does not uniquely determine stellar birth environment.
	•	Established internal consistency between age, metallicity, and reconstructed $r_{\text{birth}}$.

Documentation
	•	Added detailed markdown explanations (EN/RU) for all major analysis cells.
	•	Explicitly distinguished physical causality vs methodological reconstruction.
	•	Prepared Practicum 1 for further refactoring and extension.

Known technical debt / next steps
	•	Refactor shared paths, plotting helpers, and constants into lulab.
	•	Introduce unified RU/EN plotting support (labels, titles, output paths).
	•	Perform full pipeline review to track sample-size losses across steps.
	•	Harmonize column naming across all intermediate CSV products.


## 2026-01-03 15:21
## Engineering log — ACAP_001: i18n & theming refactor

Summary

Refactored plotting and notebook bootstrap to support clean multilingual (EN/RU) switching and explicit theme control without code duplication or hidden side effects.

All figures in ACAP_001 can now be regenerated in different languages and themes using the same notebook code.

⸻

What was done

🌍 Internationalization (i18n)
	•	Introduced topic-level YAML-based i18n for:
	•	axis labels
	•	titles
	•	legends
	•	Unified YAML structure for scalability:
	•	common — shared labels across notebooks
	•	<NOTEBOOK_ID> — notebook-specific labels/titles
	•	Updated plot_text.py:
	•	explicit set_lang()
	•	set_notebook()
	•	robust fallback logic
	•	convenience aliases L() / T()
	•	All plotting cells now reference only keys, never hardcoded strings.

🎨 Theme handling
	•	Clarified separation between:
	•	theme state (THEME)
	•	theme application (apply_theme, set_theme)
	•	Switched notebooks to explicit theme application in bootstrap.
	•	Ensured theme switching does not depend on language or import order.
	•	Verified that figures render correctly in both light and dark themes.

📊 Figures & notebooks
	•	Refactored all plotting cells (Figures 1–8):
	•	removed hardcoded text
	•	unified labels, titles, legends via i18n
	•	kept dataset column names intact
	•	Ensured consistent behavior between EN and RU notebooks.
	•	Verified figure export paths respect language (figures/en, figures/ru).

⸻

Result
	•	One notebook → multiple languages → multiple themes
	•	No duplicated code
	•	No matplotlib state leakage between runs
	•	Safe foundation for adding new notebooks and languages

⸻

Notes
	•	THEME is now treated as state, not configuration.
	•	Theme must be applied explicitly (set_theme() / apply_theme()).
	•	This is intentional to avoid hidden matplotlib side effects.


## 2026-01-04 14:18
### Practicum 2 (ACAP_002): data pipeline refactor, APOGEE × Gaia, chemo-age structure

### Context
Work focused on stabilizing and cleaning up **Practicum 2**, with emphasis on:
- strict separation between data preparation and visualization,
- full reproducibility,
- consistent i18n + theming across notebooks,
- removal of implicit / in-memory data dependencies.

This session finalized **ACAP_002_EN.ipynb** and prepared it for a clean Russian duplicate.

---

### Key problems identified
- Data flow was fragmented and implicit:
  - multiple ad-hoc DataFrames (`m`, `df_age`) created in different cells,
  - unclear provenance of APOGEE ages (Boulet+2024),
  - plotting cells depended on variables created “somewhere above”.
- Figures could not be reliably regenerated without rerunning the whole notebook.
- Inconsistent handling of themes (`THEME` vs `apply_theme`) and language switching.
- YAML i18n files had duplicated top-level keys and mixed responsibilities.
- Several cells existed only to “patch” missing variables (e.g. saving `m`), not for science.

---

### Architectural decisions
1. **CSV-first architecture**
   - Every non-trivial dataset must exist as a saved CSV.
   - Plotting cells only *load CSVs*, never construct core datasets.
   - Result: full reproducibility and decoupling from external services.

2. **Explicit data products**
   The following canonical processed datasets were defined:
   - `apogee_xmatch_raw.csv` — raw APOGEE × Gaia cross-match (debug/provenance)
   - `apogee_ready.csv` — clean APOGEE × Gaia table for structure analysis
   - `boulet_apogee_ages.csv` — APOGEE stars with asteroseismic ages (Boulet+2024)
   - `apogee_gaia_fehr_R.csv` — APOGEE × Gaia with distances and `R_gal`
   
3. **Separation of physical roles**
   - Galactic structure → APOGEE × Gaia (`apogee_ready.csv`)
   - Chemo-age relations → Boulet APOGEE ages
   - Datasets are *not merged by default* to keep assumptions explicit.

4. **Bootstrap standardization**
   - All notebooks now rely on a single bootstrap cell:
     - paths,
     - language,
     - theme,
     - figure export helpers,
     - i18n initialization.
   - Figures are saved via a unified `save_fig0(...)` helper with notebook-aware prefixes.

---

### Major refactors completed
- Fully rewrote APOGEE preparation cell:
  - robust VizieR catalog fallback,
  - explicit metallicity column detection,
  - reproducible sampling,
  - CDS XMatch via file-like upload,
  - schema normalization.
- Removed obsolete SWEET-Cat age cell from Practicum 2
  (ages now consistently sourced from Boulet+2024).
- Rebuilt the main APOGEE figure as a **single 3-panel publication-style plot**:
  - Age vs [Fe/H] (Boulet ages),
  - MDF by Galactocentric radius,
  - [Fe/H] vs R with binned statistics and star counts.
- Restored Boulet et al. (2024) as the authoritative age source
  (previously lost during refactors).
- Cleaned up ISM / animation preparation logic:
  - no more reliance on ephemeral DataFrame `m`,
  - all animation inputs now come from saved CSVs.
- Unified all labels, titles, legends via i18n (`labels.yaml`, `titles.yaml`).

---

### Documentation added
- Full narrative for Practicum 2:
  - Motivation
  - Data sources
  - Intermediate products
  - Data pipeline diagram
  - Figure-by-figure interpretation
- Clear separation between:
  - Part I — present-day Galactic structure,
  - Part II — chemo-age evolution.
- Final conclusions written for:
  - Part I,
  - Part II,
  - Entire Practicum 2.
- Markdown-friendly summaries prepared for PDF export.

---

### Outcome
- **ACAP_002_EN.ipynb** is now:
  - logically structured,
  - reproducible end-to-end,
  - scientifically clean,
  - ready for direct Russian duplication.
- Data pipeline is explicit, inspectable, and reusable.
- Practicum 2 now forms a solid observational foundation for:
  - stellar birth radius reconstruction,
  - Galactic chemical evolution modeling,
  - later animation and visualization notebooks.

### Next steps
- Create **ACAP_002_RU.ipynb** as a language-only duplicate.
- Add BibTeX-based reference handling (later).
- Extend pipeline toward birth-radius reconstruction (next practicum).

---

## Engineering Log — ACAP_003 (Practicum 3) Completion + i18n + RU Copy

**Date:** 2026-01-05  
**Topic:** TOP_0001_exoplanet_birth_radius  
**Notebook:** ACAP_003  
**Status:** completed (EN finalized, RU notebook prepared cell-by-cell, i18n enabled)


### Goal of this iteration

Bring ACAP_003 to a publication-ready, reproducible state, consistent with the standards established in ACAP_002:

- stabilize the data pipeline and intermediate products
- complete Motivation, Conclusions, and detailed per-cell explanations
- migrate final figures to the unified i18n architecture (labels & titles via YAML)
- prepare the Russian counterpart notebook ACAP_003_RU.ipynb


## What was done

### 1. Data pipeline (kept stable by design)

The original step-by-step structure was preserved intentionally — it is logically ordered and readable directly from cell names.

The pipeline relies on explicit sources and produces persistent intermediate CSV files:

- SWEET-Cat: loading, quality filtering (SWFlag == 1), column normalization
- HARPS-GTO (VizieR J/A+A/545/A32): catalog loading, basic quality cuts, [Fe/H] → feh
- NEA: planet catalog parsing, canonical host-name normalization, HMPH / LMPH classification, aggregation at the host level
- MIST grid cache: mist_grid_cache.parquet (built once, reused)
- Stellar ages: fast grid-matching in (Teff, logg, feh) for SWEET and HARPS  
  → sweetcat_ages_grid.csv, harps_ages_grid.csv
- Birth radii: toy GCE inversion  
  → sweetcat_rbirth_gce.csv, harps_rbirth_gce.csv
- Final figures: built exclusively from processed CSVs (fast, reproducible)


### 2. Notebook narrative

Added and refined:

- Motivation, Scientific idea, Structure, Data pipeline
- Detailed explanations for key cells (Cell 1–12)
- Interpretation blocks for Figure 1 and Figure 2
- Updated discussion on why pixel-perfect reproduction is difficult
- Final Conclusions (English and Russian)


### 3. i18n integration for figures

Final plotting cells were migrated to the unified i18n system:

- labels.yaml for axis labels, legends, annotations
- titles.yaml for figure and panel titles

Legacy save helpers were removed.  
We reverted to the proven pattern from ACAP_002 to avoid API mismatches:

- a notebook-scoped save helper
- automatic ACAP_003 prefix in figure filenames
- language-aware output directories


### 4. Final figures

- Figure 1  
  Multi-panel comparison (SWEET-Cat vs HARPS-GTO):  
  age and birth radius, counts plus relative frequencies, paper-like binning, i18n labels and titles

- Figure 2  
  HARPS-GTO only: birth-radius distributions split by age bins, Wilson confidence intervals, i18n-aware rendering

Both figures are generated only from processed CSV files.

### 5. Russian notebook

A cell-by-cell transfer strategy was used to preserve structure and reproducibility.

All translated text is provided in Markdown with original formatting retained.


## What was intentionally postponed

- Bibliography and BibTeX integration  
  (to be addressed at the PDF-rendering stage)
- Large-scale refactoring of the pipeline — only minimal, targeted improvements were made

## Artifacts produced

- data/processed/mist_grid_cache.parquet
- data/processed/sweetcat_ages_grid.csv
- data/processed/harps_ages_grid.csv
- data/processed/sweetcat_rbirth_gce.csv
- data/processed/harps_rbirth_gce.csv
- figures/en/ACAP_003_Figure_1.png
- figures/en/ACAP_003_Figure_2.png
- updated i18n labels.yaml (ACAP_003 entries)
- updated i18n titles.yaml (Figure 1 and Figure 2 for ACAP_003)
- ACAP_003_EN.ipynb (final)
- ACAP_003_RU.ipynb (structure fixed, text in progress)

## Reproducibility check

- All final figures are generated from local CSV files
- External services (VizieR, NEA) are used only upstream and their outputs are cached
- The notebook can be rerun end-to-end without network access once caches exist

## Next steps

- Commit ACAP_003 (EN notebook, figures, i18n updates)
- Finish ACAP_003_RU.ipynb (final verification)
- Move on to ANIM_001–002 (animation pipeline)
---

## 2026-01-06 16:28
### Engineering log — ANIM_002

This section documents the technical and architectural decisions made while refactoring and completing the **ANIM_002** notebook. The goal of this log is to preserve *why* certain choices were made, not just *what* the final code looks like.


### 1. Data sources and reproducibility

**Decision:**  
All animations in ANIM_002 use **processed CSV files only**.

**Rationale:**
- Eliminates runtime dependencies on external services (Vizier, TAP, NEA).
- Guarantees reproducibility across machines and time.
- Allows deterministic debugging of animation logic.

**Key datasets used:**
- `boulet_apogee_ages.csv` — age–metallicity sample.
- `apogee_ready.csv` — APOGEE × Gaia sample with RA/Dec/parallax.
- `apogee_gaia_ism_proxy.csv` — lightweight proxy (R_gal, Z_gal, [Fe/H]).
- SWEET-Cat / HARPS processed grids reused where applicable.

Any cell attempting to re-query catalogs was removed or rewritten to consume these files.


### 2. Bootstrap architecture

**Decision:**  
A single **bootstrap cell** initializes:
- paths (`TOPIC_ROOT`, `PROC`, `ANIM_DIR`),
- animation parameters (`FPS`, `DPI`, format),
- theme handling,
- i18n loading.

**Rationale:**
- Prevents silent divergence between notebooks (ANIM_001, ANIM_002, …).
- Ensures that helper functions (`save_animation`, `_i18n_get`) are always available.
- Makes notebooks portable and order-independent.

**Lesson learned:**  
Helpers must live either in the bootstrap or in imported modules — *never* be redefined ad hoc inside cells.


### 3. i18n integration

**Decision:**  
All user-facing text is retrieved via `_i18n_get()` from YAML files.

**Rationale:**
- Avoids hard-coded strings in animation logic.
- Enables bilingual output without code duplication.
- Keeps scientific terminology consistent across figures and notebooks.

**Key conventions:**
- Axis labels → `common.*`
- Notebook-specific titles → `ANIM_002.*`
- Legends reused from `ACAP_*` where possible.

Fallbacks are always provided to prevent runtime failures.


### 4. Animation timing model

**Decision:**  
Standardized animation timing:
- **3 s reveal + 3 s hold** for point-based animations.
- Fixed `FPS` from bootstrap.

**Rationale:**
- Prevents animations from feeling rushed.
- Ensures the final frame is readable when embedded in presentations or papers.
- Makes different animations visually comparable.


### 5. Scatter reveal strategies

Two complementary reveal modes were implemented:

1. **Ordered reveal (by age or radius)**  
   - Encodes physical causality (e.g., temporal evolution).
   - Used when the ordering itself is meaningful.

2. **Random reveal**  
   - Acts as a sanity check.
   - Confirms that perceived structure is not an artifact of reveal order.

This dual approach was kept intentionally, even when visually redundant.


### 6. Inside-out growth (R–[Fe/H])

**Key refactor:**
- Removed preliminary “sanity” scatter plots.
- Jumped directly to the physically informative animation:
  - progressive `R_max`,
  - binned median,
  - q16–q84 envelope,
  - global metallicity gradient.

**Rationale:**
- Reduces notebook length.
- Focuses attention on the scientifically relevant signal.
- Matches the narrative of inside-out Galactic disk growth.


### 7. Edge-on Galactic profile (R–Z)

**Issue encountered:**
- Flat Z distribution in early attempts.

**Root cause:**
- Accidental use of proxy datasets with `Z_gal = 0`.

**Resolution:**
- Explicitly switched to `apogee_ready.csv` with RA/Dec/parallax.
- Recomputed Galactocentric coordinates using `astropy`.

**Outcome:**
- Correct “fan-like” disk structure.
- Clear interpretation as an **edge-on view of the Milky Way disk**.


### 8. What was deliberately removed

- Repeated exploratory plots already shown in earlier notebooks.
- On-the-fly coordinate recomputation when processed values exist.
- Mixed responsibilities (e.g., saving CSV + plotting in the same cell).

These elements were either redundant or better suited for **ANIM_003**.


### 9. Final state

At the end of this refactor, **ANIM_002** is:
- reproducible,
- modular,
- i18n-complete,
- scientifically focused,
- and ready for reuse in publications or outreach material.

Speculative or exploratory visualizations have been explicitly deferred to **ANIM_003**.

## 2026-01-08 15:55
### Engineering log

- finalized ANIM_003_EN.ipynb
- finalized ANIM_003_RU.ipynb
- proofread and finalized all scenario notebooks

Project is ready for the next step - generate pdfs out of all notebooks.
