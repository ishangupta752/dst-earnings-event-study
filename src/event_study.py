"""Utilities for constructing event windows and cumulative abnormal returns."""
from __future__ import annotations

import pandas as pd


def select_event_window(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    """Select rows whose relative trading day lies in [start, end]."""
    return df.loc[df["event_day"].between(start, end)].copy()


def car_by_event(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    """Aggregate a pre-computed abnormal_return column into event-level CAR."""
    window = select_event_window(df, start, end)
    out = (
        window.groupby("event_id", as_index=False)
        .agg(
            car=("abnormal_return", "sum"),
            dst_transition=("dst_transition", "first"),
            firm_id=("firm_id", "first"),
            year=("year", "first"),
        )
    )
    return out


def mean_car_difference(events: pd.DataFrame) -> pd.Series:
    """Return mean CAR by DST status and the DST-minus-non-DST difference."""
    means = events.groupby("dst_transition")["car"].mean()
    non_dst = float(means.get(0, float("nan")))
    dst = float(means.get(1, float("nan")))
    return pd.Series({"non_dst": non_dst, "dst": dst, "difference": dst - non_dst})
