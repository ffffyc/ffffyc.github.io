---
title: "题解：P14170 二分图最大匹配期望"
date: 2025-10-14
category: "题解"
summary: "Link 题意 有一个左右分别 n,m 个点的二分图，其中左部点 i 与右部点 j 之间有边的概率为 pi,j。求出该二分图的最大匹配的期望，对 998244353 取模。 T"
math: true
top: 2
source: https://www.luogu.com.cn/article/y9o69plb
slug: y9o69plb
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P14170)

## 题意
有一个左右分别 $n,m$ 个点的二分图，其中左部点 $i$ 与右部点 $j$ 之间有边的概率为 $p_{i,j}$。求出该二分图的最大匹配的期望，对 $998244353$ 取模。

$T\le 15$，$n,m\le 8$。
## 题解
默认左右两边各有 $n$ 个点，不足的用 $0$ 补齐即可。

考虑 Hall 定理，对于任意左部点集合 $S$，若存在 $|S|>|N(S)|$ 则不合法。**对于一个不合法的方案，我们选取一个代表元 $\bm S$ 以防止记重**，我们可以选取 $|S|-|N(S)|$ 最大的集合 $S$ 作为代表元，若存在多个满足条件的 $S$，选取其中 $|S|$ 最小的一个。可以使用反证法证明此时代表元唯一。

考虑设状态 $G(S,T)$ 表示考虑左部点集 $S$ 和右部点集 $T$ 之间的所有边，满足 $N(S)=T$ 且 $S$ 为该非法子图的代表元的概率。类似地，设 $F(S,T)$ 表示考虑 $S,T$ 之间的边，满足 $N(S)=T$ 且存在左部点的完美匹配的概率。容斥转移如下：
$$F(S,T)=P(S,T)-\sum_{\substack{S'\sube S,T'\sube T\\|S'|>|T'|}}G(S',T')\cdot F(S-S',T-T')\cdot E(S',T-T')$$
$$G(S,T)=P(S,T)-\sum_{\substack{S'\sube S,T'\sube T\\|S'|-|T'|\ge |S|-|T|\\(S,T)\ne (S',T')}}G(S',T')\cdot F(S-S',T-T')\cdot E(S',T-T')$$

其中 $P(S,T)$ 表示考虑 $S,T$ 的导出子图，$N(S)=T$ 的概率，$E(S,T)$ 表示 $S,T$ 间无边的概率。式子中乘上 $F(S-S',T-T')$ 的原因是，若该部分不合法，选取其中的代表元可以得到一个更优的代表元，反之则不可能得到更优的代表元。

接下来考虑算期望最大匹配，枚举原图的代表元 $S$（若存在）与对应的 $T=N(S)$。那么剩余的 $U-S$ 部分存在完美匹配，忽略 $U-S$ 到 $T$ 的边，枚举 $U-S$ 在 $U-T$ 中的邻点集合即可。

注意此时也有 $N(S)$ 到 $S$ 的完美匹配，否则其中存在相应的右侧的代表元，删去可以得到更优的左侧代表元。所以最大匹配数为 $n-|S|+|T|$。

时间复杂度 $O(9^n)$。

:::info[代码]
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
using IO::read;
using IO::write;
using IO::flush;
using IO::getc;
using IO::putc;
#define pii pair<int,int>
#define mpr make_pair
#define fir first
#define sec second
const int N=8+2,S=256+10,mod=998244353,iv100=828542813;
inline int add(int x,int y){ return x+y>=mod?x+y-mod:x+y; }
inline int dec(int x,int y){ return x>=y?x-y:x-y+mod; }
inline void inc(int &x,int y){ x=add(x,y); }
int n,m,u,p[N][N],pc[S],sp1[N][S],sp0[N][S],sd[S][S],np[S][S],f[S][S],g[S][S];
int main(){
//	freopen("dance4.in","r",stdin);
	int T=read();
	while(T--){
		n=read(),m=read();
		for(int i=0;i<n;i++)
			for(int j=0;j<m;j++)
				p[i][j]=1ll*read()*iv100%mod;
		n=max(n,m),u=1<<n;
		for(int i=0;i<n;i++){
			sp1[i][0]=sp0[i][0]=1;
			for(int s=1;s<u;s++){
				int lb=__lg(s&-s);
				sp1[i][s]=1ll*sp1[i][s^(1<<lb)]*p[i][lb]%mod;
				sp0[i][s]=1ll*sp0[i][s^(1<<lb)]*dec(1,p[i][lb])%mod;
			}
		}
		for(int s=1;s<u;s++)
			pc[s]=pc[s>>1]+(s&1);
		np[0][0]=1;
		for(int t=0;t<u;t++)
			sd[0][t]=1;
		for(int s=1;s<u;s++)
			for(int t=0;t<u;t++){
				int lb=__lg(s&-s);
				sd[s][t]=1ll*sd[s^(1<<lb)][t]*sp0[lb][t]%mod;
				np[s][t]=0;
				for(int tp=t;~tp;tp=tp?(tp-1&t):-1)
					inc(np[s][t],1ll*np[s^(1<<lb)][tp]*sd[s^(1<<lb)][t^tp]%mod*sp1[lb][t^tp]%mod);
			}
		f[0][0]=1;
		for(int s=1;s<u;s++)
			for(int t=0;t<u;t++){
				if(pc[s]<=pc[t]){
					f[s][t]=np[s][t];
					for(int sp=s;~sp;sp=sp?(sp-1&s):-1)
						for(int tp=t;~tp;tp=tp?(tp-1&t):-1){
							if(pc[sp]<=pc[tp]) continue;
							f[s][t]=dec(f[s][t],1ll*g[sp][tp]*sd[sp][t^tp]%mod*f[s^sp][t^tp]%mod);
						}
				}else{
					g[s][t]=np[s][t];
					for(int sp=s;~sp;sp=sp?(sp-1&s):-1)
						for(int tp=t;~tp;tp=tp?(tp-1&t):-1){
							if(s==sp&&t==tp) continue;
							if(pc[sp]-pc[tp]<pc[s]-pc[t]) continue;
							g[s][t]=dec(g[s][t],1ll*g[sp][tp]*sd[sp][t^tp]%mod*f[s^sp][t^tp]%mod);
						}
				}
			}
		int ans=1ll*n*f[u-1][u-1]%mod;
		for(int s=1;s<u;s++)
			for(int t=0;t<u;t++){
				if(pc[s]<=pc[t]) continue;
				int res=0;
				for(int ts=u-1^t,tp=ts;~tp;tp=tp?(tp-1&ts):-1)
					inc(res,1ll*f[u-1^s][tp]*sd[u-1^s][u-1^t^tp]%mod);
				res=1ll*res*g[s][t]%mod*sd[s][u-1^t]%mod;
				inc(ans,1ll*(n-pc[s]+pc[t])*res%mod);
			}
		write(ans),putc('\n');
		memset(p,0,sizeof(p));
	}
	flush();
}
```
:::
