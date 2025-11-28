#!/usr/bin/env python3

import os
import numpy as np
import uproot
import awkward as ak
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -------------------------
# Samples and input / output paths
# -------------------------
samples = {
    "Zss": "p8_ee_Zss_ecm91.root",
    "Zcc": "p8_ee_Zcc_ecm91.root",
    "Zbb": "p8_ee_Zbb_ecm91.root",
    "Zud": "p8_ee_Zud_ecm91.root",
}

input_dir = "outputs/strange/analysis_stage1_1118"
tree_name = "events"

outdir = "plots/plot4_massres"
os.makedirs(outdir, exist_ok=True)

# -------------------------
# Branches to read
# -------------------------
branches_needed = [
    "Vertex_mass",
    # Ks regional masses
    "recoKS_Vertex_mass_before_VerDet",
    "recoKS_Vertex_mass_within_VerDet",
    "recoKS_Vertex_mass_beyond_VerDet",
    # Lambda regional masses
    "recoLm_Vertex_mass_before_VerDet",
    "recoLm_Vertex_mass_within_VerDet",
    "recoLm_Vertex_mass_beyond_VerDet",
]

# -------------------------
# Double-sided Crystal Ball + constant background
# -------------------------
def dscb_const(x, N, mu, sigma, alphaL, nL, alphaR, nR, C):
    """
    Double-sided Crystal Ball + constant background.
    """
    t = (x - mu) / sigma

    abs_aL = np.abs(alphaL)
    abs_aR = np.abs(alphaR)

    # Left tail constants
    AL = (nL / abs_aL) ** nL * np.exp(-0.5 * abs_aL**2)
    BL = nL / abs_aL - abs_aL

    # Right tail constants
    AR = (nR / abs_aR) ** nR * np.exp(-0.5 * abs_aR**2)
    BR = nR / abs_aR - abs_aR

    y = np.empty_like(x, dtype=float)

    core = (t > -alphaL) & (t < alphaR)
    left = t <= -alphaL
    right = t >= alphaR

    y[core] = np.exp(-0.5 * t[core] ** 2)
    y[left] = AL * (BL - t[left]) ** (-nL)
    y[right] = AR * (BR + t[right]) ** (-nR)

    return N * y + C

# -------------------------
# Helper: flatten awkward → numpy, finite only
# -------------------------
def flatten_vals(arrays, name):
    if name not in arrays.fields:
        return np.array([], dtype=float)
    vals = ak.to_numpy(ak.flatten(arrays[name], axis=None))
    return vals[np.isfinite(vals)]

# -------------------------
# Helper: multi-branch zoomed hist + DSCB fits (overlay)
# -------------------------
def make_multi_zoom_and_fit(branch_vals_dict, m_min, m_max, nbins, outfile, title):
    """
    branch_vals_dict: { label: (vals_array, color) }
    """

    import matplotlib.colors as mc

    def lighten(color, amount=0.45):
        """Brighten a color by mixing with white."""
        c = mc.to_rgb(color)
        r = c[0] + (1 - c[0]) * amount
        g = c[1] + (1 - c[1]) * amount
        b = c[2] + (1 - c[2]) * amount
        return (r, g, b)

    plt.figure(figsize=(7, 5))
    any_drawn = False

    for label, (vals, color) in branch_vals_dict.items():
        vals = vals[(vals >= m_min) & (vals <= m_max)]
        if vals.size == 0:
            continue

        counts, edges = np.histogram(vals, bins=nbins, range=(m_min, m_max))
        centers = 0.5 * (edges[:-1] + edges[1:])

        # Fit initial guesses
        A0 = counts.max()
        mu0 = centers[np.argmax(counts)]
        sigma0 = (m_max - m_min) / 20.0
        C0 = np.median(counts)
        p0 = [A0, mu0, sigma0, 1.5, 3.0, 1.5, 3.0, C0]

        bounds = (
            [0.0, m_min, 1e-5, 0.01, 1.01, 0.01, 1.01, 0.0],
            [np.inf, m_max, (m_max - m_min), 10.0, 50.0, 10.0, 50.0, np.inf],
        )

        try:
            popt, pcov = curve_fit(
                dscb_const,
                centers,
                counts,
                p0=p0,
                bounds=bounds,
                maxfev=50000,
            )
        except Exception as e:
            print(f"  Fit failed for {label}: {e}")
            popt = None

        # -----------------------------
        # Histogram → thicker
        # -----------------------------
        plt.hist(
            vals,
            bins=nbins,
            range=(m_min, m_max),
            histtype="step",
            linewidth=3.0,   # <<< THICKER HISTOGRAM LINE
            color=color,
        )

        # -----------------------------
        # Fit → thicker, brightened for contrast
        # -----------------------------
        if popt is not None:
            N, mu, sigma, alphaL, nL, alphaR, nR, C = popt
            xfit = np.linspace(m_min, m_max, 1200)
            yfit = dscb_const(xfit, *popt)

            fit_color = lighten(color, amount=0.45)

            plt.plot(
                xfit,
                yfit,
                color=fit_color,
                linewidth=2.0,   # <<< THICKER FIT LINE
                label=(
                    rf"{label}: "
                    rf"$\mu={mu:.4f}$ GeV, "
                    rf"$\sigma={sigma*1000:.1f}$ MeV"
                ),
            )
        else:
            plt.plot([], [], color=color, label=f"{label}: fit failed")

        any_drawn = True

    if not any_drawn:
        plt.close()
        print(f"  Warning: no entries to plot for {title}")
        return

    plt.xlabel("Reconstructed mass m (GeV)")
    plt.ylabel("Counts")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outfile, dpi=170)
    plt.close()
    print(f"  Saved {outfile}")


# -------------------------
# Main loop over samples
# -------------------------
for tag, fname in samples.items():
    root_file = os.path.join(input_dir, fname)
    print(f"\n=== Processing sample {tag}: {root_file} ===")

    if not os.path.exists(root_file):
        print(f"  WARNING: file not found, skipping this sample.")
        continue

    with uproot.open(root_file) as f:
        if tree_name not in f:
            print(f"  WARNING: TTree '{tree_name}' not found, skipping this sample.")
            continue

        tree = f[tree_name]
        available = set(tree.keys())
        to_read = [b for b in branches_needed if b in available]
        if not to_read:
            print("  WARNING: none of the requested mass branches found, skipping.")
            continue

        arrays = tree.arrays(to_read, library="ak")

    # ----------------------------------------------------------
    # 1) Full mass spectrum: Vertex_mass (log y)
    # ----------------------------------------------------------
    vals_full = flatten_vals(arrays, "Vertex_mass")

    if vals_full.size > 0:
        plt.figure(figsize=(7, 5))

        plt.hist(
            vals_full,
            bins=1400,
            range=(0.0, 1.4),
            histtype="step",
            linewidth=1.5,
            color="black",
        )

        plt.yscale("log")
        plt.ylim(1, None)

        plt.xlabel("Reconstructed vertex mass (GeV)")
        plt.ylabel("Counts (log)")
        plt.title(f"Full vertex mass spectrum (Vertex_mass), {tag}")

        plt.tight_layout()
        outfile_full = os.path.join(outdir, f"mass_full_{tag}.png")
        plt.savefig(outfile_full, dpi=170)
        plt.close()
        print(f"  Saved {outfile_full}")
    else:
        print("  WARNING: Vertex_mass empty or missing for this sample")

    # ----------------------------------------------------------
    # 2) K_S peak: three regions overlaid
    #    recoKS_Vertex_mass_before/within/beyond_VerDet
    # ----------------------------------------------------------
    ks_before = flatten_vals(arrays, "recoKS_Vertex_mass_before_VerDet")
    ks_within = flatten_vals(arrays, "recoKS_Vertex_mass_within_VerDet")
    ks_beyond = flatten_vals(arrays, "recoKS_Vertex_mass_beyond_VerDet")

    ks_dict = {
        r"$K_S$ before VDet": (ks_before, "tab:blue"),
        r"$K_S$ within VDet": (ks_within, "tab:green"),
        r"$K_S$ beyond VDet": (ks_beyond, "tab:red"),
    }

    if any(v[0].size > 0 for v in ks_dict.values()):
        outfile_ks = os.path.join(outdir, f"Ks_peak_regions_DSCB_{tag}.png")
        make_multi_zoom_and_fit(
            ks_dict,
            m_min=0.49,
            m_max=0.51,
            nbins=200,
            outfile=outfile_ks,
            title=rf"$K_S$ mass peak by region, {tag}",
        )
    else:
        print("  WARNING: no recoKS regional masses present for this sample")

    # ----------------------------------------------------------
    # 3) Lambda peak: three regions overlaid
    #    recoLm_Vertex_mass_before/within/beyond_VerDet
    # ----------------------------------------------------------
    lm_before = flatten_vals(arrays, "recoLm_Vertex_mass_before_VerDet")
    lm_within = flatten_vals(arrays, "recoLm_Vertex_mass_within_VerDet")
    lm_beyond = flatten_vals(arrays, "recoLm_Vertex_mass_beyond_VerDet")

    lm_dict = {
        r"$\Lambda$ before VDet": (lm_before, "tab:blue"),
        r"$\Lambda$ within VDet": (lm_within, "tab:green"),
        r"$\Lambda$ beyond VDet": (lm_beyond, "tab:red"),
    }

    if any(v[0].size > 0 for v in lm_dict.values()):
        outfile_lm = os.path.join(outdir, f"Lambda_peak_regions_DSCB_{tag}.png")
        make_multi_zoom_and_fit(
            lm_dict,
            m_min=1.11,
            m_max=1.12,
            nbins=200,
            outfile=outfile_lm,
            title=rf"$\Lambda$ mass peak by region, {tag}",
        )
    else:
        print("  WARNING: no recoLm regional masses present for this sample")

