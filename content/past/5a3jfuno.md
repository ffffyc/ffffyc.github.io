---
title: "题解 【[JRKSJ R ] deknvsq】"
date: 2021-10-14
category: "题解"
summary: "点 分 树 推 广 题。 打个广告：点分树题单。 题意 求树上从 x 出发路径长度 k 且路径上（包括起点与终点）不经过 y 的路径的边权和的和。q 次询问。强制在线。 n,q"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/5a3jfuno
slug: 5a3jfuno
---

点 分 树 推 广 题。

打个广告：[点分树题单](https://www.luogu.com.cn/training/78277)。
## 题意
求树上从 $x$ 出发路径长度 $k$ 且路径上（包括起点与终点）不经过 $y$ 的路径的边权和的和。$q$ 次询问。强制在线。

$n,q\le 5\times 10^5$.
## 题解
### $\text{Subtask 1}$
特殊性质：$n,q\le 10^4$。

暴力 $\text{dfs}$，时间复杂度 $O(nq)$，期望得分 $20\text{pts}$。
### $\text{Subtask 2}$
特殊性质：$k\le 2$。

和 [$\text{R3 a question}$](https://www.luogu.com.cn/blog/cyffff/solution-JRKSJ-R3-A) 的维护方法差不多，简单分类讨论即可。时间复杂度 $\Theta(n+q)$，期望得分 $10\text{pts}$。
### $\text{Subtask 3}$
特殊性质：树为链。

考虑 $dis_0(x,y)\le k$ 时连向 $y$ 的那一边无贡献，其余一边或其他情形可以找出以链首为根时的 $k$ 级儿子或者父亲的位置计算。需要注意链首不一定是 $1$。时间复杂度 $O((n+q)\log n)$，期望得分 $20\text{pts}$。
### $\text{Subtask 4}$
特殊性质：保证询问的 $x,y$ 之间有边。

假定 $1$ 为根。考虑 $x,y$ 的位置关系：
- $y\in\text{son}(x)$，考虑建立点分树，计算出 $\displaystyle\sum_{i=1}^n[dis_0(x,i)=k]dis_1(x,i)$ 之后减去 $\displaystyle\sum_{i=1}^n[dis_0(x,i)=k][i\in \text{subtree}(x,y)]dis_1(x,i)$ 即可，对每个 $dep$ 建立动态开点线段树，初始化在 $dfn_i$ 加上 $1\sim i$ 的路径权值和，进行区间求和即可；
- $y=\text{fa}(x)$，直接使用线段树做即可。

细节：
- 这题比较难带修，所以建立点分树的时候可以直接按照定义，搜索 $i$ 的子树并累加答案。
- 点分树内部不需要使用数据结构，直接开个数组即可，注意要动态分配内存，且询问时要有意义的距离再计算。
- 求 $\text{LCA}$ 不能使用倍增，否则复杂度会退化。可能会被卡常。

时间复杂度 $\Theta((n+q)\log n)$，期望得分 $20\text{pts}$。
### $\text{Subtask 5}$
无特殊性质，$n,q\le 5\times 10^5$。

假定 $1$ 为根。考虑 $x,y$ 的位置关系：
- $y\in\text{subtree}(x)$：与 $\text{Subtask 4}$ 做法无异；
- $y\notin\text{subtree}(x)\text{ and }y\notin\text{ancestors}(x)$：将 $k$ 减去 $dis_0(x,y)$，之后就是查询 $y,\text{fa}(y),k-dis_0(x,y)$ 了，线段树，与 $\text{Subtask 4}$ 做法无异；
- $y\in\text{ancestors}(x)$：将 $k$ 减去 $dis_0(x,y)$，考虑计算出 $y$ 的儿子中是 $x$ 的祖先的点 $z$，这个可以树上 $k$ 级祖先，倍增即可，之后就是查询 $y,z,k-dis_0(x,y)$ 了，点分树，与 $\text{Subtask 4}$ 做法无异。

注意后两种情况还得算上 $x\sim y$ 路径上的贡献。

细节挺多的，建议看代码理解。

你会发现恰好这里每一步的时空都是 $O(n\log n)$ 的，时间复杂度 $\Theta((n+q)\log n)$，但是常数十分可怕，期望得分 $100\text{pts}$。

std：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ui unsigned
#define ll long long
#define fir first
#define sec second
#define mpr make_pair
#define pii pair<int,int>
#define puu pair<ui,ui>
namespace IO{//by cyffff
	
}
const int N=5e5+10,INF=1e9+10;
int head[N],sz[N],cnt,n,m,siz[N],f[N],val[N],lst;
bool vis[N];
struct Edge{
	int to,nxt,w;
}a[N<<1];
inline void add(int u,int v,int w){
	cnt++;
	a[cnt].to=v;
	a[cnt].nxt=head[u];
	a[cnt].w=w;
	head[u]=cnt;
}
vector<int>son[N];
inline pii findroot(int rt,int f,int pre){
	sz[rt]=1;
	int mx=0;
	pii ans=mpr(INF,0);
	for(int i=head[rt];i;i=a[i].nxt){
		int t=a[i].to;
		if(vis[t]||t==f) continue;
		ans=min(ans,findroot(t,rt,pre));
		sz[rt]+=sz[t];
		mx=max(mx,sz[t]);
	}
	ans=min(ans,mpr(max(mx,pre-sz[rt]),rt));
	if(!ans.sec) ans.sec=rt;
	return ans;
}
//sz 为原树子树大小
//siz 为点分树子树大小 
inline void build(int rt,int s){
	vis[rt]=1;
	siz[rt]=s;
	for(int i=head[rt];i;i=a[i].nxt){
		int t=a[i].to;
		if(vis[t]) continue;
		int vsz;
		if(sz[t]<sz[rt]) vsz=sz[t];
		else vsz=s-sz[rt];
		int v=findroot(t,rt,vsz).sec;
		son[rt].push_back(v);
		f[v]=rt;
		build(v,vsz);
		//vsz 为这个儿子的点分树大小 
	}
}
int dfn[N],low[N],tim,fa[21][N];
ui dep[2][N];
struct ST_table{
	int ind[N],lg[N<<1],cnt,st[20][N<<1];
	inline void dfs(int rt,int f){
		dep[0][rt]=dep[0][f]+1,fa[0][rt]=f;
		st[0][++cnt]=rt,ind[rt]=cnt;
		dfn[rt]=++tim;
		for(int i=head[rt];i;i=a[i].nxt){
			int t=a[i].to;
			if(t==f) continue;
			dep[1][t]=dep[1][rt]+a[i].w;
			dfs(t,rt);
			st[0][++cnt]=rt;
		}
		low[rt]=tim;
	}
	inline int cmp(int x,int y){
		return dep[0][x]<dep[0][y]?x:y;
	}
	inline void init(){
		dfs(1,0);
		for(int i=1;(1<<i)<=cnt;i++)
	        for(int j=1;j+(1<<i)-1<=cnt;j++)
	            st[i][j]=cmp(st[i-1][j],st[i-1][j+(1<<i-1)]);
	    for(int i=1;i<=20;i++)
	    	for(int j=1;j<=n;j++)
	    		fa[i][j]=fa[i-1][fa[i-1][j]];
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
	inline ui dis(int x,int y,int k){
		return dep[k][x]+dep[k][y]-2*dep[k][LCA(x,y)];
	}
}st;
ui pool[N*80],*now=pool,*ds1[N],*ds2[N],*ds1cnt[N],*ds2cnt[N];
struct Point_Divide_Tree{
	inline void insert(int x,int r){
		int s1=st.dis(x,r,0),s2=st.dis(x,f[r],0);
		ui S1=st.dis(x,r,1),S2=st.dis(x,f[r],1);
		ds1[r][s1]+=S1,ds1cnt[r][s1]++;
		if(f[r])
			ds2[r][s2]+=S2,ds2cnt[r][s2]++;
		for(auto t:son[x])
			if(t!=f[x])
				insert(t,r);
	}
	inline void init(){
		st.init();
		int rt=findroot(1,0,n).sec;
		build(rt,n);
		for(int i=1;i<=n;i++){
			int s=siz[i];
			ds1[i]=now,now+=s+2,ds2[i]=now,now+=s+2;
			ds1cnt[i]=now,now+=s+2,ds2cnt[i]=now,now+=s+2;
			insert(i,i);
		}	
	}
	inline ui query(int x,int k){
		int cur=x,lst=0;
		ui ans=0;
		while(cur){
			int d=st.dis(x,cur,0);
			if(d<=k&&k-d<=siz[cur]){
				ui s=st.dis(x,cur,1);
				ans+=ds1[cur][k-d]+ds1cnt[cur][k-d]*s;
				if(lst&&k-d<=siz[lst])
					ans-=ds2[lst][k-d]+ds2cnt[lst][k-d]*s;
			}
			lst=cur;
			cur=f[cur];
		}
		return ans;
	}  
	inline ui query_cnt(int x,int k){
		int cur=x,lst=0;
		ui ans=0;
		while(cur){
			int d=st.dis(x,cur,0);
			if(d<=k&&k-d<=siz[cur]){
				ans+=ds1cnt[cur][k-d];
				if(lst&&k-d<=siz[lst])
					ans-=ds2cnt[lst][k-d];
			}
			lst=cur;
			cur=f[cur];
		}
		return ans;
	}  
}t1;
inline int kthF(int x,int k){
	for(int i=20;i>=0;i--)
		if(k>>i&1)
			x=fa[i][x],k-=1<<i;
	return x;
}
inline puu operator+(const puu &a,const puu &b){
	return mpr(a.fir+b.fir,a.sec+b.sec);
}
struct node{
	int ls,rs;
	ui ans,cnt;
}nd[N*20];
int root[N],ncnt;
struct Segment{
	#define ls (nd[rt].ls)
	#define rs (nd[rt].rs)
	inline void pushup(int rt){
		nd[rt].ans=nd[ls].ans+nd[rs].ans;
		nd[rt].cnt=nd[ls].cnt+nd[rs].cnt;
	}
	inline void insert(int &rt,int l,int r,int p,ui k){
		if(!rt) rt=++ncnt;
		if(l==r){
			nd[rt].ans+=k;
			nd[rt].cnt++;
			return ;
		}
		int mid=l+r>>1;
		if(p<=mid) insert(ls,l,mid,p,k);
		else insert(rs,mid+1,r,p,k);
		pushup(rt);
	}
	inline puu query(int rt,int l,int r,int L,int R){
		if(!rt) return mpr(0,0);
		if(L<=l&&r<=R) return mpr(nd[rt].ans,nd[rt].cnt);
		int mid=l+r>>1; 
		puu ans=mpr(0,0);
		if(L<=mid) ans=ans+query(ls,l,mid,L,R);
		if(R> mid) ans=ans+query(rs,mid+1,r,L,R);
		return ans;
	}
}t2;
inline ui dele1(int x,puu tmp){
	return tmp.fir-tmp.sec*dep[1][x];
}
inline ui dele2(int x,int y,puu tmp){
	return tmp.fir-tmp.sec*dep[1][y]+tmp.sec*st.dis(x,y,1);
}
inline ui query1(int x,int y,int k){//y 在 x 子树中 
	int tmp=dep[0][x]+k;
	if(tmp>n)
		return t1.query(x,k);
	return t1.query(x,k)-dele1(x,t2.query(root[tmp],1,n,dfn[y],low[y]));
}
inline ui query2(int x,int y,int k){//y 不在 x 子树中且 y 不是 x 的祖先 
	int tmp=st.dis(x,y,0),tmp2=dep[0][y]+k-tmp;
	if(tmp>k||tmp2>n)
		return t1.query(x,k);
	return t1.query(x,k)-dele2(x,y,t2.query(root[tmp2],1,n,dfn[y],low[y])); 
}
inline ui query3(int x,int y,int k){//y 不在 x 子树中且 y 是 x 的祖先
	int tmp=dep[0][x]-dep[0][y];
	ui s=dep[1][x]-dep[1][y];
	if(tmp>k)
		return t1.query(x,k);
	int ys=kthF(x,tmp-1),tmp2=dep[0][y]+k-tmp;
	return t1.query(x,k)-query1(y,ys,k-tmp)-(t1.query_cnt(y,k-tmp)-(tmp2<=n?t2.query(root[tmp2],1,n,dfn[ys],low[ys]).sec:0))*s;
}
ui last;
int main(){
	n=read(),m=read();
	for(int i=1;i<n;i++){
		int u=read(),v=read(),w=read();
		add(u,v,w),add(v,u,w);
	}
	t1.init();
	for(int i=1;i<=n;i++)
		t2.insert(root[dep[0][i]],1,n,dfn[i],dep[1][i]);
	int cnt=0;
	while(m--){
		ui x=read()^last,y=read()^last,k=read()^last;
		int tmp=st.LCA(x,y);
		if(x==y) write(last=0);
		else if(tmp==x) write(last=query1(x,y,k));
		else if(tmp!=y) write(last=query2(x,y,k));
		else write(last=query3(x,y,k)),cnt++;
		putc('\n');
	}
	flush();
}
```
再见 qwq~
