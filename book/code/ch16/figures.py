# -*- coding: utf-8 -*-
"""第 16 章插图：PID 框图、阻抗控制的弹簧-阻尼模型、全身控制优先级栈。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import figstyle as fs


def fig_pid():
    """PID 控制框图：三项并联、被控对象、反馈回路。"""
    fig, ax = fs.canvas(6.6, 3.95)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.0)

    # 输入与求和点
    ax.text(0.26, 3.15, "$r$", ha="left", va="center", fontsize=11, color=fs.INK)
    ax.text(0.26, 2.72, "目标", ha="left", va="center", fontsize=8.2, color=fs.MUTED)
    fs.arrow(ax, (0.62, 3.15), (1.02, 3.15), color=fs.INK, lw=1.1)

    c1 = Circle((1.32, 3.15), 0.27, facecolor="white", edgecolor=fs.INK, lw=1.1, zorder=4)
    ax.add_patch(c1)
    ax.text(1.32, 3.15, "$+$", ha="center", va="center", fontsize=11, color=fs.INK, zorder=5)

    # 误差引出
    ax.plot([1.59, 1.95], [3.15, 3.15], color=fs.INK, lw=1.1, zorder=2)
    ax.plot([1.95, 1.95], [1.15, 5.15], color=fs.INK, lw=1.1, zorder=2)
    ax.text(1.86, 3.42, "$e$", ha="right", va="center", fontsize=10, color=fs.ACCENT)

    # 三个分支框
    bx, bw, bh = 2.32, 1.88, 1.06
    branches = [
        (4.62, "P　比例", "$K_p\\,e$", "差多少推多少", fs.ACCENT),
        (2.62, "I　积分", "$K_i\\!\\int\\! e\\,dt$", "攒掉最后一点残差", fs.BLUE),
        (0.62, "D　微分", r"$K_d\dot{e}$", "看趋势提前刹车", fs.GREEN),
    ]
    centers = []
    for y, name, formula, role, col in branches:
        fs.box(ax, bx, y, bw, bh, "", fc="#FFFFFF", ec=col, lw=1.2)
        ax.text(bx + bw / 2, y + bh - 0.23, name, ha="center", va="center",
                fontsize=9.2, color=col, weight="bold", zorder=5)
        ax.text(bx + bw / 2, y + bh / 2 - 0.02, formula, ha="center", va="center",
                fontsize=9.4, color=fs.INK, zorder=5)
        ax.text(bx + bw / 2, y + 0.20, role, ha="center", va="center",
                fontsize=7.6, color=fs.MUTED, zorder=5)
        centers.append(y + bh / 2)

    # 分支入口与出口
    for cy in centers:
        ax.plot([1.95, 2.30], [cy, cy], color=fs.INK, lw=1.1, zorder=2)
        fs.arrow(ax, (2.10, cy), (2.30, cy), color=fs.INK, lw=1.1)
        ax.plot([bx + bw, 4.40], [cy, cy], color=fs.INK, lw=1.1, zorder=2)
        fs.arrow(ax, (4.30, cy), (4.40, cy), color=fs.INK, lw=1.1)
    ax.plot([4.40, 4.40], [centers[2], centers[0]], color=fs.INK, lw=1.1, zorder=2)
    ax.plot([4.40, 4.58], [3.15, 3.15], color=fs.INK, lw=1.1, zorder=2)

    c2 = Circle((4.85, 3.15), 0.26, facecolor="white", edgecolor=fs.INK, lw=1.1, zorder=4)
    ax.add_patch(c2)
    ax.text(4.85, 3.17, "$\\Sigma$", ha="center", va="center", fontsize=11, color=fs.INK, zorder=5)

    # 被控对象
    fs.arrow(ax, (5.11, 3.15), (5.42, 3.15), color=fs.INK, lw=1.1)
    fs.box(ax, 5.44, 2.62, 2.52, 1.06, "", fc="#F8FAFC", ec=fs.INK, lw=1.1)
    ax.text(6.70, 3.38, "被控对象", ha="center", va="center", fontsize=9.4,
            color=fs.INK, weight="bold", zorder=5)
    ax.text(6.70, 2.98, "电机 + 减速器 + 连杆", ha="center", va="center",
            fontsize=8.2, color=fs.MUTED, zorder=5)

    # 扰动输入
    fs.arrow(ax, (6.70, 4.46), (6.70, 3.76), color=fs.PINK, lw=1.1)
    ax.text(6.84, 4.50, "重力 · 负载 · 外部推力", ha="left", va="bottom",
            fontsize=8.2, color=fs.PINK)

    # 输出
    fs.arrow(ax, (7.96, 3.15), (8.72, 3.15), color=fs.INK, lw=1.1)
    ax.text(8.84, 3.30, "$q$", ha="left", va="center", fontsize=11, color=fs.INK)
    ax.text(8.84, 2.88, "关节角", ha="left", va="center", fontsize=8.2, color=fs.MUTED)

    # 反馈回路
    ax.plot([8.30, 8.30], [3.15, 0.26], color=fs.MUTED, lw=1.1, zorder=2)
    ax.plot([8.30, 1.32], [0.26, 0.26], color=fs.MUTED, lw=1.1, zorder=2)
    fs.arrow(ax, (1.32, 0.34), (1.32, 2.86), color=fs.MUTED, lw=1.1)
    ax.add_patch(Circle((8.30, 3.15), 0.05, facecolor=fs.MUTED, edgecolor="none", zorder=5))
    ax.text(6.20, 0.40, "反馈：编码器实测的关节角", ha="center", va="bottom",
            fontsize=8.4, color=fs.MUTED)
    ax.text(1.20, 2.68, "−", ha="right", va="center", fontsize=10, color=fs.MUTED)

    fs.save(fig, "ch16", "fig16-01")


def fig_impedance():
    """左：弹簧-阻尼示意；右：不同刚度下偏移与接触力。"""
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(6.6, 3.15),
                                   gridspec_kw={"width_ratios": [1.06, 1.0], "wspace": 0.16})
    axl.set_xlim(0, 10)
    axl.set_ylim(0, 8)
    axl.axis("off")

    # 虚拟平衡点（左支撑）
    axl.plot([1.10, 1.10], [2.45, 5.55], color=fs.INK, lw=1.6, zorder=3)
    for yy in np.linspace(2.50, 5.50, 9):
        axl.plot([1.10, 0.84], [yy, yy - 0.22], color=fs.FAINT, lw=0.7, zorder=2)
    axl.text(1.28, 5.96, "虚拟平衡点 $x_d$", ha="left", va="bottom", fontsize=8.4, color=fs.INK)

    # 弹簧（上）
    x0, x1, ys, amp = 1.10, 4.85, 4.90, 0.30
    n = 7
    xs = [x0]
    for i in range(n):
        xs.append(x0 + (x1 - x0) * (i + 0.5) / n)
        xs.append(x0 + (x1 - x0) * (i + 1.0) / n)
    ys_ = [ys]
    for i in range(n):
        ys_.append(ys + (amp if i % 2 == 0 else -amp))
        ys_.append(ys)
    axl.plot(xs[:-1], ys_[:-1], color=fs.ACCENT, lw=1.3, zorder=3)
    axl.text(3.86, 5.34, "刚度 $K$", ha="center", va="bottom", fontsize=8.6, color=fs.ACCENT)

    # 阻尼器（下）
    yd = 3.10
    axl.plot([1.10, 2.85], [yd, yd], color=fs.BLUE, lw=1.3, zorder=3)
    axl.add_patch(Rectangle((2.85, yd - 0.34), 1.00, 0.68, facecolor="none",
                            edgecolor=fs.BLUE, lw=1.3, zorder=3))
    axl.add_patch(Rectangle((2.97, yd - 0.16), 0.40, 0.32, facecolor=fs.BLUE,
                            edgecolor="none", alpha=0.22, zorder=3))
    axl.plot([3.85, 4.85], [yd, yd], color=fs.BLUE, lw=1.3, zorder=3)
    axl.plot([3.85, 3.85], [yd - 0.34, yd + 0.34], color=fs.BLUE, lw=1.3, zorder=3)
    axl.text(3.35, 2.52, "阻尼 $D$", ha="center", va="top", fontsize=8.6, color=fs.BLUE)

    # 末端与环境
    axl.add_patch(Circle((5.35, 4.00), 0.56, facecolor="#EEF2F7", edgecolor=fs.INK,
                         lw=1.2, zorder=4))
    axl.text(5.35, 4.00, "末端", ha="center", va="center", fontsize=8.2, color=fs.INK, zorder=5)
    axl.plot([6.72, 6.72], [1.90, 6.10], color=fs.INK, lw=2.0, zorder=3)
    for yy in np.linspace(2.00, 6.00, 11):
        axl.plot([6.72, 7.02], [yy, yy + 0.22], color=fs.FAINT, lw=0.7, zorder=2)
    axl.text(6.94, 6.22, "环境", ha="center", va="bottom", fontsize=8.6, color=fs.INK)

    fs.arrow(axl, (6.68, 4.00), (5.98, 4.00), color=fs.PINK, lw=1.2)
    axl.text(6.28, 4.18, "$F$", ha="center", va="bottom", fontsize=9, color=fs.PINK)

    # 偏移量标注
    axl.annotate("", xy=(1.10, 1.30), xytext=(5.35, 1.30),
                 arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    axl.plot([5.35, 5.35], [1.25, 3.44], color=fs.MUTED, lw=0.7, ls=(0, (3, 3)), zorder=1)
    axl.plot([1.10, 1.10], [1.25, 2.45], color=fs.MUTED, lw=0.7, ls=(0, (3, 3)), zorder=1)
    axl.text(3.22, 1.02, "偏移 $x_d - x$", ha="center", va="top", fontsize=8.4, color=fs.MUTED)

    # 右图：力-位移
    d = np.linspace(0, 0.032, 200)
    axr.plot(d * 1000, 200 * d, color=fs.BLUE, lw=1.4, label="$K = 200$ N/m")
    axr.plot(d * 1000, 1000 * d, color=fs.ACCENT, lw=1.4, label="$K = 1000$ N/m")
    axr.axhline(20, color=fs.FAINT, lw=0.9, ls=(0, (4, 3)))
    axr.text(24.0, 18.2, "20 N 力上限（示例）", ha="left", va="top",
             fontsize=8.2, color=fs.MUTED)
    axr.plot([20, 20], [0, 20], color=fs.FAINT, lw=0.9, ls=(0, (4, 3)))
    axr.plot([20], [20], marker="o", ms=4, color=fs.ACCENT)
    axr.plot([20], [4], marker="o", ms=4, color=fs.BLUE)
    axr.annotate("20 mm 偏 4 N\n还能继续往里推", xy=(20, 4), xytext=(20.6, 8.0),
                 fontsize=8.2, color=fs.BLUE,
                 arrowprops=dict(arrowstyle="-", color=fs.BLUE, lw=0.7))
    axr.annotate("同样 20 mm 已经 20 N", xy=(19.4, 20), xytext=(2.6, 27.2),
                 fontsize=8.2, color=fs.ACCENT,
                 arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.7))
    axr.text(22.6, 1.4, "$K = 200$ N/m", ha="left", va="bottom", fontsize=8.4,
             color=fs.BLUE)
    axr.text(19.0, 31.4, "$K = 1000$ N/m", ha="left", va="bottom", fontsize=8.4,
             color=fs.ACCENT)
    axr.set_xlim(0, 32)
    axr.set_ylim(0, 34)
    axr.set_xlabel("末端被顶回的位移 / mm", fontsize=9)
    axr.set_ylabel("接触力 / N", fontsize=9)
    fs.clean(axr, grid=True)
    fs.save(fig, "ch16", "fig16-02")


def fig_wbc():
    """全身控制的三层优先级：约束、任务、求解顺序。"""
    fig, ax = fs.canvas(6.6, 3.55)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    layers = [
        (4.34, "第 1 层　安全", "关节限位 · 力矩上限 · 速度上限 · 自碰撞距离",
         "硬约束，宁可停住也不能违反", fs.ACCENT),
        (2.52, "第 2 层　平衡", "质心投影落在支撑多边形内 · 接触力留在摩擦锥内",
         "在安全允许的范围内保持不倒", fs.BLUE),
        (0.70, "第 3 层　手部任务", "末端位姿跟踪 $\\tau = J^{\\top} F$ · 姿态朝向",
         "在还剩下的自由度里尽力完成", fs.GREEN),
    ]
    x0, w, h = 1.30, 5.30, 1.44
    for y, name, cons, note, col in layers:
        fs.box(ax, x0, y, w, h, "", fc="#FFFFFF", ec=col, lw=1.3)
        ax.text(x0 + 0.24, y + h - 0.30, name, ha="left", va="center", fontsize=9.4,
                color=col, weight="bold", zorder=5)
        ax.text(x0 + 0.24, y + h - 0.66, cons, ha="left", va="center", fontsize=8.3,
                color=fs.INK, zorder=5)
        ax.text(x0 + 0.24, y + 0.26, note, ha="left", va="center", fontsize=8.3,
                color=fs.MUTED, zorder=5)

    # 左侧求解顺序
    fs.arrow(ax, (0.62, 5.70), (0.62, 0.62), color=fs.MUTED, lw=1.0)
    ax.text(0.62, 5.86, "求解顺序", ha="center", va="bottom", fontsize=8.4, color=fs.MUTED)
    for i, (y, _, _, _, col) in enumerate(layers):
        ax.add_patch(Circle((0.62, y + h / 2), 0.20, facecolor="white", edgecolor=col,
                            lw=1.2, zorder=6))
        ax.text(0.62, y + h / 2, str(i + 1), ha="center", va="center", fontsize=8.6,
                color=col, weight="bold", zorder=7)

    # 右侧可用空间示意
    ax.text(8.28, 5.86, "可用自由度", ha="center", va="bottom", fontsize=8.4, color=fs.MUTED)
    bars = [(4.62, 1.00, fs.ACCENT), (2.80, 0.52, fs.BLUE), (0.98, 0.24, fs.GREEN)]
    for y, frac, col in bars:
        ax.add_patch(Rectangle((7.30, y), 1.96, 0.46, facecolor="none",
                               edgecolor=fs.FAINT, lw=0.9, zorder=3))
        ax.add_patch(Rectangle((7.30, y), 1.96 * frac, 0.46, facecolor=col,
                               edgecolor="none", alpha=0.30, zorder=3))
    ax.text(9.62, 2.86, "逐层收窄", ha="center", va="center", fontsize=8.2,
            color=fs.MUTED, rotation=270)

    # 零空间说明
    ax.text(5.0, 0.16, "低优先级的解只能在高优先级任务的零空间里找", ha="center",
            va="bottom", fontsize=8.4, color=fs.INK)
    fs.save(fig, "ch16", "fig16-03")


if __name__ == "__main__":
    fig_pid()
    fig_impedance()
    fig_wbc()
