# -*- coding: utf-8 -*-
"""第 21 章插图：能力与可靠性的差距、研究前沿地图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_gap():
    """成功率随任务时长衰减的区间，与演示 / 产品两条门槛线（示意）。"""
    fig, ax = fs.new(6.6, 3.9)
    ax.set_xscale("log")
    ax.set_xlim(8, 40000)
    ax.set_ylim(0, 115)

    xs = np.array([10, 60, 600, 3600, 28800], float)
    hi = np.array([95.0, 88.0, 73.0, 43.0, 13.0])
    lo = np.array([88.0, 74.0, 50.0, 21.0, 4.0])
    gx = np.logspace(np.log10(10), np.log10(28800), 200)
    ghi = np.interp(np.log10(gx), np.log10(xs), hi)
    glo = np.interp(np.log10(gx), np.log10(xs), lo)

    ax.fill_between(gx, glo, ghi, color="#DCE7F5", alpha=0.95,
                    edgecolor=fs.BLUE, lw=1.0, zorder=2)
    ax.plot([9.4], [109], marker="s", ms=8, color="#DCE7F5",
            markeredgecolor=fs.BLUE, markeredgewidth=1.0, zorder=6, clip_on=False)
    ax.text(11.0, 109, "当前公开系统的典型区间", ha="left", va="center",
            fontsize=8.4, color=fs.BLUE, zorder=6)

    ax.axhline(50, color=fs.MUTED, ls=(0, (4, 3)), lw=1.2, zorder=3)
    ax.axhline(99, color=fs.ACCENT, ls=(0, (4, 3)), lw=1.2, zorder=3)
    ax.text(9, 53.5, "演示可接受 50%", ha="left", va="bottom",
            fontsize=8.6, color=fs.MUTED)
    ax.text(31000, 101.5, "产品要求 99%", ha="right", va="bottom",
            fontsize=8.6, color=fs.ACCENT)

    # 右侧差距双向箭头
    ax.annotate("", xy=(20000, 97.5), xytext=(20000, 18.0),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=1.2,
                                shrinkA=0, shrinkB=0))
    ax.text(18000, 72, "同一时长\n相差约 5 倍", ha="right", va="center",
            fontsize=8.4, color=fs.ACCENT, linespacing=1.6)

    ax.set_xticks([10, 60, 600, 3600, 28800])
    ax.set_xticklabels(["10 秒", "1 分", "10 分", "1 小时", "8 小时"])
    ax.minorticks_off()
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("连续执行的任务时长", fontsize=9.5)
    ax.set_ylabel("单次任务成功率 / %", fontsize=9.5)
    fs.clean(ax)
    ax.grid(axis="y", color=fs.GRID, lw=0.7)
    ax.set_axisbelow(True)
    fs.save(fig, "ch21", "fig21-01")


def fig_map():
    """五个分区的研究前沿地图，每区四个具体问题。"""
    fig, ax = fs.canvas(6.6, 4.5)
    ax.set_xlim(-0.03, 10.03)
    ax.set_ylim(0.04, 6.56)

    regions = [
        ("感知", fs.PURPLE, ["透明物体的\n深度缺失", "接触与滑移\n在视觉不可见",
                             "变形物体的\n状态估计", "开放词汇的\n三维建图"]),
        ("学习", fs.BLUE, ["跨本体的\n动作表示", "长程任务的\n信用分配",
                           "新任务的\n少样本适应", "世界模型的\n接触精度"]),
        ("控制", fs.GREEN, ["力控在高速\n下失稳", "多指手的\n手内操作",
                            "柔顺物体的\n力位混合", "全身协调\n与平衡约束"]),
        ("数据", fs.GOLD, ["真机数据的\n采集成本", "人类视频的\n动作标注",
                           "数据质量的\n自动筛选", "跨机构数据\n口径统一"]),
        ("评测", fs.ACCENT, ["真机评测的\n可复现性", "长程任务的\n部分完成度",
                             "仿真与真机\n排名一致", "安全失效的\n量化指标"]),
    ]

    pw, gap, x0 = 1.84, 0.20, 0.02
    py, ph = 0.30, 6.10
    for i, (name, color, items) in enumerate(regions):
        x = x0 + i * (pw + gap)
        fs.box(ax, x, py, pw, ph, "", fc="#FCFCFD", ec=fs.GRID, lw=1.0, rounded=0.04)
        # 分区标题
        fs.box(ax, x, py + ph - 0.58, pw, 0.58, "", fc=color, ec=color, lw=1.0, rounded=0.04)
        ax.text(x + pw / 2, py + ph - 0.29, name, ha="center", va="center",
                fontsize=10.2, color="white", weight="bold", zorder=6)
        # 四个问题
        ih, ig = 1.13, 0.22
        for j, txt in enumerate(items):
            iy = py + ph - 0.58 - 0.24 - ih - j * (ih + ig)
            fs.box(ax, x + 0.09, iy, pw - 0.18, ih, txt, fc="white",
                   ec=color, lw=0.9, fs=8.2, rounded=0.03, tc=fs.INK)
    fs.save(fig, "ch21", "fig21-02")


if __name__ == "__main__":
    fig_gap()
    fig_map()
