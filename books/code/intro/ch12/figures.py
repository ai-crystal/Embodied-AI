# -*- coding: utf-8 -*-
"""第 12 章插图：数据金字塔、成功率置信区间、时延预算甘特图。"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy.stats import beta
import figstyle as fs


# ---------- 二项分布区间 ----------
def clopper_pearson(k, n, alpha=0.05):
    """精确（Clopper-Pearson）二项置信区间。"""
    lo = 0.0 if k <= 0 else float(beta.ppf(alpha / 2.0, k, n - k + 1))
    hi = 1.0 if k >= n else float(beta.ppf(1 - alpha / 2.0, k + 1, n - k))
    return lo, hi


def fig_pyramid():
    """数据金字塔：人类视频 -> 仿真 -> 真机。"""
    fig, ax = fs.canvas(6.6, 3.9, xlim=(0, 10), ylim=(0.0, 6.3))

    y0, y1 = 0.55, 5.55
    xl0, xl1 = 1.15, 3.42
    slope = (xl1 - xl0) / (y1 - y0)

    def xl(y):
        return xl0 + (y - y0) * slope

    def xr(y):
        return 6.15 - (y - y0) * slope

    layers = [
        (0.55, 2.30, "人类视频", "#EEF3FB", fs.BLUE),
        (2.30, 3.95, "仿真", "#ECFAF4", fs.GREEN),
        (3.95, 5.55, "真机", "#FDF1E6", fs.ACCENT),
    ]
    for a, b, name, fc, ec in layers:
        pts = [(xl(a), a), (xr(a), a), (xr(b), b), (xl(b), b)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=ec,
                             linewidth=1.1, zorder=2))
        fs.label(ax, (xl((a + b) / 2) + xr((a + b) / 2)) / 2, (a + b) / 2, name,
                 fs=9.6, color=ec, weight="bold")

    notes = [
        (4.75, "真机遥操作", "100 万+ 条", "DROID 7.6 万条", fs.ACCENT),
        (3.12, "物理仿真", "10 万+ 条", "RoboCasa 生成", fs.GREEN),
        (1.42, "人类视频", "数千小时", "没有动作标签", fs.BLUE),
    ]
    for yc, name, qty, note, col in notes:
        ax.plot([xr(yc + 0.34) + 0.10, 6.80], [yc + 0.34, yc + 0.34],
                color=fs.FAINT, lw=0.8, ls=(0, (2, 2)), zorder=1)
        fs.label(ax, 6.90, yc + 0.34, name, fs=9.0, ha="left", color=col, weight="bold")
        fs.label(ax, 6.90, yc, qty, fs=8.7, ha="left", color=fs.INK)
        fs.label(ax, 6.90, yc - 0.32, note, fs=8.3, ha="left", color=fs.MUTED)

    fs.arrow(ax, (0.55, 1.25), (0.55, 4.75), color=fs.FAINT, lw=0.9)
    ax.text(0.28, 3.00, "与真机任务的相关度", rotation=90, ha="center", va="center",
            fontsize=8.2, color=fs.MUTED)
    ax.annotate("", xy=(1.15, 0.32), xytext=(6.15, 0.32),
                arrowprops=dict(arrowstyle="<->", color=fs.FAINT, lw=0.9))
    fs.label(ax, 3.65, 0.11, "可得数据的量级", fs=8.2, color=fs.MUTED)
    fs.label(ax, 6.90, 0.40, "越往上，每小时数据越贵", fs=8.2, ha="left", color=fs.MUTED)

    fs.save(fig, "ch12", "fig12-01")


def fig_interval():
    """成功率点估计与 95% 置信区间随试验次数的变化（二项分布实算）。"""
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.set_xlim(5, 100)
    ax.set_ylim(28, 112)

    ns = np.arange(5, 101, dtype=float)
    k = 0.9 * ns                      # 成功次数按 0.9n 连续取值，区间用 Beta 分位数
    lo = beta.ppf(0.025, k, ns - k + 1) * 100
    hi = beta.ppf(0.975, k + 1, ns - k) * 100

    ax.fill_between(ns, lo, hi, color="#FDF1E6", zorder=1)
    ax.plot(ns, hi, color=fs.ACCENT, lw=1.4, zorder=3)
    ax.plot(ns, lo, color=fs.ACCENT, lw=1.4, zorder=3)
    ax.axhline(90, color=fs.MUTED, lw=0.9, ls=(0, (4, 3)), zorder=2)
    ax.text(6.2, 91.4, "真实水平 90%", fontsize=8.2, color=fs.MUTED, va="bottom")

    ax.plot([20, 20], [lo[15], hi[15]], color=fs.INK, lw=2.0, zorder=4)
    ax.scatter([20, 20], [lo[15], hi[15]], s=18, color=fs.INK, zorder=5)
    ax.annotate("20 次里成功 18 次\n区间 68% 到 99%", xy=(20, 66.2), xytext=(8.2, 40),
                fontsize=8.4, color=fs.INK, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=0.9,
                                shrinkA=3, shrinkB=3))

    ax.plot([100, 100], [lo[-1], hi[-1]], color=fs.INK, lw=2.0, zorder=4)
    ax.scatter([100, 100], [lo[-1], hi[-1]], s=18, color=fs.INK, zorder=5)
    ax.annotate("100 次里成功 90 次\n区间 82% 到 95%", xy=(98.6, hi[-1]), xytext=(83, 104.5),
                fontsize=8.4, color=fs.INK, ha="right", va="center",
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=0.9,
                                shrinkA=3, shrinkB=5))

    ax.set_xlabel("试验次数")
    ax.set_ylabel("成功率（%）")
    ax.set_xticks([20, 40, 60, 80, 100])
    ax.set_yticks([40, 60, 80, 100])
    fs.clean(ax, grid=True)
    ax.set_axisbelow(True)
    fs.save(fig, "ch12", "fig12-02")


def fig_budget():
    """时延预算甘特图：一次同步链路与分块摊薄。"""
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    ax.set_xlim(-6, 392)
    ax.set_ylim(0.75, 6.45)

    # 一轮同步链路，三段堆叠
    segs = [(0, 17, fs.BLUE, "#EEF3FB"), (17, 187, fs.ACCENT, "#FDF1E6"),
            (187, 194, fs.GREEN, "#ECFAF4")]
    for a, b, ec, fc in segs:
        ax.add_patch(plt.Rectangle((a, 3.50), b - a, 0.70, facecolor=fc, edgecolor=ec,
                                   linewidth=1.0, zorder=4))

    ax.text(100, 3.85, "推理 170 ms", ha="center", va="center", fontsize=9.0,
            color=fs.ACCENT, weight="bold", zorder=5)
    ax.annotate("感知 17 ms", xy=(8.5, 4.22), xytext=(0, 4.52),
                fontsize=8.4, color=fs.BLUE, ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-", color=fs.BLUE, lw=0.8))
    ax.annotate("执行 7 ms", xy=(190.5, 3.45), xytext=(198, 3.02),
                fontsize=8.4, color=fs.GREEN, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=fs.GREEN, lw=0.8))

    # 分块摊薄后每步
    ax.add_patch(plt.Rectangle((0, 1.20), 21, 0.70, facecolor="#F3EEFC",
                               edgecolor=fs.PURPLE, linewidth=1.0, zorder=4))
    ax.text(26, 1.55, "每步 21 ms", ha="left", va="center",
            fontsize=8.6, color=fs.PURPLE, weight="bold")
    ax.text(26, 1.22, "按 15 Hz 走", ha="left", va="center",
            fontsize=8.0, color=fs.MUTED)

    # 预算线
    for x, col in ((100, fs.PINK), (333, fs.TEAL)):
        ax.plot([x, x], [1.02, 5.30], color=col, lw=1.0, ls=(0, (5, 3)), zorder=1)
    ax.text(100, 6.20, "10 Hz 预算 100 ms", ha="center", va="center",
            fontsize=8.4, color=fs.PINK, weight="bold")
    ax.text(100, 5.68, "一轮 194 ms，超出 94 ms", ha="center", va="center",
            fontsize=8.0, color=fs.PINK)
    ax.text(333, 6.20, "3 Hz 预算 333 ms", ha="center", va="center",
            fontsize=8.4, color=fs.TEAL, weight="bold")
    ax.text(333, 5.68, "还余 139 ms", ha="center", va="center",
            fontsize=8.0, color=fs.TEAL)

    ax.set_yticks([3.85, 1.55])
    ax.set_yticklabels(["一轮链路", "分块摊薄"])
    ax.set_xlabel("时间（ms）")
    ax.set_xticks([0, 100, 200, 300])
    fs.clean(ax, grid=True, spines=("bottom",))
    ax.tick_params(axis="y", length=0)
    ax.set_axisbelow(True)
    fs.save(fig, "ch12", "fig12-03")


if __name__ == "__main__":
    fig_pyramid()
    fig_interval()
    fig_budget()
