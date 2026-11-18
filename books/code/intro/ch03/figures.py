# -*- coding: utf-8 -*-
"""第 3 章插图：八步流程与耗时、串联成功率随步数下降、三档频率的时间尺度。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import figstyle as fs


def fig_pipeline():
    """八步流程，横向耗时为时间轴上的条，按顺序首尾相接。"""
    steps = [
        ("1　看到", 0, 20, "20 ms", fs.BLUE),
        ("2　认出", 20, 55, "35 ms", fs.BLUE),
        ("3　定位", 55, 70, "15–30 ms", fs.BLUE),
        ("4　决定抓哪", 70, 290, "100–300 ms", fs.ACCENT),
        ("5　规划路径", 290, 350, "40–80 ms", fs.PURPLE),
        ("6　闭环抓取", 350, 700, "200–400 ms", fs.GREEN),
        ("7　搬运放下", 700, 1150, "300–600 ms", fs.GREEN),
        ("8　检查", 1150, 1185, "35 ms", fs.BLUE),
    ]
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    n = len(steps)
    for i, (name, s, e, lab, c) in enumerate(steps):
        y = n - 1 - i
        ax.barh(y, e - s, left=s, height=0.44, color=c, alpha=0.92,
                edgecolor="white", linewidth=0.7, zorder=3)
        ax.text(e + 16, y, lab, ha="left", va="center", fontsize=8.2, color=c, zorder=4)
        if i < n - 1:
            ax.annotate("", xy=(e, y - 0.74), xytext=(e, y - 0.26),
                        arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=0.8,
                                        mutation_scale=6, shrinkA=0, shrinkB=0), zorder=2)

    ax.set_yticks(range(n))
    ax.set_yticklabels([s[0] for s in steps][::-1], fontsize=8.8)
    ax.tick_params(axis="y", length=0, pad=4)
    ax.set_xlim(0, 1470)
    ax.set_ylim(-0.75, 7.95)
    ax.set_xticks(range(0, 1400, 200))
    ax.tick_params(axis="x", labelsize=8.6)
    ax.set_xlabel("时间（毫秒，从相机曝光算起）", fontsize=8.8, labelpad=6)
    fs.clean(ax, spines=("bottom",))
    ax.tick_params(axis="y", length=0)

    ax.annotate("", xy=(1185, 7.62), xytext=(0, 7.62),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8))
    ax.text(592, 7.68, "一次执行 1.2 s，慢的路径 1.5 s", ha="center", va="bottom",
            fontsize=8.4, color=fs.MUTED)

    handles = [Patch(facecolor=fs.BLUE, alpha=0.92, label="感知"),
               Patch(facecolor=fs.ACCENT, alpha=0.92, label="决策"),
               Patch(facecolor=fs.PURPLE, alpha=0.92, label="规划"),
               Patch(facecolor=fs.GREEN, alpha=0.92, label="执行")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.19),
              ncol=4, fontsize=8.2, frameon=False)
    fs.save(fig, "ch03", "fig03-01")


def fig_success():
    """每步成功率固定时，串行 n 步的整体成功率。"""
    n = np.arange(1, 9)
    curves = [(0.98, fs.GREEN, "每步 0.98"),
              (0.95, fs.ACCENT, "每步 0.95"),
              (0.90, fs.BLUE, "每步 0.90")]
    fig, ax = plt.subplots(figsize=(6.9, 3.7))
    for p, c, lab in curves:
        ax.plot(n, p ** n, marker="o", ms=3.6, lw=1.5, color=c, label=lab, zorder=3)
        ax.text(8.18, p ** 8, f"{p ** 8:.2f}", ha="left", va="center",
                fontsize=8.6, color=c, weight="bold")
    ax.plot([8], [0.95 ** 8], marker="o", ms=8, mfc="none", mec=fs.ACCENT, mew=1.4, zorder=4)

    ax.set_xlim(0.7, 9.35)
    ax.set_ylim(0.34, 1.04)
    ax.set_xticks(range(1, 9))
    ax.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_xlabel("串行执行的步数", fontsize=8.8)
    ax.set_ylabel("整条链路成功率", fontsize=8.8)
    ax.tick_params(labelsize=8.6)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.legend(loc="lower left", fontsize=8.2, frameon=False,
              bbox_to_anchor=(0.03, 0.06))

    ax.text(4.55, 0.393, "每步 0.95 走完八步，只剩 0.66", fontsize=8.4,
            color=fs.ACCENT, ha="left", va="center")
    fs.save(fig, "ch03", "fig03-02")


def fig_clock():
    """三档频率的时间尺度，以及延迟折算成末端位移。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.9, 2.95),
                                   gridspec_kw={"width_ratios": [1.42, 1.0]})

    rows = [("策略 一次推理", 330, fs.ACCENT, "100–330 ms"),
            ("视觉 一帧", 33, fs.BLUE, "33 ms"),
            ("伺服 一拍", 1.0, fs.GREEN, "1 ms")]
    for i, (name, t, c, lab) in enumerate(rows):
        y = 2 - i
        ax1.hlines(y, 0.55, t, color=c, lw=10, alpha=0.92, zorder=3)
        ax1.text(t * 1.35, y, lab, ha="left", va="center", fontsize=8.4, color=c)
    ax1.axvline(200, color=fs.FAINT, lw=0.9, ls=(0, (3, 2)), zorder=1)
    ax1.text(200, 2.62, "人的反应 0.2 s", ha="center", va="bottom",
             fontsize=8.0, color=fs.MUTED)
    ax1.set_xscale("log")
    ax1.set_xlim(0.5, 6000)
    ax1.set_ylim(-0.7, 2.9)
    ax1.set_yticks([2, 1, 0])
    ax1.set_yticklabels([r[0] for r in rows], fontsize=8.6)
    ax1.set_xticks([1, 10, 100, 1000])
    ax1.set_xticklabels(["1", "10", "100", "1000"], fontsize=8.2)
    ax1.tick_params(axis="y", length=0, pad=4)
    ax1.set_xlabel("一圈耗时（毫秒，对数刻度）", fontsize=8.4, labelpad=5)
    fs.clean(ax1, spines=("bottom",))
    ax1.text(0.02, 0.965, "(a)", transform=ax1.transAxes, fontsize=9.2,
             color=fs.INK, va="top", ha="left")

    delays = [("330 ms", 66.0, "66 mm"), ("33 ms", 6.6, "6.6 mm"), ("1 ms", 0.2, "0.2 mm")]
    cols = [fs.ACCENT, fs.BLUE, fs.GREEN]
    for i, ((_, d, lab), c) in enumerate(zip(delays, cols)):
        y = 2 - i
        ax2.barh(y, d, left=0.1, height=0.44, color=c, alpha=0.92,
                 edgecolor="white", linewidth=0.7, zorder=3)
        ax2.text(135, y, lab, ha="left", va="center", fontsize=8.2, color=c)
    ax2.axvline(70, color=fs.GOLD, lw=1.0, ls=(0, (3, 2)), zorder=2)
    ax2.text(70, 2.52, "杯口 70 mm", ha="center", va="bottom",
             fontsize=8.0, color=fs.GOLD)
    ax2.set_xscale("log")
    ax2.set_xlim(0.08, 900)
    ax2.set_ylim(-0.7, 2.9)
    ax2.set_yticks([0, 1, 2])
    ax2.set_yticklabels(["1 ms", "33 ms", "330 ms"], fontsize=8.4)
    ax2.set_xticks([0.1, 1, 10, 100])
    ax2.set_xticklabels(["0.1", "1", "10", "100"], fontsize=8.2)
    ax2.tick_params(axis="y", length=0, pad=4)
    ax2.set_xlabel("延迟期间末端走出的距离（毫米）", fontsize=8.4, labelpad=5)
    fs.clean(ax2, spines=("bottom",))
    ax2.text(0.03, 0.965, "(b)", transform=ax2.transAxes, fontsize=9.2,
             color=fs.INK, va="top", ha="left")

    fig.subplots_adjust(wspace=0.34)
    fs.save(fig, "ch03", "fig03-03")


if __name__ == "__main__":
    fig_pipeline()
    fig_success()
    fig_clock()
