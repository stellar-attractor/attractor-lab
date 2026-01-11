PIPELINE:

# 1. ipynb → body.tex
python topics/TOP_0001_exoplanet_birth_radius/scripts/export_bodies_from_ipynb.py

# 2. tpl.tex + body.tex → PDF
python topics/TOP_0001_exoplanet_birth_radius/scripts/build_pdfs.py


PYTHONPATH=core/src 

python topics/TOP_0001_exoplanet_birth_radius/scripts/build_one_pdf_az001.py

python topics/TOP_0001_exoplanet_birth_radius/scripts/build_one_pdf_az001.py \
  --tpl AZ_001_EN.tpl.tex \
  --jobname AZ_001_EN
