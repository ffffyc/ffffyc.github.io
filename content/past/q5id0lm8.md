---
title: "题解：P11369 [Ynoi2024] 弥留之国的爱丽丝"
date: 2024-12-05
category: "题解"
summary: "Link 题意 给你 n 个结点和 m 条有向边。每条边的颜色为黑白二色之一，初始所有边都是黑色的。 你需要进行如下两种操作共 q 次操作： 1 k，表示将第 k 条边的颜色进"
math: true
top: 2
source: https://www.luogu.com.cn/article/q5id0lm8
slug: q5id0lm8
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P11369)
## 题意

给你 $n$ 个结点和 $m$ 条有向边。每条边的颜色为黑白二色之一，初始所有边都是黑色的。

你需要进行如下两种操作共 $q$ 次操作：

- `1 k`，表示将第 $k$ 条边的颜色进行反转。
- `2 u v`，表示询问是否能从 $u$ 只经过黑色的边走到 $v$。

$n\le 5\times 10^4$，$m,q\le 10^5$。
## 题解
首先问题肯定不弱于 DAG 可达性问题，所以我们只需要考虑除以 $\omega$ 的算法。

按 $b$ 进行时间分块，取出这 $b$ 次操作中的关键点与关键边。先使用所有黑色的非关键边进行缩点，并预处理两两关键点之间能否通过这些边到达，使用 `bitset`，只需维护每个点能否到达每个关键点，时间复杂度 $O(\dfrac{q}{b}\cdot (n+m)\cdot\dfrac{b+\omega}{\omega})$。

询问时使用 `bitset` 优化 BFS 即可，时间复杂度 $O(q\cdot\dfrac{b^2}{\omega})$。

取 $b=(n+m)^{1/3}\omega^{1/3}$，得到时间复杂度 $O(\dfrac{q(n+m)+q(n+m)^{2/3}\omega^{2/3}}{\omega})$。

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
//b=[(n+m)*w]^{1/3}
//O(q*(n+m)*w^{-1}+q*(n+m)^{2/3}*w^{-1/3})
const int N=5e4+10,M=1e5+10,B=220,C=B*2+10;
int n,m,q,u[M],v[M];
bool ans[M];
struct Query{
	int op,u,v;
}qr[M]; 
vector<int>a[N],b[N];
int tim,dfn[N],low[N],bel[N],stk[N],top,blk;
bool inc[N],col[M],inb[M];
inline void Tarjan(int x){
	dfn[x]=low[x]=++tim,inc[x]=1,stk[++top]=x;
	for(auto t:a[x]){
		if(!dfn[t]) Tarjan(t),low[x]=min(low[x],low[t]);
		else if(inc[t]) low[x]=min(low[x],low[t]);
	}
	if(dfn[x]==low[x]){
		++blk;
		while(1){
			int p=stk[top--];
			inc[p]=0,bel[p]=blk;
			if(p==x) break;
		}
	}
} 
inline void init(){
	for(int i=1;i<=n;i++)
		dfn[i]=bel[i]=inc[i]=0,
		a[i].clear(),b[i].clear();
	top=tim=blk=0;
	for(int i=1;i<=m;i++)
		if(col[i]&&!inb[i])
			a[u[i]].push_back(v[i]);
}
inline void build(){
	init();
	for(int i=1;i<=n;i++)
		if(!dfn[i])
			Tarjan(i);
}
int id[C],c,rd[N];
bitset<C>f[N],pt[C],r[C],vis,cur;
inline bool query(int u,int v){
	vis.reset(),cur.reset();
	cur[u]=1;
	for(;!cur[v];){
		int p=(cur&~vis)._Find_first();
		if(p==cur.size()) return 0;
		vis[p]=1,cur=cur|pt[p]|r[p];
	}
	return 1;
}
int ct[C][C];
inline void solve(int L,int R){
	c=0;
	for(int i=1;i<=n;i++)
		rd[i]=0,f[i].reset();
	for(int i=1;i<=m;i++)
		inb[i]=0;
	vector<int>p;
	for(int i=L;i<=R;i++){
		int u=qr[i].u,v=qr[i].v;
		if(qr[i].op==1) p.push_back(::u[u]),p.push_back(::v[u]),inb[u]=1;
		else p.push_back(u),p.push_back(v);
	}
	for(int i:p)
		if(!rd[i])
			rd[i]=++c,id[c]=i; 
	build();
	for(int i=1;i<=c;i++)
		f[bel[id[i]]][i]=1;
	for(int i=1;i<=m;i++)
		if(col[i]&&!inb[i])
			b[bel[u[i]]].push_back(bel[v[i]]);
	for(int i=1;i<=blk;i++)
		for(auto j:b[i])
			f[i]|=f[j];
	for(int i=1;i<=c;i++)
		pt[i].reset(),r[i].reset();
	for(int i=1;i<=c;i++)
		for(int j=1;j<=c;j++)
			pt[i][j]=f[bel[id[i]]][j];
	for(int i=1;i<=m;i++)
		if(col[i]&&inb[i])
			r[rd[u[i]]][rd[v[i]]]=1,
			ct[rd[u[i]]][rd[v[i]]]++;
	for(int i=L;i<=R;i++){
		int op=qr[i].op;
		if(op==1){
			int id=qr[i].u;
			col[id]^=1;
			if(col[id]) ct[rd[u[id]]][rd[v[id]]]++,r[rd[u[id]]][rd[v[id]]]=1;
			else ct[rd[u[id]]][rd[v[id]]]--,!ct[rd[u[id]]][rd[v[id]]]&&(r[rd[u[id]]][rd[v[id]]]=0);
		}else{
			int u=qr[i].u,v=qr[i].v;
			ans[i]=query(rd[u],rd[v]);
		}
	}
	for(int i=1;i<=m;i++)
		if(col[i]&&inb[i])
			ct[rd[u[i]]][rd[v[i]]]--;
}
int main(){
	n=read(),m=read(),q=read();
	for(int i=1;i<=m;i++)
		u[i]=read(),v[i]=read(),col[i]=1;
	for(int i=1;i<=q;i++){
		int op=read(),u=read(),v=0;
		if(op==2) v=read();
		qr[i]={op,u,v};
	}
	for(int i=1;i<=q;i+=B)
		solve(i,min(i+B-1,q));
	for(int i=1;i<=q;i++)
		if(qr[i].op==2)
			puts(ans[i]?"YES":"NO");
	flush();
}
```
