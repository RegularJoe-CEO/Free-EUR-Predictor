# Free EUR Predictor

**Scientifically superior physics-first tool** for Estimated Ultimate Recovery (EUR) forecasting in unconventional shale wells.

## Why It Dominates Legacy Tools
Traditional software like ARIES, Petra, and PhDWin typically requires 6–12 months of production history before delivering reliable EUR estimates.

**This tool provides accurate, high-confidence forecasts much earlier** — often from just the first 30–45 days of data — while remaining grounded in real reservoir physics.

Key technical advantages:
- Multi-resolution wavelet decomposition to separate fracture and matrix flow regimes
- Rate-normalized pressure (RNP) mapping grounded in Darcy flow principles
- Probabilistic outputs with uncertainty quantification
- Flowback-aware early-data conditioning

This delivers **orders-of-magnitude better early-life intelligence** for drilling, completion, and acquisition decisions.

## Quick Start (One-Button Easy)

**Recommended: Web App (Simple Button Interface)**
```bash
git clone https://github.com/RegularJoe-CEO/Free-EUR-Predictor.git
cd Free-EUR-Predictor
pip install -r requirements.txt
streamlit run app.py
→ Browser opens with "Upload Your Production CSV" + big "Run Forecast" button.
CLI Alternative
Bashpython run_example.py sample_well.csv --days 45
Outputs are saved to the outputs/ folder:

Excel file with P10/P50/P90 EUR values and full rate curves
Professional forecast plot (PNG)

Easy to copy results directly into Petra, ARIES, or Excel.
Using Your Own Data
Drop in a CSV file using columns such as days, oil_bbl, gas_mcf, water_bbl (see  as a template). The tool handles multi-phase data and provides clear warnings if data quality needs attention.
Technical Details
Full methodology, equations (wavelet decomposition + Darcy-based RNP mapping), validation on the Permian Wolfcamp A sample, and known limitations are documented in waller_decomposition_v3.md.
Requirements (Lightweight & Cheap)

Python 3.8+
pandas, numpy, scipy, pywavelets, streamlit
No GPU required for standard runs
