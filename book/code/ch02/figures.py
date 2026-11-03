# -*- coding: utf-8 -*-
"""第 2 章插图：二连杆正运动学、逆运动学两解、五种构型、坐标链。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, Wedge, Arc, Rectangle
import figstyle as fs

L1, L2 = 0.4, 0.3


def _joint(ax, p, color, r=0.010, z=6):
    ax.add_patch(Circle(p, r, facecolor="white", edgecolor=color, lw=1.4, zorder=z))


def _ground(ax, cx, w=0.09):
    ax.add_patch(Rectangle((cx - w / 2, -0.022), w, 0.022, facecolor="#D1D5DB",
                           edgecolor="none", zorder=2))
    for x in np.linspace(cx - w / 2 + 0.008, cx + w / 2 - 0.008, 4):
        ax.plot([x, x - 0.014], [-0.022, -0.036], color=fs.FAINT, lw=0.8, zorder=1)


def fig_fk():
    """平面二连杆正运动学，标注算例数值。"""
    fig, ax = fs.canvas(6.2, 5.6, xlim=(-0.075, 0.575), ylim=(-0.125, 0.575))
    ax.set_aspect("equal")

    t1, t2 = np.deg2rad(30), np.deg2rad(45)
    E = np.array([L1 * np.cos(t1), L1 * np.sin(t1)])
    P = E + np.array([L2 * np.cos(t1 + t2), L2 * np.sin(t1 + t2)])

    fs.arrow(ax, (0, 0), (0.555, 0), color=fs.FAINT, lw=1.0, ms=9)
    fs.arrow(ax, (0, 0), (0, 0.555), color=fs.FAINT, lw=1.0, ms=9)
    fs.label(ax, 0.552, -0.032, "x", fs=9, color=fs.MUTED)
    fs.label(ax, -0.032, 0.552, "y", fs=9, color=fs.MUTED)

    _ground(ax, 0.0)

    ax.plot([0, E[0]], [0, E[1]], color=fs.BLUE, lw=3.4, solid_capstyle="round", zorder=4)
    ax.plot([E[0], P[0]], [E[1], P[1]], color=fs.ACCENT, lw=3.4, solid_capstyle="round", zorder=4)
    for p in ((0, 0), E, P):
        _joint(ax, p, fs.INK, r=0.011)

    ax.add_patch(Arc((0, 0), 0.20, 0.20, theta1=0, theta2=30, color=fs.BLUE, lw=1.1, zorder=5))
    fs.label(ax, 0.108, 0.030, r"$\theta_1=30°$", fs=9.2, color=fs.BLUE, ha="left")

    u1 = np.array([np.cos(t1), np.sin(t1)])
    ax.plot([E[0], E[0] + 0.14 * u1[0]], [E[1], E[1] + 0.14 * u1[1]],
            color=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=3)
    ax.add_patch(Arc((E[0], E[1]), 0.15, 0.15, theta1=30, theta2=73,
                     color=fs.ACCENT, lw=1.1, zorder=3.5))
    bis = np.deg2rad(52.5)
    fs.label(ax, E[0] + 0.108 * np.cos(bis), E[1] + 0.108 * np.sin(bis), r"$\theta_2=45°$",
             fs=8.8, color=fs.ACCENT, ha="left", va="bottom", rotation=52.5, rotation_mode="anchor")

    n1 = np.array([-np.sin(t1), np.cos(t1)])
    p1 = E * 0.5 + 0.050 * n1
    fs.label(ax, p1[0] - 0.010, p1[1], r"$L_1=0.4$ m", fs=9, color=fs.BLUE, ha="center")
    n2 = np.array([-np.sin(t1 + t2), np.cos(t1 + t2)])
    p2 = (E + P) * 0.5 + 0.058 * n2
    fs.label(ax, p2[0] - 0.004, p2[1], r"$L_2=0.3$ m", fs=9, color=fs.ACCENT, ha="center")

    ax.plot([P[0], P[0]], [P[1], 0], color=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=2)
    ax.plot([P[0], 0], [P[1], P[1]], color=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=2)
    fs.label(ax, P[0], -0.038, "0.424", fs=8.8, color=fs.MUTED)
    fs.label(ax, -0.036, P[1], "0.490", fs=8.8, color=fs.MUTED, rotation=90)
    fs.label(ax, P[0] + 0.016, P[1] + 0.020, "末端\n(0.424, 0.490)", fs=8.8, color=fs.INK,
             ha="left", va="bottom")

    fs.label(ax, 0.075, -0.048,
             "第一段　(0.346, 0.200)\n第二段　(0.078, 0.290)\n合计　　(0.424, 0.490)",
             fs=8.4, color=fs.MUTED, ha="left", va="top")
    fs.save(fig, "ch02", "fig02-01")


def fig_ik():
    """同一末端点的两组逆解。"""
    fig, ax = fs.canvas(6.2, 5.2, xlim=(-0.075, 0.575), ylim=(-0.10, 0.565))
    ax.set_aspect("equal")

    P = np.array([0.4241, 0.4898])
    t1a, t2a = np.deg2rad(30), np.deg2rad(45)
    t1b, t2b = np.deg2rad(68.227), np.deg2rad(-45)
    Ea = np.array([L1 * np.cos(t1a), L1 * np.sin(t1a)])
    Eb = np.array([L1 * np.cos(t1b), L1 * np.sin(t1b)])

    fs.arrow(ax, (0, 0), (0.555, 0), color=fs.FAINT, lw=1.0, ms=9)
    fs.arrow(ax, (0, 0), (0, 0.555), color=fs.FAINT, lw=1.0, ms=9)
    fs.label(ax, 0.552, -0.030, "x", fs=9, color=fs.MUTED)
    fs.label(ax, -0.030, 0.552, "y", fs=9, color=fs.MUTED)

    _ground(ax, 0.0)

    ax.plot([0, P[0]], [0, P[1]], color=fs.FAINT, lw=1.0, ls=(0, (5, 4)), zorder=1)

    ax.plot([0, Ea[0]], [0, Ea[1]], color=fs.ACCENT, lw=3.0, solid_capstyle="round", zorder=4)
    ax.plot([Ea[0], P[0]], [Ea[1], P[1]], color=fs.ACCENT, lw=3.0, solid_capstyle="round", zorder=4)
    ax.plot([0, Eb[0]], [0, Eb[1]], color=fs.BLUE, lw=3.0, solid_capstyle="round", zorder=5)
    ax.plot([Eb[0], P[0]], [Eb[1], P[1]], color=fs.BLUE, lw=3.0, solid_capstyle="round", zorder=5)

    for p in (Ea, Eb):
        _joint(ax, p, fs.INK, r=0.011)
    ax.add_patch(Circle(P, 0.014, facecolor=fs.INK, edgecolor="white", lw=1.2, zorder=8))
    _joint(ax, (0, 0), fs.INK, r=0.011)

    halo = [pe.withStroke(linewidth=3.2, foreground="white")]
    a1 = Arc((0, 0), 0.13, 0.13, theta1=0, theta2=30, color=fs.ACCENT, lw=1.1, zorder=6)
    a1.set_path_effects(halo)
    ax.add_patch(a1)
    a2 = Arc((0, 0), 0.23, 0.23, theta1=0, theta2=68.2, color=fs.BLUE, lw=1.1, zorder=6)
    a2.set_path_effects(halo)
    ax.add_patch(a2)
    fs.label(ax, 0.130, 0.028, r"$\theta_1=30°$", fs=8.6, color=fs.ACCENT, ha="left")
    fs.label(ax, 0.190, 0.196, r"$\theta_1=68.2°$", fs=8.6, color=fs.BLUE, ha="left", va="bottom")

    fs.label(ax, Ea[0] + 0.028, Ea[1] - 0.030, "肘下\n$\\theta=(30°,\\,45°)$", fs=8.8,
             color=fs.ACCENT, ha="left", va="top")
    fs.label(ax, 0.115, 0.450, "肘上\n$\\theta=(68.2°,\\,-45°)$", fs=8.8,
             color=fs.BLUE, ha="left", va="bottom")
    fs.label(ax, P[0] + 0.018, P[1] - 0.004, "末端\n(0.424, 0.490)", fs=8.8, color=fs.INK,
             ha="left", va="top")
    fs.save(fig, "ch02", "fig02-02")


def _panel(ax):
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.17, 1.70)
    ax.set_aspect("equal")
    ax.axis("off")


def _ws(ax, patch):
    patch.set_facecolor("#DCE7F2")
    patch.set_edgecolor("#7C93B0")
    patch.set_linewidth(0.8)
    patch.set_linestyle((0, (4, 3)))
    patch.set_alpha(0.9)
    patch.set_zorder(1)
    ax.add_patch(patch)


def _pedestal(ax, cx, y0=0.02, w=0.22, h=0.08):
    ax.add_patch(Rectangle((cx - w / 2, y0), w, h, facecolor="#D1D5DB", edgecolor="none", zorder=2))


def fig_configs():
    """五种构型与工作空间剖面。"""
    fig, axes = plt.subplots(1, 5, figsize=(6.6, 2.75))
    fig.subplots_adjust(left=0.004, right=0.996, top=0.99, bottom=0.02, wspace=0.05)

    # (a) 直角坐标
    ax = axes[0]
    _panel(ax)
    _ws(ax, Rectangle((0.24, 0.26), 0.58, 1.02))
    _pedestal(ax, 0.12, w=0.18)
    ax.plot([0.12, 0.12], [0.10, 1.42], color=fs.INK, lw=3.2, solid_capstyle="butt", zorder=3)
    ax.plot([0.12, 0.86], [1.42, 1.42], color=fs.INK, lw=3.2, solid_capstyle="butt", zorder=3)
    ax.add_patch(Rectangle((0.52, 1.34), 0.12, 0.10, facecolor="white", edgecolor=fs.INK, lw=1.1, zorder=4))
    ax.plot([0.58, 0.58], [1.34, 0.90], color=fs.INK, lw=2.0, zorder=4)
    ax.add_patch(Rectangle((0.545, 0.84), 0.07, 0.06, facecolor=fs.ACCENT, edgecolor="none", zorder=5))
    fs.arrow(ax, (0.26, 1.56), (0.78, 1.56), color=fs.MUTED, lw=0.9, style="<|-|>", ms=7)
    fs.label(ax, 0.52, 1.60, "x", fs=8, color=fs.MUTED)
    fs.arrow(ax, (0.92, 1.34), (0.92, 0.86), color=fs.MUTED, lw=0.9, style="<|-|>", ms=7)
    fs.label(ax, 0.955, 1.10, "z", fs=8, color=fs.MUTED)
    fs.label(ax, 0.5, -0.04, "(a) 直角坐标", fs=8.6, color=fs.INK)
    fs.label(ax, 0.5, -0.13, "3 个移动关节", fs=8, color=fs.MUTED)

    # (b) 圆柱坐标
    ax = axes[1]
    _panel(ax)
    _ws(ax, Rectangle((0.50, 0.22), 0.36, 1.06))
    _pedestal(ax, 0.38, w=0.24)
    ax.plot([0.38, 0.38], [0.10, 1.32], color=fs.INK, lw=3.2, solid_capstyle="butt", zorder=3)
    ax.plot([0.38, 0.70], [0.96, 0.96], color=fs.INK, lw=2.4, solid_capstyle="butt", zorder=3)
    ax.plot([0.70, 0.70], [0.96, 0.60], color=fs.INK, lw=2.0, zorder=4)
    ax.add_patch(Rectangle((0.665, 0.54), 0.07, 0.06, facecolor=fs.ACCENT, edgecolor="none", zorder=5))
    fs.arrow(ax, (0.42, 1.12), (0.68, 1.12), color=fs.MUTED, lw=0.9, style="<|-|>", ms=7)
    fs.label(ax, 0.55, 1.16, "r", fs=8, color=fs.MUTED)
    ax.add_patch(Arc((0.38, 1.30), 0.26, 0.26, theta1=0, theta2=200, color=fs.MUTED, lw=1.0, zorder=5))
    fs.arrow(ax, (0.267, 1.278), (0.252, 1.256), color=fs.MUTED, lw=1.0, ms=7)
    fs.label(ax, 0.46, 1.46, r"$\theta$", fs=8.4, color=fs.MUTED)
    fs.label(ax, 0.5, -0.04, "(b) 圆柱坐标", fs=8.6, color=fs.INK)
    fs.label(ax, 0.5, -0.13, "1 转 2 移", fs=8, color=fs.MUTED)

    # (c) 球坐标
    ax = axes[2]
    _panel(ax)
    _ws(ax, Wedge((0.36, 0.14), 0.70, 14, 102, width=0.40))
    _pedestal(ax, 0.36, w=0.20)
    ax.plot([0.36, 0.36], [0.10, 0.14], color=fs.INK, lw=3.0, zorder=3)
    p0 = np.array([0.36, 0.14])
    th = np.deg2rad(55)
    d = np.array([np.cos(th), np.sin(th)])
    ax.plot([p0[0], (p0 + 0.36 * d)[0]], [p0[1], (p0 + 0.36 * d)[1]],
            color=fs.INK, lw=4.6, solid_capstyle="butt", zorder=3)
    ax.plot([(p0 + 0.30 * d)[0], (p0 + 0.62 * d)[0]], [(p0 + 0.30 * d)[1], (p0 + 0.62 * d)[1]],
            color=fs.INK, lw=2.2, solid_capstyle="butt", zorder=3)
    ax.add_patch(Circle(p0 + 0.62 * d, 0.030, facecolor=fs.ACCENT, edgecolor="none", zorder=5))
    n = np.array([np.sin(th), -np.cos(th)])
    q0 = p0 + 0.30 * d + 0.055 * n
    q1 = p0 + 0.60 * d + 0.055 * n
    fs.arrow(ax, tuple(q0), tuple(q1), color=fs.MUTED, lw=0.9, style="<|-|>", ms=7)
    fs.label(ax, (q0[0] + q1[0]) / 2 + 0.01, (q0[1] + q1[1]) / 2 - 0.042, "伸缩",
             fs=8, color=fs.MUTED, ha="left")
    fs.label(ax, 0.5, -0.04, "(c) 球坐标", fs=8.6, color=fs.INK)
    fs.label(ax, 0.5, -0.13, "2 转 1 移", fs=8, color=fs.MUTED)

    # (d) 关节型
    ax = axes[3]
    _panel(ax)
    _ws(ax, Wedge((0.34, 0.12), 0.80, 2, 108, width=0.70))
    _pedestal(ax, 0.34, w=0.20)
    a1, a2 = np.deg2rad(75), np.deg2rad(-35)
    sh = np.array([0.34, 0.12])
    e = sh + 0.42 * np.array([np.cos(a1), np.sin(a1)])
    tip = e + 0.36 * np.array([np.cos(a1 + a2), np.sin(a1 + a2)])
    ax.plot([sh[0], e[0]], [sh[1], e[1]], color=fs.INK, lw=3.4, solid_capstyle="round", zorder=3)
    ax.plot([e[0], tip[0]], [e[1], tip[1]], color=fs.INK, lw=2.8, solid_capstyle="round", zorder=3)
    _joint(ax, e, fs.INK, r=0.016)
    ax.add_patch(Circle(tip, 0.030, facecolor=fs.ACCENT, edgecolor="none", zorder=5))
    fs.label(ax, e[0] - 0.055, e[1] + 0.005, "肘", fs=8, color=fs.MUTED, ha="right")
    fs.label(ax, 0.5, -0.04, "(d) 关节型", fs=8.6, color=fs.INK)
    fs.label(ax, 0.5, -0.13, "全部为转动关节", fs=8, color=fs.MUTED)

    # (e) SCARA（俯视）
    ax = axes[4]
    _panel(ax)
    _ws(ax, Wedge((0.28, 0.32), 0.72, -12, 72, width=0.62))
    ax.add_patch(Circle((0.28, 0.32), 0.075, facecolor="#D1D5DB", edgecolor="none", zorder=2))
    b1, b2 = np.deg2rad(40), np.deg2rad(-48)
    base = np.array([0.28, 0.32])
    e = base + 0.36 * np.array([np.cos(b1), np.sin(b1)])
    tip = e + 0.30 * np.array([np.cos(b1 + b2), np.sin(b1 + b2)])
    ax.plot([base[0], e[0]], [base[1], e[1]], color=fs.INK, lw=3.4, solid_capstyle="round", zorder=3)
    ax.plot([e[0], tip[0]], [e[1], tip[1]], color=fs.INK, lw=2.8, solid_capstyle="round", zorder=3)
    _joint(ax, e, fs.INK, r=0.016)
    ax.add_patch(Circle(tip, 0.040, facecolor="white", edgecolor=fs.ACCENT, lw=1.2, zorder=5))
    ax.add_patch(Circle(tip, 0.016, facecolor=fs.ACCENT, edgecolor="none", zorder=6))
    fs.label(ax, 0.5, -0.04, "(e) SCARA 俯视", fs=8.6, color=fs.INK)
    fs.label(ax, 0.5, -0.13, "2 转 1 移", fs=8, color=fs.MUTED)

    fs.save(fig, "ch02", "fig02-03")


def fig_chain():
    """世界到像素的坐标链与每段的来源、频率。"""
    fig, ax = fs.canvas(6.6, 4.9, xlim=(0, 10), ylim=(0, 10))

    rows = [
        ("世界坐标系 W", "地图原点，长期不变", "10–50 Hz"),
        ("基座坐标系 B", "机器人在世界中的落点", "1 kHz"),
        ("末端坐标系 E", "法兰中心与工具朝向", "1 kHz"),
        ("相机坐标系 C", "光心与光轴", "30 Hz"),
        ("像素坐标 (u, v)", "成像平面上的整数格", "30 Hz"),
    ]
    names = [
        ("$T_{world}^{base}$", "里程计、IMU 与地图匹配"),
        ("$T_{base}^{ee}(q)$", "编码器读数加正运动学"),
        ("$T_{ee}^{cam}$", "手眼标定"),
        ("投影 $K$", "内参标定，逐帧计算"),
    ]
    xb, w, h = 0.40, 3.20, 0.78
    ys = [9.00 - i * 1.88 for i in range(5)]
    for (t1, t2, freq), y in zip(rows, ys):
        fs.box(ax, xb, y, w, h, "", fc="#FFFFFF", ec="#9CA3AF", lw=1.0)
        ax.text(xb + 0.20, y + h * 0.66, t1, ha="left", va="center", fontsize=9.4,
                color=fs.INK, weight="bold", zorder=5)
        ax.text(xb + 0.20, y + h * 0.26, t2, ha="left", va="center", fontsize=8.2,
                color=fs.MUTED, zorder=5)
        ax.text(6.35, y + h / 2, freq, ha="left", va="center", fontsize=8.4, color=fs.MUTED)

    for i in range(4):
        y0 = ys[i] - 0.05
        y1 = ys[i + 1] + h + 0.05
        mid = (y0 + y1) / 2
        fs.arrow(ax, (xb + w / 2, y0), (xb + w / 2, y1), color=fs.MUTED, lw=1.1, ms=9)
        ax.text(xb + w / 2 + 0.22, mid, names[i][0], ha="left", va="center",
                fontsize=9.0, color=fs.ACCENT, zorder=6)
        ax.text(xb + w / 2 + 1.65, mid, names[i][1], ha="left", va="center",
                fontsize=8.2, color=fs.MUTED, zorder=6)

    ax.text(6.35, 9.90, "更新频率", ha="left", va="center", fontsize=8.2, color=fs.FAINT)
    ax.plot([6.20, 6.20], [1.30, 9.62], color=fs.GRID, lw=0.8, zorder=0)

    ax.text(0.40, 0.84,
            r"$T_{world}^{cam}=T_{world}^{base}\,T_{base}^{ee}(q)\,T_{ee}^{cam}$",
            ha="left", va="center", fontsize=9.2, color=fs.INK)
    ax.text(0.40, 0.34,
            "延迟由最慢的一段决定，30 Hz 的相机每帧 33 ms",
            ha="left", va="center", fontsize=8.4, color=fs.MUTED)
    fs.save(fig, "ch02", "fig02-04")


if __name__ == "__main__":
    fig_fk()
    fig_ik()
    fig_configs()
    fig_chain()
