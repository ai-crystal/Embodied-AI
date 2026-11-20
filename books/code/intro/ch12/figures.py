# -*- coding: utf-8 -*-
"""第 12 章插图：SayCan 双重打分、VoxPoser 吸引与排斥场、三层接口与频率。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


def fig_saycan():
    """三条技能，合理性乘可行性。数值为算例。"""
    fig, ax = fs.canvas(6.7, 3.55)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.15)

    x_name = 0.30
    x_llm, s_llm = 3.34, 1.78
    x_aff, s_aff = 5.66, 1.04
    x_pro, s_pro = 7.52, 1.50

    # 列头
    ax.text(x_name, 4.94, "技能的语言描述", ha="left", va="center", fontsize=8.8, color=fs.INK)
    ax.text(x_llm, 4.94, "合理性  p(ℓ|i)", ha="left", va="center", fontsize=8.8, color=fs.BLUE)
    ax.text(x_aff, 4.94, "可行性  p(c|s,ℓ)", ha="left", va="center", fontsize=8.8, color=fs.GREEN)
    ax.text(x_pro + 0.04, 4.94, "乘积", ha="left", va="center", fontsize=8.8, color=fs.ACCENT)
    for x in (3.16, 5.50, 7.40):
        ax.plot([x, x], [1.30, 4.74], color=fs.GRID, lw=0.9, ls=(0, (3, 3)), zorder=1)

    rows = [
        ("找一块海绵", 0.61, 0.30),
        ("把海绵拿起来", 0.42, 0.05),
        ("走到桌子那边", 0.18, 0.90),
    ]
    y0, dy, h = 3.80, 1.02, 0.36
    for i, (name, pl, pc) in enumerate(rows):
        y = y0 - i * dy
        ym = y + h / 2
        ax.text(x_name, ym, name, ha="left", va="center", fontsize=9.2, color=fs.INK)

        ax.add_patch(plt.Rectangle((x_llm, y), s_llm, h, facecolor="#EEF2F6",
                                   edgecolor="none", zorder=2))
        ax.add_patch(plt.Rectangle((x_llm, y), s_llm * pl, h, facecolor=fs.BLUE,
                                   edgecolor="none", alpha=0.80, zorder=3))
        ax.text(x_llm + s_llm * pl + 0.09, ym, f"{pl:.2f}", ha="left", va="center",
                fontsize=8.6, color=fs.BLUE)

        ax.add_patch(plt.Rectangle((x_aff, y), s_aff, h, facecolor="#EEF2F6",
                                   edgecolor="none", zorder=2))
        ax.add_patch(plt.Rectangle((x_aff, y), s_aff * pc, h, facecolor=fs.GREEN,
                                   edgecolor="none", alpha=0.80, zorder=3))
        ax.text(x_aff + s_aff * pc + 0.08, ym, f"{pc:.2f}", ha="left", va="center",
                fontsize=8.6, color=fs.GREEN)

        prod = pl * pc
        ax.add_patch(plt.Rectangle((x_pro, y), s_pro, h, facecolor="#EEF2F6",
                                   edgecolor="none", zorder=2))
        ax.add_patch(plt.Rectangle((x_pro, y), s_pro * prod, h, facecolor=fs.ACCENT,
                                   edgecolor="none", alpha=0.85, zorder=3))
        ax.text(x_pro + s_pro * prod + 0.09, ym, f"{prod:.3f}", ha="left", va="center",
                fontsize=8.6, color=fs.ACCENT,
                weight="bold" if i == 0 else "normal")

    # 选中标记
    ax.add_patch(plt.Rectangle((x_pro - 0.10, y0 - 0.09), s_pro + 1.05, h + 0.18,
                               facecolor="none", edgecolor=fs.ACCENT, lw=1.1,
                               linestyle=(0, (4, 2)), zorder=6))
    ax.text(x_pro + s_pro + 0.10, y0 + h + 0.32, "这一轮选它", ha="left", va="center",
            fontsize=8.6, color=fs.ACCENT)

    ax.text(0.30, 1.00, "两列相乘而不是相加，相关性高但当下做不到的技能，乘积被压到 0 附近",
            ha="left", va="center", fontsize=8.6, color=fs.MUTED)
    ax.text(0.30, 0.50, "第一行与第三行只差 0.02，现场换一张桌子，胜负就可能反过来",
            ha="left", va="center", fontsize=8.6, color=fs.MUTED)
    fs.save(fig, "ch12", "fig12-01")


def fig_voxposer():
    """吸引场与排斥场合成，再用规划跟随。场形为高斯叠加，仅示意。"""
    g = np.linspace(0, 1, 180)
    X, Y = np.meshgrid(g, g)

    handle = (0.68, 0.42)
    vase = (0.30, 0.66)
    start = (0.13, 0.17)
    cup = (0.60, 0.50)

    def gauss(cx, cy, sx, sy, amp=1.0):
        return amp * np.exp(-(((X - cx) ** 2) / (2 * sx ** 2) + ((Y - cy) ** 2) / (2 * sy ** 2)))

    # 吸引场：杯柄附近正分最强，杯身给一点
    A = 1.00 * gauss(handle[0], handle[1], 0.052, 0.052)
    A += 0.30 * gauss(cup[0], cup[1], 0.10, 0.11)
    A = A / A.max()

    # 排斥场：花瓶周围与桌沿给负分，取绝对值画图
    R = -1.00 * gauss(vase[0], vase[1], 0.105, 0.105)
    R += -0.50 * gauss(0.50, 0.97, 0.55, 0.055)
    R = R / np.abs(R).max()
    V = 2.0 * A + R

    fig = plt.figure(figsize=(6.8, 2.95))
    axes = [fig.add_axes([0.015, 0.09, 0.305, 0.79]),
            fig.add_axes([0.345, 0.09, 0.305, 0.79]),
            fig.add_axes([0.675, 0.09, 0.305, 0.79])]
    panels = [(A, "Blues", 0.0, 1.0, "(a) 吸引场，越深越该靠近"),
              (-R, "Reds", 0.0, 1.0, "(b) 排斥场，越深越该避开"),
              (V, "RdYlBu", -1.0, 1.0, "(c) 合成价值图，蓝去红避")]

    for ax, (data, cmap, lo, hi, title) in zip(axes, panels):
        ax.imshow(data, origin="lower", extent=[0, 1, 0, 1], cmap=cmap,
                  interpolation="bilinear", zorder=1, alpha=0.95,
                  vmin=lo, vmax=hi)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        for s_ in ("top", "right", "left", "bottom"):
            ax.spines[s_].set_color(fs.FAINT)
            ax.spines[s_].set_linewidth(0.7)
        ax.set_xlabel(title, fontsize=8.8, color=fs.INK, labelpad=3)

    # 同一批物体，三张图位置一致
    for ax in axes:
        ax.scatter([cup[0]], [cup[1]], s=230, marker="o", facecolor="none",
                   edgecolor=fs.INK, lw=1.2, zorder=5)
        ax.scatter([vase[0]], [vase[1]], s=200, marker="s", facecolor="none",
                   edgecolor="#111827", lw=1.1, zorder=5)
        ax.scatter([start[0]], [start[1]], s=50, marker="o", color=fs.GOLD, zorder=6)

    boxes = dict(facecolor="white", edgecolor="none", alpha=0.82, pad=1.4)
    axes[0].annotate("杯柄", xy=(handle[0], handle[1]), xytext=(handle[0] + 0.02, handle[1] + 0.20),
                     fontsize=8.2, color=fs.INK, zorder=7, ha="center",
                     bbox=boxes, arrowprops=dict(arrowstyle="-", color=fs.INK, lw=0.7))
    axes[0].scatter([handle[0]], [handle[1]], s=26, marker="s", color=fs.ACCENT, zorder=8)
    axes[0].annotate("杯子", xy=(cup[0], cup[1]), xytext=(cup[0] + 0.10, cup[1] - 0.20),
                     fontsize=8.2, color=fs.INK, zorder=7, ha="center",
                     bbox=boxes, arrowprops=dict(arrowstyle="-", color=fs.INK, lw=0.7))
    axes[0].annotate("起始位姿", xy=(start[0], start[1]), xytext=(start[0] + 0.13, start[1] + 0.10),
                     fontsize=8.2, color=fs.INK, zorder=7, ha="center",
                     bbox=boxes, arrowprops=dict(arrowstyle="-", color=fs.INK, lw=0.7))

    axes[1].annotate("花瓶", xy=(vase[0], vase[1]), xytext=(vase[0] + 0.16, vase[1] + 0.20),
                     fontsize=8.2, color=fs.INK, zorder=7, ha="center",
                     bbox=boxes, arrowprops=dict(arrowstyle="-", color=fs.INK, lw=0.7))
    axes[1].annotate("桌沿", xy=(0.80, 0.955), xytext=(0.62, 0.80),
                     fontsize=8.2, color=fs.INK, zorder=7, ha="center",
                     bbox=boxes, arrowprops=dict(arrowstyle="-", color=fs.INK, lw=0.7))

    # (c) 规划出的末端轨迹，从下方绕过杯子
    t = np.linspace(0, 1, 160)
    px = start[0] + (handle[0] - start[0]) * t
    py = start[1] + (handle[1] - start[1]) * t - 0.13 * np.sin(np.pi * t)
    axes[2].plot(px, py, color=fs.INK, lw=1.5, zorder=8, solid_capstyle="round")
    fs.arrow(axes[2], (px[-8], py[-8]), (handle[0] - 0.005, handle[1]), color=fs.INK, lw=1.3, z=9)
    axes[2].text(0.52, 0.92, "黑线为末端轨迹", fontsize=8.2, color=fs.INK, zorder=9, bbox=boxes)

    fig.text(0.5, 0.012, "两张图按 2 比 1 加权相加得到价值图，规划器最小化它的负值（场形为示意）",
             ha="center", va="center", fontsize=8.4, color=fs.MUTED)
    fs.save(fig, "ch12", "fig12-02")


def fig_layers():
    """三层接口与各自的时间尺度。"""
    fig, ax = fs.canvas(6.8, 3.20)
    ax.set_xlim(0, 10)
    ax.set_ylim(0.55, 5.35)

    t0, t1 = 2.52, 5.72
    span = t1 - t0
    tx = lambda sec: t0 + span * sec / 2.0

    lanes = [(4.50, "语言层", "一次决策 1 至 3 s", fs.PURPLE),
             (3.32, "技能层", "10 Hz，100 ms 一步", fs.TEAL),
             (2.09, "控制层", "1 kHz，1 ms 一次", fs.BLUE)]
    for yc, name, spec, color in lanes:
        ax.text(0.14, yc + 0.19, name, ha="left", va="center", fontsize=9.2,
                color=color, weight="bold")
        ax.text(0.14, yc - 0.16, spec, ha="left", va="center", fontsize=8.0, color=fs.MUTED)

    # 时间轴
    ax.plot([t0, t1], [1.62, 1.62], color=fs.INK, lw=1.0, zorder=2)
    for sec in (0.0, 0.5, 1.0, 1.5, 2.0):
        ax.plot([tx(sec), tx(sec)], [1.53, 1.71], color=fs.INK, lw=1.0, zorder=2)
        ax.text(tx(sec), 1.36, f"{sec:g} s", ha="center", va="top", fontsize=8.0, color=fs.MUTED)

    # 语言层：一次推理 1.2 s，再下一次
    ax.add_patch(plt.Rectangle((tx(0), 4.30), tx(1.2) - tx(0), 0.40, facecolor="#EFE9FB",
                               edgecolor=fs.PURPLE, lw=1.0, zorder=3))
    ax.text((tx(0) + tx(1.2)) / 2, 4.50, "一次推理 1.2 s", ha="center", va="center",
            fontsize=8.2, color=fs.PURPLE, zorder=4)
    ax.add_patch(plt.Rectangle((tx(1.2), 4.30), tx(2.0) - tx(1.2), 0.40, facecolor="#F7F4FD",
                               edgecolor=fs.PURPLE, lw=0.9, ls=(0, (3, 2)), zorder=3))
    ax.text((tx(1.2) + tx(2.0)) / 2, 4.50, "下一次", ha="center", va="center",
            fontsize=8.2, color=fs.PURPLE, zorder=4)

    # 技能层：每 100 ms 一格
    for k in range(21):
        w = (tx(0.1) - tx(0.0)) * 0.80
        ax.add_patch(plt.Rectangle((tx(k * 0.1), 3.15), w, 0.34,
                                   facecolor="#D9F0EC" if k % 2 == 0 else "#F4FBF9",
                                   edgecolor=fs.TEAL, lw=0.7, zorder=3))

    # 控制层：每 5 ms 一根
    for sec in np.arange(0, 2.0005, 0.005):
        ax.plot([tx(sec), tx(sec)], [1.90, 2.28], color=fs.BLUE, lw=0.4, alpha=0.42, zorder=3)

    # 竖向对齐线
    for sec in (0.0, 1.2):
        ax.plot([tx(sec), tx(sec)], [1.88, 4.72], color=fs.FAINT, lw=0.8,
                ls=(0, (2, 3)), zorder=2)

    ax.text(t0, 2.52, "每 100 ms 发一步，判一次成败", ha="left", va="center",
            fontsize=8.0, color=fs.MUTED,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2), zorder=6)
    ax.text(t0, 0.78, "控制层每 1 ms 闭环一次，图上按 5 ms 画一根", ha="left", va="center",
            fontsize=8.0, color=fs.MUTED)

    # 右侧：技能描述五项
    bx, by, bw, bh = 6.10, 1.10, 3.72, 4.00
    ax.add_patch(plt.Rectangle((bx, by), bw, bh, facecolor=fs.PAPER,
                               edgecolor=fs.FAINT, lw=0.9, zorder=2))
    ax.text(bx + 0.16, by + bh - 0.30, "一条技能要写全的五项", ha="left", va="center",
            fontsize=8.8, color=fs.INK, zorder=3)
    items = [("技能名", "固定词表里挑"),
             ("参数", "带单位与上下限"),
             ("前置条件", "不满足就不许调"),
             ("后置条件", "完成后再查一遍"),
             ("失败码", "滑脱、超时、被挡")]
    for i, (k, v) in enumerate(items):
        y = by + bh - 0.76 - i * 0.66
        ax.text(bx + 0.16, y, k, ha="left", va="center", fontsize=8.0,
                color=fs.ACCENT, weight="bold", zorder=3)
        ax.text(bx + 1.12, y, v, ha="left", va="center", fontsize=8.0,
                color=fs.MUTED, zorder=3)

    fs.save(fig, "ch12", "fig12-03")


if __name__ == "__main__":
    fig_saycan()
    fig_voxposer()
    fig_layers()
