# -*- coding: utf-8 -*-
"""第 7 章插图：三代重建方法对比、一个高斯里装了什么、语义场查询。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Circle
from matplotlib.colors import LinearSegmentedColormap
import figstyle as fs


def fig_three_gens():
    """三代方法的五栏对照矩阵。"""
    fig, ax = fs.canvas(6.7, 4.35)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.62)

    LX = 0.05
    C0 = 1.68
    CW, CG = 2.68, 0.09
    COLORS = [fs.TEAL, fs.BLUE, fs.ACCENT]
    HEADS = ["SfM　稀疏重建\n约 2006", "NeRF　神经辐射场\n2020", "3DGS　高斯泼溅\n2023"]

    HY, HH = 5.80, 0.68
    for i, (h, c) in enumerate(zip(HEADS, COLORS)):
        x = C0 + i * (CW + CG)
        fs.box(ax, x, HY, CW, HH, h, fc="#FFFFFF", ec=c, tc=c, fs=8.8, lw=1.3, weight="bold")

    ROWS = [
        ("输入", ["几十到几百张照片\n顺序随意",
                  "照片 + 相机位姿\n位姿由 SfM 给",
                  "照片 + 位姿\n+ 稀疏点云"]),
        ("表示的\n是什么", ["几万个稀疏的\n三维特征点",
                            "一个 8 层网络\n记下整个场景",
                            "100 到 500 万个\n各向异性椭球"]),
        ("建一次\n要多久", ["十几分钟\n到几小时",
                            "10 万到 30 万次迭代\n单卡一到两天",
                            "6 到 51 分钟\n单卡训完"]),
        ("出一帧\n要多久", ["不能换视角\n只能看点云",
                            "800×800\n约 30 秒",
                            "1080p 每秒\n134 到 197 帧"]),
        ("机器人\n拿它做什么", ["给后两代\n做初始化",
                               "合成训练图\n反算深度",
                               "数字孪生\n实时预览"]),
    ]

    RH, RG = 0.97, 0.06
    for r, (lab, cells) in enumerate(ROWS):
        y = HY - 0.16 - RH - r * (RH + RG)
        fs.label(ax, LX + 0.06, y + RH / 2, lab, fs=8.5, color=fs.INK, ha="left")
        for i, t in enumerate(cells):
            x = C0 + i * (CW + CG)
            fs.box(ax, x, y, CW, RH, t, fc="#FFFFFF", ec="#D8DEE6", lw=0.9, fs=8.3)

    ax.text(5.0, 0.24, "时长与帧率取自两篇论文的报数，均为单卡、室内尺度场景",
            fontsize=8.0, color=fs.FAINT, ha="center", va="center")
    fs.save(fig, "ch07", "fig07-01")


def fig_gaussian():
    """一个高斯的五个量，以及许多高斯贴住一层表面。"""
    fig, ax = fs.canvas(6.7, 4.25)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.30)

    # ---------------- (a) 单个高斯 ----------------
    cx, cy, A, B, TH = 2.35, 4.85, 1.30, 0.50, 15.0
    t = np.radians(TH)
    ct, st = np.cos(t), np.sin(t)
    ax.add_patch(Ellipse((cx, cy), 2 * A, 2 * B, angle=TH, facecolor="#FBEEDD",
                         edgecolor=fs.ACCENT, lw=1.3, zorder=2))
    # 主轴
    ax.plot([cx - A * ct, cx + A * ct], [cy - A * st, cy + A * st],
            color=fs.MUTED, lw=0.9, zorder=4)
    # 次轴
    ax.plot([cx - B * st, cx + B * st], [cy + B * ct, cy - B * ct],
            color=fs.MUTED, lw=0.8, ls=(0, (3, 2)), zorder=4)
    # 参考水平线与旋转角
    ax.plot([cx - 0.86, cx], [cy, cy], color=fs.FAINT, lw=0.8, ls=(0, (3, 2)), zorder=4)
    arc = np.linspace(np.pi, np.pi + t, 40)
    ax.plot(cx + 0.56 * np.cos(arc), cy + 0.56 * np.sin(arc),
            color=fs.MUTED, lw=0.9, zorder=5)

    def dot(x, y, num, r=0.150):
        ax.add_patch(Circle((x, y), r, facecolor="white", edgecolor=fs.INK,
                            lw=0.9, zorder=9))
        ax.text(x, y - 0.006, num, fontsize=7.4, color=fs.INK, ha="center",
                va="center", zorder=10)

    dot(cx, cy, "1")
    dot(cx + 0.68 * ct, cy + 0.68 * st, "2")
    dot(cx - 1.33, cy - 0.67, "3")
    dot(cx + 0.27, cy + 0.43, "4")
    ax.plot([cx - 1.20, cx - 0.60], [cy - 0.57, cy - 0.20], color=fs.FAINT, lw=0.7, zorder=6)
    # 球谐：三条短射线，末端三个颜色
    for ang, col in ((-18, fs.GOLD), (-34, fs.PINK), (-50, fs.BLUE)):
        a = np.radians(ang)
        ax.plot([cx + 0.24 * np.cos(a), cx + 0.60 * np.cos(a)],
                [cy + 0.24 * np.sin(a) * 0.62, cy + 0.60 * np.sin(a) * 0.62],
                color=col, lw=1.1, zorder=6)
        ax.add_patch(Circle((cx + 0.60 * np.cos(a), cy + 0.60 * np.sin(a) * 0.62), 0.052,
                            facecolor=col, edgecolor="none", zorder=7))
    dot(cx + 0.95, cy - 0.30, "5")

    fs.label(ax, 0.28, 6.02, "(a) 一个高斯有五个量", fs=9, color=fs.INK, ha="left",
             weight="bold")

    items = [
        ("1", "位置　x, y, z", "3 个数，椭球的中心", fs.INK),
        ("2", "尺度　三个半轴长", "3 个数，决定扁还是长", fs.INK),
        ("3", "旋转　四元数", "4 个数，决定朝哪边歪", fs.INK),
        ("4", "不透明度　α", "1 个数，有多挡光", fs.INK),
        ("5", "球谐　16 × 3", "48 个数，颜色随方向怎么变", fs.ACCENT),
    ]
    for i, (num, name, note, col) in enumerate(items):
        y = 3.62 - i * 0.58
        ax.add_patch(Circle((0.30, y), 0.145, facecolor="#FFFFFF", edgecolor=col, lw=0.9, zorder=5))
        ax.text(0.30, y - 0.004, num, fontsize=7.4, color=col, ha="center", va="center", zorder=6)
        ax.text(0.56, y + 0.085, name, fontsize=8.5, color=col, ha="left", va="center")
        ax.text(0.56, y - 0.175, note, fontsize=8.0, color=fs.MUTED, ha="left", va="center")
    ax.text(0.28, 0.46, "加起来 59 个浮点数，一个高斯 236 字节",
            fontsize=8.2, color=fs.INK, ha="left", va="center")

    # ---------------- (b) 一层表面 ----------------
    fs.label(ax, 5.32, 6.02, "(b) 许多高斯贴住一层表面", fs=9, color=fs.INK,
             ha="left", weight="bold")

    # 圆球：截面是圆，只碰到一个点
    ax.add_patch(Rectangle((5.30, 2.72), 1.46, 0.26, facecolor="#EDEAE3",
                           edgecolor=fs.FAINT, lw=0.8, zorder=3))
    for i in range(3):
        ax.add_patch(Circle((5.58 + i * 0.44, 3.18), 0.20, facecolor="none",
                            edgecolor=fs.FAINT, lw=0.7, ls=(0, (2, 2)), zorder=3))
        ax.add_patch(Circle((5.58 + i * 0.44, 2.98), 0.036, facecolor=fs.FAINT,
                            edgecolor="none", zorder=5))
    fs.label(ax, 6.03, 2.40, "球只碰到一个点", fs=7.9, color=fs.MUTED, ha="center")

    # 扁椭球 + 竖直椭球：贴住一整段
    ax.add_patch(Rectangle((7.10, 2.72), 2.34, 0.26, facecolor="#EDEAE3",
                           edgecolor=fs.FAINT, lw=0.8, zorder=3))
    for i in range(4):
        ax.add_patch(Ellipse((7.38 + i * 0.52, 3.10), 0.72, 0.24, angle=-3 + i * 2,
                             facecolor="#FBEEDD", edgecolor=fs.ACCENT, lw=1.0, zorder=4))

    ax.add_patch(Rectangle((9.20, 2.98), 0.24, 1.62, facecolor="#EDEAE3",
                           edgecolor=fs.FAINT, lw=0.8, zorder=3))
    for i in range(3):
        ax.add_patch(Ellipse((9.10, 3.34 + i * 0.45), 0.22, 0.56, angle=5 - i * 3,
                             facecolor="#FBEEDD", edgecolor=fs.ACCENT, lw=1.0, zorder=4))
    ax.add_patch(Ellipse((9.03, 3.06), 0.64, 0.22, angle=-42,
                         facecolor="#F7E0C6", edgecolor=fs.GOLD, lw=1.1, zorder=5))
    fs.label(ax, 8.27, 2.40, "扁的贴住一整段", fs=7.9, color=fs.ACCENT, ha="center")

    fs.save(fig, "ch07", "fig07-02")


def fig_semantic():
    """一句话变成向量，再在场景里找出对应区域。"""
    fig, ax = fs.canvas(6.7, 4.15)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.20)

    # ---- 顶部流程 ----
    fs.box(ax, 0.20, 4.86, 2.55, 0.88, "一句话\n「能装水的容器」", fs=8.6, ec=fs.INK)
    fs.arrow(ax, (2.80, 5.30), (3.15, 5.30))
    fs.box(ax, 3.20, 4.86, 2.60, 0.88, "CLIP 文本编码器\n512 维", fs=8.6, ec=fs.INK)
    fs.arrow(ax, (5.85, 5.30), (6.20, 5.30))
    fs.box(ax, 6.25, 4.86, 2.30, 0.88, "句子向量 q\n512 个浮点", fs=8.6, ec=fs.BLUE, tc=fs.BLUE)

    fs.arrow(ax, (7.40, 4.80), (7.40, 4.32), color=fs.BLUE)
    fs.label(ax, 7.40, 4.12, "逐点做点积", fs=8.0, color=fs.BLUE, ha="center")

    # ---- 场景俯视 ----
    X0, X1, Y0, Y1 = 0.95, 9.05, 0.62, 3.86
    gx = np.linspace(X0, X1, 340)
    gy = np.linspace(Y0, Y1, 160)
    GX, GY = np.meshgrid(gx, gy)

    def blob(mx, my, sx, sy, amp):
        return amp * np.exp(-(((GX - mx) / sx) ** 2 + ((GY - my) / sy) ** 2))

    F = (blob(6.05, 2.30, 0.85, 0.70, 1.00)      # 马克杯
         + blob(7.72, 2.82, 0.62, 0.52, 0.58)     # 保温杯
         + blob(4.28, 2.46, 0.70, 0.58, 0.40)     # 盘子
         + blob(2.30, 1.52, 0.80, 0.58, 0.10))    # 纸巾盒
    F = F / F.max()

    cmap = LinearSegmentedColormap.from_list(
        "sem", ["#FFFFFF", "#FCEBD6", "#F7C79E", "#E98B58", "#BE3C0B"],
        N=256)
    ax.imshow(F, origin="lower", extent=[X0, X1, Y0, Y1], cmap=cmap, vmin=0.0,
              vmax=1.0, aspect="auto", zorder=1, interpolation="bilinear")
    ax.add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, facecolor="none",
                           edgecolor=fs.FAINT, lw=0.9, zorder=6))

    def obj_label(x, y, text, col):
        ax.text(x, y, text, fontsize=7.9, color=col, ha="center", va="center", zorder=10,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.4))

    # 马克杯
    ax.add_patch(Circle((6.05, 2.30), 0.33, facecolor="#FFFFFF", edgecolor=fs.INK, lw=1.2, zorder=7))
    ax.add_patch(Circle((6.05, 2.30), 0.26, facecolor="none", edgecolor=fs.MUTED, lw=0.8, zorder=7))
    ax.add_patch(Circle((6.39, 2.30), 0.11, facecolor="none", edgecolor=fs.INK, lw=1.0, zorder=7))
    ax.add_patch(Circle((6.05, 2.30), 0.49, facecolor="none", edgecolor=fs.ACCENT,
                        lw=1.3, ls=(0, (4, 2)), zorder=8))
    obj_label(6.05, 3.06, "马克杯　命中", fs.ACCENT)

    # 保温杯
    ax.add_patch(Ellipse((7.72, 2.82), 0.46, 0.46, facecolor="#F3F4F6",
                         edgecolor=fs.INK, lw=1.1, zorder=7))
    ax.add_patch(Ellipse((7.72, 2.82), 0.16, 0.16, facecolor="none",
                         edgecolor=fs.MUTED, lw=0.8, zorder=7))
    obj_label(7.72, 3.40, "保温杯　次之", fs.MUTED)

    # 盘子
    ax.add_patch(Ellipse((4.28, 2.46), 1.00, 0.76, facecolor="#FBF7F0",
                         edgecolor=fs.INK, lw=1.1, zorder=7))
    ax.add_patch(Ellipse((4.28, 2.46), 0.60, 0.44, facecolor="none",
                         edgecolor=fs.FAINT, lw=0.8, zorder=7))
    obj_label(4.28, 3.16, "盘子　弱", fs.MUTED)

    # 纸巾盒
    ax.add_patch(Rectangle((1.92, 1.30), 0.82, 0.44, facecolor="#F6F3EC",
                           edgecolor=fs.INK, lw=1.0, zorder=7))
    obj_label(2.33, 2.14, "纸巾盒　几乎为零", fs.MUTED)

    fs.label(ax, 1.05, 0.98, "桌面上每个位置都挂着一个向量，亮的地方就是和这句话最像的一块",
             fs=8.2, color=fs.MUTED, ha="left")
    fs.label(ax, 8.95, 3.66, "俯视", fs=7.8, color=fs.FAINT, ha="right")

    fs.save(fig, "ch07", "fig07-03")


if __name__ == "__main__":
    fig_three_gens()
    fig_gaussian()
    fig_semantic()
