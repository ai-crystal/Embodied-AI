# -*- coding: utf-8 -*-
"""第 20 章插图：基准谱系、置信区间随试验次数的收缩、评测的三层。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import beta, binom
import figstyle as fs


def fig_landscape():
    """基准谱系：横轴任务长度，纵轴仿真到真机。"""
    fig, ax = plt.subplots(figsize=(6.6, 4.1))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.9)
    fs.clean(ax, spines=("left", "bottom"))
    ax.set_xticks([])
    ax.set_yticks([])

    # 两条背景带：仿真区与真机区
    ax.add_patch(Rectangle((0.08, 0.25), 9.84, 3.05, facecolor="#F4F7FB",
                           edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0.08, 5.95), 9.84, 2.35, facecolor="#FDF5F0",
                           edgecolor="none", zorder=0))
    ax.text(0.28, 3.02, "仿真基准", fontsize=8.2, color=fs.FAINT, ha="left", va="top")
    ax.text(0.28, 8.02, "真机评测", fontsize=8.2, color=fs.FAINT, ha="left", va="top")

    ax.set_xlabel("单步任务　→　多阶段长程任务", fontsize=9.4, color=fs.INK, labelpad=6)
    ax.set_ylabel("仿真　→　真机", fontsize=9.4, color=fs.INK, labelpad=6)

    # (x, y, 名称, 颜色, 标签方位)
    pts = [
        (0.85, 1.35, "Meta-World", fs.BLUE, "right"),
        (2.25, 2.55, "RLBench", fs.BLUE, "right"),
        (3.55, 1.00, "LIBERO", fs.BLUE, "right"),
        (5.15, 2.55, "CALVIN", fs.BLUE, "right"),
        (6.55, 1.00, "RoboCasa", fs.BLUE, "right"),
        (8.05, 2.55, "BEHAVIOR-1K", fs.BLUE, "above"),
    ]
    for x, y, name, c, side in pts:
        ax.scatter([x], [y], s=34, color=c, edgecolor="white", linewidth=0.9, zorder=4)
        if side == "right":
            ax.text(x + 0.22, y, name, fontsize=8.6, color=fs.INK, ha="left", va="center")
        else:
            ax.text(x, y + 0.42, name, fontsize=8.6, color=fs.INK, ha="center", va="bottom")

    # SimplerEnv：真机策略、仿真执行，落在中间地带
    ax.scatter([4.45], [4.45], s=40, facecolor="white", edgecolor=fs.PURPLE,
               linewidth=1.2, zorder=4)
    ax.text(4.72, 4.62, "SimplerEnv", fontsize=8.6, color=fs.PURPLE, ha="left", va="bottom")
    ax.text(4.72, 4.18, "真机策略，仿真执行", fontsize=8.0, color=fs.MUTED, ha="left", va="top")

    # RoboArena：多机构真机分布式评测
    ax.scatter([3.30], [7.15], s=34, color=fs.ACCENT, edgecolor="white", linewidth=0.9, zorder=4)
    ax.text(3.58, 7.32, "RoboArena", fontsize=8.6, color=fs.INK, ha="left", va="bottom")
    ax.text(3.58, 6.88, "多机构同一协议", fontsize=8.0, color=fs.MUTED, ha="left", va="top")
    fs.save(fig, "ch20", "fig20-01")


def fig_ci_width():
    """二项分布 95% 置信区间宽度随试验次数的变化（Clopper-Pearson 精确区间）。

    纵轴是区间的期望宽度：把每个可能的成功次数按二项概率加权平均，
    这样曲线才平滑，也才能看出宽度的收缩速度。
    """
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    fs.clean(ax, spines=("left", "bottom"))

    def cp_width(k, n):
        lo = beta.ppf(0.025, k, n - k + 1) if k > 0 else 0.0
        hi = beta.ppf(0.975, k + 1, n - k) if k < n else 1.0
        return (hi - lo) * 100.0

    ns = np.arange(5, 201)
    for p, c, lab in ((0.9, fs.ACCENT, "真实成功率 0.90"), (0.8, fs.BLUE, "真实成功率 0.80")):
        w = []
        for n in ns:
            ks = np.arange(n + 1)
            pm = binom.pmf(ks, n, p)
            w.append(float((pm * np.array([cp_width(k, n) for k in ks])).sum()))
        ax.plot(ns, w, color=c, lw=1.4, label=lab, zorder=3)
        for n in (20, 50, 100, 200):
            ax.plot([n], [w[n - 5]], "o", ms=4.2, color=c,
                    markeredgecolor="white", markeredgewidth=0.8, zorder=4)

    ax.axvline(20, color=fs.FAINT, lw=0.9, ls=(0, (2, 2)), zorder=1)
    ax.text(21.5, 3.0, "20 次", fontsize=8.4, color=fs.MUTED, ha="left", va="bottom")
    ax.axhline(10, color=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.text(203, 6.6, "10 个百分点", fontsize=8.2, color=fs.MUTED, ha="right", va="top")

    ax.annotate("约 29 个百分点", xy=(20, 29.2), xytext=(34, 34),
                fontsize=8.4, color=fs.ACCENT, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.8,
                                shrinkA=2, shrinkB=4))
    ax.annotate("5 次试验：约 61 个百分点", xy=(6.0, 58.5), xytext=(34, 58.5),
                fontsize=8.4, color=fs.MUTED, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=fs.FAINT, lw=0.8,
                                shrinkA=2, shrinkB=4))

    ax.set_xlim(0, 205)
    ax.set_ylim(0, 78)
    ax.set_xlabel("同一策略的试验次数 n", fontsize=9.4)
    ax.set_ylabel("95% 置信区间期望宽度 / 百分点", fontsize=9.4)
    ax.set_yticks([0, 20, 40, 60])
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0), fontsize=8.6)
    fs.save(fig, "ch20", "fig20-02")


def fig_three_layers():
    """评测的三层：组件、任务、系统，各自能回答什么问题。"""
    fig, ax = fs.canvas(6.6, 3.7)
    ax.set_xlim(0, 9.95)
    ax.set_ylim(0.45, 6.05)

    heads = [("评测对象", 0.10), ("能回答的问题", 2.85), ("典型指标", 6.25)]
    for text, x in heads:
        ax.text(x + 0.10, 5.88, text, fontsize=8.4, color=fs.MUTED, ha="left", va="center")

    rows = [
        ("组件层", "感知 · 抓取 · 规划",
         "这个模块单独拿出来，\n精度和速度够不够用？",
         "位姿误差、检测召回率、\n规划成功率与耗时", "#EEF2F8", fs.BLUE),
        ("任务层", "策略 · 技能 · 语言条件",
         "给定任务和初始状态，\n它能不能做完？",
         "成功率、部分完成度、\n干预次数", "#F7F1EA", fs.GOLD),
        ("系统层", "整机 · 长时间运行",
         "连续跑一周，\n它会不会自己停下来？",
         "MTBF、零干预时长、\n故障后恢复成功率", "#F5EFF6", fs.PURPLE),
    ]
    h = 1.42
    for i, (name, obj, ques, metric, fc, ec) in enumerate(rows):
        y = 4.05 - i * (h + 0.22)
        fs.box(ax, 0.10, y, 2.55, h, "", fc=fc, ec=ec, lw=0.9)
        ax.text(0.26, y + h - 0.30, name, fontsize=9.4, color=fs.INK, ha="left",
                va="center", weight="bold")
        ax.text(0.26, y + 0.34, obj, fontsize=8.0, color=fs.MUTED, ha="left", va="center")
        fs.box(ax, 2.85, y, 3.20, h, ques, fc="#FFFFFF", ec="#CBD5E1", fs=8.5)
        fs.box(ax, 6.25, y, 3.55, h, metric, fc="#FFFFFF", ec="#CBD5E1", fs=8.5)

    fs.save(fig, "ch20", "fig20-03")


if __name__ == "__main__":
    fig_landscape()
    fig_ci_width()
    fig_three_layers()
