---
title: "转置原理小练习：Do Use FFT"
date: 2024-04-04
category: "题解"
summary: "Link 题意 给定三个长为 n 的数组 a0,,n-1,b0,,n-1,c0,,n-1，对 i∈[0,n-1] 求出： di=Σj=0n-1cj∏k=0i(aj+bk) 对 "
math: true
top: 2
source: https://www.luogu.com.cn/article/zodm206p
slug: zodm206p
---

[$\text{Link}$](https://qoj.ac/contest/592/problem/3085)

## 题意

给定三个长为 $n$ 的数组 $a_{0,\dots,n-1},b_{0,\dots,n-1},c_{0,\dots,n-1}$，对 $\forall i\in[0,n-1]$ 求出：

$$d_i=\sum_{j=0}^{n-1}c_j\prod_{k=0}^i(a_j+b_k)$$

对 $998244353$ 取模。

$n\le 2.5\times 10^5$。
## 思路
将 $a,b$ 看成常量，那么 $d$ 就是由 $c$ 的线性变换得来，我们考虑其转置：

$$c_j=\sum_{i=0}^{n-1}d_i\prod_{k=0}^i(a_j+b_k)$$

注意到 $j$ 只出现一次，不妨令：
$$F(x)=\sum_{i=0}^{n-1}d_i\prod_{k=0}^i(x+b_k)$$

那么显然有：
$$c_j=F(a_j)$$

以 $d$ 作为输入，$c$ 作为输出，用分治 NTT 求出 $F(x)$ 再多点求值得到 $c$，便在 $O(n\log^2n)$ 的时间复杂度内解决了转置后的问题。由转置原理，我们可以在同时间复杂度内求出原问题。

多点求值的转置是老生常谈了：

$$F(x)=\sum_{i=0}^{n-1}\frac{c_i}{1-a_ix}$$

分治 NTT 即可。

要写出前面的分治 NTT 的转置，我们把原算法过程写出来：

$$F_{l,r}(x)=\sum_{i=l}^rd_i\prod_{k=l}^i(x+b_k)$$
$$G_{l,r}(x)=\prod_{k=l}^r(x+b_k)$$

1. 对于叶子结点：$F_{i,i}=b_id_i+d_ix$；
2. 对于非叶子结点：$F_{l,r}=F_{l,mid}+F_{mid+1,r}\times G_{l,mid}$，$G_{l,r}=G_{l,mid}\times G_{mid+1,r}$。

写算法转置的基本步骤很简单：
1. 将流程翻转；
2. 将每一步基本运算转置，其中最重要的就是将 $a_i$ 乘以 $v$ 加给 $b_j$ 经转置变为将 $b_j$ 乘以 $v$ 加给 $a_j$；对于多项式也是如此：将 $F$ 乘以 $G$ 加给 $H$ 经转置变为将 $H$ 转置乘 $G$ 加给 $F$。

同时，需要注意分辨常量与变量，与输入输出无关的常量不需要参与转置。不难发现 $G$ 与 $c,d$ 均无关，在此算法中属于常量，故 $G$ 的计算不需要转置。

对于 $F_{l,r}=F_{l,mid}+F_{mid+1,r}\times G_{l,mid}$，我们可以将其看成三步：$F_{l,r}\gets 0$，$F_{l,r}\gets F_{l,r}+F_{l,mid}$，$F_{l,r}\gets F_{l,r}+F_{mid+1,r}\times G_{l,mid}$，于是该算法的转置也不难写出：

1. 对于非叶子结点：$F_{l,mid}=F_{l,r}$，$F_{mid+1,r}=F_{l,r}\times^T G_{l,mid}$，其中 $F_{l,mid}$ 只需要保留 $mid-l+1$ 次；
2. 对于叶子结点：$d_i=b_i[x^0]F_{i,i}+[x^1]F_{i,i}$。

于是在 $O(n\log^2n)$ 时间复杂度内解决了原问题。

核心代码：
```cpp
namespace MulTT{
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
}
using namespace MulTT;
#define PolyY vector<Poly>
inline PolyY operator*(const PolyY &a,const PolyY &b){
	int p=a[0].size(),q=b[0].size();
	PolyY F=a,G=b;
	init(p+q);
	for(int i=0;i<2;i++)
		F[i].resize(lim),G[i].resize(lim),
		NTT(F[i],1),NTT(G[i],1);
	for(int i=0;i<lim;i++)
		F[1][i]=(1ll*F[0][i]*G[1][i]+1ll*F[1][i]*G[0][i])%mod,
		F[0][i]=1ll*F[0][i]*G[0][i]%mod;
	for(int i=0;i<2;i++)
		NTT(F[i],-1),F[i].resize(p+q-1);
	return F;
}
#define ls (rt<<1)
#define rs (rt<<1|1)
int n,m;
Poly A,B,C,D,G[N];
inline void solve1(int rt,int l,int r){
	if(l==r){
		G[rt]={B[l],1};
		return ;
	}
	int mid=l+r>>1;
	solve1(ls,l,mid),solve1(rs,mid+1,r);
	G[rt]=G[ls]*G[rs];
}
inline PolyY solve2(int l,int r){
	if(l==r) return {{1,dec(0,A[l])},{C[l],0}};
	int mid=l+r>>1;
	return solve2(l,mid)*solve2(mid+1,r);
}
inline void solve3(int rt,int l,int r,Poly F){
	if(l==r){
		D[l]=add(F[1],1ll*F[0]*B[l]%mod);
		return ;
	}
	int mid=l+r>>1;
	Poly L=F;
	L.resize(mid-l+2);
	solve3(ls,l,mid,L);
	Poly R=MulT(F,G[ls]);
	solve3(rs,mid+1,r,R);
}
int main(){
	n=read();
	Prefix(n*2);
	for(int i=0;i<n;i++)
		A.push_back(read());
	for(int i=0;i<n;i++)
		B.push_back(read());
	for(int i=0;i<n;i++)
		C.push_back(read());
	D.resize(n);
	solve1(1,0,n-1);
	PolyY T=solve2(0,n-1);
	Poly F=T[1]*Inv(T[0]);
	F.resize(n+1);
	solve3(1,0,n-1,F);
	for(auto tmp:D)
		write(tmp),putc(' ');
	flush();
}
```
