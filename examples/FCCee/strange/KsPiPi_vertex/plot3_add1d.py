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
#    "Zcc": "p8_ee_Zcc_ecm91.root",
#    "Zbb": "p8_ee_Zbb_ecm91.root",
#    "Zud": "p8_ee_Zud_ecm91.root",
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
# Common binning
# -------------------------
zmin, zmax = 0.0, 5500.0
rmin, rmax = 0.0, 5500.0
nbins = 200

bins_z = np.linspace(zmin, zmax, nbins + 1)
bins_r = np.linspace(rmin, rmax, nbins + 1)
r_centers = 0.5 * (bins_r[:-1] + bins_r[1:])

# -------------------------
# Helper: flatten awkward → numpy
# -------------------------
def flatten_vals(arrays, name):
    if name not in arrays.fields:
        return np.array([], dtype=float)
    vals = ak.to_numpy(ak.flatten(arrays[name], axis=None))
    return vals[np.isfinite(vals)]

# -------------------------
# Helper: gen/reco 2D + efficiency + 1D r projection + 1D ratio
# -------------------------
def make_gen_reco_eff_plots(
    z_gen, r_gen, z_reco, r_reco,
    label_tex, basename, tag
):
    """Make 2D gen/reco/efficiency and 1D r projections + ratio."""

    if z_gen.size == 0 or r_gen.size == 0:
        print(f"  WARNING: no gen {basename} entries in this sample")
        return

    # 2D histograms with common binning
    H_gen, _, _ = np.histogram2d(
        z_gen, r_gen, bins=[bins_z, bins_r]
    )
    if z_reco.size > 0 and r_reco.size > 0:
        H_reco, _, _ = np.histogram2d(
            z_reco, r_reco, bins=[bins_z, bins_r]
        )
    else:
        H_reco = np.zeros_like(H_gen)

    # ==============================
    # 2D GEN
    # ==============================
    H_gen_plot = H_gen.copy()
    H_gen_plot[H_gen_plot == 0] = np.nan

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

    # ==============================
    # 2D RECO
    # ==============================
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

    # ==============================
    # 2D Efficiency: reco / gen
    # ==============================
    with np.errstate(divide="ignore", invalid="ignore"):
        eff_2d = np.divide(
            H_reco,
            H_gen,
            out=np.zeros_like(H_reco, dtype=float),
            where=H_gen > 0,
        )

    eff_masked = np.ma.array(eff_2d, mask=(H_gen == 0))

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

    out_eff2d = os.path.join(outdir, f"hist2d_eff{basename}_z_vs_r_{tag}.png")
    plt.savefig(out_eff2d, dpi=170)
    plt.close()
    print(f"  Saved {out_eff2d}")

    # ==============================
    # 1D r distribution (direct, not from 2D projection)
    # ==============================

    # Direct GEN histogram
    gen_counts, gen_edges = np.histogram(
        r_gen,
        bins=5500,
        range=(1, 5501)
    )
    gen_centers = 0.5 * (gen_edges[:-1] + gen_edges[1:])
    total_gen = gen_counts.sum()

    # Direct RECO histogram
    reco_counts, reco_edges = np.histogram(
        r_reco,
        bins=5500,
        range=(1, 5501)
    )
    reco_centers = 0.5 * (reco_edges[:-1] + reco_edges[1:])
    total_reco = reco_counts.sum()

    ratio_total = (total_reco / total_gen) if total_gen > 0 else 0.0

    # ------------------------------
    # Plot GEN/RECO 1D (log-log)
    # ------------------------------
    plt.figure(figsize=(7, 5))

    # GEN
    plt.step(
        gen_centers, gen_counts,
        where="mid",
        linewidth=2.5,
        label=f"Generated: N = {total_gen:.0f}"
    )

    # RECO
    if total_reco > 0:
        plt.step(
            reco_centers, reco_counts,
            where="mid",
            linewidth=2.5,
            linestyle="--",
            label=f"Reconstructed: N = {total_reco:.0f}, ratio = {ratio_total:.3f}"
        )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlim(1, 5500)

    plt.xlabel(rf"$r_{{{label_tex}}}$ decay position [mm]")
    plt.ylabel("Counts (log scale)")
    plt.title(rf"{label_tex} decay radius distribution, {tag}")
    plt.legend()
    plt.tight_layout()

    out_1d = os.path.join(outdir, f"hist1d_genreco{basename}_r_{tag}_remove0.png")
    plt.savefig(out_1d, dpi=170)
    plt.close()
    print(f"  Saved {out_1d}")

    # ==============================
    # 1D r efficiency (direct histograms)
    # ==============================

    with np.errstate(divide="ignore", invalid="ignore"):
        eff_r = np.divide(
            reco_counts,
            gen_counts,
            out=np.zeros_like(reco_counts, dtype=float),
            where=gen_counts > 0
        )

    eff_masked = np.ma.array(eff_r, mask=(gen_counts == 0))

    plt.figure(figsize=(7, 5))
    plt.step(
        gen_centers, eff_masked,
        where="mid",
        linewidth=2.5
    )

    plt.xscale("log")
    plt.xlim(1, 5500)
    plt.ylim(0.0, 1.05)

    plt.xlabel(rf"$r_{{{label_tex}}}$ decay position [mm]")
    plt.ylabel("Reco / Gen")
    plt.title(rf"Reconstruction efficiency vs $r$ for {label_tex}, {tag}")
    plt.tight_layout()

    out_eff1d = os.path.join(outdir, f"hist1d_eff{basename}_r_{tag}_remove0.png")
    plt.savefig(out_eff1d, dpi=170)
    plt.close()
    print(f"  Saved {out_eff1d}")


# -------------------------
# Main loop over samples
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

    # Do K_S
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

