# -*- coding: utf-8 -*-
"""第 16 章插图：ZMP 与支撑多边形、LIPM 倒立摆、步态相位与训练环。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle
from scipy.spatial import ConvexHull
import figstyle as fs


# ---------- 图 16-1 ----------
def fig_zmp():
    """(a) 侧视：质心投影跑出脚外，ZMP 仍在脚底；(b) 俯视：支撑多边形随落脚切换。"""
    fig = plt.figure(figsize=(6.6, 3.75))
    axL = fig.add_axes([0.015, 0.03, 0.455, 0.92])
    axR = fig.add_axes([0.515, 0.03, 0.455, 0.92])
    for ax in (axL, axR):
        ax.axis("off")

    # ---------- (a) 侧视 ----------
    ax = axL
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.add_patch(Rectangle((0.25, 0.85), 9.5, 0.45, facecolor=fs.LIGHT, edgecolor="none", zorder=1))
    ax.plot([0.25, 9.75], [1.30, 1.30], color=fs.FAINT, lw=1.2, zorder=2)

    # 支撑脚
    ax.add_patch(Rectangle((2.55, 1.30), 1.85, 0.30, facecolor="#FFFFFF",
                           edgecolor=fs.INK, lw=1.3, zorder=4))
    ax.plot([2.62, 4.33], [1.36, 1.36], color=fs.ACCENT, lw=3.4,
            solid_capstyle="butt", zorder=6)
    # 摆动脚
    ax.add_patch(Rectangle((5.55, 2.30), 1.85, 0.30, facecolor="#FFFFFF",
                           edgecolor=fs.FAINT, lw=1.2, ls=(0, (3, 2)), zorder=4))

    # 支撑腿
    fs.limb(ax, (4.38, 4.72), (3.98, 3.06), 0.32, 0.25, color=fs.INK, z=5)
    fs.limb(ax, (3.98, 3.06), (3.22, 1.64), 0.25, 0.16, color=fs.INK, z=5)
    # 摆动腿
    fs.limb(ax, (4.80, 4.72), (5.78, 3.42), 0.32, 0.25, color=fs.MUTED, z=5)
    fs.limb(ax, (5.78, 3.42), (6.40, 2.62), 0.25, 0.16, color=fs.MUTED, z=5)

    # 躯干与头
    ax.add_patch(Polygon([(4.22, 4.68), (4.12, 5.42), (4.18, 6.02), (5.02, 6.02),
                          (5.08, 5.42), (4.98, 4.68)], closed=True,
                         facecolor=fs.INK, edgecolor="none", zorder=5))
    ax.add_patch(Ellipse((4.60, 6.42), 0.62, 0.70, facecolor=fs.INK, edgecolor="none", zorder=5))

    # 质心
    ax.add_patch(Circle((4.60, 4.95), 0.14, facecolor=fs.BLUE, edgecolor="white", lw=1.2, zorder=8))
    ax.plot([4.60, 4.60], [4.85, 1.42], color=fs.BLUE, lw=1.0, ls=(0, (4, 3)), zorder=3)
    ax.plot([4.52, 4.68], [1.32, 1.48], color=fs.BLUE, lw=1.1, zorder=6)
    ax.plot([4.68, 4.52], [1.32, 1.48], color=fs.BLUE, lw=1.1, zorder=6)

    # ZMP
    ax.add_patch(Circle((4.24, 1.30), 0.15, facecolor=fs.ACCENT, edgecolor="white",
                        lw=1.1, zorder=9))
    ax.plot([4.24, 4.24], [1.16, 0.74], color=fs.ACCENT, lw=0.9, ls=(0, (2, 2)), zorder=3)

    fs.label(ax, 2.30, 0.52, "接触面", fs=8.4, color=fs.ACCENT, ha="left")
    fs.label(ax, 4.24, 0.52, "ZMP", fs=8.6, color=fs.ACCENT, weight="bold")
    ax.plot([4.62, 5.02], [1.30, 0.76], color=fs.FAINT, lw=0.9, zorder=3)
    fs.label(ax, 5.08, 0.52, "质心投影", fs=8.4, color=fs.BLUE, ha="left")

    # 图例
    ax.add_patch(Circle((7.10, 4.35), 0.14, facecolor=fs.BLUE, edgecolor="white", lw=1.0, zorder=8))
    fs.label(ax, 7.35, 4.35, "质心", fs=8.8, ha="left")
    ax.add_patch(Circle((7.10, 3.75), 0.15, facecolor=fs.ACCENT, edgecolor="white", lw=1.0, zorder=8))
    fs.label(ax, 7.35, 3.75, "ZMP", fs=8.8, ha="left")

    fs.label(ax, 0.30, 9.55, "（a）侧视", fs=8.8, ha="left", color=fs.MUTED)
    fs.label(ax, 0.30, 8.95, "质心投影越过脚尖", fs=8.7, ha="left")
    fs.label(ax, 0.30, 8.45, "ZMP 还留在脚底", fs=8.7, ha="left")

    # ---------- (b) 俯视 ----------
    ax = axR
    ax.set_xlim(0, 8)
    ax.set_ylim(0.2, 9.6)

    feet = [("左脚", (1.75, 1.40)), ("右脚", (4.10, 3.50))]
    corners = []
    for _, (x0, y0) in feet:
        for dx in (0.0, 1.35):
            for dy in (0.0, 2.40):
                corners.append((x0 + dx, y0 + dy))
    corners = np.array(corners)
    hull = ConvexHull(corners)
    hp = corners[hull.vertices]
    ax.add_patch(Polygon(hp, closed=True, facecolor=fs.LIGHT, edgecolor=fs.MUTED,
                         lw=1.1, ls=(0, (5, 3)), alpha=0.95, zorder=2))

    for name, (x0, y0) in feet:
        ax.add_patch(Rectangle((x0, y0), 1.35, 2.40, facecolor="#FFFFFF",
                               edgecolor=fs.INK, lw=1.3, zorder=4))

    # 下一步的落脚位置
    ax.add_patch(Rectangle((1.75, 6.10), 1.35, 2.40, facecolor="none",
                           edgecolor=fs.FAINT, lw=1.1, ls=(0, (3, 3)), zorder=4))

    # ZMP 轨迹
    ax.plot([2.42, 2.42], [1.66, 3.55], color=fs.ACCENT, lw=1.9, solid_capstyle="round", zorder=7)
    ax.plot([4.77, 4.77], [3.95, 5.65], color=fs.ACCENT, lw=1.9, solid_capstyle="round", zorder=7)
    ax.annotate("", xy=(4.70, 3.92), xytext=(2.49, 3.60),
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.2,
                                linestyle=(0, (2, 2)), shrinkA=3, shrinkB=3), zorder=7)
    for xx, yy in ((2.42, 1.66), (2.42, 3.55), (4.77, 3.95), (4.77, 5.65)):
        ax.add_patch(Circle((xx, yy), 0.10, facecolor=fs.ACCENT,
                            edgecolor="white", lw=0.8, zorder=8))

    fs.label(ax, 1.60, 2.55, "左脚", fs=8.6, ha="right")
    fs.label(ax, 5.58, 4.75, "右脚", fs=8.6, ha="left")
    fs.label(ax, 3.35, 8.55, "下一步落脚", fs=8.4, color=fs.MUTED, ha="left")
    ax.plot([3.33, 3.14, 3.12], [8.42, 8.05, 7.60], color=fs.FAINT, lw=0.9, zorder=6)

    fs.label(ax, 5.85, 7.45, "支撑多边形", fs=8.5, color=fs.MUTED, ha="left")
    ax.plot([5.82, 5.22], [7.32, 6.08], color=fs.FAINT, lw=0.9, zorder=6)
    ax.add_patch(Circle((0.24, 5.10), 0.10, facecolor=fs.ACCENT, edgecolor="white", lw=0.7, zorder=8))
    fs.label(ax, 0.48, 5.10, "ZMP 轨迹", fs=8.5, color=fs.ACCENT, ha="left")

    fs.label(ax, 0.15, 9.30, "（b）俯视", fs=8.8, ha="left", color=fs.MUTED)

    fs.save(fig, "ch16", "fig16-01")


# ---------- 图 16-2 ----------
def fig_lipm():
    """(a) 倒立摆模型；(b) 位置误差按 cosh 放大（实算）。"""
    fig = plt.figure(figsize=(6.6, 3.55))
    axL = fig.add_axes([0.02, 0.03, 0.42, 0.92])
    axL.set_xlim(0, 8)
    axL.set_ylim(0, 8)
    axL.axis("off")

    # 地面
    axL.add_patch(Rectangle((0.35, 0.72), 7.4, 0.42, facecolor=fs.LIGHT, edgecolor="none", zorder=1))
    axL.plot([0.35, 7.75], [1.14, 1.14], color=fs.FAINT, lw=1.2, zorder=2)

    pivot = np.array([3.30, 1.14])
    mass = np.array([4.55, 5.42])
    axL.plot([pivot[0], mass[0]], [pivot[1], mass[1]], color=fs.MUTED, lw=3.2,
             solid_capstyle="round", zorder=3)
    axL.add_patch(Circle(mass, 0.46, facecolor="#DCE7FB", edgecolor=fs.BLUE, lw=1.4, zorder=5))
    fs.label(axL, mass[0], mass[1], "m", fs=11.0, color=fs.BLUE, weight="bold", z=6)
    axL.add_patch(Circle(pivot, 0.13, facecolor=fs.ACCENT, edgecolor="white", lw=1.0, zorder=6))

    # 竖直投影与 x - p
    axL.plot([mass[0], mass[0]], [4.96, 0.70], color=fs.BLUE, lw=1.0, ls=(0, (4, 3)), zorder=2)
    axL.plot([pivot[0], pivot[0]], [1.00, 0.70], color=fs.FAINT, lw=1.0, ls=(0, (4, 3)), zorder=2)
    axL.annotate("", xy=(pivot[0] + 0.04, 0.86), xytext=(mass[0] - 0.04, 0.86),
                 arrowprops=dict(arrowstyle="<->", color=fs.INK, lw=0.9))
    fs.label(axL, (pivot[0] + mass[0]) / 2, 0.55, "x − p", fs=8.8)

    # 高度
    axL.annotate("", xy=(2.42, 1.18), xytext=(2.42, 5.40),
                 arrowprops=dict(arrowstyle="<->", color=fs.FAINT, lw=0.9))
    fs.label(axL, 2.16, 3.40, "质心高度", fs=8.4, color=fs.MUTED, rotation=90)

    # 重力
    axL.annotate("", xy=(5.24, 4.55), xytext=(5.24, 5.42),
                 arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.2))
    fs.label(axL, 5.38, 5.00, "g", fs=9.0, ha="left", color=fs.MUTED)

    fs.label(axL, 3.02, 1.02, "ZMP", fs=8.6, color=fs.ACCENT, weight="bold", ha="right")
    fs.label(axL, 0.35, 7.55, "（a）把整机压成一个质点", fs=8.8, ha="left", color=fs.MUTED)
    axL.text(0.35, 6.95, r"$\omega=\sqrt{g/z_c}$" + " ≈ 3.5 rad/s", fontsize=10.5, color=fs.INK,
             ha="left", va="center")
    fs.label(axL, 0.35, 6.35, "误差放大 e 倍只要 0.29 s", fs=8.4, ha="left", color=fs.MUTED)

    # ---------- (b) 发散曲线 ----------
    ax = fig.add_axes([0.565, 0.155, 0.405, 0.725])
    t = np.linspace(0, 0.6, 400)
    for zc, col, lab in ((0.6, fs.ACCENT, "$z_c$ = 0.6 m"),
                         (0.8, fs.BLUE, "$z_c$ = 0.8 m"),
                         (1.0, fs.GREEN, "$z_c$ = 1.0 m")):
        w = np.sqrt(9.81 / zc)
        ax.plot(t, np.cosh(w * t), color=col, lw=1.7, label=lab)

    ax.axvline(0.3, color=fs.FAINT, lw=0.9, ls=(0, (3, 3)))
    ax.annotate("0.3 s 已放大 1.6 倍", xy=(0.305, np.cosh(3.502 * 0.305)),
                xytext=(0.345, 1.14), fontsize=8.4, color=fs.BLUE, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=0.9))
    ax.set_xlim(0, 0.6)
    ax.set_ylim(1.0, 5.4)
    ax.set_xlabel("时间（s）", fontsize=9.2)
    ax.set_ylabel("位置误差 / 初始误差", fontsize=9.2)
    ax.set_xticks([0, 0.2, 0.4, 0.6])
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.grid(True, color=fs.GRID, lw=0.7)
    ax.set_axisbelow(True)
    fs.clean(ax)
    ax.legend(loc="upper left", fontsize=8.4, handlelength=1.6, borderpad=0.2)

    fig.text(0.565, 0.945, "（b）同一个 1 cm 的初始误差", fontsize=8.8, color=fs.MUTED,
             ha="left", va="center")

    fs.save(fig, "ch16", "fig16-02")


# ---------- 图 16-3 ----------
def fig_gait_loop():
    """(a) 一个步态周期的支撑相与摆动相；(b) 学习式步态的训练环与部署链。"""
    fig = plt.figure(figsize=(6.6, 5.4))

    # ---------- (a) 步态相位 ----------
    ax = fig.add_axes([0.02, 0.665, 0.96, 0.295])
    ax.set_xlim(0, 10)
    ax.set_ylim(0.45, 3.95)
    ax.axis("off")

    x0, x1 = 1.85, 9.45
    per = x1 - x0                                  # 一个周期 1.0 s

    def T(tt):
        return x0 + tt * per

    def seg(y, a, b, label="", swing=False, color=fs.BLUE, alpha=0.18):
        if swing:
            ax.add_patch(Rectangle((T(a), y), T(b) - T(a), 0.52, facecolor="#FFFFFF",
                                   edgecolor=color, lw=1.1, ls=(0, (4, 3)), zorder=4))
        else:
            ax.add_patch(Rectangle((T(a), y), T(b) - T(a), 0.52, facecolor=color,
                                   edgecolor=color, lw=1.0, alpha=alpha, zorder=3))
        if label:
            fs.label(ax, (T(a) + T(b)) / 2, y + 0.26, label, fs=8.6, color=color, z=6)

    # 双支撑底色
    for a, b in ((0.0, 0.10), (0.50, 0.60)):
        ax.add_patch(Rectangle((T(a), 1.25), T(b) - T(a), 1.62, facecolor=fs.GOLD,
                               edgecolor="none", alpha=0.15, zorder=1))

    seg(2.05, 0.0, 0.60, "支撑 0.6 s")
    seg(2.05, 0.60, 1.00, "摆动 0.4 s", swing=True)
    seg(1.25, 0.00, 0.10, "", color=fs.GREEN)
    seg(1.25, 0.10, 0.50, "摆动 0.4 s", swing=True, color=fs.GREEN)
    seg(1.25, 0.50, 1.00, "支撑 0.5 s", color=fs.GREEN)

    fs.label(ax, x0 - 0.12, 2.31, "左腿", fs=9.0, ha="right")
    fs.label(ax, x0 - 0.12, 1.51, "右腿", fs=9.0, ha="right")

    fs.label(ax, (T(0.0) + T(0.10)) / 2 + 0.15, 3.02, "双支撑 0.1 s", fs=8.2, color=fs.GOLD)
    fs.label(ax, (T(0.50) + T(0.60)) / 2 + 0.15, 3.02, "双支撑 0.1 s", fs=8.2, color=fs.GOLD)

    # MPC 重算刻度
    for k in range(26):
        tt = k * 0.04
        ax.plot([T(tt), T(tt)], [3.30, 3.50], color=fs.ACCENT, lw=1.0, zorder=4)
    ax.plot([T(0.0), T(1.0)], [3.30, 3.30], color=fs.FAINT, lw=0.8, zorder=3)
    fs.label(ax, T(0.0), 3.70, "MPC 每 40 ms 重算一次，一个周期 25 次", fs=8.4,
             color=fs.ACCENT, ha="left")

    # 时间轴
    ax.plot([T(0.0), T(1.0)], [1.02, 1.02], color=fs.FAINT, lw=1.0, zorder=2)
    for tt, lab in ((0.0, "0"), (0.5, "0.5 s"), (1.0, "1.0 s")):
        ax.plot([T(tt), T(tt)], [1.02, 0.92], color=fs.FAINT, lw=0.9, zorder=2)
        fs.label(ax, T(tt), 0.72, lab, fs=8.4, color=fs.MUTED)

    fs.label(ax, 0.02, 3.88, "（a）一个步态周期", fs=8.8, ha="left", color=fs.MUTED)

    # ---------- (b) 训练环 ----------
    axb = fig.add_axes([0.02, 0.01, 0.96, 0.61])
    axb.set_xlim(0, 10.3)
    axb.set_ylim(1.15, 6.62)
    axb.axis("off")

    W, H = 2.65, 1.30
    boxes = [
        (0.25, 4.45, "并行仿真", "4096 个环境同时跑", fs.BLUE),
        (0.25, 2.55, "采样并算奖励", "每轮 32 个控制步", fs.BLUE),
        (3.15, 2.55, "PPO 更新", "策略网络挪一小步", fs.PURPLE),
        (3.15, 4.45, "新策略", "拿去跑下一轮", fs.PURPLE),
    ]
    for x, y, t1, t2, ec in boxes:
        fs.box(axb, x, y, W, H, "", fc="#FFFFFF", ec=ec, lw=1.2)
        fs.label(axb, x + W / 2, y + H - 0.36, t1, fs=9.4, weight="bold", color=ec)
        fs.label(axb, x + W / 2, y + 0.38, t2, fs=8.2, color=fs.MUTED)

    fs.arrow(axb, (1.58, 4.40), (1.58, 3.90), color=fs.MUTED)
    fs.arrow(axb, (2.94, 3.20), (3.11, 3.20), color=fs.MUTED)
    fs.arrow(axb, (4.48, 3.90), (4.48, 4.40), color=fs.MUTED)
    fs.arrow(axb, (3.11, 5.10), (2.94, 5.10), color=fs.MUTED)

    fs.label(axb, 2.95, 1.95, "域随机化：质量、摩擦、控制延迟、传感器噪声", fs=8.3,
             color=fs.ACCENT, ha="center")
    fs.label(axb, 2.95, 1.55, "课程学习：地形由平到陡，推力由小到大", fs=8.3,
             color=fs.ACCENT, ha="center")

    # 训练到部署
    fs.arrow(axb, (5.84, 5.10), (6.53, 5.10), color=fs.ACCENT, lw=1.4)
    fs.label(axb, 6.18, 5.44, "导出", fs=8.2, color=fs.ACCENT)

    dx, dw = 6.55, 3.05
    dep = [(4.45, "策略网络 50 Hz", "读本体感受，出目标关节角"),
           (3.00, "PD 控制器 1 kHz", "把目标角变成力矩"),
           (1.55, "关节出力矩", "机身被推着动，观测变了")]
    for y, t1, t2 in dep:
        fs.box(axb, dx, y, dw, 1.10, "", fc="#FDF1E6", ec=fs.ACCENT, lw=1.1)
        fs.label(axb, dx + dw / 2, y + 0.72, t1, fs=8.8, weight="bold", color=fs.ACCENT)
        fs.label(axb, dx + dw / 2, y + 0.32, t2, fs=7.9, color=fs.MUTED)
    fs.arrow(axb, (dx + dw / 2, 4.38), (dx + dw / 2, 4.18), color=fs.ACCENT)
    fs.arrow(axb, (dx + dw / 2, 2.93), (dx + dw / 2, 2.73), color=fs.ACCENT)

    # 观测回到策略
    axb.plot([dx + dw + 0.16, dx + dw + 0.16], [2.10, 5.00], color=fs.FAINT, lw=1.0,
             ls=(0, (3, 2)), zorder=2)
    axb.annotate("", xy=(dx + dw + 0.16, 5.05), xytext=(dx + dw + 0.16, 4.85),
                 arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=1.0))
    fs.label(axb, dx + dw + 0.42, 3.55, "新观测回去", fs=8.0, color=fs.MUTED, rotation=90)

    fs.label(axb, 0.02, 6.35, "（b）仿真里练，真机上跑", fs=8.8, ha="left", color=fs.MUTED)

    fs.save(fig, "ch16", "fig16-03")


if __name__ == "__main__":
    fig_zmp()
    fig_lipm()
    fig_gait_loop()
