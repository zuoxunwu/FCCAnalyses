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

outdir = "plots/plot1_multiplicity"
os.makedirs(outdir, exist_ok=True)

# -------------------------
# Branches to read (if present)
# -------------------------
branches_wanted = [
    "n_genKLs", "n_genKSs",
    "n_genKposs", "n_genKnegs",
    "n_genPhis", "n_genLambdas",
    "n_genPipms",
    "n_genSigma0s", "n_genSigmaposs", "n_genSigmanegs",
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

    with uproot.open(root_file) as f:
        if tree_name not in f:
            print(f"  WARNING: TTree '{tree_name}' not found in {root_file}, skipping.")
            continue

        tree = f[tree_name]

        # Only read branches that actually exist in the tree
        available = set(tree.keys())
        branches = [b for b in branches_wanted if b in available]
        if "n_genPipms" not in branches:
            print("  WARNING: n_genPipms not found, skipping sample.")
            continue

        arrays = tree.arrays(branches, library="ak")

    def get_vals(name):
        """Flatten awkward → numpy and keep finite values. Return empty if missing."""
        if name not in arrays.fields:
            return np.array([], dtype=float)
        vals = ak.to_numpy(ak.flatten(arrays[name], axis=None))
        return vals[np.isfinite(vals)]

    # =================================================================
    # 1) π± multiplicity histogram — natural x-range, integer binning
    # =================================================================
    vals_pipm = get_vals("n_genPipms")
    if vals_pipm.size == 0:
        print("  WARNING: n_genPipms empty, skipping π± plot.")
    else:
        mean_pipm = vals_pipm.mean()

        vmin = int(np.floor(vals_pipm.min()))
        vmax = int(np.ceil(vals_pipm.max()))
        bins_pipm = np.arange(vmin, vmax + 2, 1)  # integer edges

        plt.figure(figsize=(6, 4))
        plt.hist(
            vals_pipm,
            bins=bins_pipm,
            histtype="step",
            linewidth=1.8,
            color="red",
            label=rf"$\pi^\pm$: mean yield = {mean_pipm:.2f}",
        )
        plt.xlabel(r"$n_{\pi^\pm}$")
        plt.ylabel("Counts")
        plt.legend()
        plt.tight_layout()
        out_pipm = os.path.join(outdir, f"hist_n_genPipms_{tag}.png")
        plt.savefig(out_pipm, dpi=150)
        plt.close()
        print(f"  Saved {out_pipm}")

    # =================================================================
    # 2) K and Σ hadron multiplicity overlay
    # =================================================================

    # Integer bin edges 0..8 for all multiplicities
    bins_all = np.arange(0, 9, 1)
    x_step = bins_all[:-1]  # left edges for step(where="post")

    # label -> (branch name(s), color)
    species = {
        r"K_L"        : ("n_genKLs",                          "red"),
        r"K_S"        : ("n_genKSs",                          "orange"),
        r"K^\pm"      : (["n_genKposs", "n_genKnegs"],        "black"),
        r"\Phi"       : ("n_genPhis",                        "blue"),
        r"\Lambda"    : ("n_genLambdas",                     "green"),
        r"\Sigma^0"   : ("n_genSigma0s",                     "purple"),
        r"\Sigma^\pm" : (["n_genSigmaposs", "n_genSigmanegs"], "brown"),
    }

    plt.figure(figsize=(8, 6))

    any_drawn = False

    for label, (branch, color) in species.items():

        # Single-branch species
        if isinstance(branch, str):
            vals = get_vals(branch)
            if vals.size == 0:
                print(f"  Note: {branch} missing or empty in {tag}, skipping.")
                continue
            hist, _ = np.histogram(vals, bins=bins_all)
            mean_yield = vals.mean()

        # ± species: sum histograms of the two branches
        else:
            vals_list = [get_vals(b) for b in branch]
            if all(v.size == 0 for v in vals_list):
                print(f"  Note: {branch} (±) missing or empty in {tag}, skipping.")
                continue

            hists = []
            mean_yield = 0.0
            for v in vals_list:
                if v.size > 0:
                    hists.append(np.histogram(v, bins=bins_all)[0])
                    mean_yield += v.mean()

            if not hists:
                continue

            hist = np.sum(hists, axis=0)

        plt.step(
            x_step, hist,
            where="post",
            color=color,
            label=rf"${label}$: mean yield = {mean_yield:.2f}",
        )
        any_drawn = True

    if any_drawn:
        plt.xlabel("Generated multiplicity")
        plt.ylabel("Counts")
        plt.xlim(0, 8)
        plt.ylim(0,200000)
        plt.legend()
        plt.tight_layout()
        out_multi = os.path.join(outdir, f"hist_genK_Sigma_multiplicities_{tag}.png")
        plt.savefig(out_multi, dpi=150)
        plt.close()
        print(f"  Saved {out_multi}")
    else:
        plt.close()
        print("  WARNING: no K/Σ species found to draw in overlay plot.")

