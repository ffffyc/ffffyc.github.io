---
title: "题解：P12559 [UOI 2024] Zeroing the segment"
date: 2025-05-20
category: "题解"
summary: "Link 非常好数据结构，爱来自广东省集。 题意 给定一个长为 n 的正整数序列 a1 n。对于一个序列 b1 m： 初始有一常数 x=0； 你可以进行若干次操作，操作共有两种"
math: true
top: 2
source: https://www.luogu.com.cn/article/y2dtlife
slug: y2dtlife
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P12559)

非常好数据结构，爱来自广东省集。
## 题意

给定一个长为 $n$ 的正整数序列 $a_{1\sim n}$。对于一个序列 $b_{1\sim m}$：
- 初始有一常数 $x=0$；
- 你可以进行若干次操作，操作共有两种：
	- 令 $x\gets x+1$；
   - 选择 $1\le i\le m$，令 $b_i\gets b_i\oplus x$。
- 定义序列 $b_{1\sim m}$ 的权值为要使 $b_{1\sim m}$ 均变为 $0$ 所需的最小操作次数。

接下来有 $q$ 次询问，每次询问给出 $l,r$，求出 $a_{l\sim r}$ 的权值。强制在线。

$n,q\le 2\times 10^5$。
## 题解
由于 $x$ 必须达到区间中的数的最高位，可以发现每个数最多只需要操作两次。只考虑区间内含有最高位 $k$ 的数并统一减去 $2^k$，问题转化为求解 $\min(x+\sum [a_i>x])$。

将上式写作 $\max(\sum[a_i\le x]-x)$，**逆用 Hall 定理，将问题转化为二分图匹配问题**，左部点 $i$ 向右部点 $j\le a_i$ 连边，上式即为左部点失配点数。

由于所有左部点均向右部一个前缀连边，故可以以任意顺序贪心匹配，不妨按照 $r,r-1,\dots,l$ 的顺序进行匹配。

按右端点进行扫描线，扫到 $r$ 时，由于我们从右至左贪心匹配，故一定匹配 $r$。**使用 Hall 定理维护并判断是否可成功加入 $r$**，只需要判断是否满足 $\min(x-\sum[a_i\le x])\ge 0$ 即可。若不能直接匹配，则需要我们找到最左侧的匹配点 $l$ 使得删去 $l$ 后存在完美匹配。这只需要找到最小的 $x$ 使得 $(x-\sum [a_i\le x])< 0$，那么 $l$ 即为最小的满足 $a_l\le x$ 的位置。

上述操作均可使用线段树简单维护，而询问只需使用主席树维护矩形加单点求值。

精细实现可做到时间复杂度 $O((n+q)\log n)$。


```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int N=2e5+10,K=60+2,INF=1e9;
int n,k,q,t,lg[N],pw[65],rx[N],sp[N][K],cp[K],ct[K],pol[N],nx[N],rt[N][K];
ll a[N],b[N],las,st[19][N];
inline ll querymx(int l,int r){
    int t=__lg(r-l+1);
    return max(st[t][l],st[t][r-(1<<t)+1]);
}
struct Segment_Trees{
    #define ls (a[rt].lson)
    #define rs (a[rt].rson)
    struct node{
        int lson,rson,cnt;
    }a[N*20];
    int cnt;
    inline int copy(int x){
        int rt=++cnt;
        a[rt]=a[x];
        return rt;
    }
    inline void insert(int &rt,int l,int r,int p){
        rt=copy(rt),a[rt].cnt++;
        if(l==r) return ;
        int mid=l+r>>1;
        if(p<=mid) insert(ls,l,mid,p);
        else insert(rs,mid+1,r,p);
    }
    inline int query(int rt,int l,int r,int L,int R){
        if(!rt) return 0;
        if(L<=l&&r<=R) return a[rt].cnt;
        int mid=l+r>>1,ans=0;
        if(L<=mid) ans+=query(ls,l,mid,L,R);
        if(R>mid) ans+=query(rs,mid+1,r,L,R);
        return ans;
    }
}Ts;
struct Segment_Tree{
    #define ls (rt<<1)
    #define rs (rt<<1|1)
    int mn[N<<2],mnp[N<<2],tag[N<<2];
    inline void pushup(int rt){
        mn[rt]=min(mn[ls],mn[rs])+tag[rt];
        mnp[rt]=min(mnp[ls],mnp[rs]);
    }
    inline void pushtag(int rt,int v){
        tag[rt]+=v,mn[rt]+=v;
    }
    inline void build(int rt,int l,int r){
        if(l==r){ mn[rt]=rx[l],mnp[rt]=INF;return ; }
        int mid=l+r>>1;
        build(ls,l,mid),build(rs,mid+1,r);
        pushup(rt);
    }
    inline void modify(int rt,int l,int r,int p,int v){
        if(l==r){ mnp[rt]=v;return ; }
        int mid=l+r>>1;
        if(p<=mid) modify(ls,l,mid,p,v);
        else modify(rs,mid+1,r,p,v);
        pushup(rt);
    }
    inline void add(int rt,int l,int r,int L,int R,int v){
        if(L<=l&&r<=R) return pushtag(rt,v);
        int mid=l+r>>1;
        if(L<=mid) add(ls,l,mid,L,R,v);
        if(R>mid) add(rs,mid+1,r,L,R,v);
        pushup(rt);
    }
    inline int query1(int rt,int l,int r,int L,int R){
        if(L<=l&&r<=R) return mn[rt];
        int mid=l+r>>1,ans=INF;
        if(L<=mid) ans=min(ans,query1(ls,l,mid,L,R));
        if(R>mid) ans=min(ans,query1(rs,mid+1,r,L,R));
        return ans+tag[rt];
    }
    inline int query2(int rt,int l,int r,int L,int R){
        if(L<=l&&r<=R) return mnp[rt];
        int mid=l+r>>1,ans=INF;
        if(L<=mid) ans=min(ans,query2(ls,l,mid,L,R));
        if(R>mid) ans=min(ans,query2(rs,mid+1,r,L,R));
        return ans;
    }
    inline int find(int rt,int l,int r,int L,int R,int tg=0){
        if(l>R||r<L||mn[rt]+tg>=0) return -1;
        if(l==r) return l;
        tg+=tag[rt];
        int mid=l+r>>1,tp=find(ls,l,mid,L,R,tg);
        if(tp==-1) tp=find(rs,mid+1,r,L,R,tg);
        return tp;
    }
 }T;
vector<ll>vec;
ll ask(int l,int r){
    int t=__lg(querymx(l,r));
    return (1ll<<t)+(r-l+1)+(sp[r][t]-sp[l-1][t])-Ts.query(rt[r][t],1,n,l,r);
}
void init(int n,const vector<ll>&A){
    ::n=n;
    for(int i=1;i<=n;i++){
        a[i]=A[i-1],vec.push_back(a[i]);
        lg[i]=__lg(a[i]),k=max(k,lg[i]);
        b[i]=a[i]-(1ll<<lg[i]);
    }
    for(int i=1;i<=n;i++)
        st[0][i]=a[i];
    for(int i=1;i<=18;i++)
        for(int j=1;j+(1<<i)-1<=n;j++)
            st[i][j]=max(st[i-1][j],st[i-1][j+(1<<i-1)]);
    for(int i=1;i<=n;i++){
        for(int j=0;j<=k;j++)
            sp[i][j]=sp[i-1][j];
        sp[i][lg[i]]++;
    }
    for(int j=0;j<=k;j++)
        ct[j]=sp[n][j],cp[j]+=ct[j],cp[j+1]+=cp[j];
    for(int i=1;i<=n;i++)
        if(b[i]>=ct[lg[i]]) b[i]=-1;
        else b[i]=(lg[i]?cp[lg[i]-1]+1:1)+b[i];
    for(int i=0,p=0;i<=k;i++)
        for(int j=0;j<ct[i];j++)
            rx[++p]=j;
    T.build(1,1,n);
    for(int i=1;i<=n;i++)
        pol[i]=n+1;
    for(int i=n;i;i--)
        if(b[i]!=-1)
            nx[i]=pol[b[i]],pol[b[i]]=i;
    for(int i=1;i<=n;i++)
        pol[i]=0;
    for(int i=1;i<=n;i++){
        for(int j=0;j<=k;j++)
            rt[i][j]=rt[i-1][j];
        if(b[i]==-1) continue;
        int L=lg[i]?cp[lg[i]-1]+1:1,R=cp[lg[i]];
        T.add(1,1,n,b[i],R,-1);
        if(!pol[b[i]]) T.modify(1,1,n,b[i],i),pol[b[i]]=i;
        int mnp=T.find(1,1,n,L,R);
        if(mnp==-1) continue;
        int lp=T.query2(1,1,n,L,mnp);
        T.add(1,1,n,b[lp],R,1);
        int nxp=nx[pol[b[lp]]];
        if(nxp>i) pol[b[lp]]=0,T.modify(1,1,n,b[lp],INF);
        else pol[b[lp]]=nxp,T.modify(1,1,n,b[lp],nxp);
        Ts.insert(rt[i][lg[i]],1,n,lp);
    }
}
```
