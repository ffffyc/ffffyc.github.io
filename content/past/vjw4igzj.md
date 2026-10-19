---
title: "题解：P10881「KDOI-07」能量场"
date: 2024-07-30
category: "题解"
summary: "Link 题意 给你一个长为 n 的序列 a1 n，定义一条边 (u,v) 的权值为 au+av。对于一张图，定义其权值为包含的所有边的权值乘积。求所有 n 个点的有标号基环树"
math: true
top: 2
source: https://www.luogu.com.cn/article/vjw4igzj
slug: vjw4igzj
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10881)

## 题意

给你一个长为 $n$ 的序列 $a_{1\dots n}$，定义一条边 $(u,v)$ 的权值为 $a_u+a_v$。对于一张图，定义其权值为包含的所有边的权值乘积。求所有 $n$ 个点的有标号基环树的权值之和。对 $998244353$ 取模。

$n\le 10^3$。

## 思路
非常厉害的题，zky 倾情提供 solution。只讲述对正解有意义的几个 sub。

### $n\le 18$

考虑基环树把环缩起来就是一颗树，而树的权值乘积很自然就能想到矩阵树定理，我们不妨枚举哪些点在环上，我们可以 DP 求出这些点构成的环的权值和，然后将这些点缩起来（边权、度数相加）做一次矩阵树定理，为了方便我们可以将代表这个环的点删去。

时间复杂度 $O(2^nn^3)$，期望得分 $25$。

### $n\le 20$

我们不妨研究一下我们需要求行列式的矩阵的性质。我们需要求 $\det(D-A)$，其中 $D$ 只有对角线位置有值且 $D_{i,i}=na_i+\sum_{j=1}^na_j$，$A_{i,j}=a_i+a_j$，不妨设 $d_i=D_{i,i}$。

由行列式的基本性质，我们可以将求 $\det(D-A)$ 看成选取一个行的集合 $S$，将矩阵 $D$ 在集合内的行替换为 $-A$ 对应的行，对于所有 $S$ 求替换后的矩阵的行列式之和。

观察出矩阵 $A$ 的一个重要性质：$A$ 中任意三行线性相关。于是我们只需要考虑大小不超过 $2$ 的 $S$。

根据行列式的定义式，我们可以简单地将行列式求出：
- $|S|=0$，$\prod_{i=1}^nd_i$；
- $|S|=1$，$-2\sum_{i=1}^na_i\prod_{j\ne i}d_j$；
- $|S|=2$，$\sum_{i=1}^n\sum_{j=i+1}^n(2a_ia_j-a_i^2-a_j^2)\prod_{k\ne i,k\ne j}d_k$。

需要注意 $d_i$ 在模意义下等于 $0$ 的情况。

时间复杂度 $O(2^nn^2)$，期望得分 $30$。

### $n\le 200$

我们尝试进一步对特殊的边权进行处理。

对于环上的部分，我们需要给定点集对于每一种可能的环求出边权的乘积之和，注意到边权是 $a_i+a_j$ 的形式，而环上的点度数又恰为 $2$，所以每个点对答案的贡献只可能是 $a_i^0,a_i^1,a_i^2$ 之一！

注意到点的编号对环没有影响，我们只需要考虑环上分别有有 $i,j,k$ 个点对答案的贡献次幂为 $0,1,2$ 时可以形成多少个环即可。不妨将边权为 $a_u+a_v$ 看成给 $(u,v)$ 这条边定向，将指向的那个点的权值乘入答案，每个点对答案的贡献次幂即为它的入度。对于上述问题，

- 首先有 $j+2k=i+j+k$ 即 $i=k$；
- 先将入度为 $0,2$ 的点放在环上，显然只能交替放，分配方案的编号为 $i!(i-1)!$，注意环可以翻转，方案数要除以二；
- 再将入度为 $1$ 的点依次插入环中，由于这些点入度出度都为 $1$，可以任意插入两个点之间，方案数为 $\dfrac{(2i+j-1)!}{(2i-1)!}$。

即 $i$ 个 $0,2$ 度点、$j$ 个 $1$ 度点构成环的方案数为 $\dfrac{i!(i-1)!(2i+j-1)!}{2(2i-1)!}$，特判 $i=0$ 时方案数为 $(j-1)!$。

于是我们依次将每个点划分给环内/环外，进行一个 DP，设 $f_{i,a,b,c,p,q}$ 表示考虑前 $i$ 个点，划分给环内的点分别有 $a,b,c$ 个贡献了 $0,1,2$ 次幂，环外钦定的 $S$ 内的点分别为 $p,q$ 时的答案和，转移 $i$ 时枚举 $i$ 划分给哪一部分并算入对应贡献即可。而 $p,q$ 这两维也可以在转移到时并入计算，于是我们得到了一个状态为四维，转移 $O(1)$ 的做法。

时间复杂度 $O(n^4)$，期望得分 $90$。

### $n\le 1000$

回想一下，$d_i=na_i+\sum_{j}a_j$，再回看上述式子，我们发现环外的部分对答案的贡献同样是 $a_i$ 的 $0,1,2$ 次幂之一！

再考虑求出全局中 $0,1,2$ 次幂分别有 $i,j,k$ 个时对答案的贡献系数。不妨考虑先枚举一个环，环上 $0,1,2$ 次幂分别有 $i,j,i$ 个，再枚举环外的 $|S|$ 和有几个 $d_p$ 选择了其中的 $na_p$，分配标号并乘上一些 $n$ 和 $\sum a$ 即可。

再 DP 求出 $0,1,2$ 次幂分别有 $i,j,k$ 个时的和，注意到 $i+j+k=n$，我们可以省去一维，于是状态变为三维。

时间复杂度 $O(n^3)$，可以通过。

参考代码：
```cpp
int n,sv,v[N],fac[N],ifac[N],inv[N],pw0[N],pw1[N],C[N][N],g[N][N];
int f[N][N][2];
inline void Prefix(int n){
	fac[0]=1;
	for(int i=1;i<=n;i++)
		fac[i]=1ll*i*fac[i-1]%mod;
	ifac[n]=qpow(fac[n],mod-2);
	for(int i=n;i;i--)
		ifac[i-1]=1ll*i*ifac[i]%mod;
	for(int i=1;i<=n;i++)
		inv[i]=1ll*ifac[i]*fac[i-1]%mod;
	pw0[0]=pw1[0]=1;
	for(int i=1;i<=n;i++)
		pw0[i]=1ll*pw0[i-1]*n%mod,
		pw1[i]=1ll*pw1[i-1]*sv%mod;
}
int main(){
	n=read();
	for(int i=1;i<=n;i++)
		v[i]=read(),inc(sv,v[i]);
	Prefix(n);
	int in=qpow(n,mod-2);
	for(int i=0;i<=n;i++){
		C[i][0]=1;
		for(int j=1;j<=n;j++)
			C[i][j]=add(C[i-1][j-1],C[i-1][j]);
	}
	for(int i=0;i<=n;i++)
		for(int j=0;i+i+j<=n;j++){
			if(i+j+i<=2) continue;
			int v;
			if(!i) v=fac[j-1];
			else v=1ll*fac[i]*fac[i-1]%mod*fac[i+i+j-1]%mod*ifac[i+i-1]%mod*ifac[2]%mod;
			for(int l=0,p=n-i-i-j-l,tv=1ll*v*pw0[p]%mod;p>=0;l++,p--,tv=1ll*tv*sv%mod*in%mod)
				inc(g[i+l][j+p],1ll*tv*C[i+l][i]%mod*C[j+p][p]%mod);
			for(int l=0,p=n-i-i-j-1-l,tv=1ll*v*pw0[p]%mod;p>=0;l++,p--,tv=1ll*tv*sv%mod*in%mod)
				dec(g[i+l][j+p+1],2ll*tv*C[i+l][i]%mod*C[j+p][p]%mod*(j+p+1)%mod);
			for(int l=0,p=n-i-i-j-2-l,tv=1ll*v*pw0[p]%mod;p>=0;l++,p--,tv=1ll*tv*sv%mod*in%mod)
				dec(g[i+l+1][j+p],1ll*tv*C[i+l][i]%mod*C[j+p][p]%mod*(i+l+1)%mod*(i+1)%mod),
				inc(g[i+l][j+p+2],1ll*tv*C[i+l][i]%mod*C[j+p][p]%mod*(j+p+2)%mod*(j+p+1)%mod);
		}
	int r=1;
	f[0][0][0]=1;
	for(int i=0;i<n;i++,r^=1)
		for(int a=0;a<=i;a++)
			for(int b=0;a+b<=i;b++){
				if(!f[a][b][r^1]) continue;
				int t=f[a][b][r^1],x=v[i+1];
				int tx=1ll*t*x%mod,tx2=1ll*tx*x%mod;
				inc(f[a+1][b][r],t);
				inc(f[a][b+1][r],tx);
				inc(f[a][b][r],tx2);
				f[a][b][r^1]=0;
			} 
	r^=1;
	int ans=0;
	for(int a=0;a<=n;a++)
		for(int b=0;a+b<=n;b++)
			inc(ans,1ll*f[a][b][r]*g[a][b]%mod);
	write(ans);
	flush();
}
```
