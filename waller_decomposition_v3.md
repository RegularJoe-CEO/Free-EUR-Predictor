# Free EUR Predictor

**Physics-Informed Multi-Scale EUR Forecasting for Unconventional Shale Wells**

**Technical White Paper • Version 3.1**  
**Author:** Eric Waller  
**Date:** June 2026  
**Status:** Production Ready  
**License:** All Rights Reserved (see LICENSE file)

---

## Abstract

The Free EUR Predictor implements a physics-informed framework for forecasting Estimated Ultimate Recovery (EUR) in multi-stage fractured horizontal wells (MFHWs). The method integrates rate-normalized pressure (RNP) analysis derived from Darcy flow principles with multi-scale signal processing to deliver reliable EUR estimates from limited early production data, typically 30 to 45 days.

Unlike conventional decline curve analysis tools that rely heavily on long production histories and empirical fitting, this approach explicitly accounts for the superposition of drainage contributions from multiple fracture stages and the transition between flow regimes. By mapping signal components to characteristic drainage distances using hydraulic diffusivity relationships, the predictor reconstructs composite forecasts with improved early-life accuracy and quantified uncertainty.

This paper details the theoretical foundation, implementation, validation approach, practical usage, and known limitations of the framework. The accompanying open-source repository provides a complete, ready-to-run Python implementation with both command-line and web interfaces.

---

## 1. Introduction

### 1.1 The Practical Problem in Unconventional Development

Petroleum engineers and asset teams routinely face high-stakes decisions based on EUR estimates: whether to drill additional wells in a pad, how to allocate capital across prospects, how to book reserves, and how to evaluate acquisition targets. Traditional tools such as ARIES, Petra, and PhDWin perform adequately once a well has produced for six to twelve months or longer. In the critical early window, however, their forecasts carry large uncertainty because the data has not yet revealed the dominant flow regimes or the full drainage volume.

The Free EUR Predictor was developed specifically to address this early-life forecasting gap while maintaining technical rigor. It does not replace the tools you already use. Instead, it provides an independent, physics-grounded check that becomes available much sooner in the well life.

### 1.2 Core Philosophy

The framework rests on two practical observations from field data and reservoir physics:

1. Production from a multi-stage horizontal well is the superposition of contributions from dozens of individual fracture stages or stage clusters operating at different effective drainage scales.
2. Rate-normalized pressure (RNP) carries information about these different scales that can be extracted and extrapolated using principles from pressure transient analysis and hydraulic diffusivity.

By decomposing the signal, mapping components to physical lengths, fitting each component with a decline model informed by those lengths, and recombining the results, the method produces forecasts that respect the underlying reservoir physics even when production history is short.

---

## 2. Theoretical Foundation

### 2.1 Rate-Normalized Pressure (RNP)

The primary diagnostic variable is RNP, defined as:

RNP(t) = (p_i - p_wf(t)) / q(t)

where p_i is initial reservoir pressure, p_wf(t) is flowing bottomhole pressure at time t, and q(t) is the surface production rate.

RNP has units of pressure per rate and is directly analogous to the pressure transient solution for a producing well. In the linear flow regime common in shale wells, RNP plotted against square root of time yields a straight line whose slope relates to fracture surface area and reservoir properties. The Free EUR Predictor uses RNP as the base signal for decomposition because it normalizes out rate variations and highlights reservoir-controlled behavior.

### 2.2 Multi-Phase Handling

For wells producing oil, gas, and water, RNP is computed separately for each phase while tracking producing ratios (GOR, WOR) for consistency. Each phase is analyzed independently and then coupled through material balance and economic limit constraints.

### 2.3 Multi-Scale Decomposition

The method applies discrete wavelet transform (DWT) to the RNP signal (or its logarithm for stability) using the Daubechies-4 wavelet as the default basis. This decomposition separates the signal into approximation (low-frequency, longer-term drainage) and detail (higher-frequency, shorter-term) components at multiple resolution levels.

Each wavelet level corresponds approximately to a characteristic time scale τ_j ≈ 2^j × sampling interval. Using the hydraulic diffusivity equation ∂p/∂t = η ∇²p, these time scales are mapped to drainage distances via the radius of investigation approximation r_j ≈ C_eff × √τ_j, where C_eff is a basin-specific constant calibrated from analog wells.

### 2.4 Decline Fitting per Scale

Each extracted component is fitted with a generalized power-law decline of the form:

q(t) = qi / (1 + b Di t)^(1/b)

or an equivalent power-law form. Fitting is performed independently per component, allowing different decline characteristics for near-wellbore fracture-dominated flow versus far-field matrix contribution.

### 2.5 Uncertainty Quantification

Bayesian methods (Markov Chain Monte Carlo via emcee) are used to sample the posterior distributions of decline parameters rather than relying on point estimates. These samples are propagated through the EUR integration to produce full P10 / P50 / P90 distributions.

### 2.6 Parent-Child and Interference Corrections

A depletion factor based on distance to parent wells and their production history is applied to adjust initial pressure or EUR directly. The correction is optional and configurable.

---

## 3. Practical Implementation and Usage

The tool is provided as a complete Python package with two primary interfaces:

**Web Application (Recommended for most users)**  
Run `streamlit run app.py` to open a browser-based interface. Upload your production CSV, select basin parameters, and click Run Forecast. Results appear immediately with plots and downloadable Excel files.

**Command Line Interface**  
`python run_example.py your_data.csv --days 45 --basin permian_wolfcamp`

**Input Data Requirements**  
- Time series with at least 30 days of production (daily or monthly)
- Columns typically include: days (or date), oil_bbl, gas_mcf, water_bbl, and optionally p_wf_psi
- Sample file provided as reference

**Outputs**  
- Excel file with daily forecasts, cumulative volumes, ratios, and P10/P50/P90 EUR values
- Diagnostic plots (rate vs time, RNP, wavelet components, uncertainty bands)
- Log file with warnings and parameter summaries

---

## 4. Validation Approach

The framework has been tested on:
- Synthetic wells with known analytical EUR constructed from superposed stage contributions
- Field data from Permian Wolfcamp A wells with longer production histories for hindcasting
- Cross-validation against analog mature wells in multiple basins

Results consistently show tighter uncertainty bands and reduced bias in early-time forecasts compared to pure empirical Arps or Duong models when sufficient pressure data is available.

---

## 5. Limitations and Best Practices

This tool performs best when:
- Quality bottomhole pressure data (or reliable estimates) is available
- Production data has reasonable regularity (daily or consistent monthly)
- The well is in a basin where calibration constants have been established

It is not intended as a black-box replacement for full reservoir simulation or detailed history matching. Engineers should always cross-check results against their existing workflows and domain knowledge, particularly in areas with extreme parent-child interference or operational upsets.

Users are encouraged to calibrate C_eff values for their specific operating area using mature analog wells.

---

## 6. Conclusion

The Free EUR Predictor offers petroleum engineers a practical, technically grounded method for obtaining reliable EUR estimates much earlier in the well life than was previously possible with standard industry tools. By combining wavelet-based multi-scale analysis with Darcy-derived physical mapping and Bayesian uncertainty quantification, it provides an independent physics-informed perspective that complements rather than replaces your existing software stack.

The complete source code, sample data, and usage examples are available in the public repository. Feedback from practicing engineers is welcome and will be used to refine future versions.

**Repository:** https://github.com/RegularJoe-CEO/Free-EUR-Predictor

---

**© 2026 Eric Waller. All Rights Reserved.**
