# -*- coding: utf-8 -*-
"""第 6 章插图：ViT 前向流程、CLIP 对比学习、四类特征需求对照。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common"))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import figstyle as fs


def fig_vit():
    """ViT 前向流程：切 patch、线性投影、位置编码、编码器、两种输出。"""
    fig, ax = fs.canvas(6.6, 2.9)
    ax.set_xlim(0, 9.4)
    ax.set_ylim(1.10, 5.3)

    # ---- 左端：原图（实心 3x3）与 patch 序列（散开 3x3）----
    gx, gy, cell = 0.30, 4.00, 0.2333
    for i in range(3):
        for j in range(3):
            c = "#E3D6C6" if (i + j) % 2 == 0 else "#D3C0AA"
            ax.add_patch(Rectangle((gx + i * cell, gy + j * cell), cell, cell,
                                   facecolor=c, edgecolor="white", lw=0.8, zorder=3))
    ax.add_patch(Rectangle((gx, gy), 3 * cell, 3 * cell, facecolor="none",
                           edgecolor=fs.INK, lw=1.0, zorder=4))

    gx2, gy2 = 0.30, 2.40
    cell2, gap2 = 0.20, 0.0667
    for i in range(3):
        for j in range(3):
            c = "#E3D6C6" if (i + j) % 2 == 0 else "#D3C0AA"
            ax.add_patch(Rectangle((gx2 + i * (cell2 + gap2), gy2 + j * (cell2 + gap2)),
                                   cell2, cell2, facecolor=c, edgecolor=fs.FAINT,
                                   lw=0.7, zorder=3))

    fs.label(ax, 0.65, 5.14, "图像", fs=8.4, color=fs.INK, va="bottom")
    fs.label(ax, 0.65, 4.80, "224×224×3", fs=8.2, color=fs.MUTED, va="bottom")
    fs.arrow(ax, (0.65, 3.94), (0.65, 3.24), color=fs.MUTED, lw=1.0)
    fs.label(ax, 0.65, 2.26, "196 个 patch", fs=8.2, color=fs.MUTED, va="top")
    fs.label(ax, 0.65, 1.96, "每个 16×16", fs=8.0, color=fs.FAINT, va="top")

    # ---- 主干：四个框 ----
    y0, h = 2.05, 1.50
    w, gap = 1.75, 0.28
    xs = [1.45 + i * (w + gap) for i in range(4)]
    texts = ["线性投影", "加 [CLS]\n与位置编码", "12 层\nTransformer", "输出特征"]
    shapes = ["196×16×16×3", "197×768", "197×768", "768 或 196×768"]
    for x, t, s in zip(xs, texts, shapes):
        fs.box(ax, x, y0, w, h, t, fc="#FFFFFF", ec=fs.INK, fs=8.6)
        fs.label(ax, x + w / 2, y0 - 0.12, s, fs=8.0, color=fs.MUTED, va="top")

    # patch 序列 -> 第一个框
    fs.arrow(ax, (1.12, 2.80), (1.41, 2.80), color=fs.MUTED, lw=1.0)
    # 框间箭头
    for i in range(3):
        fs.arrow(ax, (xs[i] + w + 0.02, y0 + h / 2), (xs[i + 1] - 0.02, y0 + h / 2),
                 color=fs.MUTED, lw=1.1)

    # 框 2 上方标注 [CLS]
    fs.label(ax, xs[1] + w / 2, y0 + h + 0.08, "+1 个 [CLS]", fs=8.0, color=fs.ACCENT, va="bottom")

    fs.label(ax, 4.7, 1.32, "形状按 224×224 输入、patch 边长 16 计算；左侧 3×3 网格为示意。",
             fs=8.0, color=fs.MUTED)
    fs.save(fig, "ch06", "fig06-01")


def fig_clip():
    """CLIP 双塔与批内相似度矩阵。"""
    fig, ax = fs.canvas(6.6, 3.75)
    ax.set_xlim(0, 12)
    ax.set_ylim(0.5, 7.3)

    # ---- 文本塔（上方横排）----
    fs.box(ax, 0.30, 6.10, 2.00, 1.00, "一只橘猫\n坐在沙发上", fc="#FBF3E8", ec=fs.GOLD, fs=8.4)
    fs.arrow(ax, (2.34, 6.60), (2.86, 6.60), color=fs.MUTED, lw=1.1)
    fs.box(ax, 2.90, 6.10, 2.10, 1.00, "文本编码器\nTransformer", fc="#FFFFFF", ec=fs.INK, fs=8.4)
    fs.arrow(ax, (5.04, 6.60), (5.16, 6.60), color=fs.MUTED, lw=1.1)
    fs.box(ax, 5.20, 6.10, 1.60, 1.00, "768 维\n文本嵌入", fc="#EFF3FA", ec=fs.BLUE, fs=8.4)

    # ---- 图像塔（左侧竖排）----
    fs.box(ax, 0.30, 4.40, 2.10, 0.80, "图像\n224×224×3", fc="#FBF3E8", ec=fs.GOLD, fs=8.4)
    fs.arrow(ax, (1.35, 4.36), (1.35, 4.14), color=fs.MUTED, lw=1.1)
    fs.box(ax, 0.30, 3.30, 2.10, 0.80, "图像编码器\nViT-L/14", fc="#FFFFFF", ec=fs.INK, fs=8.4)
    fs.arrow(ax, (1.35, 3.26), (1.35, 3.04), color=fs.MUTED, lw=1.1)
    fs.box(ax, 0.30, 2.20, 2.10, 0.80, "768 维\n图像嵌入", fc="#EFF3FA", ec=fs.BLUE, fs=8.4)

    # ---- 相似度矩阵 ----
    mx, my, cw, ch = 4.45, 1.05, 0.62, 0.62
    n = 6
    for i in range(n):
        for j in range(n):
            if i == j:
                fc, al = fs.ACCENT, 0.80
            elif (i, j) in ((0, 1), (1, 0)):
                fc, al = fs.GOLD, 0.40
            else:
                fc, al = "#DDE4EF", 1.0
            ax.add_patch(Rectangle((mx + j * cw, my + (n - 1 - i) * ch), cw, ch,
                                   facecolor=fc, alpha=al, edgecolor="white", lw=0.8, zorder=3))
    ax.add_patch(Rectangle((mx, my), n * cw, n * ch, facecolor="none",
                           edgecolor=fs.MUTED, lw=0.9, zorder=4))

    # 文本嵌入条（矩阵上方）
    for j in range(n):
        ax.add_patch(Rectangle((mx + j * cw, my + n * ch + 0.10), cw, 0.40,
                               facecolor="#EFF3FA", edgecolor=fs.BLUE, lw=0.7, zorder=3))
        fs.label(ax, mx + (j + 0.5) * cw, my + n * ch + 0.30, f"T{j + 1}", fs=8.0, color=fs.BLUE)
    # 图像嵌入条（矩阵左侧）
    for i in range(n):
        ax.add_patch(Rectangle((mx - 0.48, my + (n - 1 - i) * ch), 0.40, ch,
                               facecolor="#EFF3FA", edgecolor=fs.BLUE, lw=0.7, zorder=3))
        fs.label(ax, mx - 0.28, my + (n - 0.5 - i) * ch, f"I{i + 1}", fs=8.0, color=fs.BLUE)

    # 两塔输出接入矩阵
    fs.arrow(ax, (6.00, 6.06), (6.00, my + n * ch + 0.54), color=fs.BLUE, lw=1.1)
    fs.arrow(ax, (2.44, 2.60), (mx - 0.52, 2.60), color=fs.BLUE, lw=1.1)

    fs.label(ax, mx + n * cw / 2, 0.72, "行 i 是第 i 张图，列 j 是第 j 段文本",
             fs=8.2, color=fs.MUTED)
    fs.label(ax, 0.30, 1.80, "两个向量各自 L2 归一化\n再算余弦相似度", fs=8.2,
             color=fs.MUTED, ha="left", va="top")

    # ---- 右侧图例 ----
    lx, ly = 8.62, 3.95
    items = [(fs.ACCENT, 0.80, "正样本对（对角）"),
             (fs.GOLD, 0.40, "难负样本（同为猫）"),
             ("#DDE4EF", 1.0, "负样本对")]
    for k, (c, a, t) in enumerate(items):
        ax.add_patch(Rectangle((lx, ly - k * 0.56), 0.34, 0.32, facecolor=c, alpha=a,
                               edgecolor=fs.MUTED, lw=0.6, zorder=3))
        fs.label(ax, lx + 0.48, ly - k * 0.56 + 0.16, t, fs=8.2, color=fs.INK, ha="left")

    fs.label(ax, lx, 2.10, "批内 6 对图文", fs=8.2, color=fs.MUTED, ha="left", va="top")
    fs.label(ax, lx, 1.76, "CLIP 实际批大小 32768", fs=8.2, color=fs.MUTED, ha="left", va="top")
    fs.label(ax, lx, 1.42, "色块深浅为示意", fs=8.2, color=fs.FAINT, ha="left", va="top")

    fs.save(fig, "ch06", "fig06-02")


def fig_needs():
    """四类特征需求与四个骨干的定性对照。"""
    fig, ax = fs.canvas(6.6, 3.27)
    ax.set_xlim(0, 9.9)
    ax.set_ylim(0.30, 5.20)

    cols = ["ResNet-50", "ViT-B/16", "DINOv2", "CLIP"]
    rows = ["空间精度", "可供性", "时序稳定", "三维一致"]
    # 强 / 中 / 弱
    grades = [["中", "中", "强", "弱"],
              ["中", "中", "中", "弱"],
              ["中", "弱", "强", "弱"],
              ["弱", "弱", "强", "弱"]]
    cmap = {"强": ("#2F6B4F", "white"), "中": ("#D9AE45", fs.INK), "弱": ("#DCD6CC", fs.MUTED)}

    x0, y0, cw, chh = 3.20, 1.60, 1.30, 0.80
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            g = grades[i][j]
            fc, tc = cmap[g]
            yy = y0 + (3 - i) * chh
            ax.add_patch(Rectangle((x0 + j * cw, yy), cw, chh, facecolor=fc,
                                   edgecolor="white", lw=1.4, zorder=3))
            fs.label(ax, x0 + (j + 0.5) * cw, yy + chh / 2, g, fs=9.0, color=tc)
        fs.label(ax, x0 - 0.14, y0 + (3 - i) * chh + chh / 2, r, fs=8.8, color=fs.INK, ha="right")

    for j, c in enumerate(cols):
        fs.label(ax, x0 + (j + 0.5) * cw, y0 + 4 * chh + 0.12, c, fs=8.6,
                 color=fs.INK, va="bottom")

    # 图例
    lx, ly = 3.20, 0.92
    for k, g in enumerate(["强", "中", "弱"]):
        fc, tc = cmap[g]
        ax.add_patch(Rectangle((lx + k * 0.86, ly), 0.32, 0.30, facecolor=fc,
                               edgecolor=fs.MUTED, lw=0.6, zorder=3))
        fs.label(ax, lx + k * 0.86 + 0.42, ly + 0.15, g, fs=8.4, color=fs.INK, ha="left")
    fs.label(ax, 5.78, ly + 0.15, "定性判断，不是实测分数。", fs=8.2, color=fs.MUTED, ha="left")
    fs.label(ax, 3.20, 0.46, "CLIP 的强项是开放词汇语义，不在这四行里。", fs=8.2,
             color=fs.FAINT, ha="left")

    fs.save(fig, "ch06", "fig06-03")


if __name__ == "__main__":
    fig_vit()
    fig_clip()
    fig_needs()
