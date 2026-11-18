# -*- coding: utf-8 -*-
"""第 8 章插图：交互循环与回合、三类算法关系、稀疏与稠密奖励的学习曲线。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


# ---------------------------------------------------------------- 图 8-1
def fig_loop():
    """智能体-环境交互循环，下方接一条状态-动作-奖励序列。"""
    fig, ax = fs.canvas(6.6, 4.1)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.7)

    # 上：两个框与两条互反的箭头
    fs.box(ax, 0.95, 4.95, 2.55, 1.15, "智能体\n策略 π(a|s)", fs=9.4, fc="#FFFFFF", ec=fs.INK)
    fs.box(ax, 6.50, 4.95, 2.55, 1.15, "环境\n物理 · 任务 · 传感器", fs=9.4, fc="#FFFFFF", ec=fs.INK)

    fs.arrow(ax, (3.53, 5.76), (6.47, 5.76), color=fs.ACCENT, lw=1.3)
    ax.text(5.0, 5.86, "动作 $a_t$", ha="center", va="bottom", fontsize=8.8, color=fs.ACCENT)

    fs.arrow(ax, (6.47, 5.28), (3.53, 5.28), color=fs.BLUE, lw=1.3)
    ax.text(5.0, 5.15, "$s_{t+1}$ 与 $r_{t+1}$", ha="center", va="top",
            fontsize=8.8, color=fs.BLUE)

    # 中：状态-动作序列（折线往返）
    top, bot = 3.55, 2.30
    xs = [0.95, 2.35, 3.75, 5.15, 6.55, 7.95, 9.35]
    labels = ["$s_0$", "$a_0$", "$s_1$", "$a_1$", "$s_2$", "$a_2$", "$s_T$"]
    for i, (x, lab) in enumerate(zip(xs, labels)):
        y = top if i % 2 == 0 else bot
        fc = "#F1F5F9" if i % 2 == 0 else "#FDF3EC"
        ec = fs.INK if i % 2 == 0 else fs.ACCENT
        fs.box(ax, x - 0.42, y - 0.28, 0.84, 0.56, lab, fs=9.2, fc=fc, ec=ec, lw=0.9)

    for i in range(len(xs) - 1):
        x0, y0 = xs[i], (top if i % 2 == 0 else bot)
        x1, y1 = xs[i + 1], (top if (i + 1) % 2 == 0 else bot)
        up = 1 if y1 > y0 else -1
        p0 = (x0 + 0.44, y0 + 0.17 * up)
        p1 = (x1 - 0.44, y1 + 0.17 * up)
        fs.arrow(ax, p0, p1, color=fs.FAINT, lw=1.0, ms=7)
        if i % 2 == 1:  # 动作到下一状态这一段带奖励
            ax.text((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + 0.24,
                    "$r_%d$" % ((i + 1) // 2), ha="center", va="bottom",
                    fontsize=8.6, color=fs.GREEN)

    # 下：一个回合的括号
    ax.annotate("", xy=(9.35, 1.32), xytext=(0.95, 1.32),
                arrowprops=dict(arrowstyle="<->", color=fs.MUTED, lw=0.9))
    ax.text(5.15, 1.14, "一个回合（episode），第 T 步到达终止状态后清零重来",
            ha="center", va="top", fontsize=8.6, color=fs.MUTED)

    # 上方说明：循环的节奏
    ax.text(5.0, 6.58, "每步 t 重复一次，机器人控制频率常见 10–100 Hz",
            ha="center", va="center", fontsize=8.6, color=fs.FAINT)
    fs.save(fig, "ch08", "fig08-01")


# ---------------------------------------------------------------- 图 8-2
def fig_families():
    """三类算法的关系：值方法、策略梯度、actor-critic。"""
    fig, ax = fs.canvas(6.6, 3.7)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.9)

    # 上：actor-critic
    fs.box(ax, 2.85, 4.05, 4.30, 1.45, "", fs=9.2, fc="#EEF2F7", ec=fs.PURPLE, lw=1.1)
    ax.text(5.0, 5.20, "actor-critic", ha="center", va="center", fontsize=9.6,
            color=fs.INK, weight="bold")
    ax.text(5.0, 4.78, "输出 π(a|s) 与 V(s) 或 Q(s,a)", ha="center", va="center",
            fontsize=9.0, color=fs.INK)
    ax.text(5.0, 4.34, "PPO · SAC · DDPG", ha="center", va="center",
            fontsize=8.8, color=fs.PURPLE)

    # 下左：值方法
    fs.box(ax, 0.55, 1.60, 3.60, 0.95, "值方法\n只学 Q(s,a)", fs=9.2,
           fc="#FFFFFF", ec=fs.BLUE, lw=1.1)
    ax.text(2.35, 1.38, "Q-learning · DQN", ha="center", va="top",
            fontsize=8.8, color=fs.BLUE)
    ax.text(2.35, 1.00, "要对动作取 max\n连续动作难处理", ha="center", va="top",
            fontsize=8.2, color=fs.MUTED, linespacing=1.5)

    # 下右：策略梯度
    fs.box(ax, 5.85, 1.60, 3.60, 0.95, "策略梯度\n直接学 π(a|s)", fs=9.2,
           fc="#FFFFFF", ec=fs.GREEN, lw=1.1)
    ax.text(7.65, 1.38, "REINFORCE", ha="center", va="top",
            fontsize=8.8, color=fs.GREEN)
    ax.text(7.65, 1.00, "回报方差大\n需要大量样本", ha="center", va="top",
            fontsize=8.2, color=fs.MUTED, linespacing=1.5)

    # 两条汇合的箭头
    fs.arrow(ax, (2.95, 2.60), (3.95, 4.00), color=fs.BLUE, lw=1.1)
    ax.text(2.86, 3.28, "用 Q 当 critic", ha="right", va="center",
            fontsize=8.4, color=fs.BLUE)
    fs.arrow(ax, (7.05, 2.60), (6.05, 4.00), color=fs.GREEN, lw=1.1)
    ax.text(7.14, 3.28, "加 baseline 降方差", ha="left", va="center",
            fontsize=8.4, color=fs.GREEN)

    fs.save(fig, "ch08", "fig08-02")


# ---------------------------------------------------------------- 图 8-3 的实验
def run_gridworld(n_seeds=20, n_ep=400, n=32, max_steps=200, gamma=0.99,
                  alpha=0.12, eps=0.15, noise=0.1, eval_every=10, eval_eps=6):
    """32x32 网格上的表格 Q-learning，对比稀疏奖励与稠密奖励。

    状态是格子坐标，动作是 8 个方向，带 10% 的执行噪声。
    稀疏奖励只在到达目标时给 +1；稠密奖励用基于势能的塑形
    r = γΦ(s') - Φ(s)，Φ(s) = 1 - 距离/对角线长，到达时再加 +1。
    每 10 个训练回合用纯贪心策略评估 6 次。
    返回 (回合轴, 稀疏成功率矩阵, 稠密成功率矩阵)，矩阵形状为 (种子, 评估点)。
    """
    goal = np.array([n - 1, n - 1], float)
    diag = np.linalg.norm([n - 1, n - 1])
    acts = np.array([[1, 0], [-1, 0], [0, 1], [0, -1],
                     [1, 1], [1, -1], [-1, 1], [-1, -1]], float)

    def phi(p):
        return 1.0 - np.linalg.norm(p - goal) / diag

    def idx(p):
        return int(round(p[0])) * n + int(round(p[1]))

    res = {}
    for mode in ("sparse", "dense"):
        curve = np.zeros((n_seeds, n_ep // eval_every))
        for s in range(n_seeds):
            rng = np.random.default_rng(1000 + s)
            Q = np.zeros((n * n, len(acts)))
            for ep in range(n_ep):
                p = rng.integers(0, n - 1, size=2).astype(float)
                while np.linalg.norm(p - goal) < 6:
                    p = rng.integers(0, n - 1, size=2).astype(float)
                for _ in range(max_steps):
                    si = idx(p)
                    a = rng.integers(0, len(acts)) if rng.random() < eps else int(np.argmax(Q[si]))
                    mv = acts[a] if rng.random() > noise else acts[rng.integers(0, len(acts))]
                    p2 = np.clip(p + mv, 0, n - 1)
                    hit = np.linalg.norm(p2 - goal) < 0.6
                    if mode == "sparse":
                        r = 1.0 if hit else 0.0
                    else:
                        r = (1.0 if hit else 0.0) + gamma * phi(p2) - phi(p)
                    sj = idx(p2)
                    target = r if hit else r + gamma * Q[sj].max()
                    Q[si, a] += alpha * (target - Q[si, a])
                    p = p2
                    if hit:
                        break
                if (ep + 1) % eval_every == 0:
                    ok = 0
                    for _ in range(eval_eps):
                        q = rng.integers(0, n - 1, size=2).astype(float)
                        for _ in range(max_steps):
                            q = np.clip(q + acts[int(np.argmax(Q[idx(q)]))], 0, n - 1)
                            if np.linalg.norm(q - goal) < 0.6:
                                ok += 1
                                break
                    curve[s, (ep + 1) // eval_every - 1] = ok / eval_eps
        res[mode] = curve
    ep = np.arange(1, n_ep // eval_every + 1) * eval_every
    return ep, res["sparse"], res["dense"]


def fig_curves(ep, sp, dn):
    """稀疏奖励与稠密奖励的成功率曲线（网格世界实测，20 个随机种子）。"""
    fig, ax = fs.new(6.6, 3.3)
    fs.clean(ax, grid=True)
    for arr, color, lab in ((dn, fs.BLUE, "稠密奖励（每步按接近目标的程度给分）"),
                            (sp, fs.ACCENT, "稀疏奖励（只在成功时给 +1）")):
        m = arr.mean(axis=0)
        sd = arr.std(axis=0)
        ax.fill_between(ep, np.clip(m - sd, 0, 1), np.clip(m + sd, 0, 1),
                        color=color, alpha=0.13, lw=0)
        ax.plot(ep, m, color=color, lw=1.4, label=lab)
    ax.set_xlabel("训练回合")
    ax.set_ylabel("贪心策略的成功率")
    ax.set_xlim(0, ep[-1])
    ax.set_ylim(-0.02, 1.04)
    ax.legend(loc="lower right")
    ax.text(0.0, -0.30, "32×32 网格，8 个动作方向，表格 Q-learning，20 个随机种子取平均",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.2, color=fs.MUTED)
    fs.save(fig, "ch08", "fig08-03")


if __name__ == "__main__":
    fig_loop()
    fig_families()
    ep, sp, dn = run_gridworld()
    for name, arr in (("sparse", sp), ("dense", dn)):
        m = arr.mean(axis=0)
        reach = np.argmax(m >= 0.5) if (m >= 0.5).any() else -1
        print("%s: 首次达到 0.5 的评估点 = %s, 末期 = %.3f"
              % (name, ep[reach] if reach >= 0 else "无", m[-5:].mean()))
    fig_curves(ep, sp, dn)
