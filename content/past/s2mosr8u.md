---
title: "题解：CF1799F Halve or Subtract"
date: 2024-09-24
category: "题解"
summary: "Link 介绍一下一种高维 wqs 的方法。 此方法来自 @YeahPotato 的专栏 严谨的 WQS 二分方法。 题意 给定一个长为 n 的序列 v1 n，三个常数 d,a"
math: true
top: 2
source: https://www.luogu.com.cn/article/s2mosr8u
slug: s2mosr8u
---

[$\text{Link}$](https://www.luogu.com.cn/problem/CF1799F)

介绍一下一种高维 wqs 的方法。

此方法来自 @[YeahPotato](https://www.luogu.com.cn/user/94976) 的专栏 [严谨的 WQS 二分方法](https://www.luogu.com/article/vsffwrc3)。

## 题意

给定一个长为 $n$ 的序列 $v_{1\dots n}$，三个常数 $d,a,b$。你可以执行若干次以下两种操作：

1. 选择 $1\le i\le n$，令 $v_i\gets\lceil\frac{v_i}{2}\rceil$。
1. 选择 $1\le i\le n$，令 $v_i\gets\max(v_i-d,0)$。

你至多进行 $a$ 次操作 1，$b$ 次操作 2，同时对于每个元素，每种操作至多进行一次。

你需要最小化操作后 $\sum v$ 的值并输出。

$1\le n\le 10^5$。
## 题解

两个显然的性质是，我们会把操作用完、我们会先用操作 1 再用操作 2。而根据费用流建图，答案关于操作次数 $a,b$ 均为下凸的。

我们设操作次数限制为 $a,b$ 时的答案为 $f(a,b)$，那么我们需要使用两层 wqs 二分分别去除两维限制，而外层二分我们需要求出「使得 $f(x,b)-kx$ 取到最小值的 $x$」，而它并不好求。问题的关键为我们无法直接通过调整斜率使得求出切到的点恰为给定值，无法同时使两维取到 $a,b$。

此时，我们就需要寻找求解凸函数单点值的更优方法。

有如下结论：

- 当 $f(x)$ 关于 $x$ 上凸时，令 $g_a(k)=ka+\displaystyle\max_{x}(f(x)-kx)$，那么有：$g_a(k)$ 关于 $k$ 下凸且 $f(a)=\displaystyle\min_kg_a(k)$。
- 当 $f(x)$ 关于 $x$ 下凸时，令 $g_a(k)=ka+\displaystyle\min_{x}(f(x)-kx)$，那么有：$g_a(k)$ 关于 $k$ 上凸且 $f(a)=\displaystyle\max_kg_a(k)$。

> 证明：不妨考虑证明其中第二条。
>
> 以下将 $g_a(k)$ 简写为 $g(k)$。令 $h(k)$ 为 $f(x)-kx$ 取到最小值的某个 $x$。
>
> 证明 $g(k)$ 上凸即证 $\forall k_1,k_2,\forall \lambda\in[0,1]$，令 $k=\lambda k_1+(1-\lambda )k_2$，有 $\lambda g(k_1)+(1-\lambda)g(k_2)\le g(k)$：
>
> $$\begin{aligned}&\lambda g(k_1)+(1-\lambda)g(k_2)\\=&\lambda [k_1a+\min_x(f(x)-k_1x)]+(1-\lambda)[k_2a+\min_x(f(x)-k_2x)]\\le&\lambda [k_1a+(f(h(k))-k_1h(k))]+(1-\lambda)[k_2a+(f(h(k))-k_2h(k))]\\=&g(k)\end{aligned}$$
>
> 还需证明 $g(k)$ 的最大值为 $f(a)$，那么由于 $f(x)$ 关于 $x$ 下凸，必定有 $g(f'(a))=f(a)$。而 $g(k)\le ka+f(a)-ka=f(a)$，所以 $f(a)=\max_k g(k)$。

有了这个结论，我们就把较对复杂的凸函数求值转化为了对较简单的凸函数求最值。

接下来，我们就可二分或三分求 $g(k_1)=k_1a+\min_x(f(x,b)-k_1x)$ 的最值；而其中 $\min_x(f(x,y)-k_1x)$ 又是关于 $y$ 的下凸函数，再用二分或三分求 $h(k_2)=k_2b+\min_{x,y}(f(x,y)-k_1x-k_2y)$ 的最值即可。

时间复杂度 $O(n\log^2 v)$。

核心代码：
```cpp
const int N=5e3+10;
int n,d,a,b,v[N];
inline ll calc(int k1,int k2){
	ll s=0;
	for(int i=1;i<=n;i++)
		s+=min({v[i],(v[i]+1)/2-k1,max(v[i]-d,0)-k2,max((v[i]+1)/2-d,0)-k1-k2});
	return s;
}
inline ll solve2(int k1){
	int L=-1e9,R=0;
	while(L<R){
		int mL=L+R>>1,mR=mL+1;
		ll v1=calc(k1,mL)+1ll*mL*b,v2=calc(k1,mR)+1ll*mR*b;
		if(v1==v2) return v1;
		if(v1<v2) L=mL+1;
		else R=mR-1;
	}
	return calc(k1,L)+1ll*L*b;
}
inline ll solve1(){
	int L=-1e9,R=0;
	while(L<R){
		int mL=L+R>>1,mR=mL+1;
		ll v1=solve2(mL)+1ll*mL*a,v2=solve2(mR)+1ll*mR*a;
		if(v1==v2) return v1;
		if(v1<v2) L=mL+1;
		else R=mR-1;
	}
	return solve2(L)+1ll*L*a;
}
```
