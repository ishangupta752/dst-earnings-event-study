"""Illustrative event-level regression helper for the paper's CAR specification."""
from __future__ import annotations

import pandas as pd
import statsmodels.formula.api as smf


def fit_car_regression(events: pd.DataFrame):
    """Fit CAR on DST status, controls, and industry fixed effects.

    Expected columns: car, dst_transition, size, book_to_market,
    analyst_coverage, industry.
    """
    formula = (
        "car ~ dst_transition + size + book_to_market + "
        "analyst_coverage + C(industry)"
    )
    return smf.ols(formula, data=events).fit()
