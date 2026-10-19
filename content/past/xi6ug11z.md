---
title: "题解 P8524【[Ynoi2078] 《太长了标题放不下》阅读报告（更新中...）】（Replaced）"
date: 2022-09-08
category: "题解"
summary: "Link 题目名称：《A theory of consciousness from a theoretical computer scienceperspective: Ins"
math: true
top: 2
source: https://www.luogu.com.cn/article/xi6ug11z
slug: xi6ug11z
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P8524)

题目名称：《A theory of consciousness from a theoretical computer scienceperspective: Insights from the Conscious Turing Machin》阅读报告（更新中...）

本题已被替换。
## 题意
给出一颗 $n$ 个点的树，$q$ 次询问，每次询问给出 $l,r$，求 $\displaystyle\min_{l\le i<j\le r}\text{dis}(i,j)$。强制在线。

$n,q\le 5\times 10^4$。
## 思路
平凡的区间点对问题。

分块，考虑询问，设左散块、整块、右散块分别为 $a,b,c$。

1. 询问同块或 $a-c$：块内按 $\text{dfn}$ 排序，取出散块，归并排序建虚树，标记原来的点为关键点，对于虚树上每个点维护一个 $dis_i$ 表示 $i$ 子树内离它最近的关键点和它之间的距离即可算出每两个关键点之间的最短距离。
2. $a-b$ 或 $b-c$：预处理 $res_{i,j}$ 表示点 $i$ 到块 $j$ 中任意一个点的最近距离。对于每个块 $j$，把所有的点放进队列 $\text{bfs}$ 一遍，求出所有的 $res_{i,j}$。std 为了维护点 $i$ 到区间块的最近距离写了一个 $O(n)-O(1)\text{ RMQ}$，其实没有必要，维护 $suf_{i,j}$ 表示点 $i$ 到块 $[bel_i+1,j]$ 的最近距离即可，同理维护 $pre_{i,j}$。
3. $b-b$：用虚树搞出 $ans_{i,j}$ 表示块 $i$ 和块 $j$ 的答案，再前缀 $\max$ 搞出 $ans'_{i,j}$ 表示块 $[i,j]$ 间的答案。

时间复杂度 $O(n\sqrt n)$。

代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
const int N=5e4+10,INF=1e9,sq=300,nq=N/sq+10;
int n,q,cnt,head[N],bl[nq],br[nq],blk,bel[N];
int ans[nq][nq],res[nq][N],pre[nq][N],suf[nq][N];
bool vis[N];
vector<int>b[nq];
struct Edge{
	int to,nxt;
}a[N<<1];
inline void add(int u,int v){
	cnt++;
	a[cnt].to=v;
	a[cnt].nxt=head[u];
	head[u]=cnt;
}
int dfn[N],tim,dep[N];
struct ST_table{
	int ind[N],lg[N<<1],cnt,st[18][N<<1];
	inline void dfs(int rt,int f){
		dep[rt]=dep[f]+1;
		st[0][++cnt]=rt,ind[rt]=cnt;
		dfn[rt]=++tim;
		for(int i=head[rt];i;i=a[i].nxt){
			int t=a[i].to;
			if(t==f) continue;
			dfs(t,rt);
			st[0][++cnt]=rt;
		}
	}
	inline int cmp(int x,int y){
		return dep[x]<dep[y]?x:y;
	}
	inline void init(){
		dfs(1,0);
		for(int i=1;(1<<i)<=cnt;i++)
	        for(int j=1;j+(1<<i)-1<=cnt;j++)
	            st[i][j]=cmp(st[i-1][j],st[i-1][j+(1<<i-1)]);
	    for(int i=2;i<=cnt;i++)
	    	lg[i]=lg[i>>1]+1;
	}
	inline int LCA(int x,int y){
		x=ind[x],y=ind[y];
		if(x>y) swap(x,y);
		int i=lg[y-x+1];
		int p=1<<i;
		return cmp(st[i][x],st[i][y-p+1]);
	}
	inline int dis(int x,int y){
		return dep[x]+dep[y]-2*dep[LCA(x,y)];
	}
}st;
inline bool cmp(int x,int y){
	return dfn[x]<dfn[y];
}
bool qry[N];
struct Query{
	int ans,top=0,stk[N],dis[N];
	vector<int>tmp;
	inline void add(int u,int v){
		if(dep[u]<dep[v]) swap(u,v);
		int w=dep[u]-dep[v];
		ans=min(ans,w+dis[u]+dis[v]);
	    tmp.push_back(u),tmp.push_back(v);
	    dis[v]=min(dis[v],w+dis[u]);
	}
	inline void build(vector<int>p){
		for(auto x:p)
			dis[x]=0;
		tmp.clear();
		stk[top=1]=p[0];
		for(int i=1;i<p.size();i++){
			int now=p[i];
			int lc=st.LCA(now,stk[top]);
			while(1){
				if(dep[lc]>=dep[stk[top-1]]){
					if(lc!=stk[top]){
						add(lc,stk[top]);
						if(lc!=stk[top-1]) stk[top]=lc;
						else top--;
					}
					break;
				}else{
					add(stk[top-1],stk[top]),top--;
				}
			}
			stk[++top]=now;
		}
		while(--top)
			add(stk[top],stk[top+1]);
		for(auto x:tmp)
			dis[x]=INF;
	}
	inline int query(vector<int>a,vector<int>b){
		ans=INF;
		vector<int>c;
		merge(a.begin(),a.end(),b.begin(),b.end(),back_inserter(c),cmp);
		build(c);
		return ans;
	}
}T;
inline void bfs(int L){
	queue<int>q;
	for(int i=1;i<=n;i++)
		vis[i]=0;
	for(int i=bl[L];i<=br[L];i++)
		q.push(i);
	while(!q.empty()){
		int x=q.front();
		q.pop();
		for(int i=head[x];i;i=a[i].nxt){
			int t=a[i].to;
			if(!vis[t])
				vis[t]=1,res[L][t]=res[L][x]+1,q.push(t);
		}
	}
}
inline vector<int> take(int l,int r){
	int L=bel[l];
	vector<int>t;
	for(auto x:b[L])
		if(l<=x&&x<=r)
			t.push_back(x);
	return t;
}
int last;
int main(){
	n=read();
	for(int i=1;i<n;i++){
		int u=read(),v=read();
		add(u,v),add(v,u);
	}
	st.init();
	for(int i=1;i<=n;i+=sq){
		bl[++blk]=i,br[blk]=min(i+sq-1,n);
		for(int j=bl[blk];j<=br[blk];j++)
			bel[j]=blk,b[blk].push_back(j);
		sort(b[blk].begin(),b[blk].end(),cmp);
	}
	memset(ans,127,sizeof(ans));
	for(int i=1;i<=blk;i++){
		ans[i][i]=T.query(b[i],vector<int>());
		for(int j=i+1;j<=blk;j++)
			ans[i][j]=T.query(b[i],b[j]);
	}
	for(int i=1;i<=blk;i++)
		for(int j=i+1;j<=blk;j++)
			ans[j][i]=min(ans[j][i],ans[j-1][i]);
	for(int i=1;i<=blk;i++)
		bfs(i);
	for(int i=1;i<=n;i++){
		suf[bel[i]][i]=INF;
		for(int j=bel[i]+1;j<=blk;j++)
			suf[j][i]=min(suf[j-1][i],res[j][i]);
	}
	for(int i=1;i<=n;i++){
		pre[bel[i]][i]=INF;
		for(int j=bel[i]-1;j>=1;j--)
			pre[j][i]=min(pre[j+1][i],res[j][i]);
	}
	int q=read();
	while(q--){
		int l=read(),r=read();
		if(l>=r) write(-1),last=0;
		else if(bel[l]==bel[r]) write(last=T.query(take(l,r),vector<int>()));
		else{
			int L=bel[l],R=bel[r];
			last=T.query(take(l,br[L]),take(bl[R],r));
			if(L+1<=R-1){
				last=min(last,ans[L+1][R-1]);
				for(int i=l;i<=br[L];i++)
					last=min(last,suf[R-1][i]);
				for(int i=bl[R];i<=r;i++)
					last=min(last,pre[L+1][i]);
			}
			write(last);
		}
		putc('\n');
	}
	flush();
}
```
再见 qwq~
