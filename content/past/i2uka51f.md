---
title: "题解：P9047 [PA2021] Poborcy podatkowi"
date: 2024-08-21
category: "题解"
summary: "Link 大概是对第一篇题解的补充。 题意 给定一棵 n 个点的树，你可以选择若干条长度为 4 的链，要求没有一条边同时属于两条选出的链，最大化选出的所有边的边权和。 n≤ 2"
math: true
top: 2
source: https://www.luogu.com.cn/article/i2uka51f
slug: i2uka51f
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P9047)

大概是对第一篇题解的补充。

## 题意

给定一棵 $n$ 个点的树，你可以选择若干条长度为 $4$ 的链，要求没有一条边同时属于两条选出的链，最大化选出的所有边的边权和。

$n\le 2\times 10^5$。
## 思路

设 $f_{x,i}$ 表示 $x$ 子树的答案，要求 $x$ 下挂了一条长为 $i$ 的链。

考虑在 $x$ 处进行合并。如果选了 $a,b,c$ 条 $1,2,3$ 的链，则我们要对 $\forall p\in[-1,1],q\in[0,1]$ 求出 $a-c=p$，$b\equiv q\pmod2$ 时的最大价值。实际上，这可以看成一个背包问题。假如没有第二条限制，则将 $0,1,2,3$ 的链分别看成重量为 $1,0,1,2$ 的物品即可。加上第二条限制只需要加一个 $0/1$ 维即可。

这是重量较小时的 $(\max,+)$ 背包问题，我们有如下解法：设重量为 $i$ 时的答案为 $w_i$，则 $w_{0,2,\dots,2k}$ 和 $w_{1,3,\dots,2k+1}$ 分别是凸的。前者考虑将重量为 $1$ 的物品的价值从大到小排序并两两分组，转化为重量为 $1$ 的背包，显然答案为凸的。后者同理。

类似于 $(+,\times)$ 卷积下背包的分治 FFT 做法，我们使用分治。先求出 $[l,mid],(mid,r]$ 的答案数组 $a,b$，然后两边分别按下标 $\bmod2$ 分组，枚举两边取哪组做 $(\max,+)$ 卷积即可。由于每组均为凸的，$(\max,+)$ 卷积可以直接使用闵可夫斯基和（归并差分数组）。

事实上，由于只用求 $O(1)$ 个位置的值，我们只需要使用 wqs 二分即可做到同复杂度，但是显然归并差分数组细节少很多。

时间复杂度 $O(n\log n)$。

参考代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
#define pii pair<int,int>
#define mpr make_pair
#define fir first
#define sec second
const int N=2e5+10;
const ll INF=1e16;
namespace PolyC{
	#define Poly vector<ll>
	inline void upd(ll &x,ll y){
		x=max(x,y);
	}
	inline Poly operator+(const Poly &a,const Poly &b){
		Poly F=a;
		F.resize(max(a.size(),b.size()));
		for(int i=0;i<b.size();i++)
			F[i]=max(F[i],b[i]);
		return F;
	}
	inline Poly operator*(const Poly &a,const Poly &b){
		int n=a.size(),m=b.size();
		Poly F,G;
		for(int i=1;i<n;i++)
			F.push_back(a[i]-a[i-1]);
		for(int i=1;i<m;i++)
			G.push_back(b[i]-b[i-1]);
		Poly H(n+m-2);
		merge(F.begin(),F.end(),G.begin(),G.end(),H.begin(),greater<ll>());
		Poly R;
		R.push_back(a[0]+b[0]);
		for(auto v:H) R.push_back(R.back()+v);
		return R;
	}
} 
using namespace PolyC;
int lc;
inline Poly Mul(Poly F,Poly G){
	int n=F.size(),m=G.size();
	Poly H(min(n+m-1,lc+2),-INF);
	for(int a=0;a<2;a++)
		for(int b=0;b<2;b++){
			Poly A,B;
			for(int i=a;i<n;i+=2)
				A.push_back(F[i]);
			for(int i=b;i<m;i+=2)
				B.push_back(G[i]);
			A=A*B;
			for(int i=0;i<A.size();i++)
				if(i*2+a+b<H.size())
					upd(H[i*2+a+b],A[i]);
		}
	return H;
}
int n;
ll f[N][4];
vector<pii>a[N];
/*
(1,0)(0,0)(1,1)(2,1) 
*/
vector<Poly>F,G;
inline vector<Poly> solve(int l,int r){
	if(l==r) return {F[l],G[l]};
	int mid=l+r>>1;
	vector<Poly> A=solve(l,mid),B=solve(mid+1,r);
	return {Mul(A[0],B[0])+Mul(A[1],B[1]),Mul(A[0],B[1])+Mul(A[1],B[0])};
}
inline void dfs(int x,int fa){
	int c=0;
	for(auto tmp:a[x]){
		int t=tmp.fir,w=tmp.sec;
		if(t==fa) continue;
		dfs(t,x),c++;
	}
	if(!c){
		f[x][1]=f[x][2]=f[x][3]=-INF;
		return ;
	}
	F.clear(),G.clear(),lc=c; 
	for(auto tmp:a[x]){
		int t=tmp.fir,w=tmp.sec;
		if(t==fa) continue;
		Poly A(3,-INF),B(2,-INF);
		A[1]=max(f[t][0],f[t][3]+w);
		A[0]=f[t][0]+w,A[2]=f[t][2]+w;
		B[1]=f[t][1]+w;
		F.push_back(A),G.push_back(B); 
	}
	vector<Poly>T=solve(0,c-1);
	f[x][0]=T[0][c],f[x][1]=T[0][c-1];
	f[x][2]=T[1][c],f[x][3]=T[0][c+1];
}
int main(){
	n=read();
	for(int i=1;i<n;i++){
		int u=read(),v=read(),w=read();
		a[u].push_back(mpr(v,w)),a[v].push_back(mpr(u,w));
	}
	dfs(1,1);
	write(f[1][0]);
	flush();
}
```
