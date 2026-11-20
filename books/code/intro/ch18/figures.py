# -*- coding: utf-8 -*-
"""第 18 章插图：产业链五层、可靠性差距、开放问题地图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import matplotlib.pyplot as plt
import figstyle as fs


def fig_chain():
    """产业链五层：每层的产出、典型玩家、钱在哪。"""
    fig, ax = fs.canvas(6.6, 4.9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.6)

    # 列位置与宽度
    c1x, c1w = 0.22, 1.96
    c2x, c2w = 2.30, 2.72
    c3x, c3w = 5.14, 2.32
    c4x, c4w = 7.58, 2.20

    # 表头
    heads = [(c1x + c1w / 2, "层"), (c2x + c2w / 2, "产出"),
             (c3x + c3w / 2, "典型玩家"), (c4x + c4w / 2, "钱在哪")]
    for x, s in heads:
        fs.label(ax, x, 7.02, s, fs=9.0, color=fs.MUTED)

    rows = [
        ("① 零部件", fs.GREEN, "减速器、丝杠、电机\n力传感器、编码器",
         "精密制造厂\n十年以上的工艺", "毛利三成上下\n受出货量限制"),
        ("② 本体", fs.BLUE, "结构、关节模组\n标定、一致性",
         "整机厂、车企\n无人机厂转过来", "多数还在亏\n看规模与返修率"),
        ("③ 模型与数据", fs.PURPLE, "权重、数据集\n仿真资产、标注",
         "大模型团队\n数据采集服务商", "边际成本低\n收入靠项目"),
        ("④ 系统集成", fs.GOLD, "工装、节拍、安全\n验收与售后",
         "行业集成商\n按项目收费", "现金流最好\n人效低，难复制"),
        ("⑤ 场景运营", fs.ACCENT, "按件或按月收费\n承担停机与赔付",
         "运营商、终端用户\n自建团队", "唯一有复利\n靠单点密度"),
    ]

    h, gap = 1.04, 0.17
    for i, (name, color, out, player, money) in enumerate(rows):
        y = 0.35 + (len(rows) - 1 - i) * (h + gap)
        fs.box(ax, c1x, y, c1w, h, name, fc=color, ec=color, tc="white",
               fs=9.4, weight="bold", rounded=0.03)
        fs.box(ax, c2x, y, c2w, h, out, fc="#FFFFFF", ec="#C9D2DC", lw=0.9, fs=8.4)
        fs.box(ax, c3x, y, c3w, h, player, fc="#FFFFFF", ec="#C9D2DC", lw=0.9, fs=8.4)
        fs.box(ax, c4x, y, c4w, h, money, fc="#FBF7F0", ec="#DCD3C6", lw=0.9, fs=8.4)

    fs.save(fig, "ch18", "fig18-01")


def fig_gap():
    """研究演示与产品门槛之间的可靠性差距。"""
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    fig.subplots_adjust(left=0.115, right=0.975, top=0.93, bottom=0.17)

    xs = [0, 1, 2, 3]
    vals = [8, 2, 0.5, 0.15]
    labs = ["单一工位\n同一动作", "同厂\n换品类", "换场地\n换产线", "开放家庭\n长尾任务"]
    notes = ["约 8 h", "约 2 h", "约 0.5 h", "约 0.15 h"]

    ax.set_yscale("log")
    ax.set_ylim(0.05, 3000)
    ax.set_xlim(-0.62, 3.62)

    # 产品门槛区
    ax.axhspan(40, 1000, color=fs.BLUE, alpha=0.06, zorder=0)
    ax.plot([-0.58, 3.58], [40, 40], color=fs.BLUE, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.plot([-0.58, 3.58], [1000, 1000], color=fs.BLUE, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.text(-0.56, 44, "上线门槛 40 h", fontsize=8.4, color=fs.BLUE, va="bottom", ha="left")
    ax.text(-0.56, 1080, "规模化门槛 1000 h", fontsize=8.4, color=fs.BLUE, va="bottom", ha="left")

    ax.bar(xs, [v - 0.05 for v in vals], width=0.52, bottom=0.05,
           color=fs.ACCENT, alpha=0.82, edgecolor=fs.INK, linewidth=0.8, zorder=3)
    for x, v, n in zip(xs, vals, notes):
        ax.text(x, v * 1.35, n, ha="center", va="bottom", fontsize=8.6, color=fs.INK)

    ax.set_xticks(xs)
    ax.set_xticklabels(labs, fontsize=9.0, color=fs.MUTED)
    ax.set_ylabel("无人干预连续运行时长（小时）", fontsize=9.6, color=fs.INK)
    ax.set_xlabel("场景的开放程度", fontsize=9.6, color=fs.INK)

    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", labelsize=8.8)
    ax.set_yticks([0.1, 1, 10, 100, 1000])
    ax.set_yticklabels(["0.1", "1", "10", "100", "1000"])
    ax.grid(True, axis="y", color=fs.GRID, lw=0.6)
    ax.set_axisbelow(True)

    ax.annotate("", xy=(3.42, 900), xytext=(3.42, 52),
                arrowprops=dict(arrowstyle="<->", color=fs.FAINT, lw=0.9))
    ax.text(3.30, 190, "缺口\n1 到 3 个\n数量级", fontsize=8.2, color=fs.MUTED,
            ha="right", va="center", linespacing=1.6)

    fs.save(fig, "ch18", "fig18-02")


def fig_map():
    """开放问题地图：五块区域与它们之间的耦合。"""
    fig, ax = fs.canvas(6.6, 4.6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.0)

    top = [
        ("感知", "看得清，摸不着", "相机、深度、语义成熟\n受力、温度、滑移靠猜"),
        ("学习", "会模仿，不举一反三", "五十条示教就能上手\n换物体、换房间就掉点"),
        ("控制", "单步准，长程散", "1 kHz 底层很成熟\n三步以上误差开始累积"),
    ]
    bottom = [
        ("数据", "能采，养不起", "公开轨迹一百万条以上\n匹配你这张桌子的极少"),
        ("评测", "能测，不可比", "仿真基准很多，排名可复现\n真机数字没人复现"),
    ]

    h = 2.15
    w = 2.72
    xs = [0.30, 3.54, 6.78]
    boxes = {}
    for x, (name, tone, body) in zip(xs, top):
        y = 4.15
        fs.box(ax, x, y, w, h, "", fc="#FFFFFF", ec=fs.INK, lw=1.0, rounded=0.03)
        fs.label(ax, x + w / 2, y + h - 0.40, name, fs=10.4, weight="bold")
        fs.label(ax, x + w / 2, y + h - 0.78, tone, fs=8.4, color=fs.ACCENT)
        fs.label(ax, x + w / 2, y + 0.72, body, fs=8.1, color=fs.MUTED)
        boxes[name] = (x, y, w, h)

    bw = 4.40
    bxs = [0.30, 5.55]
    for x, (name, tone, body) in zip(bxs, bottom):
        y = 1.00
        fs.box(ax, x, y, bw, h, "", fc="#FBF7F0", ec=fs.INK, lw=1.0, rounded=0.03)
        fs.label(ax, x + bw / 2, y + h - 0.40, name, fs=10.4, weight="bold")
        fs.label(ax, x + bw / 2, y + h - 0.78, tone, fs=8.4, color=fs.ACCENT)
        fs.label(ax, x + bw / 2, y + 0.72, body, fs=8.4, color=fs.MUTED)
        boxes[name] = (x, y, bw, h)

    dash = dict(color=fs.FAINT, lw=1.0, ls=(0, (4, 3)))
    # 控制 -> 评测
    fs.arrow(ax, (8.14, 4.12), (8.14, 3.19), **dash)
    fs.label(ax, 8.28, 3.66, "结果", fs=8.2, color=fs.MUTED, ha="left")
    # 评测 -> 数据
    fs.arrow(ax, (5.51, 2.05), (4.74, 2.05), **dash)
    fs.label(ax, 5.12, 2.26, "选数据", fs=8.2, color=fs.MUTED)
    # 数据 -> 学习
    fs.arrow(ax, (2.08, 3.16), (4.28, 4.12), **dash)
    fs.label(ax, 2.30, 3.66, "训练", fs=8.2, color=fs.MUTED, ha="left")

    fs.label(ax, 5.0, 0.55, "五块互相咬住，很难单点突破", fs=8.6, color=fs.FAINT)
    fs.save(fig, "ch18", "fig18-03")


if __name__ == "__main__":
    fig_chain()
    fig_gap()
    fig_map()
