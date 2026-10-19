---
title: "题解 P5050【【模板】多项式多点求值】"
date: 2021-07-15
category: "题解"
summary: "Link 题意 给出 n 次多项式 F(x)=Σi=0n fixi，m 组询问，第 i 次询问给出 xi，求出 F(xi) 的值。 1≤ n,m≤ 6.4× 104。 思路 U"
math: true
top: 2
source: https://www.luogu.com.cn/article/3w0tsx5d
slug: 3w0tsx5d
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P5050)
## 题意
给出 $n$ 次多项式 $F(x)=\sum_{i=0}^n f_ix^i$，$m$ 组询问，第 $i$ 次询问给出 $x_i$，求出 $F(x_i)$ 的值。

$1\le n,m\le 6.4\times 10^4$。
## 思路
$\text{Update 2021.12.22}$：更改了代码。

$\text{Update 2022.04.07}$：对代码实现与代码细节进行补充说明。

$\text{Update 2024.03.19}$：更改了代码与部分说明。

以下默认 $mid=\lfloor\frac {l+r} 2\rfloor$。

考虑构造一个多项式 $G(x)=x-x_0$，我们可以证明 $F(x)\bmod G(x)=F(x_0)$：令 $F(x)=Q(x)\cdot G(x)+r$，那么 $F(x_0)=Q(x_0)\cdot G(x_0)+r$，因为 $G(x_0)=0$，所以 $F(x_0)=r$。

分治 $\text{NTT}$ 容易求出 $G_{l,r}=\displaystyle\prod_{i=l}^r(x-x_i)$，将 $F$ 分别对 $G_{l,mid}$ 和 $G_{mid+1,r}$ 取模后传入左右区间，当 $l=r$ 时就求出了第 $l$ 个询问的答案。分治到 $[l,r]$ 时 $F$ 的次数小于 $G_{l,r}$ 的次数即 $F$ 为 $r-l$ 次多项式。

假设 $n,m$ 同阶，我们得到了一个时间复杂度 $T(n)=2T(\frac n 2)+O(n\log n)=O(n\log^2n)$ 的算法，但由于每次递归都需要多项式取模，常数较大。

我们发现算出 $Q(x)$ 的常数项即可算出 $r$，即 $r=[x^0]Q(x)\cdot x_0+[x^0]F(x)$。

在多项式取模的推导过程中，我们得到了 $Q_R\equiv \dfrac {F_R}{G_R}(\bmod x^{n-m+1})$ 这一式子。因为 ${G_{l,mid}}_R^{-1}={G_{l,r}}_R^{-1}{G_{mid+1,r}}_R$，于是可以求出 $[l,r]$ 对应的 $Q_R$ 后乘上 ${G_{mid+1,r}}_R$ 得到 $[l,mid]$ 对应的 $Q_R$，右区间同理。

$G(x)$ 的长度看似没有保障，但是注意到我们最后只需要 $[x^0]Q(x)$ 即 $[x^{n-1}]Q_R(x)$，在递归到区间 $[l,r]$ 时，$Q_R$ 之后只会乘以次数小于 $r-l+1$ 的多项式，从而只有后 $r-l$ 位有可能对答案有贡献，于是只需要保留 $Q_R$ 的后 $r-l$ 位，这也保证了该算法的时间复杂度。

时间复杂度 $O(n\log^2n)$，每次递归只需要做多项式乘法，常数小。

事实上这与转置原理方法本质相同。

核心代码：
```cpp
namespace Evaluation{
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
	Poly T[N];
	Poly Q,ans;
	inline void build(int rt,int l,int r){
		if(l==r){
			T[rt]=(Poly){1,dec(0,Q[l])};
			return ;
		}
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r);
		T[rt]=T[ls]*T[rs];
	}
	inline void solve(int rt,int l,int r,Poly F){
		if(l==r){
			ans[l]=F[0];
			return ;
		}
		int mid=l+r>>1;
		solve(ls,l,mid,MulT(F,T[rs]));
		solve(rs,mid+1,r,MulT(F,T[ls]));
	}
	inline Poly solve(Poly F,Poly Qr){
		Q=Qr;
		int n=F.size(),m=Q.size();
		if(n<m) F.resize(n=m);
		if(m<n) Q.resize(n);
		build(1,0,n-1);
		ans.resize(n),F.resize(n*2);
		solve(1,0,n-1,MulT(F,Inv(T[1])));
		ans.resize(m);
		return ans;
	}
}
```

另外我还实现了任意模数多点求值，跑一个点大概要 300ms，[评测记录](https://www.luogu.com.cn/record/65564926)。实测可以轻松跑过 [P5282](https://www.luogu.com.cn/problem/P5282)。
