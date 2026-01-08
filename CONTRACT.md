# CONTRACT.md — Working Agreement for Notebooks & Animations

## 0. Purpose
This contract defines **fixed coding patterns** for notebooks.
Goal: **maximum predictability, zero surprise refactors, copy-paste reuse**.

If something is not explicitly requested — **do not change it**.


## 1. BOOTSTRAP (FROZEN)
- Bootstrap cell is **frozen**.
- It is copied verbatim between notebooks.
- No renaming, no reordering, no “improvements”.
- Any change to bootstrap requires **explicit user approval**.

Includes (but not limited to):
- paths, FPS/DPI, export helpers
- `save_animation()`, `anim_outpath()`
- i18n init: `L`, `T`, `_i18n_get`


## 2. i18n RULES (PLOT-ONLY)
- i18n is applied **only to plot-visible text**:
  - `xlabel`, `ylabel`, `title`
  - legends
  - on-plot annotations (`time_txt`, callouts)
- Pattern is **fixed** and reused everywhere:

LABEL = _i18n_get(L, "common", "x_kpc", default="X (kpc)")
TITLE = _i18n_get(T, NOTEBOOK, "some_title_key", default="...")

Always use:
ax.set_xlabel(LABEL)
ax.set_title(TITLE)

Do NOT invent alternative access patterns.
Do NOT refactor working i18n code.

## 3. LOCAL PATCH ONLY
- Changes must be local to the requested cell.
- No cascading edits across the notebook.
- No renaming of variables unless explicitly asked.
- No “cleanup”, no “style unification”, no “best practice rewrite”.


## 4. CONSISTENT PATTERNS
- If a pattern already exists in a previous notebook or cell:
→ reuse it exactly.
-   Never introduce a new mechanism when an existing one works.
- Copy-paste friendliness is a requirement.



## 5. NO HIDDEN REFACTORING

Forbidden unless explicitly requested:
- changing animation method
- changing naming conventions
- changing data access patterns
- changing logic “for clarity”
- changing working code structure


## 6. SCIENTIFIC SCOPE
- All models are illustrative unless stated otherwise.
- Do not upgrade toy models into “more physical” ones unless asked.
- Visual clarity > physical completeness.


## 7. FAILURE MODE

If unsure:
- Ask before changing.
- Default action: do nothing.


##8. ACCEPTANCE

By continuing work, the assistant agrees to:
- Respect frozen contracts
- Prefer reuse over novelty
- Optimize for user time, not code novelty