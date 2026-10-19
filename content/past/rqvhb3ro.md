---
title: "题解：P12044 [USTCPC 2025] Algorithm Duel"
date: 2025-04-08
category: "题解"
summary: "Link 题意 给定 n 个 3n-3 维的 01 向量，保证它们线性无关。你需要选出其中一些向量，使得它们的异或结果中一的个数在 [n,2n-2] 中。 n≤ 1000。 题"
math: true
top: 2
source: https://www.luogu.com.cn/article/rqvhb3ro
slug: rqvhb3ro
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P12044)
## 题意
给定 $n$ 个 $3n-3$ 维的 `01` 向量，保证它们线性无关。你需要选出其中一些向量，使得它们的异或结果中一的个数在 $[n,2n-2]$ 中。

$n\le 1000$。
## 题解
先将这些向量塞入线性基中，再将每个最高位位置消成只有一个向量包含其，则基内每个向量 $a_i$ 都有 $|a_i|\le 2n-2$。若存在 $|a_i|\ge n$ 则直接找到了一组解，否则有所有 $|a_i|\le n-1$。

初始令向量 $x=(0,\dots,0)$，依次将 $x$ 异或上 $a_i$，过程中必定存在一个时刻使得 $n\le |x|\le 2n-2$，原因如下：
- 最终有 $|x|\ge n$，这是因为 $n$ 个最高位都必定存在；
- 过程中 $|x|$ 单次增长不超过 $n-1$，这是因为 $|a_i|\le n-1$。

故第一次 $|x|\ge n$ 的时刻必有 $|x|\le 2n-2$。

使用 `bitset` 求解线性基，时间复杂度 $O\left(\dfrac{n^3}w\right)$。
