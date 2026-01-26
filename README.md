# Waller Decomposition
[![DOI](https://zenodo.org/badge/1142184551.svg)](https://doi.org/10.5281/zenodo.18372227)

**Multi-Resolution Wavelet Decomposition for EUR Forecasting in Unconventional Wells**

**Author:** Eric Waller  
**Version:** 3.0  
**License:** All Rights Reserved (see LICENSE)

## Description

The Waller Decomposition is a physics-based wavelet framework for Estimated Ultimate Recovery (EUR) forecasting in multi-stage fractured horizontal wells. The method:

1. Decomposes Rate-Normalized Pressure (RNP) signals via discrete wavelet transform
2. Maps wavelet scales to drainage distances using hydraulic diffusivity
3. Fits decline models to each component independently
4. Reconstructs composite EUR from component contributions
5. Quantifies uncertainty via Bayesian parameter estimation (MCMC)
6. Corrects for parent-child well interference

## Key Results

| Validation | Result |
|------------|--------|
| Wavelet Sensitivity | CV = 1.48% (EUR varies < ±2.2% across 8 wavelet families) |
| Synthetic Validation | ~10% mean error, true EUR within P10-P90 bounds |

## Repository Contents

| File | Description |
|------|-------------|
| `waller_decomposition_v3.md` | Complete technical white paper (Markdown) |
| `wavelet_sensitivity.py` | Wavelet basis sensitivity analysis script |
| `synthetic_validation.py` | Synthetic well validation with Monte Carlo |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Wavelet Sensitivity Analysis

Tests EUR sensitivity across 8 wavelet families (Daubechies, Symlet, Coiflet):

```bash
python wavelet_sensitivity.py
```

**Expected Output:**
```
Wavelet Basis Sensitivity Analysis
==================================================
Wavelet         EUR (MMSCF)     Δ from Baseline
--------------------------------------------------
Daubechies-4    7,100.7         baseline
Daubechies-6    6,992.6         -1.52%
...
--------------------------------------------------
Summary Statistics:
  Mean EUR:     7,054.8 MMSCF
  Std Dev:      104.5 MMSCF
  CV:           1.48%
```

### Synthetic Validation

Runs 100 Monte Carlo realizations on a 3-stage synthetic well:

```bash
python synthetic_validation.py
```

**Expected Output:**
```
Synthetic Validation: Waller Decomposition
============================================================
D.1 Synthetic Well Design
------------------------------------------------------------
True EUR: 5,547 MMSCF

D.3 Monte Carlo Results
------------------------------------------------------------
Mean Estimated EUR       6,127 MMSCF
Mean Error               +10.5%
P10-P90 Range            5,507 - 6,767 MMSCF
```

## Citation

If you use this methodology, please cite:

```
Waller, E. (2026). The Waller Decomposition: Multi-Resolution Wavelet EUR
Forecasting for Multi-Stage Fractured Horizontal Wells. Technical White Paper v3.0.
```

## License

**License:** All Rights Reserved (see LICENSE)
Copyright (c) 2026 Eric Waller. All Rights Reserved.

This work is provided for academic review and personal evaluation only.
Commercial use, redistribution, or derivative works require explicit
written permission from the author.

For licensing inquiries: ewaller.com

## Contact

- Website: [ewaller.com](https://ewaller.com)
- Company: [luxiedge.com](https://luxiedge.com)
