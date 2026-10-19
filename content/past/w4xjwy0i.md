---
title: "题解 P7364 【有标号二分图计数】"
date: 2021-02-17
category: "题解"
summary: "P7364 有标号二分图计数 传送门 看到新题就来做了。 前置知识：多项式开根，生成函数基础 题意 求有 i 个点的有标号二分图个数。可以不连通。 思路 我们来思考 n 个点的"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/w4xjwy0i
slug: w4xjwy0i
---

# P7364 有标号二分图计数
#### [_传送门_](https://www.luogu.com.cn/problem/P7364)
看到新题就来做了。

前置知识：[多项式开根](https://www.luogu.com.cn/problem/P5205)，生成函数基础
## 题意
求有 $i$ 个点的有标号二分图个数。可以不连通。
## 思路
我们来思考 $n$ 个点的二分染色图的数量，显然答案为

$$\sum_{i=0}^n\begin{pmatrix}n\i\end{pmatrix}2^{i(n-i)}$$

设这个式子的 $\texttt{EGF}$ 为 $F(x)$，本题的 $\texttt{EGF}$ 为 $G(x)$，有标号二分连通图个数的 $\texttt{EGF}$ 为 $Q(x)$。

于是有

$$G(x)=\sum_{i=0}\dfrac{Q^i(x)}{i!}=e^{Q(x)}$$

这怎么求啊 qwq？

发现求不出 $Q(x)$，于是我们改变思路，发现

$$F(x)=\sum_{i=0}\dfrac{2^iQ^i(x)}{i!}=e^{2Q(x)}$$

发现 $G(x)=\sqrt{F(x)}$ 于是只要求出 $F(x)$ 就能一个多项式开根带走了。

那 $F(x)$ 怎么求啊 qwq？

我们有 $i\times(n-i)=\dfrac{n^2-i^2-(n-i)^2}{2}$，所以 $2^{i(n-i)}=\dfrac{(\sqrt2)^{n^2}}{(\sqrt2)^{i^2}(\sqrt2)^{(n-i)^2}}$。

可以看出这是卷积形式的式子，于是可以 NTT 带走。

代码不难写，就不放了。

（用提交答案一交，10ms）

再见 qwq~
