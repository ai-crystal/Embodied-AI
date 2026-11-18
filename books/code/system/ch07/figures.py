# -*- coding: utf-8 -*-
"""第 7 章插图：三种地图表示、三维场景图、地图的四层抽象。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import figstyle as fs

from scipy.ndimage import distance_transform_edt, gaussian_filter

# ---------- 共用的走廊几何 ----------
XW = 1.2                     # 两侧内壁在 |x| = 1.2
YL = 2.5                     # 走廊两端在 |y| = 2.5
OBS = (0.05, 0.45, -0.9, -0.5)   # 一个箱子 xmin xmax ymin ymax
SEEN_Y = 1.9                 # 只扫到 y = 1.9 为止，再往里是未知
CUT_Y = -0.7                 # 剖面所在的一刀


def corridor_class(d=0.1):
    """返回栅格类别 0 空闲 / 1 占据 / 2 未知，以及格边界坐标。"""
    xe = np.arange(-1.45, 1.45 + 1e-9, d)
    ye = np.arange(-2.75, 2.75 + 1e-9, d)
    cx = 0.5 * (xe[:-1] + xe[1:])
    cy = 0.5 * (ye[:-1] + ye[1:])
    X, Y = np.meshgrid(cx, cy)          # 行是 y，列是 x
    cls = np.ones(X.shape, dtype=int)
    free = (np.abs(X) < XW) & (np.abs(Y) < YL)
    cls[free] = 0
    box = (X > OBS[0]) & (X < OBS[1]) & (Y > OBS[2]) & (Y < OBS[3])
    cls[box] = 1
    cls[(cls == 0) & (Y > SEEN_Y)] = 2
    return cls, xe, ye


def _panel_axes(ax):
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-2.95, 4.30)
    ax.set_aspect("equal")
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.tick_params(labelsize=8, length=2.5)
    ax.set_xlabel("x / m", fontsize=8, labelpad=2)
    ax.set_ylabel("y / m", fontsize=8, labelpad=2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def fig_corridor():
    """同一段走廊的三种表示。"""
    fig = plt.figure(figsize=(7.6, 4.1))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.08, 1.0], wspace=0.40)

    cls, xe, ye = corridor_class()

    # ---------------- (a) 占据栅格 ----------------
    axa = fig.add_subplot(gs[0, 0])
    colors = {0: "#FFFFFF", 1: fs.INK, 2: "#D8DCE2"}
    rgb = np.zeros(cls.shape + (3,))
    for k, c in colors.items():
        rgb[cls == k] = np.array([int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)]) / 255.0
    axa.imshow(rgb, extent=(xe[0], xe[-1], ye[0], ye[-1]), origin="lower",
               interpolation="nearest", zorder=1)
    for xv in np.arange(-1.0, 1.01, 0.5):
        axa.plot([xv, xv], [-YL, YL], color="#DDE1E6", lw=0.5, zorder=2)
    for yv in np.arange(-2.5, 2.51, 0.5):
        axa.plot([-XW, XW], [yv, yv], color="#DDE1E6", lw=0.5, zorder=2)
    _panel_axes(axa)
    axa.set_title("(a) 占据栅格", fontsize=9.5, color=fs.INK, pad=5)

    # 顶部图例
    keys = [(0, "空闲",  "p = 0.05"), (1, "占据", "p = 0.95"), (2, "未知", "p = 0.5")]
    for i, (k, name, p) in enumerate(keys):
        yy = 4.16 - i * 0.34
        axa.add_patch(Rectangle((-1.38, yy - 0.11), 0.22, 0.22, facecolor=colors[k],
                                edgecolor=fs.FAINT, lw=0.6, zorder=5))
        axa.text(-1.08, yy, name, fontsize=8, color=fs.INK, va="center", zorder=6)
        axa.text(-0.45, yy, p, fontsize=8, color=fs.MUTED, va="center", zorder=6)

    axa.text(0.0, 2.15, "未观测", fontsize=8, color=fs.MUTED, ha="center", va="center")
    axa.text(-0.62, -2.05, "空闲", fontsize=8, color=fs.MUTED, ha="center", va="center")
    axa.plot([-1.45, 1.45], [CUT_Y, CUT_Y], color=fs.ACCENT, lw=1.0, ls=(0, (4, 2)), zorder=7)
    axa.text(-0.72, CUT_Y - 0.10, "剖面位置", fontsize=8, color=fs.ACCENT,
             ha="center", va="top", zorder=7)

    # ---------------- (b) TSDF 剖面 ----------------
    axb = fig.add_subplot(gs[0, 1])
    tau = 0.15
    x = np.linspace(-1.45, 1.45, 1201)

    def signed(xs):
        d_wall = XW - np.abs(xs)
        left = OBS[0] - xs
        right = xs - OBS[1]
        outside = np.where(xs < OBS[0], left, right)
        inside = -np.minimum(xs - OBS[0], OBS[1] - xs)
        d_box = np.where((xs > OBS[0]) & (xs < OBS[1]), inside, outside)
        return np.minimum(d_wall, d_box)

    d = signed(x)
    tsdf = np.clip(d, -tau, tau)
    axb.axvspan(-1.45, -XW, color="#E9E7E2", zorder=0)
    axb.axvspan(XW, 1.45, color="#E9E7E2", zorder=0)
    axb.axvspan(OBS[0], OBS[1], color="#E9E7E2", zorder=0)
    axb.axhline(0, color=fs.MUTED, lw=0.7, zorder=1)
    axb.axhline(tau, color=fs.FAINT, lw=0.7, ls=(0, (3, 2)), zorder=1)
    axb.axhline(-tau, color=fs.FAINT, lw=0.7, ls=(0, (3, 2)), zorder=1)
    axb.fill_between(x, -tau, np.minimum(tsdf, 0), color="#C7D7EE", alpha=0.55, zorder=2)
    axb.plot(x, tsdf, color=fs.ACCENT, lw=1.4, zorder=4)
    axb.text(-1.33, 0.185, "墙", fontsize=8, color=fs.MUTED, ha="center", va="center")
    axb.text(0.50, 0.185, "物体", fontsize=8, color=fs.MUTED, ha="center", va="center")
    axb.text(1.33, 0.185, "墙", fontsize=8, color=fs.MUTED, ha="center", va="center")
    axb.set_xlim(-1.55, 1.55)
    axb.set_ylim(-0.21, 0.22)
    axb.set_xticks([-1, 0, 1])
    axb.set_yticks([-tau, 0, tau])
    axb.set_yticklabels(["−0.15", "0 = 表面", "0.15"])
    axb.tick_params(labelsize=8, length=2.5)
    axb.set_xlabel("横穿走廊的位置 x / m", fontsize=8, labelpad=2)
    axb.set_ylabel("TSDF 值 / m", fontsize=8, labelpad=2)
    for s in ("top", "right"):
        axb.spines[s].set_visible(False)
    axb.set_title("(b) TSDF 剖面", fontsize=9.5, color=fs.INK, pad=5)

    # ---------------- (c) ESDF 等值线与梯度 ----------------
    axc = fig.add_subplot(gs[0, 2])
    solid = (cls == 1).astype(float)
    edt = distance_transform_edt(1 - solid, sampling=0.1)
    xx = 0.5 * (xe[:-1] + xe[1:])
    yy = 0.5 * (ye[:-1] + ye[1:])
    Xg, Yg = np.meshgrid(xx, yy)
    fld = np.where(cls == 1, np.nan, gaussian_filter(edt, 1.0))
    solid_rgb = np.ones(cls.shape + (3,))
    solid_rgb[cls == 1] = np.array([0.886, 0.878, 0.859])
    axc.imshow(solid_rgb, extent=(xe[0], xe[-1], ye[0], ye[-1]), origin="lower",
               interpolation="nearest", zorder=1)
    axc.contour(Xg, Yg, fld, levels=[0.2, 0.4, 0.6, 0.8], colors=fs.BLUE,
                linewidths=1.0, zorder=3)

    def grad_at(px, py):
        ix = int(np.argmin(np.abs(xx - px)))
        iy = int(np.argmin(np.abs(yy - py)))
        gy, gx = np.gradient(edt, 0.1, 0.1)
        v = np.array([gx[iy, ix], gy[iy, ix]])
        return np.array([xx[ix], yy[iy]]), v / np.linalg.norm(v)

    pts = [(-0.90, 1.60), (-0.70, 0.70), (-0.90, -0.05), (0.90, 1.30),
           (0.70, 0.60), (0.55, -1.55), (-0.60, -1.80)]
    for px, py in pts:
        p0, v = grad_at(px, py)
        fs.arrow(axc, tuple(p0 - v * 0.18), tuple(p0 + v * 0.18), color=fs.GREEN,
                 lw=1.2, ms=9, z=5)
    _panel_axes(axc)
    axc.set_title("(c) ESDF 等值线与梯度", fontsize=9.5, color=fs.INK, pad=5)
    axc.text(-1.45, 4.16, "等值线 d = 0.2 / 0.4 / 0.6 / 0.8 m", fontsize=8, color=fs.BLUE,
             va="center")
    axc.text(-1.45, 3.82, "箭头为距离增大的方向", fontsize=8, color=fs.GREEN, va="center")
    axc.text(-1.45, 3.48, "灰色为占据栅格里的障碍", fontsize=8, color=fs.MUTED, va="center")

    fs.save(fig, "ch07", "fig07-01")


def fig_graph():
    """三维场景图的节点与边。"""
    fig, ax = fs.canvas(7.2, 4.4)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.9)

    c_room = ("#E8EEF7", fs.BLUE)
    c_obj = ("#EAF3EC", fs.GREEN)
    c_part = ("#FBF1E4", fs.GOLD)

    fs.box(ax, 0.40, 3.30, 2.10, 0.78, "厨房\n（房间）", fc=c_room[0], ec=c_room[1],
           fs=9.2, lw=1.1)

    objs = [("电热水壶", 5.55), ("台面", 4.15), ("水槽", 2.75), ("橱柜", 1.35)]
    for name, y in objs:
        fs.box(ax, 3.20, y, 2.20, 0.70, name, fc=c_obj[0], ec=c_obj[1], fs=9.2, lw=1.1)
    parts = [("壶盖", 5.65), ("下水口", 2.85), ("抽屉", 1.45)]
    for name, y in parts:
        fs.box(ax, 6.30, y, 1.90, 0.50, name, fc=c_part[0], ec=c_part[1], fs=8.8, lw=1.0)

    # 房间 → 物体
    for name, y in objs:
        fs.arrow(ax, (2.52, 3.69), (3.18, y + 0.35), color=fs.FAINT, lw=0.9, ms=7)

    # 物体 → 部件
    for (name, y), (pn, py) in zip([objs[0], objs[2], objs[3]], parts):
        fs.arrow(ax, (5.42, y + 0.35), (6.28, py + 0.25), color=fs.FAINT, lw=0.9, ms=7)
        ax.text(5.86, y + 0.44, "部件", fontsize=8, color=fs.MUTED, ha="center", va="bottom")

    # 物体之间的空间关系
    fs.arrow(ax, (4.30, 5.53), (4.30, 4.87), color=fs.PURPLE, lw=1.0,
             ls=(0, (3.5, 2)), ms=7)
    ax.text(4.42, 5.20, "放在…上", fontsize=8.2, color=fs.PURPLE, ha="left", va="center")
    fs.arrow(ax, (4.30, 2.73), (4.30, 4.13), color=fs.PURPLE, lw=1.0,
             ls=(0, (3.5, 2)), ms=7)
    ax.text(4.18, 3.80, "嵌在…里", fontsize=8.2, color=fs.PURPLE, ha="right", va="center")
    fs.arrow(ax, (3.85, 1.37), (3.85, 2.73), color=fs.PURPLE, lw=1.0,
             ls=(0, (3.5, 2)), ms=7)
    ax.text(4.42, 2.38, "在…下方", fontsize=8.2, color=fs.PURPLE, ha="left", va="center")

    # 图例
    for (fill, ec), name, y in zip([c_room, c_obj, c_part],
                                   ["房间节点", "物体节点", "部件节点"],
                                   [2.55, 2.05, 1.55]):
        ax.add_patch(Rectangle((0.42, y - 0.11), 0.28, 0.22, facecolor=fill,
                               edgecolor=ec, lw=0.9, zorder=3))
        ax.text(0.80, y, name, fontsize=8.2, color=fs.INK, va="center")
    ax.plot([0.42, 0.70], [1.02, 1.02], color=fs.FAINT, lw=0.9)
    ax.text(0.80, 1.02, "结构边（包含 · 部件）", fontsize=8.2, color=fs.MUTED, va="center")
    ax.plot([0.42, 0.70], [0.58, 0.58], color=fs.PURPLE, lw=1.0, ls=(0, (3.5, 2)))
    ax.text(0.80, 0.58, "空间关系边", fontsize=8.2, color=fs.MUTED, va="center")

    ax.text(4.10, 0.55, "每个节点存类别、包围盒、点云、特征向量与最后观测时间",
            fontsize=8, color=fs.MUTED, va="bottom")
    fs.save(fig, "ch07", "fig07-02")


def fig_pyramid():
    """地图的四层抽象，右侧标存储量与更新频率。"""
    fig, ax = fs.canvas(7.0, 4.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.42, 6.5)

    layers = [
        ("几何", "TSDF · 占据 · 点云", 0.35, 6.40, 0.00, "4 MB", "10–30 Hz", "#DCE7F2"),
        ("语义", "每个体素挂一个特征向量", 1.15, 5.85, 1.37, "500 MB", "1–5 Hz", "#CFDEF0"),
        ("对象", "实例 + 位姿 + 包围盒", 1.85, 5.15, 2.74, "1 MB", "约 1 Hz", "#C2D5ED"),
        ("关系", "图边：在…上 / 属于", 2.50, 4.50, 4.11, "13 KB", "0.1 Hz", "#B4CBE9"),
    ]
    h = 1.25
    for name, detail, xl, xr, y, store, freq, color in layers:
        dx = 0.16
        ax.add_patch(Polygon([[xl, y], [xr, y], [xr - dx, y + h], [xl + dx, y + h]],
                             closed=True, facecolor=color, edgecolor="#B9C6D6",
                             lw=0.9, zorder=2))
        ax.text((xl + xr) / 2, y + h * 0.66, name, fontsize=10, color=fs.INK,
                weight="bold", ha="center", va="center", zorder=3)
        ax.text((xl + xr) / 2, y + h * 0.28, detail, fontsize=8.2, color=fs.MUTED,
                ha="center", va="center", zorder=3)
        ax.plot([xr + 0.05, 6.72], [y + h / 2, y + h / 2], color=fs.FAINT, lw=0.6,
                ls=(0, (2, 2)), zorder=1)
        ax.text(7.02, y + h / 2, store, fontsize=9, color=fs.ACCENT, ha="left", va="center")
        ax.text(8.72, y + h / 2, freq, fontsize=9, color=fs.INK, ha="left", va="center")

    ax.text(7.02, 5.55, "存储量级", fontsize=8.4, color=fs.MUTED, ha="left", va="bottom")
    ax.text(8.72, 5.55, "更新频率", fontsize=8.4, color=fs.MUTED, ha="left", va="bottom")
    ax.text(7.02, 1.62, "稠密特征，内存尖峰", fontsize=8, color=fs.MUTED, va="center")

    ax.text(0.05, 5.75, "越往上越抽象", fontsize=8.4, color=fs.FAINT, ha="left", va="bottom")
    ax.text(0.35, -0.28, "按 100 m² 住宅、2.5 cm 体素估算的量级", fontsize=8,
            color=fs.MUTED, ha="left", va="top")
    fs.save(fig, "ch07", "fig07-03")


if __name__ == "__main__":
    fig_corridor()
    fig_graph()
    fig_pyramid()
