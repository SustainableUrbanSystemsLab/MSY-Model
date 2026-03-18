"""Reusable plotting utilities for the Lake Victoria MSY notebook."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
import pandas as pd

PALETTE = {
    "ink": "#102a43",
    "accent": "#2a9d8f",
    "accent_dark": "#1b6f66",
    "warn": "#d62828",
}


def configure_plot_style() -> None:
    """Apply a consistent visual style for the notebook plots."""
    plt.style.use("default")
    plt.rcParams.update(
        {
            "figure.facecolor": "#f5f7fa",
            "axes.facecolor": "#fbfcfe",
            "axes.edgecolor": "#34495e",
            "axes.labelcolor": "#243b53",
            "axes.titlecolor": "#102a43",
            "axes.grid": True,
            "grid.color": "#d9e2ec",
            "grid.linewidth": 0.8,
            "grid.alpha": 0.8,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "legend.frameon": False,
        }
    )


def style_axes(ax) -> None:
    """Apply shared axis-level styling."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#627d98")
    ax.spines["bottom"].set_color("#627d98")
    ax.tick_params(colors="#334e68")


def tonnes_tick(x: float, _: float) -> str:
    """Pretty formatter for values expressed in tonnes."""
    if abs(x) >= 1_000_000:
        return f"{x / 1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"{x / 1_000:.0f}k"
    return f"{x:.0f}"


def make_tonnes_formatter() -> FuncFormatter:
    """Build a reusable tonnes tick formatter."""
    return FuncFormatter(tonnes_tick)


def plot_msy_sensitivity(
    k_grid,
    r_grid,
    msy_grid,
    r_baseline: float,
    k_baseline: float,
    tonnes_formatter: FuncFormatter,
):
    """Plot MSY sensitivity across r-K space."""
    lake_cmap = LinearSegmentedColormap.from_list(
        "lake_victoria",
        ["#0b3954", "#087e8b", "#5aaa95", "#bfd7b5", "#f5e663"],
    )

    fig, ax = plt.subplots(figsize=(10.5, 6.2), constrained_layout=True)
    im = ax.imshow(
        msy_grid,
        origin="lower",
        aspect="auto",
        extent=[k_grid.min(), k_grid.max(), r_grid.min(), r_grid.max()],
        cmap=lake_cmap,
    )

    ax.contour(
        k_grid,
        r_grid,
        msy_grid,
        levels=5,
        colors="white",
        linewidths=0.8,
        alpha=0.55,
    )

    scenarios_points = [
        (0.40, 1_900_000, "Low r, low K", "#f4a261"),
        (0.45, 2_160_000, "High r, high K", "#d62828"),
        (r_baseline, k_baseline, "Baseline", "#102a43"),
    ]
    for r_val, k_val, label, color in scenarios_points:
        ax.scatter(
            k_val,
            r_val,
            s=85,
            color=color,
            edgecolor="white",
            linewidth=0.9,
            zorder=3,
            label=label,
        )

    colorbar = fig.colorbar(im, ax=ax, pad=0.02)
    colorbar.ax.yaxis.set_major_formatter(tonnes_formatter)
    colorbar.set_label("MSY (tonnes/year)", color=PALETTE["ink"])

    ax.xaxis.set_major_formatter(tonnes_formatter)
    ax.set_xlabel("Carrying Capacity K (tonnes)")
    ax.set_ylabel("Intrinsic Growth Rate r (1/year)")
    ax.set_title("Nile Perch MSY Sensitivity Surface", loc="left", weight="bold")
    ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#d9e2ec", fontsize=9)

    style_axes(ax)
    plt.show()


def plot_yield_effort(
    effort,
    yield_tonnes,
    effort_msy: float,
    msy_tonnes: float,
    tonnes_formatter: FuncFormatter,
):
    """Plot Schaefer yield as a function of fishing effort."""
    fig, ax = plt.subplots(figsize=(10.5, 5.6), constrained_layout=True)
    ax.plot(effort / 1_000, yield_tonnes, color=PALETTE["accent_dark"], linewidth=3)
    ax.fill_between(effort / 1_000, yield_tonnes, color=PALETTE["accent"], alpha=0.22)

    ax.axvline(effort_msy / 1_000, color=PALETTE["warn"], linestyle=(0, (5, 4)), linewidth=2)
    ax.scatter(effort_msy / 1_000, msy_tonnes, s=95, color=PALETTE["warn"], zorder=3)
    ax.annotate(
        f"MSY point\nE_MSY={effort_msy:,.0f}\nMSY={msy_tonnes:,.0f}",
        xy=(effort_msy / 1_000, msy_tonnes),
        xytext=(16, -22),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff3f2", edgecolor="#d62828", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#d62828", lw=1.2),
        fontsize=9,
        color=PALETTE["ink"],
    )

    ax.set_title("Yield-Effort Frontier at Baseline Parameters", loc="left", weight="bold")
    ax.set_xlabel("Fishing effort (thousand units/year)")
    ax.set_ylabel("Equilibrium yield (tonnes/year)")
    ax.yaxis.set_major_formatter(tonnes_formatter)

    style_axes(ax)
    plt.show()


def plot_catch_dashboard(
    result: pd.DataFrame,
    country: str,
    msy_reference: float,
    tonnes_formatter: FuncFormatter,
):
    """Plot catch trajectory and catch-to-MSY ratio panels."""
    status_palette = {
        "Above MSY (high pressure)": "#d62828",
        "Near MSY": "#f4a261",
        "Below MSY (recovery window)": "#2a9d8f",
    }
    bar_colors = result["status"].map(status_palette)

    fig = plt.figure(figsize=(10.5, 7.0), constrained_layout=True)
    grid = fig.add_gridspec(2, 1, height_ratios=[2.2, 1], hspace=0.05)
    ax_top = fig.add_subplot(grid[0])
    ax_bottom = fig.add_subplot(grid[1], sharex=ax_top)

    ax_top.bar(
        result["year"],
        result["catch_tonnes"],
        color=bar_colors,
        edgecolor="#1f2933",
        linewidth=0.7,
        alpha=0.92,
    )
    ax_top.plot(result["year"], result["catch_tonnes"], color="#1f2a44", linewidth=1.8, marker="o")
    ax_top.axhline(msy_reference, color=PALETTE["warn"], linestyle=(0, (5, 4)), linewidth=2)
    ax_top.fill_between(
        result["year"],
        msy_reference,
        result["catch_tonnes"],
        where=result["catch_tonnes"] > msy_reference,
        interpolate=True,
        color=PALETTE["warn"],
        alpha=0.12,
    )

    ax_top.set_ylabel("Catch (tonnes)")
    ax_top.yaxis.set_major_formatter(tonnes_formatter)
    ax_top.set_title(f"{country}: Catch Trajectory Against MSY Target", loc="left", weight="bold")

    ax_bottom.plot(result["year"], result["catch_to_msy_ratio"], color="#1f2a44", linewidth=2.2, marker="o")
    ax_bottom.axhline(1.0, color=PALETTE["warn"], linestyle=(0, (5, 4)), linewidth=1.8)
    ax_bottom.axhspan(0.9, 1.1, color="#ffe8b6", alpha=0.6)

    ax_bottom.set_ylabel("Catch / MSY")
    ax_bottom.set_xlabel("Year")
    ax_bottom.set_ylim(0.7, max(1.35, result["catch_to_msy_ratio"].max() + 0.08))

    style_axes(ax_top)
    style_axes(ax_bottom)
    ax_top.tick_params(labelbottom=False)

    plt.show()
