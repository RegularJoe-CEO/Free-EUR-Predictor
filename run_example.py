"""
run_example.py - Waller Decomposition EUR Forecast
Usage: python3 run_example.py sample_well.csv
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

N_SAMPLES = 500
ECON_LIMIT_GAS = 50
ECON_LIMIT_OIL = 5
ECON_LIMIT_WATER = 10
T_MAX = 1800

def load_data(filepath):
    df = pd.read_csv(filepath)
    if "days" not in df.columns:
        raise ValueError("Missing column: days")
    
    data = {"days": df["days"].values}
    well_type = None
    
    if "rate_mscfd" in df.columns:
        data["gas"] = df["rate_mscfd"].values
        well_type = "gas"
    if "rate_bblpd" in df.columns:
        data["oil"] = df["rate_bblpd"].values
        well_type = "oil"
    if "rate_bwpd" in df.columns:
        data["water"] = df["rate_bwpd"].values
    if "pressure_psi" in df.columns:
        data["pressure"] = df["pressure_psi"].values
    
    if "gas" not in data and "oil" not in data:
        raise ValueError("Need rate_mscfd (gas) or rate_bblpd (oil)")
    
    if "gas" in data and "oil" in data:
        well_type = "both"
    
    return data, well_type

def power_law_decline(t, qi, D, n):
    return qi * (1 + D * t) ** (-n)

def fit_decline(t, rate):
    try:
        popt, pcov = curve_fit(power_law_decline, t, rate, p0=[rate[0], 0.01, 0.8],
            bounds=([0, 0.0001, 0.1], [rate[0]*3, 0.5, 2.0]), maxfev=5000)
        perr = np.sqrt(np.diag(pcov))
        return popt, perr
    except:
        return [rate[0], 0.01, 0.8], [rate[0]*0.1, 0.005, 0.1]

def forecast_phase(t, rate, econ_limit, n_samples=500, t_max=1800):
    params, errors = fit_decline(t, rate)
    qi, D, n = params
    qi_err = max(errors[0], qi * 0.05)
    D_err = max(errors[1], D * 0.10)
    n_err = max(errors[2], n * 0.05)
    
    t_forecast = np.linspace(1, t_max, 1000)
    eur_samples = []
    
    for _ in range(n_samples):
        qi_s = max(qi + qi_err * np.random.randn(), 10)
        D_s = np.clip(D + D_err * np.random.randn(), 0.001, 0.5)
        n_s = np.clip(n + n_err * np.random.randn(), 0.1, 2.0)
        q_forecast = power_law_decline(t_forecast, qi_s, D_s, n_s)
        q_forecast = np.where(q_forecast >= econ_limit, q_forecast, 0)
        eur_samples.append(np.trapz(q_forecast, t_forecast) / 1000)
    
    p10, p50, p90 = np.percentile(eur_samples, [10, 50, 90])
    q_p50 = power_law_decline(t_forecast, *params)
    q_p50 = np.where(q_p50 >= econ_limit, q_p50, 0)
    
    return {"p10": p10, "p50": p50, "p90": p90, "params": params, "t": t_forecast, "q": q_p50}

def main(filepath):
    print(f"Loading: {filepath}")
    data, well_type = load_data(filepath)
    t = data["days"]
    print(f"  {len(t)} data points, {t[-1]:.0f} days")
    
    results = {}
    
    if "gas" in data:
        print("  Forecasting gas...")
        results["gas"] = forecast_phase(t, data["gas"], ECON_LIMIT_GAS, N_SAMPLES, T_MAX)
    
    if "oil" in data:
        print("  Forecasting oil...")
        results["oil"] = forecast_phase(t, data["oil"], ECON_LIMIT_OIL, N_SAMPLES, T_MAX)
    
    if "water" in data:
        print("  Forecasting water...")
        results["water"] = forecast_phase(t, data["water"], ECON_LIMIT_WATER, N_SAMPLES, T_MAX)
    
    print("")
    print("=" * 50)
    print("EUR FORECAST")
    print("=" * 50)
    
    if "gas" in results:
        r = results["gas"]
        print(f"  Gas (MMSCF):   P10={r['p10']:>7.1f}  P50={r['p50']:>7.1f}  P90={r['p90']:>7.1f}")
    
    if "oil" in results:
        r = results["oil"]
        print(f"  Oil (MBO):     P10={r['p10']:>7.1f}  P50={r['p50']:>7.1f}  P90={r['p90']:>7.1f}")
    
    if "water" in results:
        r = results["water"]
        print(f"  Water (MBW):   P10={r['p10']:>7.1f}  P50={r['p50']:>7.1f}  P90={r['p90']:>7.1f}")
    
    print("=" * 50)
    
    if "gas" in data and "oil" in data:
        gor = data["gas"] / np.where(data["oil"] > 0, data["oil"], 0.001)
        print(f"\nGOR: Initial={gor[0]:.0f}  Current={gor[-1]:.0f} scf/bbl")
    
    if "water" in data and "oil" in data:
        wor = data["water"] / np.where(data["oil"] > 0, data["oil"], 0.001)
        print(f"WOR: Initial={wor[0]:.1f}  Current={wor[-1]:.1f} bbl/bbl")
    
    if "water" in data and "gas" in data and "oil" not in data:
        wgr = data["water"] / np.where(data["gas"] > 0, data["gas"], 0.001) * 1000
        print(f"WGR: Initial={wgr[0]:.1f}  Current={wgr[-1]:.1f} bbl/MMscf")
    
    n_plots = len(results)
    fig, axes = plt.subplots(1, n_plots, figsize=(5*n_plots, 5), dpi=150)
    if n_plots == 1:
        axes = [axes]
    
    colors = {"gas": "red", "oil": "green", "water": "blue"}
    units = {"gas": "MSCF/d", "oil": "bbl/d", "water": "bwpd"}
    eur_units = {"gas": "MMSCF", "oil": "MBO", "water": "MBW"}
    
    for i, phase in enumerate(results.keys()):
        ax = axes[i]
        r = results[phase]
        ax.scatter(t, data[phase], s=30, color="black", alpha=0.7, label="Observed")
        ax.plot(r["t"], r["q"], color=colors[phase], linewidth=2, label="P50 Forecast")
        ax.axvline(x=t[-1], color="gray", linestyle=":", linewidth=1)
        ax.set_xlabel("Time (days)")
        ax.set_ylabel(f"{phase.capitalize()} ({units[phase]})")
        ax.set_title(f"{phase.capitalize()} EUR: {r['p50']:.1f} {eur_units[phase]}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, T_MAX)
        ax.set_ylim(0, None)
    
    plt.tight_layout()
    plt.savefig("forecast_output.png", dpi=150)
    print("\nSaved: forecast_output.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_example.py <your_well.csv>")
        sys.exit(1)
    main(sys.argv[1])