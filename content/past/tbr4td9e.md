---
title: "拉格朗日反演学习笔记"
date: 2021-07-28
category: "个人记录"
summary: "拉格朗日反演 复合逆 若对于两个多项式 F,G 有 G(F(x))=x，则称 F,G 互为复合逆。 定理证明 若对多项式 F 有 G(F(x))=x，将 G(F(x)) 表为 "
math: true
top: 2
source: https://www.luogu.com.cn/article/tbr4td9e
slug: tbr4td9e
---

### 拉格朗日反演
#### 复合逆
若对于两个多项式 $F,G$ 有 $G(F(x))=x$，则称 $F,G$ 互为复合逆。
#### 定理证明
若对多项式 $F$ 有 $G(F(x))=x$，将 $G(F(x))$ 表为
$$\sum_{i\ge1}b_iF^i(x)=x$$
两边求导，注意左边 $F^i$ 是函数 $F(x)$ 和函数 $x^i$ 的复合函数
$$\sum_{i\ge1}ib_iF^{i-1}(x)F'(x)=1$$
两边同除 $F^n(x)$，提取 $x^{-1}$ 的系数，有
$$[x^{-1}]\sum_{i\ge1}ib_iF^{i-n-1}(x)F'(x)=[x^{-1}]\frac1{F^n(x)}$$
对于 $i\ne n$，有 $F^{i-n-1}(x)F'(x)=\frac1{n-i}(F^{i-n})'(x)$，其 $x^{-1}$ 项必为 $0$，故不考虑。

当 $i=n$ 时，
$$\begin{aligned}
F^{-1}(x)F'(x)
&=\frac{\sum_{i\ge1}ia_ix^{i-1}}{\sum_{i\ge1}a_ix^i}\\
&=\frac{\sum_{i\ge1}ia_ix^{i-1}}{a_1x}\cdot\frac1{1+\sum_{i\ge2}\frac{a_i}{a_1}x^{i-1}}\\
\end{aligned}$$

于是对于前面那个多项式，其 $x^{-1}$ 次项只能由 $\frac{a_1}{a_1x}$ 得到并且系数为 $1$，后面那个多项式的常数项必定为 $1$，所以 $[x^{-1}]F^{-1}(x)F'(x)=1$。

代回得到
$$nb_n=[x^{-1}]\frac1{F^n(x)}$$
$$[x^n]G(x)=\frac 1 n\cdot[x^{-1}]\frac1{F^n(x)}$$

换成更好看的形式表为

$$[x^n]G(x)=\frac 1 n\cdot[x^{n-1}]\frac {x^n} {F^n(x)}$$
同样有
$$[x^n]F(x)=\frac 1 n\cdot[x^{n-1}]\frac {x^n} {G^n(x)}$$
#### 扩展拉格朗日反演
即 $G(F(x))=H(x)$ 时的特殊形式，有结论：

$$[x^n]G(x)=\frac 1 n\cdot[x^{n-1}]H'(x)\cdot\frac {x^n} {F^n(x)}$$
### 例题
#### $1.\text{BZOJ3684}$ 大朋友和多叉树
设 $F$ 为答案的生成函数，不难得出
$$F=x+\sum_{i\in D}F^i$$
其中 $x$ 表示单个叶子节点，$F^i$ 表示选择 $i$ 颗树做当前结点的儿子。

移项一下得到 
$$F-\sum_{i\in D}F^i=x$$
设函数
$$G(x)=x-\sum_{i\in D}x^i$$
则
$$G(F(x))=x$$
直接上拉格朗日反演，得到
$$[x^n]F(x)=\frac 1 n\cdot[x^{n-1}]\frac {x^n} {G^n(x)}$$
$$[x^n]F(x)=\frac 1 n\cdot[x^{n-1}]\frac 1 {\left(\frac {G(x)} x\right)^n}$$
直接求即可，时间复杂度 $O(n\log n)$。
#### $2.\text P5828$ 边双连通图计数
设有根无向连通图的 $\text{EGF}$ 为 $F(x)$，有根边双连通图的 $\text{EGF}$ 为 $G(x)$。

我们显然可以使用[有标号无向连通图](https://www.luogu.com.cn/problem/P4841)的 $\text{EGF}$ 乘上 $n$ 以得到 $F(x)$，于是考虑用 $F,G$ 互相表示。

对于一个有根无向连通图，我们可以枚举其根所在的边双大小，再算出所有连向其它部分的边的 $\text{EGF}$。

对于一条边，我们可以有：其挂着一个无向连通图；可以连在边双中任意一个点上。所以一条边的 $\text{EGF}$ 为 $nF(x)$。（其中 $n$ 为根节点所在的边双的大小）

由于连的多条边与一条边也可看为集合与元素的关系，可以直接得到
$$\begin{aligned}
F(x)&=\sum_{n\ge1}g_n\exp(nF(x))\frac{x^n}{n!}\\
&=\sum_{n\ge1}\frac{g_n}{n!}x^ne^{nF(x)}\\
&=\sum_{n\ge1}\frac{g_n}{n!}x^n{e^{F(x)}}^n\\
&=\sum_{n\ge1}\frac{g_n}{n!}\left(x\exp(F(x))\right)^n\\
&=G(x\exp(F(x)))
\end{aligned}$$
令 $H(x)=x\exp(F(x))$，有 $F(x)=G(H(x))$，根据扩展拉格朗日反演有
$$\begin{aligned}
[x^n]G(x)&=\frac 1 n\cdot[x^{n-1}]F'(x)\frac{x^n}{H^n(x)}\\
&=\frac 1 n\cdot[x^{n-1}]F'(x)\exp(-nF(x))
\end{aligned}
$$
至此直接求解即可。

时间复杂度 $O(n\log n)$。

代码实现见[题解 P5828](https://www.luogu.com.cn/blog/cyffff/solution-p5828)。
#### $3.\text P5827$ 点双连通图计数
设有根无向连通图的 $\text{EGF}$ 为 $F(x)$，无根点双连通图的 $\text{EGF}$ 为 $G(x)$。

我们显然可以使用[有标号无向连通图](https://www.luogu.com.cn/problem/P4841)的 $\text{EGF}$ 乘上 $n$ 以得到 $F(x)$，于是考虑用 $F,G$ 互相表示。

对于一个有根无向连通图，每个点都会被包含在至少 $1$ 个点双中，且每个点双的大小不少于 $2$。注意还需要特判 $n=1$ 时输出 $1$。

考虑断掉根连出的边，无向连通图被划分成若干连通块，根据 $\exp$ 的集合意义，求出单个连通块的 $\text{EGF}$ 即可。

对于根所在的任意一个点双连通块，若在其任何除根以外的一点连上一个以该点为根的无向连通图不会影响根所在的任意一个点双的大小，故单个连通块的 $\text{EGF}$ 为
$$\sum_{n\ge1}g_{n+1}\frac{F^n(x)}{n!}$$
可以直接得到
$$\begin{aligned}
F(x)&=x\exp(\sum_{n\ge1}g_{n+1}\frac{F^n(x)}{n!})\\
&=x\exp(G'(F(x)))\\
\ln \frac{F(x)}x&=G'(F(x))
\end{aligned}$$
令 $H(x)=\ln\dfrac{F(x)}{x}$，有 $G'(F(x))=H(x)$，根据扩展拉格朗日反演有
$$\begin{aligned}
[x^n]G'(x)&=\frac 1 n\cdot[x^{n-1}]H'(x)\frac{x^n}{F^n(x)}\\
&=\frac 1 n\cdot[x^{n-1}]H'(x)\exp(\ln(\left(\frac{F(x)}{x}\right)^{-n}))\\
&=\frac 1 n\cdot[x^{n-1}]H'(x)\exp(-nH(x))
\end{aligned}
$$
至此直接求解即可。

时间复杂度 $O(n\log n)$。

代码实现见[题解 P5827](https://www.luogu.com.cn/blog/cyffff/solution-p5827)。
