#!/usr/bin/env python3
import os
import datetime as dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

from CONFIG import CONFIG

# plt.style.use("seaborn")
cmap = plt.get_cmap("tab10")


def toy_data(start=100, rate=1.333333, length=25):
    data = np.arange(0, length)
    data = start * rate ** data
    return data


def plot_graph(series_dict, xlab, threshold):
    fig, ax = plt.subplots(1, figsize=(16, 9))
    j = 0
    for country, series in series_dict.items():
        x = np.arange(0, series.size)
        for i in x:
            if i != max(x):
                ax.plot(
                    x[i : i + 2],
                    series[i : i + 2],
                    alpha=0.1 + 0.9 * float(i) / (series.size),
                    color=cmap(j),
                    label=country,
                )
            else:
                ax.plot(
                    x[i : i + 2],
                    series[i : i + 2],
                    alpha=0.1 + 0.9 * float(i) / (series.size),
                    color=cmap(j),
                    label=country,
                    marker="o",
                    markevery=[-1],
                )
        ax.text(x[-1] + 0.5, series[-1], country, color=cmap(j))
        j += 1
        if j > cmap.N:
            j = 0
        # ax.plot(x, series, label=country, marker="o", markevery=[-1])

    # for line in ax.lines:
    #     x, y = line.get_xydata()[-1]
    #    ax.text(x + 0.5, y, line.get_label(), color=line.get_color())

    at = AnchoredText(
        f"Source: https://github.com/CSSEGISandData/COVID-19, {dt.datetime.today()}",
        prop=dict(size=8),
        loc=4,
    )
    ax.add_artist(at)
    ax.set_xlim(0, ax.get_xlim()[1])
    ax.set_xlabel(f"Days after {threshold} {xlab}", fontsize=20)
    ax.set_ylabel(f"Number of {xlab}", fontsize=20)
    ax.set_yscale("log")
    plt.tight_layout()
    return fig, ax


def create_series_dict(df, threshold):
    df = df.drop(["Lat", "Long"], axis=1).groupby(by="Country/Region").sum()
    df = df.sort_values(df.columns[-1], ascending=False)
    df = df.drop("Diamond Princess")
    series_dict = dict()
    for country, series in df.iterrows():
        data = np.array(series[series >= threshold].to_list())
        if data.size >= 14:
            series_dict[country] = data[0 : min(data.size, 59)]

    return series_dict


def plot_series_dict(series_dict, xlab, threshold):
    fig, ax = plot_graph(series_dict, xlab, threshold)
    example = ax.plot(
        toy_data(start=threshold), "r--", label="33% growth every day", lw=2
    )[0]
    exx, exxy = example.get_xydata()[-1]
    ax.text(exx, exxy, example.get_label(), color=example.get_color())
    return fig


def create_single_graph(df, xlab, threshold):
    fig = plot_series_dict(create_series_dict(df, threshold), xlab, threshold)
    fig.savefig(os.path.join(os.getcwd(), "out", f"{xlab}.png"))


def create_graph_animation(series_dict, xlab, threshold):
    max_len = max([x.size for x in series_dict.values()])
    print(series_dict)
    for i in range(1, max_len):
        truncated_dict = {
            key: value[: min(value.size, i)] for key, value in series_dict.items()
        }
        fig = plot_series_dict(truncated_dict, xlab, threshold)


if __name__ == "__main__":
    # os.chdir(os.path.join(CONFIG["COVID-19_repo_location"]))
    # print(os.exec("git log -1 --format=%cd"))

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
    create_single_graph(confirmed_df, "Confirmed Cases", 100)

    deaths_df = pd.read_csv(deaths_location)
    create_single_graph(deaths_df, "Deaths", 3)

    recoveries_df = pd.read_csv(recovered_location)
    create_single_graph(confirmed_df, "Recovered Cases", 50)
