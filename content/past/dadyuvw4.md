---
title: "题解：P12020 Boolean Computer 加强版"
date: 2025-04-09
category: "题解"
summary: "Link 题意 给定 n,m,q 以及 m 个在 [0,2n) 内的整数 a1 m。现有与、或、异或、与非、或非、同或六种位运算，对于给出的一个长为 n 的运算法则 s0 n-"
math: true
top: 2
source: https://www.luogu.com.cn/article/dadyuvw4
slug: dadyuvw4
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P12020)
## 题意
给定 $n,m,q$ 以及 $m$ 个在 $[0,2^n)$ 内的整数 $a_{1\sim m}$。现有与、或、异或、与非、或非、同或六种位运算，对于给出的一个长为 $n$ 的运算法则 $s_{0\sim n-1}$，其中 $s_i$ 为六种位运算之一，数 $x,y$ 关于该运算法则的运算结果的第 $i$ 位是 $x,y$ 的第 $i$ 位通过运算 $s_i$ 得到的。

接下来给出 $q$ 次询问，每次询问给出一个运算法则 $s_{0\sim n-1}$ 与一个整数 $k$，求出有多少二元组 $1\le i,j\le m$ 满足 $a_i\odot a_j=k$。

$n\le 16$，$m,q\le 10^5$。
## 题解
单独考虑一位的情况，根据这一位的运算和该位 $k$ 的值，我们会得到一条形如「$a_i,a_j$ 该位需要有 $x$ 个 $1$」或「$a_i,a_j$ 该位需要有 $x$ 或 $y$ 个 $1$」的限制。

对于每个询问，对所有限制集大小为 $2$ 的位进行枚举，即可确定每一位需要总共有多少个 $1$。这可以视作将 $a_i$ 的二进制形式看作三进制数，并求有多少对 $(i,j)$ 满足 $a_i+a_j$ 等于给定数，可以使用引入单位根的三进制 FWT 解决。

时间复杂度 $O(n3^n+q2^n)$。

**注意到上述算法询问复杂度与询问中限制集大小为 $\bm 2$ 的限制数 $\bm c$ 正相关，不妨考虑阈值分治的思想，设计一个当 $\bm c$ 较大时较快的算法**。

考虑将限制集大小为 $1$ 的限制表述成大小为 $2$ 的限制，这可通过容斥做到，一条限制集大小为 $1$ 的限制需要容斥为三条大小为 $2$ 的限制。此时我们需要求有多少对 $(i,j)$ 满足 $a_i+a_j$ 每一位都不等于给定数，这也可通过三进制 FWT 实现。

总时间复杂度 $O(n3^n+q\min(2^c,3^{n-c}))$，可以通过。

注意实现时不要在询问复杂度上乘上 $n$。

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
const int N=65536+10,M=4.4e7+10;
int n,m,q,u,u2,pw[20],tr[N],trp[128],ty[12][2],ct[12],op[20];
vector<int>vc;
ll cnt[M],F[M],ans;
inline int oper(int x,int y,int op){
	if(op>=3) return !oper(x,y,op-3);
	if(op==0) return x&y;
	if(op==1) return x|y;
	if(op==2) return x^y;
}
struct node{
	ll v0,v1;
	node(ll a=0,ll b=0){ v0=a,v1=b; }
	inline friend node operator+(const node &a,const node &b){
		return node(a.v0+b.v0,a.v1+b.v1);
	}
	inline friend node operator*(const node &a,const node &b){
		return node(a.v0*b.v0-a.v1*b.v1,a.v0*b.v1+a.v1*b.v0-a.v1*b.v1);
	}
}w1(0,1),w2(-1,-1),G[M];
inline void FWT1(node *c){
	for(int i=1,w=1;i<=n;i++,w*=3)
		for(int j=0;j<u;j+=w*3)
			for(int k=0;k<w;k++){
				int p0=j+k,p1=j+k+w,p2=j+k+w*2;
				node v0=c[p0],v1=c[p1],v2=c[p2];
				c[p0]=v0+v1+v2;
				c[p1]=v0+v1*w1+v2*w2;
				c[p2]=v0+v1*w2+v2*w1;
			}
}
inline void FWT2(ll *c){
	for(int i=1,w=1;i<=n;i++,w*=3)
		for(int j=0;j<u;j+=w*3)
			for(int k=0;k<w;k++){
				int p0=j+k,p1=j+k+w,p2=j+k+w*2;
				ll v0=c[p0],v1=c[p1],v2=c[p2];
				c[p0]=v1+v2,c[p1]=v0+v2,c[p2]=v0+v1;
			}
}
inline void IFWT(node *c){
	for(int i=1,w=1;i<=n;i++,w*=3)
		for(int j=0;j<u;j+=w*3)
			for(int k=0;k<w;k++){
				int p0=j+k,p1=j+k+w,p2=j+k+w*2;
				node v0=c[p0],v1=c[p1],v2=c[p2];
				c[p0]=v0+v1+v2;
				c[p1]=v0+v1*w2+v2*w1;
				c[p2]=v0+v1*w1+v2*w2;
			}
	for(int i=0;i<u;i++)
		c[i].v0/=u;
}
inline void dfs1(int u,int x){
	if(u==vc.size()){ ans+=cnt[x];return ; }
	int pt=op[vc[u]],uc=vc[u];
	if(ty[pt][0]==0||ty[pt][1]==0) dfs1(u+1,x+0*pw[uc]);
	if(ty[pt][0]==1||ty[pt][1]==1) dfs1(u+1,x+1*pw[uc]);
	if(ty[pt][0]==2||ty[pt][1]==2) dfs1(u+1,x+2*pw[uc]);
}
inline void dfs2(int u,int x,int k){
	if(u==vc.size()){ ans+=F[x]*k;return ; }
	int pt=op[vc[u]],uc=vc[u];
	dfs2(u+1,x+0*pw[uc],k*(ty[pt][0]==0?-1:1));
	dfs2(u+1,x+1*pw[uc],k*(ty[pt][0]==1?-1:1));
	dfs2(u+1,x+2*pw[uc],k*(ty[pt][0]==2?-1:1));
}
int main(){
	read(),n=read(),m=read(),q=read(),u2=u=1;
	pw[0]=1;
	for(int i=1;i<=n;i++) u2*=2,u*=3,pw[i]=u;
	for(int i=1;i<u2;i++)
		tr[i]=tr[i/2]*3+(i&1);
	for(int i=1;i<=m;i++)
		cnt[tr[read()]]++;
	for(int i=0;i<u;i++)
		G[i]=node(cnt[i]);
	FWT1(G);
	for(int i=0;i<u;i++)
		G[i]=G[i]*G[i];
	IFWT(G);
	for(int i=0;i<u;i++)
		F[i]=cnt[i]=G[i].v0;
	FWT2(F);
	tr['A']=0,tr['O']=1,tr['X']=2,
	tr['a']=3,tr['o']=4,tr['x']=5;
	for(int i=0;i<6;i++)
		for(int j=0;j<2;j++){
			int c=0,id=i*2+j;
			ty[id][1]=-1;
			if(oper(0,0,i)==j) ty[id][c++]=0;
			if(oper(0,1,i)==j) ty[id][c++]=1;
			if(oper(1,1,i)==j) ty[id][c++]=2;
			ct[id]=c;
		}
	while(q--){
		for(int i=0;i<n;i++) op[n-i-1]=tr[getc()];
		int x=read(),c1=0,c2=0;ans=0;
		for(int i=0;i<n;i++) op[i]=op[i]*2+(x>>i&1),ct[op[i]]==1?++c1:++c2;
		vc.clear();
		if(c2<=9){
			int s=0;
			for(int i=0;i<n;i++)
				if(ct[op[i]]==2) vc.push_back(i);
				else s+=pw[i]*ty[op[i]][0];
			dfs1(0,s);
		}else{
			int s=0;
			for(int i=0;i<n;i++)
				if(ct[op[i]]==1) vc.push_back(i);
				else s+=pw[i]*(ty[op[i]][0]^ty[op[i]][1]^3);
			dfs2(0,s,1),ans>>=c1;
		}
		write(ans),putc('\n');
	}
	flush();
}
```
