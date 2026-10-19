---
title: "题解：AT_xmascon20_f Famous in Russia"
date: 2025-06-05
category: "题解"
summary: "Link 本题的 DP 部分相当复杂，现有的题解都不是很清晰，故我尝试描述得更加细致一些。 题意 对于给定的长为 n 的正整数序列 a1 n,b1 n，定义 f(a1 n,b1"
math: true
top: 2
source: https://www.luogu.com.cn/article/nb1dyxwd
slug: nb1dyxwd
---

[$\text{Link}$](https://www.luogu.com.cn/problem/AT_xmascon20_f)

本题的 DP 部分相当复杂，现有的题解都不是很清晰，故我尝试描述得更加细致一些。
## 题意

对于给定的长为 $n$ 的正整数序列 $a_{1\sim n},b_{1\sim n}$，定义 $f(a_{1\sim n},b_{1\sim n},k)$ 为选择 $k$ 个互不相同的 $[1,n]$ 下标 $p_{1\sim k}$，下式的最小值：

$$\max_{i=1}^k\left(b_{p_i}+\sum_{j=1}^ia_{p_j}\right)$$

给定 $n,v$ 以及正整数序列 $b_{1\sim n}$，对于 $1\le k\le n$ 分别求出：对于所有值域为 $[1,v]$ 的正整数序列 $a_{1\sim n}$，$f(a_{1\sim n},b_{1\sim n},k)$ 之和对 $998244353$ 取模的结果。

$n\le 30$，$v\le 20$，$1\le b_i\le n\cdot v$。

## 题解

快进完贪心与 slope trick，求解 $f(a_{1\sim n},b_{1\sim n},*)$ 的过程如下：

- 将 $(a_i,b_i)$ 二元组按照 $b_i$ 从小到大排序，令 $b_{n+1}=+\infty$，维护初始含有 $+\infty$ 的小根堆 $q$ 与变量 $s=0$；
- 顺序遍历 $i=1\sim n$：
	- 若 $s$ 与堆顶元素之和小于等于 $b_i$，将 $s$ 加上堆顶元素并弹出堆顶，重复执行直到条件不满足；
    - 将堆顶元素减小 $b_i-s$，并令 $s\gets b_i$；
    - 向堆内插入 $a_i$；
- 恰好弹出 $k$ 个元素时的 $s$ 即为所求。

接下来需要对该过程进行 DP。考虑求一个 $k$ 的答案，令**终止状态为恰好弹出 $k$ 个元素的状态**，则答案由「被弹出的元素之和」以及可能的「堆顶元素减少量」两部分组成。我们在过程中插入 $a_i$ 时就钦定其在终止状态中是「完全弹出并贡献给 $s$」还是「部分或全部保留在堆内」。为了避免一些细节，我们规定两个元素相等时，先插入的元素更小。由于堆是小根堆，若最终存在一个数 $x$ 保留在堆内，则所有 $>x$ 的元素也必须保留在堆内；同理若 $x$ 被弹出，则所有 $<x$ 的元素也必须弹出。

设 $f_{i,k,l,r,s}$ 表示已经填入了 $a_{1\sim i-1}$，其中已经钦定了 $k$ 个元素最终被完全弹出，接下来所有 $<l$ 的元素必须要弹出，$\ge r$ 的元素必须要保留，当前的答案为 $s$ 的方案数。

转移时首先考虑弹出元素并修改堆顶，分类讨论：
- 若 $s\le b_i$，此时堆内所有已被钦定需要弹出的元素均会被弹出，而钦定不被弹出的最小元素，即堆顶，会减小 $b_i-s$，故 $l'\gets 0,r'\gets r-b_i+s,s'\gets b_i$；
- 否则存在至少一个已被钦定需要弹出的元素仍未被弹出，若存在 $\ge 2$ 个元素，则必定有 $l\le s-b_i$，此时 $l$ 不会改变；否则只存在一个该类元素，限制变为 $s-b_i$；即 $l'\gets \min(l,s-b_i),r'\gets r,s'\gets s$。

接下来即可枚举 $a_i$ 的取值并根据其与 $l',r'$ 的大小关系更新。

时间复杂度 $O(n^3v^4)$，若使用前缀和优化可以做到 $O(n^3v^3)$。

```cpp
f[0][0][0][v+1][0]=1;
int c=0;
for(int i=1;i<=n+1;i++,c=!c)
	for(int j=0;j<i;j++)
		for(int l=0;l<=v;l++)
			for(int r=1;r<=v+1;r++)
				for(int s=0;s<=u;s++){
					int w=f[c][j][l][r][s];
					if(!w) continue;
					f[c][j][l][r][s]=0;
					int sp=max(s,b[i]),lp=min(l,sp-b[i]),rp=r==v+1?r:r-sp+s;
					if(s!=b[i-1]&&sp==b[i])
						inc(ans[j],1ll*w*s%mod*pw[n-i+1]%mod);
					if(rp<=0) continue;
					for(int t=1;t<=v;t++){
						if(t>=lp) inc(f[!c][j][lp][min(rp,t)][sp],w);
						if(t<rp&&j<n) inc(f[!c][j+1][max(lp,t)][rp][sp+t],w);
					} 
				}
```
