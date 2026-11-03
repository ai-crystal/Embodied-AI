# -*- coding: utf-8 -*-
"""第 4 章插图：针孔投影、坐标系链条与手眼、三种深度原理、深度误差曲线。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_pinhole():
    """(a) 侧视投影几何；(b) 像素平面上的 (u, v) 与主点偏移。"""
    fig = plt.figure(figsize=(6.6, 4.15))

    # ---------- (a) 侧视 ----------
    ax = fig.add_axes([0.02, 0.50, 0.96, 0.48])
    ax.set_xlim(0, 10)
    ax.set_ylim(0.55, 4.9)
    ax.axis("off")

    O = (2.3, 2.5)
    P = (8.7, 4.05)
    xi = 4.3
    t = (xi - O[0]) / (P[0] - O[0])
    p = (xi, O[1] + t * (P[1] - O[1]))

    ax.plot([1.55, 9.5], [O[1], O[1]], color=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.plot([xi, xi], [1.95, 4.4], color=fs.INK, lw=1.2, zorder=2)
    ax.plot([O[0], P[0]], [O[1], P[1]], color=fs.MUTED, lw=1.1, zorder=2)
    ax.plot([P[0], P[0]], [O[1], P[1]], color=fs.FAINT, lw=0.8, ls=(0, (3, 3)), zorder=1)

    fs.arrow(ax, (O[0] + 0.06, 2.02), (xi - 0.06, 2.02), color=fs.MUTED, lw=1.0,
             style="<|-|>", ms=7)
    ax.text(3.3, 1.88, "f = 525 px", ha="center", va="top", fontsize=8.2, color=fs.MUTED)

    fs.arrow(ax, (O[0], 1.12), (P[0], 1.12), color=fs.MUTED, lw=1.0, style="<|-|>", ms=7)
    ax.text(5.5, 0.98, "Z = 1.5 m", ha="center", va="top", fontsize=8.2, color=fs.MUTED)

    fs.arrow(ax, (P[0], O[1] + 0.05), (P[0], P[1] - 0.05), color=fs.ACCENT, lw=1.1)
    ax.text(8.88, (O[1] + P[1]) / 2, "X", ha="left", va="center", fontsize=9.4,
            color=fs.ACCENT, weight="bold")

    fs.arrow(ax, (xi, O[1] + 0.05), (xi, p[1] - 0.03), color=fs.ACCENT, lw=1.1)
    ax.text(4.52, 2.66, "x", ha="left", va="center", fontsize=9.4, color=fs.ACCENT,
            weight="bold")

    ax.scatter([O[0]], [O[1]], s=26, color=fs.INK, zorder=6)
    ax.text(2.18, 2.62, "光心 O", ha="right", va="bottom", fontsize=8.6, color=fs.INK)
    ax.scatter([p[0]], [p[1]], s=24, color=fs.ACCENT, zorder=6)
    ax.text(4.15, 3.26, "像点 p", ha="right", va="bottom", fontsize=8.6, color=fs.ACCENT)
    ax.scatter([P[0]], [P[1]], s=24, color=fs.INK, zorder=6)
    ax.text(8.55, 4.18, "物体点 P", ha="right", va="bottom", fontsize=8.6, color=fs.INK)

    ax.text(xi + 0.12, 4.5, "成像平面", ha="center", va="bottom", fontsize=8.4,
            color=fs.MUTED)
    ax.text(0.12, 4.72, "(a)", ha="left", va="top", fontsize=9, color=fs.FAINT)

    # ---------- (b) 像素平面 ----------
    ax2 = fig.add_axes([0.02, 0.02, 0.96, 0.41])
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 3.45)
    ax2.axis("off")

    x0, x1 = 3.8, 7.8
    y0, y1 = 0.3, 3.3
    ax2.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="white",
                                edgecolor=fs.INK, lw=1.1, zorder=2))
    ax2.text(x0 + 0.1, y1 - 0.12, "原点 (0, 0)", ha="left", va="top", fontsize=8.2,
             color=fs.MUTED, zorder=7)
    ax2.text(x1 - 0.1, y0 + 0.1, "(640, 480)", ha="right", va="bottom", fontsize=8.2,
             color=fs.MUTED, zorder=7)

    cxp, cyp = 5.8, 1.8
    ax2.plot([cxp], [cyp], marker="+", ms=11, mew=1.4, color=fs.ACCENT, zorder=5)
    ax2.plot([cxp, 8.05], [cyp, cyp], color=fs.ACCENT, lw=0.8, zorder=4)
    ax2.text(8.22, cyp + 0.02, "主点 (cx, cy)", ha="left", va="center", fontsize=8.4,
             color=fs.ACCENT)

    px = x0 + (540 / 640.0) * (x1 - x0)
    py = y1 - (350 / 480.0) * (y1 - y0)
    ax2.plot([cxp, px], [py, py], color=fs.BLUE, lw=0.9, ls=(0, (3, 2)), zorder=4)
    ax2.plot([px, px], [cyp, py], color=fs.BLUE, lw=0.9, ls=(0, (3, 2)), zorder=4)
    ax2.scatter([px], [py], s=26, color=fs.BLUE, zorder=6)
    ax2.plot([px, 8.05], [py, 0.72], color=fs.BLUE, lw=0.8, zorder=4)
    ax2.text(8.22, 0.7, "像素 (u, v)", ha="left", va="center", fontsize=8.4,
             color=fs.BLUE)

    fs.arrow(ax2, (x0, 0.12), (x1, 0.12), color=fs.MUTED, lw=0.9)
    ax2.text(x1 + 0.12, 0.12, "u", ha="left", va="center", fontsize=8.6, color=fs.MUTED)
    fs.arrow(ax2, (3.46, y1), (3.46, y0), color=fs.MUTED, lw=0.9)
    ax2.text(3.46, 0.08, "v", ha="center", va="top", fontsize=8.6, color=fs.MUTED)
    ax2.text(0.1, 0.1, "(b)", ha="left", va="bottom", fontsize=9, color=fs.FAINT)

    fs.save(fig, "ch04", "fig04-01")


def fig_frames():
    """世界-基座-末端-相机-像素的链条，以及眼在手上与眼在手外。"""
    fig = plt.figure(figsize=(6.6, 4.3))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # ---------- 链条 ----------
    names = ["世界\n坐标系", "基座\n坐标系", "末端\n坐标系", "相机\n坐标系", "像素\n(u, v)"]
    labels = ["T(W→B)", "T(B→E)", "T(E→C)", "K 投影"]
    w, h, gap = 1.6, 1.35, 0.45
    y = 7.95
    x = 0.1
    for i, nm in enumerate(names):
        fc = "#FFFFFF" if i < 4 else fs.LIGHT
        ec = fs.INK if i < 4 else fs.FAINT
        fs.box(ax, x, y, w, h, nm, fc=fc, ec=ec, fs=8.4, lw=1.0)
        if i < 4:
            ax.annotate("", xy=(x + w + gap - 0.04, y + h / 2),
                        xytext=(x + w + 0.04, y + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.1,
                                        mutation_scale=8, shrinkA=0, shrinkB=0))
            ax.text(x + w + gap / 2, y + h + 0.16, labels[i], ha="center", va="bottom",
                    fontsize=8.0, color=fs.ACCENT)
        x += w + gap
    ax.text(0.1, 6.62, "同一点在五个坐标系里的坐标，靠四个变换依次相接",
            ha="left", va="center", fontsize=8.6, color=fs.MUTED)

    # ---------- 两个面板 ----------
    ax.add_patch(plt.Rectangle((0.15, 0.5), 4.65, 5.7, facecolor="#FAFAFA",
                               edgecolor="#E5E7EB", lw=0.9, zorder=0))
    ax.add_patch(plt.Rectangle((5.2, 0.5), 4.65, 5.7, facecolor="#FAFAFA",
                               edgecolor="#E5E7EB", lw=0.9, zorder=0))
    ax.text(2.45, 5.82, "眼在手上", ha="center", va="bottom", fontsize=9.2, color=fs.INK,
            weight="bold")
    ax.text(2.45, 5.42, "相机随末端移动", ha="center", va="bottom", fontsize=8.2,
            color=fs.MUTED)
    ax.text(7.5, 5.82, "眼在手外", ha="center", va="bottom", fontsize=9.2, color=fs.INK,
            weight="bold")
    ax.text(7.5, 5.42, "相机固定在支架上", ha="center", va="bottom", fontsize=8.2,
            color=fs.MUTED)

    # 左：基座 + 两节臂 + 相机
    fs.box(ax, 1.25, 1.15, 1.2, 0.65, "基座", fc="white", ec=fs.MUTED, fs=8.1, lw=0.9)
    for (p0, p1) in [((1.85, 1.8), (2.45, 3.35)), ((2.45, 3.35), (3.45, 4.25))]:
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#C3CCD8", lw=7,
                solid_capstyle="round", zorder=2)
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=fs.MUTED, lw=0.8, zorder=3)
    ax.scatter([3.45], [4.25], s=30, color=fs.MUTED, zorder=5)
    fs.box(ax, 3.05, 4.3, 1.4, 0.62, "相机", fc="#EEF2F7", ec=fs.BLUE, fs=8.0, lw=1.0)
    ax.text(2.45, 0.72, "需要解出 T(E→C)", ha="center", va="center", fontsize=8.2,
            color=fs.ACCENT)

    # 右：基座 + 两节臂，独立支架 + 相机
    fs.box(ax, 5.9, 1.15, 1.2, 0.65, "基座", fc="white", ec=fs.MUTED, fs=8.1, lw=0.9)
    for (p0, p1) in [((6.5, 1.8), (7.05, 3.35)), ((7.05, 3.35), (8.0, 4.2))]:
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#C3CCD8", lw=7,
                solid_capstyle="round", zorder=2)
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=fs.MUTED, lw=0.8, zorder=3)
    ax.scatter([8.0], [4.2], s=30, color=fs.MUTED, zorder=5)
    ax.plot([9.05, 9.05], [1.3, 4.6], color=fs.MUTED, lw=2.2, solid_capstyle="butt",
            zorder=2)
    ax.plot([8.62, 9.48], [1.3, 1.3], color=fs.MUTED, lw=2.2, zorder=2)
    fs.box(ax, 8.2, 4.6, 1.55, 0.6, "相机", fc="#EEF2F7", ec=fs.BLUE, fs=8.0, lw=1.0)
    ax.text(7.5, 0.72, "需要解出 T(W→C)", ha="center", va="center", fontsize=8.2,
            color=fs.ACCENT)

    fs.save(fig, "ch04", "fig04-02")


def fig_depth():
    """三种深度测量原理的对照。"""
    fig = plt.figure(figsize=(6.6, 2.95))
    axes = []
    for left in [0.005, 0.345, 0.685]:
        a = fig.add_axes([left, 0.02, 0.305, 0.96])
        a.set_xlim(0, 10)
        a.set_ylim(0, 10)
        a.axis("off")
        axes.append(a)

    # ---------- (a) 结构光 ----------
    a = axes[0]
    fs.box(a, 0.3, 7.5, 2.9, 1.5, "投影器", fc="#FDF3E7", ec=fs.GOLD, fs=8.0, lw=1.0)
    fs.box(a, 5.9, 7.5, 2.9, 1.5, "相机", fc="#EEF2F7", ec=fs.BLUE, fs=8.0, lw=1.0)
    a.plot([3.25, 5.85], [8.25, 8.25], color=fs.FAINT, lw=0.9, ls=(0, (3, 2)))
    a.text(4.55, 8.4, "基线", ha="center", va="bottom", fontsize=8.0, color=fs.MUTED)
    a.plot([1.75, 4.55], [7.45, 2.75], color=fs.GOLD, lw=1.0, ls=(0, (4, 2)))
    a.plot([7.35, 4.85], [7.45, 2.75], color=fs.MUTED, lw=1.0)
    for (xx, yy) in [(3.55, 4.55), (3.95, 3.85), (4.32, 3.22)]:
        a.scatter([xx], [yy], s=7, color=fs.GOLD, zorder=5)
    a.add_patch(plt.matplotlib.patches.Ellipse((4.7, 2.3), 1.9, 0.85,
                                               facecolor="#E9EDF2", edgecolor=fs.INK,
                                               lw=0.9, zorder=4))
    a.text(5.0, 1.1, "图案位移 → 深度", ha="center", va="center", fontsize=8.0,
           color=fs.INK)
    a.text(0.15, 9.55, "(a) 结构光", ha="left", va="top", fontsize=8.6, color=fs.ACCENT)

    # ---------- (b) ToF ----------
    a = axes[1]
    fs.box(a, 2.6, 7.5, 4.8, 1.5, "发射 + 接收", fc="#EEF7F2", ec=fs.GREEN, fs=8.0, lw=1.0)
    a.annotate("", xy=(3.9, 3.1), xytext=(3.6, 7.45),
               arrowprops=dict(arrowstyle="-|>", color=fs.GREEN, lw=1.1,
                               mutation_scale=8, shrinkA=0, shrinkB=0))
    a.annotate("", xy=(6.2, 7.45), xytext=(5.7, 3.1),
               arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.1,
                               mutation_scale=8, shrinkA=0, shrinkB=0))
    a.text(3.02, 5.4, "出", ha="right", va="center", fontsize=8.2, color=fs.GREEN)
    a.text(6.78, 5.4, "回", ha="left", va="center", fontsize=8.2, color=fs.BLUE)
    a.add_patch(plt.matplotlib.patches.Ellipse((4.9, 2.35), 2.1, 0.9,
                                               facecolor="#E9EDF2", edgecolor=fs.INK,
                                               lw=0.9, zorder=4))
    a.text(5.0, 1.35, "z = c · t / 2", ha="center", va="center", fontsize=8.4,
           color=fs.INK)
    a.text(5.0, 0.62, "1 m 对应 6.7 ns", ha="center", va="center", fontsize=8.0,
           color=fs.MUTED)
    a.text(0.15, 9.55, "(b) 飞行时间", ha="left", va="top", fontsize=8.6, color=fs.ACCENT)

    # ---------- (c) 双目 ----------
    a = axes[2]
    fs.box(a, 0.25, 7.5, 2.8, 1.5, "相机 L", fc="#EEF2F7", ec=fs.BLUE, fs=8.0, lw=1.0)
    fs.box(a, 6.55, 7.5, 2.8, 1.5, "相机 R", fc="#EEF2F7", ec=fs.BLUE, fs=8.0, lw=1.0)
    a.plot([3.15, 6.45], [8.25, 8.25], color=fs.FAINT, lw=0.9, ls=(0, (3, 2)))
    a.plot([3.15, 3.15], [8.15, 8.35], color=fs.FAINT, lw=0.9)
    a.plot([6.45, 6.45], [8.15, 8.35], color=fs.FAINT, lw=0.9)
    a.text(4.8, 8.4, "基线 B", ha="center", va="bottom", fontsize=8.0, color=fs.MUTED)
    a.plot([1.65, 4.62], [7.45, 2.88], color=fs.MUTED, lw=1.0)
    a.plot([7.95, 5.18], [7.45, 2.88], color=fs.MUTED, lw=1.0)
    a.add_patch(plt.matplotlib.patches.Ellipse((4.9, 2.35), 1.9, 0.85,
                                               facecolor="#E9EDF2", edgecolor=fs.INK,
                                               lw=0.9, zorder=4))
    a.text(5.0, 1.35, "z = f · B / d", ha="center", va="center", fontsize=8.4,
           color=fs.INK)
    a.text(5.0, 0.62, "d 是左右像点的视差", ha="center", va="center", fontsize=8.0,
           color=fs.MUTED)
    a.text(0.15, 9.55, "(c) 双目", ha="left", va="top", fontsize=8.6, color=fs.ACCENT)

    fs.save(fig, "ch04", "fig04-03")


def fig_error():
    """双目深度误差随距离的变化，按 sigma_z = z^2 * sigma_d / (f * B) 计算。"""
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    fs.clean(ax, spines=("left", "bottom"))

    f, B = 500.0, 0.05
    z = np.linspace(0.45, 5.0, 600)
    for sd, color, lab, lw in [(0.5, fs.BLUE, r"$\sigma_d$ = 0.5 px", 1.1),
                               (0.2, fs.ACCENT, r"$\sigma_d$ = 0.2 px", 1.6),
                               (0.1, fs.MUTED, r"$\sigma_d$ = 0.1 px", 1.1)]:
        ax.plot(z, z ** 2 / (f * B) * sd * 1000, color=color, lw=lw, label=lab, zorder=3)

    ax.set_yscale("log")
    ax.set_ylim(0.6, 900)
    ax.set_xlim(0.45, 5.0)
    ax.set_xlabel("深度 z / m")
    ax.set_ylabel("深度误差 σz / mm")
    ax.set_yticks([1, 3, 10, 30, 100, 300])
    ax.set_yticklabels(["1", "3", "10", "30", "100", "300"])
    ax.grid(True, which="major", color=fs.GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    for zz, val, txt, dx, dy, ha in [(1.0, 8.0, "8 mm", 0.11, 0.40, "left"),
                                     (3.0, 72.0, "72 mm", 0.14, 1.75, "left")]:
        ax.scatter([zz], [val], s=34, color=fs.ACCENT, zorder=5, edgecolor="white",
                   linewidth=0.9)
        ax.plot([zz, zz], [0.6, val], color=fs.ACCENT, lw=0.7, ls=(0, (2, 2)), zorder=2)
        ax.annotate(txt, xy=(zz, val), xytext=(zz + dx, val * dy), fontsize=9,
                    color=fs.ACCENT, ha=ha, va="center")

    ax.legend(loc="lower right", fontsize=8.4, handlelength=1.6, borderaxespad=0.5,
              labelspacing=0.35)
    ax.text(0.63, 760, "f = 500 px,  B = 5 cm", fontsize=8.6, color=fs.MUTED, va="top")
    ax.text(0.63, 330, "σz = z² σd / (f B)", fontsize=9.0, color=fs.INK, va="top")
    fs.save(fig, "ch04", "fig04-04")


if __name__ == "__main__":
    fig_pinhole()
    fig_frames()
    fig_depth()
    fig_error()
