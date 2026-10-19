---
title: "题解 P10220【[省选联考 2024] 迷宫守卫】"
date: 2024-03-04
category: "题解"
summary: "Link 葬送了我 2024 省选的一题。 题意 有一颗深度为 n+1 的完全二叉树，其叶子上依次标有一个长为 2n 排列 a，非叶结点有选择代价 bi。Alice、Bob 两"
math: true
top: 2
source: https://www.luogu.com.cn/article/2ughj3h2
slug: 2ughj3h2
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10220)

葬送了我 2024 省选的一题。

## 题意

有一颗深度为 $n+1$ 的完全二叉树，其叶子上依次标有一个长为 $2^n$ 排列 $a$，非叶结点有选择代价 $b_i$。Alice、Bob 两人进行游戏。Alice 可以选择一些选择代价和不超过 $m$ 的非叶结点，此后 Bob 会从根开始深度优先搜索，有一初始为空的序列 $p$，设当前 Bob 在 $x$ 结点，

- 若 $x$ 结点为叶子，则将 $a_x$ 加入序列 $p$ 末尾；
- 若 $x$ 结点非叶子且被 Alice 选择，则 Bob 将先搜索左子树再搜索右子树；
- 若 $x$ 结点非叶子且未被 Alice 选择，则 Bob 将选择先搜索左子树还是先搜索右子树。

Alice 希望 $p$ 字典序尽量大，而 Bob 希望其尽量小。两人均采用最优策略，求最终的序列 $a$。多组数据。

$n\le 16$，$\sum 2^n\le 10^5$。
## 思路

设 $f_{i,x}$ 表示使得 Bob 进入 $i$ 子树后加入 $p$ 的第一个数为 $x$ 的最小代价，状态数总和为 $O(2^nn)$，容易转移（做后缀 $\min$、归并）：

$$f_{i,x}=\begin{cases}f_{ls,x}+\min(\min_{y>x}f_{rs,y},b_i)&x\in\text{subtree}(ls)\f_{rs,x}+\min_{y>x}f_{ls,y}&x\in\text{subtree}(rs)\end{cases}$$

那么 $p_1$ 的值就确定为满足 $f_{1,x}\le m$ 的最大的 $x$。

此后的选择都要满足 $p_1$ 固定，于是我们设计 $g_i$ 表示使得 $i$ 子树内已经填入 $p$ 内的数确定下来的最小代价，令 $h_i$ 表示子树内已经确定填入 $p$ 的第一个数，如果没有则为 $-1$。

$$g_{i}=\begin{cases}g_{ls}+g_{rs}&h_i=h_{ls}\land h_{rs}\ne -1\land h_{ls}<h_{rs}\g_{ls}+g_{rs}+b_i&h_i=h_{ls}\land h_{rs}\ne -1\land h_{ls}>h_{rs}\g_{ls}+\min(\min_{y>h_{i}}f_{rs,y},b_i)&h_i=h_{ls}\land h_{rs}= -1\\+\infty&h_i=h_{rs}\land h_{ls}\ne -1\land h_{ls}<h_{rs}\g_{ls}+g_{rs}&h_i=h_{rs}\land h_{ls}\ne -1\land h_{ls}>h_{rs}\g_{rs}+\min_{y>h_{i}}f_{ls,y}&h_i=h_{rs}\land h_{ls}= -1\end{cases}$$

选择完 $p_1$ 后，更新 $p_1$ 对应节点至根的 $g,h$，再从下至上依次调用另一颗子树的递归问题。根为 $i$ 的递归问题可考虑枚举子树内第一个数 $x$，将 $g_i,h_i$ 分别设为 $f_{i,x},x$ 再依次更新至根，检查 $g_1\le m$ 是否成立，再撤回更新。子树内第一个选取的数即为使得 $g_1\le m$ 成立的最大的 $x$，更新并递归即可。

每次计算 $g$ 如果都在所需的儿子的 $f$ 中二分，时间复杂度为 $O(2^nn^3)$，无法通过。注意到 $\min_{y>h_{i}}f_{*,y}$ 在 $h_i$ 确定后是不变的，可以在确定 $h_i$ 时就处理出，则每次更新一个点到根的复杂度降至 $O(n)$，总时间复杂度 $O(2^nn^2)$，可以通过。

注意到 $g$ 的转移方式仅与 $h$ 相关，可以在 $h_i$ 从 $-1$ 变为非 $-1$ 时算一下 $g_i$ 对 $g_1$ 的贡献。设定 $g_i,h_i$ 后可直接 $O(1)$ 求出对 $g_1$ 的贡献，时间复杂度降至 $O(2^nn)$。

代码（$O(2^nn)$）：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
inline ll read(){ }
inline void putc(char c){ }
inline void write(int x){ }
#define pii pair<int,ll>
#define mpr make_pair
#define fir first
#define sec second
const int N=(1<<17)+10;
const ll INF=1e16;
#define ls (x<<1)
#define rs (x<<1|1)
int n,m,p[N],rp[N],l[N],r[N];
ll k,w[N];
vector<int>vec;
vector<pii>f[N];
ll tm1[N],tm2[N];
pii g[N],pr[N];
bool gs[N],ty[N];
inline void dfs0(int x){
	ty[x]=0,g[x]=mpr(0,INF);
	f[x].clear();
	if(x>=n){
		l[x]=r[x]=x;
		f[x].push_back(mpr(p[x],0));
		return ;
	}
	dfs0(ls),dfs0(rs);
	l[x]=l[ls],r[x]=r[rs];
	vector<pii>a=f[ls],b=f[rs];
	for(int i=a.size()-2;i>=0;i--)
		a[i].sec=min(a[i].sec,a[i+1].sec);
	for(int i=b.size()-2;i>=0;i--)
		b[i].sec=min(b[i].sec,b[i+1].sec);
	a.push_back(mpr(0,INF)),b.push_back(mpr(0,INF));
	for(int i=0,j=0;i<a.size()-1||j<b.size()-1;){
		int nxa=i==a.size()-1?1e9:a[i].fir,
			nxb=j==b.size()-1?1e9:b[j].fir;
		if(nxa<nxb) f[x].push_back(mpr(nxa,f[ls][i].sec+min(b[j].sec,w[x]))),i++;
		else f[x].push_back(mpr(nxb,f[rs][j].sec+a[i].sec)),j++;
	}
}
inline void update(int x,int t){
	if(!x) return ;
	if(!ty[x]){
		ty[x]=1,g[x].fir=t;
		tm1[x]=tm2[x]=INF;
		for(auto tmp:f[ls]) if(tmp.fir>t) tm1[x]=min(tm1[x],tmp.sec);
		for(auto tmp:f[rs]) if(tmp.fir>t) tm2[x]=min(tm2[x],tmp.sec);
	}
	if(g[ls].fir==g[x].fir){//先走左儿子 
		if(ty[rs]) g[x].sec=g[ls].sec+g[rs].sec+(g[rs].fir<g[x].fir?w[x]:0);
		else g[x].sec=g[ls].sec+min(w[x],tm2[x]);
	}else{//先走右儿子 
		if(ty[ls]) g[x].sec=g[ls].fir>g[x].fir?g[ls].sec+g[rs].sec:INF;
		else g[x].sec=g[rs].sec+tm1[x];
	}
	update(x/2,t);
	if(x==1){
		gs[x]=1;
	}else if(gs[x/2]){
		if(x%2==0){
			if(g[x/2].fir==g[x].fir) gs[x]=1;
			else if(ty[x^1]&&g[x].fir>g[x/2].fir) gs[x]=1;
		}else{
			if(g[x/2].fir==g[x^1].fir) gs[x]=1;
			else if(!ty[x^1]||g[x^1].fir>g[x/2].fir) gs[x]=1;
		}
	}
}
inline bool check(int i,pii tmp){
	int x=i/2;
	if(!gs[x]) return g[1].sec<=k;
	pr[i]=g[i],g[i]=tmp,pr[x]=g[x],pr[1]=g[1],ty[i]=1;
	if(g[ls].fir==g[x].fir){
		if(ty[rs]) g[x].sec=g[ls].sec+g[rs].sec+(g[rs].fir<g[x].fir?w[x]:0);
		else g[x].sec=g[ls].sec+min(w[x],tm2[x]);
	}else{
		if(ty[ls]) g[x].sec=g[ls].fir>g[x].fir?g[ls].sec+g[rs].sec:INF;
		else g[x].sec=g[rs].sec+tm1[x];
	}
	ll v=pr[1].sec-pr[x].sec+g[x].sec;
	g[i]=pr[i],g[x]=pr[x],ty[i]=0;
	return v<=k;
}
inline void dfs(int x){
	int v=0;
	if(x==1){
		for(auto tmp:f[1])
			if(tmp.sec<=k)
				v=tmp.fir;
	}else{
		for(auto tmp:f[x])
			if(check(x,tmp))
				v=max(v,tmp.fir);
	}
	vec.push_back(v);
	g[rp[v]]=mpr(v,0),ty[rp[v]]=1;
	update(rp[v]/2,v);
	for(int i=rp[v];i!=x;i/=2)
		dfs(i^1);
}
int main(){
//	freopen("maze.in","r",stdin);
//	freopen("maze.out","w",stdout);
	int T=read();
	while(T--){
		m=read(),k=read(),n=1<<m;
		for(int i=1;i<n;i++)
			w[i]=read();
		for(int i=n;i<n*2;i++)
			rp[p[i]=read()]=i;
		vec.clear();
		dfs0(1);
		dfs(1);
		for(auto tmp:vec)
			write(tmp),putc(' ');
		putc('\n');
	}
}
```
