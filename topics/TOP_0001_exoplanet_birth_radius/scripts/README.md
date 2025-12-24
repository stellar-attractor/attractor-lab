PIPELINE:

# 1. ipynb → body.tex
python topics/.../scripts/export_bodies_from_ipynb.py

# 2. tpl.tex + body.tex → PDF
python topics/.../scripts/build_pdfs.py