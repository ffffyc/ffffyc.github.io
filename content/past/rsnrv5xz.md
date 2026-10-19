---
title: "题解 P3706【[SDOI2017]硬币游戏】"
date: 2021-09-17
category: "题解"
summary: "Link 题意 给你 n 个长为 l 的字符串 a1,2,...,n，字符集大小为 m，每次随机在末尾添加一个字符，当当前字符串包含字符串 ai 时结束操作，对 1≤ i≤ n"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/rsnrv5xz
slug: rsnrv5xz
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P3706)
## 题意
给你 $n$ 个长为 $l$ 的字符串 $a_{1,2,...,n}$，字符集大小为 $m$，每次随机在末尾添加一个字符，当当前字符串包含字符串 $a_i$ 时结束操作，对 $1\le i\le n$ 问 $a_i$ 成为结束操作时所包含的字符串的概率。

$1\le n,l\le300,m=2$
## 思路
首先给个弱化版 [$\text{Link}$](https://www.luogu.com.cn/problem/P6125)，不过这道题的做法和那题没什么关系。

- 概率生成函数

设 $X$ 为离散随机变量，则它的概率生成函数 $\displaystyle F(x)=\sum_{i=0} \text{P}(X=i)x^i$。

我们设 $F_i(x)$ 表示包含的字符串是 $a_i$ 时的概率生成函数，即 $[x^n]F_i(x)$ 为字符串长度为 $n$ 时包含了 $a_i$ 并结束的概率，则我们要求的就是 $F_i(1)$。

另外设置辅助 $\text{PGF }G(x)$ 表示长度为 $n$ 时没结束的概率。

我们可以列出方程：

$$\sum_{i=1}^n F_i(x)+G(x)=1+G(x)\cdot x$$

这个式子的意思是在序列中添加一个数，它可能在任意一个字符串结束，也可能不结束，$1$ 为空序列情况。

$$G(x)\cdot \left(\frac x 2\right)^l=\sum_{t=1}^n\sum_{i=1}^l[a_p[1,i]=a_t[l-i+1,l]]F_t(x)\left(\frac x 2\right)^{l-i}$$
