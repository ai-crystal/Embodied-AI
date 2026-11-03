# -*- coding: utf-8 -*-
"""第 13 章插图：VLA 数据通路、四种动作头、实时性时间线。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import figstyle as fs


def fig_arch():
    """VLA 通路：图像 + 指令 -> 主干 -> 动作专家 -> 动作块 -> 控制器。"""
    fig, ax = fs.canvas(6.6, 3.9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.4)

    y0, h = 2.95, 1.15
    stages = [
        (0.15, 1.50, "相机图像\n224×224×3\n30 Hz", fs.BLUE),
        (1.95, 1.50, "视觉塔 ViT\n256×1024\n一次前向", fs.TEAL),
        (3.75, 1.70, "语言主干 7B\n32 层 · 4096\n5 Hz 级", fs.PURPLE),
        (5.85, 1.55, "动作专家\n交叉注意力\n10 步采样", fs.ACCENT),
        (7.70, 1.90, "动作块\n50×7\n50 Hz 回放", fs.GREEN),
    ]
    for x, w, txt, c in stages:
        fs.box(ax, x, y0, w, h, txt, fc="white", ec=c, tc=fs.INK, fs=8.6, lw=1.1)
        ax.text(x + w / 2, y0 + h + 0.09, "", fontsize=8)

    # 阶段之间的箭头
    for i in range(len(stages) - 1):
        xa = stages[i][0] + stages[i][1]
        xb = stages[i + 1][0]
        fs.arrow(ax, (xa + 0.02, y0 + h / 2), (xb - 0.02, y0 + h / 2), color=fs.FAINT, lw=1.1)

    # 指令框
    fs.box(ax, 3.55, 4.28, 2.10, 0.86, "指令\n「红杯子放进盘子」", fc=fs.PAPER,
           ec=fs.PURPLE, fs=8.2, lw=0.9)
    fs.arrow(ax, (4.60, 4.27), (4.60, y0 + h + 0.03), color=fs.PURPLE, lw=1.0)

    # 控制器
    fs.box(ax, 7.30, 0.52, 2.30, 0.72, "关节控制器 1 kHz\n插值 · 力矩限幅", fc="white",
           ec=fs.GOLD, fs=8.4, lw=1.1)
    fs.arrow(ax, (8.65, y0 - 0.02), (8.65, 1.26), color=fs.GOLD, lw=1.1)

    # 闭环：控制器 -> 下一帧
    ax.plot([7.28, 0.90], [0.88, 0.88], color=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=2)
    fs.arrow(ax, (0.90, 0.88), (0.90, y0 - 0.02), color=fs.FAINT, lw=0.9)
    ax.text(3.55, 0.98, "下一帧图像，33 ms 之后", ha="center", va="bottom",
            fontsize=8.0, color=fs.MUTED)

    ax.text(1.40, 2.18, "块内开环执行\n块间闭环校正", ha="left", va="center",
            fontsize=8.6, color=fs.MUTED, linespacing=1.6)

    fs.save(fig, "ch13", "fig13-01")


def fig_heads():
    """四种动作头的结构小图，统一三节点版式。"""
    fig, axes = plt.subplots(2, 2, figsize=(6.6, 3.95))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.03,
                        wspace=0.06, hspace=0.20)
    panels = [
        ("(a) 离散 token", "h_t", "7 × 256 类\n交叉熵", "一次前向 · 精度 1/256",
         fs.BLUE, "格子"),
        ("(b) 连续回归", "h_t", "MLP\nL1 回归", "一次前向 · 会平均掉多峰",
         fs.TEAL, "实数"),
        ("(c) 扩散头", "h_t ⊕ ε", "去噪 K 步\n每步一次前向", "K 次前向 · 保留多峰",
         fs.ACCENT, "实数"),
        ("(d) Flow matching", "h_t ⊕ ε", "速度场积分\n10 步欧拉", "10 次前向 · 保留多峰",
         fs.GREEN, "实数"),
    ]
    for ax, (title, src, body, cost, c, kind) in zip(axes.ravel(), panels):
        ax.set_xlim(0, 10)
        ax.set_ylim(1.62, 5.60)
        ax.axis("off")
        ax.text(0.15, 5.42, title, ha="left", va="center", fontsize=8.8,
                color=fs.INK, weight="bold")

        fs.box(ax, 0.25, 2.55, 1.75, 1.20, src, fc=fs.LIGHT, ec=fs.MUTED, fs=8.2, lw=0.9)
        fs.arrow(ax, (2.02, 3.15), (2.34, 3.15), color=fs.MUTED, lw=1.0)
        fs.box(ax, 2.35, 2.35, 3.55, 1.60, body, fc="white", ec=c, fs=8.4, lw=1.2)

        # 中间输出示意：离散画格线，连续画平滑曲线
        if kind == "格子":
            ax.plot([6.05, 8.35], [3.15, 3.15], color=fs.GRID, lw=1.0, zorder=1)
            for t in np.linspace(6.05, 8.35, 9):
                ax.plot([t, t], [3.00, 3.30], color=fs.FAINT, lw=0.8, zorder=1)
            ax.scatter([6.60], [3.15], s=26, color=c, zorder=4)
        else:
            xs = np.linspace(6.05, 8.35, 40)
            ax.plot(xs, 3.12 + 0.16 * np.sin((xs - 6.05) * 3.4), color=c, lw=1.2, zorder=2)
            ax.scatter([7.20], [3.12 + 0.16 * np.sin((7.20 - 6.05) * 3.4)], s=26, color=c, zorder=4)

        fs.arrow(ax, (8.38, 3.15), (8.66, 3.15), color=fs.MUTED, lw=1.0)
        fs.box(ax, 8.68, 2.72, 1.20, 0.86, "Â", fc="white", ec=fs.INK, fs=9.2, lw=1.1)
        ax.text(4.95, 1.95, cost, ha="center", va="center", fontsize=8.0, color=fs.MUTED)

    fs.save(fig, "ch13", "fig13-02")


def fig_timing():
    """三条时间轴：相机 30 Hz、策略推理与块执行、控制 1 kHz。"""
    fig, ax = fs.canvas(6.6, 3.5)
    ax.set_xlim(-118, 560)
    ax.set_ylim(0.55, 6.35)

    # 相机 30 Hz
    yb = 5.05
    for t in range(0, 520, 33):
        ax.plot([t, t], [yb, yb + 0.42], color=fs.BLUE, lw=1.0, zorder=3)
    ax.annotate("", xy=(33, yb + 0.56), xytext=(66, yb + 0.56),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8))
    ax.text(49.5, yb + 0.64, "33 ms", ha="center", va="bottom",
            fontsize=8.0, color=fs.MUTED)
    ax.text(-14, yb + 0.21, "相机 30 Hz", ha="right", va="center",
            fontsize=8.6, color=fs.BLUE)

    # 策略推理
    yi = (3.85, 4.25)
    for a, b in [(0, 161), (167, 328), (334, 495)]:
        ax.add_patch(Rectangle((a, yi[0]), b - a, yi[1] - yi[0],
                               facecolor=fs.ACCENT, alpha=0.16, edgecolor=fs.ACCENT,
                               lw=0.9, zorder=2))
    ax.text(-14, 4.05, "推理 167 ms", ha="right", va="center",
            fontsize=8.6, color=fs.ACCENT)

    # 块执行
    ye = (3.20, 3.60)
    ax.add_patch(Rectangle((167, ye[0]), 320, ye[1] - ye[0],
                           facecolor=fs.GREEN, alpha=0.16, edgecolor=fs.GREEN,
                           lw=0.9, zorder=2))
    ax.add_patch(Rectangle((334, ye[0]), 153, ye[1] - ye[0],
                           facecolor="white", alpha=0.72, edgecolor=fs.GREEN, lw=0.8,
                           ls=(0, (3, 2)), hatch="///", zorder=3))
    ax.text(410.5, 3.40, "块 2 等待", ha="center", va="center", fontsize=7.8,
            color=fs.MUTED, zorder=5,
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.92))
    ax.text(-14, 3.40, "块执行 320 ms", ha="right", va="center",
            fontsize=8.6, color=fs.GREEN)

    for t in (167, 487):
        ax.plot([t, t], [3.16, 4.32], color=fs.FAINT, lw=0.8, ls=(0, (3, 3)), zorder=1)

    # 曝光到首动作
    ax.annotate("", xy=(167, 2.92), xytext=(0, 2.92),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8))
    ax.text(83, 2.99, "曝光到首动作 167 ms", ha="center", va="bottom",
            fontsize=8.0, color=fs.MUTED)

    # 控制环
    yc = (1.62, 2.26)
    ax.add_patch(Rectangle((0, yc[0]), 500, yc[1] - yc[0],
                           facecolor=fs.LIGHT, edgecolor=fs.GRID, lw=0.8, zorder=2))
    for t in range(0, 501, 25):
        ax.plot([t, t], [yc[0] + 0.16, yc[1] - 0.10], color=fs.GOLD, lw=0.7, zorder=3)
    ax.text(-14, (yc[0] + yc[1]) / 2, "控制 1 kHz", ha="right", va="center",
            fontsize=8.6, color=fs.GOLD)
    ax.text(0, 1.40, "实际每 1 ms 一轮，此处每 25 ms 画一格", ha="left", va="center",
            fontsize=7.8, color=fs.MUTED)

    # 执行 -> 控制
    fs.arrow(ax, (430, 3.16), (430, yc[1] + 0.05), color=fs.GOLD, lw=1.0)
    ax.text(438, 2.70, "期望位姿", ha="left", va="center",
            fontsize=7.8, color=fs.GOLD)

    # 时间轴
    ax.plot([0, 500], [1.05, 1.05], color=fs.INK, lw=1.0, zorder=2)
    for t in range(0, 501, 100):
        ax.plot([t, t], [1.05, 0.93], color=fs.INK, lw=0.9, zorder=2)
        ax.text(t, 0.82, str(t), ha="center", va="top", fontsize=8.0, color=fs.MUTED)
    ax.text(517, 0.82, "ms", ha="left", va="top", fontsize=8.0, color=fs.MUTED)

    fs.save(fig, "ch13", "fig13-03")


if __name__ == "__main__":
    fig_arch()
    fig_heads()
    fig_timing()
