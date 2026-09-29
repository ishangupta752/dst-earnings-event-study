"""Create visual summaries from results reported in the research paper."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

headline = pd.read_csv(RESULTS / "car_results.csv")

x = range(len(headline))
width = 0.36
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.bar([i - width/2 for i in x], headline["non_dst_car_pct"], width, label="Non-DST")
ax.bar([i + width/2 for i in x], headline["dst_car_pct"], width, label="DST transition")
ax.set_xticks(list(x), headline["event_window"])
ax.set_ylabel("Mean cumulative abnormal return (%)")
ax.set_xlabel("Event window (trading days)")
ax.set_title("Earnings-announcement CAR: DST vs. non-DST weeks")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES / "car_by_event_window.png", dpi=180)
plt.close(fig)

robust = pd.read_csv(RESULTS / "robustness_results.csv")
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.barh(robust["specification"], robust["dst_coefficient"])
ax.axvline(0, linewidth=1)
ax.set_xlabel("Reported DST-transition coefficient")
ax.set_title("DST effect across robustness specifications")
fig.tight_layout()
fig.savefig(FIGURES / "robustness_results.png", dpi=180)
plt.close(fig)
