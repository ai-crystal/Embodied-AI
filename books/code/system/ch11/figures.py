# -*- coding: utf-8 -*-
"""第 11 章插图：构型空间、RRT 生长、分层规划栈。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
import figstyle as fs


def fig_cspace():
    """构型空间：障碍、膨胀边界、可行路径。"""
    fig, ax = fs.canvas(6.6, 4.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.4)

    cx, cy = 4.8, 3.6
    a_out, b_out = 1.9, 1.5
    a_in, b_in = 1.4, 1.0

    # 坐标轴
    fs.arrow(ax, (0.15, 0.22), (9.9, 0.22), color=fs.FAINT, lw=0.9, ms=7)
    fs.arrow(ax, (0.15, 0.22), (0.15, 6.2), color=fs.FAINT, lw=0.9, ms=7)
    ax.text(9.92, 0.02, "$q_1$", ha="right", va="bottom", fontsize=9, color=fs.MUTED)
    ax.text(0.05, 6.25, "$q_2$", ha="left", va="bottom", fontsize=9, color=fs.MUTED)

    # 膨胀区与障碍核心
    ax.add_patch(Ellipse((cx, cy), 2 * a_out, 2 * b_out, facecolor="#F4E7DE",
                         edgecolor="none", zorder=1))
    ax.add_patch(Ellipse((cx, cy), 2 * a_out, 2 * b_out, facecolor="none",
                         edgecolor=fs.ACCENT, lw=1.1, ls=(0, (4, 2.4)), zorder=4))
    ax.add_patch(Ellipse((cx, cy), 2 * a_in, 2 * b_in, facecolor="#E2CDBE",
                         edgecolor="#B08968", lw=1.0, zorder=2))
    ax.text(cx - 0.45, cy, "障碍区", ha="center", va="center", fontsize=9, color=fs.INK, zorder=6)
    ax.text(cx, cy - 1.25, "膨胀区", ha="center", va="center", fontsize=8, color=fs.MUTED, zorder=6)

    # 膨胀量标注（顶部）
    ax.annotate("", xy=(cx, cy + b_out), xytext=(cx, cy + b_in),
                arrowprops=dict(arrowstyle="<|-|>", color=fs.ACCENT, lw=1.0,
                                mutation_scale=7, shrinkA=1, shrinkB=1))
    ax.text(cx, cy + b_out + 0.16, "膨胀量 r", ha="center", va="bottom",
            fontsize=8.4, color=fs.ACCENT)

    # 起点、终点
    S = np.array([0.75, 0.95])
    G = np.array([8.85, 5.30])
    ax.plot([S[0], G[0]], [S[1], G[1]], ls=(0, (3, 2.6)), color=fs.FAINT, lw=1.0, zorder=3)

    # 直连被挡的位置
    t = (5.95 - S[0]) / (G[0] - S[0])
    px, py = S[0] + t * (G[0] - S[0]), S[1] + t * (G[1] - S[1])
    d = 0.13
    ax.plot([px - d, px + d], [py - d, py + d], color=fs.PINK, lw=1.3, zorder=7)
    ax.plot([px - d, px + d], [py + d, py - d], color=fs.PINK, lw=1.3, zorder=7)

    # 一条绕过膨胀障碍的路径
    path = np.array([[0.75, 0.95], [2.6, 1.02], [4.4, 1.05], [6.1, 1.20],
                     [7.35, 2.15], [7.78, 3.60], [7.45, 4.95], [8.85, 5.30]])
    ax.plot(path[:, 0], path[:, 1], color=fs.BLUE, lw=1.4, zorder=5,
            solid_joinstyle="round")
    ax.scatter(path[1:-1, 0], path[1:-1, 1], s=8, color=fs.BLUE, zorder=6)

    ax.scatter([S[0]], [S[1]], s=42, color=fs.GREEN, zorder=8, edgecolor="white", linewidth=0.9)
    ax.scatter([G[0]], [G[1]], s=46, marker="s", color=fs.GOLD, zorder=8,
               edgecolor="white", linewidth=0.9)

    ax.text(S[0] + 0.05, S[1] - 0.38, "起点 S", ha="left", va="center", fontsize=8.8, color=fs.INK)
    ax.text(G[0], G[1] + 0.42, "终点 G", ha="center", va="bottom", fontsize=8.8, color=fs.INK)
    ax.text(2.15, 0.62, "可行路径", ha="left", va="center", fontsize=8.6, color=fs.BLUE)

    fs.save(fig, "ch11", "fig11-01")


# ---------- RRT ----------
START = np.array([0.10, 0.12])
GOAL = np.array([0.90, 0.86])
OBS_C = np.array([0.52, 0.50])
OBS_R = 0.17


def _free(p):
    return np.linalg.norm(p - OBS_C) > OBS_R


def _seg_free(a, b, k=14):
    for t in np.linspace(0, 1, k):
        if not _free(a + (b - a) * t):
            return False
    return True


def _rrt(seed=7, n_iter=300, step=0.045, goal_bias=0.10):
    """朴素的 RRT：向随机样本生长，带目标偏置。返回节点、边与父节点。"""
    rng = np.random.default_rng(seed)
    nodes = [START.copy()]
    parent = [-1]
    for _ in range(n_iter):
        q = GOAL if rng.random() < goal_bias else rng.random(2)
        p = np.array(nodes)
        j = int(np.argmin(np.linalg.norm(p - q, axis=1)))
        v = q - nodes[j]
        L = float(np.linalg.norm(v))
        if L < 1e-9:
            continue
        new = nodes[j] + v / L * min(step, L)
        if not _free(new) or not _seg_free(nodes[j], new):
            continue
        nodes.append(new)
        parent.append(j)
    return np.array(nodes), parent


def _path_to_goal(nodes, parent, tol=0.06):
    d = np.linalg.norm(nodes - GOAL, axis=1)
    cand = np.where(d < tol)[0]
    if len(cand) == 0:
        return None
    i = int(cand[0])
    out = [nodes[i]]
    while parent[i] >= 0:
        i = parent[i]
        out.append(nodes[i])
    return np.array(out[::-1])


def fig_rrt():
    """RRT 树的三个阶段。"""
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.62))
    fig.subplots_adjust(wspace=0.08)
    placed = []
    for ax, n_iter, tag in zip(axes, (30, 90, 300), ("a", "b", "c")):
        nodes, parent = _rrt(seed=11, n_iter=n_iter)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ("top", "right", "left", "bottom"):
            ax.spines[s].set_color(fs.FAINT)
            ax.spines[s].set_linewidth(0.8)

        for i in range(1, len(nodes)):
            a, b = nodes[parent[i]], nodes[i]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=fs.BLUE, lw=0.65, zorder=3,
                    solid_capstyle="round")
        ax.scatter(nodes[1:, 0], nodes[1:, 1], s=3.2, color=fs.FAINT, zorder=4)

        ax.add_patch(plt.Circle(tuple(OBS_C), OBS_R, facecolor="#E2CDBE",
                                edgecolor="#B08968", lw=0.9, zorder=5))
        ax.scatter([START[0]], [START[1]], s=26, color=fs.GREEN, zorder=8,
                   edgecolor="white", linewidth=0.7)
        ax.scatter([GOAL[0]], [GOAL[1]], s=34, facecolor="white", edgecolor=fs.GOLD,
                   linewidth=1.2, zorder=8)

        path = _path_to_goal(nodes, parent)
        if path is not None:
            ax.plot(path[:, 0], path[:, 1], color=fs.ACCENT, lw=1.4, zorder=7)

        ax.text(0.03, 0.965, "(%s)" % tag, ha="left", va="top", fontsize=9.2,
                color=fs.INK, weight="bold", zorder=9)
        ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="none", edgecolor=fs.FAINT,
                               lw=0.8, zorder=10))
        placed.append((ax, len(nodes)))

    # 采样次数统一排在框外，保证三个 panel 的基线一致
    y_bottom = min(ax.get_position().y0 for ax, _ in placed)
    for ax, n in placed:
        pos = ax.get_position()
        fig.text(pos.x0 + pos.width / 2, y_bottom - 0.045, "%d 次采样" % n,
                 ha="center", va="top", fontsize=8, color=fs.MUTED)

    fs.save(fig, "ch11", "fig11-02")


def fig_stack():
    """任务层、运动层、控制层的输入输出与更新频率。"""
    fig, ax = fs.canvas(6.6, 3.9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.15)

    rows = [
        (4.55, "任务层", "符号搜索 · 大模型分解", "0.1–1 Hz",
         "输入　目标语句 · 场景里的物体与关系 · 技能库",
         "输出　技能序列：抓杯 → 移到壶上 → 倾斜"),
        (2.55, "运动层", "采样规划 · 轨迹优化 · 滚动优化", "1–10 Hz",
         "输入　目标位姿 · 点云与占据栅格 · 当前关节角",
         "输出　关节轨迹（50–100 个路点，含时间戳）"),
        (0.55, "控制层", "阻抗控制 · 力矩控制 · 伺服", "100–1000 Hz",
         "输入　轨迹参考 · 关节编码器 · 力与触觉",
         "输出　关节力矩或位置指令（每周期一次）"),
    ]
    x0, w, h = 0.3, 9.05, 1.28
    for y, name, how, hz, line_in, line_out in rows:
        fs.box(ax, x0, y, w, h, "", fc="white", ec=fs.INK, lw=1.0, z=2)
        ax.text(x0 + 0.26, y + h - 0.34, name, ha="left", va="center",
                fontsize=10, color=fs.INK, weight="bold", zorder=4)
        ax.text(x0 + 1.35, y + h - 0.34, how, ha="left", va="center",
                fontsize=8.6, color=fs.MUTED, zorder=4)
        ax.text(x0 + w - 0.22, y + h - 0.34, hz, ha="right", va="center",
                fontsize=8.6, color=fs.ACCENT, zorder=4)
        ax.text(x0 + 0.26, y + 0.52, line_in, ha="left", va="center",
                fontsize=8.3, color=fs.MUTED, zorder=4)
        ax.text(x0 + 0.26, y + 0.20, line_out, ha="left", va="center",
                fontsize=8.3, color=fs.MUTED, zorder=4)

    # 层间箭头
    fs.arrow(ax, (2.05, 4.55), (2.05, 3.83), color=fs.INK, lw=1.1)
    ax.text(2.22, 4.19, "下发位姿与约束", ha="left", va="center",
            fontsize=8.1, color=fs.INK)
    fs.arrow(ax, (7.30, 3.83), (7.30, 4.55), color=fs.BLUE, lw=1.1)
    ax.text(7.13, 4.19, "回报可达性与失败", ha="right", va="center",
            fontsize=8.1, color=fs.BLUE)

    fs.arrow(ax, (2.05, 2.55), (2.05, 1.83), color=fs.INK, lw=1.1)
    ax.text(2.22, 2.19, "参考轨迹与速度", ha="left", va="center",
            fontsize=8.1, color=fs.INK)
    fs.arrow(ax, (7.30, 1.83), (7.30, 2.55), color=fs.BLUE, lw=1.1)
    ax.text(7.13, 2.19, "回报实际位姿", ha="right", va="center",
            fontsize=8.1, color=fs.BLUE)

    fs.save(fig, "ch11", "fig11-03")


if __name__ == "__main__":
    fig_cspace()
    fig_rrt()
    fig_stack()
