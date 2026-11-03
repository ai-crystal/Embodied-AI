# -*- coding: utf-8 -*-
"""第 17 章插图：ZMP 与支撑多边形、线性倒立摆、步态相位与训练环路。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
import figstyle as fs


def _ground(ax, y, x0, x1, step=0.42, h=0.16):
    """地面线 + 斜线阴影。"""
    ax.plot([x0, x1], [y, y], color=fs.INK, lw=1.1, zorder=1, solid_capstyle="butt")
    xs = np.arange(x0, x1, step)
    for x in xs:
        ax.plot([x, x - h], [y, y - h], color=fs.FAINT, lw=0.8, zorder=1)


def _hull(pts):
    """Andrew 单调链凸包，返回逆时针顶点。"""
    pts = sorted(map(tuple, pts))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def fig_zmp():
    """(a) 侧视：质心投影、ZMP、余量；(b) 俯视：支撑多边形与稳定裕度。"""
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(6.9, 3.5))
    for ax in (axa, axb):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
        ax.set_aspect("equal")
        ax.axis("off")

    # ---------------- (a) 侧视 ----------------
    ax = axa
    gy = 2.2
    _ground(ax, gy, 0.3, 9.7)

    # 脚掌
    heel, toe = 3.60, 6.30
    ax.add_patch(Rectangle((heel, gy), toe - heel, 0.40, facecolor=fs.LIGHT,
                           edgecolor=fs.MUTED, lw=1.0, zorder=2))

    # 身体
    ankle, knee, hip = (5.50, 2.62), (5.70, 3.68), (5.36, 4.66)
    fs.limb(ax, ankle, knee, 0.22, 0.32, color=fs.INK, z=4)
    fs.limb(ax, knee, hip, 0.32, 0.46, color=fs.INK, z=4)
    fs.limb(ax, hip, (5.30, 5.44), 0.50, 0.60, color=fs.INK, z=4)
    fs.limb(ax, (5.30, 5.44), (5.26, 5.80), 0.60, 0.70, color=fs.INK, z=4)
    ax.add_patch(Circle((5.22, 6.06), 0.25, facecolor=fs.INK, edgecolor="none", zorder=5))
    fs.limb(ax, (5.16, 5.70), (5.02, 5.04), 0.20, 0.16, color=fs.INK, z=4)
    fs.limb(ax, (5.02, 5.04), (5.12, 4.58), 0.16, 0.12, color=fs.INK, z=4)

    # 质心与投影
    cx = 5.34
    ax.plot([cx, cx], [4.58, gy], color=fs.MUTED, lw=1.0, ls=(0, (4, 3)), zorder=3)
    ax.add_patch(Circle((cx, 4.74), 0.15, facecolor="white", edgecolor=fs.ACCENT, lw=1.4, zorder=6))
    ax.add_patch(Circle((cx, 4.74), 0.055, facecolor=fs.ACCENT, edgecolor="none", zorder=7))
    fs.label(ax, cx + 0.30, 4.92, "质心 $m$", fs=9, ha="left", va="bottom")

    ax.add_patch(Circle((cx, gy), 0.10, facecolor="white", edgecolor=fs.MUTED, lw=1.0, zorder=6))
    fs.label(ax, 5.98, 2.76, "质心投影", fs=8.8, ha="left", va="bottom", color=fs.MUTED)

    # ZMP 与地面反力
    zx = 4.35
    ax.add_patch(Circle((zx, gy), 0.11, facecolor=fs.ACCENT, edgecolor="none", zorder=6))
    fs.label(ax, 4.22, 2.76, "ZMP（零力矩点）", fs=8.8, ha="right", va="bottom", color=fs.ACCENT)
    fs.arrow(ax, (zx, gy + 0.44), (zx, 3.86), color=fs.ACCENT, lw=1.4, ms=9)
    fs.label(ax, zx + 0.13, 3.55, "$F$", fs=9.2, ha="left", va="center", color=fs.ACCENT)

    # 稳定裕度与支撑区间
    ax.annotate("", xy=(zx, 1.64), xytext=(heel, 1.64),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=0.9))
    for x in (zx, heel):
        ax.plot([x, x], [1.64, 1.76], color=fs.ACCENT, lw=0.9)
    fs.label(ax, (heel + zx) / 2, 1.54, "稳定裕度", fs=8.4, va="top", color=fs.ACCENT)

    ax.annotate("", xy=(heel, 0.74), xytext=(toe, 0.74),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    for x in (heel, toe):
        ax.plot([x, x], [0.74, 0.86], color=fs.MUTED, lw=0.9)
    fs.label(ax, 4.95, 0.62, "支撑区间（脚跟到脚尖）", fs=8.6, color=fs.MUTED, va="top")

    fs.label(ax, 0.30, 5.20, "质心投影落在脚掌内，\n脚就不会绕边缘翻倒", fs=8.8,
             ha="left", va="center", color=fs.MUTED)
    fs.label(ax, 0.28, 6.62, "(a) 侧视", fs=9.4, ha="left", va="center", color=fs.MUTED)

    # ---------------- (b) 俯视 ----------------
    ax = axb
    fl = dict(x=2.55, y=1.75, w=1.30, h=2.90)
    fr = dict(x=6.15, y=2.55, w=1.30, h=2.90)
    corners = []
    for f in (fl, fr):
        for x in (f["x"], f["x"] + f["w"]):
            for y in (f["y"], f["y"] + f["h"]):
                corners.append((x, y))
    hull = _hull(corners)
    ax.add_patch(Polygon(hull, closed=True, facecolor=fs.ACCENT, edgecolor=fs.ACCENT,
                         alpha=0.10, lw=0, zorder=2))
    ax.add_patch(Polygon(hull, closed=True, facecolor="none", edgecolor=fs.ACCENT,
                         lw=1.1, ls=(0, (5, 3)), zorder=3))
    for f in (fl, fr):
        ax.add_patch(Rectangle((f["x"], f["y"]), f["w"], f["h"], facecolor="white",
                               edgecolor=fs.INK, lw=1.1, zorder=4))

    # 质心投影 + 稳定裕度
    cx, cy = 4.90, 3.20
    ax.add_patch(Circle((cx, cy), 0.14, facecolor=fs.ACCENT, edgecolor="none", zorder=6))
    ax.annotate("", xy=(fr["x"] - 0.02, cy), xytext=(cx + 0.16, cy),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=1.1))
    fs.label(ax, cx, 3.52, "稳定裕度", fs=8.8, color=fs.ACCENT, va="bottom")
    fs.label(ax, cx, 2.86, "质心投影", fs=8.8, color=fs.MUTED, va="top")

    fs.label(ax, 3.20, 1.40, "左脚掌", fs=9, color=fs.INK, va="top")
    fs.label(ax, 6.80, 5.66, "右脚掌", fs=9, color=fs.INK, va="bottom")
    fs.label(ax, 7.72, 4.34, "支撑多边形", fs=8.8, ha="left", color=fs.ACCENT, va="center")
    ax.annotate("", xy=(fr["x"] + fr["w"] + 0.04, 4.32), xytext=(7.68, 4.34),
                arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.8))

    fs.arrow(ax, (1.62, 1.95), (1.62, 5.35), color=fs.MUTED, lw=1.0, ms=9)
    fs.label(ax, 1.30, 3.66, "前进方向", fs=8.6, color=fs.MUTED, rotation=90)

    fs.label(ax, 0.28, 6.62, "(b) 俯视", fs=9.4, ha="left", va="center", color=fs.MUTED)

    fig.subplots_adjust(wspace=0.04)
    fs.save(fig, "ch17", "fig17-01")


def fig_lipm():
    """线性倒立摆：质点、伸缩腿、接触点与步距。"""
    fig, ax = fs.canvas(6.6, 3.9)
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 6.8)
    ax.set_aspect("equal")

    gy = 1.0
    _ground(ax, gy, 0.4, 9.9)

    C = np.array([3.00, gy])
    M = np.array([4.20, 4.90])
    N = np.array([7.20, gy])

    # 下一步的虚拟腿
    ax.plot([M[0], N[0]], [M[1], N[1]], color=fs.FAINT, lw=1.0, ls=(0, (2, 3)), zorder=2)

    # 伸缩腿：外套筒 + 内杆
    P = C + (M - C) * 0.55
    ax.plot([C[0], P[0]], [C[1], P[1]], color="#9CA3AF", lw=6.0,
            solid_capstyle="round", zorder=3)
    ax.plot([P[0], M[0]], [P[1], M[1]], color=fs.INK, lw=2.2,
            solid_capstyle="round", zorder=4)
    fs.label(ax, 2.30, 2.62, "可伸缩腿", fs=8.8, ha="right", color=fs.MUTED)

    # 质点
    ax.add_patch(Circle(M, 0.17, facecolor=fs.INK, edgecolor="none", zorder=6))
    fs.label(ax, M[0] + 0.24, M[1] + 0.12, "质心 $m$", fs=9.2, ha="left", va="bottom")

    # 重力方向与质心投影
    ax.annotate("", xy=(M[0], gy + 0.04), xytext=(M[0], M[1] - 0.18),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0,
                                linestyle=(0, (4, 3)), mutation_scale=8))
    fs.label(ax, M[0] + 0.14, 2.55, "$mg$", fs=9, ha="left", va="center", color=fs.MUTED)
    ax.add_patch(Circle((M[0], gy), 0.09, facecolor="white", edgecolor=fs.MUTED, lw=1.0, zorder=6))

    # 质心高度
    ax.annotate("", xy=(5.35, gy), xytext=(5.35, M[1]),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    ax.plot([M[0], 5.35], [M[1], M[1]], color=fs.MUTED, lw=0.7, ls=(0, (2, 2)), zorder=2)
    fs.label(ax, 5.45, 2.30, "$z_0$", fs=9.6, ha="left", va="center", color=fs.MUTED)

    # 水平偏移
    ax.annotate("", xy=(C[0], 1.42), xytext=(M[0], 1.42),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=0.9))
    for x in (C[0], M[0]):
        ax.plot([x, x], [1.42, 1.30], color=fs.ACCENT, lw=0.9)
    fs.label(ax, 3.60, 1.54, "$x$", fs=9.2, color=fs.ACCENT, va="bottom")

    # 接触点
    ax.add_patch(Circle(C, 0.11, facecolor=fs.INK, edgecolor="none", zorder=6))
    fs.label(ax, C[0] - 0.16, 1.24, "支撑脚", fs=8.8, ha="right", va="bottom", color=fs.MUTED)
    ax.add_patch(Rectangle((N[0] - 0.55, gy - 0.03), 1.10, 0.17, facecolor="none",
                           edgecolor=fs.MUTED, lw=1.0, ls=(0, (3, 2)), zorder=5))
    fs.label(ax, N[0] + 0.22, 1.22, "下一落脚点", fs=8.8, ha="left", va="bottom", color=fs.MUTED)

    # 步距
    ax.annotate("", xy=(C[0], 0.52), xytext=(N[0], 0.52),
                arrowprops=dict(arrowstyle="<->", color=fs.INK, lw=0.9))
    for x in (C[0], N[0]):
        ax.plot([x, x], [0.52, 0.66], color=fs.INK, lw=0.9)
    fs.label(ax, 5.10, 0.22, "步距 $vT$", fs=9, va="top")

    fs.label(ax, 0.40, 6.24, r"$\ddot{x}=\omega^{2}x,\quad \omega=\sqrt{g/z_0}$",
             fs=10.5, ha="left", va="center", color=fs.INK)

    fs.save(fig, "ch17", "fig17-02")


def fig_gait_loop():
    """(a) 支撑相与摆动相的时间轴；(b) 训练闭环。"""
    fig = plt.figure(figsize=(6.9, 6.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.62], hspace=0.12)
    axa = fig.add_subplot(gs[0])
    axb = fig.add_subplot(gs[1])

    # ---------------- (a) 步态相位 ----------------
    axa.set_xlim(0, 10)
    axa.set_ylim(0, 3.3)
    axa.axis("off")
    x0, x1 = 2.20, 9.60
    T = 2.0
    sx = lambda t: x0 + (x1 - x0) * t / T

    lanes = [(2.02, "左腿"), (1.28, "右腿")]
    for y, name in lanes:
        fs.label(axa, x0 - 0.16, y + 0.18, name, fs=9, ha="right", va="center")

    # 每条腿支撑 60%、摆动 40%，相位错开半个周期，于是双支撑占 20%
    segs = {
        "左腿": [(0.0, 1.2, "stance"), (1.2, 2.0, "swing")],
        "右腿": [(0.0, 0.2, "stance"), (0.2, 1.0, "swing"), (1.0, 2.0, "stance")],
    }
    for (y, name) in lanes:
        for a, b, kind in segs[name]:
            w = sx(b) - sx(a)
            if kind == "stance":
                axa.add_patch(Rectangle((sx(a), y), w, 0.36, facecolor="#D8E8E0",
                                        edgecolor=fs.GREEN, lw=1.0, zorder=3))
                if w > 0.95:
                    fs.label(axa, sx(a) + w / 2, y + 0.18, "支撑", fs=8.6, color=fs.GREEN, z=5)
            else:
                axa.add_patch(Rectangle((sx(a), y), w, 0.36, facecolor="#FDF1E6",
                                        edgecolor=fs.ACCENT, lw=1.0, ls=(0, (4, 2)), zorder=3))
                if w > 0.95:
                    fs.label(axa, sx(a) + w / 2, y + 0.18, "摆动", fs=8.6, color=fs.ACCENT, z=5)

    # 步态周期
    axa.annotate("", xy=(sx(T), 2.72), xytext=(sx(0), 2.72),
                 arrowprops=dict(arrowstyle="<->", color=fs.INK, lw=0.9))
    for t in (0.0, T):
        axa.plot([sx(t), sx(t)], [2.72, 2.60], color=fs.INK, lw=0.9)
    fs.label(axa, (sx(0) + sx(T)) / 2, 2.82, "步态周期 $T$", fs=9, va="bottom")

    # 时间轴
    axa.annotate("", xy=(x1 + 0.22, 0.92), xytext=(x0, 0.92),
                 arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0))
    for t in (0.0, 0.5, 1.0, 1.5, 2.0):
        axa.plot([sx(t), sx(t)], [0.92, 0.82], color=fs.MUTED, lw=0.8)
        fs.label(axa, sx(t), 0.66, f"{t:.1f}", fs=8.2, color=fs.MUTED, va="top")
    fs.label(axa, x1 + 0.28, 0.92, "时间 / s", fs=8.4, color=fs.MUTED, ha="left", va="center")

    fs.label(axa, 0.28, 3.02, "(a)", fs=9.4, ha="left", va="center", color=fs.MUTED)
    fs.label(axa, 2.20, 0.30, "支撑相占 60%，摆动相占 40%，两条腿同时在支撑的时间占 20%",
             fs=8.4, ha="left", va="top", color=fs.MUTED)

    # ---------------- (b) 训练闭环 ----------------
    axb.set_xlim(0, 10)
    axb.set_ylim(0, 6.3)
    axb.axis("off")

    W, H = 3.30, 1.22
    A = (0.55, 3.30)
    B = (5.95, 3.30)
    C = (5.95, 1.05)
    D = (0.55, 1.05)
    fs.box(axb, A[0], A[1], W, H, "大规模并行仿真\n单卡上万个环境", fs=9.0, ec=fs.BLUE)
    fs.box(axb, B[0], B[1], W + 0.20, H, "采样轨迹\n状态 · 动作 · 奖励", fs=9.0, ec=fs.BLUE)
    fs.box(axb, C[0], C[1], W + 0.20, H, "PPO 更新\n裁剪目标 · 优势估计", fs=9.0, ec=fs.PURPLE)
    fs.box(axb, D[0], D[1], W, H, "新策略参数\n同步回仿真", fs=9.0, ec=fs.PURPLE)

    fs.arrow(axb, (A[0] + W + 0.03, A[1] + H / 2), (B[0] - 0.03, B[1] + H / 2), color=fs.BLUE)
    fs.arrow(axb, (B[0] + (W + 0.2) / 2, B[1] - 0.03), (C[0] + (W + 0.2) / 2, C[1] + H + 0.03),
             color=fs.BLUE)
    fs.arrow(axb, (C[0] - 0.03, C[1] + H / 2), (D[0] + W + 0.03, D[1] + H / 2), color=fs.PURPLE)
    fs.arrow(axb, (D[0] + W / 2, D[1] + H + 0.03), (A[0] + W / 2, A[1] - 0.03), color=fs.PURPLE)

    fs.box(axb, A[0], 5.02, W, 0.82, "课程学习\n平地 → 碎石 → 楼梯", fs=8.4, ec=fs.GREEN)
    fs.arrow(axb, (A[0] + W / 2, 4.99), (A[0] + W / 2, A[1] + H + 0.03), color=fs.GREEN, lw=1.0)
    fs.box(axb, B[0], 5.02, W + 0.20, 0.82, "域随机化\n质量 · 摩擦 · 延迟", fs=8.4, ec=fs.GREEN)
    fs.arrow(axb, (B[0] + (W + 0.2) / 2, 4.99), (B[0] + (W + 0.2) / 2, B[1] + H + 0.03),
             color=fs.GREEN, lw=1.0)

    fs.box(axb, B[0], 0.02, W + 0.20, 0.74, "真机部署\n策略 50 Hz，PD 1 kHz", fs=8.4, ec=fs.ACCENT)
    fs.arrow(axb, (B[0] + (W + 0.2) / 2, C[1] - 0.03), (B[0] + (W + 0.2) / 2, 0.79),
             color=fs.ACCENT, lw=1.0)

    fs.label(axb, 0.30, 6.06, "(b)", fs=9.4, ha="left", va="center", color=fs.MUTED)

    fs.save(fig, "ch17", "fig17-03")


if __name__ == "__main__":
    fig_zmp()
    fig_lipm()
    fig_gait_loop()
