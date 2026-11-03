# -*- coding: utf-8 -*-
"""第 19 章插图：控制循环时延、软件栈分层、失败恢复状态机。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs


# ---------------------------------------------------------------- 图 19-1
def fig_latency():
    """一次控制循环的时延瀑布图。上：策略 250 ms；下：策略 73 ms。"""
    fig, axes = plt.subplots(2, 1, figsize=(6.7, 4.5), sharex=True,
                             gridspec_kw=dict(hspace=0.34, left=0.13, right=0.985,
                                              top=0.90, bottom=0.16))
    a, b = axes

    rows = [("相机", 0, fs.BLUE), ("感知", 1, fs.TEAL), ("策略", 2, fs.ACCENT),
            ("规划", 3, fs.PURPLE), ("控制", 4, fs.GREEN)]
    # (名称, 起点, 时长)
    case_a = [("相机", 0, 20), ("感知", 20, 35), ("策略", 55, 250),
              ("规划", 305, 40), ("控制", 345, 1)]
    case_b = [("相机", 0, 20), ("感知", 20, 35), ("策略", 55, 73),
              ("规划", 128, 40), ("控制", 168, 1)]

    ymap = {"相机": 4, "感知": 3, "策略": 2, "规划": 1, "控制": 0}
    col = {n: c for n, _, c in rows}

    def draw(ax, case, total, freq, tag, show_budget_3hz):
        for name, x0, dur in case:
            ax.barh(ymap[name], dur, left=x0, height=0.46, color=col[name],
                    edgecolor="white", linewidth=0.8, zorder=3)
            if dur >= 70:
                ax.text(x0 + dur / 2, ymap[name], f"{dur} ms", ha="center", va="center",
                        fontsize=8.8, color="white", zorder=4, weight="bold")
            else:
                ax.text(x0 + dur + 6, ymap[name], f"{dur} ms", ha="left", va="center",
                        fontsize=8.4, color=fs.MUTED, zorder=4)
        # 预算线
        ax.axvline(100, color=fs.FAINT, lw=0.9, ls=(0, (4, 3)), zorder=1)
        if show_budget_3hz:
            ax.axvline(333, color=fs.GOLD, lw=1.0, ls=(0, (4, 3)), zorder=1)
        # 总时延
        ax.annotate("", xy=(total, -0.72), xytext=(0, -0.72),
                    arrowprops=dict(arrowstyle="<->", color=fs.INK, lw=0.9))
        ax.text(total / 2, -0.92, f"一轮 {total} ms，上限 {freq}", ha="center", va="top",
                fontsize=8.6, color=fs.INK, zorder=8,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
        ax.text(0.005, 1.03, tag, transform=ax.transAxes, ha="left", va="bottom",
                fontsize=9.2, color=fs.INK)
        ax.set_ylim(-1.65, 4.85)
        ax.set_yticks(range(5))
        fs.clean(ax, spines=("bottom",))

    draw(a, case_a, 346, "2.9 Hz", "(a) 策略推理 250 ms 的串行链路", True)
    draw(b, case_b, 169, "5.9 Hz", "(b) 策略推理 73 ms 的串行链路", False)
    b.tick_params(left=False, labelleft=False)
    a.set_yticklabels(["控制", "规划", "策略", "感知", "相机"], fontsize=9.2)

    a.text(104, 4.40, "10 Hz 预算 100 ms", ha="left", va="bottom", fontsize=8.2, color=fs.MUTED)
    a.text(329, 4.40, "3 Hz 预算 333 ms", ha="right", va="bottom", fontsize=8.2, color=fs.GOLD)
    b.set_xlim(-8, 380)
    b.set_xlabel("从上一次曝光开始计时（ms）", fontsize=9.6)
    fs.save(fig, "ch19", "fig19-01")


# ---------------------------------------------------------------- 图 19-2
def fig_stack():
    """软件栈分层与各层典型运行频率。"""
    fig, ax = fs.canvas(6.7, 3.6)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0.80, 6.45)

    layers = [
        ("应用层", "任务分解 · 长程计划 · 人机交互", "0.1–1 Hz", "#F5EFE7"),
        ("技能层", "行为树 · 动作原语 · 失败恢复", "1–10 Hz", "#EEE9F5"),
        ("感知层", "检测 · 位姿 · 抓取检测 · 场景图", "10–30 Hz", "#E4F0EE"),
        ("驱动层", "轨迹插值 · 伺服环 · 总线通信", "100–1000 Hz", "#E7EDF7"),
        ("硬件层", "电机 · 减速器 · 编码器 · 传感器", "连续", "#F1F1F1"),
    ]
    x0, w, h, gap = 0.62, 9.60, 0.84, 0.16
    for i, (name, detail, freq, fc) in enumerate(layers):
        y = 5.05 - i * (h + gap)
        fs.box(ax, x0, y, w, h, "", fc=fc, ec="#C8CDD6", lw=0.8)
        ax.text(x0 + 0.22, y + h / 2, name, ha="left", va="center", fontsize=9.4,
                color=fs.INK, weight="bold")
        ax.text(x0 + 1.85, y + h / 2, detail, ha="left", va="center", fontsize=8.5,
                color=fs.MUTED)
        ax.text(x0 + w - 0.22, y + h / 2, freq, ha="right", va="center", fontsize=8.8,
                color=fs.ACCENT)

    ax.text(x0 + 0.22, 6.16, "层", ha="left", va="center", fontsize=8.2, color=fs.FAINT)
    ax.text(x0 + 1.85, 6.16, "这一层做什么", ha="left", va="center", fontsize=8.2, color=fs.FAINT)
    ax.text(x0 + w - 0.22, 6.16, "典型频率", ha="right", va="center", fontsize=8.2, color=fs.FAINT)

    fs.arrow(ax, (0.30, 5.85), (0.30, 1.15), color=fs.FAINT, lw=1.0, ms=7)
    ax.text(0.30, 5.95, "慢", ha="center", va="bottom", fontsize=8.2, color=fs.FAINT)
    ax.text(0.30, 0.99, "快", ha="center", va="top", fontsize=8.2, color=fs.FAINT)
    fs.save(fig, "ch19", "fig19-02")


# ---------------------------------------------------------------- 图 19-3
def fig_recovery():
    """失败恢复状态机。"""
    fig, ax = fs.canvas(6.7, 4.0)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0.70, 6.85)

    S = {
        "run":   (0.40, 4.30, 2.65, 1.00, "正常执行", "按计划推进", "#ECFDF5", fs.GREEN),
        "retry": (4.05, 4.30, 2.25, 1.00, "重试", "同一动作再发一次", "#FFFBEB", fs.GOLD),
        "stop":  (7.30, 4.30, 2.55, 1.00, "安全停止", "断电保持 · 等人工复位", "#FEF2F2", fs.ACCENT),
        "back":  (0.40, 2.25, 2.65, 1.00, "回退安全位", "退回已标定位姿", "#EFF6FF", fs.BLUE),
        "human": (4.05, 2.25, 2.25, 1.00, "请求人工", "语音 / 界面告警", "#F5F3FF", fs.PURPLE),
    }
    for key, (x, y, w, h, name, sub, fc, ec) in S.items():
        fs.box(ax, x, y, w, h, "", fc=fc, ec=ec, lw=1.1)
        ax.text(x + 0.18, y + h - 0.28, name, ha="left", va="center", fontsize=9.4,
                color=ec, weight="bold")
        ax.text(x + 0.18, y + 0.30, sub, ha="left", va="center", fontsize=8.0, color=fs.MUTED)

    # 1 正常 -> 重试
    fs.arrow(ax, (3.05, 4.92), (4.05, 4.92), color=fs.MUTED)
    ax.text(3.53, 5.05, "单次失败", ha="center", va="bottom", fontsize=7.0, color=fs.INK)

    # 2 重试 -> 正常
    fs.arrow(ax, (4.05, 4.52), (3.05, 4.52), color=fs.MUTED)
    ax.text(3.53, 4.43, "恢复", ha="center", va="top", fontsize=7.2, color=fs.INK)

    # 3 重试 -> 安全停止
    fs.arrow(ax, (6.30, 4.92), (7.30, 4.92), color=fs.MUTED)
    ax.text(6.80, 5.05, "用尽", ha="center", va="bottom", fontsize=7.2, color=fs.INK)

    # 4 正常 -> 回退
    fs.arrow(ax, (1.10, 4.30), (1.10, 3.25), color=fs.MUTED)
    ax.text(1.24, 3.80, "连续两次失败", ha="left", va="center", fontsize=7.8, color=fs.INK)

    # 5 回退 -> 正常
    fs.arrow(ax, (2.62, 3.25), (2.62, 4.30), color=fs.MUTED)
    ax.text(2.76, 3.62, "已复归位", ha="left", va="center", fontsize=7.8, color=fs.INK)

    # 6 回退 -> 请求人工
    fs.arrow(ax, (3.05, 3.00), (4.05, 3.00), color=fs.MUTED)
    ax.text(3.53, 3.07, "无手段", ha="center", va="bottom", fontsize=7.0, color=fs.INK)

    # 7 请求人工 -> 回退
    fs.arrow(ax, (4.05, 2.68), (3.05, 2.68), color=fs.MUTED)
    ax.text(3.53, 2.57, "人工放行", ha="center", va="top", fontsize=7.0, color=fs.INK)

    # 8 请求人工 -> 安全停止
    fs.arrow(ax, (4.90, 3.25), (4.90, 4.30), color=fs.MUTED)
    ax.text(5.04, 3.74, "超时未响应", ha="left", va="center", fontsize=7.8, color=fs.INK)

    # 9 正常 -> 安全停止（绕上方）
    ax.plot([1.75, 1.75], [5.30, 6.30], color=fs.MUTED, lw=1.1, zorder=2)
    ax.plot([1.75, 8.60], [6.30, 6.30], color=fs.MUTED, lw=1.1, zorder=2)
    fs.arrow(ax, (8.60, 6.30), (8.60, 5.30), color=fs.MUTED)
    ax.text(5.20, 6.38, "急停按下 / 有人进入工作区", ha="center", va="bottom",
            fontsize=7.8, color=fs.ACCENT)

    ax.text(0.40, 1.62, "箭头旁的文字是转移条件，每条都带超时上限。同一条指令带唯一 ID，重发不会产生第二个动作。",
            ha="left", va="center", fontsize=7.8, color=fs.MUTED)
    ax.text(0.40, 1.20, "重试上限 2 次，单动作超时取正常耗时的 2 倍，等人工的超时是 30 s。",
            ha="left", va="center", fontsize=7.8, color=fs.MUTED)
    fs.save(fig, "ch19", "fig19-03")


if __name__ == "__main__":
    fig_latency()
    fig_stack()
    fig_recovery()
