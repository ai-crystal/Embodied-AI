# -*- coding: utf-8 -*-
"""第 9 章插图：协变量偏移、遥操作数据链路、扩散动作生成。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import figstyle as fs


def fig_covariate():
    """专家轨迹与学到的策略轨迹，偏差随步数放大。"""
    fig, ax = fs.new(6.6, 3.9)
    fs.clean(ax, grid=True)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 30)

    t = np.linspace(0, 1, 400)
    ex = 4 + 52 * t
    ey = 6 + 16 * t + 4 * np.sin(np.pi * t)
    drift = 12 * t ** 2.6
    ly = ey - drift

    # 训练数据覆盖的状态带
    ax.fill_between(ex, ey - 1.3, ey + 1.3, color=fs.GRID, alpha=0.85, zorder=1, lw=0)
    ax.plot(ex, ey, color=fs.INK, lw=1.4, zorder=4)
    ax.plot(ex, ly, color=fs.ACCENT, lw=1.4, zorder=4, ls=(0, (5, 1.6)))

    ax.plot([ex[0]], [ey[0]], "o", ms=6, mfc="white", mec=fs.INK, mew=1.2, zorder=6)
    ax.text(ex[0] + 1.2, ey[0] - 2.6, "同一初始状态", fontsize=8.6, color=fs.MUTED,
            ha="left", va="center")

    # 偏差标注
    marks = [(0.40, "1 cm", 1), (0.70, "5 cm", 1), (1.00, "12 cm", -1)]
    for frac, lab, side in marks:
        i = int(round(frac * (len(t) - 1)))
        x0, y_top, y_bot = ex[i], ey[i], ly[i]
        ax.annotate("", xy=(x0, y_top - 0.5), xytext=(x0, y_bot + 0.5),
                    arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=0.9,
                                    shrinkA=0, shrinkB=0, mutation_scale=7))
        ax.plot([x0], [y_bot], "o", ms=3.2, color=fs.ACCENT, zorder=6)
        if side > 0:
            ax.text(x0 + 1.2, y_bot - 1.9, lab, fontsize=8.2, color=fs.ACCENT,
                    ha="left", va="center")
        else:
            ax.text(x0 - 1.3, (y_top + y_bot) / 2, lab, fontsize=8.2, color=fs.ACCENT,
                    ha="right", va="center")

    ax.text(46, 25.4, "专家轨迹", fontsize=9.4, color=fs.INK, ha="left", va="center")
    ax.text(48.5, 6.6, "学到的策略", fontsize=9.4, color=fs.ACCENT, ha="left", va="center")
    ax.text(6.5, 27.4, "灰色带：训练数据覆盖的状态", fontsize=8.6, color=fs.MUTED,
            ha="left", va="center")
    ax.annotate("观测落到带外\n策略开始猜", xy=(45.5, 13.6), xytext=(29.0, 2.6),
                fontsize=8.4, color=fs.MUTED, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=1.0,
                                connectionstyle="arc3,rad=-0.16"))

    ax.set_xlabel("桌面横向位置 / cm")
    ax.set_ylabel("纵向 / cm")
    ax.tick_params(length=3)
    fs.save(fig, "ch09", "fig09-01")


def fig_teleop():
    """遥操作采集链路与时间戳对齐。"""
    fig, ax = fs.canvas(6.6, 3.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.62)

    # 人
    fs.human(ax, cx=0.62, cy=3.35, s=0.72, color=fs.INK, z=3)
    ax.text(0.62, 4.16, "操作者", fontsize=8.8, color=fs.INK, ha="center", va="center")

    # 三个箱体
    y, h = 3.05, 1.00
    fs.box(ax, 1.75, y, 1.62, h, "主手\n读取关节角", fs=8.8, ec=fs.BLUE)
    fs.box(ax, 3.92, y, 1.62, h, "从手\n跟随同一角度", fs=8.8, ec=fs.BLUE)
    fs.box(ax, 6.08, y, 1.55, h, "相机\n俯视工作区", fs=8.8, ec=fs.GREEN)

    fs.arrow(ax, (0.95, 3.55), (1.72, 3.55), color=fs.MUTED)
    fs.arrow(ax, (3.40, 3.55), (3.89, 3.55), color=fs.MUTED)
    fs.arrow(ax, (5.57, 3.55), (6.05, 3.55), color=fs.MUTED)

    # 数据集
    fs.box(ax, 3.30, 1.02, 6.05, 1.28,
           "数据集　图像帧 · 关节角 · 夹爪开合 · 时间戳\n按同一时钟对齐，重采样到 50 Hz",
           fs=8.9, ec=fs.INK, fc="#FCFCFD")
    fs.arrow(ax, (2.45, 3.02), (3.75, 2.33), color=fs.FAINT, rad=-0.12)
    fs.arrow(ax, (4.65, 3.02), (5.10, 2.33), color=fs.FAINT, rad=-0.10)
    fs.arrow(ax, (6.85, 3.02), (7.00, 2.33), color=fs.FAINT)

    # 时间戳对齐
    ax.text(4.18, 0.70, "关节 50 Hz", fontsize=8.2, color=fs.BLUE, ha="right", va="center")
    ax.text(4.18, 0.36, "图像 30 fps", fontsize=8.2, color=fs.GREEN, ha="right", va="center")
    x0, x1 = 4.30, 9.20
    jt = np.arange(x0, x1 + 1e-9, 0.3667)
    it = np.arange(x0, x1 + 1e-9, 0.6120)
    for k, x in enumerate(jt):
        ax.plot([x, x], [0.64, 0.76], color=fs.BLUE, lw=1.0, solid_capstyle="butt")
    for x in it:
        ax.plot([x, x], [0.30, 0.42], color=fs.GREEN, lw=1.0, solid_capstyle="butt")
    ax.plot([x0, x1], [0.70, 0.70], color=fs.BLUE, lw=0.6, alpha=0.45)
    ax.plot([x0, x1], [0.36, 0.36], color=fs.GREEN, lw=0.6, alpha=0.45)
    for x in jt[::3]:
        near = it[np.argmin(np.abs(it - x))]
        ax.plot([x, x], [0.28, 0.72], color=fs.FAINT, lw=0.6, ls=(0, (2, 2)), zorder=1)
        ax.plot([near, near], [0.28, 0.72], color=fs.FAINT, lw=0.6, ls=(0, (2, 2)), zorder=1)
    ax.text(4.30, 0.08, "虚线为最近帧匹配，最坏相差半帧（约 17 ms）",
            fontsize=8.0, color=fs.MUTED, ha="left", va="center")
    fs.save(fig, "ch09", "fig09-02")


def fig_diffusion():
    """一条动作块在四个噪声等级下的样子，以及加噪与去噪方向。"""
    fig = plt.figure(figsize=(6.6, 2.8))

    n = 16
    a0 = np.stack([np.linspace(-0.95, 0.95, n),
                   0.52 * np.sin(1.55 * np.linspace(-0.95, 0.95, n))], axis=1)
    rng = np.random.default_rng(7)
    eps = rng.normal(0, 1, a0.shape)

    def abar(t):
        f = lambda s: np.cos((s + 0.008) / 1.008 * np.pi / 2) ** 2
        return f(t) / f(0)

    levels = [(1.00, "k = 100　纯噪声"), (0.60, "k = 60　噪声仍占优"),
              (0.30, "k = 30　形状可辨"), (0.00, "k = 0　可执行动作块")]

    x0, w, gap = 0.022, 0.186, 0.072
    h = 0.186 * 6.6 / 2.8
    y0 = 0.395
    for i, (t, lab) in enumerate(levels):
        ax = fig.add_axes([x0 + i * (w + gap), y0, w, h])
        ax.set_xlim(-2.15, 2.15)
        ax.set_ylim(-2.15, 2.15)
        ax.axis("off")
        ax.add_patch(Rectangle((-2.15, -2.15), 4.3, 4.3, fill=False,
                               ec=fs.GRID, lw=0.9, zorder=1))
        a = np.sqrt(abar(t)) * a0 + np.sqrt(1 - abar(t)) * eps
        if i:
            ax.plot(a0[:, 0], a0[:, 1], color=fs.FAINT, lw=0.9, ls=(0, (2, 2)), zorder=2)
            ax.plot(a[:, 0], a[:, 1], color=fs.BLUE, lw=0.9, alpha=0.8, zorder=3)
        else:
            cloud = rng.normal(0, 1, (90, 2))
            cloud = cloud[np.max(np.abs(cloud), axis=1) < 2.05]
            ax.plot(cloud[:, 0], cloud[:, 1], "o", ms=2.4, color=fs.FAINT,
                    alpha=0.5, zorder=3)
        ax.plot(a[:, 0], a[:, 1], "o", ms=2.2, color=fs.BLUE, alpha=0.9, zorder=4)
        fig.text(x0 + i * (w + gap) + w / 2, 0.325, lab, fontsize=8.2,
                 color=fs.INK if i in (0, 3) else fs.MUTED, ha="center", va="center")

    # 上方：采样方向（去噪）
    fig.add_artist(FancyArrowPatch((0.022, 0.925), (0.978, 0.925), transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=11, color=fs.ACCENT, lw=1.2))
    fig.text(0.5, 0.972, "采样：从噪声出发，每步去噪，10 步后得到动作块",
             fontsize=8.6, color=fs.ACCENT, ha="center", va="center")
    # 下方：训练方向（加噪）
    fig.add_artist(FancyArrowPatch((0.978, 0.185), (0.022, 0.185), transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=11, color=fs.MUTED, lw=1.1))
    fig.text(0.5, 0.105, "训练：随机取一步 k，给真实动作加噪，让网络预测噪声",
             fontsize=8.6, color=fs.MUTED, ha="center", va="center")
    fs.save(fig, "ch09", "fig09-03")


if __name__ == "__main__":
    fig_covariate()
    fig_teleop()
    fig_diffusion()
