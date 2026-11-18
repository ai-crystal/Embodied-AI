# -*- coding: utf-8 -*-
"""第 4 章插图：针孔投影、四种深度方案、深度误差随距离变化。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Circle
import figstyle as fs


def fig_pinhole():
    """(a) 侧视的相似三角形；(b) 像平面正视图与内参。"""
    fig = plt.figure(figsize=(6.6, 3.55))
    ax = fig.add_axes([0.015, 0.03, 0.60, 0.93])
    ax.set_xlim(0, 7.0)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    y0 = 1.35          # 光轴高度
    xo, xi, xob = 1.45, 2.50, 6.05
    H = 1.45
    Z = xob - xo
    f = xi - xo
    h = H * f / Z
    top = y0 + H
    htop = y0 + h

    # 光轴
    ax.plot([0.30, 6.80], [y0, y0], color=fs.FAINT, lw=0.9, ls=(0, (5, 3)), zorder=1)

    # 像平面
    ax.plot([xi, xi], [y0 - 0.62, top + 0.22], color=fs.BLUE, lw=1.3, zorder=2)
    fs.label(ax, xi, top + 0.36, "像平面", fs=9.0, color=fs.BLUE)

    # 物体（马克杯轮廓）
    cup = Polygon([[xob - 0.28, y0], [xob - 0.36, top], [xob + 0.36, top],
                   [xob + 0.28, y0]], closed=True, facecolor="#E7E2D9",
                  edgecolor=fs.INK, lw=1.1, zorder=3)
    ax.add_patch(cup)

    # 主光线：物体顶端 -> 光心 -> 像
    ax.plot([xob, xo], [top, y0], color=fs.ACCENT, lw=1.3, zorder=4)
    ax.plot([xi, xi], [y0, htop], color=fs.ACCENT, lw=3.2, solid_capstyle="butt", zorder=5)
    ax.add_patch(Circle((xi, htop), 0.045, facecolor=fs.ACCENT, edgecolor="white",
                        lw=0.8, zorder=6))
    ax.add_patch(Circle((xo, y0), 0.055, facecolor=fs.INK, edgecolor="white", lw=0.8, zorder=6))
    fs.label(ax, xo - 0.02, y0 - 0.24, "光心", fs=8.6, color=fs.INK, ha="center")

    # H 与 h 的标注
    ax.annotate("", xy=(xob + 0.72, top), xytext=(xob + 0.72, y0),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    fs.label(ax, xob + 0.84, (y0 + top) / 2, "H", fs=9.2, color=fs.MUTED, ha="left")
    ax.annotate("", xy=(xi + 0.30, htop), xytext=(xi + 0.30, y0),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=0.9))
    fs.label(ax, xi + 0.38, y0 + h / 2 + 0.05, "h", fs=9.2, color=fs.ACCENT, ha="left")

    # f 与 Z 的尺寸线
    ax.annotate("", xy=(xo, 0.86), xytext=(xi, 0.86),
                arrowprops=dict(arrowstyle="<->", color=fs.BLUE, lw=0.9))
    fs.label(ax, (xo + xi) / 2, 0.62, "f", fs=9.2, color=fs.BLUE)
    ax.annotate("", xy=(xo, 0.30), xytext=(xob, 0.30),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    fs.label(ax, 2.60, 0.30, "Z", fs=9.2, color=fs.MUTED,
             bbox=dict(boxstyle="square,pad=0.06", fc="white", ec="none"))

    fs.label(ax, 4.15, 2.94, "h / H = f / Z", fs=10.2, color=fs.INK)
    fs.label(ax, 4.15, 2.66, "两个相似三角形", fs=8.4, color=fs.MUTED)
    fs.label(ax, 0.30, 3.80, "(a)", fs=9.4, color=fs.MUTED, ha="left")

    # ---------- (b) 像平面正视图 ----------
    ax2 = fig.add_axes([0.655, 0.04, 0.335, 0.92])
    ax2.set_xlim(0, 5.0)
    ax2.set_ylim(0, 4.0)
    ax2.axis("off")

    x0, yb, w, hh = 0.60, 0.82, 3.00, 2.25
    ax2.add_patch(Rectangle((x0, yb), w, hh, facecolor="#F6F7F9", edgecolor=fs.INK, lw=1.1))
    inset = 0.012
    for i in range(1, 8):
        ax2.plot([x0 + w * i / 8] * 2, [yb + inset, yb + hh - inset], color=fs.GRID,
                 lw=0.7, zorder=1, solid_capstyle="butt")
    for j in range(1, 6):
        ax2.plot([x0 + inset, x0 + w - inset], [yb + hh * j / 6] * 2, color=fs.GRID,
                 lw=0.7, zorder=1, solid_capstyle="butt")

    cx, cy = x0 + w * 322 / 640, yb + hh * (1 - 241 / 480)
    ax2.plot([cx - 0.09, cx + 0.09], [cy, cy], color=fs.ACCENT, lw=1.2)
    ax2.plot([cx, cx], [cy - 0.09, cy + 0.09], color=fs.ACCENT, lw=1.2)
    fs.label(ax2, cx + 0.02, cy + 0.19, "主点", fs=8.2, color=fs.ACCENT, ha="center")

    # 一个像素
    ax2.add_patch(Rectangle((1.12, 1.18), 0.115, 0.108, facecolor=fs.ACCENT,
                            edgecolor="none", zorder=4))

    ax2.annotate("", xy=(x0, 3.48), xytext=(cx, 3.48),
                 arrowprops=dict(arrowstyle="<->", color=fs.BLUE, lw=0.9))
    fs.label(ax2, (x0 + cx) / 2, 3.66, "cx = 322", fs=8.8, color=fs.BLUE)
    ax2.annotate("", xy=(3.82, cy), xytext=(3.82, yb + hh),
                 arrowprops=dict(arrowstyle="<->", color=fs.BLUE, lw=0.9))
    fs.label(ax2, 3.96, (cy + yb + hh) / 2 + 0.02, "cy", fs=8.8, color=fs.BLUE, ha="left")

    fs.label(ax2, 0.30, 3.24, "640 × 480 像素", fs=8.4, color=fs.MUTED, ha="left")
    fs.label(ax2, 1.08, 0.52, "1.5 m 处，一个像素 = 2.9 mm", fs=8.4, color=fs.ACCENT, ha="left")
    fs.label(ax2, 4.42, 3.72, "(b)", fs=9.4, color=fs.MUTED, ha="left")

    fs.save(fig, "ch04", "fig04-01")


def fig_depth_kinds():
    """四种深度来源的原理小图。"""
    fig = plt.figure(figsize=(6.6, 4.75))
    gs = fig.add_gridspec(2, 2, left=0.015, right=0.985, top=0.975, bottom=0.03,
                          hspace=0.22, wspace=0.10)

    # ---------- (a) 结构光 ----------
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.add_patch(Rectangle((7.75, 0.85), 0.55, 3.55, facecolor="#EDEAE4",
                           edgecolor=fs.INK, lw=0.9))
    ax.add_patch(Rectangle((7.10, 2.05), 0.65, 1.05, facecolor="#E1DCD2",
                           edgecolor=fs.INK, lw=0.9))
    fs.box(ax, 0.35, 0.95, 1.85, 0.85, "投影仪", fs=8.2, ec=fs.PURPLE, fc="#F3EFFB", tc=fs.PURPLE)
    fs.box(ax, 0.35, 3.05, 1.85, 0.85, "相机", fs=8.2, ec=fs.BLUE, fc="#EEF3FB", tc=fs.BLUE)
    for yv in (1.25, 1.85, 2.45, 3.05):
        ax.plot([7.72], [yv], marker="o", ms=2.6, color=fs.PURPLE, zorder=5)
    for yv in (2.25, 2.55, 2.85):
        ax.plot([7.07], [yv], marker="o", ms=2.6, color=fs.PURPLE, zorder=5)
    fs.arrow(ax, (2.28, 1.38), (7.00, 2.55), color=fs.PURPLE, lw=0.9, ms=7)
    fs.arrow(ax, (7.02, 2.62), (2.28, 3.48), color=fs.BLUE, lw=0.9, ms=7)
    ax.annotate("", xy=(0.28, 1.80), xytext=(0.28, 3.05),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8))
    fs.label(ax, 0.20, 2.42, "B", fs=8.4, color=fs.MUTED, ha="right")
    fs.label(ax, 8.55, 4.70, "图案被物体推歪", fs=8.0, color=fs.MUTED, ha="right")
    fs.label(ax, 0.30, 4.72, "(a) 结构光", fs=9.6, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 5.00, 0.45, "白墙与强阳光下图案糊掉", fs=8.0, color=fs.ACCENT)

    # ---------- (b) ToF ----------
    ax = fig.add_subplot(gs[0, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.add_patch(Rectangle((7.95, 0.85), 0.45, 3.55, facecolor="#EDEAE4",
                           edgecolor=fs.INK, lw=0.9))
    fs.box(ax, 0.35, 1.85, 1.95, 1.15, "ToF 传感器", fs=8.0, ec=fs.GREEN, fc="#EAF6F1", tc=fs.GREEN)
    xo = np.linspace(2.40, 7.90, 300)
    ax.plot(xo, 3.75 + 0.26 * np.sin((xo - 2.40) * 2.4), color=fs.GREEN, lw=1.1)
    ax.plot(xo, 2.25 + 0.26 * np.sin((xo - 2.40) * 2.4 - 2.0), color=fs.GOLD, lw=1.1)
    fs.label(ax, 2.48, 4.20, "发出", fs=8.0, color=fs.GREEN, ha="left")
    fs.label(ax, 3.92, 1.40, "反射回来，晚了一点", fs=8.0, color=fs.GOLD, ha="center")
    xg = 2.40 + (np.pi / 2) / 2.4 + 2 * np.pi / 2.4
    xo_peak = xg + 2.0 / 2.4
    ax.plot([xg, xg], [1.62, 4.01], color=fs.FAINT, lw=0.7, ls=(0, (3, 2)))
    ax.plot([xo_peak, xo_peak], [1.62, 2.51], color=fs.FAINT, lw=0.7, ls=(0, (3, 2)))
    ax.annotate("", xy=(xg, 1.68), xytext=(xo_peak, 1.68),
                arrowprops=dict(arrowstyle="<->", color=fs.GOLD, lw=1.0))
    fs.label(ax, (xg + xo_peak) / 2, 1.40, "Δφ", fs=8.6, color=fs.GOLD)
    fs.label(ax, 0.30, 4.72, "(b) 飞行时间", fs=9.6, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 5.00, 0.45, "深色吸光、阳光与多机互扰", fs=8.0, color=fs.ACCENT)

    # ---------- (c) 双目 ----------
    ax = fig.add_subplot(gs[1, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    fs.box(ax, 0.35, 3.55, 1.55, 0.80, "左相机", fs=8.0, ec=fs.BLUE, fc="#EEF3FB", tc=fs.BLUE)
    fs.box(ax, 2.55, 3.55, 1.55, 0.80, "右相机", fs=8.0, ec=fs.TEAL, fc="#E8F4F2", tc=fs.TEAL)
    ax.annotate("", xy=(0.35, 3.28), xytext=(4.10, 3.28),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.8))
    fs.label(ax, 2.22, 3.10, "B", fs=8.4, color=fs.MUTED)
    ax.add_patch(Circle((8.30, 2.55), 0.14, facecolor=fs.ACCENT, edgecolor="white", lw=0.8, zorder=5))
    fs.arrow(ax, (1.15, 3.52), (8.20, 2.62), color=fs.BLUE, lw=0.85, ms=6)
    fs.arrow(ax, (3.35, 3.52), (8.20, 2.62), color=fs.TEAL, lw=0.85, ms=6)
    ax.add_patch(Rectangle((0.35, 1.75), 4.10, 0.62, facecolor="#F6F7F9",
                           edgecolor=fs.INK, lw=0.8))
    ax.add_patch(Rectangle((0.35, 0.85), 4.10, 0.62, facecolor="#F6F7F9",
                           edgecolor=fs.INK, lw=0.8))
    ax.plot([2.85, 2.85], [1.78, 2.34], color=fs.BLUE, lw=2.2, solid_capstyle="butt")
    ax.plot([3.65, 3.65], [0.88, 1.44], color=fs.TEAL, lw=2.2, solid_capstyle="butt")
    ax.annotate("", xy=(2.85, 1.62), xytext=(3.65, 1.62),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=0.9))
    fs.label(ax, 2.72, 1.62, "视差", fs=8.0, color=fs.ACCENT, ha="right")
    fs.label(ax, 0.42, 2.06, "左图", fs=8.0, color=fs.BLUE, ha="left")
    fs.label(ax, 0.42, 1.16, "右图", fs=8.0, color=fs.TEAL, ha="left")
    fs.label(ax, 8.30, 2.16, "物点", fs=8.0, color=fs.ACCENT)
    fs.label(ax, 0.30, 4.72, "(c) 双目三角", fs=9.6, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 5.00, 0.45, "无纹理白墙、重复花纹", fs=8.0, color=fs.ACCENT)

    # ---------- (d) 单目估计 ----------
    ax = fig.add_subplot(gs[1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.add_patch(Rectangle((0.35, 1.60), 2.35, 2.05, facecolor="#F6F7F9",
                           edgecolor=fs.INK, lw=0.9))
    ax.plot([0.35, 2.70], [2.20, 2.20], color=fs.MUTED, lw=0.9)
    ax.add_patch(Polygon([[1.35, 2.20], [1.55, 2.95], [1.90, 2.95], [2.10, 2.20]],
                         closed=True, facecolor="#E1DCD2", edgecolor=fs.INK, lw=0.8))
    fs.label(ax, 1.52, 1.35, "一张图", fs=8.2, color=fs.MUTED)
    fs.arrow(ax, (2.80, 2.62), (3.55, 2.62), color=fs.FAINT, lw=1.0, ms=7)
    fs.box(ax, 3.62, 2.10, 1.95, 1.05, "深度网络", fs=8.0, ec=fs.PURPLE, fc="#F3EFFB", tc=fs.PURPLE)
    fs.arrow(ax, (5.65, 2.62), (6.40, 2.62), color=fs.FAINT, lw=1.0, ms=7)
    ax.add_patch(Rectangle((6.48, 1.60), 2.30, 2.05, facecolor="#FDF6EC",
                           edgecolor=fs.INK, lw=0.9))
    for i in range(9):
        g = 0.20 + 0.085 * i
        ax.add_patch(Rectangle((6.48 + 2.30 * i / 9, 1.60), 2.30 / 9, 2.05,
                               facecolor=plt.cm.YlOrBr_r(g), edgecolor="none", alpha=0.85))
    fs.label(ax, 7.63, 1.35, "深度图", fs=8.2, color=fs.MUTED)
    fs.label(ax, 8.80, 3.95, "只给出相对远近", fs=8.0, color=fs.MUTED, ha="right")
    fs.label(ax, 0.30, 4.72, "(d) 单目估计", fs=9.6, color=fs.INK, ha="left", weight="bold")
    fs.label(ax, 5.00, 0.45, "尺度不确定，透明与反光只能猜", fs=8.0, color=fs.ACCENT)

    fs.save(fig, "ch04", "fig04-02")


def fig_depth_error():
    """按 σz = z²σd/(fB) 计算的深度误差曲线。"""
    f, B = 500.0, 0.05
    z = np.linspace(0.3, 5.0, 400)

    fig, ax = fs.new(6.6, 3.6)
    fig.subplots_adjust(left=0.085, right=0.975, top=0.93, bottom=0.155)
    fs.clean(ax, grid=True)

    for sd, color, ls, lab in ((0.2, fs.BLUE, "-", "σd = 0.2 像素"),
                               (0.5, fs.FAINT, (0, (4, 2.5)), "σd = 0.5 像素")):
        sz = z ** 2 * sd / (f * B) * 1000.0
        ax.plot(z, sz, color=color, lw=1.8, ls=ls, zorder=3, label=lab)

    # 参考线：平行夹爪能容忍的偏差量级
    ax.axhline(5.0, color=fs.ACCENT, lw=0.9, ls=(0, (1.5, 2.0)), zorder=2)
    ax.text(4.95, 7.4, "5 mm 参考线", ha="right", va="bottom", fontsize=8.2, color=fs.ACCENT)

    for zz in (1.00, 3.00):
        val = zz ** 2 * 0.2 / (f * B) * 1000.0
        ax.plot([zz], [val], marker="o", ms=5.4, color=fs.ACCENT,
                markeredgecolor="white", markeredgewidth=1.0, zorder=5)

    ax.set_xlim(0.3, 5.0)
    ax.set_ylim(0, 130)
    ax.set_xlabel("距离 z（m）")
    ax.set_ylabel("深度误差 σz（mm）")

    ax.legend(loc="upper left", bbox_to_anchor=(0.015, 0.985), fontsize=8.6,
              handlelength=2.0, labelspacing=0.35)
    ax.text(0.985, 0.395, "按 σz = z²σd / (fB) 计算\nf = 500 像素，B = 5 cm\n"
            "圆点为 1 m 的 8 mm 与 3 m 的 72 mm",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.2, color=fs.MUTED,
            linespacing=1.9)
    fs.save(fig, "ch04", "fig04-03")


if __name__ == "__main__":
    fig_pinhole()
    fig_depth_kinds()
    fig_depth_error()
