"""Core MSY math and table helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def msy(r: float, K: float) -> float:
    """Compute MSY from Schaefer parameters."""
    return (r * K) / 4


def e_msy(r: float, q: float) -> float:
    """Compute fishing effort that corresponds to MSY."""
    return r / (2 * q)


def build_scenario_table(r_values: np.ndarray, k_values: np.ndarray) -> pd.DataFrame:
    """Build a scenario table for combinations of r and K."""
    scenarios = []
    for r in r_values:
        for k_tonnes in k_values:
            scenarios.append(
                {
                    "r": float(r),
                    "K_tonnes": float(k_tonnes),
                    "MSY_tonnes_per_year": msy(float(r), float(k_tonnes)),
                }
            )
    return pd.DataFrame(scenarios)


def classify_pressure(ratio: float) -> str:
    """Classify fishing pressure from catch-to-MSY ratio."""
    if ratio > 1.1:
        return "Above MSY (high pressure)"
    if ratio >= 0.9:
        return "Near MSY"
    return "Below MSY (recovery window)"


def build_catch_table(
    years: np.ndarray, catch_tonnes: np.ndarray, msy_reference: float
) -> pd.DataFrame:
    """Build a catch table with ratio and pressure status."""
    result = pd.DataFrame(
        {
            "year": years.astype(int),
            "catch_tonnes": catch_tonnes.astype(float),
        }
    )
    result["catch_to_msy_ratio"] = result["catch_tonnes"] / float(msy_reference)
    result["status"] = result["catch_to_msy_ratio"].map(classify_pressure)
    return result
