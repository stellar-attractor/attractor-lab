PIPELINE:

# 1. ipynb → body.tex
python topics/TOP_0001_exoplanet_birth_radius/scripts/export_bodies_from_ipynb.py

# 2. tpl.tex + body.tex → PDF
python topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdfs.py