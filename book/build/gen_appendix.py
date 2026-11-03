# -*- coding: utf-8 -*-
"""由 refs.json 生成附录 C（参考文献与延伸阅读）。

用法: python gen_appendix.py
输出: book/appendix/appC.md
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
ROOT = os.path.dirname(BOOK)
REFS = os.path.join(HERE, "refs.json")
OUT = os.path.join(BOOK, "appendix", "appC.md")

GROUPS = [
    ("C.1　感知与视觉表征", [
        "resnet", "vit", "detr", "clip", "dinov2", "sam", "sam2",
        "depthanything", "spatialvlm", "blink"]),
    ("C.2　三维重建与定位", [
        "nerf", "gaussian_splatting", "orbslam2", "droidslam"]),
    ("C.3　位姿估计与抓取", [
        "posecnn", "pvnet", "foundationpose", "graspnet", "dexnet",
        "contactgraspnet", "dexgraspnet"]),
    ("C.4　场景理解与地图", [
        "conceptgraphs", "habitat", "thor", "alfred", "minedojo"]),
    ("C.5　强化学习", [
        "dqn", "ddpg", "ppo", "sac", "dreamerv3", "decision_transformer", "diffuser"]),
    ("C.6　仿真与仿真到真实", [
        "domain_randomization", "isaacgym", "rma", "parkour", "humanoid_transformer"]),
    ("C.7　模仿学习与操作策略", [
        "dagger", "diffusion_policy", "act", "mobile_aloha", "transporter",
        "cliport", "peract", "rvt", "diffuser_actor3d", "umi", "robocat"]),
    ("C.8　语言模型与高层规划", [
        "saycan", "code_as_policies", "voxposer", "palm_e", "vima",
        "inner_monologue", "progprompt", "react", "voyager", "gato"]),
    ("C.9　视觉-语言-动作模型", [
        "rt1", "rt2", "openvla", "octo", "pi0", "pi05", "gr00t", "rdt"]),
    ("C.10　机器人数据", [
        "openx", "droid", "robomind", "data_scaling"]),
    ("C.11　评测基准", [
        "calvin", "libero", "simplerenv", "behavior1k", "robocasa",
        "metaworld", "rlbench"]),
    ("C.12　世界模型与空间智能", [
        "vjepa", "genie", "unisim", "cosmos"]),
    ("C.13　规划", [
        "rrtstar"]),
    ("C.14　综述与工具", [
        "embodied_survey", "foundation_robot_survey", "lerobot"]),
]

HEAD = """# 附录 C　参考文献与延伸阅读

按主题分组，同一组内按发表年份排序。每一项给出作者、标题、年份与 arXiv 编号，便于直接检索原文。标 ★ 的是建议先读的入门篇目，标 ▲ 的是综述或教材类文献。

"""


def authors(r):
    au = r.get("authors") or []
    au = [a.replace(" and ", " ") for a in au]
    if len(au) > 3:
        return ", ".join(au[:3]) + ", et al."
    return ", ".join(au)


def entry(r):
    title = r["title"].replace("$", "").replace("\\", "")
    year = r.get("year") or ""
    arx = r.get("arxiv") or ""
    s = f"{authors(r)}. {title}. {year}."
    if arx:
        s += f" arXiv:{arx}"
    return s


STAR = {"ppo", "sac", "diffusion_policy", "rt2", "openvla", "openx", "act", "pi0",
        "saycan", "clip", "sam", "nerf", "dqn", "domain_randomization", "rrtstar",
        "vjepa", "genie", "umi", "calvin", "libero", "dreamerv3", "action_chunk"}
SURVEY = {"embodied_survey", "foundation_robot_survey", "lerobot"}


def main():
    refs = {r["key"]: r for r in json.load(open(REFS, encoding="utf-8"))}
    out = [HEAD]
    used = set()
    for title, keys in GROUPS:
        items = [refs[k] for k in keys if k in refs]
        if not items:
            continue
        items.sort(key=lambda r: (r.get("year") or 0, r["title"]))
        out.append(f"## {title}\n")
        for r in items:
            mark = "★ " if r["key"] in STAR else ("▲ " if r["key"] in SURVEY else "")
            out.append(f"- {mark}{entry(r)}")
            used.add(r["key"])
        out.append("")
    rest = [r for k, r in refs.items() if k not in used]
    if rest:
        out.append("## C.15　其他\n")
        for r in sorted(rest, key=lambda r: r.get("year") or 0):
            out.append(f"- {entry(r)}")
        out.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(out))
    print("appC.md:", len(used) + len(rest), "条")


if __name__ == "__main__":
    main()
