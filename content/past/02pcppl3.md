---
title: "题解 P8885【「JEOI-R1」子序列】"
date: 2023-11-15
category: "题解"
summary: "Link 题意 给定一个长为 n 的仅包含 0、1 和 ? 的字符串 s，你需要将字符串中的每个 ? 分别替换成 0 或 1 之一。称一个序列是好的当且仅当其恰好拥有奇数个本质"
math: true
top: 2
source: https://www.luogu.com.cn/article/02pcppl3
slug: 02pcppl3
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P8885)

## 题意

给定一个长为 $n$ 的仅包含 `0`、`1` 和 `?` 的字符串 $s$，你需要将字符串中的每个 `?` 分别替换成 `0` 或 `1` 之一。称一个序列是**好的**当且仅当其恰好拥有奇数个本质不同的**子序列**（包含空串），称一个序列是**极好的**当且仅当其拥有奇数个好的非空**子串**。每次询问给出 $s$ 的一个子串 $[l,r]$，求其有多少种替换方案，使得这个子串是**极好的**。

$n\le 5\times10^4$，$m\le 5\times 10^5$。

## 题解
校内模拟赛出了这题的加强版，将字符集扩大为 $3$ 并增大了 $m$ 的数据范围。

令 $v$ 等于字符集大小 $2$。

首先我们考虑描述好的序列。本质不同子序列有广为人知的 $\text{dp}$：令 $f_i$ 表示以 $i$ 结尾的本质不同子序列个数，$f_s$ 表示 $\sum f_i+1$，则在序列后加入字符 $c$ 的时候令 $f_i\gets f_s$。考虑在 $\bmod2$ 意义下，显然初始时 $f_i=0,f_s=1$，加入一个字符 $c$ 就会交换 $f_s,f_c$。显然一个好的序列进行完 $\text{dp}$ 后 $f_s=1$。

先思考全局询问的做法。注意到这个 $\text{dp}$ 只拥有 $v+1$ 个状态（$1$ 分别在 $1\dots v$ 或者 $s$） 处。状态数少，考虑 $\text{dp}$ 套 $\text{dp}$。令 $g_{i,f_0,f_1,f_s,t}$ 表示前缀 $i$ 有多少个后缀的 $\text{dp}$ 状态为 $1$ 在 $f_0,f_1,f_s$ 处，前缀 $i$ 有 $t$ 个子串是好的，其中后四维都是在模 $2$ 意义下的。考虑转移，枚举位置 $i$ 能填的字符 $c$（不妨假设 $c=0$），则有转移 $g_{i,f_0,f_1,f_s,t}\to g_{i+1,f_s\oplus1,f_1,f_0,t\oplus f_0}$，$c=1$ 同理。最终答案就是 $\sum g_{n,*,*,*,1}$。

令 $V=2^{v+2}$，后面四维可以压缩成一个 $[0,V)$
 的数，转移可以用 $V\times V$ 的矩阵描述，用线段树维护矩阵可做到 $O(V^3n+V^3m\log n)$，非常糟糕。

$n,m$ 不同阶，考虑减少合并次数，使用二区间合并（猫树分治），对于分治区间 $[l,r]$ 与其中点 $mid$，记录 $s_i=\prod_{j=i}^{mid}A_j$，$p_i=\prod_{j=mid+1}^iA_j$（$A_j$ 表示 $j$ 处的转移矩阵），询问直接求 $s_lp_r$，可做到 $O(V^3n\log n+V^3m)$ 的复杂度，后文将直接用 $T(A,B)$ 来代替 $O(An\log n+Bm)$。

考虑将询问时相乘的矩阵变成向量，定义 $1\times V$ 的向量 $S_{0,i}=[i=0]$
，$V\times 1$ 的向量 $T_{i,0}=[2^{v+1}\subset i]$，不难发现 $[l,r]$ 的答案就是 $Ss_lp_rT$，不妨先令 $s_i\gets Ss_i$，$p_i\gets p_iT$，则复杂度降低为 $T(V^3,V)$。

继续优化，可以发现猫树中每层都重新算 $s,p$ 浪费很大，考虑在相邻两层间递推 $s,p$，不难发现对于 $i\in[l,mid]$，$s_i\gets s_i\prod_{j=mid+1}^rA_j$，$i\in[mid+1,r]$，$p_i\gets \prod_{j=l}^{mid}A_jp_i$。$\prod_{j=l}^{mid}A_j$ 和 $\prod_{j=mid+1}^rA_j$ 可以简单求，注意到此处是向量乘矩阵，时间复杂度被我们优化到了 $T(V^2,V)$。

总时间复杂度 $O(V^3n+V^2n\log n+Vm+m\log n)$，快速求猫树两点 $\text{LCA}$ 可以将后面的 $m\log n$ 去掉。矩阵稀疏，只有 $O(V)$ 个点，利用此点可继续优化复杂度至 $O(V^2n\log n+Vm)$，本题中 $V=16$。可以通过 $v=3,m=10^6$ 的加强版（$V=32$）。

核心代码：
```cpp
Matrix ml[N],pr[N],sf[N];
inline void solve(int rt,int l,int r){
	if(l==r){
		ml[l]=mt[s[l]];
		sf[l]=S*ml[l],pr[l]=ml[l]*T;
		return ;
	}
	int mid=l+r>>1;
	solve(ls,l,mid),solve(rs,mid+1,r);
	for(int i=l;i<=mid;i++)
		for(int j=st[i];qr[j].fir==i;j++){
			pii tmp=qr[j].sec;
			if(tmp.fir>r) break;
			int r=tmp.fir;
			ans[tmp.sec]=(sf[i]*pr[r])[0][0];
			st[i]=j+1;
		}
	for(int i=l;i<=mid;i++)
		sf[i]=sf[i]*ml[mid+1];
	for(int i=mid+1;i<=r;i++)
		pr[i]=ml[l]*pr[i];
	ml[l]=ml[l]*ml[mid+1];
}
```
