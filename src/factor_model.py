"""Expected-return and abnormal-return helpers for an event study.

These functions implement the methodology described in the associated paper.
They do not download or redistribute CRSP/Compustat data.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def fit_ff3(estimation_window: pd.DataFrame):
    """Fit R-Rf = alpha + beta_m*MKT_RF + beta_s*SMB + beta_h*HML."""
    required = ["excess_return", "MKT_RF", "SMB", "HML"]
    clean = estimation_window[required].dropna()
    x = sm.add_constant(clean[["MKT_RF", "SMB", "HML"]])
    return sm.OLS(clean["excess_return"], x).fit()


def abnormal_returns(event_window: pd.DataFrame, fitted_model) -> pd.Series:
    """Compute realized minus factor-model-implied excess returns."""
    x = sm.add_constant(
        event_window[["MKT_RF", "SMB", "HML"]],
        has_constant="add",
    )
    expected = fitted_model.predict(x)
    return event_window["excess_return"] - expected


def cumulative_abnormal_return(ar: pd.Series) -> float:
    """Sum abnormal returns across an event window."""
    return float(np.sum(ar.dropna()))
