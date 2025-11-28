#!/usr/bin/env python3

import os
import numpy as np
import uproot
import awkward as ak
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

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

outdir = "plots/plot3_vertexreco"
os.makedirs(outdir, exist_ok=True)

# -------------------------
# Branches needed
# -------------------------
branches_needed = [
    "genKS_Vertex_z", "genKS_Vertex_r",
    "genLm_Vertex_z", "genLm_Vertex_r",
    "recoKS_Vertex_z", "recoKS_Vertex_r",
    "recoLm_Vertex_z", "recoLm_Vertex_r",
]

# -------------------------
# Common binning for ALL histograms
# -------------------------
zmin, zmax = 0.0, 5500.0
rmin, rmax = 0.0, 5500.0
nbins = 200

bins_z = np.linspace(zmin, zmax, nbins + 1)
bins_r = np.linspace(rmin, rmax, nbins + 1)

# -------------------------
# Helper: flatten awkward → numpy, finite only
# -------------------------
def flatten_vals(arrays, name):
    if name not in arrays.fields:
        return np.array([], dtype=float)
    vals = ak.to_numpy(ak.flatten(arrays[name], axis=None))
    return vals[np.isfinite(vals)]

# -------------------------
# Main loop over samples
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
        branches_to_read = [b for b in branches_needed if b in available]

        if not branches_to_read:
            print("  WARNING: none of the needed branches found, skipping.")
            continue

        arrays = tree.arrays(branches_to_read, library="ak")

    # Extract gen & reco for K_S and Lambda
    ks_z_gen = flatten_vals(arrays, "genKS_Vertex_z")
    ks_r_gen = flatten_vals(arrays, "genKS_Vertex_r")
    lm_z_gen = flatten_vals(arrays, "genLm_Vertex_z")
    lm_r_gen = flatten_vals(arrays, "genLm_Vertex_r")

    ks_z_reco = flatten_vals(arrays, "recoKS_Vertex_z")
    ks_r_reco = flatten_vals(arrays, "recoKS_Vertex_r")
    lm_z_reco = flatten_vals(arrays, "recoLm_Vertex_z")
    lm_r_reco = flatten_vals(arrays, "recoLm_Vertex_r")

    # Helper function to do gen/reco/efficiency histograms & plots
    def make_gen_reco_eff_plots(
        z_gen, r_gen, z_reco, r_reco,
        label_tex, tag, basename
    ):
        """Make gen/reco 2D histograms and efficiency map reco/gen."""

        # Need at least some gen entries, otherwise nothing to normalize to
        if z_gen.size == 0 or r_gen.size == 0:
            print(f"  WARNING: no gen {basename} entries in this sample")
            return

        # 2D histograms with *common* binning
        H_gen, _, _ = np.histogram2d(
            z_gen, r_gen, bins=[bins_z, bins_r]
        )
        H_reco = np.zeros_like(H_gen)
        if z_reco.size > 0 and r_reco.size > 0:
            H_reco, _, _ = np.histogram2d(
                z_reco, r_reco, bins=[bins_z, bins_r]
            )

        # ---------------- Gen plot ----------------
        H_gen_plot = H_gen.copy()
        H_gen_plot[H_gen_plot == 0] = np.nan  # avoid log(0)

        plt.figure(figsize=(8, 7))
        plt.pcolormesh(
            bins_z, bins_r, H_gen_plot.T,
            norm=LogNorm(),
            cmap="viridis",
            shading="auto",
        )
        cbar = plt.colorbar()
        cbar.set_label("Counts (log scale)")

        plt.xlabel(rf"$z_{{{label_tex}}}^{{\mathrm{{gen}}}}$ decay position [mm]")
        plt.ylabel(rf"$r_{{{label_tex}}}^{{\mathrm{{gen}}}}$ decay position [mm]")
        plt.title(rf"Generated {label_tex} decay position in $(z, r)$, {tag}")
        plt.tight_layout()

        out_gen = os.path.join(outdir, f"hist2d_gen{basename}_z_vs_r_{tag}.png")
        plt.savefig(out_gen, dpi=170)
        plt.close()
        print(f"  Saved {out_gen}")

        # ---------------- Reco plot ----------------
        if np.all(H_reco == 0):
            print(f"  WARNING: no reco {basename} entries in this sample")
        else:
            H_reco_plot = H_reco.copy()
            H_reco_plot[H_reco_plot == 0] = np.nan

            plt.figure(figsize=(8, 7))
            plt.pcolormesh(
                bins_z, bins_r, H_reco_plot.T,
                norm=LogNorm(),
                cmap="cividis",
                shading="auto",
            )
            cbar = plt.colorbar()
            cbar.set_label("Counts (log scale)")

            plt.xlabel(rf"$z_{{{label_tex}}}^{{\mathrm{{reco}}}}$ decay position [mm]")
            plt.ylabel(rf"$r_{{{label_tex}}}^{{\mathrm{{reco}}}}$ decay position [mm]")
            plt.title(rf"Reconstructed {label_tex} decay position in $(z, r)$, {tag}")
            plt.tight_layout()

            out_reco = os.path.join(outdir, f"hist2d_reco{basename}_z_vs_r_{tag}.png")
            plt.savefig(out_reco, dpi=170)
            plt.close()
            print(f"  Saved {out_reco}")

        # ---------------- Efficiency plot reco/gen ----------------
        # Efficiency = H_reco / H_gen, with safe division
        with np.errstate(divide="ignore", invalid="ignore"):
            eff = np.divide(
                H_reco,
                H_gen,
                out=np.zeros_like(H_reco, dtype=float),
                where=H_gen > 0,
            )

        # Mask bins where there was no generated entry
        eff_masked = np.ma.array(eff, mask=(H_gen == 0))

        plt.figure(figsize=(8, 7))
        im = plt.pcolormesh(
            bins_z, bins_r, eff_masked.T,
            vmin=0.0,
            vmax=1.0,
            cmap="viridis",
            shading="auto",
        )
        cbar = plt.colorbar(im)
        cbar.set_label("Reco / Gen (efficiency)")

        plt.xlabel(rf"$z_{{{label_tex}}}$ decay position [mm]")
        plt.ylabel(rf"$r_{{{label_tex}}}$ decay position [mm]")
        plt.title(rf"Reconstruction efficiency of {label_tex} in $(z, r)$, {tag}")
        plt.tight_layout()

        out_eff = os.path.join(outdir, f"hist2d_eff{basename}_z_vs_r_{tag}.png")
        plt.savefig(out_eff, dpi=170)
        plt.close()
        print(f"  Saved {out_eff}")

    # Do KS
    make_gen_reco_eff_plots(
        ks_z_gen, ks_r_gen,
        ks_z_reco, ks_r_reco,
        label_tex="K_S", basename="KS", tag=tag
    )

    # Do Lambda
    make_gen_reco_eff_plots(
        lm_z_gen, lm_r_gen,
        lm_z_reco, lm_r_reco,
        label_tex=r"\Lambda", basename="Lm", tag=tag
    )

