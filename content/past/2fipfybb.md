---
title: "题解 【Wreck】"
date: 2021-05-10
category: "题解"
summary: "这是一个假题解。 题意 给你一个长为 n 的序列 a，有 m 次查询，每次查询 mini=lr (ai k) Subtask 1 1≤ n,m≤ 104,1≤ ai,k≤ 10"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/2fipfybb
slug: 2fipfybb
---

这是一个假题解。

## 题意
给你一个长为 $n$ 的序列 $a$，有 $m$ 次查询，每次查询

$$\min_{i=l}^r (a_i \bmod k)$$
## $\text{Subtask 1}$
$1\le n,m\le 10^4,1\le a_i,k\le 10^5$。

暴力枚举。

时间复杂度 $O(nm)$，期望得分 $3pts$。
## $\text{Subtask 2}$
$1\le n,m\le 10^5,1\le a_i,k\le 300$。

考虑对于所有 $k$ 一起处理询问，可以考虑分块，询问时先对 $k$ 取模后再求区间最小值。

时间复杂度 $O(nk)$，期望得分 $6pts$。结合 $\text{Subtask 1}$ 可得 $9pts$。
## $\text{Subtask 3}$
$1\le n,m\le 10^5,10^3\le a_i,k\le 10^5$。

考虑枚举 $i=jk,i<v,j\in\Bbb{N}$，则问题转化为单点修改区间后继问题，关于这个东西的实现可以去看 $\text{mcyl35}$ 的题解，这里用 $\text{zkw}$ 线段树实现。

时间复杂度 $O(\frac{nv}{k}\log n)$，期望得分 $10pts$。结合 $\text{Subtask 1}$ 可得 $13pts$。
## $\text{Subtask 4}$
$1\le n,m\le 10^5,1\le a_i,k\le 10^5$。

根号分治。

考虑设置阀值 $S$，对于 $k\le S$，使用 $\text{Subtask 2}$，$k>S$，使用 $\text{Subtask 3}$。

不难发现时间复杂度为 $O(nS+\frac{nv}S\log n)$，当 $S=\sqrt v$ 时时间复杂度平衡为 $O(n\sqrt v\log n)$，期望得分 $38pts$。
## $\text{Subtask 5}$
$1\le n,m\le 3\times10^5,1\le a_i,k\le 10^5$，数据随机。

可以沿用 $\text{Subtask 4}$ 的方法，时间复杂度 $O(n\sqrt v\log n)$，期望得分 $52pts$。

另外我们发现数据随机时，答案通常会比较小，可以考虑对答案乱搞，具体做法没想到，期望得分 $14pts$。
## $\text{Subtask 6}$
$1\le n,m\le 3\times10^5,10^3\le a_i,k\le 10^5$。

给根号分治第一档错的选手的安慰分。

期望得分 $54pts$。
## $\text{Subtask 7}$
$1\le n,m\le 3\times10^5,1\le a_i,k\le 10^5$。

使用更高级的区间后继写法，即分块套猫树。

时间复杂度 $O(n(\sqrt n+\sqrt v))$，空间复杂度 $O(n)$。

然后如果您 $\textcolor{#052242}{\text{MLE}}$ 了，你可能使用了 `queue` 存储询问，导致空间未清空，如果您 $\textcolor{#052242}{\text{TLE}}$ 了，你可能使用了前向星存储询问，常数过大，正解为使用 `vector` 存储，但在清空 `vector` 后一定要将此 `vector` 于局部定义的空 `vector` 进行 `swap`，否则~~清空了，但没完全清空~~ `vector` 的空间不会释放。

贴一下 `std` 吧：
```cpp
#include<bits/stdc++.h>
using namespace std;
int n,d2;
int read()
{
	int s=0;
	char ch=getchar();
	while(ch<'0'||ch>'9') ch=getchar();
	while(ch>='0'&&ch<='9') s=s*10+ch-'0',ch=getchar();
	return s;
}
const int mxn=3e5,mxv=1e5,sq=400;
pair<int,int> a[mxn+5];
struct ask
{
	int w,l,r,k;
};
vector<ask> t[mxn+5],f[sq+5];
int ans[mxn+5];
long long sum[sq+5];
int be[mxn+5];
int l[mxn+5],r[mxn+5];
int nxt[mxn+5],pre[mxn+5];
int pos[mxn*2+5];
int lg[mxn*4+5];
typedef unsigned u256 __attribute((vector_size(32)));//35为了卡常使用了指令集，但其实并没有效果
int mx[605];
int ne[mxn+5];
u256 ct[18][1100/8];
void build(const int mod)
{
	int i;
	memset(mx,127,sizeof(mx));
	for(i=1;i<=n;i++)
		ne[i]=a[i].first%mod,mx[be[i]]=min(mx[be[i]],ne[i]);
}
int simpleask(int pl,int pr)
{
	int ans=2e9,i;
	if(be[pl]==be[pr])
	{
		for(;pl<=pr;pl++)
			ans=min(ans,ne[pl]);
		return ans;
	}
	ans=min(simpleask(l[be[pr]],pr),simpleask(pl,r[be[pl]]));
	for(i=be[pl]+1;i<be[pr];i++)
		ans=min(ans,mx[i]);
	return ans;
}
int bl;
void getpos(int w,int l,int r)
{
	if(l==r) pos[l]=w;
	else
	{
		int mid=l+r>>1;
		getpos(w<<1,l,mid);
		getpos(w<<1|1,mid+1,r);
	}
}
void init()
{
	bl=500;
	int i,j,t=0;
	for(i=1;i<=n;i+=bl)
		l[++t]=i,r[t]=min(i+bl-1,n);
	for(d2=1;d2<t;d2<<=1);
	for(i=1;i<=t;i++)
		for(j=l[i];j<=r[i];j++)
			be[j]=i;
	getpos(1,1,d2);
	for(i=2;i<=d2*2;i++)
		lg[i]=lg[i/2]+1;
}
void add_cat(int l,int r,int d,int x,unsigned v)
{
	if(l==r) return;
	int mid=l+r>>1,i,L,R;
	u256 o=u256{v,v,v,v,v,v,v,v};
	u256 *t=ct[d];
	if(x<=mid)
	{
		L=l,R=x;
		if((L>>3)==(R>>3))
			for(i=L&7;i<=(R&7);i++)
				 t[L>>3][i]=v;
		else
		{
			for(i=L&7;i<=7;i++)
				t[L>>3][i]=v;
			for(i=0;i<=(R&7);i++)
        		t[R>>3][i]=v;
        	for(i=(L>>3)+1;i!=(R>>3);i++)
			    t[i]=o;
		}
		add_cat(l,mid,d+1,x,v);
	}
	else
	{
		L=x,R=r;
		if((L>>3)==(R>>3))
			for(i=L&7;i<=(R&7);i++)
				 t[L>>3][i]=v;
		else
		{
			for(i=L&7;i<=7;i++)
				t[L>>3][i]=v;
			for(i=0;i<=(R&7);i++)
        		t[R>>3][i]=v;
        	for(i=(L>>3)+1;i!=(R>>3);i++)
			    t[i]=o;
		}
		add_cat(mid+1,r,d+1,x,v);
	}
}
void add_bl(int x,int v)
{
	int b=be[x],i;
	for(i=x;i<=r[b];i++)
		pre[i]=v;
	for(i=x;i>=l[b];i--)
		nxt[i]=v;
	add_cat(1,d2,1,b,v);
}
int ask_cat(int pl,int pr)
{
	if(pl>pr) return 2e9;
	if(pl==pr) return pre[r[pl]];
	int d=lg[pos[pl]]-lg[pos[pl]^pos[pr]];
	return min(ct[d][pl>>3][pl&7],ct[d][pr>>3][pr&7]);
}
int ask_bl(int l,int r)
{
	return min(min(pre[r],nxt[l]),ask_cat(be[l]+1,be[r]-1));
}
int main()
{
	memset(ans,127,sizeof(ans));
	memset(ct,127,sizeof(ct));
	memset(pre,127,sizeof(pre));
	memset(nxt,127,sizeof(nxt));	
	n=read();
	int m=read(),i,j,mn;
	ask p;
	for(i=1;i<=n;i++)
		a[i]=make_pair(read(),i);
	init();
	for(i=1;i<=m;i++)
	{
		p.w=i,p.l=read(),p.r=read(),p.k=read();
		if(be[p.l]==be[p.r])
		{
			mn=2e9;
			for(;p.l<=p.r;p.l++)
				mn=min(mn,a[p.l].first%p.k);
			ans[i]=mn;
			continue;
		}
		if(p.k<=sq)
			f[p.k].push_back(p),sum[p.k]+=p.r-p.l+1;
		else
			t[mxv/p.k*p.k].push_back(p);
	}
	for(i=1;i<=sq;i++)
	{	
		if(sum[i]<=n)
		{
			while(f[i].size())
			{
				mn=2e9;
				p=f[i].back();
				f[i].pop_back();
				for(;p.l<=p.r;p.l++)
					mn=min(mn,a[p.l].first%i);
				ans[p.w]=mn;
			}
			continue;
		}
		build(i);
		while(f[i].size())
		{
			p=f[i].back();
			f[i].pop_back();
			ans[p.w]=simpleask(p.l,p.r);
		}
	}
	sort(a+1,a+1+n);
	j=n;
	for(i=mxv;i>=0;i--)
	{
		for(;j>=1&&a[j].first>=i;j--)
			add_bl(a[j].second,a[j].first);
		while(t[i].size())
		{
			p=t[i].back();
			t[i].pop_back();
			ans[p.w]=min(ans[p.w],ask_bl(p.l,p.r)-i);
			if(i)
				t[i-p.k].push_back(p);
		}
		vector<ask> qwq;
		swap(t[i],qwq);
	}
	for(i=1;i<=m;i++)
		printf("%d\n",ans[i]);
        return -1;
}
```
大概 std 最慢点 1.3s 左右，可能会有评测机波动。
