---
title: "题解：群星"
date: 2026-01-13
category: "题解"
summary: "题意 给你 n 个有理数 piqi，请找到最大的一个正有理数 ab，使得对于所有的 i∈[1,n]，均存在 k∈ N+ 满足 piqi=k ab。 你只需要输出答案对 109+"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/zb4f1qz8
slug: zb4f1qz8
---

## 题意

给你 $n$ 个有理数 $\dfrac{p_i}{q_i}$，请找到最大的一个正有理数 $\dfrac{a}{b}$，使得对于所有的 $i\in[1,n]$，均存在 $k\in \mathbb N^+$ 满足 $\dfrac{p_i}{q_i}=k\cdot \dfrac{a}{b}$。
		
你只需要输出答案对 $10^9+7$ 取模的结果即可。

$1\le n\le 400$，$\sum n\le 2\times10^5$，$1\le p_i,q_i\le 10^{18}$，$p_i,q_i\not\equiv0\pmod{10^9+7}$。

## 题解

本题想法来源于 [[THUPC 2024 决赛] 朔望](https://www.luogu.com.cn/problem/P10548)。
### $p_i=1$

:::info[具体做法]
采用 [P5655](https://www.luogu.com.cn/problem/P5655) 的做法即可。

我们有：
$$\text{lcm}(a_1,\dots,a_i)=\text{lcm}(a_1,\dots,a_{i-1})\cdot\dfrac{a_i}{\gcd(a_i,\text{lcm}(a_1,\dots,a_{i-1}))}$$
		
那么令 $b_i=\dfrac{\text{lcm}(a_1,\dots,a_{i})}{\text{lcm}(a_1,\dots,a_{i-1})}$，有：
$$b_i=\dfrac{a_i}{\gcd(a_i,\prod_{j=1}^{i-1}b_j)}$$
		
其中 $b_i$ 的含义即为 $a_i$ 中比 $a_{1\sim i-1}$ 多出的贡献。由于 $\gcd$ 的性质，分母等于 $\gcd(a_i,\prod_{j=1}^{i-1}b_j\bmod a_i)$。

时间复杂度 $O(\sum (n^2+n\log v))$，期望得分 $15$ 分。
:::


### $O(n^3\log v)$
:::info[具体做法]
需要求出

$$\gcd_{i=1}^n\left(p_i\cdot\prod_{j\ne i} q_j\right)$$
增量加数，加入一个 $i(i\ge 2)$ 时会将之前的答案乘上 $q_i$ 并且与 $x=p_i\cdot\prod_{j<i} q_{j}$ 取 $\gcd$。
		
由于值域极大，考虑类比前述 $\text{lcm}$ 做法，将答案拆解为 $b_{1\sim n}$ 的乘积。
		
加入 $i$ 时，若 $i=1$ 则初始化 $b_i=p_i$，否则初始化 $b_i=q_i$。
		
初始化数组 $c_{1\sim i}$：$c_i=p_i$，$\forall j\in[1,i),c_j=q_j$。那么 $c$ 数组的乘积就表示 $x$。
		
我们枚举 $j$，求出 $b_j$ 与此时 $x$ 的 $\gcd$，记作 $v$，则将 $b_j$ 赋值为 $v$，将 $x$ 除去 $v$。由于 $x$ 是用 $\prod c$ 表示的，我们需要再枚举一个 $c_k$。
		
需要 $O(n^3)$ 次 $\gcd$，时间复杂度 $O(\sum n^3\log v)$，期望得分 $20$ 分。
:::

### $O(n^3)$
:::info[具体做法]
上述做法中，对所有 $c_k$ 做 $\gcd$ 是浪费的。

考虑到 $c_i$ 最终除去的为：

$$\dfrac{\gcd\left(b_j,\prod_{k=1}^i c_k\right)}{\gcd\left( b_j,\prod_{k=1}^{i-1} c_k\right)}$$

令 $s_i$ 表示 $\left(\prod_{k=1}^i c_k\right)\bmod{b_j}$，$d_i$ 表示 $\gcd(b_{j},s_i)$，显然 $\dfrac{d_i}{d_{i-1}}$ 只有 $O(\log v)$ 个位置不为 $1$，目标为判断是否有 $d_{i-1}=d_{i}$。
		
考察 $d_{i-1}=d_{i}$ 即 $\gcd(b_j,s_{i-1})=\gcd(b_j,s_i)$ 成立的条件。对每一质因子 $p$ 考虑，若 $b_j,s_{i-1},s_{i}$ 中分别有 $x,y,z$ 个 $p$，其中 $y\le z$ 恒成立，上式成立要求 $\min(x,y)=\min(x,z)$，等价于 $\min(x,z)\le y$，对应回原式即为 $s_{i-1}\bmod d_i=0$。
		
从右向左依次求出 $d_i$ 即可。
		
时间复杂度 $O(\sum (n^3+n^2\log^2 v))$，期望得分 $40$ 分。
:::
### $\sum n\le 10^4$

使用 Pollard-Rho 进行质因数分解。

时间复杂度 $O(\sum (nv^{1/4}+n\cdot\text{poly}\log(nv)))$，期望得分 $10$ 分。
### $O(n^2\log v)$

之前的做法似乎没有优化空间了，质因数分解也难以进行。

事实上，我们并不需要进行彻底的质因数分解。考虑对 $a_{1\sim n}$ 进行类质因数分解，求出一组互质的数 $p_{1\sim k}$ 作为基底，将 $a_{1\sim n}$ 分解为这些基底的幂次乘积。

具体地，
- 减量构造，将所有 $a_n$ 的质因数删去。
- 找出 $a_{1\sim n-1}$ 中与 $a_n$ 不互质的所有数，记作集合 $P$；
- 维护一个集合 $S$，初始 $S=\{a_n\}$；
- 枚举 $P$ 中的所有数 $x$，分离出所有 $x$ 与 $a_n$ 的公共质因子部分，记作 $x'$，将 $x'$ 加入集合 $S$。
- 重复执行：
	- 找到 $S$ 中不互质的两个整数 $p,q$，若找不到则停止；
   - 向 $S$ 中加入 $\gcd(p,q)$ 并将 $p,q$ 分别除以 $\gcd(p,q)$，删除可能出现的 $1$。
- 递归为 $n-1$ 规模的子问题。

每个数每次被加入集合 $P$ 后，质因子个数必定减少，故总的 $|P|$ 是 $O(n\omega(v))$ 的。

暴力执行以上所有操作，瓶颈为找出集合 $P$。

总时间复杂度 $O(\sum(n^2\log v+n\cdot\text{poly}\log (nv)))$，期望得分 $60$ 分。

### $O(n^2)$

考虑优化复杂度瓶颈，更快速地找出集合 $P$。

对 $1\sim n-1$ 建立线段树，维护区间的乘积，对 $a_n$ 取模。

自上至下搜索，若区间中所有数均与 $a_n$ 互质则停止返回。这可以使用记录的区间乘积来判断。

总时间复杂度 $O(\sum(n^2+n\cdot\text{poly}\log (nv)))$，期望得分 $95\sim100$ 分。
