---
title: "典藏 tricks"
date: 2022-11-20
category: "解题思路"
tags: ["杂项"]
summary: "已经不是 tricks 的形状了。 数据结构 1. 可以考虑若询问 i 和询问 j 成包含关系时，i 与 j 的答案关系。只考虑当前不被包含的询问，则 k∈[li,ri] 的 "
math: true
top: 3
hidden: true
source: https://www.luogu.com.cn/article/rx9no3rg
slug: rx9no3rg
---

已经不是 tricks 的形状了。

## 数据结构
1. 可以考虑若询问 $i$ 和询问 $j$ 成包含关系时，$i$ 与 $j$ 的答案关系。只考虑当前不被包含的询问，则 $k\in[l_i,r_i]$ 的 $i$ 是一段连续的询问，不妨以询问编号为下标建立数据结构。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1957&pid=3)）
2. 对 $x\le A,y\le B,z\le C$ 修改，最终查询全局值一类问题，考虑对 $z$ 轴做扫描线，二维问题可用线段树解决。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1946&pid=2)）
3. 带修改，取一段区间进行 $\text{dp}$，不妨考虑 $f_r=kf_{l-1}+b$ 之类可复合的形式。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1942&pid=2)）
4. 模数非质数时进行除法，仅有 $p$ 的质因子需要特殊维护。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1930&pid=1)，[$\text{Sasha and a Very Easy Test}$](https://www.luogu.com.cn/problem/CF1109E)）
0. 点对权值 $\min,\max$ 等查询找支配点对。
5. 对于序列维不好维护，不妨对序列维扫描线，维护每个时刻的值。
6. 历史和想不到 tag 怎么推就想矩乘怎么做。
7. 减半报警器。
8. 排序作为（分块）瓶颈时，考虑预处理排序/离线统一排序。
9. 区间取反可以同时维护取反后的结果，取反时直接交换。
11. 路径问题可以考虑限制一个点为叶子，不断删叶子求解。（5378）
12. 猫树分治代替线段树分治，设操作数为 $m$，序列长为 $n$，修改查询复杂度分别为 $c_1,c_2$，时间复杂度从 $O(mc_1\log n+nc_2)$ 变为 $O(mc_1+nc_2\log n)$。（5338）
13. 双栈模拟队列、单 $\log$ 代价单栈模拟队列。（uoj693）
14. 二进制分组。
15. 线段树维护假在线 `push_back` 和 `pop_back`。（uoj191）
16. 直径结论拓展：树上一个点到一个点集内最远的点一定是点集内直径端点之一。维护子树、前缀直径等。
17. 颜色段均摊可方便求解将 $f_{l,r}$ 划分为若干矩形的问题。（5338，P9970）
18. 最值分治上枚举短区间二分有时只有 $O(1)$ 种答案，可提前二分。（5392，P10169）

## 动态规划
1. $f_i=\max f_j+1$ 一类的，不妨考虑将 $i$ 用数据结构存在 $f_i$ 的位置，在数据结构上二分找到最大的满足转移限制的点 $j$。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1960&pid=2)）
2. 树上问题只关心一条路径时可以考虑区间 $\text{dp}$ 上树。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1948&pid=0)）
3. 区间 $\text{dp}$ 遇到 $f_{l,r}=\sum_{k,[k]}f_{l,k}+f_{k,r}$ 一类的，不妨考虑分别对 $l,r$ 维护树状数组 $f_{l,k}$ 之和，$f_{k,r}$ 之和。转移顺序：$r,1\to n$，$l,r\to 1$。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1948&pid=2)，[$\text{Random IS}$](https://www.luogu.com.cn/problem/AT_arc108_e)）
4. 交换定义域与值域。将 $0/1$ 从值域交换至定义域可降维，从定义域转换至值域可考虑 `bitset` 优化（5361）。
5. 多想状态是否可用区间及相关信息描述。
6. 求 $\sum_{i}a_ic_i=X$ 的 $\{c_i\}$ 的组数，并且 $n,a_i$ 都很小而 $X$ 很大的题目可以考虑数位 DP。（[$\text{Link}$](https://www.luogu.com.cn/problem/CF1290F)）
7. wqs 二分。
8. 拉格朗日插值。
9. $01$ 序列交换问题，相对位置不变。
10. 矩阵乘法时考虑什么时候可以转成向量乘矩阵优化复杂度。
11. 所求问题的子问题的动态规划状态数少时考虑 DP 套 DP。
12. 能否枚举答案？
13. 状态中是否有两维乘积小于等于 $n$？是否有两维不需要同时存在？
14. NTT 优化树上背包：轻重链剖分后维护非重儿子乘积，多次利用分治 NTT 即可。
15. 转移只与左右端点有关的区间 DP，考虑在网格图上描述。
16. 排列问题，考虑按值域做连续段 DP。
17. 一些优化 DP 的矩乘用稀疏矩阵乘法可以优化复杂度。
18. DP 方程组可考虑将每个 DP 值用其它 DP 值表示并递推。

## 字符串
1. $\text{KMP Fail}$ 树上祖先对应此前缀的所有 $\text{Border}$，不妨考虑倍增、$\text{dfs}$ 序等。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1954&pid=2)）
2. $\text{Trie}$ 树合并的复杂度其实是 $O(\min(s_1,s_2))$ 的。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1941&pid=1)）
3. $\text{KMP Fail}$ 树上 $\sum_{i}\text{dis}(i,i+1)=O(n)$。

## 数学
1. 划分区间，对每个区间的和的 $\gcd$ 就是每个 $r$ 处前缀和的 $\gcd$。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1941&pid=0)）
2. $\binom{n}{m}\bmod2=[m\subseteq n]$，可以互相转化。结论可拓展到高进制。结论可拓展到多项式系数。
3. 考虑钦定第一个（最后一个）合法（不合法）位置。
0. 正难则反正难则反正难则反。
0. $\text{popcount}$ 拆成各位之和。
0. $(\sum a)^2$ 拆成 $\sum a(\sum a)$（交换求和顺序）。
1. $v=\sum_i[v\ge i]$。
8. $mod=p^q$，维护多项式 $f(px)$。（5331，P10045）
9. $\forall i<j<k,i\text{ xor }k>\min(i\text{ xor }j,j\text{ xor }k)$。

## 杂项
1. 贪心邻项交换排序。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1947&pid=2)，[$\text{Google Code Jam}$](https://www.luogu.com.cn/problem/CF277D)）
5. 取 $a\sim b$ 个石子，$\text{SG}$ 值是有循环节的，可以 $O(1)$ 求。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1943&pid=0)）
6. 竞赛图最短路最大值为 $2$。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1939&pid=1)）
8. 考虑序列上 $i$ 有最大右端点 $w_i$ 使得 $[i,w_i]$ 合法，且 $w_i\le w_{i+1}$ 的问题，考虑分治，对于 $[l,r]$，若 $w_l=w_r$，则将区间赋值并退出，否则取中点递归。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1937&pid=2)，[$\text{Decinc Dividing}$](https://www.luogu.com.cn/problem/CF1693D)）
9. 树，点 $i$ 带权在 $[1,i-1]$ 中随机父亲，点 $\forall j>i$ 在点 $i$ 子树内的概率是相等的。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1936&pid=1)，[过程](https://www.luogu.com.cn/paste/f6t667rn)）
7. 看到浮点数输出就想在精度上突破（特别是概率期望相关）。
8. 竞赛图缩点呈链状（枚举最后一个强连通分量大小）。
9. 有看似意义不大的意外的小数据范围，考虑同余最短路（转圈）。
10. 求期望操作次数，推势能函数，每进行一次操作使势能函数变化量为一。
11. 答案与 $\gcd$ 相关时可能上界很小。
12. 所求为分数但是复杂度不方便求逆元时可以计算分子分母，在需要时求逆降低复杂度。
13. 很多时候贡献可以交换枚举顺序来考虑。
14. 善用增量法。（[$\text{Link}$](https://www.luogu.com.cn/problem/CF1286E)）
15. 求 $A$ 能否操作变成 $B$，如果操作可反向，则将 $A,B$ 同时往一个方向操作，如果最后 $A,B$ 重合则答案为是。
16. 排列问题观察逆排列性质。
17. 善用调整法。
18. 序列有序当且仅当对于所有 $v$，大于等于它的形成一段后缀。
18. $\min,\max$ 相关 $\text{dp}$ 问题，是否可以保留一行前 $n$ 大？（5300，THUWC2024A）
19. 某些看似复杂的递推式可以被分成足够少段计算。（5345，P5083）
20. 若干集合交集为空，并集为全集，考虑容斥交为 $X$，并为 $Y$，枚举 $X\cup Y$，则每种所有集合 $X\cup Y$ 位都相同的都唯一对应一种 $X,Y$，可考虑类似拓展。
21. 多次背包求 $x$ 个数和为 $y$ 方案数可用多项式快速幂做到 $\sum y^2\log x$（暴力）或者 $\sum y\log y$（NTT）。
22. 为多个位置二分并对答案取 $\max$，记一次检查复杂度为 $c$，复杂度为 $O(nc\log V)$，若以随机顺序先检查 $ans-1$ 处是否可行，可行再二分则复杂度变为 $O(nc+c\log n\log V)$。
23. 竞赛图考虑补图。

## 问题的转化
1. $\text{Hall}$ 定理：一个二分图有完美匹配，当且仅当二分图其中一个点集的子集向另外一个点集连边，任意这样的子集所能连到的对应的节点集合大小大于等于当前集合。判断存在性，通常用于二分。
3. 与 $S$ 有交的集合数为 $U$ 的子集数减去 $U/S$ 的子集数。图有性质时，可配合上面这条使用求出点集内向多少个点连了边。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1947&pid=1)，[$\text{Medals}$](https://www.luogu.com.cn/problem/AT_arc106_e)）
7. $x\bmod y=x-y\lfloor\dfrac x y\rfloor$ 用来拆和式。（[$\text{Link}$](http://192.168.102.138/JudgeOnline/problem.php?cid=1937&pid=1)）
4. 求前 $k$ 大的值的和转化为二分第 $k$ 大，求 $\ge x$ 的数的个数。
5. 总和可以转为期望乘以方案数，合法方案数可以转为合法概率乘以总方案数。
6. 要求不出现或者全出现（出现仅一次）考虑 $\text{xor hashing}$。
10. 数特殊图连通块考虑给每个连通块选个代表元进行代表元计数。
8. 操作对区间进行，考虑差分变为配对的单点操作。（[$\text{Link}$](https://www.luogu.com.cn/problem/P3543)）
9. 奇偶位分开考虑。
10. 一般图难做的问题考虑随机染色转化为二分图。（5290）
11. 点分治合并果子把多子树合并转化为双子树合并，可以消除不同子树限制。
12. 最小割问题考虑用多个 $0,1$ 变量刻画，看作 $\sum_{(u,v,w)}[a_u=1][a_v=0]w$，反之亦然。
