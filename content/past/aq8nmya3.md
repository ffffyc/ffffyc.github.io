---
title: "题解 【01序列 - Extra】"
date: 2021-03-01
category: "题解"
summary: "n≤106,m≤2.3×107 很显然我们在这里已经给出了 O(nlog n+m) 的正解，这里不多讲，先给个 std cpp include using namespace "
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/aq8nmya3
slug: aq8nmya3
---

$n\le10^6,m\le2.3\times10^7$

很显然我们在[这里](https://www.luogu.com.cn/blog/cyffff/ti-xie-t1-01-xu-lie-post)已经给出了 $O(n\log n+m)$ 的正解，这里不多讲，先给个 $std$
```cpp
#include<bits/stdc++.h>
using namespace std;
const int N=1e6+10;
int n,m,st[20][N],lg[N],a[N],pre[N],pp[N];
inline int query(int l,int r){
	int q=lg[r-l+1];
	return max(st[q][l],st[q][r-(1<<q)+1]);
}
int main(){
    n=read(),m=read();
    for(int i=1;i<=n;i++){
    	a[i]=read();
	}
	a[0]=2;
	int sum=0,o=0,z=0;
	for(int i=1;i<=n;i++){
		if(a[i]) sum--,o++;
		else sum++,z++;
		st[0][i]=z-o;
		pp[i]=o;
		pre[i]=pre[i-1]+(a[i]==1&&a[i-1]==0);
	}
	for(int i=2;i<=n;i++){
	    lg[i]=lg[i>>1]+1;
	}
	int ln=lg[n];
	for(int i=1;i<=ln;i++){
		for(int j=1;j+(1<<i)-1<=n;j++){
			st[i][j]=max(st[i-1][j],st[i-1][j+(1<<i-1)]);
		}
	}
	unsigned seed=read();
	srand(seed),init(n);
	long long ans=0;
	for(int i=1;i<=m;i++){
		int opt=readopt(),l=readrange(),r=readrange();if(l>r)swap(l,r);
		if(opt==1){
			int asns=query(l,r);
			ans^=1ll*i*max(pp[r]-pp[l-1],asns-(l-1-pp[l-1])+pp[r]);
		}else{
			ans^=1ll*i*(1+!(pre[l]==pre[r]));
		}
	}
	printf("%lld",ans);
    return 0;
}
```
那这篇题解讲什么呢？

### 《暴力是怎样炼成的》
没错这道题还是能被 $\texttt{35}$ 极强的暴力过的呢

#### $\to0pts$
$O(nm)$ 想得分？
#### $\to4pts$
第一问我们没有什么玄妙的做法，于是我们只考虑乱搞第二问。

我们发现只要 $[l,r]$ 中最后一个 $1$ 前有 $0$ 即可，这可以用前缀和判断.

于是有了朴素 $O(n\log n+m\log n)$ 暴力倍增找到最后一个 $1$。

二分似乎能得很高分（？
#### $\to88pts$
~~没错跨度就这么大~~

这时我们发现倍增 $1$ 的时候可以顺便判前面是否有 $0$。
#### $\to 96pts$
我们发现序列里全是 $1$ 的数据居然能把我们卡满！

于是特判，如果区间全为 $0$ 或 $1$ 直接返回。

还可以发现区间较小时可以把我们的复杂度卡得比较满，于是可以设立分界点，小范围 $O(n)$ 暴力，大范围 $O(\log n)$ 倍增。
#### $\to 100pts$
将 $\texttt{ST}$表 数组调整后可以使访问更加连续，成功吊打std。

最后给出暴力代码:
```cpp
#include<bits/stdc++.h>
using namespace std;
int pre[1000005];
int st[20][1000005];
bool a[1000005];
int ask(int l,int r)
{
	int k=log2(r-l+1);
	return max(st[k][l],st[k][r-(1<<k)+1]);
}
int u[1000005];
int ct;
int ll;
int ask2(int l,int r)
{
	if(pre[r]-pre[l-1]==0||pre[r]-pre[l-1]==r-l+1) return 1;
	int i,w=0,s=pre[l-1];
	if(r-l<7)
	{
		bool fl=0;
		for(;l<=r;l++)
			if(a[l]==0)
				fl=1;
			else if(fl)
				return 2;
		return 1;
	}
	for(i=1<<ll;i>=1;i>>=1)
		if(w+i<=ct&&u[w+i]<=r)
		{
			w+=i;
			if(pre[u[w]]-s<u[w]-l+1) return 2;
		}	
	return 1;
}
int main()
{
	int n=read(),m=read(),i,j,opt,l,r,x,seed,lll;
	long long s=0;
	for(i=1;i<=n;i++)
	{
		a[i]=read(),pre[i]=pre[i-1]+a[i],st[0][i]=i-pre[i]*2;
		if(a[i]==1)
			u[++ct]=i;
	}
	ll=log2(ct);
	lll=log2(n);	
	for(j=1;j<=lll;j++)
		for(i=1;i+(1<<j)-1<=n;i++)
			st[j][i]=max(st[j-1][i],st[j-1][i+(1<<j-1)]);
	seed=read();
	srand(seed);init(n);
	for(i=1;i<=m;i++)
	{
		opt=readopt();l=readrange();r=readrange();if(l>r)swap(l,r);
		if(opt==1) s^=1ll*i*max(ask(l,r)-(l-1-pre[l-1])+pre[r],pre[r]-pre[l-1]);
		else s^=1ll*i*ask2(l,r);
	}
	cout<<s;
}
```
暴力碾标算
