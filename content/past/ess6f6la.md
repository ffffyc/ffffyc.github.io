---
title: "题解：P11368 [Ynoi2024] After god"
date: 2024-12-05
category: "题解"
summary: "Link 题意 你需要维护两个长为 n 的序列 a1 n,b1 n，初值均为 0。接下来 m 次操作，每次操作中给出 x,y，依次执行： 令 ax y； 令 i∈[1,n],b"
math: true
top: 2
source: https://www.luogu.com.cn/article/ess6f6la
slug: ess6f6la
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P11368)
## 题意

你需要维护两个长为 $n$ 的序列 $a_{1\sim n},b_{1\sim n}$，初值均为 $0$。接下来 $m$ 次操作，每次操作中给出 $x,y$，依次执行：
- 令 $a_x\gets y$；
- 令 $\forall i\in[1,n],b_i\gets b_i+\displaystyle\max_{j=1}^i a_j$；
- 查询 $\displaystyle\sum_{i=1}^x b_i$。

$n,m\le 10^6$。
## 题解

直接维护前缀最大值需要单侧递归上传，复杂度过高不做考虑。

令 $a_{i,t}$ 为时刻 $t$ 对应的 $a_i$，$c_{i,t}$ 为时刻 $t$ 中前缀 $a_{1\sim i,t}$ 的最大值。所求为 $\sum_{i=1}^x\sum_{j=1}^t c_{i,j}$。

考虑**交换求和顺序，对序列维做扫描线**。设当前扫描到 $i$，则维护所有的 $c_{i,t}$ 以及其历史和 $\sum_{j=1}^ic_{j,t}$，对位置 $i$ 的若干次修改构成对 $c_{i,t}$ 的若干次区间取 $\max$ 操作，而一次查询即为前缀历史和查询。写一个维护历史和的吉司机线段树即可维护。

时间复杂度 $O(n\log n)$。
