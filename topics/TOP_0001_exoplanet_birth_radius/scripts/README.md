PIPELINE:

# 1. ipynb → body.tex
python topics/TOP_0001_exoplanet_birth_radius/scripts/export_bodies_from_ipynb.py

# 2. tpl.tex + body.tex → PDF
python topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdf.py

One template:
python3 topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdf.py --tpl ACAP_001_EN.tpl.tex

Pattern:
python3 topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdf.py --pattern "ACAP_*_EN.tpl.tex"

Several patterns:
python3 topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdf.py --pattern "ACAP_*_EN.tpl.tex" --pattern "ANIM_*.tpl.tex"

Divided by comma:
python3 topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdf.py --pattern "ACAP_*_EN.tpl.tex,ACAP_*_RU.tpl.tex"

ALL:
python3 topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdf.py

===

## PDF Build Pipeline — How It Works

This project uses a **template-driven PDF build pipeline**.  
The key design principle is that **LaTeX templates (`*.tpl.tex`) are the single source of truth** for what gets built into PDFs.


### 1. What `build_pdf.py` Processes

`build_pdf.py` **does not scan notebooks (`.ipynb`)**.

It processes **only LaTeX templates** located in:
`topics//tex/*.tpl.tex`

If a template exists, it is considered *publishable*.  
If it does not exist, the corresponding notebook is **ignored by design**.

**Rule:** no template → no PDF.

### 2. What Happens During a Build

For each `*.tpl.tex` file:

1. The template includes a generated body:
   \input{_tmp/XXX_YYY_LANG_body.tex}
2.	The body file:
	•	is generated earlier from a notebook
	•	already contains all content (text, equations, figures, references)
3.	build_pdf.py then:
	•	sanitizes template headers (LaTeX-safe)
	•	sanitizes Unicode math in body files (pdflatex compatibility)
	•	runs latexmk
	•	writes the final PDF into:

`topics/<TOPIC>/build/`

### 3. Notebooks Without Templates

If a notebook exists but no matching .tpl.tex file is present:
	•	it is not built
	•	it produces no PDF
	•	it causes no errors

This is intentional.

Why this is a feature:
	•	not every notebook is meant for publication
	•	drafts and experiments can coexist safely
	•	publication control is explicit and manual

Think of *.tpl.tex as a publication contract.


### 4. Typical Workflow
.ipynb
   ↓ export_bodies_from_ipynb.py
_tmp/XXX_body.tex
   ↓ (template exists?)
XXX.tpl.tex
   ↓ build_pdf.py
build/XXX.pdf

If any step is missing, the pipeline stops cleanly.


### 5. Pattern-Based Builds

You can build:
	•	a single document
	•	a subset
	•	or everything

Examples:
python build_pdf.py --tpl ACAP_001_EN.tpl.tex
python build_pdf.py --pattern "ACAP_*"
python build_pdf.py --pattern "*_EN"

Only matching templates are processed.

### 6. Why This Architecture Scales

This design provides:
	•	strict separation between content and publication
	•	full control over what is released
	•	safe coexistence of many notebooks
	•	predictable, reproducible builds

It is intentional, minimal, and production-grade.