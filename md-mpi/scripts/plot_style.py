#!/usr/bin/env python3
"""Shared Matplotlib style helpers for all report plots."""

from matplotlib import pyplot as plt

# Color-blind-friendly palette (Okabe-Ito inspired)
COLOR_EULER = "#E69F00"     # orange
COLOR_VERLET = "#0072B2"    # blue
COLOR_RK4 = "#332288"       # indigo
COLOR_REFERENCE = "#6C6C6C" # gray
COLOR_ACCENT = "#CC79A7"    # magenta

INTEGRATOR_STYLE = {
    "euler": {"color": COLOR_EULER, "linestyle": "--", "linewidth": 2.0},
    "verlet": {"color": COLOR_VERLET, "linestyle": "-", "linewidth": 2.0},
    "rk4": {"color": COLOR_RK4, "linestyle": "-.", "linewidth": 2.0},
    "exact": {"color": COLOR_REFERENCE, "linestyle": "--", "linewidth": 1.6},
}


def apply_plot_style():
    """Apply consistent style defaults used across all figures."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "lines.linewidth": 2.0,
            "lines.markersize": 5.5,
            "axes.formatter.useoffset": False,
            "axes.formatter.use_mathtext": True,
            "savefig.dpi": 300,
        }
    )


def apply_major_grid(ax, axis="both"):
    """Draw a subtle major-only grid and disable minor-grid clutter."""
    ax.grid(True, which="major", axis=axis, alpha=0.22, linewidth=0.6)
    ax.grid(False, which="minor", axis=axis)


def disable_offset_text(ax):
    """Disable floating axis offset text like '1e-5'/'1e6'."""
    for offset in (ax.xaxis.offsetText, ax.yaxis.offsetText):
        offset.set_visible(False)
    try:
        ax.ticklabel_format(axis="both", style="plain", useOffset=False)
    except Exception:
        # Log axes do not support ticklabel_format(style='plain').
        pass


def save_figure(fig, path):
    """Save with tight bounding box and constrained layout support."""
    fig.savefig(path, bbox_inches="tight")
