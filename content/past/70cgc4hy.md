---
title: "题解：P10800「CZOI-R1」卡牌"
date: 2024-07-22
category: "题解"
summary: "Link 最近做的最神金的一道数据结构题。 题意 给出 m 个值域为 [1,n] 的四元组 ti,0 3，定义四元组 A 胜于四元组 B 当且仅当最多存在一个 j∈[0,3] "
math: true
top: 2
source: https://www.luogu.com.cn/article/70cgc4hy
slug: 70cgc4hy
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10800)

最近做的最神金的一道数据结构题。
## 题意
给出 $m$ 个值域为 $[1,n]$ 的四元组 $t_{i,0\sim 3}$，定义四元组 $A$ 胜于四元组 $B$ 当且仅当最多存在一个 $j\in[0,3]$ 使得 $A_j\le B_j$，求出有多少个值域为 $[1,n]$ 的四元组 $A$ 胜于所有的 $t_{1\sim n}$。

$n,m\le 5\times 10^5$。
## 题解
为了易读，本文中递增表示不递减，递减表示不递增。

一个直接的思路就是令 $v_{i,j,k}$ 表示有几个合法四元组前三维分别为 $i,j,k$，此时合法四元组的第四维是一个后缀。

那么我们考虑一个限制 $t$：
- 如果前三维均比 $t$ 大，则无需考虑该限制；
- 如果前三维恰有一维不比 $t$ 大，则第四维要比 $t$ 大；
- 如果前三维有至少两维不比 $t$ 大，则必然不合法。

考虑这个恰有一维是不需要的，我们可以将它转为对 $v$ 的操作：
- 对于 $i\le t_0$，将 $v_{i,j,k}$ 对 $n-t_3$ 取 $\min$；
- 对于 $j\le t_1$，将 $v_{i,j,k}$ 对 $n-t_3$ 取 $\min$；
- 对于 $k\le t_2$，将 $v_{i,j,k}$ 对 $n-t_3$ 取 $\min$；
- 对于 $i\le t_0\land j\le t_1$，将 $v_{i,j,k}$ 设为 $0$；
- 对于 $i\le t_0\land k\le t_2$，将 $v_{i,j,k}$ 设为 $0$；
- 对于 $j\le t_1\land k\le t_2$，将 $v_{i,j,k}$ 设为 $0$。

显然这些操作的顺序对答案无影响，则我们可以处理出 $a_i,b_j,c_k$ 表示考虑前三种操作后第 $i$ 行，第 $j$ 列，第 $k$ 层的取 $\min$ 标记。不考虑置零操作，则 $v_{i,j,k}=\min(a_i,b_j,c_k)$，其中 $a,b,c$ 均单调递增。

再考虑置零操作。设第 $j$ 列最大清到行 $u_j$（第一种），第 $k$ 层最大清到行 $x_k$（第二种）、列 $y_k$（第三种），其中 $u,x,y$ 均单调递减。

答案即可表示为
$$\sum_{i,j,k}^{i>u_j\land i>x_k\land j>y_k}\min(a_i,b_j,c_k)$$
但这样不优。

令 $f_j$ 为最大的 $i$ 使得 $a_i\le b_j$，$g_k$ 为最大的 $j$ 使得 $b_j\le c_k$，$h_k$ 为最大的 $i$ 使得 $a_i\le c_k$，显然 $f,g,h$ 均单调递增。

考虑对 $k$ 扫描线，则第 $k$ 层的 $v_{i,j,k}$ 如下所示：

$$\begin{pmatrix}
b_1&b_2&\dots&b_{j}&c_k&\dots&c_k\\
.&.&\dots &.&.&\dots&.\\
b_1&b_2&\dots&b_{j}&c_k&\dots&c_k\\
b_1&b_2&\dots&b_{j}&a_{h_k}&\dots&a_{h_k}\\
.&.&\dots &.&.&\dots&.\\
b_1&b_2&\dots &b_j&a_{f_j+1}&\dots&a_{f_j+1}\\
b_1&b_2&\dots &a_{f_j}&a_{f_j}&\dots&a_{f_j}\\
.&.&\dots &.&.&\dots&.\\
b_1&a_{f_2}&\dots &a_{f_2}&a_{f_2}&\dots&a_{f_2}\\
.&.&\dots &.&.&\dots&.\\
.&.&\dots &.&.&\dots&.\\
a_{1}&a_{1}&\dots &a_{1}&a_{1}&\dots&a_{1}\\
\end{pmatrix}
$$

其中 $j=g_k$。则答案分为四个部分：

- 在 $g_k$ 列及之前的取到 $a_i$ 作为最小值的部分：$\displaystyle\sum_{j=y_k+1}^{g_k}\sum_{i=\max(x_k,u_j)+1}^{f_j}a_i$；
- 取到 $b_j$ 作为最小值的部分：$\displaystyle\sum_{j=y_k+1}^{g_k}[n-\max(x_k,u_j,f_j)]b_j$；
- 在 $g_k$ 列之后的取到 $a_i$ 作为最小值的部分：$\displaystyle\sum_{j=\max(y_k,g_k)+1}^{n}\sum_{i=\max(x_k,u_j)+1}^{h_k}a_i$；
- 取到 $c_k$ 作为最小值的部分：$\displaystyle c_k\sum_{j=\max(y_k,g_k)+1}^{n}[n-\max(x_k,u_j,h_k)]$。

再求出 $p_i$ 为最大的 $j$ 使得 $u_j\ge i$，$q_i$ 为最小的 $j$ 使得 $f_j\ge i$。在移动 $k\to k+1$ 时增加 $h$、减少 $x$ 并依据式子对四个部分分别增量，分别使用线段树或树状数组维护即可。

认为 $n,m$ 同阶，时间复杂度 $O(n\log n)$。

参考代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define ui unsigned
namespace IO{//by cyffff
	
}
inline void umn(int &x,int y){ x=min(x,y); }
inline void umx(int &x,int y){ x=max(x,y); }
const int N=5e5+10;
int n,m,a[N],b[N],c[N],f[N],g[N],h[N],u[N],x[N],y[N],p[N],q[N];
struct Segment_Tree{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	ui ans[N<<2],sum[N<<2],tag[N<<2];
	inline void pushup(int rt){
		ans[rt]=ans[ls]+ans[rs];
		sum[rt]=sum[ls]+sum[rs];
	}
	inline void pushtag(int rt,ui v){
		tag[rt]+=v,ans[rt]+=sum[rt]*v;
	}
	inline void pushdown(int rt){
		if(!tag[rt]) return ;
		pushtag(ls,tag[rt]);
		pushtag(rs,tag[rt]);
		tag[rt]=0;
	}
	inline void build(int rt,int l,int r){
		if(l==r){
			sum[rt]=b[l];
			return ;
		}
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r);
		pushup(rt);
	}
	inline void modify(int rt,int l,int r,int L,int R,ui v){
		if(L>R) return ;
		if(L<=l&&r<=R) return pushtag(rt,v);
		pushdown(rt);
		int mid=l+r>>1;
		if(L<=mid) modify(ls,l,mid,L,R,v);
		if(R>mid) modify(rs,mid+1,r,L,R,v);
		pushup(rt);
	}
	inline ui query(int rt,int l,int r,int L,int R){
		if(L>R) return 0;
		if(L<=l&&r<=R) return ans[rt];
		pushdown(rt);
		int mid=l+r>>1;
		ui s=0;
		if(L<=mid) s+=query(ls,l,mid,L,R);
		if(R>mid) s+=query(rs,mid+1,r,L,R);
		return s;
	}
}T3;
struct BIT{
	#define lowbit(i) (i&-i)
	ui t1[N],t2[N];
	inline void add(int x,ui v){
		for(int i=x;i<=n;i+=lowbit(i))
			t1[i]+=v,t2[i]+=1u*x*v;
	}
	inline ui query(int x){
		ui s1=0,s2=0;
		for(int i=x;i;i-=lowbit(i))
			s1+=t1[i],s2+=t2[i];
		return 1u*(x+1)*s1-s2; 
	}
	inline ui query(int l,int r){
		return l<=r?query(r)-query(l-1):0;
	}
}T[3];
int main(){
	n=read(),m=read();
	for(int i=1;i<=n+1;i++)
		a[i]=b[i]=c[i]=n;
	for(int i=1;i<=m;i++){
		int A=read(),B=read(),C=read(),D=read();
		umn(a[A],n-D),umn(b[B],n-D),umn(c[C],n-D);
		umx(u[B],A),umx(x[C],A),umx(y[C],B);
	}
	for(int i=n;i;i--)
		umn(a[i],a[i+1]),umn(b[i],b[i+1]),umn(c[i],c[i+1]),
		umx(u[i],u[i+1]),umx(x[i],x[i+1]),umx(y[i],y[i+1]);
	x[0]=n;
	for(int i=0,j=1;j<=n;j++){
		while(i<n&&a[i+1]<=b[j]) i++;
		f[j]=i;
	}
	for(int j=0,k=1;k<=n;k++){
		while(j<n&&b[j+1]<=c[k]) j++;
		g[k]=j;
	}
	for(int i=0,k=1;k<=n;k++){
		while(i<n&&a[i+1]<=c[k]) i++;
		h[k]=i;
	}
	for(int j=0,k=n;k;k--){
		while(j<n&&u[j+1]>=k) j++;
		p[k]=j;
	}
	for(int j=n+1,k=n;k;k--){
		while(j&&f[j-1]>=k) j--;
		q[k]=j;
	}
	T3.build(1,1,n);
	ui ans=0;
	for(int k=1;k<=n;k++){
		for(int i=h[k-1]+1;i<=h[k];i++)
			if(i>x[k-1]){
				T[1].add(p[i]+1,a[i]);
				T[2].add(p[i]+1,-1);
			}
		for(int i=x[k-1];i>x[k];i--){
			T[0].add(max(p[i]+1,q[i]),a[i]);
			T3.modify(1,1,n,p[i]+1,q[i]-1,1);
			if(i<=h[k]) T[1].add(p[i]+1,a[i]);
			if(i>h[k]) T[2].add(p[i]+1,1);
		}
		ans+=T[0].query(y[k]+1,g[k]);
		ans+=T3.query(1,1,n,y[k]+1,g[k]);
		ans+=T[1].query(max(y[k],g[k])+1,n);
		ans+=1u*c[k]*T[2].query(max(y[k],g[k])+1,n);
	}
	write(ans);
	flush();
}
```
