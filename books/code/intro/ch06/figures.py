# -*- coding: utf-8 -*-
"""第 6 章插图：三种几何表示、三维场景图、四层抽象金字塔。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
from matplotlib.colors import ListedColormap
from scipy.ndimage import distance_transform_edt
import figstyle as fs

# ---- 场景：一段净宽 1.8 m 的走廊通向一间屋子，屋里有桌子和箱子 ----
WALL = [  # (x0, x1, y0, y1) 墙体
    (1.80, 2.08, 0.00, 5.68), (3.92, 4.20, 0.00, 3.60),   # 下方走廊两侧墙
    (0.00, 1.80, 5.68, 5.96), (4.20, 5.96, 5.68, 5.96),
    (0.00, 0.28, 0.00, 5.96), (5.68, 5.96, 0.00, 5.96),
    (0.00, 1.80, 0.00, 0.28), (3.92, 5.96, 0.00, 0.28),
    (1.80, 2.08, 3.60, 5.96),                             # 走廊上端的两侧短墙延续
    (3.92, 4.20, 0.00, 3.60),
    (4.20, 4.34, 1.60, 3.60),                             # 隔断：把右上角挡在视线外
]
OBST = [(1.05, 2.55, 3.30, 4.00),        # 桌子
        (4.75, 5.25, 4.60, 5.10)]        # 箱子
UNSEEN = [(4.34, 5.68, 1.60, 3.60)]      # 隔断后面的角落，没看过

RES = 0.05
TAU = 0.15


def _raster(res=RES, xr=(0.0, 5.96), yr=(0.0, 5.96)):
    xs = np.arange(xr[0], xr[1] + res / 2, res)
    ys = np.arange(yr[0], yr[1] + res / 2, res)
    X, Y = np.meshgrid(xs, ys, indexing="ij")

    def mask(rects):
        m = np.zeros_like(X, dtype=bool)
        for x0, x1, y0, y1 in rects:
            m |= (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
        return m

    wall = mask(WALL) | mask(OBST)
    unseen = mask(UNSEEN) & ~wall
    free = ~wall & ~unseen
    return xs, ys, X, Y, wall, unseen, free


def fig_three_maps():
    xs, ys, X, Y, wall, unseen, free = _raster()
    _, _, X2, Y2, wall2, unseen2, _ = _raster(res=0.02)
    dist = distance_transform_edt(~(wall2 | unseen2), sampling=(0.02, 0.02))

    fig, axes = plt.subplots(1, 3, figsize=(6.6, 3.45),
                             gridspec_kw=dict(width_ratios=[1.0, 0.92, 1.0], wspace=0.52))

    XL, YL = (-0.35, 6.30), (-1.05, 6.55)

    # ---------------- (a) 占据栅格 ----------------
    ax = axes[0]
    img = np.where(wall, 2, np.where(unseen, 1, 0))
    cmap = ListedColormap(["#FFFFFF", fs.LIGHT, fs.INK])
    ax.imshow(img.T, origin="lower", cmap=cmap, interpolation="nearest",
              extent=[xs[0] - RES / 2, xs[-1] + RES / 2, ys[0] - RES / 2, ys[-1] + RES / 2],
              vmin=0, vmax=2, aspect="equal")
    ax.set_xlim(*XL)
    ax.set_ylim(*YL)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.tick_params(labelsize=8.0, length=2.4)
    ax.set_xlabel("x / m", fontsize=8.2, labelpad=1.5)
    ax.set_ylabel("y / m", fontsize=8.2, labelpad=1.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fs.label(ax, 0.0, 6.22, "(a) 占据栅格", fs=9, color=fs.INK, ha="left", weight="bold")
    ax.text(4.98, 2.60, "没看过", fontsize=8.0, color="#4B5563", ha="center", va="center",
            zorder=7)
    # 剖面线
    ax.plot([1.95, 4.05], [1.00, 1.00], ls=(0, (3, 2)), color=fs.ACCENT, lw=0.9, zorder=6)
    # 图例
    for i, (c, t) in enumerate([(fs.INK, "占据"), ("#FFFFFF", "空闲"), (fs.LIGHT, "未知")]):
        ax.add_patch(Rectangle((0.05 + i * 2.10, -0.62), 0.32, 0.32, facecolor=c,
                               edgecolor=fs.FAINT, lw=0.7, zorder=6))
        fs.label(ax, 0.46 + i * 2.10, -0.46, t, fs=8.0, color=fs.MUTED, ha="left")

    # ---------------- (b) TSDF 剖面 ----------------
    ax = axes[1]
    xv = np.linspace(1.95, 4.05, 900)
    d = np.minimum(xv - 2.08, 3.92 - xv)     # 到最近墙面的有符号距离，室外为正
    tsdf = np.clip(d, -TAU, TAU)
    ax.axhspan(-TAU, TAU, color=fs.PAPER, zorder=0)
    ax.axhline(0, color=fs.FAINT, lw=0.7, zorder=1)
    for xw in (2.08, 3.92):
        ax.axvline(xw, color=fs.FAINT, lw=0.7, ls=(0, (2, 2)), zorder=1)
    ax.plot(xv, tsdf, color=fs.ACCENT, lw=1.7, zorder=4)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlim(1.90, 4.12)
    ax.set_ylim(-0.25, 0.31)
    ax.set_xticks([2.0, 2.5, 3.0, 3.5, 4.0])
    ax.set_yticks([-0.15, 0.0, 0.15])
    ax.set_yticklabels(["-0.15", "0", "+0.15"])
    ax.tick_params(labelsize=8.0, length=2.4)
    ax.set_xlabel("x / m", fontsize=8.2, labelpad=1.5)
    ax.set_ylabel("TSDF / m", fontsize=8.2, labelpad=1.5)
    fs.label(ax, 3.00, 0.245, "整段压平在 +0.15", fs=8.0, color=fs.MUTED)
    fs.label(ax, 1.94, -0.205, "墙内", fs=8.0, color=fs.MUTED, ha="left")
    ax.set_yticks([-0.15, 0.0, 0.15])
    fs.label(ax, 1.95, 0.295, "(b) TSDF 剖面", fs=9, color=fs.INK, ha="left", weight="bold")

    # ---------------- (c) ESDF ----------------
    ax = axes[2]
    dm = np.where(unseen2, np.nan, dist)
    from matplotlib.colors import LinearSegmentedColormap
    cmap2 = LinearSegmentedColormap.from_list("esdf", ["#FFFFFF", "#DCE6F7", "#9FBBEA", fs.BLUE])
    lv = np.arange(0.0, 1.30, 0.1)
    ax.contourf(X2, Y2, dm, levels=lv, cmap=cmap2, vmin=0.0, vmax=1.15, zorder=2)
    ax.contour(X2, Y2, dm, levels=[0.6, 0.9], colors=fs.BLUE,
               linewidths=[0.95, 1.1], zorder=4)
    ax.contour(X2, Y2, dm, levels=[0.3], colors=fs.BLUE, linewidths=[0.8], zorder=4)
    for x0, x1, y0, y1 in WALL + OBST:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="#D0D0D0",
                               edgecolor="#B8B8B8", lw=0.4, zorder=5))
    for x0, x1, y0, y1 in UNSEEN:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="#F4F4F4",
                               edgecolor=fs.FAINT, lw=0.6, hatch="////", zorder=5))
    ax.text(5.00, 2.62, "未测", fontsize=8.0, color=fs.MUTED, ha="center", va="center", zorder=8)
    ax.set_xlim(*XL)
    ax.set_ylim(*YL)
    ax.set_aspect("equal")
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([])
    ax.tick_params(labelsize=8.0, length=2.4)
    ax.set_xlabel("x / m", fontsize=8.2, labelpad=1.5)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    fs.label(ax, 0.0, 6.22, "(c) ESDF", fs=9, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 0.10, -0.46, "深 = 远，间隔 0.3 m", fs=8.0, color=fs.BLUE, ha="left")

    fs.save(fig, "ch06", "fig06-01")


def fig_scene_graph():
    fig, ax = fs.canvas(7.0, 4.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.4)

    # ---------------- (a) 俯视 ----------------
    ax.add_patch(FancyBboxPatch((0.25, 0.95), 3.30, 5.35,
                                boxstyle="round,pad=0.006,rounding_size=0.03",
                                facecolor="#FCFCFB", edgecolor=fs.FAINT, lw=1.0, zorder=1))
    fs.label(ax, 0.45, 6.03, "客厅", fs=8.4, color=fs.MUTED, ha="left")

    ax.add_patch(Rectangle((0.85, 3.35), 1.85, 1.25, facecolor=fs.PAPER,
                           edgecolor=fs.INK, lw=1.0, zorder=3))
    fs.label(ax, 1.26, 3.60, "餐桌", fs=8.2)
    fs.label(ax, 0.85, 3.18, "0.8 m 高", fs=8.0, color=fs.MUTED, ha="left")

    ax.add_patch(Circle((2.28, 3.92), 0.085, facecolor="white", edgecolor=fs.ACCENT, lw=1.2, zorder=4))
    ax.add_patch(Circle((2.39, 3.92), 0.042, facecolor="none", edgecolor=fs.ACCENT, lw=1.0, zorder=4))
    fs.label(ax, 2.12, 4.36, "马克杯", fs=8.0, color=fs.ACCENT)

    ax.add_patch(Circle((1.60, 4.18), 0.22, facecolor="#F6F3EC", edgecolor=fs.MUTED, lw=1.0, zorder=3))
    ax.add_patch(Circle((1.60, 4.18), 0.15, facecolor="none", edgecolor=fs.FAINT, lw=0.7, zorder=3))
    fs.label(ax, 1.60, 4.18, "盘", fs=8.0, color=fs.MUTED)

    ax.add_patch(Rectangle((2.88, 2.15), 0.50, 0.36, facecolor="#F6F3EC",
                           edgecolor=fs.MUTED, lw=1.0, zorder=3))
    fs.label(ax, 3.13, 2.74, "纸巾盒", fs=8.0)

    ax.add_patch(Rectangle((0.85, 1.15), 1.20, 0.62, facecolor="#F1EEE7",
                           edgecolor=fs.MUTED, lw=1.0, zorder=3))
    fs.label(ax, 1.45, 1.46, "橱柜", fs=8.0)
    ax.add_patch(Rectangle((0.85, 1.98), 1.20, 0.95, facecolor="none",
                           edgecolor=fs.FAINT, lw=0.8, ls=(0, (3, 2)), zorder=2))
    fs.label(ax, 1.45, 2.45, "未观察", fs=8.0, color=fs.FAINT)

    fs.label(ax, 1.90, 0.55, "(a) 房间俯视", fs=9, color=fs.INK, weight="bold")

    # ---------------- (b) 图 ----------------
    fs.label(ax, 6.95, 7.08, "(b) 场景图", fs=9, color=fs.INK, weight="bold")

    def node(x, y, w, h, text, kind="obj"):
        if kind == "room":
            fs.box(ax, x, y, w, h, text, fc="#F1EEE7", ec=fs.MUTED, fs=8.8, weight="bold")
        elif kind == "part":
            fs.box(ax, x, y, w, h, text, fc=fs.PAPER, ec=fs.GOLD, fs=8.6, lw=1.1)
            ax.add_patch(FancyBboxPatch((x - 0.05, y - 0.05), w + 0.10, h + 0.10,
                                        boxstyle="round,pad=0.006,rounding_size=0.02",
                                        facecolor="none", edgecolor=fs.GOLD, lw=0.7,
                                        ls=(0, (2, 2)), zorder=2))
        else:
            fs.box(ax, x, y, w, h, text, fc="white", ec=fs.INK, fs=8.4)

    W, H = 1.30, 0.46
    node(6.25, 6.05, W, H, "客厅", "room")
    node(5.05, 4.55, W, H, "餐桌")
    node(7.55, 4.55, W, H, "橱柜")
    node(4.35, 3.05, W, H, "马克杯")
    node(6.35, 3.05, W, H, "盘")
    node(8.35, 3.05, W, H, "纸巾盒")
    node(6.10, 1.45, W, H, "杯身", "part")
    node(4.35, 1.45, W, H, "杯柄", "part")

    def rel(p0, p1, text, dx=0.0, dy=0.0, color=fs.MUTED, dash=False):
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.0,
                                    shrinkA=1, shrinkB=1,
                                    linestyle=(0, (3, 2)) if dash else "-"))
        mx, my = (p0[0] + p1[0]) / 2 + dx, (p0[1] + p1[1]) / 2 + dy
        ax.text(mx, my, text, fontsize=8.0, color=color, ha="center", va="center",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0), zorder=10)

    rel((6.55, 6.03), (5.80, 5.03), "内含", dx=-0.12, dy=0.05)
    rel((7.25, 6.03), (8.05, 5.03), "内含", dx=0.16, dy=0.05)
    rel((5.62, 4.53), (5.10, 3.53), "上", dx=-0.16, dy=0.02)
    rel((6.02, 4.53), (6.90, 3.53), "上", dx=0.16, dy=0.02)
    rel((8.20, 4.53), (8.90, 3.53), "内", dx=0.15, dy=0.02)
    rel((4.80, 3.03), (4.95, 1.93), "部件", dx=-0.24, dy=0.10, color=fs.GOLD, dash=True)
    rel((5.42, 3.03), (6.55, 1.93), "部件", dx=0.20, dy=0.12, color=fs.GOLD, dash=True)

    ax.plot([3.95, 4.42], [0.62, 0.62], color=fs.MUTED, lw=1.0)
    ax.annotate("", xy=(4.48, 0.62), xytext=(4.38, 0.62),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0))
    fs.label(ax, 4.58, 0.62, "空间关系", fs=8.0, color=fs.MUTED, ha="left")
    ax.plot([6.20, 6.67], [0.62, 0.62], color=fs.GOLD, lw=1.0, ls=(0, (3, 2)))
    ax.annotate("", xy=(6.73, 0.62), xytext=(6.63, 0.62),
                arrowprops=dict(arrowstyle="-|>", color=fs.GOLD, lw=1.0))
    fs.label(ax, 6.83, 0.62, "组成关系", fs=8.0, color=fs.GOLD, ha="left")

    fs.save(fig, "ch06", "fig06-02")


def fig_pyramid():
    fig, ax = fs.canvas(6.9, 3.85)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)

    cx = 3.20
    layers = [
        ("几何", "占据栅格 · 体素 · TSDF · ESDF", "3 千万体素（2 cm）", "约 100 MB", "30 Hz"),
        ("语义", "每个体素挂一个 512 维向量", "216 万向量（5 cm）", "2 GB", "5-10 Hz"),
        ("对象", "掩码 · 中心 · 外框 · 一句描述", "几十个节点", "约 100 KB", "1 Hz"),
        ("关系", "上 / 内 / 旁 + 属于 + 部件", "上百条边", "约 10 KB", "进任务时重建"),
    ]
    h = 1.28
    gap = 0.10
    y0 = 0.55
    for i, (name, sub, cnt, mem, freq) in enumerate(layers):
        hw = 2.92 - i * 0.52
        y = y0 + i * (h + gap)
        fc = ["#F3F4F6", "#F6F3EC", "#FBF7F0", "#FFFFFF"][i]
        ec = [fs.MUTED, fs.GOLD, fs.ACCENT, fs.INK][i]
        ax.add_patch(FancyBboxPatch((cx - hw, y), 2 * hw, h,
                                    boxstyle="round,pad=0.006,rounding_size=0.03",
                                    facecolor=fc, edgecolor=ec, lw=1.1, zorder=3))
        fs.label(ax, cx, y + h - 0.36, name, fs=11.5, color=ec, weight="bold")
        fs.label(ax, cx, y + 0.32, sub, fs=8.0, color=fs.MUTED)
        fs.label(ax, 6.55, y + h / 2 + 0.24, cnt, fs=8.2, color=fs.INK, ha="left")
        fs.label(ax, 6.55, y + h / 2 - 0.10, mem, fs=8.2, color=fs.ACCENT, ha="left")
        fs.label(ax, 8.95, y + h / 2, freq, fs=8.4, color=fs.BLUE, ha="left")

    fs.label(ax, 6.55, 5.98, "存储量", fs=8.6, color=fs.MUTED, ha="left")
    fs.label(ax, 8.95, 5.98, "更新频率", fs=8.6, color=fs.MUTED, ha="left")
    ax.plot([8.75, 8.75], [0.45, 6.05], color=fs.GRID, lw=0.8, zorder=1)

    ax.annotate("", xy=(0.22, 5.62), xytext=(0.22, 0.62),
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=1.0))
    ax.text(0.09, 3.12, "越往上越抽象", fontsize=8.2, color=fs.MUTED,
            rotation=90, ha="center", va="center")

    ax.text(5.35, 0.15, "同一次观测，四层各写一遍；越往下越贵，越往上越像人能说的话",
            fontsize=8.2, color=fs.MUTED, ha="center", va="center")

    fs.save(fig, "ch06", "fig06-03")


if __name__ == "__main__":
    fig_three_maps()
    fig_scene_graph()
    fig_pyramid()
