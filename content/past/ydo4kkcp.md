---
title: "题解：AT_xmascon20_d Determinant"
date: 2025-04-29
category: "题解"
summary: "Link 低！秩！矩！阵！分！解！ 题意 给定整数 n,c，求解 n× n 的矩阵 Ai,j 的行列式： Ai,j=cases1,&i=j\\\\0,&i j j i=0,&oth"
math: true
top: 2
source: https://www.luogu.com.cn/article/ydo4kkcp
slug: ydo4kkcp
---

[$\text{Link}$](https://www.luogu.com.cn/problem/AT_xmascon20_d)

低！秩！矩！阵！分！解！
## 题意
给定整数 $n,c$，求解 $n\times n$ 的矩阵 $A_{i,j}$ 的行列式：
$$A_{i,j}=\begin{cases}1,&i=j\\0,&i\ne j\land j\bmod i=0\c,&\text{otherwise}\end{cases}$$ 

对 $998244353$ 取模。

$n\le 10^9$。
## 思路
注意到 $A_{i,j}$ 里面不等于 $c$ 的位置很少，不妨令 $A=B+C$，其中 $C$ 表示一个 $n\times n$ 的全 $c$ 矩阵，
$$B_{i,j}=\begin{cases}1-c,&i=j\\-c,&i\ne j\land j\bmod i=0\\0,&\text{otherwise}\end{cases}$$ 

容易发现，$B_{i,j}$ 是一个上三角矩阵，而 $C_{i,j}$ 的秩为一。

对于求解 $\det(A+B)$ 的问题，其中 $\text{rank}(A)$ 为常数，考虑使用低秩矩阵分解。根据行列式的定义式有：
- 选取一个集合 $S\sube\{1,2,\dots,n\}$；
- $\forall i\in S$，将 $B_{i,j}$ 替换为 $A_{i,j}$；
- $\det(A+B)$ 的值等于所有子集 $S$ 得到的矩阵 $B'_{i,j}$ 的行列式之和；
- 根据行列式基本性质，只有在 $|S|\le \text{rank}(A)$ 时才有可能做出贡献。

本题中 $\text{rank}(C)=1$，于是考虑计算将 $B_{i,j}$ 中至多一行替换为全 $C$ 的行列式。写出行列式的定义式：

$$\det(B)=\sum_{p_{1\sim n}}(-1)^{\text{inv}(p)}\prod_{i=1}^nB_{i,p_i}$$

由于 $B_{i,j}$ 是上三角矩阵，在没有替换时必有 $p_i=i$。如果替换了第 $k$ 行，那么在 $p_{1\sim n}$ 上就会形成一个环，其中环上除了 $k$ 的每个结点的编号都是下一个结点的因数。

考虑计算贡献，令 $f(i)$ 表示替换第 $i$ 行的贡献，则有：

$$f(n)=\dfrac{c}{1-c}(1+\sum_{d|n,d\ne n}f(d))$$

$$f(n)=c+c\sum_{d|n}f(d)$$

需要求解 $f(n)$ 的前缀和，令 $g(n)=[n=1]-c$，则 $(f\times g)(i)=c$，于是可以模仿杜教筛进行求解。由于 $f(n)$ 并不是积性函数，小的部分只能线性对数计算，故需要调整分治界做到最优复杂度。

注意特判 $c=1$，在 $n\le 2$ 时答案为 $1$。

时间复杂度 $O(n^{2/3}\log^{1/3} n)$。

```cpp
int n,c,ic,f[N],fs[N];
unordered_map<int,int>mp;
inline void Prefix(int n){
	for(int i=1;i<=n;i++){
		f[i]=1ll*c*ic%mod*add(f[i],1)%mod;
		fs[i]=add(fs[i-1],f[i]);
		for(int j=i+i;j<=n;j+=i)
			inc(f[j],f[i]);
	}
}
inline int solve(int n){
	if(n<=N-10) return fs[n];
	if(mp.count(n)) return mp[n];
	int s=1ll*c*n%mod;
	for(int l=2,r;l<=n;l=r+1)
		r=n/(n/l),inc(s,1ll*c*(r-l+1)%mod*solve(n/l)%mod);
	return mp[n]=1ll*s*ic%mod;
}
int main(){
	n=read(),c=read(),ic=qpow(dec(1,c),mod-2);
	Prefix(min(n,N-10));
	if(c==1) return puts(n<=2?"1":"0"),0;
	write(1ll*qpow(dec(1,c),n)*(solve(n)+1)%mod);
	flush();
}
```
