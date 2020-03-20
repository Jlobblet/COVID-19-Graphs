#!/usr/bin/env python3
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

from CONFIG import CONFIG

# plt.style.use("seaborn")


def toy_data(start=100, rate=1.333333, length=20):
    data = np.arange(0, length)
    data = start * rate ** data
    return data


def create_graph(df, xlab, threshold):
    df = df.drop(["Lat", "Long"], axis=1).groupby(by="Country/Region").sum()
    df = df.drop("Cruise Ship")
    df = df.sort_values(df.columns[-1], ascending=False)
    series_dict = dict()
    for country, series in df.iterrows():
        data = np.array(series[series >= threshold].to_list())
        if data.size >= 10:
            series_dict[country] = data[0 : min(data.size - 1, 29)]

    fig, ax = plt.subplots(1, figsize=(16, 9))
    for country, series in series_dict.items():
        x = np.arange(0, series.size)
        ax.plot(x, series, label=country)
    ax.plot(toy_data(start=threshold), "r--", label="33% growth every day", lw=2)

    for line in ax.lines:
        x, y = line.get_xydata()[-1]
        ax.text(x, y, line.get_label(), color=line.get_color())

    at = AnchoredText("Source: https://github.com/CSSEGISandData/COVID-19", prop=dict(size=8), loc=4)
    ax.add_artist(at)
    ax.set_xlim(0, ax.get_xlim()[1])
    ax.set_xlabel(f"Days after {threshold} {xlab}")
    ax.set_ylabel(f"Number of {xlab}")
    ax.set_yscale("log")
    plt.tight_layout()
    fig.savefig(os.path.join(os.getcwd(), "out", f"{xlab}.png"))


if __name__ == "__main__":
    confirmed_location = os.path.join(
        CONFIG["COVID-19_repo_location"],
        CONFIG["time_series_path"],
        CONFIG["time_series_confirmed"],
    )

    deaths_location = os.path.join(
        CONFIG["COVID-19_repo_location"],
        CONFIG["time_series_path"],
        CONFIG["time_series_deaths"],
    )

    recovered_location = os.path.join(
        CONFIG["COVID-19_repo_location"],
        CONFIG["time_series_path"],
        CONFIG["time_series_recovered"],
    )

    confirmed_df = pd.read_csv(confirmed_location)
    create_graph(confirmed_df, "Confirmed Cases", 100)

    deaths_df = pd.read_csv(deaths_location)
    create_graph(deaths_df, "Deaths", 3)

    recoveries_df = pd.read_csv(recovered_location)
    create_graph(confirmed_df, "Recovered Cases", 50)
