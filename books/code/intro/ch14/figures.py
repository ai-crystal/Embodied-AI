# -*- coding: utf-8 -*-
"""第 14 章插图：三类世界模型、预测-评估-执行循环、四类空间任务。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon
import figstyle as fs


def fig_three():
    """三条路线：像素、隐空间、交互式。每行一条流水线。"""
    fig, ax = fs.canvas(6.6, 4.05)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.15)

    rows = [
        (5.40, "（a）\n像素空间", fs.BLUE, "#EEF3FB",
         ["一帧观测\nH×W×3", "视频生成模型\n7B 到 14B", "32 帧 = 3.2 s\n720p", "逐像素比对\n错一格也算错"],
         "输出能直接拿给人看，代价是每个像素都要对。",
         "杯沿错一格，穿模就露出来了。"),
        (3.35, "（b）\n隐空间", fs.GREEN, "#ECF6F1",
         ["一段视频\n16 帧", "编码器\nViT", "表征 z\n每块一个", "预测未来\n只比表征"],
         "不比像素，只比表征，细节被主动丢掉。",
         "省下的是生成成本，丢掉的也是细节。"),
        (1.30, "（c）\n交互式", fs.ACCENT, "#FDF1E6",
         ["无标注视频\n3 万小时", "隐动作 a\n8 个码", "动力学模型\n逐帧推", "下一帧\n10 FPS"],
         "动作没人标，从相邻两帧的变化里反推。",
         "人给一个 a，模型就得推一步。"),
    ]

    for y, tag, color, tint, texts, n1, n2 in rows:
        fs.box(ax, 0.15, y - 0.50, 1.30, 1.00, tag, fs=9.0, ec=color, fc=tint,
               tc=color, weight="bold")
        xs = [1.62, 3.64, 5.66, 7.68]
        for i, (x, t) in enumerate(zip(xs, texts)):
            ec = color if i in (1, 2) else fs.MUTED
            fs.box(ax, x, y - 0.40, 1.66, 0.80, t, fs=8.5, ec=ec, fc="#FFFFFF")
            if i:
                fs.arrow(ax, (x - 0.33, y), (x - 0.04, y), color=fs.FAINT, lw=1.0)
        fs.label(ax, 1.62, y - 0.72, n1, fs=8.1, color=fs.MUTED, ha="left", va="center")
        fs.label(ax, 1.62, y - 0.98, n2, fs=8.1, color=fs.FAINT, ha="left", va="center")

    fs.save(fig, "ch14", "fig14-01")


def fig_loop():
    """预测-评估-执行的一圈，以及这一圈的算力账。"""
    fig, ax = fs.canvas(6.6, 3.56)
    ax.set_xlim(0, 10)
    ax.set_ylim(0.95, 6.25)

    fs.label(ax, 0.25, 6.02, "一个控制周期里走一遍", fs=9.2, ha="left", weight="bold")

    y, h = 4.55, 0.92
    fs.box(ax, 0.25, y, 1.62, h, "当前观测\n图像 + 关节角", fs=8.2, ec=fs.MUTED)
    fs.box(ax, 2.22, y, 1.78, h, "世界模型\n在表征上推演", fs=8.4, ec=fs.ACCENT, fc="#FDF1E6")
    fs.box(ax, 6.45, y, 1.55, h, "打分器\n价值 + 奖励", fs=8.4, ec=fs.PURPLE, fc="#F3EFFC")
    fs.box(ax, 8.40, y, 1.45, h, "选最高的一条\n只执行第一步", fs=8.0, ec=fs.GREEN, fc="#ECF6F1")

    fs.arrow(ax, (1.89, y + h / 2), (2.20, y + h / 2), color=fs.INK, lw=1.1)
    fs.arrow(ax, (4.02, y + h / 2), (4.33, y + h / 2), color=fs.INK, lw=1.1)
    fs.arrow(ax, (6.00, y + h / 2), (6.43, y + h / 2), color=fs.INK, lw=1.1)
    fs.arrow(ax, (8.02, y + h / 2), (8.38, y + h / 2), color=fs.INK, lw=1.1)

    # 一条想象中的轨迹，五格代表几步
    for k in range(5):
        ax.add_patch(Rectangle((4.36 + k * 0.34, y + 0.22), 0.26, 0.48,
                               facecolor="#DCE7F7" if k < 2 else "#FFFFFF",
                               edgecolor=fs.BLUE if k < 2 else fs.FAINT, lw=0.8, zorder=3))
    fs.label(ax, 5.16, y + 0.92, "一条轨迹 = 15 步", fs=8.2, color=fs.BLUE)

    # 算力账
    ax.add_patch(Rectangle((1.55, 2.72), 6.10, 1.12, facecolor="#FCFCFD",
                           edgecolor=fs.FAINT, lw=0.9, linestyle=(0, (4, 3)), zorder=2))
    fs.label(ax, 1.74, 3.56, "这一圈要花多少", fs=8.8, ha="left", weight="bold")
    fs.label(ax, 1.74, 3.22, "32 条 × 15 步 = 480 次前向", fs=8.2, color=fs.MUTED, ha="left")
    fs.label(ax, 1.74, 2.90, "单步 2 ms 就是 0.96 s，控制环一圈只有 100 ms", fs=8.2, color=fs.MUTED, ha="left")

    # 执行之后回到观测
    fs.arrow(ax, (9.12, y - 0.02), (9.12, 2.22), color=fs.GREEN, lw=1.1)
    fs.box(ax, 8.35, 1.32, 1.55, 0.88, "机械臂动一步\n只动这一步", fs=8.2, ec=fs.GREEN, fc="#ECF6F1")
    fs.arrow(ax, (8.37, 1.76), (1.06, 1.76), color=fs.GREEN, lw=1.1)
    fs.label(ax, 4.70, 1.94, "世界变了，下一次观测从这里开始", fs=8.2, color=fs.GREEN)
    fs.arrow(ax, (1.06, 1.78), (1.06, y - 0.03), color=fs.GREEN, lw=1.1)

    fs.save(fig, "ch14", "fig14-03")


def fig_four():
    """四类空间任务：深度、法向、对应、三维问答。"""
    fig, ax = fs.canvas(6.6, 4.40)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.60)

    # (a) 相对深度
    fs.label(ax, 0.20, 6.34, "（a）相对深度", fs=9.2, ha="left", weight="bold", color=fs.BLUE)
    ax.add_patch(Polygon([(0.40, 4.82), (4.40, 4.82), (4.02, 5.98), (0.78, 5.98)],
                         closed=True, facecolor=fs.LIGHT, edgecolor=fs.GRID, lw=0.8, zorder=2))
    for px, py, lab in ((1.65, 4.98, "A"), (3.02, 5.48, "B")):
        ax.add_patch(plt.Circle((px, py), 0.10, facecolor=fs.ACCENT, edgecolor="white",
                                lw=0.8, zorder=5))
        fs.label(ax, px + 0.18, py + 0.02, lab, fs=8.6, color=fs.INK, ha="left")
    fs.label(ax, 2.40, 4.55, "问：哪个点离相机更近", fs=8.2, color=fs.MUTED)
    fs.label(ax, 2.40, 4.26, "GPT-4V 58.9　人 99.2　随机 50", fs=8.1, color=fs.INK)

    # (b) 表面法向：一段曲面 + 切线与法线
    fs.label(ax, 5.20, 6.34, "（b）表面法向", fs=9.2, ha="left", weight="bold", color=fs.GREEN)
    cx, cy, r = 7.45, 4.42, 1.32
    th = np.linspace(np.deg2rad(48), np.deg2rad(132), 60)
    outer = np.column_stack([cx + r * np.cos(th), cy + r * np.sin(th)])
    inner = np.column_stack([cx + (r - 0.14) * np.cos(th[::-1]), cy + (r - 0.14) * np.sin(th[::-1])])
    ax.add_patch(Polygon(np.vstack([outer, inner]), closed=True, facecolor="#E7F0EA",
                         edgecolor=fs.GREEN, lw=1.0, zorder=3))
    ax.plot([cx - 0.62, cx + 0.62], [cy + r, cy + r], color=fs.GREEN, lw=1.0,
            ls=(0, (3, 2)), zorder=4)
    fs.arrow(ax, (cx, cy + r), (cx, cy + r + 0.30), color=fs.GREEN, lw=1.2, ms=9)
    fs.label(ax, cx - 0.14, cy + r + 0.16, "n", fs=8.8, color=fs.GREEN, ha="right")
    ax.add_patch(plt.Circle((cx, cy + r), 0.055, facecolor=fs.INK, edgecolor="white",
                            lw=0.7, zorder=6))
    fs.label(ax, 7.40, 4.55, "问：这一点朝哪个方向", fs=8.2, color=fs.MUTED)
    fs.label(ax, 7.40, 4.26, "没有统一考卷，通常单测平均角误差", fs=8.1, color=fs.INK)

    # (c) 点对应
    fs.label(ax, 0.20, 3.34, "（c）点对应", fs=9.2, ha="left", weight="bold", color=fs.PURPLE)
    for x0 in (0.40, 2.62):
        ax.add_patch(Rectangle((x0, 1.92), 1.78, 1.06, facecolor=fs.PAPER,
                               edgecolor=fs.MUTED, lw=0.9, zorder=3))
    ax.plot([0.62, 1.92], [2.10, 2.72], color=fs.FAINT, lw=0.8, zorder=4)
    ax.plot([2.86, 4.14], [2.16, 2.66], color=fs.FAINT, lw=0.8, zorder=4)
    for px, py in ((1.22, 2.50), (3.50, 2.42)):
        ax.add_patch(plt.Circle((px, py), 0.085, facecolor=fs.PURPLE, edgecolor="white",
                                lw=0.8, zorder=6))
        ax.plot([px - 0.16, px + 0.16], [py, py], color=fs.PURPLE, lw=0.7, zorder=5)
        ax.plot([px, px], [py - 0.16, py + 0.16], color=fs.PURPLE, lw=0.7, zorder=5)
    ax.annotate("", xy=(3.42, 2.56), xytext=(1.30, 2.62),
                arrowprops=dict(arrowstyle="<->", color=fs.PURPLE, lw=0.9,
                                connectionstyle="arc3,rad=-0.12"))
    fs.label(ax, 2.16, 3.16, "同一个点", fs=8.0, color=fs.PURPLE)
    fs.label(ax, 2.40, 1.66, "问：两张图里哪两个点是同一个点", fs=8.2, color=fs.MUTED)
    fs.label(ax, 2.40, 1.36, "GPT-4V 31.5　人 99.4　随机 25", fs=8.1, color=fs.INK)

    # (d) 三维问答
    fs.label(ax, 5.20, 3.34, "（d）三维问答", fs=9.2, ha="left", weight="bold", color=fs.ACCENT)
    ax.add_patch(Rectangle((5.30, 1.92), 4.35, 1.06, facecolor="#FFFFFF",
                           edgecolor=fs.GRID, lw=0.9, zorder=3))
    ax.add_patch(Rectangle((5.66, 2.04), 0.58, 0.52, facecolor=fs.LIGHT,
                           edgecolor=fs.MUTED, lw=0.9, zorder=5))
    ax.add_patch(Rectangle((8.42, 2.10), 0.42, 0.68, facecolor=fs.LIGHT,
                           edgecolor=fs.MUTED, lw=0.9, zorder=5))
    ax.annotate("", xy=(8.38, 2.42), xytext=(6.30, 2.42),
                arrowprops=dict(arrowstyle="<->", color=fs.ACCENT, lw=1.0))
    fs.label(ax, 7.34, 2.58, "? m", fs=8.6, color=fs.ACCENT)
    fs.label(ax, 7.47, 1.66, "问：这两个物体相距多少米", fs=8.2, color=fs.MUTED)
    fs.label(ax, 7.47, 1.36, "GPT-4V 1.0% 的答案带数字，SpatialVLM 99.0%", fs=8.1, color=fs.INK)

    fs.save(fig, "ch14", "fig14-02")


if __name__ == "__main__":
    fig_three()
    fig_loop()
    fig_four()
