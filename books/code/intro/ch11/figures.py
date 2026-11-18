# -*- coding: utf-8 -*-
"""第 11 章插图：VLA 总体架构、四种动作头、三条时间轴。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import figstyle as fs


def fig_arch():
    """图像 + 指令 -> 主干 -> 动作专家 -> 动作块 -> 控制器，下方是缓冲。"""
    fig, ax = fs.canvas(6.6, 4.36)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)

    # 指令
    fs.box(ax, 0.15, 5.85, 2.05, 0.60, "一句话指令", fs=8.8, ec=fs.MUTED, fc="#FFFFFF")
    fs.arrow(ax, (1.75, 5.82), (2.95, 5.34), color=fs.MUTED)

    # 主链
    fs.box(ax, 0.15, 3.85, 1.75, 1.45, "图像\n腕部相机\n30 Hz", fs=8.8, ec=fs.MUTED, fc="#FFFFFF")
    fs.box(ax, 2.35, 3.85, 2.05, 1.45, "视觉-语言主干\n7B 参数\n每帧一次", fs=8.8, ec=fs.BLUE, fc="#EEF3FB")
    fs.box(ax, 4.75, 3.85, 1.90, 1.45, "动作专家\n流匹配 10 步\n300M", fs=8.8, ec=fs.ACCENT, fc="#FDF1E6")
    fs.box(ax, 6.95, 3.85, 1.55, 1.45, "动作块\n25 步 0.5 s\n50 Hz", fs=8.4, ec=fs.GREEN, fc="#ECF6F1")
    fs.box(ax, 8.80, 3.85, 1.05, 1.45, "控制器\n1 kHz", fs=8.8, ec=fs.PURPLE, fc="#F3EFFC")

    for x0, x1 in ((1.92, 2.33), (4.42, 4.73), (6.67, 6.93), (8.52, 8.78)):
        fs.arrow(ax, (x0, 4.575), (x1, 4.575), color=fs.INK)

    # 推理频率括线
    ax.annotate("", xy=(2.40, 3.56), xytext=(6.62, 3.56),
                arrowprops=dict(arrowstyle="<->", color=fs.FAINT, lw=0.9))
    fs.label(ax, 4.51, 3.40, "这两段一次 3 到 10 Hz", fs=8.4, color=fs.MUTED, va="top")

    # 缓冲容器
    cont = FancyBboxPatch((0.15, 0.62), 9.70, 2.33,
                          boxstyle="round,pad=0.006,rounding_size=0.06",
                          linewidth=1.1, edgecolor=fs.FAINT, facecolor="#FCFCFD",
                          linestyle=(0, (4, 3)), zorder=2)
    ax.add_patch(cont)
    fs.label(ax, 0.42, 2.70, "缓冲把两种速率解耦", fs=9.2, ha="left", weight="bold")
    fs.label(ax, 0.42, 2.34, "一次推理写满 25 格，每格一步 20 ms", fs=8.3, color=fs.MUTED, ha="left")

    pitch, w0 = 0.30, 0.25
    for i in range(25):
        x = 0.90 + i * pitch
        filled = i < 9
        ax.add_patch(Rectangle((x, 1.38), w0, 0.52,
                               facecolor="#DCE7F7" if filled else "#FFFFFF",
                               edgecolor=fs.BLUE if filled else fs.FAINT,
                               lw=0.8, zorder=3))
    ax.add_patch(Rectangle((6.55, 2.26), 0.26, 0.26, facecolor="#DCE7F7",
                           edgecolor=fs.BLUE, lw=0.8, zorder=3))
    fs.label(ax, 6.90, 2.39, "已执行", fs=8.0, ha="left", color=fs.MUTED)
    ax.add_patch(Rectangle((7.95, 2.26), 0.26, 0.26, facecolor="#FFFFFF",
                           edgecolor=fs.FAINT, lw=0.8, zorder=3))
    fs.label(ax, 8.30, 2.39, "待执行", fs=8.0, ha="left", color=fs.MUTED)

    fs.label(ax, 0.42, 0.92, "25 格 = 0.5 s，缓冲深度按推理延迟的 p99 定", fs=8.3,
             color=fs.MUTED, ha="left")

    fs.arrow(ax, (8.00, 3.83), (8.00, 2.98), color=fs.GREEN)
    fs.label(ax, 8.10, 3.42, "写入", fs=8.2, ha="left", color=fs.GREEN)
    fs.arrow(ax, (9.40, 2.98), (9.40, 3.83), color=fs.PURPLE)
    fs.label(ax, 9.30, 3.42, "取用", fs=8.2, ha="right", color=fs.PURPLE)

    fs.save(fig, "ch11", "fig11-01")


def fig_heads():
    """四种动作头的结构小图，2x2。"""
    fig, ax = fs.canvas(6.6, 4.22)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.4)

    # (a) 离散 token
    fs.label(ax, 0.25, 6.00, "（a）离散 token，自回归逐维出", fs=9.4, ha="left", weight="bold")
    fs.box(ax, 0.25, 4.62, 0.95, 0.72, "主干", fs=8.6, ec=fs.BLUE, fc="#EEF3FB")
    for i in range(5):
        x = 1.44 + i * 0.42
        ax.add_patch(Rectangle((x, 4.73), 0.34, 0.50, facecolor="#FDF1E6",
                               edgecolor=fs.ACCENT, lw=0.9, zorder=3))
        fs.label(ax, x + 0.17, 4.98, str(i + 1), fs=8.0, color=fs.ACCENT)
    fs.label(ax, 3.62, 4.98, "…", fs=9.0, color=fs.ACCENT)
    fs.arrow(ax, (1.24, 4.98), (1.40, 4.98), color=fs.INK)
    fs.arrow(ax, (3.68, 4.98), (3.96, 4.98), color=fs.INK)
    fs.box(ax, 4.00, 4.62, 0.72, 0.72, "动作", fs=8.6, ec=fs.INK, fc="#FFFFFF")
    fs.label(ax, 0.25, 4.34, "每维 256 个 bin，7 个 token 依次出", fs=8.0, color=fs.MUTED, ha="left")
    fs.label(ax, 0.25, 3.62, "7 次串行前向，延迟随动作维数线性涨", fs=8.3, color=fs.MUTED, ha="left")

    # (b) 连续回归
    fs.label(ax, 5.35, 6.00, "（b）连续回归，一次出全部", fs=9.4, ha="left", weight="bold")
    fs.box(ax, 5.35, 4.62, 0.90, 0.72, "主干", fs=8.6, ec=fs.BLUE, fc="#EEF3FB")
    fs.box(ax, 6.45, 4.62, 0.82, 0.72, "MLP", fs=8.6, ec=fs.TEAL, fc="#ECF6F4")
    fs.box(ax, 7.47, 4.62, 0.92, 0.72, "7 个数", fs=8.6, ec=fs.INK, fc="#FFFFFF")
    fs.arrow(ax, (6.27, 4.98), (6.42, 4.98), color=fs.INK)
    fs.arrow(ax, (7.29, 4.98), (7.44, 4.98), color=fs.INK)
    fs.label(ax, 5.35, 4.34, "一次前向，延迟最低", fs=8.0, color=fs.MUTED, ha="left")
    fs.label(ax, 5.35, 3.62, "两条路都可行时，平均出一个都不像的中间值", fs=8.3, color=fs.MUTED, ha="left")

    # (c) 扩散头
    fs.label(ax, 0.25, 2.95, "（c）扩散头，迭代去噪", fs=9.4, ha="left", weight="bold")
    fs.box(ax, 0.25, 1.55, 0.85, 0.72, "噪声", fs=8.6, ec=fs.MUTED, fc="#FFFFFF")
    fs.box(ax, 1.30, 1.55, 1.42, 0.72, "去噪 ×20", fs=8.2, ec=fs.GOLD, fc="#FBF3E6")
    fs.box(ax, 2.98, 1.55, 0.98, 0.72, "动作块", fs=8.6, ec=fs.INK, fc="#FFFFFF")
    fs.arrow(ax, (1.12, 1.91), (1.27, 1.91), color=fs.INK)
    fs.arrow(ax, (2.74, 1.91), (2.95, 1.91), color=fs.INK)
    fs.label(ax, 0.25, 1.27, "主干跑一次，小头迭代 20 步", fs=8.0, color=fs.MUTED, ha="left")
    fs.label(ax, 0.25, 0.60, "能表达多个可行解，延迟由步数决定", fs=8.3, color=fs.MUTED, ha="left")

    # (d) 流匹配
    fs.label(ax, 5.35, 2.95, "（d）流匹配，沿直线积分", fs=9.4, ha="left", weight="bold")
    fs.box(ax, 5.35, 1.55, 0.85, 0.72, "噪声", fs=8.6, ec=fs.MUTED, fc="#FFFFFF")
    fs.box(ax, 6.40, 1.55, 1.30, 0.72, "速度场 ×10", fs=8.0, ec=fs.PINK, fc="#FCF0F5")
    fs.box(ax, 7.98, 1.55, 0.95, 0.72, "动作块", fs=8.6, ec=fs.INK, fc="#FFFFFF")
    fs.arrow(ax, (6.22, 1.91), (6.37, 1.91), color=fs.INK)
    fs.arrow(ax, (7.72, 1.91), (7.95, 1.91), color=fs.INK)
    fs.label(ax, 5.35, 1.27, "10 步欧拉，前缀的 KV 缓存复用", fs=8.0, color=fs.MUTED, ha="left")
    fs.label(ax, 5.35, 0.60, "路径更直，步数更少，50 Hz 靠它", fs=8.3, color=fs.MUTED, ha="left")

    fs.save(fig, "ch11", "fig11-02")


def fig_timeline():
    """相机 30 Hz、策略 5 Hz、动作块、控制 1 kHz 三条时间轴。"""
    fig, ax = fs.canvas(6.6, 3.30)
    ax.set_xlim(-250, 1085)
    ax.set_ylim(0, 5.7)

    T = 1000.0
    # 车道标签
    fs.label(ax, -240, 4.62, "相机 30 Hz", fs=8.8, ha="left")
    fs.label(ax, -240, 3.28, "策略 5 Hz", fs=8.8, ha="left")
    fs.label(ax, -240, 2.15, "动作块", fs=8.8, ha="left")
    fs.label(ax, -240, 0.62, "控制 1 kHz", fs=8.8, ha="left")

    # 相机：曝光 + 读出
    for i in range(30):
        x = i * (T / 30.0)
        ax.add_patch(Rectangle((x, 4.38), 12.0, 0.46, facecolor="#F6E3C8",
                               edgecolor=fs.GOLD, lw=0.5, zorder=3))
        ax.add_patch(Rectangle((x + 12.0, 4.38), 8.0, 0.46, facecolor="#E5E7EB",
                               edgecolor="none", zorder=3))
    fs.label(ax, 220, 4.14, "曝光 12 ms，读出 8 ms", fs=8.0, color=fs.MUTED, ha="left")

    # 策略：每 200 ms 一次，推理 150 ms
    for i in range(5):
        x = i * 200.0
        ax.add_patch(Rectangle((x, 3.05), 150.0, 0.46, facecolor="#FDF1E6",
                               edgecolor=fs.ACCENT, lw=0.7, zorder=3))
    fs.label(ax, 215, 2.80, "推理 150 ms，之后空 50 ms", fs=8.0, color=fs.ACCENT, ha="left")

    # 动作块：四块重叠，块长 0.5 s，每 200 ms 换一块
    bars = [(0.0, 2.42, 500.0, "块 k"), (200.0, 2.08, 500.0, "块 k+1"),
            (400.0, 1.74, 500.0, "块 k+2"), (600.0, 1.40, 400.0, "块 k+3")]
    for x0, y, w, name in bars:
        ax.add_patch(Rectangle((x0, y), w, 0.26, facecolor="#ECF6F1",
                               edgecolor=fs.GREEN, lw=0.8, alpha=0.95, zorder=3))
        fs.label(ax, x0 + 10, y + 0.13, name, fs=7.9, color=fs.GREEN, ha="left")
    fs.label(ax, 710, 2.55, "每块覆盖 0.5 s，每 200 ms 换一块", fs=8.0, color=fs.MUTED, ha="left")

    # 控制：1 kHz 密刻度
    for i in range(0, 101):
        x = i * 10.0
        ax.plot([x, x], [0.36, 0.58], color=fs.PURPLE, lw=0.6, alpha=0.5, zorder=3)
    ax.plot([0, T], [0.47, 0.47], color=fs.PURPLE, lw=1.0, alpha=0.6, zorder=2)
    fs.label(ax, 215, 0.22, "1 s 一千个目标，只有 125 个是新算出来的", fs=8.0,
             color=fs.MUTED, ha="left")

    # 延迟箭头
    ax.annotate("", xy=(180, 5.36), xytext=(0, 5.36),
                arrowprops=dict(arrowstyle="-|>", color=fs.ACCENT, lw=1.2,
                                shrinkA=0, shrinkB=0))
    ax.plot([180, 180], [0.36, 5.30], color=fs.ACCENT, lw=0.9, ls=(0, (3, 3)), alpha=0.8, zorder=2)
    ax.plot([0, 0], [4.84, 5.30], color=fs.ACCENT, lw=0.9, ls=(0, (3, 3)), alpha=0.8, zorder=2)
    fs.label(ax, 196, 5.46, "第一帧的动作 180 ms 后才生效", fs=8.2, color=fs.ACCENT, ha="left")

    # 时间轴
    ax.plot([0, T], [0.02, 0.02], color=fs.FAINT, lw=0.9)
    for t in (0, 250, 500, 750, 1000):
        ax.plot([t, t], [0.02, -0.06], color=fs.FAINT, lw=0.9)
        fs.label(ax, t, -0.20, "%d" % t, fs=7.9, color=fs.MUTED)
    fs.label(ax, 1040, -0.20, "ms", fs=7.9, color=fs.MUTED, ha="left")

    fs.save(fig, "ch11", "fig11-03")


if __name__ == "__main__":
    fig_arch()
    fig_heads()
    fig_timeline()
