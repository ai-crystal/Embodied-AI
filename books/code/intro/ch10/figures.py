# -*- coding: utf-8 -*-
"""第 10 章插图：训练环路、并行环境数与时长、sim2real 差距五来源。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
import figstyle as fs


def fig_loop():
    """训练 -> 评估 -> 部署 -> 回流 的四站环路。"""
    fig, ax = fs.canvas(6.6, 4.0)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)

    W, H = 3.30, 1.30
    boxes = [
        (0.55, 4.85, "训练\n显卡上跑几千个环境", fs.BLUE, "#EFF4FC"),
        (6.15, 4.85, "评估\n固定种子 + 随机种子", fs.TEAL, "#ECF6F4"),
        (6.15, 0.95, "部署\n真机零样本先跑降级版", fs.ACCENT, "#FDF1E6"),
        (0.55, 0.95, "回流\n看录像 · 标失败 · 改参数", fs.PURPLE, "#F3F0FB"),
    ]
    for x, y, text, ec, fc in boxes:
        fs.box(ax, x, y, W, H, text, fs=8.8, ec=ec, fc=fc, lw=1.2)

    # 上：训练 -> 评估
    fs.arrow(ax, (3.93, 5.50), (6.07, 5.50), color=fs.MUTED)
    ax.text(5.00, 5.70, "策略快照", ha="center", va="bottom", fontsize=8.2, color=fs.MUTED)

    # 右：评估 -> 部署
    fs.arrow(ax, (7.80, 4.77), (7.80, 2.33), color=fs.MUTED)
    ax.text(7.95, 3.55, "通过才上机", ha="left", va="center", fontsize=8.2, color=fs.MUTED)

    # 下：部署 -> 回流
    fs.arrow(ax, (6.07, 1.60), (3.93, 1.60), color=fs.ACCENT)
    ax.text(5.00, 1.40, "每次失败一段录像", ha="center", va="top", fontsize=8.2, color=fs.ACCENT)

    # 左：回流 -> 训练
    fs.arrow(ax, (2.20, 2.33), (2.20, 4.77), color=fs.PURPLE)
    ax.text(2.05, 3.55, "参数进随机化", ha="right", va="center", fontsize=8.2, color=fs.PURPLE)

    ax.text(5.00, 3.62, "一圈的时间由最贵的一站决定", ha="center", va="center",
            fontsize=10.5, color=fs.INK)
    ax.text(5.00, 3.14, "训练按 GPU 小时算，部署按人天算", ha="center", va="center",
            fontsize=8.4, color=fs.MUTED)
    ax.text(5.00, 2.72, "回流最便宜也最容易被跳过", ha="center", va="center",
            fontsize=8.4, color=fs.MUTED)
    fs.save(fig, "ch10", "fig10-01")


def fig_speed():
    """并行环境数与训练时长（数据取自 Isaac Gym 论文第 5 节）。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.35),
                             gridspec_kw={"width_ratios": [1.28, 1.0], "wspace": 0.42})
    ax, ax2 = axes

    data = [
        ("Shadow Hand", [(256, 5.0e4), (16384, 3.0e3)], fs.ACCENT,
         ("14 小时", (2, 8, "left", "bottom")), ("1 小时", (2, 8, "left", "bottom"))),
        ("Humanoid", [(256, 1.0e4), (4096, 1.0e3)], fs.BLUE,
         ("2.7 小时", (2, 8, "left", "bottom")), ("17 分钟", (2, 9, "left", "bottom"))),
        ("Ant", [(256, 1.0e3), (8192, 1.0e2)], fs.GREEN,
         ("17 分钟", (2, -9, "left", "top")), ("100 秒", (2, 8, "left", "bottom"))),
    ]
    for name, pts, c, lab0, lab1 in data:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, "-", color=c, lw=1.4, zorder=2, label=name)
        ax.scatter(xs, ys, s=28, color=c, zorder=3, edgecolor="white", linewidth=0.8)
        for (x, y), (txt, (dx, dy, ha, va)) in zip(pts, (lab0, lab1)):
            ax.annotate(txt, (x, y), textcoords="offset points", xytext=(dx, dy),
                        fontsize=8.0, color=c, ha=ha, va=va, zorder=4)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(170, 3.4e4)
    ax.set_ylim(50, 2.4e5)
    ax.set_xticks([256, 1024, 4096, 16384])
    ax.set_xticklabels(["256", "1k", "4k", "16k"])
    ax.set_yticks([1e2, 1e3, 1e4, 1e5])
    ax.set_yticklabels(["$10^2$", "$10^3$", "$10^4$", "$10^5$"])
    ax.set_xlabel("并行环境数", fontsize=9)
    ax.set_ylabel("训练到目标分数的时间（秒）", fontsize=9)
    fs.clean(ax, grid=True)
    ax.legend(loc="upper right", fontsize=8.0, handlelength=1.4, borderpad=0.25,
              labelspacing=0.35)
    ax.text(-0.02, 1.03, "(a)", transform=ax.transAxes, fontsize=9, color=fs.INK,
            ha="left", va="bottom")

    # (b) 同一模仿任务：CPU 集群与单卡
    names = ["PyBullet\n16 个 CPU 核", "Isaac Gym\n1 张 A100"]
    hours = [30.0, 0.1]
    colors = [fs.FAINT, fs.ACCENT]
    ypos = [1.0, 0.0]
    ax2.barh(ypos, hours, height=0.40, color=colors, edgecolor="white", zorder=2)
    ax2.set_xscale("log")
    ax2.set_xlim(0.04, 260)
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(names, fontsize=8.2)
    ax2.set_xlabel("训练耗时（小时，对数轴）", fontsize=9)
    ax2.set_xticks([0.1, 1, 10, 100])
    ax2.set_xticklabels(["0.1", "1", "10", "100"])
    fs.clean(ax2, grid=True)
    ax2.set_ylim(-0.66, 1.78)
    ax2.text(30 * 1.15, 1.0, "30 小时", va="center", ha="left", fontsize=8.4, color=fs.INK)
    ax2.text(0.1 * 1.2, 0.0, "6 分钟", va="center", ha="left", fontsize=8.4, color=fs.INK)
    ax2.text(0.048, 1.60, "同一模仿任务，3900 万样本", fontsize=8.0, color=fs.MUTED,
             ha="left", va="center")
    ax2.text(0.048, 1.34, "单卡比 16 核 CPU 快 300 倍", fontsize=8.0, color=fs.MUTED,
             ha="left", va="center")
    ax2.text(-0.02, 1.03, "(b)", transform=ax2.transAxes, fontsize=9, color=fs.INK,
             ha="left", va="bottom")

    fig.subplots_adjust(left=0.135, right=0.98, top=0.90, bottom=0.20)
    fs.save(fig, "ch10", "fig10-02")


def fig_gap():
    """仿真假设、真机实际、常用对策 三列五行。"""
    fig, ax = fs.canvas(6.9, 4.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.0)

    cA, wA = 0.22, 2.72
    cB, wB = 3.42, 3.16
    cC, wC = 7.10, 2.68
    rows = [
        ("接触模型", "点接触 + 线性弹簧", "橡胶指尖受力变形，接触面长大", "随机化接触刚度"),
        ("摩擦", "单一库仑系数", "随速度、湿度变化，静摩擦更大", "随机化摩擦区间"),
        ("执行器", "理想力矩源或简单 PD", "减速器间隙、齿隙、温升衰减", "辨识后挂执行器网络"),
        ("传感噪声", "干净信号，少量高斯噪声", "量化、漂移，深度有空洞", "给观测加有结构的噪声"),
        ("延迟", "默认零延迟", "端到端 10 到 40 ms", "显式延迟 1 到 5 步"),
    ]

    hy, hh = 6.42, 0.50
    heads = [(cA, wA, "仿真里的假设", fs.BLUE, "#EFF4FC"),
             (cB, wB, "真机上发生什么", fs.ACCENT, "#FDF1E6"),
             (cC, wC, "常用对策", fs.GREEN, "#ECF6F2")]
    for x, w, text, ec, fc in heads:
        fs.box(ax, x, hy, w, hh, text, fs=9.0, ec=ec, fc=fc, weight="bold", tc=ec)

    for i, (kw, sim, real, fix) in enumerate(rows):
        y = 5.52 - i * 1.02
        fs.box(ax, cA, y, wA, 0.84, "", fc="#FFFFFF", ec=fs.FAINT, lw=0.9)
        ax.text(cA + 0.10, y + 0.56, kw, ha="left", va="center", fontsize=8.6,
                color=fs.INK, weight="bold")
        ax.text(cA + 0.10, y + 0.25, sim, ha="left", va="center", fontsize=8.0, color=fs.MUTED)

        fs.box(ax, cB, y, wB, 0.84, "", fc="#FFFFFF", ec="#D9C7B8", lw=0.9)
        ax.text(cB + 0.14, y + 0.42, real, ha="left", va="center", fontsize=8.3, color=fs.INK)

        fs.box(ax, cC, y, wC, 0.84, "", fc="#FFFFFF", ec=fs.GREEN, lw=0.9)
        ax.text(cC + 0.12, y + 0.42, fix, ha="left", va="center", fontsize=8.3, color=fs.GREEN)

        fs.arrow(ax, (cA + wA + 0.03, y + 0.42), (cB - 0.04, y + 0.42),
                 color=fs.ACCENT, lw=0.9, ms=6)
        fs.arrow(ax, (cB + wB + 0.03, y + 0.42), (cC - 0.04, y + 0.42),
                 color=fs.GREEN, lw=0.9, ls=(0, (3, 2)), ms=6)

    fy = 0.58
    fs.arrow(ax, (0.28, fy), (0.66, fy), color=fs.ACCENT, lw=0.9, ms=6)
    ax.text(0.76, fy, "差距来源", ha="left", va="center", fontsize=8.2, color=fs.MUTED)
    fs.arrow(ax, (2.24, fy), (2.62, fy), color=fs.GREEN, lw=0.9, ls=(0, (3, 2)), ms=6)
    ax.text(2.72, fy, "对应补法", ha="left", va="center", fontsize=8.2, color=fs.MUTED)
    ax.text(4.90, fy, "五处偏差里，延迟最便宜也最容易被漏掉", ha="left", va="center",
            fontsize=8.2, color=fs.MUTED)
    fs.save(fig, "ch10", "fig10-03")


if __name__ == "__main__":
    fig_loop()
    fig_speed()
    fig_gap()
