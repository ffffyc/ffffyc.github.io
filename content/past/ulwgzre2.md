---
title: "2021.7.8 模拟赛"
date: 2021-07-08
category: "个人记录"
tags: ["杂项"]
summary: "现在在打，很慌。 写完了 T1T3T4，T2 一眼 Tarjan，不会（ 打算写个 O(n2) 骗点分。 但是不给部分分数据范围是什么啊！！ 没有部分分数据范围！！！ O(n2"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/ulwgzre2
slug: ulwgzre2
---

现在在打，很慌。

写完了 T1T3T4，T2 一眼 $\text{Tarjan}$，不会（

打算写个 $O(n^2)$ 骗点分。

但是不给部分分数据范围是什么啊！！

没有部分分数据范围！！！

$O(n^2)$ 也不会了/wq

自我安慰：有 $m=0$ 的点。

期望 $100+0+100+100=300$

和 $\text{panshuo}$ 讨论了一下：$\text{Tarjan}$ 找环缩点+点分治+组合数+特判，胡出来了但根本不想写

噫！$m=0$ 有 $30$ 分！

$100+30+100+100=330=rk2$。

居然还有样例和 $m=1$ 的点！我居然没写！

大亏。

第一是 $100+50+100+100=350$。
### 题解
#### Problem  A 简单的数学题
即 [$\text{P7593}$](https://www.luogu.com.cn/problem/P7593)，过水不讲。
```cpp
#include<bits/stdc++.h> 
using namespace std;
#define ll long long
ll n,k,s,t,m;
int main(){
	t=read();
	while(t--){
		n=read(),k=read(),s=read();
		if(k==1){
			if(s>n){
				puts("No");
			}else{
				puts("Yes");
			}
			continue;
		}
		m=n*(n+1)/2-(n-k)*(n-k+1)/2;
		if(s>m){
			puts("No");
			continue;
		}
		if(k*(k+1)/2>s){
			puts("No");
		}else{
			puts("Yes");
		}
	}
    return 0;
}
```
#### Problem  B 游戏
暂时不会，等会了再补。
#### Problem  C 玩具装箱
$dp_n$ 代表以 $n$ 作为一个箱子结尾时最少的代价。

$$dp_i=\max_{j=\max(i-m+1,1)}^{i}(dp_{i-1}+k+(i-j+1)\times(\max_{k=j}^i(a_k)-\min_{k=j}^i(a_k)))$$

$O(nm)$ 即可。
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int N=2e4+10,M=1e3+10;
int n,m,a[N],k,st1[16][N],st2[16][N],lg[N];
ll dp[N];
inline pair<int,int> query(int l,int r){
	int x=lg[r-l+1];
	return make_pair(min(st1[x][l],st1[x][r-(1<<x)+1]),max(st2[x][l],st2[x][r-(1<<x)+1]));
}
int main(){
	n=read(),m=read(),k=read();
	lg[0]=-1;
	for(int i=1;i<=n;i++)
		st1[0][i]=st2[0][i]=read(),lg[i]=lg[i>>1]+1;
	for(int i=1;i<=15;i++){
		for(int j=1;j+(1<<i)-1<=n;j++){
			st1[i][j]=min(st1[i-1][j],st1[i-1][j+(1<<i-1)]);
			st2[i][j]=max(st2[i-1][j],st2[i-1][j+(1<<i-1)]);
		}
	}
	memset(dp,127,sizeof(dp));
	dp[0]=0;
	for(int i=1;i<=n;i++){
		for(int j=max(i-m+1,1);j<=i;j++){
			pair<int,int>a=query(j,i);
			dp[i]=min(dp[i],dp[j-1]+k+1ll*(i-j+1)*(a.second-a.first));
		}
	}
	printf("%lld",dp[n]);
}
```
#### Problem  D 异象石
结论题，和 [$\text{P3320}$](https://www.luogu.com.cn/problem/P3320) 差不多。

结论：答案 = 所有询问点按照 $\text{dfs}$ 排序后相邻之间的距离之和 $/2$（$1,n$ 相邻）.

不会证。

之前做过这题就 $A$ 了。

拿个 $\text{set}$ 存 $\text{dfn}$，每次加删点直接在 $\text{set}$ 中找到相邻点，然后把距离调整即可。

注意要开 $\text{long long}$

```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int N=5e5+10;
int head[N],cnt,n,m;
ll cur;
#define sit set<int>::iterator
set<int>ds;
sit IT;
struct Edge{
	int to,nxt,val;
}a[N<<1];
inline void add(int u,int v,int w){
	cnt++;
	a[cnt].to=v;
	a[cnt].nxt=head[u];
	a[cnt].val=w;
	head[u]=cnt;
}
int dep[N],ind[N],lg[N],tim,dfn[N],idfn[N];
ll diss[N];
struct ST_table{
	int cnt,st[20][N];
	inline void dfs(int rt,int f=0,int de=0,ll summ=0){
		dep[rt]=de;
		diss[rt]=summ; 
		st[0][++cnt]=rt;
		ind[rt]=cnt;
		idfn[dfn[rt]=++tim]=rt;
		for(int i=head[rt];i;i=a[i].nxt){
			int t=a[i].to;
			if(t!=f){
				dfs(t,rt,de+1,summ+a[i].val);
				st[0][++cnt]=rt;
			}
		}
	}
	inline int cmp(int x,int y){
		return dep[x]<dep[y]?x:y;
	}
	inline void init(){
		dfs(1);
		for(int i=1;(1<<i)<=cnt;i++) {
	        for(int j=1;j+(1<<i)-1<=cnt;j++) {
	            st[i][j]=cmp(st[i-1][j],st[i-1][j+(1<<i-1)]);
	        }
	    }
	    for(int i=2;i<=cnt;i++){
	    	lg[i]=lg[i>>1]+1;
		}
	}
	inline int LCA(int x,int y){
		x=ind[x],y=ind[y];
		if(x>y) swap(x,y);
		int i=lg[y-x+1];
		int p=1<<i;
		return cmp(st[i][x],st[i][y-p+1]);
	}
	inline ll dis(int x,int y){
		ll w=diss[x]+diss[y]-2*diss[LCA(x,y)];
		return w;
	}
}st;
int main(){
//	freopen("2.in","r",stdin);
//	freopen("2.out","w",stdout);
	n=read();
	for(int i=1;i<n;i++){
		int u=read(),v=read(),w=read();
		add(u,v,w);
		add(v,u,w);
	}
	st.init();
	m=read();
	while(m--){
		char opt=getc();
		if(opt=='?'){
			write(cur/2);
			putc('\n');
		}else{
			int x,y,a,b;
			x=dfn[y=read()];
			if(opt=='+') ds.insert(x);
			a=idfn[((IT=ds.lower_bound(x))==ds.begin()?*--ds.end():*--IT)];
			b=idfn[((IT=ds.upper_bound(x))==ds.end()?*ds.begin():*IT)];
			if(opt=='-') ds.erase(x);
			x=y;
			ll val=st.dis(a,x)+st.dis(b,x)-st.dis(a,b);
			if(opt=='+'){
				cur+=val;
			}else{
				cur-=val;
			}
		}
	}
	flush();
}
```
