---
title: "题解 P5273【【模板】多项式幂函数 (加强版)】"
date: 2021-03-04
category: "题解"
summary: "传送门 板子题。 题意 给 n-1 次多项式 F(x) 和 k，求 G(x) Fk(x)( xn)。 思路 然后思考正解： 首先我们有 G(x) Fk(x)( xn) G(x)"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/dh2onfpz
slug: dh2onfpz
---

[_传送门_](https://www.luogu.com.cn/problem/P5273)

板子题。
## 题意
给 $n-1$ 次多项式 $F(x)$ 和 $k$，求 $G(x)\equiv F^k(x)(\bmod x^n)$。
## 思路
然后思考正解：

首先我们有
$$G(x)\equiv F^k(x)(\bmod x^n)$$
$$\ln G(x)\equiv k\ln F(x)(\bmod x^n)$$
$$G(x)\equiv e^{k\ln F(x)}(\bmod x^n)$$

由于 $k$ 很大要将 $k$ 对 998244352 取模（拓展欧拉定理）。

然后我们惊奇地发现:$f_0\ne1$，我们不能求 $\ln F(x)$！

于是我们可以求 $\ln \dfrac{F(x)}{f_0}$，最后 $\times f_0$ 即可。

然后我们又惊奇地发现:$f_0=0$ 时没法这样做。

于是我们设 $f_l\ne0$，于是将多项式整体左移 $l$ 位，除掉，最后再右移 $k\times l$ 位，左边填 $0$。

最后给 Code:
```cpp
#define ll long long
const int mod=998244353,N=6e5+10;
inline void print(int *a){
	for(int i=0;a[i]||a[i+1]||a[i+2]||a[i+3]||a[i+4]||a[i+5];i++){
		printf("%d ",a[i]);
	}
	puts("");
}
struct ntt{
	int n,a[N],b[N],c[N],qqqq[N],s[N],ss[N],d[N],e[N],rev[N],f[N],g[N],inv[N],lim;
	char m[N];
	inline void init(int n,int mode=1){
		if(mode){
			int l=0;
			for(lim=1;lim<=n;lim<<=1)l++;
			for(int i=1;i<lim;i++){
				rev[i]=(rev[i>>1]>>1)|((i&1)<<(l-1));
			}
		}else{
			for(lim=1;lim<=n;lim<<=1);
		}
	}
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
		inv[1]=1;
		for(int i=2;i<=n;i++){
			inv[i]=1ll*(mod-mod/i)*inv[mod%i]%mod;
		}
	}
	inline void NTT(int *a,bool t){
		for(int i=0;i<lim;i++){
			if(i<rev[i]){
				swap(a[i],a[rev[i]]);
			}
		}
		for(int i=1;i<lim;i<<=1){
			int gl=qpow(3,(mod-1)/(i<<1));
			for(int j=0;j<lim;j+=(i<<1)){
				int t1,t2,now=1;
				for(int k=0;k<i;k++,now=1ll*now*gl%mod){
					t1=a[j+k];
					t2=1ll*now*a[i+j+k]%mod;
					a[j+k]=(t1+t2)%mod;
					a[i+j+k]=(t1-t2+mod)%mod;
				}
			}
		}
		if(!t) return ;
		int Inv=qpow(lim,mod-2);
		reverse(a+1,a+lim);
		for(int i=0;i<lim;i++){
			a[i]=1ll*a[i]*Inv%mod;
		}
	}
	inline void Inv(int dg,int *a,int *b){
		if(dg==1){
			b[0]=qpow(a[0],mod-2);
			return ;
		}
		Inv(dg+1>>1,a,b);
		init((dg<<1)-1);
		for(int i=0;i<dg;i++){
			c[i]=a[i];
		}
		for(int i=dg;i<lim;i++){
			c[i]=0;
		}
		NTT(c,0);
		NTT(b,0);
		for(int i=0;i<lim;i++){
			b[i]=1ll*(2-1ll*c[i]*b[i]%mod+mod)%mod*b[i]%mod;
		}
		NTT(b,1);
		for(int i=dg;i<lim;i++){
			b[i]=0;
		}
	}
	inline void Mul(int *a,int *b,int n){
		init(n);
		memset(c,0,lim<<2);
		memcpy(c,b,n<<2);
		NTT(a,0);
		NTT(c,0);
		for(int i=0;i<lim;i++){
			a[i]=1ll*a[i]*c[i]%mod;
		}
		NTT(a,1);
	}
	inline void Der(int *a,int *b,int n){
		for(int i=1;i<n;i++){
			b[i-1]=1ll*i*a[i]%mod;
		}
		b[n-1]=0;
	}
	inline void Invder(int *a,int *b,int n){
		for(int i=1;i<n;i++){
			b[i]=1ll*a[i-1]*inv[i]%mod;
		}
		b[0]=0;
	}
	inline void polyln(int *a,int *b,int n){
		for(int i=0;i<(n<<2);i++){
			qqqq[i]=d[i]=0;
		}
		Der(a,qqqq,n);
		Inv(n,a,d);
		Mul(qqqq,d,n);
		Invder(qqqq,b,n);
	}
	inline void Log(int n,int *f,int *g){
		init(n);
		polyln(f,g,lim);
		for(int i=n;i<lim;i++){
			g[i]=0;
		}
	}
	inline void polyexp(int n,int *a,int *b){
		if(n==1){
			b[0]=1;
			return ;
		}
		Exp(n+1>>1,a,b);
		init(n<<1);
		Log(n,b,s);
		for(int i=0;i<n;i++){
			s[i]=a[i]>=s[i]?a[i]-s[i]:a[i]+mod-s[i];
		}
		for(int i=n;i<lim;i++){
			b[i]=s[i]=0;
		}
		s[0]++;
		NTT(s,0);
		NTT(b,0);
		for(int i=0;i<lim;i++){
			b[i]=1ll*b[i]*s[i]%mod;
		}
		NTT(b,1);
		for(int i=n;i<lim;i++){
			b[i]=0;
		}
	}
	inline void Exp(int n,int *a,int *b){
		polyexp(n,a,b);
	}
	inline void polypow(int n,int k1,int k2,int *a,int *b){
		int fst=0;
		for(;fst<n&&!a[fst];fst++);
		if(1ll*fst*k1>=n){
			memset(b,0,n<<2);
			return ;
		}
		int Q=qpow(f[fst],mod-2),P=qpow(f[fst],k2);
		for(int i=0;i<n;i++){
			a[i]=1ll*a[i+fst]*Q%mod;
		}
		Log(n,a,ss);
		for(int i=0;i<n;i++){
			a[i]=1ll*ss[i]*k1%mod;
		}
		memset(ss,0,n<<2);
		Exp(n,a,ss);
		fst*=k1;
		for(int i=0;i<fst;i++){
			b[i]=0;
		}
		for(int i=fst;i<n;i++){
			b[i]=1ll*ss[i-fst]*P%mod;
		}
	}
	inline void Pow(int n,char* m,int sz,int *f,int *g){
		int k1=0,k2=0,k3=0;
		for(int i=1;i<=sz;i++){
			k1=(10ll*k1+m[i]-'0')%mod;
			k2=(10ll*k2+m[i]-'0')%(mod-1);
		}
		for(int i=1;i<=min(6,sz);i++){
			k3=10*k3+m[i]-'0';
		}
		if(f[0]==0&&k3>=n){
			memset(g,0,n<<2);
			return ;
		}
		init(n<<1|1);
		polypow(n,k1,k2,f,g);
	}
	inline void MAIN(){
		n=read();
		get(m);
	    memset(f,0,sizeof(f));
		for(int i=0;i<n;i++){
			f[i]=read();
		}
		init(n,0);
		Prefix(lim<<1);
		Pow(n,m,strlen(m+1),f,g);
		for(int i=0;i<n;i++){
			write(g[i]);
			out[len++]=' ';
		}
	}
}w;
/*
4 999999999122344455
1 2 3 4
*/
```
欢迎 $\texttt{hack!}$

再见 qwq~
