# -*- coding: utf-8 -*-
"""第 1 章插图：感知-行动闭环、屏幕动作与物理动作的差别。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import figstyle as fs


def fig_loop():
    """四步闭环：看见 -> 想 -> 动手 -> 世界变了。"""
    fig, ax = fs.canvas(6.6, 4.0)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.3)

    W, H = 3.40, 1.18
    boxes = [
        (0.60, 4.55, "看见\n相机 · 深度 · 力与触觉", "#FFFFFF"),
        (6.00, 4.55, "想\n认出物体 · 决定抓哪", "#FFFFFF"),
        (6.00, 1.05, "动手\n关节转动 · 夹爪开合", "#FFFFFF"),
        (0.60, 1.05, "世界变了\n杯子挪了位置", "#FBF7F0"),
    ]
    for x, y, text, fc in boxes:
        fs.box(ax, x, y, W, H, text, fs=9.0, ec=fs.INK, fc=fc)

    fs.arrow(ax, (4.05, 5.14), (5.95, 5.14))
    ax.text(5.00, 5.32, "像素", ha="center", va="bottom", fontsize=8.4, color=fs.MUTED)

    fs.arrow(ax, (7.70, 4.50), (7.70, 2.28))
    ax.text(7.86, 3.40, "动作", ha="left", va="center", fontsize=8.4, color=fs.MUTED)

    fs.arrow(ax, (5.95, 1.64), (4.05, 1.64), color=fs.ACCENT)
    ax.text(5.00, 1.46, "接触", ha="center", va="top", fontsize=8.4, color=fs.ACCENT)

    fs.arrow(ax, (2.30, 2.28), (2.30, 4.50))
    ax.text(2.14, 3.40, "光与力", ha="right", va="center", fontsize=8.4, color=fs.MUTED)

    ax.text(5.00, 3.52, "这一圈每秒转几十次", ha="center", va="center",
            fontsize=11.5, color=fs.INK)
    ax.text(5.00, 3.06, "转得慢就迟钝，转得停，任务断在那里", ha="center", va="center",
            fontsize=8.2, color=fs.MUTED)
    ax.text(5.00, 2.60, "每一次看见，都建立在上一次动手的结果上", ha="center",
            va="center", fontsize=8.2, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-01")


def fig_compare():
    """屏幕里的动作与物理世界的动作，两栏对照。"""
    fig, ax = fs.canvas(6.6, 3.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.2)

    left = (0.35, "屏幕里的 Agent", fs.BLUE, "#EEF3FB",
            [("点一个按钮", "位置永远准确"),
             ("发一次请求", "失败可以重发"),
             ("写错一行", "撤销就回去了"),
             ("一次操作", "几乎不花时间和钱")])
    right = (5.35, "机器人", fs.ACCENT, "#FDF1E6",
             [("转一个关节", "差 2 毫米就是差 2 毫米"),
              ("推一个杯子", "推倒就扶不起来"),
              ("夹一次", "太用力会碎，太轻会滑"),
              ("一次动作", "几百毫秒，还可能撞到东西")])

    for x0, title, color, fc, rows in (left, right):
        fs.box(ax, x0, 5.95, 4.30, 0.95, title, fs=10.2, ec=color, fc=fc, weight="bold", tc=color)
        for i, (a, b) in enumerate(rows):
            y = 4.70 - i * 1.28
            fs.box(ax, x0, y, 4.30, 1.02, "", fc="#FFFFFF", ec="#C9D2DC", lw=0.9)
            ax.text(x0 + 0.26, y + 0.66, a, ha="left", va="center", fontsize=8.8, color=fs.INK)
            ax.text(x0 + 0.26, y + 0.30, b, ha="left", va="center", fontsize=8.2, color=fs.MUTED)

    ax.annotate("", xy=(4.95, 3.95), xytext=(4.75, 3.95),
                arrowprops=dict(arrowstyle="-|>", color=fs.FAINT, lw=1.0))
    ax.text(5.0, 0.42, "同一句指令，落到两种介质上，代价完全不同",
            ha="center", va="center", fontsize=8.4, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-02")


if __name__ == "__main__":
    fig_loop()
    fig_compare()
