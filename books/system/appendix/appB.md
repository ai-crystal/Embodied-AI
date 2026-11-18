# 附录 B　术语中英对照

术语按主题分组，同一主题内按中文拼音顺序排列。英文列中的写法是文献里最常见的形态，写法有分歧的给出括号里的别称。

## B.1 身体与机构

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 构型空间 | configuration space (C-space) | 所有关节角组成的高维空间，一个点代表一个姿态 |
| 关节 | joint | 两个连杆之间的可动连接 |
| 自由度 | degree of freedom (DoF) | 系统能独立改变的运动量个数 |
| 末端执行器 | end effector | 装在机械臂末端、直接与物体作用的部件 |
| 工作空间 | workspace | 末端能够到达的位置集合 |
| 冗余 | redundancy | 自由度多于任务所需数量 |
| 奇异位形 | singularity | 雅可比降秩、末端某些方向失去运动能力的位形 |
| 齐次变换 | homogeneous transform | 把旋转与平移打包成 $4\times4$ 矩阵 |
| 雅可比矩阵 | Jacobian | 关节速度到末端速度的线性映射 |
| 正运动学 | forward kinematics | 由关节角算末端位姿 |
| 逆运动学 | inverse kinematics | 由末端位姿反解关节角 |
| 四元数 | quaternion | 无奇异点的姿态表示 |
| 万向锁 | gimbal lock | 欧拉角在特定角度失去一个自由度 |
| 平行夹爪 | parallel jaw gripper | 两指平行开合的夹持器 |
| 吸盘 | vacuum gripper | 靠负压吸附的末端工具 |
| 欠驱动 | underactuated | 控制输入少于自由度 |

## B.2 感知与三维

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 内参 | intrinsic parameters | 焦距与主点，描述相机内部的投影关系 |
| 外参 | extrinsic parameters | 相机相对世界或基座的位姿 |
| 针孔模型 | pinhole model | 最基本的透视投影模型 |
| 视差 | disparity | 同一物点在左右视图中的像素差 |
| 点云 | point cloud | 一组带坐标的三维点 |
| 体素 | voxel | 三维空间的规则小立方体单元 |
| 八叉树 | octree | 按八分递归划分空间的树结构 |
| 截断符号距离场 | truncated signed distance field (TSDF) | 每个体素存到最近表面的带符号距离，截断在薄层内 |
| 欧氏符号距离场 | Euclidean signed distance field (ESDF) | 到最近障碍的距离与梯度，用于避障 |
| 占据栅格 | occupancy grid | 每个格子存被占据的概率 |
| 同时定位与建图 | simultaneous localization and mapping (SLAM) | 一边估计自身位姿一边建图 |
| 回环检测 | loop closure | 认出回到过的地方并修正累计漂移 |
| 位姿 | pose | 位置加姿态，共 6 个自由度 |
| 六维位姿估计 | 6D pose estimation | 从图像估计物体的旋转与平移 |
| 实例分割 | instance segmentation | 区分同类物体的不同个体并给出掩码 |
| 提示式分割 | promptable segmentation | 用点、框、文本提示指定要分割的对象 |
| 开放词汇 | open vocabulary | 能处理训练时没见过的类别名称 |
| 可供性 | affordance | 物体相对于某个行动者能提供的操作可能性 |
| 抓取位姿 | grasp pose | 夹爪接近物体时的位置与朝向 |
| 力闭合 | force closure | 接触力能抵抗任意方向外力的抓取状态 |
| 摩擦锥 | friction cone | 接触点不滑动的力方向集合 |

## B.3 学习与决策

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 马尔可夫决策过程 | Markov decision process (MDP) | 用状态、动作、奖励、转移描述序贯决策 |
| 策略 | policy | 从观测到动作的映射 |
| 值函数 | value function | 从某状态出发的期望累计回报 |
| 动作价值 | action-value function | 在某状态采取某动作后的期望累计回报 |
| 贝尔曼方程 | Bellman equation | 值函数的递推关系 |
| 经验回放 | experience replay | 把历史转移存起来重复采样 |
| 目标网络 | target network | 用滞后更新的副本稳定训练 |
| 策略梯度 | policy gradient | 直接对策略参数求梯度 |
| 优势函数 | advantage function | 动作相对平均水平好多少 |
| 广义优势估计 | generalized advantage estimation (GAE) | 用折扣与偏差折中估计优势 |
| 近端策略优化 | proximal policy optimization (PPO) | 用裁剪限制更新幅度的策略梯度方法 |
| 软演员评论家 | soft actor-critic (SAC) | 最大熵框架下的离线策略算法 |
| 行为克隆 | behavior cloning (BC) | 用示教数据做监督学习 |
| 协变量偏移 | covariate shift | 执行时遇到的观测分布与训练分布不一致 |
| 数据集聚合 | dataset aggregation (DAgger) | 让专家标注学生自己走到的状态 |
| 动作块 | action chunk | 一次预测连续多步动作 |
| 扩散策略 | diffusion policy | 用去噪过程生成动作序列 |
| 流匹配 | flow matching | 学习从噪声到动作的连续变换 |
| 域随机化 | domain randomization | 训练时随机化环境参数以提升迁移 |
| 仿真到真实 | sim-to-real | 把仿真里学到的策略迁移到真机 |
| 世界模型 | world model | 预测动作后果的内部模型 |
| 模型预测控制 | model predictive control (MPC) | 滚动求解有限时域最优控制 |
| 任务与运动规划 | task and motion planning (TAMP) | 符号层任务规划与几何层运动规划交替求解 |

## B.4 大模型与机器人基础模型

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 视觉-语言-动作模型 | vision-language-action model (VLA) | 输入图像与指令、输出动作的模型 |
| 视觉Transformer | vision transformer (ViT) | 把图像切成 patch 后用注意力处理 |
| 对比语言图像预训练 | contrastive language-image pre-training (CLIP) | 用图文配对做对比学习 |
| 自监督学习 | self-supervised learning | 用数据自身构造监督信号 |
| 基础模型 | foundation model | 大规模预训练、可迁移到多种下游任务 |
| 动作标记化 | action tokenization | 把连续动作离散成词表里的 token |
| 动作专家 | action expert | 接在视觉语言主干后专门输出动作的模块 |
| 双系统 | dual system | 慢的语义模型加快的动作模型 |
| 低秩适配 | low-rank adaptation (LoRA) | 只训练低秩增量参数的微调方法 |
| 联合嵌入预测 | joint embedding predictive architecture (JEPA) | 在表征空间预测未来 |
| 空间推理 | spatial reasoning | 判断位置、朝向、距离、包含关系的能力 |

## B.5 控制、系统与评测

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 比例积分微分控制 | proportional-integral-derivative control (PID) | 按误差、误差累积、误差变化率调节 |
| 阻抗控制 | impedance control | 让末端表现得像弹簧加阻尼 |
| 导纳控制 | admittance control | 由力测偏差反推位置修正 |
| 力位混合控制 | hybrid force-position control | 部分方向控力、部分方向控位置 |
| 全身控制 | whole-body control (WBC) | 在多个任务与约束间分配关节力矩 |
| 零力矩点 | zero moment point (ZMP) | 地面反力合力矩为零的点 |
| 线性倒立摆模型 | linear inverted pendulum model (LIPM) | 把行走简化成质点加伸缩腿 |
| 状态估计 | state estimation | 由带噪观测推断系统状态 |
| 卡尔曼滤波 | Kalman filter | 高斯假设下的递推贝叶斯估计 |
| 实时操作系统 | real-time operating system (RTOS) | 保证响应时限的操作系统 |
| 服务质量 | quality of service (QoS) | 中间件里可靠性、时限、队列策略的配置 |
| 看门狗 | watchdog | 监测进程是否卡死并触发恢复的机制 |
| 平均无故障时间 | mean time between failures (MTBF) | 可靠性指标 |
| 安全性完整性等级 | safety integrity level (SIL) | 功能安全标准里的风险等级 |
| 遥操作 | teleoperation | 人远程操纵机器人 |
| 人工接管 | human takeover | 系统失败时由人接手 |
| 评测基准 | benchmark | 统一的场景、任务与指标集合 |
| 置信区间 | confidence interval | 估计值的不确定性范围 |
