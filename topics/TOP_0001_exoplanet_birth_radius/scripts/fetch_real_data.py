from __future__ import annotations

from pathlib import Path
import urllib.request
import pandas as pd


# SWEET-Cat official direct CSV (see SWEET-Cat Python tutorial)
SWEETCAT_URL = "https://sweetcat.iastro.pt/catalog/SWEETCAT_Dataframe.csv"

# NASA Exoplanet Archive TAP query (default_flag=1 = best/default rows per planet)
NEA_PS_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    "query=select+*+from+ps+where+default_flag=1&format=csv"
)

TOPIC_DIR = Path(__file__).resolve().parents[1]
RAW = TOPIC_DIR / "data" / "raw"
PROCESSED = TOPIC_DIR / "data" / "processed"


def download_csv(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading: {url}")
    with urllib.request.urlopen(url) as r:
        out.write_bytes(r.read())
    print(f"Saved: {out}")


def _extract_gaia_num(series: pd.Series) -> pd.Series:
    """
    Extract numeric Gaia DR3 source_id from various string/numeric representations.
    Returns pandas nullable Int64 series.
    """
    s = series.astype(str)

    # Take the first long-ish digit group; Gaia source_id is typically 18-19 digits.
    # But we accept any digits to be permissive.
    digits = s.str.extract(r"(\d+)")[0]
    return pd.to_numeric(digits, errors="coerce").astype("Int64")


def build_processed(
    sweetcat_csv: Path,
    nea_csv: Path,
    out_csv: Path,
    max_distance_pc: float = 2000.0,
) -> None:
    # --- Load ---
    sc = pd.read_csv(sweetcat_csv, low_memory=False)
    nea = pd.read_csv(nea_csv, low_memory=False)

    # --- SWEET-Cat: keep homogeneous params only (paper uses SWFlag=1) ---
    if "SWFlag" in sc.columns:
        sc = sc[sc["SWFlag"] == 1].copy()

    # --- Filter planets below brown-dwarf limit (~13 Mj), if mass column exists ---
    massj_cols = [c for c in ["pl_bmassj", "pl_massj"] if c in nea.columns]
    if massj_cols:
        mj = pd.to_numeric(nea[massj_cols[0]], errors="coerce")
        nea = nea[(mj.isna()) | (mj < 13)].copy()

    # --- Build robust join keys ---
    # SWEET-Cat Gaia key
    if "gaia_dr3" in sc.columns:
        sc["gaia_dr3_num"] = pd.to_numeric(sc["gaia_dr3"], errors="coerce").astype("Int64")
    else:
        sc["gaia_dr3_num"] = pd.Series([pd.NA] * len(sc), dtype="Int64")

    # NEA Gaia key (usually "gaia_id"; may be blank / formatted)
    if "gaia_id" in nea.columns:
        nea["gaia_dr3_num"] = _extract_gaia_num(nea["gaia_id"])
    else:
        nea["gaia_dr3_num"] = pd.Series([pd.NA] * len(nea), dtype="Int64")

    # --- Primary merge: Gaia DR3 numeric source_id ---
    nea_k = nea.dropna(subset=["gaia_dr3_num"]).copy()
    sc_k = sc.dropna(subset=["gaia_dr3_num"]).copy()

    merged = pd.DataFrame()
    if len(nea_k) and len(sc_k):
        merged = nea_k.merge(sc_k, on="gaia_dr3_num", how="inner", suffixes=("_nea", "_sc"))

    # --- Fallback merge: by host name if Gaia match is too small ---
    # NEA uses "hostname"; SWEET-Cat typically uses "Name"
    if merged.empty or len(merged) < 50:
        if "hostname" in nea.columns and "Name" in sc.columns:
            nea2 = nea.copy()
            sc2 = sc.copy()
            nea2["hostname_norm"] = nea2["hostname"].astype(str).str.strip().str.lower()
            sc2["hostname_norm"] = sc2["Name"].astype(str).str.strip().str.lower()

            merged2 = nea2.merge(sc2, on="hostname_norm", how="inner", suffixes=("_nea", "_sc"))

            # If Gaia-merge was small, prefer the larger result; otherwise keep Gaia-merge
            if merged.empty or len(merged2) > len(merged):
                merged = merged2

    if merged.empty:
        raise RuntimeError(
            "No rows merged between NEA and SWEET-Cat. "
            "Likely key mismatch. We can add another fallback if needed."
        )

    # --- Distance cut (SWEET-Cat distance column is often 'Distance') ---
    if "Distance" in merged.columns:
        dist = pd.to_numeric(merged["Distance"], errors="coerce")
        merged = merged[(dist.isna()) | (dist <= max_distance_pc)].copy()

    # --- Select compact columns for the first real pipeline pass ---
    wanted = [
        # NEA side
        "pl_name", "hostname", "pl_orbper", "pl_rade", "pl_bmassj", "pl_massj",
        "ra", "dec", "sy_dist", "sy_plx",
        # SWEET-Cat side
        "Name", "[Fe/H]", "e[Fe/H]", "Teff", "Logg", "Distance", "SWFlag",
        # join keys
        "gaia_dr3_num", "hostname_norm",
    ]

    keep = [c for c in wanted if c in merged.columns]

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    merged[keep].to_csv(out_csv, index=False)
    print(f"Processed saved: {out_csv}  (rows={len(merged)})")
    print("Columns:", keep)


def main() -> None:
    sweetcat_csv = RAW / "sweetcat.csv"
    nea_csv = RAW / "nea_ps_default_flag_1.csv"
    out_csv = PROCESSED / "sample_planets_real.csv"

    download_csv(SWEETCAT_URL, sweetcat_csv)
    download_csv(NEA_PS_URL, nea_csv)
    build_processed(sweetcat_csv, nea_csv, out_csv)


if __name__ == "__main__":
    main()