---
title: "题解：P12152「蓬莱人形 Round 1」催眠术"
date: 2025-05-20
category: "题解"
summary: "Link 进阶计数套路考察。 题意 给定 n,m,k，还有一个长为 m 的值域在 [1,k] 中的整数序列 a，再给定一个大小为 n × (m+1) 的矩阵 c1 n,0 m。"
math: true
top: 2
source: https://www.luogu.com.cn/article/tsi0vlf1
slug: tsi0vlf1
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P12152)

进阶计数套路考察。
## 题意

给定 $n,m,k$，还有一个长为 $m$ 的值域在 $[1,k]$ 中的整数序列 $a$，再给定一个大小为 $n \times (m+1)$ 的矩阵 $c_{1\sim n,0\sim m}$。

定义一个整数序列是好的，当且仅当它的值域在 $[1,k]$ 中且所有值域在 $[1,k]$ 的长为 $m$ 的整数序列都是它的子序列。

定义一个好的整数序列 $b$ 的价值为 $\prod\limits_{i=1}^n c_{i,p_i}$，其中 $p_i$ 为 $a$ 的最长前缀长度使得 $a_{1 \sim p_i}$ 是 $b_{1\sim i}$ 的一个子序列，若不存在则 $p_i = 0$。

求所有长度为 $n$ 的好序列的价值和，答案对 $10^9+7$ 取模。

$n,m,k\le 400$。
## 思路

为避免变量重名，将用 $v$ 表示输入的 $k$。

题目强制我们一个个地向后填数，且要求所有长为 $m$ 的序列都出现过，即可以划分出 $m$ 段且每一段内所有 $[1,v]$ 的数均出现，这也可以告诉我们 $m\cdot v\le n$，否则无解。

若无需考虑匹配 $a_{1\sim m}$，则可以记状态 $f_{i,j,p}$ 表示填了 $i$ 个数，当前处于第 $j$ 段，该段内已填 $p$ 种数。由于需要匹配，则需要添加一维记录当前匹配的位置，且由于匹配过的数是确定的，需要分开记录匹配过的数与未匹配过的数。设 $f_{i,j,k,p,q}$ 表示填了 $i$ 个数，目前匹配到位置 $j$，已经填完了 $k$ 段，当前段中已经填入了 $p$ 种匹配过的数，$q$ 种未匹配的数。由于 $j,k\le m$ 且 $p,q\le v$，状态是可接受的。

但是我们需要要求相邻两个匹配的位置间不能出现于右侧匹配位置相同的数，这需要得知上一次匹配时有多少种未匹配的数，但我们不能在状态上再填一维。

不妨称**一次转移**为以下两种之一：
- 在一段中相邻两个匹配位置之间进行转移；
- 在一段中最后一个匹配位置至段末之间进行转移。

一次转移的特点为转移不相交且转移的终止位置需要起始位置的信息，**不妨新开状态表示当前处于一次一类/二类转移，并在开启一次转移的时候提前将贡献乘入**。

知道了这些后转移方程并不难推出，但存在相当一部分的细节需要思考。

时间复杂度 $O(n^3)$，可以通过。

类似题目推荐：[P9385 [THUPC 2023 决赛] 阴阳阵](https://www.luogu.com.cn/problem/P9385)。

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
const int N=400+10,M=800+10,mod=1e9+7;
inline int add(int x,int y){ return x+y>=mod?x+y-mod:x+y; }
inline int dec(int x,int y){ return x>=y?x-y:x-y+mod; }
inline void inc(int &x,int y){ x=add(x,y); }
int n,m,v,a[N],w[N][N],sp[N],pr[N][N],ip[N][N],fac[N],ifac[N],pw[N];
int f[2][M][M],g[2][M][M][2],h[2][M][N],t[2][M];
inline int qpow(int x,int y){
	int res=1;
	while(y){
		if(y&1) res=1ll*res*x%mod;
		x=1ll*x*x%mod;
		y>>=1;
	}
	return res;
}
inline void Prefix(int n){
	fac[0]=pw[0]=1;
	for(int i=1;i<=n;i++)
		fac[i]=1ll*fac[i-1]*i%mod,
		pw[i]=1ll*pw[i-1]*v%mod;
	ifac[n]=qpow(fac[n],mod-2);
	for(int i=n;i;i--)
		ifac[i-1]=1ll*ifac[i]*i%mod;
}
/*
f[i][j/p][k/q]:填到位置 i, 已匹配到位置 j, 已匹配 k 段, 在当前段中有 p/q 个已出现的匹配/未匹配数
g[i][j/p][k/q][0/1]:处于第一种转移, 要求匹配 a_j 并已为其钦定一个值, 是否有一个要求某数不能出现的限制 
h[i][j/p][k]:处于第二种转移, 要求结束该段, 在当前段内有 p 个已出现的数 
t[i][j/p]:已匹配整个 a_{1\sim m}, 目前已匹配 k 段, 在当前段内有 p 个已出现的数
*/
inline int pos(int i,int j){ return i*(v+1)+j; }
inline pii pos(int i){ return mpr(i/(v+1),i%(v+1)); }
inline bool chk(int i,int v,int k){ return ip[i][v]<=k; }
int main(){
	n=read(),m=read(),v=read();
	if(m*v>n) return puts("0"),0;
	for(int i=1;i<=m;i++)
		a[i]=read();
	for(int i=1;i<=n;i++)
		for(int j=0;j<=m;j++)
			w[i][j]=read();
	Prefix(n); 
	sp[n+1]=1;
	for(int i=n;i;i--)
		sp[i]=1ll*sp[i+1]*w[i][m]%mod;
	for(int j=1;j<=v;j++)
		ip[0][j]=v+1;
	for(int i=1;i<=n;i++){
		pr[i][1]=a[i];
		for(int j=1,p=1;j<=v;j++)
			if(pr[i-1][j]!=a[i])
				pr[i][++p]=pr[i-1][j];
		for(int j=1;j<=v;j++)
			ip[i][j]=v+1;
		for(int j=1;j<=v;j++)
			if(pr[i][j])
				ip[i][pr[i][j]]=j;
	}
	int ans=0,c=0,u=pos(m,v);
	f[0][pos(0,0)][pos(0,0)]=1;
	for(int i=1;i<=n;i++,c^=1){
		for(int A=0;A<=u;A++)
			for(int B=0;B<=u;B++){
				int j=pos(A).fir,k=pos(B).fir,p=pos(A).sec,q=pos(B).sec,wc;
				wc=f[c][A][B];
				if(wc){
					//f->g
					if(chk(j,a[j+1],p)) inc(g[c][pos(j,p)][pos(k,q)][1],wc);
					else{
						if(q) inc(g[c][pos(j,p+1)][pos(k,q-1)][1],1ll*wc*q%mod);
						inc(g[c][pos(j,p+1)][pos(k,q)][0],wc);
					}
					//f->h 要给一段内非匹配的数定顺序 
					if(chk(j,a[j+1],p)) inc(h[c][pos(j,p+q)][k],1ll*wc*fac[v-p]%mod);
					else inc(h[c][pos(j,p+q)][k],1ll*wc*q%mod*fac[v-p-1]%mod);
					f[c][A][B]=0;
				}
				for(int a=0;a<=1;a++){
					wc=g[c][A][B][a];
					if(wc){
						//g->g 要求在预留的是已出现过的数时不能触及 p+q=k 
						if(p+q+1+a<=v) inc(g[!c][pos(j,p)][pos(k,q+1)][a],1ll*wc*w[i][j]%mod);
						inc(g[!c][pos(j,p)][pos(k,q)][a],1ll*wc*w[i][j]%mod*(p+q-1)%mod);
						//g->f 若结束一段则需要给一段内非匹配的数定顺序 
						if(j+1<m){
							if(p+q<v) inc(f[!c][pos(j+1,p)][pos(k,q)],1ll*wc*w[i][j+1]%mod);
							else inc(f[!c][pos(j+1,0)][pos(k+1,0)],1ll*wc*w[i][j+1]%mod*fac[q]%mod);
						}else{
							//g->t 需要给这一段的非匹配数定顺序 
							if(p+q<v) inc(t[!c][pos(k,p+q)],1ll*wc*w[i][j+1]%mod*fac[v-p]%mod);
							else inc(t[!c][pos(k+1,0)],1ll*wc*w[i][j+1]%mod*fac[v-p]%mod*fac[k+1==m?0:v]%mod);
						}
						g[c][A][B][a]=0; 
					}
				}
			}
		for(int A=0;A<=u;A++)
			for(int k=0;k<=m;k++){
				int j=pos(A).fir,p=pos(A).sec,wc;
				wc=h[c][A][k];
				if(wc){
					//h->h
					if(p+1<v) inc(h[!c][pos(j,p+1)][k],1ll*wc*w[i][j]%mod);
					inc(h[!c][pos(j,p)][k],1ll*wc*w[i][j]%mod*(p-1)%mod);
					//h->f
					if(p+1==v) inc(f[!c][pos(j,0)][pos(k+1,0)],1ll*wc*w[i][j]%mod);
					h[c][A][k]=0;
				}
			}
		for(int A=0;A<=u;A++){
			int k=pos(A).fir,p=pos(A).sec,wc;
			wc=t[c][A];
			if(wc){
				if(k==m) inc(ans,1ll*wc*sp[i]%mod*pw[n-i+1]%mod);
				else{
					//t->t
					if(p+1<v) inc(t[!c][pos(k,p+1)],1ll*wc*w[i][m]%mod);
					if(p+1==v) inc(t[!c][pos(k+1,0)],1ll*wc*w[i][m]%mod*fac[k+1==m?0:v]%mod);
					inc(t[!c][pos(k,p)],1ll*wc*w[i][m]%mod*p%mod);
				}
				t[c][A]=0;
			}
		}
	}
	inc(ans,t[c][pos(m,0)]);
	write(ans);
	flush();
}
```
