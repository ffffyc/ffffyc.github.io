---
title: "题解 P7448&P7601【[Ynoi2007] rdiq】"
date: 2021-05-30
category: "题解"
summary: "Link\\&\\text{Link} 在这道题被公布后算一血（？ ~~虽然区间本质不同逆序对那题没抢到~~ 一道神仙题。 前置知识：区间逆序对。 题意如题，就不说了。 接下来的大"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/amnbio1g
slug: amnbio1g
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P7448)[$\&\text{Link}$](https://www.luogu.com.cn/problem/P7601)

在这道题被公布后算一血（？

~~虽然区间本质不同逆序对那题没抢到~~

一道神仙题。

前置知识：[区间逆序对](https://www.luogu.com.cn/problem/P5047)。

题意如题，就不说了。

接下来的大部分都是复读（

首先我们知道要用莫队二次离线，然后考虑 $[l,r]\to[l,r+1]$，如果是直接求逆序对的话贡献就是 $i\in[l,r],a_i>a_{r+1}$ 的个数。

考虑本质不同，设 $a_i$ 在序列中上次出现的位置为 $last_i$，则 $i\in[l,last_{r+1}-1],(a_i,a_{last_{r+1}})$ 与 $(a_i,a_{r+1})$ 的本质相同，故不考虑，则贡献为 $i\in[last_{r+1},r],a_i>a_{r+1}$。

所以查询转为查询有多少值 $x$ 在区间 $[last_{r+1},r]$ 中出现，并不在区间 $[l,last_{r+1}-1 ]$中出现，并且 $x>a[r]$。

然后来看看扫描线部分，令 $r=1,2,..,n$，维护 $\{(i,a_i)|1\le i\le r,\forall j\in[i+1,r],a_i\ne a_j\}$（这里维护右端不同与维护左端本质一致），扫到 $r$ 时，$[l,r]$ 即查询 $\max(l-1,last_{r})<i<r,a_i>a_r$ 的点数了。

然后就转化为了 $O(n)$ 的单点加，$O(n\sqrt m)$ 的矩阵求和。

显然，我们需要一个 $O(\sqrt n)$ 单点加，$O(1)$ 矩阵求和的数据结构。

这个可以分块套分块，具体我不怎么会讲，就复制官方题解了：

>有一个使用分块套分块拼出单点修改矩形和的数据结构，两个分块大小均为 $O(n^{0.25})$，这样修改复杂度是 $O(n^{0.25}\times n^{0.25})=O(\sqrt n)$ 的，查询复杂度是 $O(1)$ 的，只是常数大了点。
>
>第 $1,2$ 层网格只有 $\sqrt n+1$ 个，是线性空间的，点修改需要在 $4$ 个 $n^{k1}\times n^{k2} $，$k1,k2=0.25,0.5$ 的网格上重算二维前缀和，空间为 $O(n)$。
>
>第 $3,4$ 层网格可以不维护，而是直接算 $1,2$ 层未处理的修改对 $n$ 个可能的查询的贡献，时间复杂度为 $O(\sqrt n)$，空间复杂度为 $O(n)$。

时间复杂度 $O(n(\sqrt m+\sqrt n))$，空间复杂度 $O(n)$。

代码（还挺短的）：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define node tuple<int,int,int>
#define give(x,y,z) tie(x,y,z)
namespace IO{//by cyffff
	
}
const int N=1e5+10;
int a[N],b[N],curL=1,curR;
int divv[N],bel1[N],bel2[N],beg1[520],beg2[35],sz1,sz2;
int blo;
int n,m,k;
ll ans[N*5];
struct query{
	int l,r,ind;
	ll ans;
	inline friend bool operator<(const query &a,const query &b){
		return divv[a.l]^divv[b.l]?a.l<b.l:divv[a.l]&1?a.r<b.r:a.r>b.r;
	}
}q[N*5];
vector<node>vec[N];
int tong[N],p[N],wz[N],pre[N],suf[N],last[N];
int s1[35][35],s2[520][35],s3[35][520],s4[520][520],s5[N];
inline void init(){
	memset(tong,0,sizeof(tong));
	for(int i=1;i<=n;i++){
		tong[a[i]]++;
	}
	for(int i=1;i<=n;i++){
		tong[i]+=tong[i-1];
	}
	for(int i=1;i<=n;i++){
		p[i]=tong[a[i]]--;
		wz[p[i]]=i;
	}
	memset(last,0,sizeof(last));
	for(int i=1;i<=n;i++){
		pre[i]=last[a[i]];
		last[a[i]]=i;
	}
	memset(last,0,sizeof(last));
	for(int i=n;i>=1;i--){
		suf[i]=last[a[i]];
		last[a[i]]=i;
	}
	memset(s1,0,sizeof(s1));
	memset(s2,0,sizeof(s2));
	memset(s3,0,sizeof(s3));
	memset(s4,0,sizeof(s4));
	memset(s5,0,sizeof(s5));
}
inline void modify(int q,int v){
	int x=p[q];
	int x1=bel1[q],x2=bel2[q],y1=bel1[x],y2=bel2[x];
	int qx=beg1[x1],qy=beg1[y1],px=beg2[x2],py=beg2[y2];
	for(int i=1;i<x2;i++)
		for(int j=1;j<y2;j++)
			s1[i][j]+=v;
	for(int i=px;i<x1;i++)
		for(int j=1;j<y2;j++)
			s2[i][j]+=v;
	for(int i=1;i<x2;i++)
		for(int j=py;j<y1;j++)
			s3[i][j]+=v;
	for(int i=px;i<x1;i++)
		for(int j=py;j<y1;j++)
			s4[i][j]+=v;
	for(int i=qx;i<q;i++)
		if(p[i]<qy)
			s5[i]+=v;
	for(int i=qy;i<x;i++)
		if(wz[i]<q)
			s5[wz[i]]+=v;
}
inline int query(int q){
	int x=p[q];
	int x1=bel1[q],x2=bel2[q],y1=bel1[x],y2=bel2[x];
	return s1[x2][y2]+s2[x1][y2]+s3[x2][y1]+s4[x1][y1]+s5[q];
}
inline void solve(){
	init();
	for(int i=1;i<=n;i++){
		if(pre[i]) modify(pre[i],-1);
		modify(i,1);
		for(auto t:vec[i]){
			int l,r,ind;
			ll v=0;
			give(l,r,ind)=t;
			for(int j=l;j<=r;j++){
				if(suf[j]<i) v-=query(suf[j]);
				v+=query(j);
			}
			if(ind<0) q[-ind].ans-=v;
			else q[ind].ans+=v;
		}
	}
}
int main(){
//	freopen("P7601_1.in","r",stdin);
//	freopen("P7601_1.wrong","w",stdout);
	n=read();
	for(int i=1;i<=n;i++){
		a[i]=read();
	}
	m=read();
	for(int i=1;i<=m;i++){
		q[i].l=read(),q[i].r=read(),q[i].ind=i;
	}
	blo=n/sqrt(m);
	for(int i=1;i<=n;i++){
		divv[i]=(i-1)/blo+1;
	}
	sort(q+1,q+m+1);
	blo=sqrt(sqrt(n));
	sz1=blo*blo,sz2=blo*sz1;
	for(int i=1;i<=n;i++){
		bel1[i]=(i-1)/sz1+1;
		bel2[i]=(i-1)/sz2+1;
	}
	for(int i=n;i>=1;i--){
		beg1[bel1[i]]=i;
		beg2[bel2[i]]=bel1[i];
	}
	for(int i=1;i<=m;i++){
		int l=q[i].l,r=q[i].r;
		if(curR<r) curR=r;
		if(curL>l) vec[curR].emplace_back(l,curL-1,i),curL=l;
		if(curR>r) curR=r;
		if(curL<l) vec[curR].emplace_back(curL,l-1,-i),curL=l;
	}
	for(int i=1;i<=n;i++){
		a[i]=n-a[i]+1;
	}
	solve();
	reverse(a+1,a+n+1);
	for(int i=1;i<=n;i++){
		a[i]=n-a[i]+1;
		vec[i].clear();
	}
	curL=1,curR=0;
	for(int i=1;i<=m;i++){
		int l=q[i].l,r=q[i].r;
		if(curR<r) vec[n-curL+1].emplace_back(n-r+1,n-curR,i),curR=r;
		if(curL>l) curL=l;
		if(curR>r) vec[n-curL+1].emplace_back(n-curR+1,n-r,-i),curR=r;
		if(curL<l) curL=l;
	}
	solve();
	for(int i=1;i<=m;i++){
		q[i].ans+=q[i-1].ans;
	}
	for(int i=1;i<=m;i++){
		ans[q[i].ind]=q[i].ans;
	}
	for(int i=1;i<=m;i++){
		write(ans[i]);
		putc('\n');
	}
	flush();
}
```
再见 qwq~
