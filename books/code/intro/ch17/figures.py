# -*- coding: utf-8 -*-
"""第 17 章插图：力闭合与形闭合、视触觉传感器剖面、手内旋转三阶段。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, FancyBboxPatch
import figstyle as fs

CHAR = 6.6 * 72.0 / 10.0   # xlim 取 0-10 时每个数据单位对应的磅数


def tw(text, size):
    """估算文本宽度（数据单位），中文按 1.0 em，西文按 0.56 em。"""
    w = 0.0
    for ch in text:
        w += 1.0 if ord(ch) > 0x2E80 else 0.56
    return w * size / CHAR


def fig_closures():
    """(a) 力闭合：两点夹持 + 摩擦锥；(b) 形闭合：手指与掌心围住物体。"""
    fig, ax = fs.canvas(6.6, 3.4)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.1)

    # ---------------- (a) ----------------
    ax.text(0.35, 4.82, "(a) 力闭合", ha="left", va="center", fontsize=10.2,
            color=fs.ACCENT, weight="bold")

    ox, oy, ow, oh = 1.90, 2.30, 1.20, 1.65
    cy = oy + oh / 2

    fs.box(ax, 1.12, cy - 0.58, 0.72, 1.16, "", fc="#E8EDF3", ec=fs.INK, lw=1.1)
    fs.box(ax, 3.16, cy - 0.58, 0.72, 1.16, "", fc="#E8EDF3", ec=fs.INK, lw=1.1)
    fs.box(ax, ox, oy, ow, oh, "", fc="#FFFFFF", ec=fs.INK, lw=1.2)

    # 两侧摩擦锥
    for sx, sgn in ((ox, 1), (ox + ow, -1)):
        tip = (sx + sgn * 0.62 * np.cos(np.deg2rad(25)),
               cy + 0.62 * np.sin(np.deg2rad(25)))
        ax.add_patch(Polygon([[sx, cy], tip, [tip[0], 2 * cy - tip[1]]], closed=True,
                             facecolor=fs.ACCENT, alpha=0.10, edgecolor="none", zorder=3))
        for yy in (tip[1], 2 * cy - tip[1]):
            ax.plot([sx, tip[0]], [cy, yy], color=fs.ACCENT, lw=1.0,
                    ls=(0, (3, 2)), zorder=4)
        ax.plot([sx], [cy], marker="o", ms=4.2, color=fs.ACCENT, zorder=6)

    fs.label(ax, ox + ow / 2, cy + 0.50, "物体", fs=9, color=fs.INK)

    # 外载
    fs.arrow(ax, (ox + 0.60, oy - 0.08), (ox + 0.60, oy - 0.78), color=fs.BLUE, lw=1.3)
    fs.label(ax, ox + 0.46, oy - 0.42, "外载", fs=9, color=fs.BLUE, ha="right")

    fs.label(ax, 0.35, 0.98, "橙色虚线是摩擦锥，半角由 μ 决定", fs=8.8, color=fs.MUTED, ha="left")
    fs.label(ax, 0.35, 0.56, "两个指面压住物体，靠摩擦力顶住外载", fs=9, color=fs.INK, ha="left")
    fs.label(ax, 0.35, 0.20, "μ 从 0.6 掉到 0.2，同一个抓取就滑", fs=8.8, color=fs.MUTED, ha="left")

    # ---------------- (b) ----------------
    ax.text(5.35, 4.82, "(b) 形闭合", ha="left", va="center", fontsize=10.2,
            color=fs.GREEN, weight="bold")

    cx, cy2, r = 7.62, 2.98, 0.70

    ax.add_patch(FancyBboxPatch((cx - 1.12, 1.76), 2.24, 0.52,
                                boxstyle="round,pad=0.01,rounding_size=0.12",
                                facecolor="#EDF3EE", edgecolor=fs.GREEN, lw=1.1, zorder=2))
    ax.add_patch(Circle((cx, cy2), r, facecolor="#FFFFFF", edgecolor=fs.INK, lw=1.2, zorder=3))
    fs.label(ax, cx, cy2 + 0.06, "物体", fs=9, color=fs.INK, z=5)

    fs.box(ax, cx - 1.66, cy2 - 0.32, 0.44, 0.64, "", fc="#EDF3EE", ec=fs.GREEN, lw=1.1)
    fs.box(ax, cx + 1.22, cy2 - 0.32, 0.44, 0.64, "", fc="#EDF3EE", ec=fs.GREEN, lw=1.1)
    fs.box(ax, cx - 0.32, cy2 + 0.80, 0.64, 0.42, "", fc="#EDF3EE", ec=fs.GREEN, lw=1.1)

    # 四个接触点与法向
    for dx, dy, gap in ((-1, 0, 0.38), (1, 0, 0.38), (0, 1, 0.38), (0, -1, 0.20)):
        px, py = cx + dx * r, cy2 + dy * r
        ax.plot([px], [py], marker="o", ms=4.2, color=fs.GREEN, zorder=7)
        ax.annotate("", xy=(px + dx * 0.04, py + dy * 0.04),
                    xytext=(px + dx * gap, py + dy * gap),
                    arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=1.0,
                                    shrinkA=1, shrinkB=2), zorder=6)

    fs.label(ax, cx, 0.98, "手指与掌心围住物体", fs=9, color=fs.INK)
    fs.label(ax, cx, 0.56, "物体要动，先得挤开一根手指", fs=8.8, color=fs.MUTED)
    fs.label(ax, cx, 0.20, "摩擦系数为零也锁得住", fs=8.8, color=fs.MUTED)

    fs.save(fig, "ch17", "fig17-01")


def fig_tactile():
    """视触觉传感器剖面 + 相机输出。"""
    fig, ax = fs.canvas(6.6, 3.6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.3)

    # 指尖外壳与透明弹性体
    ax.add_patch(FancyBboxPatch((0.32, 0.46), 5.90, 4.30,
                                boxstyle="round,pad=0.02,rounding_size=0.18",
                                facecolor="#F7F7F5", edgecolor=fs.FAINT, lw=1.0, zorder=1))
    ax.add_patch(Rectangle((0.52, 0.64), 5.50, 3.70, facecolor="#EAF1F5",
                           edgecolor="none", zorder=2))

    # 反光涂层（中间被压出凹陷）
    xs = np.linspace(0.52, 6.02, 400)
    ys = 4.18 - 0.30 * np.exp(-((xs - 2.55) ** 2) / (2 * 0.40 ** 2))
    ax.fill_between(xs, ys, ys + 0.09, color=fs.ACCENT, alpha=0.8, zorder=5)
    ax.plot(xs, ys, color=fs.ACCENT, lw=1.1, zorder=6)

    # 压上来的物体（底面跟着胶膜一起凹）
    xo = np.linspace(1.95, 3.15, 60)
    yb = 4.18 - 0.30 * np.exp(-((xo - 2.55) ** 2) / (2 * 0.40 ** 2)) + 0.012
    pts = list(zip(xo, yb)) + [(3.05, 4.60), (2.05, 4.60)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="#DCE3EA", edgecolor=fs.INK,
                         lw=1.1, zorder=6))
    fs.label(ax, 2.55, 5.02, "物体", fs=9, color=fs.INK)

    # 相机与视场
    ax.add_patch(Polygon([[2.32, 1.44], [2.78, 1.44], [3.52, 4.16], [1.58, 4.16]],
                         closed=True, facecolor=fs.BLUE, alpha=0.06, edgecolor="none", zorder=2))
    ax.plot([2.55, 1.58], [1.44, 4.16], color=fs.BLUE, lw=0.8, ls=(0, (2, 2)), zorder=3)
    ax.plot([2.55, 3.52], [1.44, 4.16], color=fs.BLUE, lw=0.8, ls=(0, (2, 2)), zorder=3)
    fs.box(ax, 2.05, 0.80, 1.00, 0.62, "", fc="#FFFFFF", ec=fs.INK, lw=1.0)

    # LED 与光线
    for x0, col, dirs in ((0.95, fs.GOLD, (1.95, 2.55)),
                          (5.45, fs.TEAL, (2.55, 3.15))):
        ax.add_patch(Polygon([[x0 - 0.24, 1.98], [x0 + 0.24, 1.98], [x0, 2.42]],
                             closed=True, facecolor=col, edgecolor="none", zorder=6))
        for xe in dirs:
            ax.plot([x0, xe], [2.44, 4.14], color=col, lw=0.7, alpha=0.6, zorder=4)

    # 编号
    marks = [(2.55, 1.11, "1", fs.INK), (0.56, 2.16, "2", fs.GOLD),
             (5.84, 2.16, "2", fs.TEAL), (0.86, 1.30, "3", fs.BLUE),
             (5.80, 4.52, "4", fs.ACCENT)]
    for mx, my, s, col in marks:
        ax.add_patch(Circle((mx, my), 0.145, facecolor="white", edgecolor=col,
                            lw=0.9, zorder=9))
        ax.text(mx, my - 0.005, s, ha="center", va="center", fontsize=8.2,
                color=col, zorder=10)

    # 图例
    fs.label(ax, 3.20, 0.16, "1 相机　　2 LED　　3 透明弹性体　　4 反光涂层",
             fs=8.6, color=fs.MUTED)

    # 相机输出
    gx, gy = np.meshgrid(np.linspace(-1, 1, 120), np.linspace(-1, 1, 90))
    d = np.exp(-((gx - 0.05) ** 2 + (gy + 0.05) ** 2) / 0.10)
    img = np.clip(np.stack([0.90 - 0.62 * d * (gx + 0.30),
                            0.88 - 0.50 * d * (gy - 0.25),
                            0.74 + 0.34 * d], axis=-1), 0, 1)
    ax.imshow(img, extent=(7.05, 9.72, 2.70, 4.60), aspect="auto", zorder=2)
    ax.add_patch(Rectangle((7.05, 2.70), 2.67, 1.90, facecolor="none",
                           edgecolor=fs.INK, lw=1.0, zorder=5))
    fs.label(ax, 8.39, 4.82, "相机看到的一帧", fs=9, color=fs.INK)
    fs.label(ax, 8.39, 2.40, "颜色与明暗对应表面法线", fs=8.4, color=fs.MUTED)
    fs.label(ax, 8.39, 2.06, "红绿蓝三通道 = 三个光照方向", fs=8.4, color=fs.MUTED)
    fs.label(ax, 8.39, 1.62, "2 cm 感应区配 640×480 相机", fs=8.4, color=fs.MUTED)
    fs.label(ax, 8.39, 1.28, "每个像素约 0.03 mm", fs=8.4, color=fs.MUTED)

    fs.save(fig, "ch17", "fig17-02")


def _finger(ax, x, y, dashed=False):
    ec = fs.FAINT if dashed else fs.INK
    fc = "#FFFFFF" if dashed else "#E8EDF3"
    ax.add_patch(FancyBboxPatch((x - 0.20, y - 0.26), 0.40, 0.52,
                                boxstyle="round,pad=0.01,rounding_size=0.09",
                                facecolor=fc, edgecolor=ec, lw=1.0,
                                linestyle=(0, (3, 2)) if dashed else "-", zorder=4))


def _rod(ax, cx, cy, deg, half=0.82, lw=9.0, color=fs.INK):
    a = np.deg2rad(deg)
    dx, dy = np.cos(a) * half, np.sin(a) * half
    ax.plot([cx - dx, cx + dx], [cy - dy, cy + dy], color=color, lw=lw,
            solid_capstyle="round", zorder=3)
    return a


def fig_inhand():
    """手内旋转三阶段：两点捏住 -> 单点推转 -> 重新合上。"""
    fig, ax = fs.canvas(6.6, 3.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.9)

    centers = [1.85, 5.00, 8.15]
    cy = 3.10
    R = 0.095

    # (a) 两点捏住
    ax.text(centers[0] - 1.06, 4.56, "(a)", ha="left", va="center", fontsize=9.4,
            color=fs.MUTED, weight="bold")
    _rod(ax, centers[0], cy, 0)
    for s in (-1, 1):
        ax.plot([centers[0]], [cy + s * R], marker="o", ms=4.0, color=fs.ACCENT, zorder=6)
        _finger(ax, centers[0], cy + s * 0.34)
    fs.label(ax, centers[0], 1.50, "两点捏住", fs=8.8, color=fs.INK)
    fs.label(ax, centers[0], 1.12, "接触点 2 个", fs=8.4, color=fs.ACCENT)

    # (b) 单点推转
    ax.text(centers[1] - 1.06, 4.56, "(b)", ha="left", va="center", fontsize=9.4,
            color=fs.MUTED, weight="bold")
    a = _rod(ax, centers[1], cy, 40)
    n = np.array([np.sin(a), -np.cos(a)])
    p = np.array([centers[1], cy]) + R * n
    ax.plot([p[0]], [p[1]], marker="o", ms=4.0, color=fs.ACCENT, zorder=6)
    fp = p + 0.31 * n
    _finger(ax, fp[0], fp[1])
    gp = np.array([centers[1], cy]) - 0.425 * n
    _finger(ax, gp[0], gp[1], dashed=True)
    ax.annotate("", xy=(gp[0] - 0.52, gp[1] + 0.30), xytext=(gp[0] - 0.16, gp[1] + 0.10),
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=0.9,
                                shrinkA=1, shrinkB=1), zorder=5)
    th = np.linspace(np.deg2rad(-38), np.deg2rad(56), 60)
    ax.plot(centers[1] + 0.95 * np.cos(th), cy + 0.95 * np.sin(th),
            color=fs.GOLD, lw=1.2, zorder=6)
    ax.annotate("", xy=(centers[1] + 0.95 * np.cos(th[-1]), cy + 0.95 * np.sin(th[-1])),
                xytext=(centers[1] + 0.95 * np.cos(th[-6]), cy + 0.95 * np.sin(th[-6])),
                arrowprops=dict(arrowstyle="-|>", color=fs.GOLD, lw=1.2,
                                shrinkA=0, shrinkB=0), zorder=7)
    fs.label(ax, centers[1], 1.50, "松开一根，单点推着转", fs=8.8, color=fs.INK)
    fs.label(ax, centers[1], 1.12, "接触点 1 个", fs=8.4, color=fs.ACCENT)

    # (c) 重新合上
    ax.text(centers[2] - 1.06, 4.56, "(c)", ha="left", va="center", fontsize=9.4,
            color=fs.MUTED, weight="bold")
    _rod(ax, centers[2], cy, 88)
    for s in (-1, 1):
        ax.plot([centers[2] + s * R], [cy], marker="o", ms=4.0, color=fs.ACCENT, zorder=6)
        _finger(ax, centers[2] + s * 0.34, cy)
    fs.label(ax, centers[2], 1.50, "转到角度，重新合上", fs=8.8, color=fs.INK)
    fs.label(ax, centers[2], 1.12, "接触点 2 个", fs=8.4, color=fs.ACCENT)

    # 阶段箭头
    for i in (0, 1):
        fs.arrow(ax, (centers[i] + 1.42, cy), (centers[i + 1] - 1.30, cy),
                 color=fs.FAINT, lw=1.0)

    fs.label(ax, 5.00, 0.52, "中间那一段约 50 到 150 毫秒，只靠一个接触点撑着",
             fs=8.6, color=fs.GOLD)

    fs.save(fig, "ch17", "fig17-03")


if __name__ == "__main__":
    fig_closures()
    fig_tactile()
    fig_inhand()
