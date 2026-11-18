# 附录 D　工具链速查

这一章列的是上手时会用到的几套工具，以及最小可跑的示例。版本变化很快，命令的具体参数请以官方文档为准，这里重点说明每套工具解决什么问题、在链条里处于什么位置。

## D.1 ROS 2

ROS 2 是机器人领域最常用的中间件，它解决的事情说起来简单：让几十个程序（节点）互相传数据，并且能分布在多台机器上。

几个核心概念值得先弄清楚。

**节点**（node）是一个进程，负责一件小事，比如读相机、跑检测、算逆解。**话题**（topic）是单向的广播通道，发布者往上面写，订阅者从上面读，两边互不知道对方存在。**服务**（service）是请求-应答模式，调用后等结果。**动作**（action）适合长耗时任务，能反馈进度、能取消，机械臂"移动到某处"通常用它。

QoS 是 ROS 2 相对 ROS 1 的关键改进。可以给话题指定可靠性（可靠传输还是尽力而为）、历史深度、时限。相机图像用"尽力而为、只保留最新一帧"，否则队列积压会让画面越来越滞后。这个设置在系统集成时非常关键。

安装与最小示例（Ubuntu 22.04 加 ROS 2 Humble）：

```bash
sudo apt install ros-humble-desktop
source /opt/ros/humble/setup.bash

# 终端 1：发布一个字符串
ros2 run demo_nodes_cpp talker

# 终端 2：订阅并打印
ros2 run demo_nodes_py listener

# 查看当前有哪些话题与节点
ros2 topic list
ros2 node list

# 录包与回放，调试时几乎必用
ros2 bag record -o mybag /camera/image_raw /joint_states
ros2 bag play mybag
```

自己写一个发布者，Python 版本大约二十行：

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__("talker")
        self.pub = self.create_publisher(String, "chatter", 10)
        self.create_timer(0.5, self.tick)

    def tick(self):
        msg = String()
        msg.data = "hello"
        self.pub.publish(msg)

rclpy.init()
rclpy.spin(Talker())
```

## D.2 MuJoCo

MuJoCo 是接触动力学仿真器，模型用 MJCF（XML）描述，读起来比 URDF 清楚，接触求解稳定，是强化学习研究的常用选择。它现在是开源的，Python 绑定叫 `mujoco`。

```bash
pip install mujoco
```

```python
import mujoco

model = mujoco.MjModel.from_xml_path("scene.xml")
data = mujoco.MjData(model)

for _ in range(1000):
    data.ctrl[:] = 0.0          # 给执行器指令
    mujoco.mj_step(model, data)
    print(data.qpos[:3])        # 打印基座位姿
```

MJCF 里最常改的几项是关节类型（hinge、slide、free）、执行器增益、几何体的摩擦系数与接触参数。调不通时先看 `mj_step` 是否稳定，再看接触参数是否让物体抖动。

## D.3 Isaac Lab

Isaac Lab 建在 NVIDIA Isaac Sim 之上，用 GPU 并行跑几千个环境，专为大规模强化学习设计。第 10 章讲的"把训练从周变成小时"，靠的就是这种并行。

```bash
# 官方推荐用 conda 建环境，然后
pip install isaaclab
# 训练一个四足行走任务（任务名随版本变化）
python scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Velocity-Flat-Anymal-C-v0 --headless
```

它需要 RTX 显卡与较新的驱动，第一次启动会编译着色器，可能等十几分钟。训练日志里重点看平均回报与 episode 长度，后者先涨说明策略学会了活下来。

## D.4 LeRobot

LeRobot 是 Hugging Face 维护的机器人学习库，把数据集格式、策略模型、训练脚本、真机部署都打包在一起，适合复现模仿学习与 VLA 的最小闭环。

```bash
pip install lerobot

# 查看可用数据集
python -m lerobot.datasets 2>/dev/null || true

# 训练一个 ACT 策略（数据集与设备按需替换）
python -m lerobot.scripts.train \
  --dataset.repo_id=lerobot/aloha_sim_insertion_human \
  --policy.type=act \
  --output_dir=outputs/act_demo \
  --wandb.enable=false
```

数据集采用 Parquet 加视频的格式，一条 episode 包含多路相机画面、关节状态、动作与语言指令。自己采数据时最容易出问题的地方是时间戳对齐，相机帧率与控制频率不一致会导致动作与画面错位半帧到两帧。

## D.5 策略部署的常见参数

部署一个训练好的策略，需要确认下面这些量，缺一个就会出现"训练好好的，真机不动"。

- 观测的归一化方式（均值方差还是 min-max），训练与部署必须一致。
- 图像尺寸与裁剪、颜色通道顺序（RGB 还是 BGR）。
- 控制频率（Hz）与动作的含义（关节位置、关节速度、末端位姿增量）。
- 动作块的执行方式（整块执行还是时间集成）。
- 关节顺序与符号约定（不同厂商的 URDF 顺序常常不同）。

## D.6 一张最小系统清单

要把上面这些拼成一个能跑的系统，通常还需要下面几类组件。

- 相机驱动与标定工具（内参用棋盘格，手眼用标定板）。
- 机械臂驱动（厂商 SDK 或者 ros2_control 的硬件接口）。
- 抓取与位姿的推理服务（可以是本地 GPU，也可以是局域网内的另一台机器）。
- 可视化与调试（RViz、Foxglove 一类工具，用来确认坐标系是否一致）。
- 日志与回放（把相机、关节、动作、时间戳一起录下来，出问题时才能复盘）。

坐标系不一致是这套系统里最高频的错误来源。出现"点云在 RViz 里位置不对"时，先确认每个 TF 的时间戳与父子关系，再看外参是不是用了旧标定。
