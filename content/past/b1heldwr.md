---
title: "题解 P5158【【模板】多项式快速插值】"
date: 2021-07-16
category: "题解"
summary: "Link 题意 给出 n-1 次多项式 F(x) 的 n 个点值 F(xi)=yi，求出这个多项式 F(x)。 1≤ n≤105。 思路 Update 2024.03.19：更"
math: true
top: 2
source: https://www.luogu.com.cn/article/b1heldwr
slug: b1heldwr
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P5158)
## 题意
给出 $n-1$ 次多项式 $F(x)$ 的 $n$ 个点值 $F(x_i)=y_i$，求出这个多项式 $F(x)$。

$1\le n\le10^5$。
## 思路
$\text{Update 2024.03.19}$：更改了代码与部分说明。

以下默认 $mid=\lfloor\frac {l+r} 2\rfloor$。

回顾拉格朗日插值的式子：

$$F(x)=\sum_{i=1}^n y_i\prod_{i\ne j}\dfrac{x-x_j}{x_i-x_j}$$

将后面的分母提到前面：

$$F(x)=\sum_{i=1}^n \dfrac{y_i}{\prod_{i\ne j}{x_i-x_j}}\prod_{i\ne j}{(x-x_j)}$$

设 $\delta(x)=\displaystyle\prod_{i=1}^n(x-x_i)$，则：

$$\prod_{i\ne j}({x_i-x_j})=\lim_{x\to x_i}\dfrac{\delta(x)}{x-x_i}=\delta'(x_i)$$

$$F(x)=\sum_{i=1}^n \dfrac{y_i}{\delta'(x_i)}\prod_{i\ne j}{(x-x_j)}$$

$\delta(x)$ 容易分治 $\text{NTT}$ 求出，然后使用多点求值求出 $\delta'(x_i)$，不会多点求值可以看[这里](https://www.luogu.com.cn/blog/cyffff/solution-p5050)。

接下来直接分治 $\text{NTT}$ 即可。具体地，设 $G_{l,r}(x)=\prod_{i=l}^r(x-x_i)$，$H_{l,r}(x)$ 为 $(x_l,y_l),(x_{l+1}y_{l+1}),\dots (x_r,y_r)$ 插出来的多项式，即 $\sum_{i=l}^r \frac{y_i}{\delta'(x_i)}\prod_{i\ne j}^{l\le j\le r}{(x-x_j)}$，不难导出：

$$G_{l,r}(x)=G_{l,mid}(x)\cdot G_{mid+1,r}(x)$$

$$H_{l,r}(x)=H_{l,mid}(x)\cdot G_{mid+1,r}(x)+H_{mid+1,r}(x)\cdot G_{l,mid}(x)$$

每一步的时间复杂度均为 $O(n\log^2 n)$，于是总时间复杂度为 $O(n\log^2 n)$。

核心代码：
```cpp
namespace Interpolation{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	inline Poly MulT(const Poly &a,const Poly &b){
		Poly F=a,G=b;
		int n=a.size(),m=b.size();
		reverse(G.begin(),G.end());
		init(n);
		F.resize(lim),G.resize(lim);
		NTT(F,1),NTT(G,1);
		for(int i=0;i<lim;i++)
			G[i]=1ll*F[i]*G[i]%mod;
		NTT(G,-1);
		for(int i=m-1;i<n;i++)
			F[i-m+1]=G[i];
		F.resize(max(0,n-m+1));
		return F;
	}
	Poly TR[N],T[N];
	Poly Q,QY,ans;
	inline void build(int rt,int l,int r){
		if(l==r){
			TR[rt]=(Poly){1,dec(0,Q[l])};
			T[rt]=TR[rt],reverse(T[rt].begin(),T[rt].end());
			return ;
		}
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r);
		TR[rt]=TR[ls]*TR[rs];
		T[rt]=TR[rt],reverse(T[rt].begin(),T[rt].end());
	}
	inline void solve(int rt,int l,int r,Poly F){
		if(l==r){
			ans[l]=F[0];
			return ;
		}
		int mid=l+r>>1;
		solve(ls,l,mid,MulT(F,TR[rs]));
		solve(rs,mid+1,r,MulT(F,TR[ls]));
	}
	inline Poly solve(int rt,int l,int r){
		if(l==r)
			return (Poly){1ll*QY[l]*qpow(ans[l],mod-2)%mod};
		int mid=l+r>>1;
		Poly L=solve(ls,l,mid),R=solve(rs,mid+1,r);
		return L*T[rs]+R*T[ls];
	}
	inline Poly solve(Poly X,Poly Y){
		Q=X,QY=Y;
		int n=X.size();
		build(1,0,n-1);
		Poly F=Deriv(T[1]);
		ans.resize(n),F.resize(n*2);
		solve(1,0,n-1,MulT(F,Inv(TR[1])));
		return solve(1,0,n-1);
	}
}
```
