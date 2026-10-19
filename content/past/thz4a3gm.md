---
title: "题解 CF1553I【Stairs】"
date: 2023-10-29
category: "题解"
summary: "Link 题意 给定一个长度为 n 的排列 p。 令其中第 i 个位置的权值为 p 中最长的包含 i 的连续自然数按顺序组成的区间的长度。例如，p=[4,1,2,3,7,6,5"
math: true
top: 2
source: https://www.luogu.com.cn/article/thz4a3gm
slug: thz4a3gm
---

[$\text{Link}$](https://www.luogu.com.cn/problem/CF1553I)

# 题意
给定一个长度为 $n$ 的排列 $p$。

令其中第 $i$ 个位置的权值为 $p$ 中最长的包含 $i$ 的连续自然数按顺序组成的区间的长度。例如，$p=[4,1,2,3,7,6,5]$ 中，第 $6$ 个位置的权值为 $[5,7]$ 的长度，第 $2$ 个位置的权值为 $[2,4]$ 的长度。

将这些权值依次拼在一起，就得到了 $p$ 的「阶梯序列」。

给定 $a$，你需要求出存在多少个排列 $p$，使得 $a$ 为 $p$ 的「阶梯序列」。答案对 $998244353$ 取模。

$n\le 10^5$。
## 题解
考虑建立排列与阶梯序列之间的关系，注意到确定了阶梯序列就能确定排列“每一段的长度”，即阶梯序列是由若干段“$a_i$ 个连续的 $a_i$”组成的（否则无解），我们将连续的 $a_i$ 个 $a_i$ 缩成一个数，我们称缩成的序列为 $b_{1,\dots,m}$，则排列是由 $b_1$ 个连续自然数、$b_2$ 个连续自然数...组成的。

注意到相邻的两段不能缩成一段，难以限制，考虑容斥，设 $f_{i,j}$ 为考虑了 $b_1\sim b_i$，最多存在 $j$ 段的方案数（相当于钦定若干段之间组成大段），则答案就是 $\displaystyle\sum_{i=1}^m(-1)^{m-i}i!f_{m,i}$，其中 $i!$ 是给钦定的若干段之间定大小顺序。

考虑转移，$b_i$ 是否是 $1$ 是关键的，考虑枚举最后一段的位置，容易得到：

$$f_{0,0}=1$$

$$f_{i,j}=\begin{cases}f_{i-1,j-1}+2\displaystyle\sum_{k=0}^{i-2}f_{k,j-1}&b_i=1\\2\displaystyle\sum_{k=0}^{i-1}f_{k,j-1}&b_i>1\end{cases}$$

考虑生成函数，定义 $F_i(x)=\sum_{j}f_{i,j}x^j$，$S_i(x)=\sum_{j=0}^iF_j(x)$，则：

$$F_0(x)=1$$

$$F_i(x)=\begin{cases}xF_{i-1}(x)+2xS_{i-2}(x)&b_i=1\\2xS_{i-1}(x)&b_i>1\end{cases}$$

我们需要求出 $F_{m}(x)$。**考虑将生成函数写进矩阵**：

$$\begin{bmatrix}S_{i-1}(x)\F_i(x)\end{bmatrix}=\begin{cases}\begin{bmatrix}1&1\\2x&x\end{bmatrix}&b_i=1\\begin{bmatrix}1&1\\2x&2x\end{bmatrix}&b_i>1\end{cases}\times\begin{bmatrix}S_{i-2}(x)\F_{i-1}(x)\end{bmatrix}$$

我们只需求出 $m$ 个系数为多项式的矩阵的乘积，分治 $\text{NTT}$，合并左右结果时将矩阵乘法中普通乘法改为多项式乘法即可，时间复杂度 $O(n\log^2 n)$。

注意到合并时我们进行了 $8$ 次多项式乘法，$24$ 次 $\text{NTT}$，但其实只有左右共 $8$ 个多项式和 $4$ 次乘法的和结果需要进行 $\text{NTT}$，共 $12$ 次，提前 $\text{NTT}$ 可以将常数变成 $1/2$。

代码（未卡常，省略多项式模板）：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
namespace IO{//by cyffff
	
}
const int N=262144+10,mod=998244353,inv2=mod+1>>1;
namespace Init{

}
using namespace Init;
namespace PolyC{

}
using namespace PolyC;
int n,m,a[N],b[N],ans;
inline vector<Poly> solve(int l,int r){
	if(l==r){
		if(l==1) return {{1},{0},{0,b[l]==1?1:2},{0}}; 
		else return {{1},{1},{0,2},{0,b[l]==1?1:2}};
	}
	int mid=l+r>>1;
	vector<Poly>ls=solve(l,mid),rs=solve(mid+1,r);
	vector<Poly>tmp;
	tmp.push_back(rs[0]*ls[0]+rs[1]*ls[2]);
	tmp.push_back(rs[0]*ls[1]+rs[1]*ls[3]);
	tmp.push_back(rs[2]*ls[0]+rs[3]*ls[2]);
	tmp.push_back(rs[2]*ls[1]+rs[3]*ls[3]);
	return tmp;
}
int main(){
	n=read();
	Prefix(n);
	int l=0;
	for(int i=1,j=1;i<=n;){
		a[i]=read();
		j=i+a[i]-1;
		if(j>n) return puts("0"),0;
		b[++l]=a[i];
		for(int k=i+1;k<=j;k++){
			a[k]=read();
			if(a[k]!=a[i]) return puts("0"),0;
		}
		i=j+1;
	}
	vector<Poly>tmp=solve(1,l);
	Poly F=tmp[2];
	for(int i=1;i<=l;i++){
		int v=1ll*F[i]*fac[i]%mod;
		if(l-i&1) ans=dec(ans,v);
		else ans=add(ans,v);
	}
	write(ans);
	flush();
}
```
