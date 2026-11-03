# -*- coding: utf-8 -*-
"""第 5 章插图：ADD 与 ADD-S、三种抓取表示、位姿到抓取的管线。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs
from matplotlib.patches import Polygon, Circle, Rectangle, FancyBboxPatch, Arc


# ---------------------------------------------------------------- 工具

def rot2(deg):
    a = np.radians(deg)
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s], [s, c]])


def add_metric(P, Q):
    """ADD：同序号配对后的平均距离。"""
    return float(np.linalg.norm(P - Q, axis=1).mean())


def adds_metric(P, Q):
    """ADD-S：每个点到对方点集最近点的平均距离。"""
    D = np.linalg.norm(P[:, None, :] - Q[None, :, :], axis=2)
    return float(D.min(axis=1).mean())


def ellipse_pts(cx, cy, rx, ry, n=80):
    t = np.linspace(0, 2 * np.pi, n)
    return np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], axis=1)


def draw_poly(ax, P, color, ls="-", lw=1.2, alpha=1.0, z=3):
    pts = np.vstack([P, P[:1]])
    ax.plot(pts[:, 0], pts[:, 1], color=color, ls=ls, lw=lw, alpha=alpha, zorder=z)


def draw_pts(ax, P, color, filled=True, tag_off=0.0, fs_tag=8.0, z=6):
    """画点；tag_off 不为 0 时把序号标在向外（正）或向心（负）的方向。"""
    c = P.mean(axis=0)
    for i, p in enumerate(P):
        if filled:
            ax.scatter([p[0]], [p[1]], s=26, facecolor=color, edgecolor="white",
                       linewidth=0.7, zorder=z)
        else:
            ax.scatter([p[0]], [p[1]], s=30, facecolor="white", edgecolor=color,
                       linewidth=1.1, zorder=z)
        if abs(tag_off) > 1e-9:
            u = p - c
            n = np.linalg.norm(u)
            u = u / n if n > 1e-6 else np.array([0.0, 1.0])
            q = p + u * tag_off
            ax.text(q[0], q[1], str(i + 1), fontsize=fs_tag, color=color,
                    ha="center", va="center", zorder=z + 1)


# ---------------------------------------------------------------- 图 5-1

def fig_add():
    """ADD 与 ADD-S：非对称工件与对称方盒上的同一种旋转误差。"""
    # 左：L 形工件，8 个点（6 个角 + 2 个边中点），单位 cm
    L = np.array([[0, 0], [2, 0], [4, 0], [4, 1.6],
                  [1.6, 1.6], [1.6, 5], [0, 5], [0, 2.5]], float)
    cL = L.mean(axis=0)
    PL = (rot2(10) @ (L - cL).T).T + cL + np.array([0.08, 0.05])
    # 右：8×5 的方盒，绕对称轴差 178°
    R = np.array([[0, 0], [4, 0], [8, 0], [8, 2.5],
                  [8, 5], [4, 5], [0, 5], [0, 2.5]], float)
    cR = R.mean(axis=0)
    PR = (rot2(178) @ (R - cR).T).T + cR + np.array([0.06, -0.04])

    dL = float(np.linalg.norm(L.max(0) - L.min(0)))
    dR = float(np.linalg.norm(R.max(0) - R.min(0)))
    addL, addsL = add_metric(L, PL), adds_metric(L, PL)
    addR, addsR = add_metric(R, PR), adds_metric(R, PR)
    print("L   ADD %.2f  ADD-S %.2f  diam %.2f thr %.2f" % (addL, addsL, dL, 0.1 * dL))
    print("R   ADD %.2f  ADD-S %.2f  diam %.2f thr %.2f" % (addR, addsR, dR, 0.1 * dR))

    fig, axes = plt.subplots(1, 2, figsize=(6.7, 3.5),
                             gridspec_kw=dict(width_ratios=[1.0, 1.24], wspace=0.06))

    # ---------------- (a) 非对称
    ax = axes[0]
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.6, 5.4); ax.set_ylim(-2.9, 7.2)
    draw_poly(ax, L, fs.INK, "-", 1.3)
    draw_poly(ax, PL, fs.BLUE, "--", 1.1)
    for i in range(len(L)):
        ax.plot([L[i, 0], PL[i, 0]], [L[i, 1], PL[i, 1]], color=fs.FAINT,
                lw=0.7, alpha=0.9, zorder=2)
    draw_pts(ax, L, fs.INK, True)
    draw_pts(ax, PL, fs.BLUE, False)

    ax.text(0.02, 0.98, "(a) 非对称工件，转 10°", transform=ax.transAxes,
            fontsize=9.0, color=fs.INK, ha="left", va="top")
    # 图例
    ax.scatter([0.55], [-1.05], s=26, facecolor=fs.INK, edgecolor="white", lw=0.7, zorder=6)
    ax.text(0.85, -1.05, "真值位姿", fontsize=8.2, color=fs.INK, va="center")
    ax.scatter([3.05], [-1.05], s=30, facecolor="white", edgecolor=fs.BLUE, lw=1.1, zorder=6)
    ax.text(3.35, -1.05, "预测位姿", fontsize=8.2, color=fs.BLUE, va="center")
    ax.text(2.0, -2.05, "ADD %.2f cm，阈值 %.2f cm，判对" % (addL, 0.1 * dL),
            fontsize=8.3, color=fs.GREEN, ha="center", va="center")
    ax.text(2.0, -2.68, "ADD-S 与 ADD 几乎相同", fontsize=8.0, color=fs.MUTED,
            ha="center", va="center")

    # ---------------- (b) 对称
    ax = axes[1]
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.9, 10.3); ax.set_ylim(-2.9, 7.2)
    draw_poly(ax, R, fs.INK, "-", 1.3)
    draw_poly(ax, PR, fs.BLUE, "--", 1.1)
    for i in (0, 2, 6):
        axplot_i = i
        ax.plot([R[axplot_i, 0], PR[axplot_i, 0]], [R[axplot_i, 1], PR[axplot_i, 1]],
                color=fs.FAINT, lw=0.8, ls=(0, (2, 2)), zorder=2)
    # ADD-S 的最近点配对，用绿色粗线示例两条
    for i in (0, 4):
        D = np.linalg.norm(PR - R[i], axis=1)
        j = int(D.argmin())
        ax.plot([R[i, 0], PR[j, 0]], [R[i, 1], PR[j, 1]], color=fs.GREEN,
                lw=2.6, zorder=8, solid_capstyle="round")
    draw_pts(ax, R, fs.INK, True, tag_off=0.48)
    draw_pts(ax, PR, fs.BLUE, False)

    ax.text(0.02, 0.98, "(b) 对称方盒，绕轴差 2°", transform=ax.transAxes,
            fontsize=9.0, color=fs.INK, ha="left", va="top")
    ax.text(4.2, -1.05, "灰虚线为同序号点的配对，绿线为 ADD-S 的最近点配对",
            fontsize=8.0, color=fs.MUTED, ha="center", va="center")
    ax.text(4.2, -1.95, "ADD %.2f cm，阈值 %.2f cm，判错" % (addR, 0.1 * dR),
            fontsize=8.3, color=fs.ACCENT, ha="center", va="center")
    ax.text(4.2, -2.6, "ADD-S %.2f cm，判对" % addsR,
            fontsize=8.3, color=fs.GREEN, ha="center", va="center")

    fs.save(fig, "ch05", "fig05-01")


# ---------------------------------------------------------------- 图 5-2

def fig_grasp_repr():
    """三种抓取表示：(a) 2D 矩形 (b) 6-DoF 平行夹爪 (c) 多指抓取。"""
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 3.05),
                             gridspec_kw=dict(wspace=0.06))
    for ax in axes:
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(0, 10); ax.set_ylim(-2.2, 8.6)

    # ---------------- (a) 2D 抓取矩形
    ax = axes[0]
    ax.add_patch(Rectangle((0.35, 1.0), 9.3, 6.3, facecolor="#FCFCFD",
                           edgecolor=fs.GRID, lw=1.0, zorder=1))
    cx, cy, th, w, h = 4.7, 3.9, 24.0, 3.5, 1.3
    ax.add_patch(Polygon(ellipse_pts(cx, cy, 2.2, 1.5), closed=True,
                         facecolor=fs.LIGHT, edgecolor=fs.MUTED, lw=1.0, zorder=3))
    Rt = rot2(th)
    corners = np.array([[-w / 2, -h / 2], [w / 2, -h / 2],
                        [w / 2, h / 2], [-w / 2, h / 2]])
    ax.add_patch(Polygon((Rt @ corners.T).T + np.array([cx, cy]), closed=True,
                         facecolor="none", edgecolor=fs.ACCENT, lw=1.2, zorder=5))
    for sgn in (-1, 1):
        a = Rt @ np.array([sgn * w / 2, -h / 2]) + np.array([cx, cy])
        b = Rt @ np.array([sgn * w / 2, h / 2]) + np.array([cx, cy])
        ax.plot([a[0], b[0]], [a[1], b[1]], color=fs.ACCENT, lw=2.4,
                solid_capstyle="round", zorder=6)
    ax.scatter([cx], [cy], s=15, color=fs.INK, zorder=8)
    # 开度箭头画在矩形外，靠上
    base = np.array([cx, cy]) + Rt @ np.array([0, h / 2 + 0.78])
    p0 = base + Rt @ np.array([-w / 2, 0])
    p1 = base + Rt @ np.array([w / 2, 0])
    fs.arrow(ax, tuple(p0), tuple(p1), color=fs.BLUE, lw=1.0, style="<|-|>", ms=7, z=7)
    mid = (p0 + p1) / 2 + Rt @ np.array([0, 0.42])
    ax.text(mid[0], mid[1], "w", fontsize=8.6, color=fs.BLUE, ha="center", va="center")
    # 角度弧
    ax.plot([cx, cx + 3.1], [cy, cy], color=fs.FAINT, lw=0.8, ls=(0, (3, 2)), zorder=7)
    ax.add_patch(Arc((cx, cy), 5.2, 5.2, theta1=0, theta2=th, color=fs.GREEN, lw=1.1,
                     zorder=7))
    ax.text(cx + 3.15 * np.cos(np.radians(12)), cy + 3.15 * np.sin(np.radians(12)),
            "θ", fontsize=8.6, color=fs.GREEN, ha="left", va="center", zorder=7)
    ax.text(5.0, 7.95, "(a) 2D 抓取矩形", fontsize=9.0, color=fs.INK, ha="center")
    ax.text(5.0, 0.35, "(x, y, θ, w, q)", fontsize=8.3, color=fs.MUTED, ha="center")
    ax.text(5.0, -1.1, "默认从正上方垂直下抓", fontsize=8.0, color=fs.MUTED,
            ha="center", va="center")

    # ---------------- (b) 6-DoF 平行夹爪
    ax = axes[1]
    ax.add_patch(Rectangle((3.3, 1.3), 3.4, 3.1, facecolor=fs.LIGHT,
                           edgecolor=fs.MUTED, lw=1.0, zorder=3))
    ax.add_patch(FancyBboxPatch((2.85, 4.70), 4.3, 0.64,
                                boxstyle="round,pad=0.01,rounding_size=0.06",
                                facecolor="#E8EDF5", edgecolor=fs.INK, lw=1.0, zorder=4))
    ax.text(5.0, 5.02, "手掌", fontsize=8.1, color=fs.INK, ha="center", va="center",
            zorder=6)
    for x0 in (2.95, 6.6):
        ax.add_patch(Rectangle((x0, 1.45), 0.45, 3.25, facecolor="#E8EDF5",
                               edgecolor=fs.INK, lw=1.0, zorder=4))
    for p in ([3.4, 2.85], [6.6, 2.85]):
        ax.scatter([p[0]], [p[1]], s=34, color=fs.ACCENT, zorder=7,
                   edgecolor="white", linewidth=0.8)
    fs.arrow(ax, (5.0, 7.55), (5.0, 5.45), color=fs.PURPLE, lw=1.3, ms=9)
    ax.text(5.22, 6.7, "接近方向 a", fontsize=8.1, color=fs.PURPLE,
            ha="left", va="center")
    fs.arrow(ax, (3.55, 1.02), (6.45, 1.02), color=fs.BLUE, lw=1.0,
             style="<|-|>", ms=7)
    ax.text(5.0, 0.45, "基线方向 b", fontsize=8.1, color=fs.BLUE, ha="center",
            va="center")
    ax.text(5.0, 7.95, "(b) 6-DoF 平行夹爪", fontsize=9.0, color=fs.INK, ha="center")
    ax.text(5.0, -1.1, "位姿 6 个自由度，实际存 7 个数", fontsize=8.0,
            color=fs.MUTED, ha="center", va="center")

    # ---------------- (c) 多指抓取
    ax = axes[2]
    ax.add_patch(Circle((4.0, 3.3), 1.5, facecolor=fs.LIGHT, edgecolor=fs.MUTED,
                        lw=1.0, zorder=3))
    ax.text(4.0, 3.3, "物体", fontsize=8.1, color=fs.MUTED, ha="center", va="center")
    ax.add_patch(FancyBboxPatch((2.62, 6.15), 3.45, 0.75,
                                boxstyle="round,pad=0.01,rounding_size=0.08",
                                facecolor="#E8EDF5", edgecolor=fs.INK, lw=1.0, zorder=5))
    ax.text(4.34, 6.53, "手掌", fontsize=8.1, color=fs.INK, ha="center", va="center")
    roots = [(3.2, 6.15), (4.2, 6.15), (5.2, 6.15)]
    contacts = []
    for ang in (128, 95, 62):
        a = np.radians(ang)
        contacts.append((4.0 + 1.5 * np.cos(a), 3.3 + 1.5 * np.sin(a)))
    for r, ct in zip(roots, contacts):
        fs.limb(ax, r, ct, 0.40, 0.28, color="#CBD5E1", z=4)
        ax.scatter([ct[0]], [ct[1]], s=34, color=fs.ACCENT, zorder=8,
                   edgecolor="white", linewidth=0.8)
    ax.annotate("三个接触点", xy=(contacts[2][0] + 0.04, contacts[2][1] - 0.10),
                xytext=(5.95, 3.95), fontsize=8.1, color=fs.ACCENT, ha="left",
                va="center",
                arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.8,
                                shrinkA=2, shrinkB=4))
    ax.text(5.0, 7.95, "(c) 多指抓取", fontsize=9.0, color=fs.INK, ha="center")
    ax.text(5.0, -1.1, "手腕位姿 + 每根手指的关节角", fontsize=8.0, color=fs.MUTED,
            ha="center", va="center")

    fs.save(fig, "ch05", "fig05-02")


# ---------------------------------------------------------------- 图 5-3

def fig_pipeline():
    """从 RGB-D 到执行的管线，虚线是失败分支。"""
    fig, ax = fs.canvas(6.7, 2.9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    labels = ["RGB-D\n输入", "实例 / 提示\n分割", "6D 位姿\n估计",
              "抓取候选\n生成", "碰撞与\n可达性筛选", "执行\n与监测"]
    w, h, y, pitch, x0 = 0.132, 0.20, 0.60, 0.164, 0.016
    centers = []
    for i, lab in enumerate(labels):
        x = x0 + i * pitch
        ec = fs.ACCENT if i in (2, 4) else fs.INK
        fs.box(ax, x, y, w, h, lab, fc="white", ec=ec, fs=8.2, lw=1.1)
        centers.append(x + w / 2)
        if i:
            fs.arrow(ax, (x - 0.028, y + h / 2), (x - 0.004, y + h / 2),
                     color=fs.MUTED, lw=1.0, ms=7)

    fails = {
        1: "掩码粘连\n位姿被拉偏",
        2: "深度缺失\n对称等价解",
        4: "全部候选\n被否决",
    }
    for i, txt in fails.items():
        cx = centers[i]
        fs.arrow(ax, (cx, y - 0.006), (cx, 0.42), color=fs.ACCENT, lw=0.9,
                 ls=(0, (3, 2)), ms=7)
        ax.text(cx, 0.345, txt, fontsize=8.0, color=fs.ACCENT, ha="center",
                va="center", linespacing=1.5)

    ax.text(0.5, 0.13, "虚线是失败分支，需要回退、重试或重新采样抓取", fontsize=8.3,
            color=fs.MUTED, ha="center")

    fs.save(fig, "ch05", "fig05-03")


if __name__ == "__main__":
    fig_add()
    fig_grasp_repr()
    fig_pipeline()
