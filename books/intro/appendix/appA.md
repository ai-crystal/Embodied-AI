# 附录 A　术语表

按主题分组，同一主题的词放在一起，方便对照。第三列是一句话说明，够用就行；想看完整推导，顺着附录 B 的论文读原文。

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
| 神经辐射场 | neural radiance field（NeRF） | 用一个小网络记住整个场景的密度与颜色，可从新视角渲染 |
| 高斯泼溅 | 3D Gaussian splatting（3DGS） | 用上百万个带朝向的椭球表示场景，渲染快，编辑也方便 |
| 体渲染 | volume rendering | 沿光线累加颜色与不透明度，NeRF 与 3DGS 都用它出图 |
| 语义场 | semantic field | 每个体素或椭球挂一个语言特征向量，可以用一句话查位置 |
| 数字孪生 | digital twin | 把真实场景扫进仿真，得到一份可反复练手的副本 |

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
| 形闭合 | form closure | 靠几何包围卡住物体，摩擦为零也不脱手 |
| 接触点 | contact point | 手指或夹爪与物体真正接触的位置，抓取分析的起点 |
| 抓取矩阵 | grasp matrix | 把接触力映射成物体合力的矩阵，判断能不能顶住外力 |

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

## A.6　规划、控制与身体

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 构型空间障碍 | configuration space obstacle | 机器人任何部位碰到障碍时，对应的那一片关节角区域 |
| 膨胀 | inflation | 把障碍按机器人半径放大一圈，把"面接触"简化成"点不能进" |
| 路径规划 | path planning | 只关心几何上走不走得通，不关心速度和力 |
| 轨迹优化 | trajectory optimization | 在满足速度、加速度约束的前提下把路径磨光滑 |
| 快速扩展随机树 | rapidly-exploring random tree（RRT） | 在空间里随机撒点连成树，找到一条可行路径就停 |
| 概率路线图 | probabilistic roadmap（PRM） | 先撒点建一张图，之后在图上反复查路径 |
| A 星 | A* | 带启发式的图搜索，估计到终点的距离来少走弯路 |
| 模型预测控制 | model predictive control（MPC） | 每几十毫秒用模型往前推演一遍，只执行第一步 |
| 任务与运动规划 | task and motion planning（TAMP） | 上层定先做什么后做什么，下层定怎么走过去，两层交替 |
| 全身控制 | whole-body control（WBC） | 把平衡、手部任务、安全约束放进一个优化里分配力矩 |
| 零力矩点 | zero moment point（ZMP） | 地面反力合力矩为零的点，落在支撑多边形内才不会翻 |
| 线性倒立摆模型 | linear inverted pendulum model（LIPM） | 把行走简化成一个质点在可伸缩腿上前后摆 |
| 阻抗控制 | impedance control | 让末端表现得像弹簧加阻尼，碰到东西会退让而不是硬顶 |
| 力控 | force control | 直接控制接触力的大小，装配、打磨、擦桌子都要用 |
| 触觉 | tactile sensing | 接触处的压力、形变与滑动，视觉看不到的那部分 |
| 视触觉 | vision-based tactile sensing | 用相机拍弹性体的形变，把"手感"变成一张彩色图 |

## A.7　产业与落地

| 中文 | 英文 | 一句话说明 |
|---|---|---|
| 本体 | robot body / hardware platform | 机械结构与驱动、传感、算力的整机，不含算法 |
| 系统集成 | system integration | 把本体、相机、算法、工位拼成能连续跑的一套东西 |
| 场景运营 | deployment operation | 上线之后的运维、标定、数据回流与人工兜底 |
| 投资回收期 | payback period | 省下的人力与投入的成本相抵要多久 |
| 平均无故障时间 | mean time between failures（MTBF） | 两次故障之间的平均运行时长，衡量能不能连续跑 |
| 数据飞轮 | data flywheel | 部署越多、数据越多、模型越好，再带来更多部署 |
| 演示 | demo | 一次成功或一段剪辑过的视频，不等于能连续运行 |
