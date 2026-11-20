# -*- coding: utf-8 -*-
"""第 11 章插图：构型空间里的膨胀、RRT 生长、分层规划栈。

地图与算法都在本文件里实跑，图上的路径长度、节点数、代价都是脚本算出来的。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

# ---------- 场景：1.2 m x 0.9 m 的桌面，一个 L 形障碍 ----------
AX, AY = 1.20, 0.90          # 台面尺寸
R = 0.12                     # 机器人在平面上的半径（膨胀量）
RECTS = [(0.40, 0.00, 0.52, 0.52),   # 竖条 x0 y0 x1 y1
         (0.40, 0.40, 0.78, 0.52)]   # 横条
START = np.array([0.17, 0.20])
GOAL = np.array([1.03, 0.20])


def rect_dist(p, r):
    """点到轴对齐矩形的距离，点在矩形内时为 0。"""
    x0, y0, x1, y1 = r
    dx = max(x0 - p[0], 0.0, p[0] - x1)
    dy = max(y0 - p[1], 0.0, p[1] - y1)
    return np.hypot(dx, dy)


def free(p, eps=0.0):
    """构型空间里这个点是否可行：点机器人与膨胀障碍不相交，且不出台面。"""
    if p[0] < R + eps or p[0] > AX - R - eps:
        return False
    if p[1] < R + eps or p[1] > AY - R - eps:
        return False
    return all(rect_dist(p, r) >= R + eps for r in RECTS)


def seg_free(p0, p1, n=24):
    for t in np.linspace(0, 1, n):
        if not free(p0 + (p1 - p0) * t):
            return False
    return True


# ---------- A*：0.01 m 栅格，8 邻域 ----------
def astar(step=0.01, margin=0.035):
    """栅格搜索；margin 是往膨胀障碍外面留的安全余量。"""
    import heapq
    nx = int(round(AX / step)) + 1
    ny = int(round(AY / step)) + 1
    grid = np.zeros((nx, ny), dtype=bool)          # True = 可走
    for i in range(nx):
        for j in range(ny):
            grid[i, j] = free(np.array([i * step, j * step]), margin)
    si = (int(round(START[0] / step)), int(round(START[1] / step)))
    gi = (int(round(GOAL[0] / step)), int(round(GOAL[1] / step)))
    nb = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
          (-1, -1, 1.4142), (-1, 1, 1.4142), (1, -1, 1.4142), (1, 1, 1.4142)]
    g = {si: 0.0}
    prev = {}
    h = lambda c: np.hypot((c[0] - gi[0]) * step, (c[1] - gi[1]) * step)
    pq = [(h(si), 0.0, si)]
    seen = set()
    while pq:
        _, gc, c = heapq.heappop(pq)
        if c in seen:
            continue
        seen.add(c)
        if c == gi:
            break
        for dx, dy, w in nb:
            nc = (c[0] + dx, c[1] + dy)
            if not (0 <= nc[0] < nx and 0 <= nc[1] < ny) or not grid[nc]:
                continue
            ng = gc + w * step
            if ng < g.get(nc, 1e9):
                g[nc] = ng
                prev[nc] = c
                heapq.heappush(pq, (ng + h(nc), ng, nc))
    if gi not in g:
        raise RuntimeError("A* 没找到路")
    path = [gi]
    while path[-1] != si:
        path.append(prev[path[-1]])
    path = [np.array([c[0] * step, c[1] * step]) for c in reversed(path)]
    return np.array(path), grid.sum() * step * step


def shorten(path):
    """拉直：能直连就直连，去掉多余的拐点。"""
    out = [path[0]]
    i = 0
    while i < len(path) - 1:
        j = len(path) - 1
        while j > i + 1 and not seg_free(path[i], path[j]):
            j -= 1
        out.append(path[j])
        i = j
    return np.array(out)


def path_len(path):
    return float(np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1)))


# ---------- RRT / RRT* ----------
def rrt(n_iter=2400, step=0.08, goal_bias=0.06, seed=7, star=False, gamma=2.6):
    """在膨胀后的构型空间里长树；返回节点、父指针、每次迭代的路径代价。"""
    rng = np.random.default_rng(seed)
    nodes = [START.copy()]
    parent = [-1]
    cost = [0.0]
    snapshots = {}
    best = []           # (节点数, 若已连到终点的代价)
    first_sol = None
    path_at = {}

    def nearest(p):
        d = [np.linalg.norm(nd - p) for nd in nodes]
        return int(np.argmin(d))

    for it in range(n_iter):
        if rng.random() < goal_bias:
            xr = GOAL.copy()
        else:
            xr = np.array([rng.uniform(R, AX - R), rng.uniform(R, AY - R)])
        i0 = nearest(xr)
        d = xr - nodes[i0]
        L = np.linalg.norm(d)
        if L < 1e-9:
            continue
        xnew = nodes[i0] + d / L * min(step, L)
        if not free(xnew) or not seg_free(nodes[i0], xnew, 12):
            continue
        if star:
            dmax = min(gamma * np.sqrt(np.log(len(nodes) + 1) / (len(nodes) + 1)), 2.0 * step)
            near = [k for k, nd in enumerate(nodes)
                    if np.linalg.norm(nd - xnew) <= dmax and seg_free(nd, xnew, 12)]
            k_best, c_best = i0, cost[i0] + np.linalg.norm(xnew - nodes[i0])
            for k in near:
                c = cost[k] + np.linalg.norm(xnew - nodes[k])
                if c < c_best:
                    k_best, c_best = k, c
            nodes.append(xnew)
            parent.append(k_best)
            cost.append(c_best)
            for k in near:
                c = c_best + np.linalg.norm(xnew - nodes[k])
                if c < cost[k]:
                    parent[k] = len(nodes) - 1
                    cost[k] = c
                    # 子树代价一并更新
                    changed = True
                    while changed:
                        changed = False
                        for m in range(len(nodes)):
                            if parent[m] >= 0:
                                cc = cost[parent[m]] + np.linalg.norm(nodes[m] - nodes[parent[m]])
                                if abs(cc - cost[m]) > 1e-9:
                                    cost[m] = cc
                                    changed = True
        else:
            nodes.append(xnew)
            parent.append(i0)
            cost.append(cost[i0] + np.linalg.norm(xnew - nodes[i0]))

        # 终点判定：离终点足够近就直接连上
        if first_sol is None and np.linalg.norm(xnew - GOAL) <= step and seg_free(xnew, GOAL, 12):
            first_sol = len(nodes)
            path_at["first"] = back(nodes, parent, len(nodes) - 1)
        if first_sol is not None:
            best.append((len(nodes), cost[-1]))

    # 终点取离目标最近的节点补齐
    k = int(np.argmin([np.linalg.norm(nd - GOAL) for nd in nodes]))
    path_at["final"] = back(nodes, parent, k)
    return nodes, parent, cost, first_sol, path_at


def back(nodes, parent, k):
    out = [nodes[k]]
    while parent[k] >= 0:
        k = parent[k]
        out.append(nodes[k])
    if np.linalg.norm(out[0] - GOAL) > 1e-6:
        out = [GOAL.copy()] + out
    return np.array(out[::-1])


def tree_edges(nodes, parent):
    return [(nodes[parent[i]], nodes[i]) for i in range(1, len(nodes))]


# ============================ 图 11-1 ============================
def fig_cspace():
    path_raw, farea = astar(0.01)
    path = shorten(path_raw)
    L = path_len(path)
    clear = min(min(rect_dist(p, r) for r in RECTS) for p in path)
    # 走廊：膨胀障碍顶端（0.52 + R）到台面内边界（AY - R）之间那条窄带
    corridor = (AY - R) - (0.52 + R)
    frac = corridor * (0.78 - 0.28 - 2 * R) / (AX * AY)
    print(f"[11-1] 可行面积 {farea:.3f} m2（占台面 {farea/(AX*AY):.0%}），A* 折线 "
          f"{path_len(path_raw):.3f} m，拉直后 {L:.3f} m，最小间隙 {clear - R:.3f} m；"
          f"走廊高 {corridor:.2f} m，面积占比约 {frac:.1%}")

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.0))
    for ax in axes:
        ax.set_xlim(-0.02, AX + 0.02)
        ax.set_ylim(-0.04, AY + 0.06)
        ax.set_aspect("equal")
        ax.set_xticks([0, 0.3, 0.6, 0.9, 1.2])
        ax.set_yticks([0, 0.3, 0.6, 0.9])
        ax.tick_params(labelsize=8)
        for sp in ("top", "right", "left", "bottom"):
            ax.spines[sp].set_color(fs.FAINT)

    # (a) 工作空间：机器人有半径，直线撞上
    ax = axes[0]
    for r in RECTS:
        ax.add_patch(plt.Rectangle((r[0], r[1]), r[2] - r[0], r[3] - r[1],
                                   facecolor="#E7E3DC", edgecolor=fs.INK, lw=1.0, zorder=2))
    ax.plot([START[0], GOAL[0]], [START[1], GOAL[1]], ls=(0, (4, 3)),
            color=fs.ACCENT, lw=1.2, zorder=4)
    for t, col in ((0.0, fs.BLUE), (0.156, fs.ACCENT), (0.40, fs.ACCENT)):
        c = START + (GOAL - START) * t
        ax.add_patch(plt.Circle(c, R, facecolor="none", edgecolor=col, lw=1.1,
                                ls="-" if t == 0 else (0, (2.2, 2.2)), zorder=5))
    ax.plot(*START, "o", ms=5, color=fs.GREEN, zorder=6)
    ax.plot(*GOAL, "o", ms=5, color=fs.PURPLE, zorder=6)
    fs.label(ax, 0.15, 0.375, "起点", fs=8.6, color=fs.GREEN)
    ax.plot([0.15, 0.15], [0.355, 0.328], color=fs.GREEN, lw=0.7, zorder=4)
    fs.label(ax, 1.04, 0.315, "终点", fs=8.6, color=fs.PURPLE)
    fs.label(ax, 0.70, 0.335, "撞上", fs=8.6, color=fs.ACCENT, ha="left")
    fs.arrow(ax, (0.715, 0.320), (0.622, 0.272), color=fs.ACCENT, lw=0.9, ms=7)
    fs.label(ax, 0.04, 0.885, "（a）工作空间", fs=8.8, color=fs.MUTED, ha="left")
    fs.label(ax, 0.15, 0.035, "半径 0.12 m", fs=8.0, color=fs.BLUE)

    # (b) 构型空间：点机器人 + 膨胀障碍 + 绕行路径
    ax = axes[1]
    for r in RECTS:
        x0, y0, x1, y1 = r
        w, h = x1 - x0, y1 - y0
        ax.add_patch(fs.FancyBboxPatch((x0 - R, y0 - R), w + 2 * R, h + 2 * R,
                                       boxstyle=f"round,pad=0,rounding_size={R}",
                                       facecolor="#F7DCCB", edgecolor=fs.ACCENT,
                                       lw=1.1, alpha=0.9, zorder=2))
        ax.add_patch(plt.Rectangle((x0, y0), w, h, facecolor="none",
                                   edgecolor=fs.INK, lw=0.9, ls=(0, (3, 2)), zorder=3))
    ax.plot(path[:, 0], path[:, 1], color=fs.BLUE, lw=1.7, zorder=5,
            solid_capstyle="round")
    ax.plot(*START, "o", ms=5, color=fs.GREEN, zorder=6)
    ax.plot(*GOAL, "o", ms=5, color=fs.PURPLE, zorder=6)
    fs.label(ax, 0.15, 0.095, "起点", fs=8.6, color=fs.GREEN)
    fs.label(ax, 1.04, 0.315, "终点", fs=8.6, color=fs.PURPLE)
    fs.label(ax, 0.04, 0.885, "（b）构型空间", fs=8.8, color=fs.MUTED, ha="left")
    fs.label(ax, 0.68, 0.845, f"绕行 {L:.2f} m", fs=8.4, color=fs.BLUE)
    fs.label(ax, 0.905, 0.050, f"外扩 {R:.2f} m", fs=8.2, color=fs.ACCENT)
    fs.arrow(ax, (0.735, 0.088), (0.735, 0.268), color=fs.ACCENT, lw=0.9, ms=7)
    fs.save(fig, "ch11", "fig11-01")


# ============================ 图 11-2 ============================
def fig_rrt():
    nodes, parent, cost, first_sol, path_at = rrt(2400, star=False, seed=7)
    print(f"[11-2] RRT 第一次连到终点用了 {first_sol} 个节点，代价 {path_len(path_at['first']):.3f} m；"
          f"跑满 {len(nodes)} 个节点后最优代价 {path_len(path_at['final']):.3f} m")
    nodes2, parent2, cost2, first2, pa2 = rrt(2400, star=True, seed=7)
    print(f"[11-2] RRT* 同样 2400 次迭代，节点 {len(nodes2)}，第一次代价 "
          f"{path_len(pa2['first']):.3f} m，最终代价 {path_len(pa2['final']):.3f} m")

    frames = [(60, "（a）60 个节点"), (400, "（b）400 个节点"),
              (len(nodes), f"（c）{len(nodes)} 个节点")]
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.25))
    for ax, (n, lab) in zip(axes, frames):
        ax.set_xlim(-0.02, AX + 0.02)
        ax.set_ylim(-0.02, AY + 0.02)
        ax.set_aspect("equal")
        ax.set_xticks([0, 0.6, 1.2])
        ax.set_yticks([0, 0.45, 0.9])
        ax.tick_params(labelsize=8, length=2.5)
        for sp in ("top", "right", "left", "bottom"):
            ax.spines[sp].set_color(fs.FAINT)
        for r in RECTS:
            x0, y0, x1, y1 = r
            ax.add_patch(fs.FancyBboxPatch((x0 - R, y0 - R), (x1 - x0) + 2 * R, (y1 - y0) + 2 * R,
                                           boxstyle=f"round,pad=0,rounding_size={R}",
                                           facecolor="#F1EFEA", edgecolor="#C9C4BC",
                                           lw=0.7, zorder=1))
        n = min(n, len(nodes))
        for p0, p1 in tree_edges(nodes[:n], parent[:n]):
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#B6BCC4", lw=0.5, zorder=2)
        ax.plot([nd[0] for nd in nodes[:n]], [nd[1] for nd in nodes[:n]], ".",
                ms=1.5, color=fs.MUTED, zorder=3)
        if n >= first_sol:
            seg = path_at["first"]
            ax.plot([p[0] for p in seg], [p[1] for p in seg], color=fs.ACCENT, lw=1.4, zorder=5)
        ax.plot(*START, "o", ms=4, color=fs.GREEN, zorder=6)
        ax.plot(*GOAL, "o", ms=4, color=fs.PURPLE, zorder=6)
        ax.set_title(lab, fontsize=8.6, color=fs.INK, pad=3)
    fs.save(fig, "ch11", "fig11-02")


# ============================ 图 11-3 ============================
def fig_stack():
    fig, ax = fs.canvas(6.6, 3.6, xlim=(0, 10), ylim=(0, 8.0))
    rows = [
        ("任务层 · 符号", ["把「放进柜子」拆成有序动作", "开门 · 抓杯 · 移入 · 关门"],
         ["1 至 3 s 一次", "事件触发"], fs.PURPLE),
        ("运动层 · 几何", ["每个动作算一条关节轨迹", "采样规划或轨迹优化"],
         ["50 至 200 ms", "10 Hz 重规划"], fs.BLUE),
        ("控制层 · 力矩", ["把轨迹变成每毫秒的关节指令", "MPC 加伺服"],
         ["1 kHz", "跟踪误差闭环"], fs.TEAL),
    ]
    H = 1.05
    tops = [5.95, 4.10, 2.25]
    for i, (name, body, freq, col) in enumerate(rows):
        y = tops[i]
        fs.box(ax, 0.35, y, 2.15, H, name, fs=9.6, ec=col, fc="#FFFFFF", tc=col, weight="bold")
        fs.box(ax, 2.75, y, 4.05, H, chr(10).join(body), fs=8.2, ec="#C9D2DC", fc="#FFFFFF", lw=0.9)
        fs.box(ax, 7.05, y, 2.55, H, chr(10).join(freq), fs=8.4, ec="#C9D2DC", fc=fs.PAPER, lw=0.9)

    fs.label(ax, 1.42, 7.32, "层", fs=8.0, color=fs.MUTED)
    fs.label(ax, 4.77, 7.32, "这一层把输入变成什么", fs=8.0, color=fs.MUTED)
    fs.label(ax, 8.32, 7.32, "多久跑一次", fs=8.0, color=fs.MUTED)

    # 向下：子目标
    fs.arrow(ax, (4.95, 5.92), (4.95, 5.18), color=fs.MUTED, lw=1.1)
    fs.label(ax, 5.10, 5.55, "符号动作", fs=8.0, color=fs.MUTED, ha="left")
    fs.arrow(ax, (4.95, 4.07), (4.95, 3.33), color=fs.MUTED, lw=1.1)
    fs.label(ax, 5.10, 3.70, "关节轨迹", fs=8.0, color=fs.MUTED, ha="left")

    # 向上：失败回传
    fs.arrow(ax, (3.02, 5.18), (3.02, 5.92), color=fs.ACCENT, lw=1.0, ls=(0, (3, 2)))
    fs.label(ax, 3.18, 5.55, "几何不可行", fs=8.0, color=fs.ACCENT, ha="left")
    fs.arrow(ax, (3.02, 3.33), (3.02, 4.07), color=fs.ACCENT, lw=1.0, ls=(0, (3, 2)))
    fs.label(ax, 3.18, 3.70, "跟踪超差", fs=8.0, color=fs.ACCENT, ha="left")

    # 底部时间尺，按对数排
    ax.plot([0.55, 9.45], [1.30, 1.30], color=fs.FAINT, lw=1.0)
    for t in (0.001, 0.1, 1.0, 3.0):
        x = 0.55 + (np.log10(t) + 3) / (np.log10(3.0) + 3) * 8.90
        ax.plot([x, x], [1.25, 1.35], color=fs.FAINT, lw=1.0)
        lab = {0.001: "1 ms", 0.1: "100 ms", 1.0: "1 s", 3.0: "3 s"}[t]
        ax.text(x, 1.10, lab, ha="center", va="top", fontsize=8.0, color=fs.MUTED)
    ax.text(5.0, 0.52, "越往上越慢，越往上越需要搜", ha="center", va="center",
            fontsize=8.4, color=fs.MUTED)
    fs.save(fig, "ch11", "fig11-03")


if __name__ == "__main__":
    fig_cspace()
    fig_rrt()
    fig_stack()
