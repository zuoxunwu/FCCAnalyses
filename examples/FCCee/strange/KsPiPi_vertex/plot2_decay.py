#!/usr/bin/env python3

import os
import numpy as np
import uproot
import awkward as ak
import matplotlib.pyplot as plt

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

outdir = "plots/plot2_decay"
os.makedirs(outdir, exist_ok=True)

# -------------------------
# Branches to load
# -------------------------
branches = [
    "genKS_Vertex_d", "genKS_Vertex_p",
    "genLm_Vertex_d", "genLm_Vertex_p",
]

# -------------------------
# Loop over samples
# -------------------------
for tag, fname in samples.items():
    root_file = os.path.join(input_dir, fname)
    print(f"\n=== Processing sample {tag}: {root_file} ===")

    if not os.path.exists(root_file):
        print(f"  WARNING: file not found, skipping: {root_file}")
        continue

    # Read ROOT file
    with uproot.open(root_file) as f:
        if tree_name not in f:
            print(f"  WARNING: TTree '{tree_name}' not found in {root_file}, skipping.")
            continue

        tree = f[tree_name]
        available = set(tree.keys())
        branches_to_read = [b for b in branches if b in available]

        if not branches_to_read:
            print("  WARNING: none of the requested branches found, skipping sample.")
            continue

        arrays = tree.arrays(branches_to_read, library="ak")

    def get_vals(name):
        """Flatten awkward → numpy and keep finite values."""
        if name not in arrays.fields:
            return np.array([], dtype=float)
        vals = ak.to_numpy(ak.flatten(arrays[name], axis=None))
        return vals[np.isfinite(vals)]

    # Extract variables
    ks_d = get_vals("genKS_Vertex_d")
    lm_d = get_vals("genLm_Vertex_d")
    ks_p = get_vals("genKS_Vertex_p")
    lm_p = get_vals("genLm_Vertex_p")

    # ============================================================
    # 1) Overlay: flight distance d (K_S and Lambda), log y
    # ============================================================
    if ks_d.size > 0 or lm_d.size > 0:
        plt.figure(figsize=(7, 5))

        d_min, d_max = 0.0, 8000.0
        bins_d = np.linspace(d_min, d_max, 200)

        if ks_d.size > 0:
            mean_ks_d = ks_d.mean()
            plt.hist(
                ks_d,
                bins=bins_d,
                histtype="step",
                linewidth=1.7,
                color="blue",
                label=rf"$K_S$: mean flight distance = {mean_ks_d:.2f} mm",
            )

        if lm_d.size > 0:
            mean_lm_d = lm_d.mean()
            plt.hist(
                lm_d,
                bins=bins_d,
                histtype="step",
                linewidth=1.7,
                color="red",
                label=rf"$\Lambda$: mean flight distance = {mean_lm_d:.2f} mm",
            )

        plt.xlabel(r"Flight distance $d$ (mm)")
        plt.ylabel("Counts")
        plt.yscale("log")
        plt.xlim(d_min, d_max)
        plt.title(r"Flight distance of $K_S$ and $\Lambda$")
        plt.legend()
        plt.tight_layout()

        out_d = os.path.join(outdir, f"hist1d_genKS_Lm_d_{tag}.png")
        plt.savefig(out_d, dpi=170)
        plt.close()
        print(f"  Saved {out_d}")
    else:
        print("  Warning: no entries for K_S or Lambda flight distance d")

    # ============================================================
    # 2) Overlay: momentum p (K_S and Lambda) — now with MEAN in legend
    # ============================================================
    if ks_p.size > 0 or lm_p.size > 0:
        plt.figure(figsize=(7, 5))

        # common binning from combined non-empty arrays
        nonempty_p = [v for v in [ks_p, lm_p] if v.size > 0]
        all_p = np.concatenate(nonempty_p) if nonempty_p else np.array([0.0])
        p_min = 0.0
        p_max = all_p.max() if all_p.size > 0 else 1.0
        bins_p = np.linspace(p_min, p_max, 200)

        if ks_p.size > 0:
            mean_ks_p = ks_p.mean()
            plt.hist(
                ks_p,
                bins=bins_p,
                histtype="step",
                linewidth=1.7,
                color="blue",
                label=rf"$K_S$: mean $p$ = {mean_ks_p:.2f} GeV",
            )

        if lm_p.size > 0:
            mean_lm_p = lm_p.mean()
            plt.hist(
                lm_p,
                bins=bins_p,
                histtype="step",
                linewidth=1.7,
                color="red",
                label=rf"$\Lambda$: mean $p$ = {mean_lm_p:.2f} GeV",
            )

        plt.xlabel(r"Vertex momentum $p$ (GeV)")
        plt.ylabel("Counts")
        plt.title(r"Momentum of $K_S$ and $\Lambda$ vertices")
        plt.legend()
        plt.tight_layout()

        out_p = os.path.join(outdir, f"hist1d_genKS_Lm_p_{tag}.png")
        plt.savefig(out_p, dpi=170)
        plt.close()
        print(f"  Saved {out_p}")
    else:
        print("  Warning: no entries for momentum p")

