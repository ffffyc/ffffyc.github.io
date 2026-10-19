---
title: "题解 P5809【【模板】多项式复合逆】"
date: 2024-03-21
category: "题解"
summary: "Link 力求把最新技术翻译地人人都能看懂。 推荐先学习：拉格朗日反演。 题意 给出 n 次多项式 F(x)，求一个 n 次多项式 G(x) 满足 F(G(x)) x xn+1"
math: true
top: 2
source: https://www.luogu.com.cn/article/t2cijmdo
slug: t2cijmdo
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P5809)

力求把最新技术翻译地人人都能看懂。

推荐先学习：[拉格朗日反演](https://www.luogu.com.cn/article/tbr4td9e)。
## 题意
给出 $n$ 次多项式 $F(x)$，求一个 $n$ 次多项式 $G(x)$ 满足 $F(G(x))\equiv x\pmod {x^{n+1}}$。保证 $[x^0]F(x)=0$ 且 $[x^1]F(x)\ne 0$。

$n\le 2\times 10^4$。
## 思路
我们将 $[x^1]F(x)$ 化成 $1$ 以便后续处理。令 $F'(x)$ 为原多项式，$v$ 为 $[x^1]F'(x)$，$F(x)$ 为 $\dfrac{F'(x)}{v}$。

那么我们有：$F(G(x))=\dfrac{x}{v}$，$F^k(G(x))=\dfrac{x^k}{v^k}$，根据扩展拉格朗日反演，我们有：

$$[x^n]F^k(x)=\frac1{n}\cdot[x^{n-1}]\frac{kx^{k-1}}{v^k}\cdot\frac{x^n}{G^n(x)}$$

$$[x^n]F^k(x)=\frac k {nv^k}\cdot[x^{n-k}]\frac{x^n}{G^n(x)}$$
$$\sum_kx^{n-k}\frac{nv^k}k[x^n]F^k(x)=\left(\frac{G(x)}x\right)^{-n}$$

$$G(x)=x\left(\sum_kx^{n-k}\frac{nv^k}{k}[x^n]F^k(x)\right)^{-1/n}$$

$$G(x)=\frac{x}v\left(\sum_kx^{n-k}\frac{n}{kv^{n-k}}[x^n]F^k(x)\right)^{-1/n}$$

可以发现此处需要开根的多项式常数项为 $1$，直接用多项式快速幂即可。于是接下来我们的任务就是对 $\forall k\in[0,n]$ 求出 $[x^n]F^k(x)$。不难发现，这等价于求多项式 $[x^n]\dfrac{1}{1-yF(x)}$。

首先我们需要了解 Bostan-Mori 算法，该算法可在 $O(k\log k\log n)$ 的复杂度下对 $O(k)$ 次的多项式 $F(x),G(x)$ 求出 $[x^n]\dfrac{F(x)}{G(x)}$。具体地，
$$[x^n]\dfrac{F(x)}{G(x)}=[x^n]\dfrac{F(x)G(-x)}{G(x)G(-x)}=[x^n]\dfrac{F_0(x^2)}{G_0(x^2)}+x\dfrac{F_1(x^2)}{G_0(x^2)}$$

两边分别只有偶数次和奇数次有值，根据 $n$ 的奇偶性取一边递归即可。当 $n=0$ 时直接返回 $\dfrac{[x^0]F(x)}{[x^0]G(x)}$ 即可。

二元多项式的情况也是一样的：
$$[x^n]\dfrac{F(x,y)}{G(x,y)}=[x^n]\dfrac{F(x,y)G(-x,y)}{G(x,y)G(-x,y)}=[x^n]\dfrac{F_0(x^2,y)}{G_0(x^2,y)}+x\dfrac{F_1(x^2,y)}{G_0(x^2,y)}$$

注意到递归到第 $t$ 层时 $x$ 只需要保留 $\lfloor\dfrac{n}{2^t}\rfloor$ 次，而 $y$ 每层次数只会翻倍，只有 $2^{t+1}$ 次，所以整个二元多项式只有 $O(n)$ 项。

于是我们在 $O(n\log^2n)$ 的时间复杂度内解决了多项式复合逆问题。

核心代码：
```cpp
namespace PolyC{
	//...
	#define PolyY vector<Poly>
	inline PolyY operator*(const PolyY &a,const PolyY &b){
		int n=a.size(),m=b.size(),p=a[0].size(),q=b[0].size();
		Poly P,Q;
		P.resize(n*(p+q-1)),Q.resize(m*(p+q-1));
		for(int i=0;i<n;i++)
			for(int j=0;j<p;j++)
				P[i*(p+q-1)+j]=a[i][j];
		for(int i=0;i<m;i++)
			for(int j=0;j<q;j++)
				Q[i*(p+q-1)+j]=b[i][j];
		P=P*Q;
		PolyY F(n+m-1,Poly(p+q-1,0)); 
		for(int i=0;i<n+m-1;i++)
			for(int j=0;j<p+q-1;j++)
				F[i][j]=P[i*(p+q-1)+j]; 
		return F;
	}
}
using namespace PolyC;
inline Poly BostanMori(int n,PolyY F,PolyY G){
	if(!n) return F[0]*Inv(G[0]);
	if(n+1<F.size()) F.resize(n+1);
	if(n+1<G.size()) G.resize(n+1);
	PolyY H=G;
	for(int i=1;i<H.size();i+=2)
		for(int j=0;j<H[i].size();j++)
			H[i][j]=dec(0,H[i][j]);
	F=F*H,G=G*H;
	PolyY A,B;
	for(int i=n&1;i<F.size();i+=2) A.push_back(F[i]);
	for(int i=0;i<G.size();i+=2) B.push_back(G[i]);
	return BostanMori(n/2,A,B);
}
inline Poly CompInv(Poly F){
	int n=F.size();
	int t=F[1],v=qpow(t,mod-2);
	for(int i=0;i<n;i++)
		F[i]=1ll*F[i]*v%mod;
	PolyY P,Q;
	for(int i=0;i<n;i++)
		P.push_back({!i,0}),
		Q.push_back({!i,dec(0,F[i])});
	Poly G=BostanMori(n-1,P,Q),H(n,0); 
	G.resize(n);
	for(int i=0;i<n;i++)
		H[n-1-i]=1ll*G[i]*(n-1)%mod*inv[i]%mod;
	for(int i=0,w=1;i<n;i++,w=1ll*w*v%mod)
		H[i]=1ll*H[i]*w%mod;
	H=Pow(H,mod-inv[n-1]);
	H.insert(H.begin(),0),H.resize(n);
	for(int i=0;i<n;i++)
		H[i]=1ll*H[i]*v%mod;
	return H;
}
```
