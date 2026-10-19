---
title: "题解 NOIP2022 62C【区间】"
date: 2022-11-22
category: "题解"
summary: "题意 给出 n 个数轴上的区间 [li,ri]，定义 w(L,R)=|i=LR[li,ri]|，m 个询问 [l,r]，求出 2(r-l+1)(r-l+2)Σi=lrΣj=ir"
math: true
top: 2
source: https://www.luogu.com.cn/article/9uadyd4z
slug: 9uadyd4z
---

## 题意
给出 $n$ 个数轴上的区间 $[l_i,r_i]$，定义 $\displaystyle w(L,R)=\left|\bigcup_{i=L}^R[l_i,r_i]\right|$，$m$ 个询问 $[l,r]$，求出 $\displaystyle\dfrac{2}{(r-l+1)(r-l+2)}\sum_{i=l}^r\sum_{j=i}^rw(i,j)$，对 $998244353$ 取模。

$n\le 8\times 10^5$，$m\le 10^6$，$1\le l_i< r_i\le 998244353$，时限 4s。
## 思路
数轴上的区间不好处理，将 $[l,r]$ 用 $[l,r-1]$ 表示，每个点 $i$ 对应了 $i$ 到 $i+1$ 的区间。

考虑离线扫描线。这个区间应该是离不开颜色段均摊的。

我们定义 $S_i$ 为扫到 $i$ 时刻的颜色段均摊，每一个颜色段用 $(x,y)$ 表示，其中 $x$ 为此段属于哪个区间 $[l_x,r_x]$，$y$ 表示这段的长度。

考虑要求什么：

$$\begin{aligned}&\sum_{i=1}^r\sum_{j\ge l}\sum_{(x,y)\in S_i}[x\ge j]y\\
&=\sum_{i=1}^r\sum_{(x,y)\in S_i}[x\ge l](x-l+1)y\\
&=\sum_{i=1}^r\sum_{(x,y)\in S_i}[x\ge l]xy-(l-1)\sum_{(x,y)\in S_i}[x\ge l]y\end{aligned}$$

在插入、删除颜色段的时候在 $x$ 的位置修改一下。发现一个 $x$，它会对每个时刻都有 $xy-(l-1)y$ 的贡献。考虑使用维护区间历史版本和的线段树，一颗维护 $xy$，一颗维护 $y$。

历史版本和线段树用加一次函数的形式更容易理解和维护。

预处理 $1\sim n$ 的逆元，时间复杂度 $O((n+q)\log n)$。

参考代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
#define sit set<node>::iterator
const int N=8e5+10,Q=2e6+10,mod=998244353;
inline int qpow(int x,int y){
	int res=1;
	while(y){
		if(y&1) res=1ll*res*x%mod;
		x=1ll*x*x%mod;
		y>>=1;
	}
	return res;
}
int n,q,L[N],R[N],ans[Q],inv[N];
struct Query{
	int l,id;
};
vector<Query>vec[N];
struct node{
	int l;
	mutable int r,v;
	node(int L=0,int R=0,int V=0){l=L,r=R,v=V;}
	inline friend bool operator<(const node &a,const node &b){
		return a.l<b.l;
	}
};
struct Line{
	int k,b;
	Line(int K=0,int B=0){ k=K%mod,b=B%mod; }
	inline friend Line operator+(const Line &a,const Line &b){
		return {(a.k+b.k)%mod,(a.b+b.b)%mod};
	}
	inline int getv(int x){
		return (1ll*k*x+b)%mod; 
	}
};
struct Segment_Tree{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	Line sum[N<<2];
	inline void pushup(int rt){
		sum[rt]=sum[ls]+sum[rs];
	}
	inline void modify(int rt,int l,int r,int p,Line v){
		if(l==r){
			sum[rt]=sum[rt]+v;
			return ;
		}
		int mid=l+r>>1;
		if(p<=mid) modify(ls,l,mid,p,v);
		else modify(rs,mid+1,r,p,v);
		pushup(rt);
	}
	inline int query(int rt,int l,int r,int L,int R,int x){
		if(L<=l&&r<=R)
			return sum[rt].getv(x);
		int mid=l+r>>1,ans=0;
		if(L<=mid) ans=(ans+query(ls,l,mid,L,R,x))%mod;
		if(R>mid) ans=(ans+query(rs,mid+1,r,L,R,x))%mod;
		return ans;
	}
}T1,T2;
set<node>st;
inline sit split(int p){
	sit it=st.lower_bound(node(p));
	if(it!=st.end()&&it->l==p)
		return it;
	--it;
	int r=it->r,v=it->v;
	it->r=p-1;
	return st.insert(node(p,r,v)).first;
}
inline void ins(int l,int r,int id){
	if(l>r) return ;
	sit itr=split(r+1),itl=split(l);
	for(sit it=itl;it!=itr;++it){
		int x=it->v,y=it->r-it->l+1;
		T1.modify(1,0,n,x,Line(mod-1ll*x*y%mod,1ll*x*y%mod*(id-1)%mod));
		T2.modify(1,0,n,x,Line(mod-y,1ll*y*(id-1)%mod));
	}
	int x=id,y=r-l+1;
	T1.modify(1,0,n,x,Line(1ll*x*y%mod,mod-1ll*x*y%mod*(id-1)%mod));
	T2.modify(1,0,n,x,Line(y,mod-1ll*y*(id-1)%mod));
	st.erase(itl,itr),st.insert(node(l,r,id));
}
/*
2 1
1 5
4 8
1 2
*/
int main(){
	n=read(),q=read();
	for(int i=1;i<=n;i++)
		L[i]=read(),R[i]=read()-1;
	st.insert(node(1,mod));
	for(int i=1;i<=q;i++){
		int l=read(),r=read();
		vec[r].push_back((Query){l,i});
	}
	for(int i=1;i<=n;i++){
		ins(L[i],R[i],i);
		for(auto q:vec[i])
			ans[q.id]=(T1.query(1,0,n,q.l,n,i)-1ll*(q.l-1)*T2.query(1,0,n,q.l,n,i)%mod+mod)%mod*qpow(1ll*(i-q.l+1)*(i-q.l+2)/2%mod,mod-2)%mod;
	}
	for(int i=1;i<=q;i++)
		write(ans[i]),putc('\n');
	flush();
}
```
