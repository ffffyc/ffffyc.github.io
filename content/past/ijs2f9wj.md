---
title: "题解 P8935【[JRKSJ R7] 茎】"
date: 2022-12-23
category: "题解"
summary: "Link 题意 你有一棵 n 个点的根节点为 1 的有根树，现在你要对这棵树进行剪枝，每次你可以选择一个还未被剪掉的节点 u 进行操作，然后剪掉 u 的子树所有点（包括 u）。"
math: true
top: 2
source: https://www.luogu.com.cn/article/ijs2f9wj
slug: ijs2f9wj
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P8935)
## 题意
你有一棵 $n$ 个点的根节点为 $1$ 的有根树，现在你要对这棵树进行剪枝，每次你可以选择一个还未被剪掉的节点 $u$ 进行操作，然后剪掉 $u$ 的子树所有点（包括 $u$）。当且仅当你剪掉 $1$ 时，操作停止。 

你需要在恰好第 $k$ 次剪枝时对 $x$ 进行操作，求有多少种不同的操作序列，对 $10^9+7$ 取模。

$1\le k\le n\le 500$。
## 思路
考虑先算 $f_{u,i}$ 表示 $u$ 子树内进行 $i$ 次操作，不必须删完的方案数。先得到不考虑 $u$ 的方案数，转移为 $f_{u,0}=1$，$\displaystyle\forall t\in \text{sons}(u),f_{u,i}f_{t,j}\binom{i+j}{j}\to f_{u,i+j}$。再考虑 $u$，$f_{u,i}\gets f_{u,i}+f_{u,i-1}$。

令 $x$ 与其祖先组成的点集为 $S$，从 $1$ 开始向 $x$ 倒序 DP。我们定义 $g_{u,i}$ 表示考虑到 $S$ 中 $u$ 及其所有祖先，我们已经钦定了这些点的不在 $S$ 中的子树的**在 $u$ 之前**的 $i$ 个操作。这些操作有相对顺序，但还未被放在操作序列中。

我们令 $h_{u,i}$ 表示 $u$ 不在 $S$ 内的子树进行 $i$ 次操作的方案数。$h_{u,0}=1$，$\displaystyle\forall t\in \text{sons}(u)\text{ and }t\notin S,h_{u,i}f_{t,j}\binom{i+j}{j}\to h_{u,i+j}$。

考虑一次转移，当 $u$ 不被操作时，$g_{u,i}=g_{fa_u,i}$。注意 $x$ 不能不被操作。当 $u$ 被放在 $p$ 位置时，$g_{fa_u,p+k}$ 都可以转移到 $g_{u,p}$。再将 $u$ 不在 $S$ 中的子树的操作加入到 $j$ 中：$\displaystyle g_{x,i}h_{x,l}\binom{i+l}{l}\to g_{x,i+l}$。

最终的答案为 $g_{x,k-1}$。

使用后缀和优化，时间复杂度为 $O(n^2)$。

代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
const int N=500+10,mod=1e9+7;
int n,k,p,fac[N],ifac[N],cnt,head[N];
struct Edge{
	int to,nxt;
}a[N<<1];
inline void add(int u,int v){
	cnt++;
	a[cnt].to=v;
	a[cnt].nxt=head[u];
	head[u]=cnt;
}
inline int qpow(int x,int y){
	int res=1;
	while(y){
		if(y&1) res=1ll*res*x%mod;
		x=1ll*x*x%mod;
		y/=2; 
	}
	return res;
}
inline void Prefix(int n){
	fac[0]=1;
	for(int i=1;i<=n;i++)
		fac[i]=1ll*fac[i-1]*i%mod;
	ifac[n]=qpow(fac[n],mod-2);
	for(int i=n;i;i--)
		ifac[i-1]=1ll*ifac[i]*i%mod;
}
inline int C(int n,int m){
	return n<m?0:1ll*fac[n]*ifac[m]%mod*ifac[n-m]%mod;
}
int f[N][N],g[2][N*2],pr[N],tmp[N],fr[N],siz[N],ans;
bool fl[N];
inline void dfs(int x,int fa){
	f[x][0]=1,fr[x]=fa;
	for(int i=head[x];i;i=a[i].nxt){
		int t=a[i].to;
		if(t==fa) continue;
		dfs(t,x);
		for(int j=siz[x];j>=0;j--)
			for(int k=siz[t];k>=1;k--)
				f[x][j+k]=(f[x][j+k]+1ll*f[x][j]*f[t][k]%mod*C(j+k,k))%mod;
		siz[x]+=siz[t];
	}
	for(int i=siz[x];i>=0;i--)
		f[x][i+1]=(f[x][i+1]+f[x][i])%mod; 
	siz[x]++;
}
inline void oth(int x){//这个节点其它子树 i 次操作的方案数 
	int s=0;
	tmp[0]=1;
	for(int i=1;i<=n;i++)
		tmp[i]=0;
	for(int i=head[x];i;i=a[i].nxt){
		int t=a[i].to;
		if(t==fr[x]||fl[t]) continue;
		for(int j=s;j>=0;j--)
			for(int k=siz[t];k>=1;k--)
				tmp[j+k]=(tmp[j+k]+1ll*tmp[j]*f[t][k]%mod*C(j+k,k))%mod;
		s+=siz[t];
	}
}
vector<int>s;
int main(){
	n=read(),k=read(),p=read();
	Prefix(n);
	for(int i=1;i<n;i++){
		int u=read(),v=read();
		add(u,v),add(v,u);
	}
	dfs(1,0);
	int t=p;
	while(t){
		s.push_back(t);
		fl[t]=1,t=fr[t];
	}
	reverse(s.begin(),s.end());
	oth(s[0]);
	int l=s.size();
	for(int j=0;j<=n;j++)
		g[0][j]=tmp[j];
	for(int i=1;i<s.size();i++){
		int c=i&1;
		oth(s[i]);
		int sz=siz[s[i]];
		if(i!=l-1) sz-=siz[s[i+1]];
		for(int t=0;t<=n;t++)
			g[c][t]=g[!c][t]*(i!=l-1);
		for(int t=n;t>=0;t--)
			pr[t]=(pr[t+1]+g[!c][t])%mod;
		for(int d=n;d>=0;d--)
			g[c][d]=(g[c][d]+pr[d])%mod;
		for(int j=n-1;j>=0;j--)
			for(int d=sz;d;d--)
				g[c][j+d]=(g[c][j+d]+1ll*g[c][j]*tmp[d]%mod*C(j+d,d))%mod;
	}
	write(g[l-1&1][k-1]);
	flush();
}
```
