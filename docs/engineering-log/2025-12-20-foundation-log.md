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
