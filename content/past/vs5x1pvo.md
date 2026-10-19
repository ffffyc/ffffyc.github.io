---
title: "题解：P10590 磁力块"
date: 2024-08-26
category: "题解"
summary: "Link 来自传奇讨论区大神 @年年有年 的 O(nlog n) 做法！ 题意 有 n+1 块磁铁 0 n，每个磁铁都有四个属性 (di,mi,pi,ri)，如果你拥有了磁铁 "
math: true
top: 2
source: https://www.luogu.com.cn/article/vs5x1pvo
slug: vs5x1pvo
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10590)

来自传奇讨论区大神 @[年年有年](https://www.luogu.com.cn/user/377973) 的 $O(n\log n)$ 做法！

## 题意

有 $n+1$ 块磁铁 $0\sim n$，每个磁铁都有四个属性 $(d_i,m_i,p_i,r_i)$，如果你拥有了磁铁 $i$，那么你就能吸引并拥有所有满足 $d_j\le r_i,m_j\le p_i$ 的磁铁 $j$，初始你只拥有磁铁 $0$，求最后你能得到多少的磁铁。

$n\le 2.5\times 10^5$。
## 思路
考虑我们 BFS 中要求出满足两维偏序限制的还未被拥有过的磁铁，则预先对一维排序，另一维使用数据结构维护。

具体做法为，我们对线段树每个结点维护一个 `vector`，初始按 $m$ 从小到大排序，将 $i$ `push_back` 至所有包含 $d_i$ 的结点，这样每个结点的 `vector` 中的下标就满足其 $m$ 值是递增的。对每个结点维护一个指针 $u$ 表示这个结点的 `vector` 的前 $u$ 个磁铁都已经访问过，搜一个磁铁 $i$ 能更新的磁铁时直接在 $[1,r_i]$ 所拆出的所有结点上不断增加指针直至其对应 $m$ 值大于 $p_i$ 即可。

所有 `vector` 的大小和为 $O(n\log n)$，指针只会后移，所以时间复杂度为 $O(n\log n)$。

参考代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
    
}
const int N=2.5e5+10;
int n,x[N],y[N],m[N],p[N],r[N],d[N],tp[N];
bool vis[N];
vector<ll>lsh;
inline ll dis(int i,int j){
	return 1ll*(x[i]-x[j])*(x[i]-x[j])+1ll*(y[i]-y[j])*(y[i]-y[j]);
}
inline bool cmp(int i,int j){
	return m[i]<m[j];
}
queue<int>q;
struct Segment_Tree{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	int id[N<<2];
	vector<int>vec[N<<2];
	inline void ins(int rt,int l,int r,int p,int v){
		vec[rt].push_back(v);
		if(l==r) return ;
		int mid=l+r>>1;
		if(p<=mid) ins(ls,l,mid,p,v);
		else ins(rs,mid+1,r,p,v);
	}
	inline void upd(int rt,int l,int r,int L,int R,int w){
		if(id[rt]==vec[rt].size()) return ;
		if(L<=l&&r<=R){
			while(id[rt]<vec[rt].size()&&m[vec[rt][id[rt]]]<=w){
				if(!vis[vec[rt][id[rt]]]) q.push(vec[rt][id[rt]]),vis[vec[rt][id[rt]]]=1;
				id[rt]++;
			}
			return ;
		}
		int mid=l+r>>1;
		if(L<=mid) upd(ls,l,mid,L,R,w);
		if(R>mid) upd(rs,mid+1,r,L,R,w);
	}
}T;
int main(){
	x[0]=read(),y[0]=read(),p[0]=read(),r[0]=read();
	n=read();
	lsh.push_back(0);
	for(int i=1;i<=n;i++)
		x[i]=read(),y[i]=read(),m[i]=read(),p[i]=read(),r[i]=read(),
		lsh.push_back(dis(0,i)),tp[i]=i;
	sort(lsh.begin(),lsh.end());
	lsh.erase(unique(lsh.begin(),lsh.end()),lsh.end());
	int c=lsh.size()-1; 
	for(int i=0;i<=n;i++)
		d[i]=lower_bound(lsh.begin(),lsh.end(),dis(0,i))-lsh.begin(),
		r[i]=upper_bound(lsh.begin(),lsh.end(),1ll*r[i]*r[i])-lsh.begin()-1;
	sort(tp+1,tp+n+1,cmp);
	for(int i=1;i<=n;i++)
		T.ins(1,1,c,d[tp[i]],tp[i]);
	q.push(0);
	while(!q.empty()){
		int x=q.front();
		q.pop();
		T.upd(1,1,c,1,r[x],p[x]);
	}
	int ans=0;
	for(int i=1;i<=n;i++)
		ans+=vis[i];
	write(ans);
	flush();
}
```
