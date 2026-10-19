---
title: "题解：[广东省队集训 2025] 异或症测试 3"
date: 2025-04-22
category: "题解"
summary: "[[广东省队集训 2025] 异或症测试 3](http://8.138.223.198/p/10) 给你一个大小为 n 的集合 B 和一个整数 X，你要求出有多少个非空集合 "
math: true
top: 2
source: https://www.luogu.com.cn/article/qeaxqt3r
slug: qeaxqt3r
---

### [[广东省队集训 2025] 异或症测试 3](http://8.138.223.198/p/10)

给你一个大小为 $n$ 的集合 $B$ 和一个整数 $X$，你要求出有多少个非空集合 $S\sube\{1,2,\dots,X\}$ 使得 $B$ 是 $S$ 的线性基。其中 $B$ 中的所有元素与 $X$ 均为 $m$ 位二进制数。

答案对 $998244353$ 取模。

$n,m\le 2000$。
****

写一个详细一点的官方做法。

定义标准基为一组线性基使得没有任何一个数包含另一个数的最高位。对标准基进行计数即可不重复计数同一组基。

由于能异或出的每个数均被基内的数唯一表示，将基内的数重编号为 $1\sim n$，将每个可异或出的数重编号为其对应的异或方案，问题转化为求 $[1,x]$ 有多少子集对应的基大小为 $n$，其中的 $x$ 可贪心求解。
****
不妨考虑 $x=2^n-1$ 的部分分。总方案数为 $2^{2^n-1}$，但是其中可能有一些方案基的大小不为 $n$。设 $f_i$ 表示 $[1,2^i)$ 有多少子集的线性基大小为 $i$，$g_{i,j}$ 表示 $[1,2^i)$ 中有多少线性基大小为 $j$。不妨考虑从高往低填基内每一位，有：

$$g_{i,j}=g_{i-1,j-1}+2^j\cdot g_{i-1,j}$$

前者表示这一位有数，后者表示这一位无数。由于计数的是标准基，故有数的情况下这一位其它数不能有值。简单容斥得到：

$$f_i=2^{2^i-1}-\sum_{j=0}^{i-1}f_jg_{i,j}$$
****
接下来的难点在于求出所有大小为 $i$ 的线性基 $B$ 的 $\sum 2^{\text{cnt}(B)}$，其中 $\text{cnt}(B)$ 为 $B$ 能异或出多少 $[1,x]$ 内的数。

考虑一个好一点的计算 $\text{cnt}(B)$ 的方法：从高至低枚举每一个有值的位，若当前数异或上这一位的值 $\le x$，那么就将当前数异或上这一位的值且将 $\text{cnt}(B)$ 加上 $2^c$，其中 $c$ 为 $B$ 在这一位之后还有多少位有值。

设计一个数位 DP，由于我们需要低于当前位有多少位有值但我们又只能由高至低位进行 DP，不妨设计状态 $f_{i,j,0/1}$ 表示当前考虑到第 $i$ 位，当前数是否顶到上界，钦定此后还有 $j$ 位有值的贡献。

判定当前数可以异或这一位的值可能需要这一位的值在低位的信息。如果出现了这种情况那么必定可选之后的位，为该情况新建一个状态。

同时遇见一个无值的位需要知道之前是否有选取成功任何一位，但由于必定有 $x\ge 2^{n-1}$，我们只需要特殊转移 $f_{n,*,1}$ 即可。

最后的容斥只需从部分分的容斥方法稍作更改即可。

总时间复杂度为 $O(n^3/w)$，瓶颈为处理线性基。

```cpp
const int N=2e3+10,mod=998244353,i2=mod+1>>1;
inline int add(int x,int y){ return x+y>=mod?x+y-mod:x+y; }
inline int dec(int x,int y){ return x>=y?x-y:x-y+mod; }
inline void inc(int &x,int y){ x=add(x,y); }
inline int qpow(int x,int y){
	int res=1;
	while(y){
		if(y&1) res=1ll*res*x%mod;
		x=1ll*x*x%mod;
		y>>=1;
	}
	return res;
}
using bit=bitset<N>;
int n,m,f[N][N],dp[N][N][3],id[N],rid[N],g[N],pw[N],pw2[N],ppw[N];
bit A[N],X;
bool vis[N];
inline bool ins(bit x){
    for(int i=m;i;i--){
        if(!x[i]) continue;
        if(!vis[i]){ vis[i]=1,A[i]=x;return 1; }
        x^=A[i];
    }
    return 0;
}
int main(){
    freopen("basis.in","r",stdin);
    freopen("basis.out","w",stdout);
    n=read(),m=read();
    for(int i=1;i<=n;i++){
        bit tp;
        for(int j=m;j;j--)
            tp[j]=getc()-'0';
        if(!ins(tp)) return puts("0"),0;
    }
    for(int i=m;i;i--)
        X[i]=getc()-'0';
    for(int i=1;i<=m;i++)
        for(int j=i+1;j<=m;j++)
            if(vis[i]&&vis[j]&&A[j][i])
                A[j]^=A[i];
    for(int i=1,j=0;i<=m;i++)
    	if(vis[i])
    		j++,id[i]=j,rid[j]=i;
    for(int i=m;i;i--){
    	if(vis[i]) break;
    	if(X[i]) return puts("0"),0;
	}
	bit tp,xp;
	for(int i=n;i;i--){
		bit x=tp^A[rid[i]];
		bool fl=0;
		for(int j=m;j&&!fl;j--){
			if(j<rid[i]&&x[j]&&vis[j]) x^=A[j];
			if(x[j]&&!X[j]) fl=1;
			if(!x[j]&&X[j]) break;
		}
		if(!fl) tp^=A[rid[i]],xp[i]=1;
	}
	X=xp;
	if(!X[n]) return puts("0"),0;
    pw[0]=pw2[0]=1;
    for(int i=1;i<=n;i++)
        pw[i]=2ll*pw[i-1]%mod,
        pw2[i]=2ll*pw2[i-1]%(mod-1);
    for(int i=0;i<=n;i++)
    	ppw[i]=qpow(2,pw2[i]);
    dp[0][0][0]=dp[0][0][1]=1;
    for(int i=1;i<=n;i++){
    	for(int j=0;j<=i;j++){
    		dp[i][j][0]=dp[i-1][j][0];
    		if(i==n) dp[i][j][1]=dp[i-1][j][0]; 
    		else if(X[i]) dp[i][j][1]=1ll*i2*add(dp[i-1][j][0],dp[i-1][j][1])%mod;
			else dp[i][j][1]=1ll*i2*dp[i-1][j][1]%mod; 
			if(!X[i]) dp[i][j][2]=add(dp[i-1][j][2],1ll*dp[i-1][j][0]*pw[i-j-1]%mod);
			else dp[i][j][2]=dp[i-1][j][2];
    		if(j){
    			inc(dp[i][j][0],1ll*dp[i-1][j-1][0]*ppw[j-1]%mod*pw[i-j]%mod);
    			if(X[i]) inc(dp[i][j][1],add(dp[i-1][j-1][2],1ll*dp[i-1][j-1][1]*ppw[j-1]%mod*pw[i-j]%mod));
    			else inc(dp[i][j][1],1ll*dp[i-1][j-1][1]*pw[i-j]%mod);
    			if(!X[i]) inc(dp[i][j][2],1ll*dp[i-1][j-1][2]*ppw[j-1]%mod*pw[i-j]%mod);
			}
		}
	}
    f[0][0]=1;
    for(int i=1;i<=n;i++)
        for(int j=0;j<=n;j++){
            f[i][j]=1ll*pw[j]*f[i-1][j]%mod;
            if(j) inc(f[i][j],f[i-1][j-1]);
        }
    for(int i=0;i<=n;i++){
        g[i]=1ll*dp[n][i][1]*qpow(f[n][i],mod-2)%mod;
        for(int j=0;j<i;j++)
	        g[i]=dec(g[i],1ll*f[i][j]*g[j]%mod);
    }
    write(g[n]);
}
```
