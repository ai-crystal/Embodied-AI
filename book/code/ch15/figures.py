# -*- coding: utf-8 -*-
"""第 15 章插图：三类世界模型、世界模型在环、空间能力评测。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, Ellipse, Arc, FancyBboxPatch
import figstyle as fs


# ---------------------------------------------------------------- 图 15-1
def fig_three():
    """三类世界模型的对比：像素空间、隐空间、交互式。"""
    fig, ax = fs.canvas(7.2, 4.5)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.4)

    panels = [
        (0.25, "（a）像素空间预测", "第 $t$ 帧\n（RGB 像素）", "视频扩散\n或自回归",
         "pix", "逐像素重建未来帧",
         ["强项　结果可以直接看", "代价　算力大，细节靠猜"]),
        (4.25, "（b）隐空间预测", "第 $t$ 帧", "编码器 +\n表征预测器",
         "lat", "只给隐向量，不还原画面",
         ["强项　忽略不可预测的细节", "代价　看不见，也难当模拟器"]),
        (8.25, "（c）交互式预测", "当前帧 +\n动作 $a_t$", "动作条件\n生成器",
         "act", "动作驱动，逐帧推进",
         ["强项　人可以直接上手操作", "代价　动作与画面对应很弱"]),
    ]

    for x0, title, in_txt, mid_txt, kind, cap, notes in panels:
        ax.add_patch(Rectangle((x0, 0.50), 3.5, 6.20, facecolor="#FCFAF6",
                               edgecolor=fs.GRID, lw=0.9, zorder=1))
        ax.text(x0 + 1.75, 6.38, title, ha="center", va="center", fontsize=9.6,
                color=fs.INK, weight="bold", zorder=4)

        bw = 2.15 if kind == "act" else 2.4
        bx = x0 + (0.45 if kind == "act" else 0.55)
        cx = bx + bw / 2
        fs.box(ax, bx, 5.15, bw, 0.85, in_txt, fs=9.0, fc="white", ec=fs.MUTED, lw=1.0)
        fs.arrow(ax, (cx, 5.10), (cx, 4.62), color=fs.FAINT, lw=1.0)
        fs.box(ax, bx, 3.72, bw, 0.85, mid_txt, fs=9.0, fc="white", ec=fs.INK, lw=1.1)
        fs.arrow(ax, (cx, 3.67), (cx, 3.19), color=fs.FAINT, lw=1.0)

        # 第三行：三种输出各画一种小图
        if kind == "pix":
            for i in range(4):
                fx = x0 + 0.52 + i * 0.62
                ax.add_patch(Rectangle((fx, 2.40), 0.52, 0.66, facecolor="#F2F5F9",
                                       edgecolor=fs.MUTED, lw=0.8, zorder=3))
                ax.plot([fx, fx + 0.52], [2.72, 2.72], color=fs.FAINT, lw=0.6, zorder=4)
                ax.add_patch(Ellipse((fx + 0.24, 2.60), 0.20, 0.14, facecolor=fs.ACCENT,
                                     alpha=0.55, edgecolor="none", zorder=4))
        elif kind == "lat":
            for i, hh in enumerate([0.22, 0.36, 0.28, 0.42, 0.31, 0.24]):
                lx = x0 + 0.72 + i * 0.32
                ax.add_patch(Rectangle((lx, 2.55), 0.20, hh, facecolor="#DCE6F5",
                                       edgecolor=fs.BLUE, lw=0.8, zorder=3))
            ax.text(x0 + 2.62, 2.80, "…", ha="left", va="center", fontsize=10,
                    color=fs.BLUE, zorder=4)
            ax.text(x0 + 1.75, 3.12, "$\\hat z_{t+k}$", ha="center", va="bottom",
                    fontsize=8.6, color=fs.BLUE, zorder=4)
        else:
            for i in range(3):
                fx = x0 + 0.45 + i * 0.72
                ax.add_patch(Rectangle((fx, 2.38), 0.56, 0.62, facecolor="#F2F5F9",
                                       edgecolor=fs.MUTED, lw=0.8, zorder=3))
                ax.plot([fx, fx + 0.56], [2.66, 2.66], color=fs.FAINT, lw=0.6, zorder=4)
                ax.add_patch(Circle((fx + 0.26, 2.56), 0.09, facecolor=fs.GREEN,
                                    alpha=0.55, edgecolor="none", zorder=4))
                if i < 2:
                    fs.arrow(ax, (fx + 0.58, 2.69), (fx + 0.68, 2.69),
                             color=fs.GREEN, lw=1.0, ms=7)
            # 输出回流到输入的循环：右侧折线箭头
            ax.plot([x0 + 2.62, x0 + 2.86], [4.14, 4.14], color=fs.GREEN, lw=1.0, zorder=2)
            ax.plot([x0 + 2.86, x0 + 2.86], [4.14, 5.57], color=fs.GREEN, lw=1.0, zorder=2)
            fs.arrow(ax, (x0 + 2.86, 5.57), (x0 + 2.62, 5.57), color=fs.GREEN, lw=1.0, ms=7)
            ax.text(x0 + 3.14, 4.86, "循环", ha="center", va="center", fontsize=8.0,
                    color=fs.GREEN, rotation=90, zorder=5)

        ax.text(x0 + 1.75, 2.00, cap, ha="center", va="center", fontsize=8.4,
                color=fs.MUTED, zorder=4)
        ax.plot([x0 + 0.45, x0 + 3.05], [1.68, 1.68], color=fs.GRID, lw=0.8, zorder=2)
        ax.text(x0 + 1.75, 1.34, notes[0], ha="center", va="center", fontsize=8.2,
                color=fs.GREEN, zorder=4)
        ax.text(x0 + 1.75, 0.98, notes[1], ha="center", va="center", fontsize=8.2,
                color=fs.ACCENT, zorder=4)

    fs.save(fig, "ch15", "fig15-01")


# ---------------------------------------------------------------- 图 15-2
def fig_loop():
    """世界模型在环：采样、想象、打分、执行、回到真实观测。"""
    fig, ax = fs.canvas(7.0, 3.3)
    ax.set_xlim(0, 11)
    ax.set_ylim(1.20, 6.05)

    boxes = [
        ("A", 0.25, 4.95, 2.30, "当前观测 $o_t$"),
        ("B", 3.50, 4.95, 2.60, "策略采样 $N$ 条\n动作块"),
        ("C", 7.00, 4.95, 3.30, "世界模型\n滚 $k$ 步"),
        ("D", 7.00, 2.40, 3.30, "按预测回报\n排序选一条"),
        ("E", 3.50, 2.40, 2.60, "执行第一段\n动作块"),
        ("F", 0.25, 2.40, 2.30, "真实环境\n推进 $\\Delta t$"),
    ]
    for _, x, y, w, txt in boxes:
        fs.box(ax, x, y, w, 0.95, txt, fs=9.0, fc="white", ec=fs.INK, lw=1.1)

    fs.arrow(ax, (2.58, 5.42), (3.47, 5.42), color=fs.MUTED, lw=1.1)
    fs.arrow(ax, (6.13, 5.42), (6.97, 5.42), color=fs.MUTED, lw=1.1)
    fs.arrow(ax, (8.65, 4.92), (8.65, 3.38), color=fs.MUTED, lw=1.1)
    fs.arrow(ax, (6.97, 2.88), (6.13, 2.88), color=fs.MUTED, lw=1.1)
    fs.arrow(ax, (3.47, 2.88), (2.58, 2.88), color=fs.MUTED, lw=1.1)
    fs.arrow(ax, (1.40, 3.38), (1.40, 4.92), color=fs.MUTED, lw=1.1)

    ax.text(3.02, 5.52, "候选", ha="center", va="bottom", fontsize=8.0, color=fs.MUTED)
    ax.text(8.82, 4.16, "预测回报", ha="left", va="center", fontsize=8.0, color=fs.MUTED)
    ax.text(3.02, 2.98, "下发", ha="center", va="bottom", fontsize=8.0, color=fs.MUTED)

    # 中间：三条候选轨迹的预测回报（示意）
    ax.add_patch(Rectangle((3.62, 3.44), 3.10, 1.16, facecolor="#FCFAF6",
                           edgecolor=fs.GRID, lw=0.8, zorder=1))
    ax.text(5.17, 4.38, "三条候选的预测回报", ha="center", va="center",
            fontsize=8.0, color=fs.MUTED, zorder=4)
    bars = [("1", 1.90, fs.GREEN), ("2", 1.18, fs.GOLD), ("3", 0.58, fs.FAINT)]
    for i, (lab, w, c) in enumerate(bars):
        y = 4.10 - i * 0.21
        ax.add_patch(Rectangle((4.18, y - 0.075), w, 0.15, facecolor=c, alpha=0.85,
                               edgecolor="none", zorder=4))
        ax.text(4.06, y, lab, ha="right", va="center", fontsize=8.0, color=fs.MUTED, zorder=4)

    ax.text(5.5, 1.80, "整圈只有一步走真机，其余都在模型里；模型这一步的偏差会留进下一圈的观测。",
            ha="center", va="center", fontsize=8.4, color=fs.INK)

    fs.save(fig, "ch15", "fig15-02")


# ---------------------------------------------------------------- 图 15-3
def _card(ax, label):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0.01, 0.01), 0.98, 0.98, facecolor="#FCFAF6",
                           edgecolor=fs.GRID, lw=0.9, zorder=1))
    ax.text(0.05, 0.93, label, ha="left", va="center", fontsize=9.2,
            color=fs.INK, weight="bold", zorder=6)


def fig_tasks():
    """空间能力评测的四类任务。"""
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.6))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.06, hspace=0.06)
    fig.canvas.draw()

    # (a) 相对深度
    ax = axes[0, 0]
    _card(ax, "（a）相对深度")
    ax.add_patch(Polygon([[0.04, 0.18], [0.96, 0.18], [0.72, 0.54], [0.28, 0.54]],
                         closed=True, facecolor="#F0F2F5", edgecolor=fs.FAINT, lw=0.8, zorder=2))
    ax.plot([0.04, 0.96], [0.18, 0.18], color=fs.MUTED, lw=1.0, zorder=3)
    # 远处的箱子（落在台面远边上）
    ax.add_patch(Rectangle((0.55, 0.50), 0.14, 0.13, facecolor="#E8EDF3",
                           edgecolor=fs.MUTED, lw=0.9, zorder=4))
    ax.add_patch(Polygon([[0.55, 0.63], [0.59, 0.68], [0.73, 0.68], [0.69, 0.63]],
                         closed=True, facecolor="#DDE4EC", edgecolor=fs.MUTED, lw=0.9, zorder=4))
    # 近处的杯子
    ax.add_patch(Rectangle((0.27, 0.28), 0.10, 0.18, facecolor="#F3E4D8",
                           edgecolor=fs.MUTED, lw=0.9, zorder=4))
    ax.add_patch(Ellipse((0.32, 0.46), 0.10, 0.045, facecolor="#EBD6C4",
                         edgecolor=fs.MUTED, lw=0.9, zorder=5))
    ax.add_patch(Circle((0.32, 0.37), 0.016, facecolor=fs.ACCENT, edgecolor="white",
                        lw=0.7, zorder=7))
    ax.add_patch(Circle((0.60, 0.565), 0.016, facecolor=fs.BLUE, edgecolor="white",
                        lw=0.7, zorder=7))
    ax.text(0.255, 0.37, "A", ha="right", va="center", fontsize=8.6, color=fs.ACCENT, zorder=7)
    ax.text(0.625, 0.565, "B", ha="left", va="center", fontsize=8.6, color=fs.BLUE, zorder=7)
    ax.text(0.5, 0.83, "A、B 哪一点更近？", ha="center", va="center", fontsize=8.8, color=fs.INK)
    ax.text(0.5, 0.07, "人 99.2　GPT-4V 58.9　随机 50", ha="center", va="center",
            fontsize=8.0, color=fs.MUTED)

    # (b) 表面法向：侧视图，一条斜表面 + 两个候选方向
    ax = axes[0, 1]
    _card(ax, "（b）表面法向")
    A0, A1 = np.array([0.12, 0.30]), np.array([0.88, 0.50])
    ax.plot([A0[0], A1[0]], [A0[1], A1[1]], color=fs.INK, lw=1.8, zorder=4,
            solid_capstyle="round")
    for t in np.linspace(0.06, 0.94, 12):
        px = A0 + (A1 - A0) * t
        ax.plot([px[0] + 0.012, px[0] - 0.012], [px[1] - 0.005, px[1] - 0.045],
                color=fs.FAINT, lw=0.7, zorder=3)
    P = np.array([0.46, 0.389])
    d = A1 - A0
    # 用显示坐标算真正的垂直方向，避免坐标轴不等比造成视觉上不垂直
    pd = ax.transData.transform(P)
    dd = ax.transData.transform(A1) - ax.transData.transform(A0)
    n = np.array([-dd[1], dd[0]])
    n = n / np.linalg.norm(n)
    L = 0.26 * ax.get_window_extent().height
    tip = ax.transData.inverted().transform(pd + n * L)
    fs.arrow(ax, tuple(P), tuple(tip), color=fs.GREEN, lw=1.4, ms=9, z=6)
    fs.arrow(ax, tuple(P), (0.66, 0.66), color=fs.ACCENT, lw=1.4, ms=9, z=6)
    ax.text(tip[0] - 0.055, tip[1] + 0.02, "1", ha="center", va="center",
            fontsize=8.6, color=fs.GREEN, zorder=7)
    ax.text(0.675, 0.645, "2", ha="left", va="center", fontsize=8.6, color=fs.ACCENT, zorder=7)
    ax.text(0.5, 0.83, "哪个箭头垂直于表面？", ha="center", va="center", fontsize=8.8, color=fs.INK)
    ax.text(0.5, 0.07, "只看局部几何，与物体是什么无关", ha="center", va="center",
            fontsize=8.0, color=fs.MUTED)

    # (c) 对应关系
    ax = axes[1, 0]
    _card(ax, "（c）对应关系")
    for x0 in (0.06, 0.50):
        ax.add_patch(Rectangle((x0, 0.22), 0.40, 0.52, facecolor="white",
                               edgecolor=fs.FAINT, lw=0.8, zorder=2))
    # 左图：正对视角的杯子
    ax.add_patch(Rectangle((0.20, 0.36), 0.12, 0.20, facecolor="#F3E4D8",
                           edgecolor=fs.MUTED, lw=0.9, zorder=3))
    ax.add_patch(Ellipse((0.26, 0.555), 0.12, 0.04, facecolor="#EBD6C4",
                         edgecolor=fs.MUTED, lw=0.9, zorder=4))
    ax.add_patch(Arc((0.33, 0.46), 0.09, 0.11, theta1=-90, theta2=90,
                     edgecolor=fs.MUTED, lw=0.9, zorder=3))
    ax.add_patch(Circle((0.225, 0.475), 0.015, facecolor=fs.ACCENT, edgecolor="white",
                        lw=0.7, zorder=6))
    ax.text(0.185, 0.475, "1", ha="right", va="center", fontsize=8.6, color=fs.ACCENT, zorder=6)
    # 右图：转过一个角度的杯子，三个候选点
    ax.add_patch(Polygon([[0.63, 0.36], [0.72, 0.375], [0.72, 0.545], [0.63, 0.53]],
                         closed=True, facecolor="#F3E4D8", edgecolor=fs.MUTED, lw=0.9, zorder=3))
    ax.add_patch(Ellipse((0.675, 0.538), 0.09, 0.035, facecolor="#EBD6C4",
                         edgecolor=fs.MUTED, lw=0.9, zorder=4))
    for lab, (px, py), (tx, ty, ha), c in (
            ("A", (0.648, 0.45), (0.615, 0.415, "right"), fs.BLUE),
            ("B", (0.712, 0.432), (0.742, 0.404, "left"), fs.GREEN),
            ("C", (0.80, 0.51), (0.818, 0.51, "left"), fs.PURPLE)):
        ax.add_patch(Circle((px, py), 0.015, facecolor=c, edgecolor="white", lw=0.7, zorder=6))
        ax.text(tx, ty, lab, ha=ha, va="center", fontsize=8.6, color=c, zorder=6)
    ax.text(0.5, 0.83, "右图哪一点与左图的 1 是同一处？", ha="center", va="center",
            fontsize=8.8, color=fs.INK)
    ax.text(0.5, 0.10, "人 99.4　GPT-4V 37.2　随机 25", ha="center", va="center",
            fontsize=8.0, color=fs.MUTED)

    # (d) 3D 问答
    ax = axes[1, 1]
    _card(ax, "（d）三维关系问答")
    ax.add_patch(Polygon([[0.06, 0.34], [0.94, 0.34], [0.94, 0.24], [0.06, 0.24]],
                         closed=True, facecolor="#F0F2F5", edgecolor=fs.FAINT, lw=0.8, zorder=2))
    ax.plot([0.06, 0.94], [0.34, 0.34], color=fs.MUTED, lw=1.2, zorder=3)
    ax.add_patch(Rectangle((0.17, 0.34), 0.10, 0.18, facecolor="#F3E4D8",
                           edgecolor=fs.MUTED, lw=0.9, zorder=4))
    ax.add_patch(Arc((0.27, 0.43), 0.08, 0.10, theta1=-90, theta2=90,
                     edgecolor=fs.MUTED, lw=0.9, zorder=4))
    ax.add_patch(Ellipse((0.72, 0.345), 0.26, 0.06, facecolor="#E8EDF3",
                         edgecolor=fs.MUTED, lw=0.9, zorder=4))
    ax.add_patch(Ellipse((0.72, 0.375), 0.20, 0.045, facecolor="white",
                         edgecolor=fs.FAINT, lw=0.7, zorder=5))
    ax.text(0.5, 0.83, "杯子在盘子的左边吗？", ha="center", va="center", fontsize=8.8, color=fs.INK)
    ax.text(0.5, 0.10, "人 98.3　GPT-4V 72.0　随机 50", ha="center", va="center",
            fontsize=8.0, color=fs.MUTED)

    fs.save(fig, "ch15", "fig15-03")


if __name__ == "__main__":
    fig_three()
    fig_loop()
    fig_tasks()
