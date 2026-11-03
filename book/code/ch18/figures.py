# -*- coding: utf-8 -*-
"""第 18 章插图：力闭合与形闭合、视触觉剖面、手内旋转三阶段。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge, Circle, FancyArrowPatch, Polygon, FancyBboxPatch
import figstyle as fs


def fig_closures():
    """(a) 两指对顶的力闭合；(b) 三指围住的形闭合。"""
    fig, ax = fs.canvas(6.6, 2.70)
    ax.set_xlim(0.85, 9.05)
    ax.set_ylim(1.15, 4.50)
    ax.set_aspect("equal")

    # 分栏细线
    ax.plot([4.70, 4.70], [1.25, 4.10], color=fs.GRID, lw=1.0, zorder=0)

    # ---------------- (a) 力闭合 ----------------
    obj_x0, obj_x1 = 2.00, 3.25
    obj_y0, obj_y1 = 1.95, 3.25
    cy = 2.60
    ax.add_patch(Rectangle((obj_x0, obj_y0), obj_x1 - obj_x0, obj_y1 - obj_y0,
                           facecolor="#F5EFE6", edgecolor=fs.INK, lw=1.1, zorder=2))
    fs.label(ax, 2.62, 2.18, "物体", fs=8.8)

    for x0 in (1.30, 3.25):
        ax.add_patch(Rectangle((x0, 1.85), 0.70, 1.50, facecolor="#E8EAED",
                               edgecolor=fs.MUTED, lw=0.9, zorder=3))

    # 摩擦锥
    half = 32
    ax.add_patch(Wedge((obj_x0, cy), 0.46, -half, half, facecolor=fs.ACCENT,
                       edgecolor=fs.ACCENT, lw=0.7, alpha=0.14, zorder=4))
    ax.add_patch(Wedge((obj_x1, cy), 0.46, 180 - half, 180 + half, facecolor=fs.ACCENT,
                       edgecolor=fs.ACCENT, lw=0.7, alpha=0.14, zorder=4))
    fs.label(ax, 2.14, 3.06, "摩擦锥", fs=8.0, color=fs.ACCENT, ha="left")

    # 法向压力与摩擦力
    for cx in (obj_x0, obj_x1):
        d = 1 if cx == obj_x0 else -1
        fs.arrow(ax, (cx + d * 0.02, cy), (cx + d * 0.34, cy), color=fs.INK, lw=1.2, z=6)
        ax.scatter([cx], [cy], s=26, color=fs.ACCENT, zorder=7, edgecolor="white", linewidth=0.6)
    fs.label(ax, 2.47, 2.79, "N", fs=8.0, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 3.02, 2.79, "N", fs=8.0, color=fs.INK, ha="right", weight="bold")

    fs.arrow(ax, (2.14, 2.44), (2.14, 2.78), color=fs.BLUE, lw=1.1, z=6)
    fs.arrow(ax, (3.11, 2.44), (3.11, 2.78), color=fs.BLUE, lw=1.1, z=6)
    fs.label(ax, 2.19, 2.34, "f", fs=8.0, color=fs.BLUE, ha="left", weight="bold")

    # 外载
    fs.arrow(ax, (2.62, 3.78), (2.62, 3.31), color=fs.GOLD, lw=1.2)
    fs.label(ax, 2.70, 3.64, "外载", fs=8.0, color=fs.GOLD, ha="left")

    fs.label(ax, 2.60, 4.32, "(a) 力闭合", fs=9.6, weight="bold")
    fs.label(ax, 2.60, 1.62, "N 压力，f 摩擦力，扇形为摩擦锥", fs=8.0, color=fs.MUTED)
    fs.label(ax, 2.60, 1.32, "锥内可抵抗剪切，锥外打滑", fs=8.2, color=fs.MUTED)

    # ---------------- (b) 形闭合 ----------------
    cx, cyy, r = 7.05, 2.60, 0.60
    ax.add_patch(Circle((cx, cyy), r, facecolor="#F5EFE6", edgecolor=fs.INK, lw=1.1, zorder=2))
    fs.label(ax, cx, cyy, "物体", fs=8.8)

    for deg in (90, 210, 330):
        th = np.deg2rad(deg)
        u = np.array([np.cos(th), np.sin(th)])
        p_in = np.array([cx, cyy]) + u * r
        p_ad = np.array([cx, cyy]) + u * (r + 0.055)
        t = np.array([-u[1], u[0]]) * 0.30
        ax.plot([p_ad[0] - t[0], p_ad[0] + t[0]], [p_ad[1] - t[1], p_ad[1] + t[1]],
                color="#B6C0CC", lw=8, solid_capstyle="round", zorder=4)
        fs.arrow(ax, tuple(p_in + u * 0.02), tuple(np.array([cx, cyy]) + u * (r - 0.38)),
                 color=fs.ACCENT, lw=1.2, z=6)
        ax.scatter([p_in[0]], [p_in[1]], s=26, color=fs.ACCENT, zorder=7,
                   edgecolor="white", linewidth=0.6)

    fs.label(ax, 7.05, 4.32, "(b) 形闭合", fs=9.6, weight="bold")
    fs.label(ax, 7.05, 1.62, "三个接触点围住物体", fs=8.0, color=fs.MUTED)
    fs.label(ax, 7.05, 1.32, "摩擦为零也不脱手", fs=8.2, color=fs.MUTED)

    fs.save(fig, "ch18", "fig18-01")


def fig_vision_tactile():
    """视触觉传感器剖面：LED 打光、涂层形变、相机成像。"""
    fig, ax = fs.canvas(6.6, 2.38)
    ax.set_xlim(0, 10)
    ax.set_ylim(0.55, 4.15)
    ax.set_aspect("equal")

    # 外壳
    ax.add_patch(FancyBboxPatch((1.85, 0.95), 4.50, 2.55,
                                boxstyle="round,pad=0.01,rounding_size=0.06",
                                facecolor="white", edgecolor=fs.MUTED, lw=1.0, zorder=1))
    # 弹性体：下表面随接触形变
    xs = np.linspace(1.85, 6.35, 400)
    shoulder = 0.5 * (1 + np.tanh((xs - 3.92) / 0.10)) * 0.5 * (1 + np.tanh((5.28 - xs) / 0.10))
    dent = 0.30 * shoulder
    ys = 2.30 - dent
    poly = [(1.85, 3.50), (6.35, 3.50)] + list(zip(xs[::-1], ys[::-1]))
    ax.add_patch(Polygon(poly, closed=True, facecolor="#DDEBF3", edgecolor=fs.BLUE,
                         lw=1.4, alpha=0.95, zorder=2))
    fs.label(ax, 2.02, 3.34, "透明弹性体", fs=8.2, color=fs.BLUE, ha="left")

    # 物体
    ax.add_patch(FancyBboxPatch((3.95, 3.50), 1.30, 0.55,
                                boxstyle="round,pad=0.01,rounding_size=0.03",
                                facecolor="#F0E4D3", edgecolor=fs.GOLD, lw=1.0, zorder=5))
    fs.label(ax, 4.60, 3.775, "物体", fs=8.2, color=fs.GOLD)

    # 标记点
    mx = np.array([2.10, 2.45, 2.80, 3.12, 3.40, 3.64, 3.85, 4.05, 4.28, 4.55,
                   4.80, 5.05, 5.22, 5.40, 5.66, 5.95, 6.20])
    my = 2.30 - 0.30 * (0.5 * (1 + np.tanh((mx - 3.92) / 0.10)) * 0.5 * (1 + np.tanh((5.28 - mx) / 0.10)))
    ax.scatter(mx, my, s=12, color=fs.PINK, zorder=7, linewidths=0)

    # 相机
    ax.add_patch(Rectangle((4.15, 1.00), 1.00, 0.64, facecolor="#EDF1F5",
                           edgecolor=fs.INK, lw=0.9, zorder=4))
    ax.add_patch(Polygon([[4.28, 1.64], [5.02, 1.64], [5.14, 1.86], [4.16, 1.86]],
                         closed=True, facecolor="#DDE5EE", edgecolor=fs.INK, lw=0.8, zorder=4))
    fs.label(ax, 4.65, 1.32, "相机", fs=8.2)

    # 视场
    ax.plot([4.65, 2.55], [1.86, 2.26], color=fs.FAINT, lw=0.7, ls=(0, (2, 3)), zorder=2)
    ax.plot([4.65, 6.05], [1.86, 2.26], color=fs.FAINT, lw=0.7, ls=(0, (2, 3)), zorder=2)

    # LED 与光线
    coat = lambda x: 2.30 - 0.30 * (0.5 * (1 + np.tanh((x - 3.92) / 0.10)) *
                                    0.5 * (1 + np.tanh((5.28 - x) / 0.10)))
    for lx, tx in ((2.38, 3.55), (5.82, 5.05)):
        ax.add_patch(Circle((lx, 2.02), 0.09, facecolor=fs.GOLD, edgecolor="white", lw=0.6, zorder=6))
        ax.plot([lx + 0.09, tx], [2.09, coat(tx)], color=fs.GOLD, lw=0.9, alpha=0.85, zorder=5)
        ax.plot([lx + 0.09, tx + 0.32], [2.09, coat(tx + 0.32)], color=fs.GOLD, lw=0.9,
                alpha=0.5, zorder=5)
        fs.label(ax, lx, 1.82, "LED", fs=8.0, color=fs.GOLD)

    # 形变深度
    ax.plot([3.92, 5.28], [2.30, 2.30], color=fs.FAINT, lw=0.8, ls=(0, (3, 2)), zorder=3)
    fs.label(ax, 4.38, 2.15, "下凹 δ", fs=8.0, color=fs.MUTED, ha="left")

    # 右侧引注
    fs.arrow(ax, (6.44, 2.56), (5.86, 2.32), color=fs.MUTED, lw=0.9)
    fs.label(ax, 6.50, 2.62, "反射涂层与标记点", fs=8.2, ha="left")
    fs.label(ax, 6.50, 1.45, "形变幅度已放大", fs=8.0, color=fs.FAINT, ha="left")

    fs.save(fig, "ch18", "fig18-02")


def _rot_square(cx, cy, side, deg):
    th = np.deg2rad(deg)
    c, s = np.cos(th), np.sin(th)
    pts = []
    for dx, dy in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
        x, y = dx * side, dy * side
        pts.append((cx + c * x - s * y, cy + s * x + c * y))
    return pts


def _pad(ax, cx, cy, deg, dist, color="#C9D2DC", lw=8, alpha=1.0, ls="-", half=0.27):
    th = np.deg2rad(deg)
    u = np.array([np.cos(th), np.sin(th)])
    p = np.array([cx, cy]) + u * dist
    t = np.array([-u[1], u[0]]) * half
    ax.plot([p[0] - t[0], p[0] + t[0]], [p[1] - t[1], p[1] + t[1]],
            color=color, lw=lw, solid_capstyle="round", alpha=alpha, ls=ls, zorder=6)


def _cross_x(pts, y0):
    """多边形与水平线的交点中最小的 x。"""
    xs = []
    n = len(pts)
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        if abs(y2 - y1) < 1e-9:
            if abs(y0 - y1) < 1e-9:
                xs += [x1, x2]
            continue
        t = (y0 - y1) / (y2 - y1)
        if -1e-9 <= t <= 1 + 1e-9:
            xs.append(x1 + t * (x2 - x1))
    return min(xs), max(xs)


def _cross_y(pts, x0):
    """多边形与竖直线的交点中最小的 y。"""
    ys = []
    n = len(pts)
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        if abs(x2 - x1) < 1e-9:
            if abs(x0 - x1) < 1e-9:
                ys += [y1, y2]
            continue
        t = (x0 - x1) / (x2 - x1)
        if -1e-9 <= t <= 1 + 1e-9:
            ys.append(y1 + t * (y2 - y1))
    return min(ys), max(ys)


def fig_inhand():
    """手内旋转三阶段：夹紧、松一侧受控滑动、换指接住。"""
    fig, ax = fs.canvas(6.6, 1.65)
    ax.set_xlim(0, 15)
    ax.set_ylim(1.15, 4.90)
    ax.set_aspect("equal")

    data = [
        (2.5, 0, "夹紧", "两侧对顶，法向力留余量", "a"),
        (7.5, 30, "松一侧并转动", "切向推，接触转为受控滑动", "b"),
        (12.5, 90, "换指接住", "接触点整体前移一格", "c"),
    ]
    side = 1.05
    cy = 3.15

    for cx, deg, name, desc, tag in data:
        pts = _rot_square(cx, cy, side, deg)
        ax.add_patch(Polygon(pts, closed=True, facecolor="#F5EFE6", edgecolor=fs.INK,
                             lw=1.1, zorder=3))

        xl, xr = _cross_x(pts, cy)
        yb, _ = _cross_y(pts, cx)

        _pad(ax, cx, cy, 180, abs(xl - cx) + 0.16)
        if tag == "b":
            _pad(ax, cx, cy, 0, abs(xr - cx) + 0.48, alpha=0.35, ls=(0, (2, 2)))
        else:
            _pad(ax, cx, cy, 0, abs(xr - cx) + 0.16)
        if tag == "c":
            _pad(ax, cx, cy, 270, abs(yb - cy) + 0.16, color="#7FB3AC")
        else:
            _pad(ax, cx, cy, 270, abs(yb - cy) + 0.16, alpha=0.45)

        ax.scatter([xl], [cy], s=52, color=fs.ACCENT, zorder=8, edgecolor="white", lw=0.8)
        ax.scatter([xr], [cy], s=52,
                   color=fs.ACCENT if tag != "b" else "white", zorder=8,
                   edgecolor=fs.ACCENT, lw=1.2)
        if tag == "c":
            ax.scatter([cx], [yb], s=52, color=fs.TEAL, zorder=8, edgecolor="white", lw=0.8)

        if deg > 0:
            ax.add_patch(FancyArrowPatch((cx + 0.60, cy + 0.98), (cx - 0.50, cy + 0.98),
                                         connectionstyle="arc3,rad=-0.30",
                                         arrowstyle="-|>", mutation_scale=11,
                                         color=fs.ACCENT, lw=1.1, zorder=9))
            fs.label(ax, cx + 0.70, cy + 1.06, f"转 {deg}°", fs=8.0, color=fs.ACCENT, ha="left")

        fs.label(ax, cx, 1.84, name, fs=9.0, weight="bold")
        fs.label(ax, cx, 1.40, desc, fs=8.0, color=fs.MUTED)
        fs.label(ax, cx - 1.95, 4.58, f"({tag})", fs=8.6, color=fs.MUTED)

    for x0, x1 in ((4.60, 5.35), (9.60, 10.35)):
        fs.arrow(ax, (x0, cy), (x1, cy), color=fs.FAINT, lw=1.0, ms=10)

    fs.save(fig, "ch18", "fig18-03")


if __name__ == "__main__":
    fig_closures()
    fig_vision_tactile()
    fig_inhand()
