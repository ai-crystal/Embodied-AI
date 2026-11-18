# -*- coding: utf-8 -*-
"""第 8 章插图：交互循环与回合、三类算法关系、稀疏与稠密奖励的学习曲线。

第三张图不是示意图。脚本里带一个 36x36 网格上的表格 Q-learning 实验，
稀疏奖励与稠密奖励各跑 8 个随机种子，曲线是实测值，跑完约 10 秒。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_loop():
    """(a) 智能体与环境的循环 (b) 一条回合的时间轴。"""
    fig, ax = fs.canvas(6.6, 4.9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0.95, 8.25)

    # ---------- (a) ----------
    fs.label(ax, 0.10, 8.02, "(a)", fs=10, color=fs.MUTED, ha="left", va="top")

    W, H = 3.55, 1.20
    fs.box(ax, 0.42, 6.18, W, H, "智能体（策略）\n看画面和关节角\n输出三维速度增量", fs=9.0)
    fs.box(ax, 6.05, 6.18, W, H, "环境（桌面与方块）\n执行动作，物理演化\n给出新画面和新分数", fs=9.0)

    fs.arrow(ax, (4.00, 7.08), (6.02, 7.08))
    fs.label(ax, 5.00, 7.16, "动作 $a_t$", fs=9.0, color=fs.INK, va="bottom")

    fs.arrow(ax, (6.02, 6.48), (4.00, 6.48), color=fs.ACCENT)
    fs.label(ax, 5.00, 6.40, "状态与奖励", fs=9.0, color=fs.ACCENT, va="top")

    fs.label(ax, 5.00, 5.62, "转一圈交换一次，一步 100 毫秒", fs=9.0, color=fs.MUTED)

    # ---------- (b) ----------
    fs.label(ax, 0.10, 5.15, "(b)", fs=10, color=fs.MUTED, ha="left", va="top")

    x0, x1, y = 0.55, 9.45, 2.60
    ax.plot([x0, x1 + 0.12], [y, y], color=fs.INK, lw=1.4, zorder=2)
    ax.plot([x1 + 0.12, x1 + 0.05], [y, y + 0.09], color=fs.INK, lw=1.4, zorder=2)
    ax.plot([x1 + 0.12, x1 + 0.05], [y, y - 0.09], color=fs.INK, lw=1.4, zorder=2)

    def X(t):
        return x0 + (x1 - x0) * t / 120.0

    marks = [
        (0, "回合开始\n机械臂回到初始位姿", 2.88, "left"),
        (45, "手接近方块\n夹爪合上", 3.40, "center"),
        (95, "方块进入目标区\n奖励 +1", 2.88, "center"),
        (120, "回合结束\n环境清零", 3.40, "right"),
    ]
    for t, text, ly, ha in marks:
        x = X(t)
        ax.scatter([x], [y], s=26, color=fs.ACCENT, zorder=5, edgecolor="white", linewidth=0.9)
        ax.plot([x, x], [y + 0.03, ly - 0.05], color=fs.FAINT, lw=0.8, zorder=1)
        fs.label(ax, x, ly, text, fs=8.6, ha=ha, va="bottom")

    for t in (0, 30, 60, 90, 120):
        ax.plot([X(t), X(t)], [y - 0.05, y + 0.05], color=fs.MUTED, lw=0.9, zorder=3)
        fs.label(ax, X(t), y - 0.12, f"{t}", fs=8.2, color=fs.MUTED, va="top")

    fs.label(ax, 5.00, 1.72, "一步 = 100 毫秒，120 步 = 12 秒，这就是一个回合",
             fs=9.0, color=fs.MUTED)
    fs.label(ax, 5.00, 1.28, "中途超时不算失败，只把回报截断，否则策略会学会抢先结束",
             fs=8.4, color=fs.FAINT)

    fs.save(fig, "ch08", "fig08-01")


def fig_families():
    """价值方法、策略梯度、actor-critic 三条路线的关系。"""
    fig, ax = fs.canvas(6.6, 4.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.85)

    fs.box(ax, 0.35, 4.60, 4.25, 2.06,
           "价值方法\n先给每个动作打分\n再挑分最高的那个\n代表 DQN（2013）",
           fs=9.0, ec=fs.BLUE, fc="#EEF3FB")
    fs.box(ax, 5.40, 4.60, 4.25, 2.06,
           "策略梯度\n直接把动作概率往上推\n回报高就推得多\n代表 REINFORCE",
           fs=9.0, ec=fs.PURPLE, fc="#F3EEFB")
    fs.box(ax, 2.20, 1.84, 5.60, 2.08,
           "actor-critic\nactor 出动作，critic 当对照组\n两边一起学，互为依赖\nPPO（2017）到 SAC（2018）都属于这一支",
           fs=9.0, ec=fs.GREEN, fc="#EAF5F0")

    fs.arrow(ax, (1.75, 4.55), (3.20, 3.96), color=fs.BLUE, rad=-0.10)
    fs.label(ax, 0.45, 4.42, "价值函数\n当 baseline", fs=8.6, color=fs.BLUE, ha="left", va="top")

    fs.arrow(ax, (8.25, 4.55), (6.80, 3.96), color=fs.PURPLE, rad=0.10)
    fs.label(ax, 9.55, 4.42, "减掉\nbaseline", fs=8.6, color=fs.PURPLE, ha="right", va="top")

    fs.box(ax, 0.55, 0.45, 4.10, 1.00, "裁剪概率比\n一批数据训十个 epoch", fs=8.6,
           ec=fs.GREEN, fc="#FFFFFF")
    fs.box(ax, 5.35, 0.45, 4.10, 1.00, "奖励里加熵\n能完成就多留几种做法", fs=8.6,
           ec=fs.GREEN, fc="#FFFFFF")
    fs.label(ax, 2.60, 1.58, "PPO", fs=9.2, color=fs.GREEN, weight="bold")
    fs.label(ax, 7.40, 1.58, "SAC", fs=9.2, color=fs.GREEN, weight="bold")

    fs.save(fig, "ch08", "fig08-02")


def _smooth(x, k):
    return np.convolve(x, np.ones(k) / k, mode="valid")


def _qlearn(dense, seed, n=36, episodes=600, alpha=0.15, gamma=0.99,
            coef=0.02, eps0=0.3, decay=300, maxstep=300, evals=5):
    """36x36 网格上的表格 Q-learning，返回每个回合结束时贪心策略的成功率。

    dense=False 只在到达目标时给 +1；dense=True 每步再加一截势能差，
    势能取负的曼哈顿距离，系数 coef。
    """
    rng = np.random.default_rng(seed)
    goal = (n - 1, n - 1)
    acts = ((0, 1), (1, 0), (0, -1), (-1, 0))
    Q = np.zeros((n, n, 4))
    dist = lambda s: abs(s[0] - goal[0]) + abs(s[1] - goal[1])
    curve = []

    for ep in range(episodes):
        eps = max(0.05, eps0 * (1.0 - ep / decay))
        s = (int(rng.integers(0, n)), int(rng.integers(0, n)))
        for _ in range(maxstep):
            a = int(rng.integers(4)) if rng.random() < eps else int(np.argmax(Q[s[0], s[1]]))
            dx, dy = acts[a]
            ns = (min(n - 1, max(0, s[0] + dx)), min(n - 1, max(0, s[1] + dy)))
            r = 1.0 if ns == goal else 0.0
            if dense:
                r += coef * (dist(s) - dist(ns))
            nxt = 0.0 if ns == goal else np.max(Q[ns[0], ns[1]])
            Q[s[0], s[1], a] += alpha * (r + gamma * nxt - Q[s[0], s[1], a])
            s = ns
            if s == goal:
                break

        hit = 0
        for _ in range(evals):
            s = (int(rng.integers(0, n)), int(rng.integers(0, n)))
            for _ in range(maxstep):
                a = int(np.argmax(Q[s[0], s[1]]))
                dx, dy = acts[a]
                s = (min(n - 1, max(0, s[0] + dx)), min(n - 1, max(0, s[1] + dy)))
                if s == goal:
                    hit += 1
                    break
        curve.append(hit / evals)
    return np.array(curve)


def fig_reward_curve(seeds=8, k=15):
    """稀疏奖励与势能塑形奖励的学习曲线（实测）。"""
    fig, ax = fs.new(6.6, 3.5)
    fs.clean(ax, grid=True)

    def stat(dense):
        runs = [_smooth(_qlearn(dense, s), k) for s in range(seeds)]
        m = np.mean(runs, axis=0)
        sd = np.std(runs, axis=0)
        ep = np.arange(len(m)) + k
        return ep, m, sd

    for dense, name, color in ((True, "稠密奖励（每步给势能差）", fs.GREEN),
                               (False, "稀疏奖励（成功才给 1）", fs.ACCENT)):
        ep, m, sd = stat(dense)
        idx = np.where(m >= 0.5)[0]
        print("%-4s 达到 50%% 的回合 %s，末值 %.2f" % (
            name[:2], (idx[0] + k) if len(idx) else None, m[-1]))
        ax.plot(ep, m, color=color, lw=1.8, label=name, zorder=4)
        ax.fill_between(ep, np.clip(m - sd, 0, 1.08), np.clip(m + sd, 0, 1.08),
                        color=color, alpha=0.16, lw=0, zorder=2)

    ax.set_xlim(0, 600)
    ax.set_ylim(0, 1.20)
    ax.set_xlabel("训练回合")
    ax.set_ylabel("贪心策略成功率")
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.axhline(0.5, color=fs.GRID, lw=1.0, zorder=1)
    ax.annotate("稠密：15 回合到 0.79", xy=(18, 0.80), xytext=(62, 0.87), fontsize=8.2,
                color=fs.GREEN, va="center",
                arrowprops=dict(arrowstyle="-", color=fs.GREEN, lw=0.7))
    ax.annotate("稀疏：170 回合到 0.50", xy=(170, 0.50), xytext=(196, 0.34), fontsize=8.2,
                color=fs.ACCENT, va="center",
                arrowprops=dict(arrowstyle="-", color=fs.ACCENT, lw=0.7))
    ax.legend(loc="lower right", fontsize=8.6)
    ax.text(10, 1.16, "36×36 网格，8 个随机种子，阴影为一倍标准差",
            fontsize=8.2, color=fs.MUTED, va="top")
    fs.save(fig, "ch08", "fig08-03")


if __name__ == "__main__":
    fig_loop()
    fig_families()
    fig_reward_curve()
