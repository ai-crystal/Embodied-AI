# -*- coding: utf-8 -*-
"""第 10 章插图：训练部署环路、sim2real 差距来源、Dreamer 模块结构。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import matplotlib.pyplot as plt
import figstyle as fs


def fig_loop():
    """仿真训练到真机部署的环路。"""
    fig, ax = fs.canvas(6.6, 3.9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.0)

    W, H = 3.5, 1.45
    sim_fc, sim_ec = "#EEF3FA", fs.BLUE
    real_fc, real_ec = "#FBF1E7", fs.ACCENT
    boxes = [
        (0.40, 3.95, "仿真训练\n几千个环境并行采样\n按 PPO 更新策略", sim_fc, sim_ec),
        (6.10, 3.95, "仿真评估\n换场景、加扰动\n统计成功率", sim_fc, sim_ec),
        (6.10, 0.60, "真机部署\n同一份权重\n不做微调", real_fc, real_ec),
        (0.40, 0.60, "数据回流\n失败片段与真机轨迹\n喂回重训和标定", real_fc, real_ec),
    ]
    for x, y, t, fc, ec in boxes:
        fs.box(ax, x, y, W, H, t, fc=fc, ec=ec, fs=9.0, lw=1.1)

    fs.arrow(ax, (3.90, 4.68), (6.10, 4.68), color=fs.MUTED)
    fs.label(ax, 5.00, 4.84, "检查点", fs=8.6, color=fs.MUTED)

    fs.arrow(ax, (7.85, 3.95), (7.85, 2.05), color=fs.MUTED)
    fs.label(ax, 8.05, 3.00, "过门槛才上线", fs=8.6, color=fs.MUTED, ha="left")

    fs.arrow(ax, (6.10, 1.33), (3.90, 1.33), color=fs.MUTED)
    fs.label(ax, 5.00, 1.15, "日志与视频", fs=8.6, color=fs.MUTED)

    fs.arrow(ax, (2.15, 2.05), (2.15, 3.95), color=fs.MUTED)
    fs.label(ax, 1.95, 3.00, "差距归因", fs=8.6, color=fs.MUTED, ha="right")

    fs.label(ax, 5.00, 3.34, "一轮迭代", fs=9.4, color=fs.INK)
    fs.label(ax, 5.00, 3.02, "几个小时", fs=9.4, color=fs.ACCENT)
    fs.label(ax, 5.00, 2.64, "纯 CPU 要按天算", fs=8.2, color=fs.MUTED)

    # 图例
    fs.box(ax, 0.40, 5.55, 0.26, 0.26, "", fc=sim_fc, ec=sim_ec, lw=0.9)
    fs.label(ax, 0.74, 5.68, "仿真侧", fs=8.2, color=fs.MUTED, ha="left")
    fs.box(ax, 1.62, 5.55, 0.26, 0.26, "", fc=real_fc, ec=real_ec, lw=0.9)
    fs.label(ax, 1.96, 5.68, "真机侧", fs=8.2, color=fs.MUTED, ha="left")

    fs.save(fig, "ch10", "fig10-01")


def fig_gap():
    """sim2real gap 的五个来源，仿真与真机逐项对照，下方给出常用对策。"""
    fig, ax = fs.canvas(6.6, 4.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)

    cols = [1.15, 2.75, 4.35, 5.95, 7.55]
    w = 1.35
    heads = ["刚体动力学", "接触摩擦", "执行器", "传感器", "通信"]
    sim = ["理想刚体\n无间隙", "单点刚碰\n摩擦恒定", "力矩直达\n无滞后", "读数干净\n无噪声", "内存拷贝\n微秒级"]
    real = ["连杆有弹性\n齿轮有背隙", "面接触形变\n摩擦不均", "电流环滞后\n力矩会饱和", "零漂量化\n运动模糊", "总线抖动\n几毫秒"]

    for i, x in enumerate(cols):
        fs.label(ax, x + w / 2, 5.72, heads[i], fs=8.8, color=fs.INK, weight="bold")
        fs.box(ax, x, 4.60, w, 0.70, sim[i], fc="#EEF3FA", ec=fs.BLUE, fs=8.4, lw=1.0)
        fs.box(ax, x, 3.05, w, 0.70, real[i], fc="#FBF1E7", ec=fs.ACCENT, fs=8.4, lw=1.0)
        fs.arrow(ax, (x + w / 2, 4.56), (x + w / 2, 3.79), color=fs.ACCENT, lw=1.1,
                 style="<|-|>", ms=7)
        fs.arrow(ax, (x + w / 2, 3.01), (x + w / 2, 1.79), color=fs.FAINT, lw=0.9, ms=6)

    fs.label(ax, 0.55, 4.95, "仿真", fs=9.0, color=fs.BLUE)
    fs.label(ax, 0.55, 3.40, "真机", fs=9.0, color=fs.ACCENT)
    fs.label(ax, 0.55, 1.40, "补法", fs=9.0, color=fs.GOLD)

    fs.box(ax, 1.15, 1.05, 2.95, 0.70, "系统辨识与参数标定", fc="#F6F1E7", ec=fs.GOLD, fs=9.0)
    fs.box(ax, 4.35, 1.05, 2.95, 0.70, "域随机化与在线自适应", fc="#F6F1E7", ec=fs.GOLD, fs=9.0)
    fs.box(ax, 7.55, 1.05, 1.35, 0.70, "延迟建模\n时间戳对齐", fc="#F6F1E7", ec=fs.GOLD, fs=8.2)

    fs.label(ax, 5.00, 0.42, "五处不一致叠起来才是完整的差距，哪一处致命要按任务逐个判断。",
             fs=8.6, color=fs.MUTED)
    fs.save(fig, "ch10", "fig10-02")


def fig_dreamer():
    """Dreamer 的模块结构：编码器、隐状态、序列模型、三个预测头、actor-critic。"""
    fig, ax = fs.canvas(6.6, 4.4)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)

    inp = dict(fc="#FFFFFF", ec=fs.MUTED, lw=0.9)
    mod = dict(fc="#EEF3FA", ec=fs.BLUE, lw=1.1)
    rl = dict(fc="#FBF1E7", ec=fs.GOLD, lw=1.1)

    fs.box(ax, 0.30, 3.90, 1.55, 0.72, "观测 o_t", fs=9.0, **inp)
    fs.box(ax, 2.20, 3.90, 1.45, 0.72, "编码器\n图像 → z", fs=8.6, **mod)
    fs.box(ax, 4.30, 3.72, 1.90, 0.96, "隐状态\n(h_t, z_t)", fs=9.0, **mod)

    fs.box(ax, 0.30, 1.45, 1.55, 0.75, "上一动作 a", fs=9.0, **inp)
    fs.box(ax, 2.20, 1.30, 1.55, 1.00, "序列模型\nGRU", fs=9.0, **mod)

    fs.box(ax, 6.70, 4.35, 2.30, 0.80, "解码器\n重建图像", fs=8.8, **mod)
    fs.box(ax, 6.70, 3.40, 2.30, 0.80, "奖励预测\n估计回报", fs=8.8, **mod)
    fs.box(ax, 6.70, 2.45, 2.30, 0.80, "继续预测\n估计是否终止", fs=8.8, **mod)
    fs.box(ax, 6.70, 0.90, 2.30, 0.90, "actor / critic\n只在想象里更新", fs=8.8, **rl)

    fs.arrow(ax, (1.85, 4.26), (2.20, 4.26), color=fs.MUTED)
    fs.arrow(ax, (3.65, 4.26), (4.30, 4.26), color=fs.MUTED)
    fs.arrow(ax, (1.85, 1.83), (2.20, 1.83), color=fs.MUTED)
    fs.arrow(ax, (3.75, 2.10), (4.75, 3.72), color=fs.MUTED)

    fs.arrow(ax, (6.20, 4.50), (6.70, 4.75), color=fs.MUTED)
    fs.arrow(ax, (6.20, 4.25), (6.70, 3.80), color=fs.MUTED)
    fs.arrow(ax, (6.20, 4.00), (6.70, 2.85), color=fs.MUTED)

    ax.plot([5.25, 5.25], [3.72, 1.35], color=fs.MUTED, lw=1.2, zorder=2,
            solid_capstyle="butt")
    fs.arrow(ax, (5.25, 1.35), (6.70, 1.35), color=fs.MUTED)
    fs.label(ax, 5.45, 2.52, "读隐状态", fs=8.2, color=fs.MUTED, ha="left")

    fs.label(ax, 5.00, 0.42, "世界模型用真实数据学预测，actor 只在想象轨迹上试动作。",
             fs=8.6, color=fs.MUTED)
    fs.save(fig, "ch10", "fig10-03")


if __name__ == "__main__":
    fig_loop()
    fig_gap()
    fig_dreamer()
