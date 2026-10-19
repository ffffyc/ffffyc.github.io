---
title: "题解：P9041 [PA2021] Fiolki 2"
date: 2024-08-15
category: "题解"
summary: "Link 题意 给定一个 n 个点 m 条边的 DAG，定义 f(l,r) 表示最多选取多少条不相交路径 (si,ti) 满足 si∈[1,k],ti∈[l,r]，其中不能有任"
math: true
top: 2
source: https://www.luogu.com.cn/article/hdgex5pl
slug: hdgex5pl
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P9041)
## 题意

给定一个 $n$ 个点 $m$ 条边的 DAG，定义 $f(l,r)$ 表示最多选取多少条不相交路径 $(s_i,t_i)$ 满足 $s_i\in[1,k],t_i\in[l,r]$，其中不能有任意一点同时在两条选出的路径上。对 $\forall x\in[0,k)$ 求出有多少 $[l,r]\sube(k,n]$ 使得 $f(l,r)=x$。

$n\le 10^5$，$m\le 10^6$，$k\le\min(n-1,50)$。
## 思路

不相交路径，考虑 LGV 引理。

LGV 引理的内容是：指定起点 $s_{1\dots k}$ 和终点 $t_{1\dots k}$，令 $e_{i,j}$ 表示 $i\to j$ 的所有路径的边权乘积和，则 $\det(e_{s_i,t_j})$ 等于每个 $s_i\to t_{p_i}$ 的不相交路径组的权值和乘以 $(-1)^{\text{inv}(p)}$ 之和，其中 $p$ 是一个 $[1,k]$ 的排列；而我们需要解决的问题是：指定起点终点集合，从中任意匹配起点终点并要求存在匹配的起点终点之间的不相交路径，求最大匹配数。

注意到我们只需要判断存在性，我们可以指定一个大质数 $P=10^9+7$，给每条边随机赋上 $[0,P)$ 的权值，则 $f(l,r)$ 就等于矩阵 $e_{i,j}(i\in[1,k],j\in[l,r])$ 的秩，即 $e_{*,j}(j\in[l,r])$ 中最大可取出几组线性无关的向量，这个问题明显需要使用线性基解决。

我们可以使用拓扑排序求出我们需要的 $e_{i,j}$。扫描线扫右端点 $i$，对每个 $x\in[0,k)$ 求最大的 $l$ 使得 $f(l,i)=x$，扫描线加线性基有一个很经典的 trick：记录线性基内每个元素 $v_i$ 的加入时间 $t_i$，加入一个元素 $(v,t)$ 的时候，如果现在考虑到的位上 $i$ 的 $t_i<t$，则交换 $(v_i,t_i)$ 与 $(v,t)$。使用此 trick 便可解决本题。

总时间复杂度 $O(nk^2+mk)$。

参考代码：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
    
}
#define pii pair<int,int>
#define mpr make_pair
#define fir first
#define sec second
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
vector<pii>a[N];
inline void bfs(){
    queue<int>q;
    for(int i=1;i<=k;i++)
        ct[i][i-1]=1;
    for(int i=1;i<=n;i++)
        if(!d[i])
            q.push(i);
    while(!q.empty()){
        int x=q.front();
        q.pop();
        for(auto tp:a[x]){
            int t=tp.fir,w=tp.sec;
            ct[t]=ct[t]+ct[x]*w;
            if(!--d[t]) q.push(t);
        }
    }
    for(int i=1;i<=n;i++)
        assert(!d[i]);
}
struct LnB{
    int tim[K];
    Poly v[K];
    inline void ins(Poly vt,int t){
        for(int i=0;i<k;i++){
            if(!vt[i]) continue;
            if(!tim[i]){
                tim[i]=t,v[i]=vt;
                return ;
            }else{
                if(tim[i]<t) swap(tim[i],t),swap(v[i],vt);
                int b=1ll*qpow(v[i][i],mod-2)*vt[i]%mod;
                vt=vt-v[i]*b;
            }
            assert(!vt[i]);
        }
    }
}L;
ll ans[K];
int main(){
    n=read(),m=read(),k=read();
    for(int i=1;i<=m;i++){
        int u=read(),v=read();
        a[u].push_back(mpr(v,Rand(1,mod-1))),d[v]++;
    }
    for(int i=1;i<=n;i++)
        ct[i].resize(k);
    bfs();
    for(int i=k+1;i<=n;i++){
        L.ins(ct[i],i);
        vector<int>vec;
        for(int j=0;j<k;j++)
            if(L.tim[j])
                vec.push_back(L.tim[j]);
        vec.push_back(k),vec.push_back(i);
        sort(vec.begin(),vec.end(),greater<int>());
        for(int j=0;j+1<vec.size();j++)
            ans[j]+=vec[j]-vec[j+1];
    }
    for(int i=0;i<=k;i++)
        write(ans[i]),putc('\n');
	flush();
}
```
