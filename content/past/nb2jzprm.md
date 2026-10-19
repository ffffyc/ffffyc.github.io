---
title: "题解：P10698 [SNCPC2024] 最大流"
date: 2024-08-15
category: "题解"
summary: "Link 题意 给定一个 n 个点 m 条边的单位网络，保证该网络不存在环。给定一个常数 k，设从 1 到 i 的最大流为 fi，对 i∈[2,n] 求出 min(fi,k)。"
math: true
top: 2
source: https://www.luogu.com.cn/article/nb2jzprm
slug: nb2jzprm
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10698)
## 题意

给定一个 $n$ 个点 $m$ 条边的单位网络，保证该网络不存在环。给定一个常数 $k$，设从 $1$ 到 $i$ 的最大流为 $f_i$，对 $\forall i\in[2,n]$ 求出 $\min(f_i,k)$。

$n\le 10^5$，$m\le 2\times10^5$，$k\le\min(n-1,50)$。
## 思路

不相交路径，考虑 LGV 引理。但此处不相交路径只要求边不相交，于是我们把边看成点，每个点的所有入边向所有出边连边，这样边不相交便转化为了点不相交。

从 [P9041](https://www.luogu.com.cn/problem/P9041) 我们了解到，该问题的解法为给每条边随机赋上 $[0,P)$ 的权值，则起点集合 $s_{1\dots x}$ 到终点集合 $t_{1\dots y}$ 的答案就是矩阵 $e_{s_i,t_j}(i\in[1,x],j\in[1,y])$ 的秩。

我们现在需要解决两个问题：
1. 起点集合（即 $1$ 的所有出边）可能很大。我们新建源点 $s$ 和 $k$ 个虚点 $p_{1\dots k}$，连边 $s\to p_i,p_i\to t$ 即可，其中 $t$ 为 $1$ 的任意出点。于是起点集合的大小被我们减小到了 $O(k)$。
2. 如果一个点的入度出度均较大，那么这个点的入边出边之间的边数会很大。注意到这些边都会随机赋一个权，相当于每个出边对应的向量为所有入边对应的向量的随机线性组合。于是对于入边，我们只需要保留线性无关的不超过 $k$ 组向量即可，这个任务可以交给线性基解决。

总时间复杂度 $O((n+m)k^2)$。

参考代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
    
}
namespace rad{
    mt19937_64 R(chrono::system_clock::now().time_since_epoch().count());
    inline int Rand(int l,int r){
        uniform_int_distribution<int> distribution(l,r);
        return distribution(R);
    }
}using namespace rad;
const int N=1e5+10,K=50+2,mod=1e9+9;
namespace PolyC{
    #define Poly vector<int>
    inline int qpow(int x,int y){
        int res=1;
        while(y){
            if(y&1) res=1ll*res*x%mod;
            x=1ll*x*x%mod;
            y>>=1;
        }
        return res;
    }
    inline int add(int a,int b){
        return a+b>=mod?a+b-mod:a+b;
    }
    inline int dec(int a,int b){
        return a>=b?a-b:a+mod-b;
    }
    inline Poly operator+(const Poly &a,const Poly &b){
        Poly F=a;
        F.resize(max(a.size(),b.size()));
        for(int i=0;i<b.size();i++)
            F[i]=add(F[i],b[i]);
        return F;
    }
    inline Poly operator-(const Poly &a,const Poly &b){
        Poly F=a;
        F.resize(max(a.size(),b.size()));
        for(int i=0;i<b.size();i++)
            F[i]=dec(F[i],b[i]);
        return F;
    }
    inline Poly operator*(const Poly &a,const int &b){
        Poly F=a;
        for(int i=0;i<F.size();i++)
            F[i]=1ll*F[i]*b%mod;
        return F;
    }
}
using namespace PolyC;
int n,m,k,d[N];
Poly ct[N];
vector<int>a[N];
struct LnB{
	int c;
    bool vs[K];
    Poly v[K];
    inline void ins(Poly vt){
        for(int i=0;i<k;i++){
            if(!vt[i]) continue;
            if(!vs[i]){
                vs[i]=1,v[i]=vt,c++;
                return ;
            }else{
                int b=1ll*qpow(v[i][i],mod-2)*vt[i]%mod;
                vt=vt-v[i]*b;
            }
        }
    }
}L[N];
inline void bfs(){
    queue<int>q;
    for(int t:a[1]){
    	Poly X(k,0);
    	for(int i=0;i<k;i++)
    		X[i]=Rand(1,mod-1);
    	L[t].ins(X),d[t]--;
	}
    for(int i=2;i<=n;i++)
        if(!d[i])
            q.push(i);
    while(!q.empty()){
        int x=q.front();
        q.pop();
        vector<Poly>vc;
        for(int i=0;i<k;i++)
        	if(L[x].vs[i])
        		vc.push_back(L[x].v[i]);
        for(auto t:a[x]){
            Poly X(k,0);
            for(auto I:vc)
            	X=X+I*Rand(1,mod-1);
            L[t].ins(X);
            if(!--d[t]) q.push(t);
        }
    }
}
int main(){
    n=read(),m=read(),k=read();
    for(int i=1;i<=m;i++){
        int u=read(),v=read();
        a[u].push_back(v),d[v]++;
    }
    for(int i=1;i<=n;i++)
        ct[i].resize(k);
    bfs();
    for(int i=2;i<=n;i++)
        write(L[i].c),putc(' ');
	flush();
}
```
