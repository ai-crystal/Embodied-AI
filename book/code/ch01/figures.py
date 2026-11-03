# -*- coding: utf-8 -*-
"""第 1 章插图：闭环、能力栈、一次抓放任务的时序。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import matplotlib.pyplot as plt
import figstyle as fs


def fig_loop():
    """感知-决策-行动闭环。四个角各一个框，箭头沿矩形边流动。"""
    fig, ax = fs.canvas(6.6, 4.2)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.4)

    W, H = 3.0, 1.5
    boxes = {
        "sense": (0.5, 4.5, "感知\n相机 · 深度 · 力 / 触觉"),
        "repr": (6.5, 4.5, "场景表示\n物体 · 位姿 · 地图"),
        "decide": (6.5, 0.6, "决策\n策略 · 规划 · 大模型"),
        "act": (0.5, 0.6, "动作\n关节指令 · 夹爪开合"),
    }
    for x, y, text in boxes.values():
        fs.box(ax, x, y, W, H, text, fs=9.2, fc="#FFFFFF", ec=fs.INK)

    # 上边：感知 -> 表示
    fs.arrow(ax, (3.6, 5.25), (6.4, 5.25))
    ax.text(5.0, 5.45, "像素 / 点云", ha="center", va="bottom", fontsize=8.6, color=fs.MUTED)
    # 右边：表示 -> 决策
    fs.arrow(ax, (8.0, 4.4), (8.0, 2.2))
    ax.text(8.18, 3.3, "目标\n约束", ha="left", va="center", fontsize=8.6, color=fs.MUTED)
    # 下边：决策 -> 动作
    fs.arrow(ax, (6.4, 1.35), (3.6, 1.35))
    ax.text(5.0, 1.12, "关节轨迹 / 力矩", ha="center", va="top", fontsize=8.6, color=fs.MUTED)
    # 左边：动作 -> 感知（经由环境）
    fs.arrow(ax, (2.0, 2.2), (2.0, 4.4))
    ax.text(1.82, 3.3, "改变\n世界", ha="right", va="center", fontsize=8.6, color=fs.MUTED)

    ax.text(5.0, 3.45, "闭环", ha="center", va="center", fontsize=13, color=fs.ACCENT)
    ax.text(5.0, 2.98, "每秒重复几十到上千次", ha="center", va="center", fontsize=8.8, color=fs.MUTED)
    fs.save(fig, "ch01", "fig01-01")


def fig_stack():
    """能力栈：从身体到应用，右侧标出对应章节。"""
    fig, ax = fs.canvas(6.6, 3.9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.0)

    layers = [
        ("应用层", "抓取上架 · 分拣 · 家务 · 巡检", "第 19–21 章", "#EEF2F7"),
        ("基础模型层", "视觉-语言-动作模型 · 世界模型", "第 12–15 章", "#E7EEF6"),
        ("学习层", "强化学习 · 模仿学习 · 规划", "第 8–11 章", "#E0EAF4"),
        ("感知层", "相机几何 · 位姿 · 特征 · 地图", "第 4–7 章", "#D9E5F2"),
        ("身体层", "机构 · 关节 · 传感器 · 执行器", "第 2、16–18 章", "#D2E0EF"),
    ]
    x0, w, h, gap = 0.7, 6.3, 0.92, 0.16
    for i, (name, detail, ch, color) in enumerate(layers):
        y = 4.75 - i * (h + gap)
        fs.box(ax, x0, y, w, h, "", fc=color, ec="#B9C6D6", lw=0.9)
        ax.text(x0 + 0.28, y + h / 2, name, ha="left", va="center",
                fontsize=9.6, color=fs.INK, weight="bold")
        ax.text(x0 + 2.15, y + h / 2, detail, ha="left", va="center",
                fontsize=8.6, color=fs.MUTED)
        ax.text(x0 + w + 0.25, y + h / 2, ch, ha="left", va="center",
                fontsize=8.4, color=fs.ACCENT)

    # 左侧向下箭头：越往下越接近物理世界
    fs.arrow(ax, (0.28, 5.4), (0.28, 0.55), color=fs.FAINT, lw=1.0)
    ax.text(0.05, 5.5, "抽象", ha="left", va="bottom", fontsize=8.2, color=fs.FAINT)
    ax.text(0.05, 0.42, "物理", ha="left", va="top", fontsize=8.2, color=fs.FAINT)
    fs.save(fig, "ch01", "fig01-02")


def fig_timeline():
    """一次抓放任务的延迟分解（典型量级，非实测）。"""
    fig, ax = fs.canvas(6.6, 3.2)
    ax.set_xlim(-150, 420)
    ax.set_ylim(-0.1, 7.4)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)

    stages = [
        ("相机曝光与传输", 20, "#DCE7F2"),
        ("视觉推理", 40, "#CFDEF0"),
        ("位姿与抓取检测", 30, "#C2D5ED"),
        ("策略推理（VLA）", 200, "#B4CBE9"),
        ("运动规划", 80, "#A6C1E5"),
        ("下发力矩", 2, "#8FAFD8"),
        ("机械臂运动并接触", 300, "#E7DFD3"),
    ]
    h = 0.52
    for i, (name, dur, color) in enumerate(stages):
        y = 6.5 - i * 0.92
        ax.barh(y, dur, height=h, left=0, color=color, edgecolor="#9AA8B8", lw=0.8, zorder=3)
        ax.text(-8, y, name, ha="right", va="center", fontsize=8.8, color=fs.INK)
        ax.text(dur + 6, y, f"{dur} ms", ha="left", va="center", fontsize=8.2,
                color=fs.MUTED)

    ax.annotate("", xy=(415, -0.02), xytext=(-145, -0.02),
                arrowprops=dict(arrowstyle="-|>", color=fs.MUTED, lw=1.0))
    for t in (0, 100, 200, 300, 400):
        ax.plot([t, t], [-0.02, -0.12], color=fs.MUTED, lw=0.8)
        ax.text(t, -0.2, f"{t}", ha="center", va="top", fontsize=7.8, color=fs.MUTED)
    ax.text(412, 0.22, "耗时 / ms", ha="right", va="bottom", fontsize=8, color=fs.MUTED)
    ax.text(300, 7.05, "合计约 0.67 s", ha="left", va="center", fontsize=8.8,
            color=fs.ACCENT)
    fs.save(fig, "ch01", "fig01-03")


if __name__ == "__main__":
    fig_loop()
    fig_stack()
    fig_timeline()
