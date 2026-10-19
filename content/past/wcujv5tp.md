---
title: "题解 P6466【分散层叠算法】"
date: 2023-08-04
category: "题解"
summary: "Link 题意 给出 k 个长为 n 的有序数组，q 次查询，每次给出数 x，分别求出每个数组中 x 的非严格后继，输出它们的异或和。强制在线。 k≤ 100，n≤ 104，q"
math: true
top: 2
source: https://www.luogu.com.cn/article/wcujv5tp
slug: wcujv5tp
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P6466)
## 题意

给出 $k$ 个长为 $n$ 的有序数组，$q$ 次查询，每次给出数 $x$，分别求出每个数组中 $x$ 的非严格后继，输出它们的异或和。强制在线。

$k\leq 100$，$n\leq 10^4$，$q\leq 5\times 10^5$。
## 思路
分散层叠算法，可以在 $O(k+\log n)$ 的时间复杂度内完成对 $k$ 个长为 $n$ 的序列求某个数的前驱后继。

考虑对 $k$ 个序列建线段树，每个节点维护一个有序数组。对于叶子结点，第 $i$ 个叶子结点的数组即为给出的序列 $i$。

我们定下来一个常数 $p$，对于一个非叶子结点，我们将其左儿子的序列从大到小，每隔 $p$ 个取出一个数，得到数组 $L$（从小到大排），同理得到数组 $R$。

我们将 $L$ 与 $R$ 归并起来，得到此结点的数组，同时我们还需要记录数组中每个数来自左儿子（设为红色）还是右儿子（设为蓝色），位于左儿子（右儿子）的数组中的哪个位置。

对于一次询问，我们在根节点数组上二分出 $x$ 的后继 $t$，考虑如何得到左儿子和右儿子中 $x$ 的后继。假设 $t$ 为红色，在左儿子中的位置为 $i$，则左儿子中，$x$ 的后继的位置一定在 $(i-p,i]$ 中（$i-p$ 位置在此结点的数组中，显然它小于 $x$）。同理找出 $x$ 在根节点上的数组中第一个蓝色后继，令它在右儿子中的位置为 $j$，则右儿子中 $x$ 的后继的位置一定在 $(j-p,j]$ 中。于是我们 $O(p)$ 向前枚举 $x$ 后继位置，向左右儿子递归即可。注意到我们需要求出数组中每个数后面第一个与它异色的数的位置，可以在 `pushup` 时求出。

令 $p$ 为大于等于 $2$ 的常数，则我们发现所有数组长度之和为 $O(nk)$，单次询问每个结点贡献均为常数，总时间复杂度为 $O(nk+q(k+\log n))$。

线段树方法的优势在于可以支持修改和区间查询，更方便维护一些分块中多块二分的问题，例如[由乃打扑克](https://www.luogu.com.cn/problem/P5356)。

代码实现：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
const int N=100+10,L=1e4+10;
int n,k,q,d,s[N][L];
struct Segment_Tree{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	const int K=2;
	struct node{
		int val,pos,xp;
		bool s;
		node(int v=0,int p=0,int o=0){ val=v,pos=p,s=o,xp=-1; }
		inline friend bool operator<(const node &a,const node &b){
			return a.val<b.val;
		}
	};
	node pol[N*L*2],*now=pol;
	node *a[N<<2];
	int siz[N<<2]; 
	inline void pushup(int rt){
		static node l[L],r[L];
		int c1=0,c2=0;
		for(int i=siz[ls]-1;i>=0;i-=K)
			l[c1++]=node(a[ls][i].val,i,0);
		for(int i=siz[rs]-1;i>=0;i-=K)
			r[c2++]=node(a[rs][i].val,i,1);
		reverse(l,l+c1);
		reverse(r,r+c2);
		siz[rt]=c1+c2;
		a[rt]=now,now+=siz[rt];
		merge(l,l+c1,r,r+c2,a[rt]);
		for(int lsl=-1,lsr=-1,i=siz[rt]-1;i>=0;i--){
			if(!a[rt][i].s) lsl=i,a[rt][i].xp=lsr;
			else lsr=i,a[rt][i].xp=lsl;
		}
	}
	inline void build(int rt,int l,int r){
		if(l==r){
			siz[rt]=n;
			a[rt]=now,now+=siz[rt];
			for(int i=0;i<siz[rt];i++)
				a[rt][i]=node(s[l][i],i);
			return ;
		}
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r);
		pushup(rt);
	}
	int ans;
	inline void query(int rt,int l,int r,int p,int x){
		while(p&&a[rt][p-1].val>=x) p--;
		if(l==r){
			ans^=a[rt][p].val;
			return ;
		}
		int mid=l+r>>1;
		if(!a[rt][p].s){
			query(ls,l,mid,a[rt][p].pos,x);
			if(a[rt][p].xp!=-1) query(rs,mid+1,r,a[rt][a[rt][p].xp].pos,x);
		}else{
			if(a[rt][p].xp!=-1) query(ls,l,mid,a[rt][a[rt][p].xp].pos,x);
			query(rs,mid+1,r,a[rt][p].pos,x);
		}
	}
	inline int query(int x){
		ans=0;
		int p=lower_bound(a[1],a[1]+siz[1],node(x))-a[1];
		query(1,1,k,p,x);
		return ans;
	}
}T;
int main(){
	n=read(),k=read(),q=read(),d=read();
	for(int i=1;i<=k;i++)
		for(int j=0;j<n;j++)
			s[i][j]=read();
	T.build(1,1,k);
	for(int i=1,lst=0;i<=q;i++){
		lst=T.query(read()^lst);
		if(i%d==0) write(lst),putc('\n');
	}
	flush();
}
```
