# -*- coding: utf-8 -*-
"""第 8 章插图：协变量偏移、动作块的两种执行方式、遥操作采集链路。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
import figstyle as fs


def _bezier(p0, p1, p2, p3, n=260):
    t = np.linspace(0, 1, n)[:, None]
    p = ((1 - t) ** 3) * np.array(p0) + 3 * ((1 - t) ** 2) * t * np.array(p1) \
        + 3 * (1 - t) * (t ** 2) * np.array(p2) + (t ** 3) * np.array(p3)
    return p[:, 0], p[:, 1]


def fig_covariate_shift():
    """(a) 俯视图上专家轨迹与策略轨迹分开；(b) 偏差随执行时间的量级。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.15),
                             gridspec_kw=dict(width_ratios=[1.08, 1.0], wspace=0.28))

    # ---------------- (a) 俯视图 ----------------
    ax = axes[0]
    ax.set_xlim(0, 8.0)
    ax.set_ylim(0, 5.95)
    ax.axis("off")
    ax.text(0.05, 5.72, "(a)", fontsize=9.0, color=fs.INK, weight="bold", va="top")

    ax.add_patch(Rectangle((0.30, 0.45), 7.35, 5.10, facecolor=fs.PAPER,
                           edgecolor="#D9CDBB", lw=1.0, zorder=0))

    ax.add_patch(Ellipse((1.45, 2.35), 0.58, 0.46, facecolor="#FFFFFF",
                         edgecolor=fs.MUTED, lw=1.0, zorder=4))
    fs.label(ax, 1.45, 1.94, "杯子", fs=8.0, color=fs.MUTED, va="top")

    ax.add_patch(Ellipse((6.55, 4.30), 1.16, 0.92, facecolor="#FFFFFF",
                         edgecolor=fs.MUTED, lw=1.0, zorder=4))
    ax.add_patch(Ellipse((6.55, 4.30), 0.70, 0.54, facecolor="none",
                         edgecolor=fs.FAINT, lw=0.8, zorder=4))
    fs.label(ax, 6.55, 4.30, "盘子", fs=8.0, color=fs.MUTED)

    ax.add_patch(Rectangle((6.44, 1.10), 1.14, 0.60, facecolor="#FFFFFF",
                           edgecolor=fs.MUTED, lw=1.0, zorder=4))
    fs.label(ax, 7.01, 1.40, "纸巾盒", fs=8.0, color=fs.MUTED)

    # 专家轨迹与训练数据覆盖的容差带
    ex, ey = _bezier((1.45, 2.35), (2.35, 3.95), (4.55, 4.95), (6.45, 4.32))
    d = np.gradient(np.stack([ex, ey], axis=1), axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], axis=1)
    nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9)
    band = 0.17
    ax.fill(np.concatenate([ex + nrm[:, 0] * band, (ex - nrm[:, 0] * band)[::-1]]),
            np.concatenate([ey + nrm[:, 1] * band, (ey - nrm[:, 1] * band)[::-1]]),
            facecolor=fs.GREEN, alpha=0.13, edgecolor="none", zorder=1)
    ax.plot(ex, ey, color=fs.GREEN, lw=2.0, zorder=3, solid_capstyle="round")
    fs.label(ax, 0.52, 5.22, "专家走过的路", fs=8.4, color=fs.GREEN, ha="left")
    fs.label(ax, 0.52, 4.90, "绿带是训练数据覆盖到的状态", fs=8.0, color=fs.GREEN, ha="left")

    # 策略自己走出来的轨迹
    px, py = _bezier((1.45, 2.35), (2.55, 2.05), (3.95, 1.62), (7.18, 1.44))
    ax.plot(px, py, color=fs.ACCENT, lw=2.0, ls=(0, (5, 2)), zorder=3)
    fs.label(ax, 2.85, 1.10, "策略自己走出来的路", fs=8.2, color=fs.ACCENT)

    for frac, tag, dx, dy, ha in ((0.17, "1 s", 0.16, 0.14, "left"),
                                  (0.45, "3 s", 0.10, 0.20, "left"),
                                  (0.78, "6 s", -0.20, 0.18, "left")):
        i = int(frac * (len(px) - 1))
        ax.plot([px[i]], [py[i]], "o", ms=3.4, color=fs.ACCENT, zorder=6)
        fs.label(ax, px[i] + dx, py[i] + dy, tag, fs=8.0, color=fs.MUTED,
                 ha=ha, va="bottom" if dy > 0 else "top")

    ax.annotate("这一段的画面\n训练时从没出现过", xy=(4.88, 1.72), xytext=(4.30, 2.95),
                fontsize=7.8, color=fs.INK, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=0.8,
                                shrinkA=2, shrinkB=2))

    # ---------------- (b) 偏差曲线 ----------------
    ax = axes[1]
    ax.set_xlim(-0.35, 7.6)
    ax.set_ylim(0, 14.8)
    fs.clean(ax, grid=True, spines=("left", "bottom"))
    ax.set_xticks([0, 2, 4, 6])
    ax.set_yticks([0, 4, 8, 12])
    ax.set_xlabel("执行时间（秒）", fontsize=9.0)
    ax.set_ylabel("与专家轨迹的偏差（厘米）", fontsize=9.0)

    anchors_t = np.array([0.0, 0.6, 1.2, 2.2, 3.2, 4.6, 6.4, 7.2])
    anchors_e = np.array([0.25, 0.55, 1.0, 2.7, 5.0, 8.6, 12.0, 13.6])
    tt = np.linspace(0, 7.2, 260)
    ee = 10 ** np.interp(tt, anchors_t, np.log10(anchors_e))
    ax.axhspan(0, 3, color=fs.GREEN, alpha=0.10, zorder=0)
    ax.axhspan(3, 14.8, color=fs.ACCENT, alpha=0.05, zorder=0)
    ax.plot(tt, ee, color=fs.ACCENT, lw=2.0, zorder=3)

    for t0, e0, txt, dx, dy in ((1.2, 1.0, "1 cm", -0.15, 1.6),
                                (3.2, 5.0, "5 cm", -0.15, 1.7),
                                (6.4, 12.0, "12 cm", -0.20, 1.5)):
        ax.plot([t0], [e0], "o", ms=4.2, color=fs.ACCENT, zorder=4)
        ax.plot([0, t0], [e0, e0], color=fs.FAINT, lw=0.7, ls=(0, (3, 2)), zorder=2)
        ax.plot([t0, t0], [0, e0], color=fs.FAINT, lw=0.7, ls=(0, (3, 2)), zorder=2)
        ax.annotate(txt, xy=(t0, e0), xytext=(t0 + dx, e0 + dy), fontsize=8.2,
                    color=fs.INK, ha="right", va="center")

    fs.label(ax, 5.35, 1.55, "还在训练分布里\n能纠回来", fs=8.0, color=fs.GREEN)
    fs.label(ax, 1.30, 9.90, "越来越像瞎猜", fs=8.0, color=fs.ACCENT)
    ax.text(-0.28, 14.1, "(b)", fontsize=9.0, color=fs.INK, weight="bold")

    fs.save(fig, "ch08", "fig08-01")


def fig_action_chunk():
    """(a) 整块执行；(b) 时间集成。横轴统一为 16 个时间步。"""
    fig, ax = fs.canvas(6.6, 3.9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.2)

    x0, x1 = 0.95, 9.10
    step = (x1 - x0) / 16.0

    def xt(i):
        return x0 + i * step

    for i in range(0, 17, 4):
        ax.plot([xt(i), xt(i)], [0.82, 5.95], color=fs.GRID, lw=0.7, zorder=0)
        ax.text(xt(i), 0.60, str(i), ha="center", va="top", fontsize=8.0, color=fs.MUTED)

    ax.plot([x0, x1], [0.82, 0.82], color=fs.MUTED, lw=0.9, zorder=1)
    fs.label(ax, 9.38, 0.60, "时间步", fs=8.0, color=fs.MUTED, ha="left", va="top")

    # ---------------- (a) 整块执行 ----------------
    ax.text(0.55, 6.92, "(a) 整块执行", fontsize=9.4, color=fs.INK, weight="bold")
    y_a, h = 5.30, 0.56
    for s, lab in ((0, "第 1 块，8 步"), (8, "第 2 块，8 步")):
        fs.box(ax, xt(s) + 0.02, y_a, step * 8 - 0.04, h, lab, fs=8.4,
               ec=fs.BLUE, fc="#EEF3FB", lw=1.0)
    for s in (0, 8):
        ax.plot([xt(s)], [y_a + h + 0.06], marker="v", ms=4.2, color=fs.BLUE, zorder=5)
        fs.label(ax, xt(s) + 0.10, y_a + h + 0.22, "看一眼", fs=8.0, color=fs.BLUE, ha="left")
    fs.label(ax, xt(4.6), 4.92, "这 8 步里不回头，中途发生什么都要等它走完",
             fs=8.2, color=fs.MUTED)

    # ---------------- (b) 时间集成 ----------------
    ax.text(0.55, 4.42, "(b) 时间集成", fontsize=9.4, color=fs.INK, weight="bold")
    y_b, n, hb = 1.48, 5, 0.34
    for i in range(n):
        s = xt(i)
        fs.box(ax, s + 0.02, y_b + i * hb, step * 8 - 0.04, hb - 0.05, "", fs=8.0,
               ec=fs.PURPLE, fc=fs.PURPLE, lw=0.9, alpha=0.20 + 0.14 * i, z=3 + i)
    top = y_b + (n - 1) * hb
    fs.label(ax, xt(4) + 2.00, top + hb / 2 - 0.03, "8 步", fs=8.0, color="#FFFFFF")

    t_now = xt(4)
    ax.plot([t_now, t_now], [y_b - 0.06, top + hb - 0.02], color=fs.ACCENT,
            lw=1.2, ls=(0, (4, 2)), zorder=9)
    fs.label(ax, xt(4.7), 3.42, "此刻有 5 个预测重叠，按 exp(-m·i) 加权平均，越新权重越大",
             fs=8.2, color=fs.INK)
    fs.label(ax, xt(4.4), 1.10, "每走一步都推理一次，动作跟得上观测，代价是推理次数多 8 倍",
             fs=8.2, color=fs.MUTED)

    fs.save(fig, "ch08", "fig08-02")


def fig_teleop_chain():
    """遥操作采集链路：人 → 主手 → 从手 → 桌面，传感器与时间戳汇入数据集。"""
    fig, ax = fs.canvas(6.6, 3.8)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.3)

    W, H, Y = 1.88, 1.12, 3.30
    xs = [0.22, 2.46, 4.70, 6.94]
    heads = [("人", "看着画面动手", fs.PAPER),
             ("主手", "被推动，读角度", "#FFFFFF"),
             ("从手", "同步复现动作", "#FFFFFF"),
             ("桌面", "杯子与盘子", "#FFFFFF")]
    for x, (t, s, fc) in zip(xs, heads):
        fs.box(ax, x, Y, W, H, "", fc=fc, ec=fs.INK, lw=1.1)
        fs.label(ax, x + W / 2, Y + H - 0.30, t, fs=9.6, color=fs.INK, weight="bold")
        fs.label(ax, x + W / 2, Y + 0.36, s, fs=8.0, color=fs.MUTED)

    for i in range(3):
        fs.arrow(ax, (xs[i] + W + 0.03, Y + H / 2), (xs[i + 1] - 0.03, Y + H / 2),
                 color=fs.MUTED if i < 2 else fs.ACCENT, lw=1.2)

    # 反馈弧：画面与力感回到人
    ax.annotate("", xy=(xs[0] + W / 2, Y + H + 0.05), xytext=(xs[3] + W / 2, Y + H + 0.05),
                arrowprops=dict(arrowstyle="-|>", color=fs.BLUE, lw=1.1,
                                connectionstyle="arc3,rad=0.22",
                                shrinkA=2, shrinkB=2))
    fs.label(ax, (xs[0] + xs[3] + W) / 2, 5.62, "画面与力感", fs=8.4, color=fs.BLUE)

    # 第二层：两路传感器
    fs.box(ax, 4.52, 1.86, 2.24, 0.94, "", fc="#FFFFFF", ec=fs.GREEN, lw=1.0)
    fs.label(ax, 5.64, 2.52, "编码器 50 Hz", fs=8.6, color=fs.GREEN)
    fs.label(ax, 5.64, 2.16, "关节角 + 夹爪宽度", fs=8.0, color=fs.MUTED)

    fs.box(ax, 6.88, 1.86, 2.24, 0.94, "", fc="#FFFFFF", ec=fs.BLUE, lw=1.0)
    fs.label(ax, 8.00, 2.52, "腕部相机 30 fps", fs=8.6, color=fs.BLUE)
    fs.label(ax, 8.00, 2.16, "640 × 480 彩色图", fs=8.0, color=fs.MUTED)

    fs.arrow(ax, (5.64, Y - 0.03), (5.64, 2.82), color=fs.GREEN, lw=1.0)
    fs.arrow(ax, (8.00, Y - 0.03), (8.00, 2.82), color=fs.BLUE, lw=1.0)
    fs.label(ax, 5.50, 3.06, "读数", fs=8.0, color=fs.GREEN, ha="right")
    fs.label(ax, 8.14, 3.06, "图像", fs=8.0, color=fs.BLUE, ha="left")

    # 第三层：数据集
    fs.box(ax, 1.05, 0.18, 8.05, 1.22, "", fc="#FDF1E6", ec=fs.ACCENT, lw=1.2)
    fs.label(ax, 5.08, 1.08, "一条示教", fs=9.4, color=fs.ACCENT, weight="bold")
    fs.label(ax, 5.08, 0.74, "600 张图 + 1000 个关节点 + 夹爪开合 + 时间戳", fs=8.2, color=fs.INK)
    fs.label(ax, 5.08, 0.40, "两路频率不同，靠时间戳对齐，最坏差半帧 17 ms", fs=8.0, color=fs.MUTED)

    fs.arrow(ax, (5.64, 1.82), (5.64, 1.42), color=fs.MUTED, lw=1.0)
    fs.arrow(ax, (8.00, 1.82), (8.00, 1.42), color=fs.MUTED, lw=1.0)

    fs.save(fig, "ch08", "fig08-03")


if __name__ == "__main__":
    fig_covariate_shift()
    fig_action_chunk()
    fig_teleop_chain()
