---
title: "题解 P10249【【模板】多项式复合函数】"
date: 2024-03-21
category: "题解"
summary: "Link 力求把最新技术翻译地人人都能看懂。 推荐先学习：多项式复合逆、转置原理。 题意 给出两个 n 次多项式 F(x),G(x)，求出 H(x) F(G(x))( xn+1"
math: true
top: 2
source: https://www.luogu.com.cn/article/qn0xklxe
slug: qn0xklxe
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10249)

力求把最新技术翻译地人人都能看懂。

推荐先学习：[多项式复合逆](https://www.luogu.com.cn/article/t2cijmdo)、[转置原理](https://www.cnblogs.com/rainybunny/p/15755358.html)。
## 题意
给出两个 $n$ 次多项式 $F(x),G(x)$，求出 $H(x)\equiv F(G(x))(\bmod x^{n+1})$。

$n\le 2\times 10^5$。
## 思路
我们有：

$$h_i=\sum_{j=0}^nf_j[x^i]G^j(x)$$

那么这是由 $f$ 至 $h$ 的一个线性变换，不妨考虑转置原理，该问题的转置为：

$$f_j=\sum_{i=0}^nh_i[x^i]G^j(x)$$

不难发现 $F(x)=[x^n]\dfrac{H_R(x)}{1-yG(x)}$，其中 $H_R(x)$ 表示把 $H(x)$ 系数翻转得到的多项式。如果 $H(x)$ 是输入，$F(x)$ 是输出，那么我们可以直接使用 Bostan-Mori 算法得到答案，那么根据转置原理，我们写出该算法的转置即可。可以配合代码理解。

关于 Bostan-Mori 算法的过程与复杂度证明，可参见[多项式复合逆](https://www.luogu.com.cn/article/t2cijmdo)。

时间复杂度 $O(n\log^2n)$。

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
namespace MulTT{
	inline Poly MulT(const Poly &a,const Poly &b){
		Poly F=a,G=b;
		int n=a.size(),m=b.size();
		reverse(G.begin(),G.end());
		init(n);
		F.resize(lim),G.resize(lim);
		NTT(F,1),NTT(G,1);
		for(int i=0;i<lim;i++)
			G[i]=1ll*F[i]*G[i]%mod;
		NTT(G,-1);
		for(int i=m-1;i<n;i++)
			F[i-m+1]=G[i];
		F.resize(max(0,n-m+1));
		return F;
	}
	inline PolyY MulT(const PolyY &a,const PolyY &b){
		int n=a.size(),m=b.size(),p=a[0].size(),q=b[0].size();
		Poly P,Q;
		P.resize(n*p),Q.resize(m*p);
		for(int i=0;i<n;i++)
			for(int j=0;j<p;j++)
				P[i*p+j]=a[i][j];
		for(int i=0;i<m;i++)
			for(int j=0;j<q;j++)
				Q[i*p+j]=b[m-1-i][q-1-j];
		init(n*p);
		P.resize(lim),Q.resize(lim);
		NTT(P,1),NTT(Q,1);
		for(int i=0;i<lim;i++)
			P[i]=1ll*P[i]*Q[i]%mod;
		NTT(P,-1);
		PolyY F(n-m+1,Poly(p-q+1,0));
		for(int i=m-1;i<n;i++)
			for(int j=q-1;j<p;j++)
				F[i-m+1][j-q+1]=P[i*p+j]; 
		return F;
	}
}
using namespace MulTT;
inline PolyY BostanMoriT(int n,Poly P,PolyY G){
	if(!n){
		int p=G[0].size();
		P.resize(p*2-1);
		return {MulT(P,Inv(G[0]))};
	}
	if(n+1<G.size()) G.resize(n+1);
	PolyY H=G;
	for(int i=1;i<H.size();i+=2)
		for(int j=0;j<H[i].size();j++)
			H[i][j]=dec(0,H[i][j]);
	G=G*H;
	PolyY A,B;
	for(int i=0;i<G.size();i+=2) B.push_back(G[i]);
	PolyY F=BostanMoriT(n/2,P,B);
	int p=H.size(),q=F[0].size();
	A.resize(p*2);
	for(int i=0,j=0;i<p*2;i++){
		if((i&1)==(n&1)&&j<F.size()) A[i]=F[j++];
		else A[i]=Poly(q,0);
	}
	F=MulT(A,H);
	return F;
}
inline Poly Comp(Poly F,Poly G){
	int n=F.size();
	G.resize(n);
	PolyY Q;
	for(int i=0;i<n;i++)
		Q.push_back({!i,dec(0,G[i])});
	PolyY P=BostanMoriT(n-1,F,Q);
	Poly H(n,0); 
	for(int i=0;i<n;i++)
		H[n-1-i]=P[i][0];
	return H;
}
```
