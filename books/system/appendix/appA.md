# 附录 A　数学与工具速查

这一章把书里反复用到的数学工具集中列出来，供查公式时翻。每个条目尽量给一句直觉解释，推导略去。

## A.1 向量与矩阵

向量写成列向量 $\mathbf{x}\in\mathbb{R}^n$，内积 $\mathbf{x}^\top\mathbf{y}=\sum_i x_i y_i$，几何意义是一个向量在另一个方向上的投影长度乘以对方长度。两个向量正交时内积为零。

矩阵 $\mathbf{A}\in\mathbb{R}^{m\times n}$ 表示从 $n$ 维到 $m$ 维的线性映射。秩 $\mathrm{rank}(\mathbf{A})$ 是映射后空间的维数，秩亏意味着有方向的信息被压没了。

方阵的逆只有在满秩时存在。实际计算中很少真的求逆，解线性方程组 $\mathbf{A}\mathbf{x}=\mathbf{b}$ 用分解（LU、Cholesky、QR）比求逆稳定得多，代价也更低。

特征值分解 $\mathbf{A}\mathbf{v}=\lambda\mathbf{v}$ 用来找矩阵的"不变方向"。对称正定矩阵的特征值全为正，它的特征向量构成一组正交基，这是协方差矩阵能用来做主成分分析（PCA）的原因。

奇异值分解 $\mathbf{A}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$ 对任意矩阵都成立，$\boldsymbol{\Sigma}$ 对角上的奇异值衡量各个方向被放大或缩小的倍数。条件数是最大奇异值与最小奇异值之比，条件数很大意味着输入的小扰动会被放大成输出的大误差，机器人在奇异位形附近遇到的正是这种情况。

## A.2 旋转的三种表示

**旋转矩阵** $\mathbf{R}\in SO(3)$ 满足 $\mathbf{R}^\top\mathbf{R}=\mathbf{I}$ 且 $\det\mathbf{R}=1$。它作用在向量上直接给出旋转后的坐标，串接旋转就是矩阵连乘。缺点是 9 个数只有 3 个自由度，冗余带来数值漂移，需要定期正交化。

绕 $x,y,z$ 轴分别旋转 $\alpha,\beta,\gamma$ 的基本矩阵是

$$
\mathbf{R}_x(\alpha)=
\begin{bmatrix}
1&0&0\\
0&\cos\alpha&-\sin\alpha\\
0&\sin\alpha&\cos\alpha
\end{bmatrix},
\quad
\mathbf{R}_z(\gamma)=
\begin{bmatrix}
\cos\gamma&-\sin\gamma&0\\
\sin\gamma&\cos\gamma&0\\
0&0&1
\end{bmatrix}.
$$

$\mathbf{R}_y(\beta)$ 同理，只是把 $\cos\beta$ 放在 $(1,1)$ 与 $(3,3)$ 位置，$\sin\beta$ 的符号按右手系排列。

**欧拉角**用三个角描述姿态，直观但有两种毛病。一是同一姿态有多组角表示，二是万向锁：当中间那个角转到 $\pm 90^\circ$ 时，第一个轴与第三个轴重合，失去一个自由度，此时姿态的微小变化会导致另外两个角剧烈跳变。所以欧拉角适合给人看，不适合在算法内部长期存储。

**四元数** $\mathbf{q}=(w,x,y,z)$，单位四元数满足 $w^2+x^2+y^2+z^2=1$。它用 4 个数表示 3 个自由度，没有奇异点，插值平滑（球面线性插值 slerp），所以姿态估计、IMU 融合、动画系统里普遍使用。两个四元数 $\mathbf{q}$ 与 $-\mathbf{q}$ 表示同一个旋转，这一点在比较姿态时要注意。

单位四元数转旋转矩阵的公式是

$$
\mathbf{R}=
\begin{bmatrix}
1-2(y^2+z^2)&2(xy-wz)&2(xz+wy)\\
2(xy+wz)&1-2(x^2+z^2)&2(yz-wx)\\
2(xz-wy)&2(yz+wx)&1-2(x^2+y^2)
\end{bmatrix}.
$$

## A.3 齐次变换

把旋转和平移打包成 $4\times4$ 矩阵

$$
\mathbf{T}=\begin{bmatrix}\mathbf{R}&\mathbf{t}\\ \mathbf{0}^\top&1\end{bmatrix},
$$

它的作用是把点 $\mathbf{p}$ 变成 $\mathbf{R}\mathbf{p}+\mathbf{t}$。写成齐次坐标后，坐标系串联就是矩阵连乘，$\mathbf{T}_{ac}=\mathbf{T}_{ab}\mathbf{T}_{bc}$ 表示从 $c$ 系到 $a$ 系的变换等于先到 $b$ 系再到 $a$ 系。求逆有闭式解

$$
\mathbf{T}^{-1}=\begin{bmatrix}\mathbf{R}^\top&-\mathbf{R}^\top\mathbf{t}\\ \mathbf{0}^\top&1\end{bmatrix},
$$

不必调用通用矩阵求逆。书里所有坐标链条都用这个记号，第 2 章与第 4 章的图 2-4、图 4-2 画的就是它。

## A.4 手眼标定

相机固定在机械臂末端时，末端到相机的变换 $\mathbf{T}_{ec}$ 未知，需要标定。让机械臂走两个位姿，相机观测同一个标定板，可以写出

$$
\mathbf{A}\mathbf{X}=\mathbf{X}\mathbf{B},
$$

其中 $\mathbf{A}$ 是两次末端位姿之间的相对变换（由机器人读数得到），$\mathbf{B}$ 是两次相机观测之间的相对变换（由标定板位姿得到），$\mathbf{X}$ 就是要求的 $\mathbf{T}_{ec}$。这类方程叫 $\mathbf{A}\mathbf{X}=\mathbf{X}\mathbf{B}$ 问题，经典解法是先解旋转再解平移。相机固定在支架上（眼在手外）时，方程形式一样，只是未知量换成基座到相机的变换。

## A.5 概率与估计

贝叶斯公式 $\mathrm{p}(x\mid z)=\mathrm{p}(z\mid x)\mathrm{p}(x)/\mathrm{p}(z)$ 是状态估计的骨架。$\mathrm{p}(x)$ 是先验，$\mathrm{p}(z\mid x)$ 是似然，$\mathrm{p}(x\mid z)$ 是后验。卡尔曼滤波就是把这件事在高斯假设下做在线递推，预测步用运动模型把先验往前推，更新步用观测修正。

协方差矩阵 $\boldsymbol{\Sigma}$ 的对角线是各分量的方差，非对角线是相关性。两个随机变量的相关系数等于协方差除以标准差之积，取值在 $[-1,1]$。

最小二乘解 $\hat{\mathbf{x}}=(\mathbf{A}^\top\mathbf{A})^{-1}\mathbf{A}^\top\mathbf{b}$ 在观测数多于未知数时使用。加正则项变成 $\hat{\mathbf{x}}=(\mathbf{A}^\top\mathbf{A}+\lambda\mathbf{I})^{-1}\mathbf{A}^\top\mathbf{b}$，用来抑制病态问题，$\lambda$ 越大解越靠近零。

梯度下降的更新是 $\mathbf{x}\leftarrow\mathbf{x}-\eta\nabla f(\mathbf{x})$，$\eta$ 是步长。步长太大会震荡，太小会慢。带动量的版本把历史梯度累加，用来穿过狭长的谷地。

二次规划（QP）的标准形式是

$$
\min_{\mathbf{x}}\ \tfrac12\mathbf{x}^\top\mathbf{H}\mathbf{x}+\mathbf{f}^\top\mathbf{x}
\quad\text{s.t.}\quad \mathbf{A}\mathbf{x}\le\mathbf{b},
$$

$\mathbf{H}$ 半正定时有唯一全局最优。全身控制（第 16 章）把多个任务的误差写成二次代价，把关节限位与力矩上限写成线性约束，最后求解的就是这种问题。

## A.6 常用指标

**成功率**用二项分布描述。$n$ 次独立试验中成功 $k$ 次，成功率估计 $\hat{p}=k/n$，标准误约 $\sqrt{\hat{p}(1-\hat{p})/n}$。$n=20$、$\hat{p}=0.9$ 时标准误约 0.067，95% 置信区间大致是 $[0.77,1.0]$，宽得足以让两个"90%"没有统计差别。

**ADD**（Average Distance of model points）衡量位姿误差

$$
\mathrm{ADD}=\frac{1}{m}\sum_{i=1}^{m}\big\|(\mathbf{R}\mathbf{x}_i+\mathbf{t})-(\mathbf{R}'\mathbf{x}_i+\mathbf{t}')\big\|_2,
$$

$\mathbf{x}_i$ 是模型上的采样点，$\mathbf{R},\mathbf{t}$ 是预测位姿，带撇的是真值。对称物体要换成 ADD-S，把对应关系改成最近点

$$
\mathrm{ADD\text{-}S}=\frac{1}{m}\sum_{i=1}^{m}\min_{j}\big\|(\mathbf{R}\mathbf{x}_i+\mathbf{t})-(\mathbf{R}'\mathbf{x}_j+\mathbf{t}')\big\|_2 .
$$

**位姿误差的分解**习惯写成平移误差（米或毫米）与旋转误差（度）两个数，因为它们的来源和影响不同：平移误差决定抓不抓得到，旋转误差决定夹爪姿态对不对。

**跟踪误差**常用均方根误差 RMSE，单位与原始量一致；控制领域也常用绝对误差均值 MAE 与最大误差，后者对安全性更关键。

**时延**用从传感器曝光到动作下发的端到端时间衡量，中位数说明常态，95 分位数说明最坏情况，工程上更关心后者，因为最坏情况决定了系统能跑多快而不抖。

## A.7 单位与量级

长度用米，力用牛顿，力矩用牛·米，角度在公式里用弧度、在参数表里用度。1 kgf 约 9.8 N，一个苹果约 1 N，一瓶 500 毫升矿泉水约 5 N。

相机内参用像素，焦距常写成 $f_x,f_y$，与物理焦距的关系是 $f_x=f/\text{像素宽度}$。深度单位统一用米，传感器原始输出常是毫米，混用是常见 bug。

时间上，控制循环常用 1 kHz（周期 1 ms），视觉常用 10 到 30 Hz，策略推理常在 3 到 10 Hz。这三档频率差了三个数量级，系统集成时必须显式处理，第 19 章会展开。
