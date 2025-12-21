from pathlib import Path
from lulab.tex.export import export_tex_snippets

TOPIC_DIR = Path(__file__).resolve().parents[1]
NB = TOPIC_DIR / "notebooks" / "CHR.ipynb"
OUT = TOPIC_DIR / "tex" / "snippets"

def main():
    written = export_tex_snippets(NB, OUT)
    print("Exported snippets:")
    for p in written:
        print(" -", p)

if __name__ == "__main__":
    main()