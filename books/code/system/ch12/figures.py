# -*- coding: utf-8 -*-
"""第 12 章插图：SayCan 双重打分、VoxPoser 价值场叠加、分层接口。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_saycan():
    """三条候选技能的双重打分：可行性、合理性、乘积。"""
    skills = ["找一个海绵", "拿起海绵", "去垃圾桶"]
    afford = [0.86, 0.42, 0.95]     # p(c|s)：技能在当前状态下能成功的概率
    reason = [0.42, 0.35, 0.03]     # p(l|i)：语言模型认为这步有助于完成指令的概率
    prod = [a * b for a, b in zip(afford, reason)]
    order = np.argsort(prod)[::-1]
    rank = {idx: r + 1 for r, idx in enumerate(order)}

    fig, ax = plt.subplots(figsize=(6.6, 2.95))
    ypos = np.arange(len(skills))[::-1]
    h = 0.30

    for i, y in enumerate(ypos):
        ax.barh(y + 0.185, afford[i], height=h, color="#CFDEF0",
                edgecolor=fs.BLUE, lw=1.0, zorder=3)
        ax.barh(y - 0.185, reason[i], height=h, color="#F3D6C8",
                edgecolor=fs.ACCENT, lw=1.0, zorder=3)
        ax.text(afford[i] + 0.015, y + 0.185, f"{afford[i]:.2f}",
                va="center", ha="left", fontsize=8.2, color=fs.BLUE)
        ax.text(reason[i] + 0.015, y - 0.185, f"{reason[i]:.2f}",
                va="center", ha="left", fontsize=8.2, color=fs.ACCENT)
        ax.text(1.10, y, f"{rank[i]}", va="center", ha="center", fontsize=9.5,
                color=fs.INK, weight="bold")
        ax.text(1.16, y, f"{prod[i]:.2f}", va="center", ha="left", fontsize=9.5,
                color=fs.ACCENT if rank[i] == 1 else fs.MUTED,
                weight="bold" if rank[i] == 1 else "normal")

    ax.set_yticks(ypos)
    ax.set_yticklabels(skills, fontsize=9.5)
    ax.set_xlim(0, 1.30)
    ax.set_ylim(-0.62, len(skills) - 0.38)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("概率", fontsize=9)
    fs.clean(ax, grid=True, spines=("bottom",))

    ax.text(1.10, len(skills) - 0.52, "排序  乘积", ha="center", va="bottom",
            fontsize=8.4, color=fs.MUTED)
    ax.plot([1.055, 1.055], [-0.50, len(skills) - 0.55], color=fs.GRID, lw=1.0, zorder=1)

    handles = [plt.Rectangle((0, 0), 0.1, 0.1, facecolor="#CFDEF0", edgecolor=fs.BLUE, lw=1.0),
               plt.Rectangle((0, 0), 0.1, 0.1, facecolor="#F3D6C8", edgecolor=fs.ACCENT, lw=1.0)]
    ax.legend(handles, ["可行性 p(c|s)", "合理性 p(l|i)"], loc="lower left",
              bbox_to_anchor=(0.0, 1.01), ncol=2, fontsize=8.6,
              handlelength=1.2, handleheight=0.9, columnspacing=1.4)
    ax.text(0.5, -0.37, "乘积 = 可行性 × 合理性，逐步取乘积最大的技能执行",
            transform=ax.transAxes, ha="center", va="top", fontsize=8.6, color=fs.MUTED)
    fig.subplots_adjust(left=0.16, right=0.99, top=0.84, bottom=0.30)
    fs.save(fig, "ch12", "fig12-01")


def _fields(n=240):
    x = np.linspace(0, 1, n)
    X, Y = np.meshgrid(x, x)
    hx, hy, sa = 0.74, 0.66, 0.085          # 把手位置与吸引场宽度
    vx, vy, rv = 0.46, 0.44, 0.17           # 花瓶位置与排斥半径
    d_h = np.hypot(X - hx, Y - hy)
    d_v = np.hypot(X - vx, Y - vy)
    att = np.exp(-d_h ** 2 / (2 * sa ** 2))
    rep = np.clip(1 - d_v / rv, 0, 1)
    V = 2.0 * att - 1.0 * rep
    return X, Y, att, rep, V, (hx, hy), (vx, vy), rv


def _grad(X, Y, att, rep, hx, hy, sa, vx, vy, rv):
    d_v = np.maximum(np.hypot(X - vx, Y - vy), 1e-6)
    ga_x = -att * (X - hx) / sa ** 2
    ga_y = -att * (Y - hy) / sa ** 2
    gr_x = (X - vx) / (d_v * rv)
    gr_y = (Y - vy) / (d_v * rv)
    inside = (d_v < rv).astype(float)
    return 2.0 * ga_x - gr_x * inside, 2.0 * ga_y - gr_y * inside


def _plan_path(att, rep, start, goal):
    """在代价图上做 8 邻域最短路，代价 = 1 + 12*排斥 + 0.5*(1-吸引)。"""
    import heapq
    n = att.shape[0]
    cost = 1.0 + 12.0 * rep + 0.5 * (1.0 - att)
    si = (int(round(start[1] * (n - 1))), int(round(start[0] * (n - 1))))
    gi = (int(round(goal[1] * (n - 1))), int(round(goal[0] * (n - 1))))
    dist = np.full((n, n), np.inf)
    prev = np.full((n, n, 2), -1, dtype=int)
    dist[si] = 0.0
    pq = [(0.0, si)]
    steps = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while pq:
        d, (r, c) = heapq.heappop(pq)
        if d > dist[r, c]:
            continue
        if (r, c) == gi:
            break
        for dr, dc in steps:
            rr, cc = r + dr, c + dc
            if 0 <= rr < n and 0 <= cc < n:
                nd = d + 0.5 * (cost[r, c] + cost[rr, cc]) * (np.hypot(dr, dc))
                if nd < dist[rr, cc]:
                    dist[rr, cc] = nd
                    prev[rr, cc] = (r, c)
                    heapq.heappush(pq, (nd, (rr, cc)))
    path = [gi]
    while path[-1] != si:
        r, c = path[-1]
        path.append(tuple(prev[r, c]))
    path = np.array(path[::-1], float) / (n - 1)
    # 平滑
    k = 9
    pad = np.vstack([np.repeat(path[:1], k, 0), path, np.repeat(path[-1:], k, 0)])
    sm = np.vstack([np.convolve(pad[:, 0], np.ones(2 * k + 1) / (2 * k + 1), "valid"),
                    np.convolve(pad[:, 1], np.ones(2 * k + 1) / (2 * k + 1), "valid")]).T
    return sm[::4]


def fig_voxposer():
    """吸引场、排斥场与合成场，合成场上的梯度上升路径。"""
    X, Y, att, rep, V, (hx, hy), (vx, vy), rv = _fields()
    extent = [0, 1, 0, 1]

    fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.62))
    titles = ["(a) 吸引场", "(b) 排斥场", "(c) 合成场与路径"]
    cmaps = ["Blues", "Oranges", "RdYlBu_r"]
    for ax, t, cm, field in zip(axes, titles, cmaps, [att, rep, V]):
        im = ax.imshow(field, extent=extent, origin="lower", cmap=cm,
                       vmin=float(field.min()), vmax=float(field.max()), zorder=1)
        ax.contour(X, Y, field, levels=5, colors="white", linewidths=0.5, alpha=0.75, zorder=2)
        ax.set_title(t, fontsize=9.2, color=fs.INK, pad=5)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([0, 0.5, 1.0]); ax.set_yticks([0, 0.5, 1.0])
        ax.tick_params(labelsize=7.6, length=2)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        cb = fig.colorbar(im, ax=ax, fraction=0.042, pad=0.02)
        cb.ax.tick_params(labelsize=7.2, length=2)
        cb.outline.set_linewidth(0.5)

    # (a) 目标与起点
    axes[0].plot([hx], [hy], marker="*", ms=11, color=fs.ACCENT, zorder=6)
    axes[0].text(hx - 0.05, hy + 0.09, "把手", fontsize=8.2, color=fs.ACCENT,
                 ha="right", va="bottom", zorder=6)
    axes[0].plot([0.16], [0.20], marker="o", ms=5.5, mfc="white", mec=fs.INK, mew=1.0, zorder=6)
    axes[0].text(0.16, 0.10, "起点", fontsize=8.2, color=fs.INK, ha="center", va="top", zorder=6)

    # (b) 障碍
    axes[1].add_patch(plt.Circle((vx, vy), 0.045, facecolor="#D6D3D1", edgecolor=fs.INK,
                                 lw=0.9, zorder=6))
    axes[1].text(vx + 0.06, vy + 0.07, "花瓶", fontsize=8.2, color=fs.INK, zorder=6)
    axes[1].text(0.06, 0.90, "越近代价越高", fontsize=8.0, color="#7C2D12",
                 ha="left", va="center", zorder=6)

    # (c) 在合成代价图上的轨迹
    path = _plan_path(att, rep, (0.16, 0.20), (hx, hy))
    axes[2].plot(path[:, 0], path[:, 1], color=fs.PINK, lw=1.6, zorder=7, solid_capstyle="round")
    k = int(len(path) * 0.45)
    axes[2].annotate("", xy=(path[k + 3, 0], path[k + 3, 1]),
                     xytext=(path[k, 0], path[k, 1]),
                     arrowprops=dict(arrowstyle="-|>", color=fs.PINK, lw=1.6,
                                     mutation_scale=11), zorder=9)
    axes[2].plot([hx], [hy], marker="*", ms=11, color=fs.ACCENT, zorder=8)
    axes[2].plot([path[0, 0]], [path[0, 1]], marker="o", ms=5.5, mfc="white", mec=fs.INK,
                 mew=1.0, zorder=8)
    axes[2].add_patch(plt.Circle((vx, vy), 0.045, facecolor="#D6D3D1", edgecolor=fs.INK,
                                 lw=0.9, zorder=6))
    axes[2].text(0.05, 0.90, "路径绕开高处", fontsize=8.0, color=fs.PINK,
                 ha="left", va="center", zorder=9)

    fig.subplots_adjust(left=0.045, right=0.975, top=0.88, bottom=0.06, wspace=0.42)
    fs.save(fig, "ch12", "fig12-02")


def fig_interface():
    """LLM 层 / 技能层 / 控制层之间的下发与回传。"""
    fig, ax = fs.canvas(6.6, 4.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.8)

    bands = [
        (5.10, "语言层", "读指令与失败报告，选下一项技能", "1–3 s 一次", "#F5EFE6", fs.ACCENT),
        (3.10, "技能层", "查前置条件，生成并监控轨迹", "10 Hz 监控", "#EDF1F7", fs.BLUE),
        (1.10, "控制层", "跟踪关节轨迹，闭环力与位置", "1 kHz", "#EAF2EF", fs.GREEN),
    ]
    x0, w, h = 0.55, 6.15, 1.05
    for y, name, detail, freq, fc, ec in bands:
        fs.box(ax, x0, y, w, h, "", fc=fc, ec=ec, lw=1.1)
        ax.text(x0 + 0.18, y + h * 0.66, name, ha="left", va="center",
                fontsize=9.8, color=fs.INK, weight="bold", zorder=5)
        ax.text(x0 + 1.55, y + h * 0.66, detail, ha="left", va="center",
                fontsize=8.6, color=fs.MUTED, zorder=5)
        ax.text(x0 + w - 0.16, y + h * 0.30, freq, ha="right", va="center",
                fontsize=8.4, color=fs.GOLD, zorder=5)

    # 层间：左侧向下（下发），右侧向上（回传）
    xd, xu = 1.35, 4.55
    pairs = [
        (5.10, 4.15, "技能名 + 参数", "失败码 + 现场快照"),
        (3.10, 2.15, "目标位姿 / 轨迹", "跟踪误差 / 力 / 到达"),
    ]
    for y_hi, y_lo, down_t, up_t in pairs:
        fs.arrow(ax, (xd, y_hi), (xd, y_lo), color=fs.ACCENT, lw=1.3, ms=9, z=4)
        ax.text(xd + 0.13, (y_hi + y_lo) / 2, down_t, ha="left", va="center",
                fontsize=8.5, color=fs.ACCENT, zorder=5)
        fs.arrow(ax, (xu, y_lo), (xu, y_hi), color=fs.BLUE, lw=1.3, ms=9, z=4)
        ax.text(xu + 0.13, (y_hi + y_lo) / 2, up_t, ha="left", va="center",
                fontsize=8.5, color=fs.BLUE, zorder=5)

    # 右侧：抽象/物理方向
    fs.arrow(ax, (9.30, 1.25), (9.30, 5.95), color=fs.FAINT, lw=1.0, ms=9, z=2)
    ax.text(9.30, 6.12, "抽象", ha="center", va="bottom", fontsize=8.2, color=fs.FAINT)
    ax.text(9.30, 1.08, "物理", ha="center", va="top", fontsize=8.2, color=fs.FAINT)

    # 图例：下发与回传
    fs.arrow(ax, (7.05, 3.98), (7.05, 3.56), color=fs.ACCENT, lw=1.3, ms=9, z=4)
    ax.text(7.20, 3.77, "向下　目标与调用", ha="left", va="center", fontsize=8.4, color=fs.ACCENT)
    fs.arrow(ax, (7.05, 2.88), (7.05, 3.30), color=fs.BLUE, lw=1.3, ms=9, z=4)
    ax.text(7.20, 3.09, "向上　结果与失败", ha="left", va="center", fontsize=8.4, color=fs.BLUE)

    ax.text(x0, 0.55, "护栏　整条计划最多 30 步；同一 (技能, 参数) 连续失败 2 次即禁用；"
                      "每 3 步必须有一条后置条件变真。",
            ha="left", va="center", fontsize=8.5, color=fs.MUTED)
    fs.save(fig, "ch12", "fig12-03")


if __name__ == "__main__":
    fig_saycan()
    fig_voxposer()
    fig_interface()
