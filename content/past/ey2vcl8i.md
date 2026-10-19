---
title: "题解：P10717「KDOI-05」简单的树上问题"
date: 2024-07-14
category: "题解"
summary: "Link 题意 给你一颗 n 个结点的树，有 k 次操作，第 i 次操作： 每个点初始都处于未激活状态； 以 pi,j 的概率激活点 j； 对于每个未激活的点 i，如果存在激活"
math: true
top: 2
source: https://www.luogu.com.cn/article/ey2vcl8i
slug: ey2vcl8i
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10717)
## 题意
给你一颗 $n$ 个结点的树，有 $k$ 次操作，第 $i$ 次操作：
- 每个点初始都处于未激活状态；
- 以 $p_{i,j}$ 的概率激活点 $j$；
- 对于每个未激活的点 $i$，如果存在激活的结点 $j,k$ 且 $i$ 在 $j$ 到 $k$ 的路径上，则 $i$ 也会被激活。

给出 $v_{i,s}$ 表示当 $i$ 在 $s$ 这些操作被激活时的权值。对于某种可能的情况，记 $S_i$ 为结点 $i$ 在哪些操作中被激活了，整棵树的权值为 $\prod_{i=1}^nv_{i,S_i}$。请求出这棵树的权值的期望。

$n\le 100$，$k\le 8$。
## 思路

考虑 $k=1$，这和[上一场梦熊周赛的 C](https://www.luogu.com.cn/problem/P10674) 完全一致，令 $f_{u,0/1/2}$ 分别表示「$u$ 子树内没有结点被激活」/「$u$ 子树内有结点被激活且钦定子树外没有结点被激活」/「$u$ 子树内有结点被激活且钦定子树外有结点被激活」时 $u$ 子树内的期望权值。

和该题一样，我们在合并子树的过程中需要将仅有一个子树内有结点被激活与有大于等于两个子树内有结点被激活分开讨论。不妨为后者新建一个状态 $3$，注意到状态 $3$ 由若干 $0/2$ 状态合并而来，此时子树外是否有结点被激活均可。令 $t_{0/1/2/3}$ 分别表示已经合并的子树的信息，转移如下，其中 $(a,b)\to c$ 表示 $t_a\times f_{v,b}\to t_c'$：

- $(0,0)\to 0$；
- $(0,1),(1,0)\to1$；
- $(0,2),(2,0)\to2$；
- $(2,2),(3,0/2)\to3$；

我们再考虑 $u$ 是否在初始时被激活，其中 $(a,b)\to c$ 表示 $a$ 状态在结点 $u$ 的初始激活状态为 $b$ 时转移到 $c$ 状态，将概率乘进去即可：
- $(0/1/2/3,0)\to 0/1/2/3$；
- $(0/2/3,1)\to 3$；

将 $0/1$ 状态乘上 $v_{u,0}$，$2/3$ 状态乘上 $v_{u,1}$，再将 $3$ 状态分别加给 $1/2$ 状态，$u$ 结点就计算完毕了。
****
考虑 $k$ 更大的情况。注意到直接给定了 $2^k$ 种情况的权值，提示我们将 $k$ 次操作一同考虑。

将 $k$ 次操作中 $u$ 的状态压缩，状态改写为 $f_{u,S}$，表示 $u$ 子树 $k$ 次操作下状态分别为 $S$ 时的期望权值，其中 $S\in \{0,1,2\}^k$，$t_{T},T\in\{0,1,2,3\}^k$ 同理。

于是我们可以得到一个非常暴力的做法：

- 加入一个子树，枚举 $k$ 次操作的转移，转移共有 $8$ 种，复杂度为 $O(8^k)$；
- 决定 $u$ 的初始激活状态，直接枚举 $u$ 初始激活的操作集合，复杂度为 $O(8^k)$；
- 将 $3$ 状态传至 $1/2$ 状态，直接枚举每个 $3$ 传给 $1$ 还是 $2$，复杂度为 $O(8^k)$。

总复杂度 $O(n8^k)$，无法通过。

不妨从看起来比较好下手的第三部分开始优化，我们注意到**这是一个类似高维后缀和的操作，我们可以类似地逐位下传**，复杂度降至 $O(k4^k)$。第二部分也可通过类似的思路逐位加入 $u$ 的初始激活信息做到 $O(k4^k)$。

接下来就是最为困难的第一部分了，我们依旧尝试用类似的思路解决。注意到 $0/2/3$ 状态的和是好求的，因为这些状态不会向外转移。由此我们考虑 **$3$ 状态的信息可由 $0/2/3$ 减去 $0/2$ 得到**。我们转移前使用高维前缀和将每一维为 $0/2$ 的状态加给 $3$ 状态，只考虑 $0/1/2$ 的 $5$ 种转移和 $(3,3)\to 3$ 共 $6$ 种转移，转移完我们便得到了 $0,1,2$ 状态的真实值和 $0/2/3$ 状态的和，将后者减去 $0,2$ 状态的值便可得到 $3$ 状态的真实值。单次高维前缀和/差分为 $O(k4^k)$，单次转移为 $O(6^k)$。

至此，我们将总复杂度优化至 $O(n6^k+nk4^k)$，可以通过。

可配合代码理解：

```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
const int N=100+10,K=10,S=256+10,U=65536+10,T=1679616+10,mod=998244353;
inline int add(int x,int y){ return x+y>=mod?x+y-mod:x+y; }
inline void inc(int &x,int y){ x=add(x,y); }
inline void dec(int &x,int y){ x=add(x,mod-y); }
int n,k,u1,u2,u3,p[N][K],v[N][S],dp[N][U],tmp[U],tmq[U];
vector<int>a[N];
struct node{
	int a,b,c;
}stk[T];
inline void dfs(int d,int a,int b,int c){//预处理 6^k 种转移
	if(d==k){
		stk[u3++]={a,b,c};
		return ;
	}
	dfs(d+1,a|(0<<d*2),b|(0<<d*2),c|(0<<d*2));
	dfs(d+1,a|(0<<d*2),b|(1<<d*2),c|(1<<d*2));
	dfs(d+1,a|(1<<d*2),b|(0<<d*2),c|(1<<d*2));
	dfs(d+1,a|(0<<d*2),b|(2<<d*2),c|(2<<d*2));
	dfs(d+1,a|(2<<d*2),b|(0<<d*2),c|(2<<d*2));
	dfs(d+1,a|(3<<d*2),b|(3<<d*2),c|(3<<d*2));
}
inline void PFS(int *a){//将 0/2 加给 3 状态的高维前缀和
	for(int i=0;i<k;i++)
		for(int j=0;j<u2;j++){
			int c=j>>i*2&3;
			if(c==0||c==2) inc(a[j|(3<<i*2)],a[j]);
		}
}
inline void PFD(int *a){//将 0/2 从 3 状态中删去的高维前缀差分
	for(int i=0;i<k;i++)
		for(int j=0;j<u2;j++){
			int c=j>>i*2&3;
			if(c==0||c==2) dec(a[j|(3<<i*2)],a[j]);
		}
}
inline void dfs(int x,int fa){
	for(auto t:a[x]){
		if(t==fa) continue;
		dfs(t,x);
	}
	tmp[0]=1;
	PFS(tmp);
	for(auto t:a[x]){
		if(t==fa) continue;
		PFS(dp[t]);
		for(int i=0;i<u3;i++)
			inc(tmq[stk[i].c],1ll*tmp[stk[i].a]*1ll*dp[t][stk[i].b]%mod);
		for(int i=0;i<u2;i++)
			tmp[i]=tmq[i],tmq[i]=0;
	}
	PFD(tmp);
	for(int i=0;i<k;i++)//第二部分
		for(int j=u2-1;j>=0;j--){
			int c=j>>(i*2)&3;
			if(c==0||c==2) inc(tmp[j|(3<<i*2)],1ll*tmp[j]*p[x][i]%mod);
			if(c==0||c==1||c==2) tmp[j]=1ll*tmp[j]*(1-p[x][i]+mod)%mod;
		}
	for(int i=0;i<u2;i++){
		int t=0;
		for(int j=0;j<k;j++){
			int c=i>>(j*2)&3;
			if(c==2||c==3) t|=1<<j;
		}
		tmp[i]=1ll*tmp[i]*v[x][t]%mod;
	}
	for(int i=0;i<k;i++)//第三部分
		for(int j=0;j<u2;j++){
			int c=j>>(i*2)&3;
			if(c==1||c==2) inc(tmp[j],tmp[j|(3<<i*2)]);
			if(c==3) tmp[j]=0;
		}
	for(int i=0;i<u2;i++)
		dp[x][i]=tmp[i],tmp[i]=0;
}
int main(){
	n=read(),k=read();
	for(int i=1;i<n;i++){
		int u=read(),v=read();
		a[u].push_back(v),a[v].push_back(u);
	}
	for(int i=0;i<k;i++)
		for(int j=1;j<=n;j++)
			p[j][i]=read();
	u1=1<<k,u2=1<<k*2;
	for(int i=1;i<=n;i++)
		for(int j=0;j<u1;j++)
			v[i][j]=read();
	dfs(0,0,0,0);
	dfs(1,1);
	int s=0;
	for(int i=0;i<u2;i++){
		bool fl=0;
		for(int j=0;j<k;j++){
			int c=i>>(j*2)&3;
			if(c==2||c==3) fl=1;
		}
		if(!fl) inc(s,dp[1][i]);
	}
	write(s);
	flush();
}
```
