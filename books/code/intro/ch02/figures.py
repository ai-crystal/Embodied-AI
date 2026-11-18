# -*- coding: utf-8 -*-
"""第 2 章插图：二连杆正运动学、逆运动学两解、坐标系链条。"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle
import figstyle as fs

L1, L2 = 0.4, 0.3
TH1, TH2 = 30.0, 45.0


def joints(th1_deg, th2_deg):
    a = math.radians(th1_deg)
    b = math.radians(th1_deg + th2_deg)
    elbow = (L1 * math.cos(a), L1 * math.sin(a))
    tcp = (elbow[0] + L2 * math.cos(b), elbow[1] + L2 * math.sin(b))
    return elbow, tcp


def axis_arrows(ax, xmax, ymax):
    ax.annotate("", xy=(xmax, 0), xytext=(-0.02, 0),
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=1.0, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(0, ymax), xytext=(0, -0.02),
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=1.0, shrinkA=0, shrinkB=0))
    fs.label(ax, xmax - 0.01, -0.030, "x", fs=8.6, color=fs.MUTED, ha="right")
    fs.label(ax, -0.014, ymax - 0.02, "y", fs=8.6, color=fs.MUTED, ha="right", va="top")


def draw_arm(ax, th1, th2, link_colors=(fs.INK, fs.INK), lw=5.2, ms=7.0, base=True):
    elbow, tcp = joints(th1, th2)
    ax.plot([0, elbow[0]], [0, elbow[1]], color=link_colors[0], lw=lw,
            solid_capstyle="round", zorder=4)
    ax.plot([elbow[0], tcp[0]], [elbow[1], tcp[1]], color=link_colors[1], lw=lw * 0.86,
            solid_capstyle="round", zorder=4)
    for p in ((0.0, 0.0), elbow):
        ax.add_patch(Circle(p, 0.0115, facecolor="white", edgecolor=fs.ACCENT,
                            lw=1.3, zorder=6))
    if base:
        ax.add_patch(Rectangle((-0.032, -0.030), 0.064, 0.017, facecolor=fs.LIGHT,
                               edgecolor=fs.FAINT, lw=0.9, zorder=5))
    return elbow, tcp


def fig_fk():
    """正运动学：二连杆算例。"""
    fig = plt.figure(figsize=(6.6, 3.9))
    ax = fig.add_axes([0.015, 0.02, 0.50, 0.96])
    ax.set_xlim(-0.088, 0.66)
    ax.set_ylim(-0.075, 0.575)
    ax.set_aspect("equal")
    ax.axis("off")
    axis_arrows(ax, 0.62, 0.545)

    elbow, tcp = draw_arm(ax, TH1, TH2)

    ax.add_patch(Arc((0, 0), 0.29, 0.29, theta1=0, theta2=TH1, color=fs.ACCENT, lw=1.0))
    fs.label(ax, 0.196, 0.058, "$\\theta_1$ = 30°", fs=8.6, color=fs.ACCENT, ha="left")
    ax.add_patch(Arc(elbow, 0.185, 0.185, theta1=TH1, theta2=TH1 + TH2,
                     color=fs.ACCENT, lw=1.0))
    fs.label(ax, 0.437, 0.300, "$\\theta_2$ = 45°", fs=8.6, color=fs.ACCENT, ha="left")

    fs.label(ax, 0.158, 0.135, "$L_1$ = 0.4 m", fs=8.6, color=fs.INK, rotation=30,
             ha="center", va="bottom")
    fs.label(ax, 0.300, 0.370, "$L_2$ = 0.3 m", fs=8.6, color=fs.INK, rotation=75,
             ha="center", va="bottom")

    ax.plot([tcp[0], tcp[0]], [tcp[1], 0], color=fs.FAINT, lw=0.8, ls=(0, (3, 3)), zorder=2)
    ax.plot([tcp[0], 0], [tcp[1], tcp[1]], color=fs.FAINT, lw=0.8, ls=(0, (3, 3)), zorder=2)
    ax.plot([tcp[0]], [tcp[1]], marker="o", ms=6.5, color=fs.ACCENT, zorder=7)
    fs.label(ax, tcp[0] + 0.018, tcp[1] + 0.020, "末端", fs=8.6, color=fs.ACCENT, ha="left")
    fs.label(ax, tcp[0], -0.026, "0.424", fs=8.4, color=fs.MUTED, ha="center", va="top")
    fs.label(ax, -0.010, tcp[1], "0.490", fs=8.4, color=fs.MUTED, ha="right")

    ax2 = fig.add_axes([0.535, 0.03, 0.45, 0.94])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    rows = [
        (0.955, "算例", 9.6, fs.ACCENT, "bold"),
        (0.885, "$L_1$ = 0.4 m　$L_2$ = 0.3 m", 8.8, fs.INK, "normal"),
        (0.820, "$\\theta_1$ = 30°　$\\theta_2$ = 45°", 8.8, fs.INK, "normal"),
        (0.735, "肘关节的位置", 8.2, fs.MUTED, "normal"),
        (0.672, "0.4×cos30° = 0.346", 8.6, fs.INK, "normal"),
        (0.609, "0.4×sin30° = 0.200", 8.6, fs.INK, "normal"),
        (0.524, "第二根连杆的绝对角度", 8.2, fs.MUTED, "normal"),
        (0.461, "30° + 45° = 75°", 8.6, fs.INK, "normal"),
        (0.376, "末端位置", 8.2, fs.MUTED, "normal"),
        (0.313, "x = 0.346 + 0.3×cos75°", 8.6, fs.INK, "normal"),
        (0.250, "　= 0.346 + 0.078 = 0.424", 8.6, fs.ACCENT, "normal"),
        (0.174, "y = 0.200 + 0.3×sin75°", 8.6, fs.INK, "normal"),
        (0.111, "　= 0.200 + 0.290 = 0.490", 8.6, fs.ACCENT, "normal"),
    ]
    for y, s, f, c, w in rows:
        ax2.text(0.0, y, s, fontsize=f, color=c, weight=w, ha="left", va="center")
    fs.save(fig, "ch02", "fig02-01")


def fig_ik():
    """逆运动学：同一个目标点的两个解。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.5))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.10, wspace=0.05)
    sols = [
        (30.0, 45.0, "(a) 肘向下", "$\\theta_1$ = 30°　$\\theta_2$ = 45°"),
        (68.2, -45.0, "(b) 肘向上", "$\\theta_1$ = 68.2°　$\\theta_2$ = -45°"),
    ]
    target = joints(30.0, 45.0)[1]
    for ax, (t1, t2, tag, lab) in zip(axes, sols):
        ax.set_xlim(-0.05, 0.58)
        ax.set_ylim(-0.05, 0.62)
        ax.set_aspect("equal")
        ax.axis("off")
        axis_arrows(ax, 0.545, 0.585)

        ax.plot([0, target[0]], [0, target[1]], color=fs.FAINT, lw=0.8,
                ls=(0, (4, 3)), zorder=1)
        elbow, tcp = draw_arm(ax, t1, t2)
        ax.plot([target[0]], [target[1]], marker="o", ms=6.5, color=fs.ACCENT, zorder=7)
        fs.label(ax, target[0] + 0.016, target[1] + 0.032, "目标点", fs=8.4,
                 color=fs.ACCENT, ha="left")

        ax.add_patch(Arc((0, 0), 0.24, 0.24, theta1=0, theta2=t1, color=fs.BLUE, lw=0.9))
        fs.label(ax, 0.148, 0.028, "$\\theta_1$", fs=8.2, color=fs.BLUE, ha="left")
        if t2 > 0:
            ax.add_patch(Arc(elbow, 0.165, 0.165, theta1=t1, theta2=t1 + t2,
                             color=fs.BLUE, lw=0.9))
            fs.label(ax, elbow[0] + 0.085, elbow[1] + 0.098, "$\\theta_2$", fs=8.2, color=fs.BLUE)
        else:
            ax.add_patch(Arc(elbow, 0.165, 0.165, theta1=t1 + t2, theta2=t1,
                             color=fs.BLUE, lw=0.9))
            fs.label(ax, elbow[0] + 0.046, elbow[1] + 0.132, "$\\theta_2$", fs=8.2,
                     color=fs.BLUE, ha="left", va="bottom")
        fs.label(ax, 0.27, 0.60, lab, fs=8.4, color=fs.INK)
        ax.text(0.5, -0.075, tag, transform=ax.transAxes, ha="center", va="center",
                fontsize=9.2, color=fs.INK, weight="bold")
    fs.save(fig, "ch02", "fig02-02")


def fig_chain():
    """坐标链条：世界 -> 基座 -> 末端 -> 相机 -> 像素。"""
    fig, ax = fs.canvas(6.6, 4.9)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 6.3)

    nodes = [
        (5.35, "世界坐标 W", "桌子、盘子和杯子在哪", fs.GREEN),
        (4.25, "基座坐标 B", "底盘，螺丝拧紧后不动", fs.INK),
        (3.15, "末端坐标 E", "指尖中心，跟着关节动", fs.ACCENT),
        (2.05, "相机坐标 C", "腕上相机光心，z 轴朝前", fs.BLUE),
        (0.95, "像素坐标 P", "图像里的 (u, v) 加深度", fs.PURPLE),
    ]
    W, H = 4.20, 0.78
    for y, name, desc, col in nodes:
        fs.box(ax, 0.30, y, W, H, "", fc="#FFFFFF", ec=col, lw=1.2)
        ax.text(0.50, y + H * 0.66, name, fontsize=9.2, color=col, va="center",
                ha="left", weight="bold", zorder=6)
        ax.text(0.50, y + H * 0.28, desc, fontsize=8.2, color=fs.MUTED, va="center",
                ha="left", zorder=6)

    links = [
        ("T_world_base　安装时标定一次（0 Hz）"),
        ("T_base_ee　由六个编码器读数算出（1 kHz）"),
        ("T_ee_cam　手眼标定，撞过就得重做（0 Hz）"),
        ("K　内参矩阵，投影成像素（30 Hz）"),
    ]
    for i, lab in enumerate(links):
        y_top = nodes[i][0]
        y_bot = nodes[i + 1][0] + H
        fs.arrow(ax, (2.40, y_top - 0.012), (2.40, y_bot + 0.012), color=fs.FAINT, lw=1.1)
        ax.text(4.66, (y_top + y_bot) / 2, lab, fontsize=8.4, color=fs.INK,
                va="center", ha="left")

    ax.text(0.30, 0.52, "四段变换里任何一段不准，最后那个像素就落不准",
            fontsize=8.4, color=fs.MUTED, ha="left")
    fs.save(fig, "ch02", "fig02-03")


if __name__ == "__main__":
    fig_fk()
    fig_ik()
    fig_chain()
