# -*- coding: utf-8 -*-
"""第 5 章插图：三种抓取表示、掩码到执行的管线、力闭合示意。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Arc, Wedge, Polygon
import figstyle as fs


def mug_top(ax, cx, cy, r=0.55, fc="#E3E8EF", ec=fs.FAINT, lw=1.0, z=2):
    """俯视马克杯：把手 + 杯身 + 杯口。"""
    ax.add_patch(Arc((cx + r * 1.10, cy), r * 0.92, r * 0.92, theta1=-70, theta2=70,
                     lw=1.9, color=ec, zorder=z))
    ax.add_patch(Circle((cx, cy), r, facecolor=fc, edgecolor=ec, lw=lw, zorder=z))
    ax.add_patch(Circle((cx, cy), r * 0.70, facecolor="white", edgecolor=ec, lw=0.8, zorder=z + 1))


def jaws(ax, cx, cy, ang, opening=1.30, depth=1.05, color=fs.ACCENT, lw=3.4, z=4, alpha=1.0):
    """平行夹爪的两根指：沿 ang 方向开合。"""
    a = np.deg2rad(ang)
    u = np.array([np.cos(a), np.sin(a)])
    n = np.array([-np.sin(a), np.cos(a)])
    c = np.array([cx, cy])
    for s in (-1, 1):
        p = c + s * u * opening / 2
        p0, p1 = p - n * depth / 2, p + n * depth / 2
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, alpha=alpha,
                solid_capstyle="round", zorder=z)


def fig_grasp_repr():
    """三种抓取表示：(a) 2D 抓取矩形 (b) 6-DoF 平行夹爪 (c) 接触点。"""
    fig, ax = fs.canvas(6.9, 2.95)
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 5.6)

    # ---------------- (a) 2D 抓取矩形 ----------------
    c = np.array([2.25, 2.60])
    ang, op, dp = 20.0, 1.40, 1.30
    a = np.deg2rad(ang)
    u = np.array([np.cos(a), np.sin(a)])
    n = np.array([-np.sin(a), np.cos(a)])
    mug_top(ax, c[0], c[1], r=0.60)
    corners = [c + u * op / 2 + n * dp / 2, c + u * op / 2 - n * dp / 2,
               c - u * op / 2 - n * dp / 2, c - u * op / 2 + n * dp / 2]
    ax.add_patch(Polygon(corners, closed=True, facecolor="none", edgecolor=fs.ACCENT,
                         lw=1.0, ls=(0, (4, 2)), zorder=5))
    jaws(ax, c[0], c[1], ang, opening=op, depth=0.92, lw=3.8)
    ax.add_patch(Circle(c, 0.072, facecolor="white", edgecolor=fs.ACCENT, lw=1.2, zorder=7))
    ax.add_patch(Circle(c, 0.026, facecolor=fs.ACCENT, edgecolor="none", zorder=8))

    e0 = c - n * (dp / 2 + 0.16) - u * op / 2
    e1 = c - n * (dp / 2 + 0.16) + u * op / 2
    ax.annotate("", xy=(e0[0], e0[1]), xytext=(e1[0], e1[1]),
                arrowprops=dict(arrowstyle="<|-|>", color=fs.INK, lw=0.9,
                                shrinkA=1, shrinkB=1), zorder=8)
    fs.label(ax, 2.72, 1.34, "张开宽度", fs=8.4, color=fs.INK)

    fs.label(ax, 2.25, 4.45, "抓取矩形", fs=8.8, color=fs.ACCENT, weight="bold")
    fs.label(ax, 2.25, 4.10, "中心 · 角度 · 张开度", fs=8.2, color=fs.MUTED)
    fs.label(ax, 2.25, 0.55, "(a) 图像里的矩形", fs=9.4, color=fs.INK, weight="bold")

    # ---------------- (b) 6-DoF 平行夹爪 ----------------
    bx, by = 6.60, 2.62
    mug_top(ax, bx, by, r=0.56)
    jaws(ax, bx, by, 0, opening=1.30, depth=1.00, color=fs.FAINT, lw=2.6, alpha=0.7, z=3)
    jaws(ax, bx, by, 62, opening=1.30, depth=1.00, color=fs.FAINT, lw=2.6, alpha=0.7, z=3)
    jaws(ax, bx, by, -28, opening=1.30, depth=1.00, color=fs.ACCENT, lw=3.6, z=4)
    ax.add_patch(Arc((bx, by), 2.36, 2.36, theta1=-50, theta2=10, lw=0.9, color=fs.MUTED,
                     ls=(0, (3, 2)), zorder=5))
    ax.annotate("", xy=(bx + 1.18 * np.cos(np.deg2rad(-50)), by + 1.18 * np.sin(np.deg2rad(-50))),
                xytext=(bx + 1.18 * np.cos(np.deg2rad(-61)), by + 1.18 * np.sin(np.deg2rad(-61))),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=0.8, shrinkA=0, shrinkB=0),
                zorder=6)
    fs.label(ax, 6.60, 4.45, "位姿 6 个数", fs=8.8, color=fs.ACCENT, weight="bold")
    fs.label(ax, 6.60, 4.10, "再加一个张开宽度", fs=8.2, color=fs.MUTED)
    fs.label(ax, 6.60, 1.28, "绕接近轴，任意角度", fs=8.3, color=fs.MUTED)
    fs.label(ax, 6.60, 0.55, "(b) 六自由度夹爪", fs=9.4, color=fs.INK, weight="bold")

    # ---------------- (c) 接触点 ----------------
    cx, cy = 11.05, 2.62
    rng = np.random.default_rng(7)
    th = rng.uniform(0, 2 * np.pi, 150)
    rr = 0.58 + rng.normal(0, 0.030, 150)
    px, py = cx + rr * np.cos(th), cy + rr * np.sin(th)
    th2 = rng.uniform(-1.15, 1.15, 55)
    px2 = cx + 0.66 + 0.18 * np.cos(th2)
    py2 = cy + 0.40 * np.sin(th2)
    ax.scatter(np.concatenate([px, px2]), np.concatenate([py, py2]), s=3.2,
               color=fs.FAINT, zorder=3, alpha=0.9)
    c1 = np.array([cx - 0.60, cy + 0.04])
    c2 = np.array([cx + 0.60, cy - 0.04])
    for p, s in ((c1, -1), (c2, 1)):
        ax.add_patch(Circle(p, 0.080, facecolor="white", edgecolor=fs.ACCENT, lw=1.3, zorder=8))
        ax.add_patch(Circle(p, 0.028, facecolor=fs.ACCENT, edgecolor="none", zorder=9))
        ax.annotate("", xy=(p[0] + s * 0.62, p[1] + s * 0.06), xytext=(p[0] + s * 0.13, p[1]),
                    arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.0, shrinkA=2, shrinkB=1),
                    zorder=7)
    ax.annotate("", xy=(c1[0], cy - 0.88), xytext=(c2[0], cy - 0.88),
                arrowprops=dict(arrowstyle="<|-|>", color=fs.INK, lw=0.9, shrinkA=1, shrinkB=1),
                zorder=8)
    for p in (c1, c2):
        ax.plot([p[0], p[0]], [p[1] - 0.09, cy - 0.82], color=fs.FAINT, lw=0.7,
                ls=(0, (2, 2)), zorder=5)
    fs.label(ax, cx, cy - 1.08, "两点距离 = 宽度", fs=8.3, color=fs.INK)
    fs.label(ax, 9.22, 3.50, "接触点 + 法向", fs=8.2, color=fs.BLUE, ha="left")
    fs.label(ax, 11.05, 4.45, "抓在看得见的表面上", fs=8.8, color=fs.ACCENT, weight="bold")
    fs.label(ax, 11.05, 4.10, "位置取自点云，只学转角与宽度", fs=8.2, color=fs.MUTED)
    fs.label(ax, 11.05, 0.55, "(c) 接触点对", fs=9.4, color=fs.INK, weight="bold")

    for x in (4.55, 8.80):
        ax.plot([x, x], [0.35, 5.00], color=fs.GRID, lw=0.8, zorder=1)

    fs.save(fig, "ch05", "fig05-01")


def fig_pipeline():
    """RGB-D 到执行：六段管线与三条失败回退。"""
    fig, ax = fs.canvas(6.9, 3.55)
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0.15, 5.95)

    W, H, G = 1.80, 1.05, 0.42
    x0, yb = 0.28, 4.15
    stages = ["RGB-D\n一帧", "掩码\n与点云", "6D\n位姿", "抓取\n候选", "碰撞\n与可达", "执行\n与复核"]
    xs = [x0 + i * (W + G) for i in range(len(stages))]
    for i, (x, s) in enumerate(zip(xs, stages)):
        ec = fs.ACCENT if i in (1, 2, 5) else fs.INK
        fs.box(ax, x, yb, W, H, s, fs=8.8, ec=ec, fc="#FFFFFF", lw=1.2)
        if i:
            fs.arrow(ax, (xs[i - 1] + W + 0.05, yb + H / 2), (x - 0.05, yb + H / 2),
                     color=fs.INK, lw=1.0, ms=7)

    fs.label(ax, 6.60, 5.62, "每一步都有自己出错的方式，虚线是回去的路", fs=8.8, color=fs.INK)

    fails = [(1, "粘连、漏检"), (2, "对称等价解"), (5, "滑了，抓起空")]
    cw, chh = 1.92, 0.58
    for i, txt in fails:
        cxx = xs[i] + W / 2 - cw / 2
        fs.box(ax, cxx, 2.62, cw, chh, txt, fs=8.2, ec=fs.FAINT, fc="#FCFAF7", lw=0.9)
        fs.arrow(ax, (xs[i] + W / 2, yb - 0.06), (xs[i] + W / 2, 2.62 + chh + 0.06),
                 color=fs.FAINT, lw=0.9, ls=(0, (3, 2)), ms=7)
        fs.arrow(ax, (xs[i] + W / 2, 2.62 - 0.06), (xs[i] + W / 2, 1.66),
                 color=fs.FAINT, lw=0.9, ls=(0, (3, 2)), ms=7)

    ax.plot([xs[5] + W / 2, xs[0] + W / 2], [1.60, 1.60], color=fs.FAINT, lw=0.9,
            ls=(0, (3, 2)), zorder=2)
    fs.arrow(ax, (xs[0] + W / 2, 1.60), (xs[0] + W / 2, yb - 0.06),
             color=fs.FAINT, lw=0.9, ls=(0, (3, 2)), ms=7)
    fs.label(ax, 6.60, 1.18, "重拍一帧，或者换个视角再来", fs=8.4, color=fs.MUTED)
    fs.label(ax, 6.60, 0.52, "失败很少报错，多数时候是安静地给一个错答案", fs=8.4, color=fs.MUTED)

    fs.save(fig, "ch05", "fig05-02")


def fig_force_closure():
    """力闭合：两个接触点、摩擦锥、外载；右侧三种摩擦系数下的锥角。"""
    fig, ax = fs.canvas(6.6, 3.30)
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0.15, 5.25)

    cx, cy, R = 3.05, 2.80, 1.02
    ax.add_patch(Circle((cx, cy), R, facecolor="#E9EDF3", edgecolor=fs.FAINT, lw=1.0, zorder=2))
    ax.add_patch(Circle((cx, cy), R * 0.70, facecolor="#F7F9FC", edgecolor=fs.FAINT, lw=0.8,
                        zorder=3))

    half, L = 31.0, 1.12
    pL = np.array([cx - R, cy])
    pR = np.array([cx + R, cy])
    for p, d in ((pL, 0.0), (pR, 180.0)):
        ax.add_patch(Wedge(p, L, d - half, d + half, facecolor=fs.ACCENT, edgecolor="none",
                           alpha=0.10, zorder=6))
        for sg in (-1, 1):
            e = p + L * np.array([np.cos(np.deg2rad(d + sg * half)),
                                  np.sin(np.deg2rad(d + sg * half))])
            ax.plot([p[0], e[0]], [p[1], e[1]], color=fs.ACCENT, lw=0.6,
                    alpha=0.45, zorder=7)
        ax.add_patch(Arc(p, 2 * L, 2 * L, theta1=d - half, theta2=d + half,
                         lw=0.6, color=fs.ACCENT, alpha=0.45, zorder=7))

    for p, d in ((pL, 1), (pR, -1)):
        ax.annotate("", xy=(p[0] + d * 0.92, p[1]), xytext=(p[0] + d * 0.03, p[1]),
                    arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.4,
                                    shrinkA=1, shrinkB=1), zorder=9)
        ax.add_patch(Circle(p, 0.070, facecolor="white", edgecolor=fs.ACCENT, lw=1.3, zorder=9))
        ax.add_patch(Circle(p, 0.026, facecolor=fs.ACCENT, edgecolor="none", zorder=10))

    LE = "#AEB4BC"
    fs.label(ax, 0.28, 1.94, "接触点", fs=8.4, color=fs.INK, ha="left")
    ax.plot([0.84, pL[0] - 0.09], [1.98, cy - 0.06], color=LE, lw=0.7, zorder=8)
    fs.label(ax, 0.28, 3.86, "摩擦锥", fs=8.4, color=fs.ACCENT, ha="left")
    tx, ty = pL[0] + 0.58 * np.cos(np.deg2rad(31)), cy + 0.58 * np.sin(np.deg2rad(31))
    ax.plot([0.90, tx], [3.82, ty], color=LE, lw=0.7, zorder=8)
    ax.add_patch(Circle((tx, ty), 0.022, facecolor=LE, edgecolor="none", zorder=9))

    ax.annotate("", xy=(cx, cy - R - 1.02), xytext=(cx, cy - R + 0.02),
                arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.5,
                                shrinkA=1, shrinkB=1), zorder=9)
    fs.label(ax, cx + 0.16, cy - R - 0.56, "重力 + 加速", fs=8.5, color=fs.BLUE, ha="left")
    fs.label(ax, cx + 0.16, cy - R - 0.86, "4.1 N（350 g 的杯子）", fs=8.2, color=fs.BLUE, ha="left")

    fs.label(ax, 3.25, 5.02, "两个接触点，两片摩擦锥", fs=9.0, color=fs.INK, weight="bold")
    fs.label(ax, 3.25, 4.66, "载荷要竖直，两个接触力就得斜着凑，", fs=8.3, color=fs.MUTED)
    fs.label(ax, 3.25, 4.38, "斜的那部分全靠摩擦", fs=8.3, color=fs.MUTED)

    ax.plot([6.35, 6.35], [0.30, 4.95], color=fs.GRID, lw=0.8, zorder=1)

    mus = [(0.2, 11, "光滑玻璃 + 干金属"), (0.6, 31, "指面贴橡胶垫"), (1.0, 45, "软胶指面")]
    for i, (mu, hf, note) in enumerate(mus):
        ay = 3.72 - i * 1.20
        ap = (7.00, ay)
        main = (i == 1)
        ax.add_patch(Wedge(ap, 1.02, -hf, hf, facecolor=fs.ACCENT if main else "#E9EBEF",
                           edgecolor=fs.ACCENT if main else fs.FAINT, lw=0.9,
                           alpha=0.32 if main else 0.9, zorder=3))
        ax.plot([ap[0], ap[0] + 1.02], [ay, ay], color=fs.ACCENT if main else fs.FAINT,
                lw=0.8, zorder=4)
        ax.add_patch(Circle(ap, 0.050, facecolor="white",
                            edgecolor=fs.ACCENT if main else fs.FAINT, lw=1.1, zorder=5))
        fs.label(ax, 8.16, ay + 0.26, f"μ = {mu}", fs=8.5, color=fs.INK, ha="left")
        fs.label(ax, 8.16, ay - 0.02, f"锥半角 {hf}°", fs=8.3, color=fs.MUTED, ha="left")
        fs.label(ax, 8.16, ay - 0.30, note, fs=8.0, color=fs.MUTED, ha="left")

    fs.label(ax, 7.00, 5.02, "锥半角 = arctan μ", fs=9.0, color=fs.INK, weight="bold", ha="left")
    fs.label(ax, 7.00, 4.66, "同样的夹持力，锥越窄越容易滑", fs=8.3, color=fs.MUTED, ha="left")

    fs.save(fig, "ch05", "fig05-03")


if __name__ == "__main__":
    fig_grasp_repr()
    fig_pipeline()
    fig_force_closure()
