---
title: "题解：[广东省队集训 2025] 小方的疑惑"
date: 2025-04-29
category: "题解"
summary: "[[广东省队集训 2025] 小方的疑惑](http://8.138.223.198/p/23) 给你一棵 n 个结点的有根树，点带有点权 ai。若一个非叶子结点的权值大于 0"
math: true
top: 2
source: https://www.luogu.com.cn/article/nghpdk02
slug: nghpdk02
---

### [[广东省队集训 2025] 小方的疑惑](http://8.138.223.198/p/23)

给你一棵 $n$ 个结点的有根树，点带有点权 $a_i$。若一个非叶子结点的权值大于 $0$，则可以将其权值减一并选择其一个儿子将其权值加一。问若干次操作后可生成的序列 $a_{1\sim n}$ 数量。

答案对 $10^9+7$ 取模。

$n\le 8000$。
****
考虑一个暴力 DP：设 $f_{i,j}$ 表示子树 $i$ 的点权和为 $j$ 的方案数，充要条件只有 $j$ 不小于子树 $i$ 原本的点权和且总点权和不变。合并子树需要进行卷积，而加入 $i$ 为将 $f_{i,j}$ 向左平移 $a_i$ 位并舍去溢出至负数部分，再做一遍前缀和。

注意到 $f_{i,j}$ 为一个 $sz_i$ 次多项式，考虑维护点值，瓶颈在于点值平移。为了避免对每个点做点值平移，考虑维护点值平移标记，但此时卷积又不好做了。

考虑维护 $f(x)=\sum_i c_i\binom{x+i+t}{i}$，其中 $t$ 为需要平移的位数。此时对多项式做前缀和有：

$$\sum_{x'=0}^x\binom{x'+i+t}{i}=\binom{x+i+t+1}{i+1}-\binom{i+t}{i+1}$$

对多项式做点值平移有：

$$\binom{x+i+1}{i}=\sum_{j=0}^i\binom{x+j}{j}$$
$$\binom{x+i+t}{i}=\sum_{j=0}^i\binom{x+j}{j}\binom{t+i-j-1}{i-j}$$

故我们做到了 $O(\deg)$ 前缀和和 $O(\deg^2)$ 点值平移。这样维护系数的好处是将多项式乘上 $\binom{x+k}{k}$ 相当于将多项式做 $k$ 次前缀和，于是我们可以在其中一个多项式带有点值平移标记的情况下完成 $O(\deg_1\cdot \deg_2)$ 的多项式乘法。

合并 $f_1(x),f_2(x)$ 时，不妨令 $\deg_1\le \deg_2$，将 $f_1(x)$ 的点值平移标记清空再进行卷积，时间复杂度 $O(\deg_1\cdot(\deg_1+\deg_2))$，由树形背包复杂度分析得知其为 $O(n^2)$。

```cpp
int tag[N];
Poly F[N];
inline void Pres(Poly &a,int d){
	int n=a.size(),s=0;
	for(int i=0,v=1;i<n;i++){
		v=1ll*v*(d+i)%mod*inv[i+1]%mod;
		s=dec(s,1ll*a[i]*v%mod);
	}
	a.insert(a.begin(),s);
}
inline void Move(Poly &a,int &d){
	if(!d) return ;
	int n=a.size();
	Poly F(n,0);
	for(int i=0,v=1;i<n;i++)
		F[i]=v,v=1ll*v*(d+i)%mod*inv[i+1]%mod;
	for(int i=0;i<n;i++)
		for(int j=1;i+j<n;j++)
			inc(a[i],1ll*a[i+j]*F[j]%mod);
	d=0;
}
inline void Mult(Poly &a,Poly &b,int &ad,int &bd){
	int n=a.size(),m=b.size();
	if(n<m) swap(n,m),swap(a,b),swap(ad,bd);
	Move(b,bd);
	Poly c(n+m-1,0);
	for(int i=0;i<m;i++){
		for(int j=0;j<n+i;j++)
			inc(c[j],1ll*a[j]*b[i]%mod);
		Pres(a,ad);
	}
	a=c;
}
inline void dfs(int x){
    for(auto t:a[x])
        dfs(t);
    F[x]=(Poly){1};
    for(auto t:a[x])
    	Mult(F[x],F[t],tag[x],tag[t]);
    inc(tag[x],v[x]);
	Pres(F[x],tag[x]);
}
```
****
另附一个比较有意义的组合意义 $64$ 分做法。

将所有位置分为三类：操作后 $a_i$ 变小/不变/变大。可以贪心地给每一种结果赋予一个操作顺序，比如按照 DFS 序处理所有变大的位置，找到其最近的还需变小的祖先进行操作。

设 $f_{i,j}$ 表示子树 $i$ 内还有 $j$ 个点需要变大。转移时先将子树的 DP 数组卷起来再考虑 $i$ 的贡献，设卷积结果为 $g_{0\sim sz_i}$。

若 $i$ 被选作变小，则枚举 $k$ 表示 $a_i$ 分给了 $k$ 个位置。那么有：
$$f_{i,j},f_{i,j+1}\gets\sum_{k\ge 1}\binom{a_i}{k}g_{j+k}$$

这是因为我们是贪心地操作，前 $k-1$ 个位置都必须不再变大，而第 $k$ 个位置可选取是否继续变大。

若 $i$ 被选作不变或变大可以简单转移，分别是将 $f_{i,j}$ 加上 $g_j$ 和 $g_{j-1}$。

时间复杂度 $O(n^3)$。

```cpp
inline void dfs(int x){
    for(auto t:a[x])
        dfs(t);
    siz[x]=0,g[0]=1;
    for(int i=1;i<=n;i++)
        g[i]=0;
    for(auto t:a[x]){
        for(int i=0;i<=siz[x];i++)
            for(int j=0;j<=siz[t];j++)
                inc(tp[i+j],1ll*g[i]*f[t][j]%mod);
        siz[x]+=siz[t];
        for(int i=0;i<=siz[x];i++)
            g[i]=tp[i],tp[i]=0;
    }
    siz[x]++;
    for(int j=0,v=1;j<=siz[x];j++)
        c[j]=1ll*v*ifac[j]%mod,v=1ll*v*(::v[x]-j)%mod;
    for(int i=0;i<=siz[x];i++)
        f[x][i]=g[i];
    for(int i=1;i<=siz[x];i++)
        inc(f[x][i],g[i-1]);
    for(int i=0;i<=siz[x];i++)
        for(int j=1;i+j<=siz[x]&&j<=v[x];j++)
            inc(f[x][i],1ll*g[i+j]*c[j]%mod),
            inc(f[x][i+1],1ll*g[i+j]*c[j]%mod);
}
```
