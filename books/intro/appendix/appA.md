# 附录 A　术语表

按主题分组，每组内按中文拼音排序。第三列是一句话说明，够用就行；想看完整推导，顺着附录 B 的论文读原文。

## A.1　身体与机构

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 构型空间 | configuration space | 所有关节角组成的高维空间，机器的一个姿态就是里面的一个点 |
| 关节 | joint | 两根连杆之间的可动连接 |
| 减速器 | reducer | 装在电机与关节之间，把转速换成力矩 |
| 静稳定 | static stability | 不靠主动控制也能站住的状态 |
| 零力矩点 | zero moment point（ZMP） | 地面反力合力矩为零的那个点，落在支撑多边形内才不翻 |
| 末端执行器 | end effector | 装在机械臂末端、直接与物体打交道的部件 |
| 奇异位形 | singularity | 某些方向突然动不了的姿态，附近关节会猛转 |
| 齐次变换 | homogeneous transform | 把旋转和平移打包成一个 $4\times4$ 矩阵，用来串坐标系 |
| 冗余 | redundancy | 自由度多于任务所需，同一末端位姿有无穷多组解 |
| 逆运动学 | inverse kinematics | 由末端位姿反算关节角，可能多解也可能无解 |
| 平行夹爪 | parallel jaw gripper | 两指平行开合的夹持器，工业上最常见 |
| 欠驱动 | underactuated | 控制输入少于自由度，例如靠重力与接触被动成形的多指手 |
| 四元数 | quaternion | 用四个数表示姿态，没有奇异点，工程里常用 |
| 万向锁 | gimbal lock | 欧拉角在特定角度退化，丢一个自由度 |
| 腕部相机 | wrist camera | 装在机械臂末端的相机，眼在手上，近距离看清 |
| 正运动学 | forward kinematics | 由关节角算末端位姿，唯一且便宜 |
| 自由度 | degree of freedom（DoF） | 机器能独立改变的运动量个数 |
| 工作空间 | workspace | 末端能到达的位置集合 |

## A.2　感知与三维

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 八叉树 | octree | 把空间按八等分递归切分，适合稀疏点云 |
| 不可观 | unobservable | 数据里根本没有的信息，算法再强也估不出来，例如单目的绝对尺度 |
| 点云 | point cloud | 一组带三维坐标的点，深度反投影就得到它 |
| 法向 | normal | 表面上某点的朝向，用于配准与抓取评估 |
| 回环检测 | loop closure | 认出“这个地方来过”，用它纠正累计漂移 |
| 截断符号距离场 | truncated signed distance field（TSDF） | 每个体素存到最近表面的带符号距离，截断在薄层内 |
| 内参 | intrinsics | 焦距与主点，描述像素与射线的关系 |
| 欧氏符号距离场 | Euclidean signed distance field（ESDF） | 每个体素存到最近障碍的距离，避障时取梯度即可 |
| 视差 | disparity | 同一个点在左右两张图上的像素差，双目的深度就靠它 |
| 手眼标定 | hand-eye calibration | 求相机与末端之间的固定变换，装一次标一次 |
| 体素 | voxel | 三维空间里的规则小立方体，点云的降采样单位 |
| 同时定位与建图 | simultaneous localization and mapping（SLAM） | 一边估自己的位姿一边建图，两者互相依赖 |
| 外参 | extrinsics | 相机相对基座或末端的位姿 |
| 位姿 | pose | 位置加姿态，共 6 个自由度 |
| 针孔模型 | pinhole model | 最基本的透视投影模型，一个像素对应一条射线 |
| 占据栅格 | occupancy grid | 每个格子记“被占据的概率”，规划器最常用的地图 |
| 主点 | principal point | 光轴与像平面的交点，内参里的 cx、cy |

## A.3　位姿与抓取

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 可供性 | affordance | 物体相对某个行动者能提供的操作可能，例如把手可以拉 |
| 力闭合 | force closure | 接触力能抵抗任意方向外力，抓起来不会滑 |
| 摩擦锥 | friction cone | 接触点不滑动时，力方向允许的锥形范围 |
| 六维位姿估计 | 6D pose estimation | 从图像估计物体的旋转与平移 |
| 实例分割 | instance segmentation | 把同类物体的不同个体分开并给出掩码 |
| 提示式分割 | promptable segmentation | 用点、框或文字提示指定要切哪块 |
| 开放词汇 | open vocabulary | 能处理训练时没见过的类别名 |
| 对称等价解 | symmetric ambiguity | 对称物体转一个角度看起来一样，位姿不唯一 |
| 抓取位姿 | grasp pose | 夹爪接近物体时的位置与朝向 |
| 抓取矩形 | grasp rectangle | 2D 抓取的五元组表示（中心、角度、开度、质量） |

## A.4　学习与仿真

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 策略 | policy | 从观测到动作的映射，训练的目标就是它 |
| 策略梯度 | policy gradient | 直接对策略参数求梯度，按回报好坏调概率 |
| 动作块 | action chunk | 一次预测连续多步动作，缓解推理慢的问题 |
| 动作价值 | action-value function | 在某状态做某动作之后能拿到的期望回报 |
| 广义优势估计 | generalized advantage estimation（GAE） | 用折扣折中偏差与方差的优势估计 |
| 价值函数 | value function | 从某状态出发的期望累计回报 |
| 经验回放 | experience replay | 把历史转移存起来重复采样，提高数据利用率 |
| 扩散策略 | diffusion policy | 用去噪过程生成动作序列，能表达多模态 |
| 流匹配 | flow matching | 学习从噪声到动作的连续速度场，步数比扩散少 |
| 马尔可夫决策过程 | Markov decision process（MDP） | 用状态、动作、奖励、转移描述序贯决策 |
| 模仿学习 | imitation learning | 从人的示教里学策略，行为克隆是其中最简单的一种 |
| 目标网络 | target network | 用滞后更新的副本算目标值，稳定训练 |
| 强化学习 | reinforcement learning | 靠试错最大化累计回报 |
| 软演员评论家 | soft actor-critic（SAC） | 最大熵框架下的离线策略算法，连续控制常用 |
| 时间集成 | temporal ensembling | 把多轮预测的同一时刻动作加权平均，抖动用它压 |
| 示教 | demonstration | 人操作一遍录下来的轨迹，含图像、动作与时间戳 |
| 稀疏奖励 | sparse reward | 只有成功那一刻才给分，学起来极慢 |
| 域随机化 | domain randomization | 训练时随机化光照、摩擦、延迟，逼策略学会适应 |
| 仿真到真实 | sim-to-real | 把仿真里训好的策略搬到真机 |
| 协变量偏移 | covariate shift | 执行时遇到的观测分布与训练时不一样，误差越滚越大 |
| 行为克隆 | behavior cloning | 把示教当成监督学习，观测进、动作出 |
| 优势函数 | advantage function | 某动作比平均水平好多少 |
| 演员评论家 | actor-critic | 一个网络出动作、一个网络估价值，一起训练 |

## A.5　大模型与系统

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 动作标记化 | action tokenization | 把连续动作切成离散 token，让语言模型能输出 |
| 对比学习 | contrastive learning | 拉近正样本、推远负样本，CLIP 的核心 |
| 基础模型 | foundation model | 大规模预训练、能迁移到多种下游任务的模型 |
| 视觉-语言-动作模型 | vision-language-action model（VLA） | 输入图像与指令、直接输出动作的模型 |
| 世界模型 | world model | 预测“做了这个动作之后会怎样”的内部模型 |
| 双系统 | dual system | 慢的语义模型负责想，快的动作模型负责动 |
| 提示 | prompt | 给模型的输入指令，可以是文字、图像或点 |
| 任务与运动规划 | task and motion planning（TAMP） | 符号层定顺序、几何层定路径，交替求解 |
| 时延预算 | latency budget | 从曝光到动作下发允许花的总时间 |
| 遥操作 | teleoperation | 人远程操纵机器人，采集数据的主要方式 |
| 置信区间 | confidence interval | 估计值的不确定范围，20 次试验时宽得吓人 |
| 中间件 | middleware | 让几十个程序互相传数据的软件层，ROS 2 是代表 |
| 抓取检测 | grasp detection | 从图像或点云直接给出抓取位姿的模块 |
