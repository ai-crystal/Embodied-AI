# -*- coding: utf-8 -*-
"""第 14 章插图：数据金字塔、采集方式对比、Open X-Embodiment 分布。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import figstyle as fs


def fig_pyramid():
    """数据金字塔：三层，各标注量级与代表数据集。"""
    fig, ax = fs.canvas(6.8, 4.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.4)

    cx = 2.55
    # (底半宽, 顶半宽, y0, y1, 填充, 边框)
    layers = [
        (2.05, 1.62, 0.78, 2.12, "#EDE4D8", "#C9B49B"),
        (1.62, 1.08, 2.12, 3.46, "#E4E7EE", "#A9B4C8"),
        (1.08, 0.72, 3.46, 4.80, "#F6E3DA", "#D9A48C"),
    ]
    names = ["人类视频与网络图文", "仿真与视频生成", "真机遥操作"]
    scales = ["$10^{4}$–$10^{5}$ 小时", "$10^{3}$–$10^{4}$ 小时", "$10^{2}$–$10^{4}$ 小时"]
    notes = ["有画面，没有动作", "有动作，物理是近似的", "动作准，量最少"]

    for (hb, ht, y0, y1, fc, ec), nm, sc, nt in zip(layers, names, scales, notes):
        quad = [(cx - hb, y0), (cx + hb, y0), (cx + ht, y1), (cx - ht, y1)]
        ax.add_patch(Polygon(quad, closed=True, facecolor=fc, edgecolor=ec, lw=1.1, zorder=2))
        cy = (y0 + y1) / 2
        ax.text(cx, cy + 0.34, nm, ha="center", va="center", fontsize=9.6,
                color=fs.INK, weight="bold", zorder=5)
        ax.text(cx, cy - 0.02, sc, ha="center", va="center", fontsize=9.0,
                color=fs.ACCENT, zorder=5)
        ax.text(cx, cy - 0.38, nt, ha="center", va="center", fontsize=8.2,
                color=fs.MUTED, zorder=5)

    # 右侧：代表数据集
    ax.text(5.05, 5.22, "代表数据集", ha="left", va="center", fontsize=9.0, color=fs.MUTED)
    rows = [
        (4.13, "DROID 350 h｜RoboMIND 305 h", "π0 自采约 1 万 h"),
        (2.79, "RoboCasa 10 万条", "GR00T 78 万条 ≈ 6500 h"),
        (1.45, "EPIC-KITCHENS 100 h", "网络视频百万小时级"),
    ]
    for cy, l1, l2 in rows:
        ax.text(5.05, cy + 0.17, l1, ha="left", va="center", fontsize=8.8, color=fs.INK)
        ax.text(5.05, cy - 0.17, l2, ha="left", va="center", fontsize=8.8, color=fs.MUTED)

    # 左侧箭头
    fs.arrow(ax, (0.42, 1.05), (0.42, 4.55), color=fs.FAINT, lw=1.0)
    ax.text(0.20, 2.80, "数量递减 · 单位成本递增", ha="center", va="center",
            fontsize=8.4, color=fs.MUTED, rotation=90)

    ax.text(0.55, 0.36, "量级为各论文公开数据的汇总估计，相邻两层相差约一个数量级。",
            ha="left", va="center", fontsize=8.4, color=fs.MUTED)
    fs.save(fig, "ch14", "fig14-01")


def fig_methods():
    """几种采集方式在规模、精度、成本上的相对位置（定性刻度）。"""
    fig, ax = fs.new(6.8, 4.2)
    fig.subplots_adjust(left=0.150, right=0.975, top=0.955, bottom=0.155)

    pts = [
        # 名称, 规模(小时), 精度档, 气泡大小, 标签位置, 对齐
        ("人类第一视角视频", 1e5, 1.0, 80, (1.35e5, 1.0), "left"),
        ("仿真", 1.1e4, 2.0, 420, (6.2e3, 1.52), "right"),
        ("动捕", 2.6e2, 4.3, 1300, (2.6e2, 5.14), "center"),
        ("VR 遥操作", 8e2, 3.0, 520, (6.0e2, 3.42), "right"),
        ("手持夹爪 UMI", 3.4e3, 3.85, 100, (4.4e3, 4.18), "left"),
        ("主从遥操作", 1.6e4, 4.95, 1500, (3.1e4, 5.28), "left"),
    ]
    colors = [fs.FAINT, fs.BLUE, fs.GOLD, fs.PURPLE, fs.GREEN, fs.ACCENT]
    for (nm, x, y, s, (tx, ty), ha), c in zip(pts, colors):
        ax.scatter([x], [y], s=s, color=c, alpha=0.26, edgecolor="none", zorder=2)
        ax.scatter([x], [y], s=26, color=c, edgecolor="white", linewidth=0.9, zorder=4)
        ax.text(tx, ty, nm, fontsize=8.8, color=fs.INK, ha=ha, va="center", zorder=5)

    ax.set_xscale("log")
    ax.set_xlim(6e1, 3e6)
    ax.set_ylim(0.30, 5.85)
    ax.set_xticks([1e2, 1e3, 1e4, 1e5])
    ax.set_xticklabels(["$10^2$", "$10^3$", "$10^4$", "$10^5$"])
    ax.set_xlabel("可获得的数据总量（小时，对数刻度）", fontsize=9.6)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["无动作标签", "近似物理", "厘米级", "毫米级", "本体一致"], fontsize=8.8)
    ax.set_ylabel("动作标签与部署机器人的一致性", fontsize=9.6)
    fs.clean(ax, grid=True, spines=("left", "bottom"))

    # 注释文字
    ax.text(4.4e3, 3.50, "实测 111 条 / 小时", fontsize=8.0, color=fs.GREEN,
            ha="left", va="center")
    ax.text(1.45e4, 2.56, "11 小时算出约 6500 小时", fontsize=8.2, color=fs.BLUE,
            ha="left", va="center")
    ax.text(1.35e5, 1.62, "有画面，没有动作", fontsize=8.0, color=fs.MUTED,
            ha="left", va="center")

    # 气泡大小图例
    x0 = 1.35e2
    for i, (s, lab) in enumerate([(100, "低"), (520, "中"), (1500, "高")]):
        ax.scatter([x0 * (2.4 ** i)], [0.72], s=s * 0.45, color=fs.MUTED, alpha=0.24,
                   edgecolor="none", zorder=2)
        ax.text(x0 * (2.4 ** i), 0.45, lab, fontsize=8.0, color=fs.MUTED,
                ha="center", va="center")
    ax.text(x0 * 9.2, 0.72, "气泡 ≈ 硬件与场地成本", fontsize=8.2, color=fs.MUTED,
            ha="left", va="center")
    fs.save(fig, "ch14", "fig14-02")


def fig_oxe():
    """Open X-Embodiment：本体分布（左）与技能长尾（右）。"""
    fig, axes = fs.new(7.0, 3.5, ncols=2)
    fig.subplots_adjust(left=0.135, right=0.978, top=0.930, bottom=0.140, wspace=0.54)

    # (a) 每个本体的数据集数量
    ax = axes[0]
    emb = ["Franka", "xArm", "Sawyer", "Google Robot", "Kuka iiwa", "UR5",
           "WidowX", "Hello Stretch", "PR2", "DLR SARA", "其余 12 种\n（各 1 个）"]
    cnt = [24, 6, 4, 3, 3, 3, 2, 2, 2, 2, 12]
    ypos = np.arange(len(emb))[::-1]
    for i, (y, v) in enumerate(zip(ypos, cnt)):
        c = fs.ACCENT if i == 0 else ("#B9C6DA" if i == len(emb) - 1 else fs.INK)
        ax.barh(y, v, height=0.62, color=c, edgecolor="none", zorder=3)
        ax.text(v + 0.55, y, f"{v}", ha="left", va="center", fontsize=8.2, color=fs.MUTED,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
    ax.set_yticks(ypos)
    ax.set_yticklabels(emb, fontsize=8.4)
    ax.set_xlim(0, 28)
    ax.set_xticks([0, 10, 20])
    ax.set_xlabel("数据集个数", fontsize=9.0)
    ax.text(0.01, 1.055, "(a) 本体分布", transform=ax.transAxes, fontsize=8.6, color=fs.MUTED)
    fs.clean(ax, grid=True, spines=("left", "bottom"))

    # (b) 语言标注中的技能分布（对数刻度）
    ax = axes[1]
    sk = ["picking", "moving", "pushing", "placing", "sliding",
          "putting", "navigating", "separating", "pointing"]
    val = [650, 159, 135, 118, 54, 37, 22, 21, 21]
    ypos = np.arange(len(sk))[::-1]
    for i, (y, v) in enumerate(zip(ypos, val)):
        c = fs.ACCENT if i == 0 else ("#C7D3E4" if v < 50 else fs.INK)
        ax.barh(y, v, height=0.62, color=c, edgecolor="none", zorder=3)
        ax.text(v * 1.14, y, f"{v}", ha="left", va="center", fontsize=8.2, color=fs.MUTED,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
    ax.set_yticks(ypos)
    ax.set_yticklabels(sk, fontsize=8.4)
    ax.set_xscale("log")
    ax.set_xlim(8, 3200)
    ax.set_xticks([10, 100, 1000])
    ax.set_xticklabels(["10", "100", "1000"])
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel("标注次数（千条，对数刻度）", fontsize=9.0)
    ax.text(0.01, 1.055, "(b) 技能分布", transform=ax.transAxes, fontsize=8.6, color=fs.MUTED)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    fs.save(fig, "ch14", "fig14-03")


if __name__ == "__main__":
    fig_pyramid()
    fig_methods()
    fig_oxe()
