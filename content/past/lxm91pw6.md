---
title: "题解：P10764 [BalticOI 2024] Wall"
date: 2024-07-24
category: "题解"
summary: "Link 题意 给你两个长为 n 的序列 ai,0/1，有 n 个砖块墙，其中墙 i 的高度可能为 ai 或者 bi，请求出每种情况下这些墙积水深度的总和。 形式化地，设墙 i"
math: true
top: 2
source: https://www.luogu.com.cn/article/lxm91pw6
slug: lxm91pw6
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10764)
## 题意
给你两个长为 $n$ 的序列 $a_{i,0/1}$，有 $n$ 个砖块墙，其中墙 $i$ 的高度可能为 $a_i$ 或者 $b_i$，请求出每种情况下这些墙**积水深度**的总和。

形式化地，设墙 $i$ 的高度为 $h_i$，则最终墙 $i$ 的**水面高度**为 $\displaystyle\min\left(\max_{j=1}^{i}h_j,\max_{j=i}^nh_j\right)$。

$n\le 5\times 10^5$。
## 题解
观察一下题面给的图并手玩一会可以发现前缀最大值和后缀最大值是重要的。更具体地，设某种情况下墙 $i$ 的高度为 $h_i$，设前缀最大值的位置分别为 $p_{1\sim k}$，则 $(p_i,p_{i+1})$ 内的墙的积水**水面高度**均为 $p_i$。后缀最大值是同理的。于是我们要设计某种与前缀最大值有关的状态，同时为了防止算重，对于两个相同的高度，我们令后面的大于前面的。

设 $f_{i,0/1}$ 表示 $h_i=a_{i,0/1}$ 是一个前缀最大值时前缀 $i$ 的所有情况的水面高度和，$c_{i,0/1}$ 为此时的方案数。

我们考虑如何从 $i$ 转移到 $j$，不妨以 $(i,p)$ 转移到 $(j,q)$ 为例，其中 $p,q=0/1$：
- 必须满足 $a_{i,p}\le a_{j,q}$，$\forall k\in(i,j),\min(a_{k,0},a_{k,1})<a_{i,p}$；
- 考虑 $(i,j)$ 内的方案数，令 $t=\sum_{k=i+1}^{j-1}[\max(a_{k,0},a_{k,1})<a_{i,p}]$，则 $(i,j)$ 内有 $t$ 个位置可任意选择，方案数为 $2^t$；
- 新增的水面高度为 $(j-i)a_{i,p}$。

经过一些尝试，以下标顺序转移是困难的。考虑到我们转移过程中要涉及权值比较且只能从小权值转移到大权值，于是我们不妨考虑**按值域从小到大转移**。转移中与 $i$ 相关的信息较多，我们使用**刷表法**。

我们把所有的 $a_{i,0/1}$ 排序后从小到大扫，设现在扫到 $a_{i,p}$，考虑向后更新。设 $r_i$ 表示已经扫到了几个 $a_{i,p}$，$t_i$ 表示 $[1,i]$ 有几个已经被扫到了 $2$ 次即 $\sum_{j=1}^i[r_j=2]$。用并查集找到 $i$ 后第一个 $r_j=0$ 的 $j$，则对于 $k\in(i,j],q\in[0,1]$ 且 $a_{k,q}$ 还未被扫到，$f_{k,q}\gets f_{k,q}+2^{t_k-t_i}[f_{i,p}+(k-i)a_{i,p}]$，$c_{k,q}\gets c_{k,q}\cdot 2^{t_k-t_i}c_{i,p}$。拆掉括号，分离 $i,k$ 后可以使用线段树维护。

实现中许多边界情况不需要我们考虑，比如上述式子中 $t_k$ 应为 $t_{k-1}$，但 $a_{k,q}$ 还未扫到即 $r_k\ne 2,t_k=t_{k-1}$；又如我们不需要分别处理已被扫到和未被扫到、$p,q=0/1$ 之类的问题，更具体可以参考代码。

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
const int N=5e5+10,mod=1e9+7,inv2=(mod+1)/2;
inline int add(int x,int y){ return x+y>=mod?x+y-mod:x+y; }
inline int dec(int x,int y){ return x>=y?x-y:x+mod-y; }
struct node{
	int v,p;
	inline friend bool operator<(const node &a,const node &b){
		return a.v==b.v?a.p<b.p:a.v<b.v;
	}
}a[N<<1];
struct TD{
	int a,b,c;
	TD(int A=0,int B=0,int C=0){ a=A,b=B,c=C; }
	inline friend TD operator +(const TD &a,const TD &b){
		return TD(add(a.a,b.a),add(a.b,b.b),add(a.c,b.c));
	}
	inline friend TD operator *(const TD &a,const int &b){
		return TD(1ll*a.a*b%mod,1ll*a.b*b%mod,1ll*a.c*b%mod);
	}
};
int n,pw[N],ipw[N],fa[N],c[N],f[N][2],p[N][2],g[N][2],q[N][2];
inline int find(int x){ return x==fa[x]?x:fa[x]=find(fa[x]); }
struct BIT{
	#define lowbit(x) (x&-x)
	int t[N];
	inline void clear(){
		for(int i=1;i<=n;i++)
			t[i]=0;
	}
	inline void add(int x,int v){
		for(int i=x;i<=n;i+=lowbit(i))
			t[i]+=v;
	}
	inline int query(int x){
		int s=0;
		for(int i=x;i;i-=lowbit(i))
			s+=t[i];
		return s;
	}
}T0;
struct Segment_Tree{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	TD vs[N<<2];
	int tag[N<<2];
	inline void pushadd(int rt,TD v){
		vs[rt]=vs[rt]+v*tag[rt];
	}
	inline void pushtag(int rt,int v){
		tag[rt]=1ll*tag[rt]*v%mod;
	}
	inline void pushdown(int rt){
		if(vs[rt].a||vs[rt].b||vs[rt].c){
			pushadd(ls,vs[rt]);
			pushadd(rs,vs[rt]);
			vs[rt]=TD();
		}
		if(tag[rt]!=1){
			pushtag(ls,tag[rt]);
			pushtag(rs,tag[rt]);
			tag[rt]=1;
		}
	}
	inline void build(int rt,int l,int r){
		tag[rt]=1,vs[rt]=TD();
		if(l==r){ return ; }
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r);
	}
	inline void add(int rt,int l,int r,int L,int R,TD v){
		if(L>R) return ;
		if(L<=l&&r<=R) return pushadd(rt,v);
		pushdown(rt);
		int mid=l+r>>1;
		if(L<=mid) add(ls,l,mid,L,R,v);
		if(R>mid) add(rs,mid+1,r,L,R,v);
	}
	inline void mul(int rt,int l,int r,int L,int R,int v){
		if(L>R) return ;
		if(L<=l&&r<=R) return pushtag(rt,v);
		pushdown(rt);
		int mid=l+r>>1;
		if(L<=mid) mul(ls,l,mid,L,R,v);
		if(R>mid) mul(rs,mid+1,r,L,R,v);
	}
	inline TD query(int rt,int l,int r,int p){
		if(l==r) return vs[rt];
		pushdown(rt);
		int mid=l+r>>1;
		if(p<=mid) return query(ls,l,mid,p);
		else return query(rs,mid+1,r,p);
	}
}T;
int main(){
	n=read();
	for(int i=1;i<=n;i++)
		a[i]={read(),i};
	for(int i=1;i<=n;i++)
		a[i+n]={read(),i};
	pw[0]=ipw[0]=1;
	for(int i=1;i<=n;i++)
		pw[i]=add(pw[i-1],pw[i-1]),
		ipw[i]=1ll*inv2*ipw[i-1]%mod;
	sort(a+1,a+n*2+1);
	for(int i=0;i<=n+1;i++)
		fa[i]=i;
	T.build(1,1,n);
	T.add(1,1,n,1,1,TD(0,0,1));
	for(int i=1;i<=n*2;i++){
		int v=a[i].v,t=a[i].p;
		TD res=T.query(1,1,n,t);
		f[t][c[t]]=(res.a+1ll*t*res.b)%mod;
		p[t][c[t]]=res.c;
		int ct=T0.query(t);
		int pt=find(t+1);
		if(pt==n+1) pt=n;
		T.add(1,1,n,t+1,pt,TD(dec(f[t][c[t]],1ll*t*v%mod*p[t][c[t]]%mod),1ll*v*p[t][c[t]]%mod,p[t][c[t]])*ipw[ct]);
		c[t]++;
		if(c[t]==1) fa[t]=t+1;
		if(c[t]==2) T0.add(t,1),T.mul(1,1,n,t,n,2);
	}
	for(int i=0;i<=n+1;i++)
		fa[i]=i,c[i]=0;
	T0.clear(),T.build(1,1,n);
	T.add(1,1,n,n,n,TD(0,0,1));
	int ans=0;
	for(int i=1;i<=n*2;i++){
		int v=a[i].v,t=a[i].p;
		TD res=T.query(1,1,n,t);
		g[t][c[t]]=(res.a+1ll*t*res.b)%mod;
		q[t][c[t]]=res.c;
		ans=(ans+1ll*v*p[t][c[t]]%mod*q[t][c[t]])%mod;
		int ct=T0.query(t);
		int pt=find(t-1);
		if(pt==0) pt=1;
		T.add(1,1,n,pt,t-1,TD(add(g[t][c[t]],1ll*t*v%mod*q[t][c[t]]%mod),mod-1ll*v*q[t][c[t]]%mod,q[t][c[t]])*pw[ct]);
		c[t]++;
		if(c[t]==1) fa[t]=t-1;
		if(c[t]==2) T0.add(t,1),T.mul(1,1,n,t,n,inv2);
	}
	for(int i=1;i<=n*2;i++)
		ans=dec(ans,1ll*pw[n-1]*a[i].v%mod);
	for(int i=1;i<=n;i++)
		ans=(ans+1ll*f[i][0]*q[i][0]+1ll*p[i][0]*g[i][0]+1ll*f[i][1]*q[i][1]+1ll*p[i][1]*g[i][1])%mod;
	write(ans);
	flush();
}
```
