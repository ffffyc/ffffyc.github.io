---
title: "题解：P14471 [集训队互测 2025] 火花"
date: 2025-11-14
category: "题解"
summary: "Link 非常有学习价值的题目。 题意 给定一颗 n 个点的树，给定常数 k,t 与序列 c1 n,v1 n，结点 i 上有 ci 个价值为 vi 的物品。 接下来 A 与 B"
math: true
top: 2
source: https://www.luogu.com.cn/article/nj1vxml8
slug: nj1vxml8
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P14471)

非常有学习价值的题目。
## 题意

给定一颗 $n$ 个点的树，给定常数 $k,t$ 与序列 $c_{1\sim n},v_{1\sim n}$，结点 $i$ 上有 $c_i$ 个价值为 $v_i$ 的物品。

接下来 A 与 B 先后取物品：
- A 可以总共选择不超过 $t$ 个互不相同的结点，对于每个选择的结点，从该结点到根路径上所有结点取走一个物品。
- B 可以总共取走不超过 $k$ 个物品，要求 B 取过物品的结点形成包含根的连通块。

最大化 A 与 B 取到的物品的价值总和。

$n,k\le 10^4$，$nk(t+1)\le 10^7$，**保证 $\bm{t<\min c_i}$**。
## 题解
先看 $t=0$ 的部分分，这是简单的树形依赖背包模板，使用 DFS 序的解法，在 DFS 序上进行 DP，处理到点 $p$ 时决定取走点 $p$ 中至少一个物品或者跳过 $p$ 的子树，使用单调队列优化即可。

记 $s_x$ 表示 $x$ 到根路径上的结点的单价和，表示 A 选择结点 $x$ 的收益。

本题主要的难点为 A 在当前处理的结点 $p$ 处取走的物品依赖于子树中选择了多少结点，而我们对 B 进行树形依赖背包时会从浅至深决策。

为了解决这个问题，我们**对欧拉序进行 DP**。在进入 $p$ 子树和离开 $p$ 子树时分别进行一部分决策。

注意到我们需要两次处理到 $p$ 之间中有多少结点被 A 选择，这**启示我们记录前缀和/后缀和，差分得到所需信息**。不妨使用前缀和，定义状态 $f_{i,j,l}$ 表示处理到欧拉序的第 $i$ 项，前面 B 选择了 $j$ 件物品，A 选择了 $l$ 个结点。

具体转移如下，设当前结点为 $p$：
- 如果这是 $p$ 初次出现，即进入 $p$ 子树：
  - 决策 B 是否取走 $p$ 上物品：
    - 如果取走了，那么限制取走 $[1,l+1]$ 个物品，转移至 $i+1$；
    - 如果不取走，那么决策子树中 A 取走了多少个结点，显然会取走 $s_x$ 最大的若干个结点，转移至 $i+2\cdot siz_p$；
- 如果这是 $p$ 第二次出现，即离开 $p$ 子树：
  - 决策 A 是否选择结点 $p$：
    - 如果选择了，那么再允许 B 取走 $[0,c_p-l-1)$ 个物品；
    - 如果不选择，那么再允许 B 取走 $[0,c_p-l-1]$ 个物品；

可以发现，两次允许 B 取走的物品之和为 $c_p$ 减去在 $p$ 子树中 $l$ 的增加量，且由于 $t<c_p$，两次决策都是良定义的。

对于跳过子树的部分，记 $g_{p,i}$ 表示 $p$ 子树中 $s_x$ 的前 $i$ 大之和，因为 $g_{p,i}$ 明显是凸的，所以 $f_{i,j,*}$ 与 $g_{p,*}$ 的 $(\max,+)$ 卷积可以通过决策单调性做到 $O(t\log t)\sim O(t)$。

总时间复杂度 $O(nkt\log t)\sim O(nkt)$。

:::info[代码]
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
#define vi vector<ll>
const int N=2e4+10;
const ll INF=1e18;
inline void upd(ll &x,ll y){ x=max(x,y); }
int n,k,t,fa[N],siz[N],id[N],op[N],tim,c[N],v[N];
ll s[N];
vi sc[N];
vector<vi>f[N];
vector<int>a[N];
//f[i][j][l] 表示考虑到 i，前面二阶段选了 j 个，一阶段选了 l 个 
inline void merges(vi &a,vi b){
	vi c(a.size()+b.size());
	merge(a.begin(),a.end(),b.begin(),b.end(),c.begin(),greater<ll>());
	swap(a,c);
	if(a.size()>t) a.resize(t);
}
inline void dfs(int x){
	sc[x].emplace_back(s[x]),id[++tim]=x,siz[x]=1;
	for(auto t:a[x])
		dfs(t),siz[x]+=siz[t],merges(sc[x],sc[t]);
	id[++tim]=x,op[tim]=1;
}
int que[N];
inline vi solve1(const vi &a,int v,int c){
	vi b(k+1,-INF);
//	for(int i=0;i<=k;i++){
//		ll mx=0;
//		for(int j=1;j<=min(i,c);j++)
//			upd(mx,a[i-j]+1ll*j*v);
//		b[i]=mx;
//	}
	int hd=1,tl=0;
	for(int i=0;i<=k;i++){
		while(hd<=tl&&i-que[hd]>c) hd++;
		if(hd<=tl) b[i]=a[que[hd]]+1ll*v*(i-que[hd]);
		while(hd<=tl&&a[que[tl]]+1ll*v*(i-que[tl])<=a[i]) tl--;
		que[++tl]=i;
	}
	return b;
}
inline void solve2(const vi &a,vi &b,int p,int l,int r,int L,int R){
	if(l>r) return ;
	if(L==R){
		for(int i=l;i<=r;i++)
			b[i]=a[i-L]+sc[p][L];
		return ;
	}
	int mid=l+r>>1,ps=0;
	ll ans=-INF;
	for(int i=L;i<=min(R,mid);i++)
		if(a[mid-i]+sc[p][i]>ans)
			ans=a[mid-i]+sc[p][i],ps=i;
	b[mid]=ans;
	solve2(a,b,p,l,mid-1,L,ps);
	solve2(a,b,p,mid+1,r,ps,R);
}
int main(){
	n=read(),k=read(),t=read();
	for(int i=1;i<=n;i++)
		c[i]=read(),s[i]=v[i]=read();
	for(int i=2;i<=n;i++)
		a[fa[i]=read()].push_back(i),s[i]+=s[fa[i]];
	dfs(1);
	for(int i=1;i<=tim+1;i++)
		f[i]=vector<vi>(k+1,vi(t+1,-INF));
	f[1][0][0]=0;
	for(int i=1;i<=tim;i++){
		int p=id[i];
		for(int l=0;l<=t;l++){
			vi a(k+1);
			for(int j=0;j<=k;j++) a[j]=f[i][j][l];
			if(op[i]==0){
				vi b=solve1(a,v[p],l+1);
				for(int j=0;j<=k;j++) upd(f[i+1][j][l],b[j]); 
			}else{
				vi b=solve1(a,v[p],c[p]-l-2);
				for(int j=0;j<=k;j++) b[j]=max(b[j],a[j]);
				for(int j=0;j<=k;j++) upd(f[i+1][j][l],max(b[j],j>=c[p]-l-1?a[j-(c[p]-l-1)]+1ll*v[p]*(c[p]-l-1):-INF)); 
				if(l<t) for(int j=0;j<=k;j++) upd(f[i+1][j][l+1],b[j]+s[p]);
			}
		}
		if(op[i]==0){
			for(int c=1;c<sc[p].size();c++) sc[p][c]+=sc[p][c-1];
			sc[p].insert(sc[p].begin(),0);
			for(int j=0;j<=k;j++){
				vi a(t+1),b(t+1);
				for(int l=0;l<=t;l++) a[l]=f[i][j][l];
//				for(int l=0;l<=t;l++){
//					ll mx=-INF;
//					for(int c=0;c<=l&&c<sc[p].size();c++)
//						upd(mx,a[l-c]+sc[p][c]);
//					upd(f[i+siz[p]*2][j][l],mx);
//				}
				solve2(a,b,p,0,t,0,sc[p].size()-1);
				for(int l=0;l<=t;l++) upd(f[i+siz[p]*2][j][l],b[l]);
			}
		}
	}
	ll ans=0;
	for(int j=0;j<=k;j++)
		upd(ans,f[tim+1][j][t]);
	write(ans);
	flush();
}
```

:::
