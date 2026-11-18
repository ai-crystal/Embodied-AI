# 附录 B　延伸阅读

下面的篇目是按“读完能补上哪块”挑的，不是按影响力排的。每一条给一句读它的理由，正式出处与编号一并列出，方便直接检索原文。

## B.1　视觉与三维

- **Learning Transferable Visual Models From Natural Language Supervision**（Alec Radford, Jong Wook Kim, Chris Hallacy, et al.，2021）。想搞懂“为什么模型能认出没见过的杯子”，从这里开始。双塔对比学习，读完就明白开放词汇是怎么来的。 arXiv:2103.00020
- **Segment Anything**（Alexander Kirillov, Eric Mintun, Nikhila Ravi, et al.，2023）。提示式分割的代表作。给一个点或一个框就能切出物体，是机器人感知流水线里最常用的一块。 arXiv:2304.02643
- **Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data**（Lihe Yang, Bingyi Kang, Zilong Huang, et al.，2024）。单目深度估计的转折点。读它能知道“只有 RGB 也能估深度”做到了什么程度，以及哪里不可靠。 arXiv:2401.10891
- **ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereo and RGB-D Cameras**（Raul Mur-Artal, Juan D. Tardos，2016）。经典视觉 SLAM 的教科书级实现。前端跟踪、后端优化、回环检测三件事讲得最清楚。 arXiv:1610.06475

## B.2　位姿与抓取

- **PVNet: Pixel-wise Voting Network for 6DoF Pose Estimation**（Sida Peng, Yuan Liu, Qixing Huang, et al.，2018）。关键点投票路线，用像素投出关键点再解位姿。理解“遮挡下为什么还能估准”的好例子。 arXiv:1812.11788
- **FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects**（Bowen Wen, Wei Yang, Jan Kautz, et al.，2023）。把基础模型用到 6D 位姿上，给 CAD 或少量参考图就能用，不用为每个物体训练。 arXiv:2312.08344
- **Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes**（Martin Sundermeyer, Arsalan Mousavian, Rudolph Triebel, et al.，2021）。6-DoF 抓取生成的常用基线，把抓取预测成接触点，读完能理解平行夹爪为什么只需两个点。 arXiv:2103.14127

## B.3　学习与仿真

- **A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning**（Stephane Ross, Geoffrey J. Gordon, J. Andrew Bagnell，2010）。模仿学习必读。讲清行为克隆为什么会越走越偏，以及让专家补标注能补到什么程度。 arXiv:1011.0686
- **Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware**（Tony Z. Zhao, Vikash Kumar, Sergey Levine, et al.，2023）。动作块与时间集成的来源，也是低成本双臂 ALOHA 的方法篇。想复现示教学习先读它。 arXiv:2304.13705
- **Diffusion Policy: Visuomotor Policy Learning via Action Diffusion**（Cheng Chi, Zhenjia Xu, Siyuan Feng, et al.，2023）。扩散策略的原始论文。动作生成当去噪这件事，读完会有一个准确的直觉。 arXiv:2303.04137
- **Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots**（Cheng Chi, Zhenjia Xu, Chuer Pan, et al.，2024）。把采集成本打下来的代表作。手持夹爪加相机就能采数据，适合预算有限的团队。 arXiv:2402.10329
- **Proximal Policy Optimization Algorithms**（John Schulman, Filip Wolski, Prafulla Dhariwal, et al.，2017）。策略梯度的工程主力。公式不多，重点是裁剪和实现细节，做强化学习绕不开。 arXiv:1707.06347
- **Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor**（Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, et al.，2018）。连续控制的另一个主力，最大熵框架。和 PPO 对比着读，能知道各自的适用场景。 arXiv:1801.01290
- **Isaac Gym: High Performance GPU-Based Physics Simulation For Robot Learning**（Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, et al.，2021）。GPU 并行仿真的分水岭。读完能理解“几千个环境同时跑”为什么改变了训练周期。 arXiv:2108.10470
- **Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World**（Josh Tobin, Rachel Fong, Alex Ray, et al.，2017）。域随机化的经典论文，用纯仿真训练把策略搬到真机。只讲一个技巧，但讲透了。 arXiv:1703.06907

## B.4　大模型与机器人

- **Do As I Can, Not As I Say: Grounding Language in Robotic Affordances**（Michael Ahn, Anthony Brohan, Noah Brown, et al.，2022）。把语言模型接到技能库上的第一代做法。可行性与合理性相乘的思路，后来被反复借用。 arXiv:2204.01691
- **VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models**（Wenlong Huang, Chen Wang, Ruohan Zhang, et al.，2023）。把语言变成三维价值场，再用规划跟随。理解“语言怎么落到空间”最直观的一篇。 arXiv:2307.05973
- **RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control**（Anthony Brohan, Noah Brown, Justice Carbajal, et al.，2023）。VLA 的起点。把动作变成文本 token，让视觉语言模型直接输出动作。 arXiv:2307.15818
- **OpenVLA: An Open-Source Vision-Language-Action Model**（Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al.，2024）。开源 VLA 的代表，7B 参数、可微调、能在单卡上跑。想动手做 VLA 从它开始。 arXiv:2406.09246
- **π_0: A Vision-Language-Action Flow Model for General Robot Control**（Kevin Black, Noah Brown, Danny Driess, et al.，2024）。flow matching 动作头与 50 Hz 控制的代表。读它能理解为什么“动作要一段一段出”。 arXiv:2410.24164
- **GR00T N1: An Open Foundation Model for Generalist Humanoid Robots**（ NVIDIA,  :, Johan Bjorck, et al.，2025）。双系统思路的代表，慢的语义模型加快的动作模型，人形场景的工程取舍写得很清楚。 arXiv:2503.14734

## B.5　数据、基准与综述

- **Open X-Embodiment: Robotic Learning Datasets and RT-X Models**（Open X-Embodiment Collaboration, Abby O'Neill, Abdul Rehman, et al.，2023）。22 种本体、百万级轨迹的合集。想理解“跨本体数据为什么难统一”，读它的数据表。 arXiv:2310.08864
- **DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset**（Alexander Khazatsky, Karl Pertsch, Suraj Nair, et al.，2024）。在真实办公室与家庭里采的数据集，采集流程与失败样本的处理值得细看。 arXiv:2403.12945
- **CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks**（Oier Mees, Lukas Hermann, Erick Rosete-Beas, et al.，2021）。长程语言条件任务的经典基准，五连指令的成功率是它的招牌指标。 arXiv:2112.03227
- **LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning**（Bo Liu, Yifeng Zhu, Chongkai Gao, et al.，2023）。终身学习视角的基准，四套任务分别考迁移与遗忘。 arXiv:2306.03310
- **Evaluating Real-World Robot Manipulation Policies in Simulation**（Xuanlin Li, Kyle Hsu, Jiayuan Gu, et al.，2024）。把真机策略搬进仿真评测的尝试，讨论“仿真分数能不能代表真机”最认真的一篇。 arXiv:2405.05941
- **BLINK: Multimodal Large Language Models Can See but Not Perceive**（Xingyu Fu, Yushi Hu, Bangzheng Li, et al.，2024）。揭示多模态模型“看得见但看不懂”的评测。空间类题目上的差距一目了然。 arXiv:2404.12390
- **A Survey of Embodied AI: From Simulators to Research Tasks**（Jiafei Duan, Samson Yu, Hui Li Tan, et al.，2021）。综述，适合当索引。读完这本册子再翻它，能把论文摆到正确的位置上。 arXiv:2103.04918
