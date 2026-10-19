---
title: "题解 【[JRKSJ R4] risrqnis A】"
date: 2021-10-27
category: "题解"
summary: "题目背景的意思是，CSP-S2021 中也有这个 trick。 题意 给你一个长度为 n 的序列 a，有 q 次操作，初始有一个空集 S，共有两种操作： 1 l r，S S\\x"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/qwl7i1tz
slug: qwl7i1tz
---

题目背景的意思是，CSP-S2021 中也有这个 trick。

## 题意
给你一个长度为 $n$ 的序列 $a$，有 $q$ 次操作，初始有一个空集 $S$，共有两种操作：

- `1 l r`，$S\gets S\cup\{x|l\le x\le r\}$；
- `2 l r`，查询 $\displaystyle\sum_{i=l}^r[a_i\in S]$。

数据范围：$n,q\le10^6$.

## 题解
称所有 $a_i\in S$ 的 $i$ 的数 $i$ 为“合法结点”。

考虑算出每次插入操作后每个数是不是合法结点，查询时统计区间的合法结点数的个数即可。

考虑将原序列排序，得到序列 $b$，对于一次插入操作，在 $b$ 上二分找到第一个 $\ge l$ 的数 $L$，最后一个 $\le r$ 的数 $R$，将 $[L,R]$ 中的数的原位置标记为合法结点。考虑使用树状数组，标记合法结点后可以直接查询。

现在遇到了一个问题：一个数可能会被多次标记合法结点，导致复杂度出错。

考虑使用[并查集惰性删除](https://www.luogu.com.cn/discuss/372365)的简单 trick，删除一个数 $i$ 时，将集合 $i$ 合并至集合 $i+1$，对于一个本次新标记的点 $i$，下一个需要标记的点为 $\text{find}(i+1)$。容易发现，这样每个数都不会被重复标记。

由于每个数都只会被标记一次，时间复杂度为 $\Theta((n+q)\log n)$。如果你用平衡树删除，也可能能过呢（

实现过于简单，没有代码。
