# lulab/io/defaults.py
from __future__ import annotations

# -------------------------
# Project-wide defaults
# -------------------------
DEFAULT_TOPIC_ID = "TOP_0001_exoplanet_birth_radius"
DEFAULT_LANG = "en"  # "ru" is also supported

# -------------------------
# Common filenames
# -------------------------
SWEETCAT_RAW = "sweetcat.csv"
NEA_RAW = "nea_ps_default_flag_1.csv"

AGES_GRID_CSV = "sweetcat_ages_grid.csv"
RBIRTH_TOY_CSV = "sweetcat_rbirth_toy.csv"
RBIRTH_GCE_CSV = "sweetcat_rbirth_gce.csv"

# -------------------------
# Physical / sanity limits
# -------------------------
AGE_MIN_GYR = 0.1
AGE_MAX_GYR = 12.0  # hard cut to avoid isochrone grid edge pile-ups

RBIRTH_MIN_KPC = 0.5
RBIRTH_MAX_KPC = 20.0

# Plot-friendly defaults
RBIRTH_PLOT_MAX_KPC = 10.0

# -------------------------
# GCE canonical constants
# -------------------------
R_SUN_KPC = 8.0
T_DISK_GYR = 13.5

FEH_EARLY = -0.65
FEH_TODAY = 0.0
GRAD_EARLY = -0.15
GRAD_TODAY = -0.07

TAU_Z_GYR = 3.0
TAU_G_GYR = 2.0

# -------------------------
# Figure defaults
# -------------------------
FIG_DPI = 200

HIST_BINS_DEFAULT = 30
RBIRTH_HIST_RANGE = (0.0, 10.0)
RBIRTH_HIST_BINS = 60