# -*- coding: utf-8 -*-
"""第 3 章插图：六十年时间线、三条路线信号流、规则与数据的分界。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import figstyle as fs


def _extent(ax, texts):
    """返回一组 text 在数据坐标下的联合包围盒 (x0, y0, x1, y1)。"""
    ax.figure.canvas.draw()
    r = ax.figure.canvas.get_renderer()
    inv = ax.transData.inverted()
    xs, ys = [], []
    for t in texts:
        bb = t.get_window_extent(r)
        (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        xs += [x0, x1]
        ys += [y0, y1]
    return min(xs), min(ys), max(xs), max(ys)


def _text_w(ax, s, fontsize):
    """返回字符串在数据坐标下的宽度（用于排布避让）。"""
    t = ax.text(0.5, 0.5, s, fontsize=fontsize)
    x0, _, x1, _ = _extent(ax, [t])
    t.remove()
    return abs(x1 - x0)


def fig_timeline():
    """三条泳道的时间线，标签两行交替排布。"""
    fig, ax = fs.canvas(7.6, 5.2)
    ax.set_xlim(1940, 2038)
    ax.set_ylim(0, 1)

    lanes = [
        ("决策", 0.85, fs.BLUE, [
            (1966, "Shakey 先建模"),
            (1986, "包容式架构"),
            (1999, "概率定位"),
            (2013, "DQN"),
            (2022, "SayCan 接语言"),
            (2025, "通用策略"),
        ]),
        ("感知", 0.53, fs.TEAL, [
            (1987, "相机标定", 1),
            (1999, "SIFT 特征", 0),
            (2012, "检测网络", 1),
            (2017, "抓取网络", 0),
            (2024, "开放词汇", 1),
        ]),
        ("身体", 0.23, fs.GOLD, [
            (1961, "Unimate 进厂"),
            (2002, "清扫机器人"),
            (2010, "PR2 双臂"),
            (2021, "四足奔跑"),
            (2025, "人形整机"),
        ]),
    ]

    x_lo, x_hi = 1950, 2032
    for name, cy, color, items in lanes:
        ax.add_patch(Rectangle((x_lo, cy - 0.13), x_hi - x_lo, 0.26,
                               facecolor="#FAFAFA", edgecolor="none", zorder=1))
        ax.plot([x_lo, x_hi], [cy, cy], color="#D1D5DB", lw=1.0, zorder=2)
        ax.add_patch(Rectangle((x_lo - 1.4, cy - 0.13), 1.4, 0.26,
                               facecolor=color, edgecolor="none", zorder=2))
        fs.label(ax, x_lo - 2.6, cy, name, fs=10.5, color=color, weight="bold", ha="right")

        taken = {0: [], 1: []}
        for i, item in enumerate(items):
            year, text = item[0], item[1]
            fixed_row = item[2] if len(item) > 2 else None
            probe_t = ax.text(year, 0, text, fontsize=8.4, ha="center", va="center")
            probe_y = ax.text(year, 0, str(year), fontsize=7.6, weight="bold", ha="center", va="center")
            bx0, _, bx1, _ = _extent(ax, [probe_t, probe_y])
            probe_t.remove()
            probe_y.remove()
            w = (bx1 - bx0) + 1.6
            order = [fixed_row] if fixed_row is not None else [i % 2, 1 - i % 2]
            row = order[0]
            for r in order:
                clash = any(abs(year - yc) < (w + wc) / 2 + 0.8 for yc, wc in taken[r])
                if not clash:
                    row = r
                    break
            else:
                print("WARN 标签无法避让:", name, year, text)
            taken[row].append((year, w))
            up = (row == 0)
            y_edge = cy + 0.02 if up else cy - 0.02
            y_far = cy + 0.115 if up else cy - 0.115
            ax.plot([year, year], [y_edge, y_far], color="#9CA3AF", lw=0.7, zorder=3)
            ax.scatter([year], [cy], s=26, color=color, edgecolor="white", linewidth=0.9, zorder=4)
            y0 = cy + 0.02 if up else cy - 0.115
            fs.box(ax, year - w / 2, y0, w, 0.095, "", fc="white", ec="#D1D5DB",
                   lw=0.8, rounded=0.012, z=5)
            fs.label(ax, year, y0 + 0.064, str(year), fs=7.6, color=color, weight="bold", z=6)
            fs.label(ax, year, y0 + 0.030, text, fs=8.4, color=fs.INK, z=6)

    # 底部年份轴
    ax.annotate("", xy=(x_hi + 2, 0.05), xytext=(x_lo - 2, 0.05),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0))
    for dec in range(1960, 2031, 10):
        ax.plot([dec, dec], [0.05, 0.035], color=fs.MUTED, lw=0.8)
        fs.label(ax, dec, 0.012, str(dec), fs=8.2, color=fs.MUTED)
    fs.label(ax, 2034, 0.075, "年", fs=8.2, color=fs.MUTED, ha="right", va="bottom")

    fs.save(fig, "ch03", "fig03-01")


def fig_routes():
    """三条路线的信号流对比，三个 panel。"""
    fig, axes = plt.subplots(1, 3, figsize=(7.8, 4.0))
    fig.subplots_adjust(left=0.02, right=0.985, top=0.86, bottom=0.04, wspace=0.13)
    panels = [
        ("(a) 模块化流水线", "每个接口都由人定义", fs.BLUE),
        ("(b) 端到端 VLA", "中间环节不对外暴露", fs.ACCENT),
        ("(c) 分层快慢系统", "慢的给目标，快的给反应", fs.PURPLE),
    ]
    for ax, (tt, sub, col) in zip(axes, panels):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title(tt, fontsize=9.8, color=fs.INK, pad=16)
        ax.text(0.5, 1.012, sub, transform=ax.transAxes, fontsize=8.4,
                color=col, ha="center", va="bottom")

    # (a) 模块化：一条人搭的流水线
    ax = axes[0]
    x, w, h = 0.06, 0.88, 0.125
    items = [("相机图像", 0.80), ("检测 · 分割 · 位姿", 0.605),
             ("抓取选择 + 路径规划", 0.41), ("关节控制器", 0.215)]
    labels = ["物体框与位姿", "抓取位姿", "关节角序列"]
    for text, y in items:
        fs.box(ax, x, y, w, h, text, fc="white", ec=fs.BLUE, fs=8.6, lw=1.1)
    for i in range(3):
        fs.arrow(ax, (0.5, items[i][1] - 0.003), (0.5, items[i + 1][1] + h + 0.003),
                 color=fs.MUTED, lw=1.1)
        fs.label(ax, 0.575, (items[i][1] + items[i + 1][1] + h) / 2, labels[i],
                 fs=7.6, color=fs.MUTED, ha="left")
    fs.arrow(ax, (0.5, 0.212), (0.5, 0.135), color=fs.MUTED, lw=1.1)
    fs.label(ax, 0.5, 0.085, "电机指令", fs=8.2, color=fs.MUTED)

    # (b) 端到端：一个网络吃掉中间环节
    ax = axes[1]
    fs.box(ax, x, 0.80, w, 0.125, "相机图像 + 语言指令", fc="white", ec=fs.ACCENT, fs=8.6, lw=1.1)
    fs.arrow(ax, (0.5, 0.797), (0.5, 0.725), color=fs.MUTED, lw=1.1)
    fs.box(ax, x, 0.50, w, 0.22, "一个网络\n（十亿级参数）", fc="#FBEAE1", ec=fs.ACCENT,
           fs=9.2, lw=1.3)
    fs.arrow(ax, (0.5, 0.497), (0.5, 0.405), color=fs.MUTED, lw=1.1)
    fs.box(ax, x, 0.275, w, 0.125, "动作块：位姿增量", fc="white", ec=fs.ACCENT, fs=8.6, lw=1.1)
    fs.arrow(ax, (0.5, 0.272), (0.5, 0.195), color=fs.MUTED, lw=1.1)
    fs.label(ax, 0.5, 0.145, "关节伺服（仍然是人写的）", fs=8.0, color=fs.MUTED)

    # (c) 分层：慢的想，快的动
    ax = axes[2]
    fs.box(ax, x, 0.80, w, 0.125, "语言指令", fc="white", ec=fs.PURPLE, fs=8.6, lw=1.1)
    fs.arrow(ax, (0.5, 0.797), (0.5, 0.73), color=fs.MUTED, lw=1.1)
    fs.box(ax, x, 0.585, w, 0.14, "LLM 慢思考　约 1 Hz", fc="#EFEAFB", ec=fs.PURPLE, fs=8.6, lw=1.2)
    fs.arrow(ax, (0.5, 0.582), (0.5, 0.52), color=fs.MUTED, lw=1.1)
    fs.box(ax, x, 0.40, w, 0.115, "技能名 + 参数", fc="white", ec=fs.PURPLE, fs=8.6, lw=1.1)
    fs.arrow(ax, (0.5, 0.397), (0.5, 0.335), color=fs.MUTED, lw=1.1)
    fs.box(ax, x, 0.19, w, 0.14, "策略快反射　约 50 Hz", fc="#EFEAFB", ec=fs.PURPLE, fs=8.6, lw=1.2)
    fs.arrow(ax, (0.5, 0.187), (0.5, 0.125), color=fs.MUTED, lw=1.1)
    fs.label(ax, 0.5, 0.08, "关节动作", fs=8.2, color=fs.MUTED)

    fs.save(fig, "ch03", "fig03-02")


def fig_rule_vs_data():
    """同一任务下，模块化与端到端各自哪些环节靠人写规则。"""
    fig, ax = fs.canvas(7.4, 4.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    RULE = "#E8DFD2"
    DATA = "#D8E4F3"

    x_stage, w_stage = 0.02, 0.235
    x_mod, w_cell = 0.285, 0.325
    x_e2e = 0.645

    fs.label(ax, x_stage + w_stage / 2, 0.925, "环节", fs=9.0, weight="bold")
    fs.label(ax, x_mod + w_cell / 2, 0.925, "模块化流水线", fs=9.0, weight="bold", color=fs.BLUE)
    fs.label(ax, x_e2e + w_cell / 2, 0.925, "端到端 VLA", fs=9.0, weight="bold", color=fs.ACCENT)

    rows = [
        ("任务分解", "人写状态机", "数据决定"),
        ("检测与位姿", "数据决定", "数据决定"),
        ("抓取点选择", "人写几何判据", "数据决定"),
        ("路径与避障", "人写采样规划", "数据决定"),
        ("关节伺服", "人写 PID", "人写 PID"),
        ("失败恢复", "人写重试逻辑", "空缺"),
    ]
    h, gap, top = 0.085, 0.021, 0.855
    for i, (stage, left, right) in enumerate(rows):
        y = top - (i + 1) * (h + gap)
        fs.label(ax, x_stage + 0.012, y + h / 2, stage, fs=8.8, color=fs.INK, ha="left")
        for xx, txt in ((x_mod, left), (x_e2e, right)):
            if txt == "空缺":
                fs.box(ax, xx, y, w_cell, h, "空缺（靠人接管）", fc="white", ec=fs.FAINT,
                       tc=fs.MUTED, fs=8.4, lw=1.0, rounded=0.012)
            else:
                rule = txt in ("人写状态机", "人写几何判据", "人写采样规划",
                               "人写 PID", "人写重试逻辑")
                fs.box(ax, xx, y, w_cell, h, txt, fc=(RULE if rule else DATA),
                       ec=("#C9BBA8" if rule else "#A9C0DE"), fs=8.4, lw=1.0, rounded=0.012)

    ly = 0.098
    ax.add_patch(Rectangle((0.06, ly), 0.05, 0.042, facecolor=RULE, edgecolor="#C9BBA8", lw=1.0))
    fs.label(ax, 0.125, ly + 0.021, "人写规则", fs=8.4, color=fs.INK, ha="left")
    ax.add_patch(Rectangle((0.31, ly), 0.05, 0.042, facecolor=DATA, edgecolor="#A9C0DE", lw=1.0))
    fs.label(ax, 0.375, ly + 0.021, "数据决定", fs=8.4, color=fs.INK, ha="left")
    fs.label(ax, 0.60, ly + 0.021, "两列相同的格子，谁也绕不过去", fs=8.2, color=fs.MUTED, ha="left")

    fs.save(fig, "ch03", "fig03-03")


if __name__ == "__main__":
    fig_timeline()
    fig_routes()
    fig_rule_vs_data()
