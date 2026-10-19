---
title: "GDOI 2022 普及组 游寄"
date: 2022-04-16
category: "游记"
tags: ["GDOI 2022"]
summary: "Day 1 啥玩意？ 8:25 拿到题。题目下载。 8:30 比赛开始。 A 一个模拟，3 分钟敲完。？？？。 B 搞出前缀异或和，去 0，去重即可。 C 贪心，每次找使用的权"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/ejvwvjoh
slug: ejvwvjoh
---

## $\text{Day 1}$
啥玩意？

$8:25$ 拿到题。[题目下载](https://www.luogu.com.cn/fe/api/problem/downloadAttachment/bt8zj637)。

$8:30$ 比赛开始。

$\text A$ 一个模拟，3 分钟敲完。[？？？](https://www.luogu.com.cn/paste/bots7yjj)。

$\text B$ 搞出前缀异或和，去 $0$，去重即可。

$\text C$ 贪心，每次找使用的权值最大的结点，删掉，把所有儿子加入。找权值最大的节点用线段树。$O(n\log n)$。

$\text D$ 

枚举公差 $d$，找出所有 $d|a_i$ 的 $c_i$，考虑对于一个极长的公差为 $d$ 的等差数列 $[l,r]$，查分完求的就是 $\displaystyle\sum_{i=l}^r\sum_{j=i}^{\min(r,i+x-1)}\prod_{k=i}^jc_k$，求出 $c$ 的前缀积的前缀和即可。前缀积的逆元可以通过 $O(1)$ 求每个元素的逆元去 $\log$。$O(n\ln n)$。

我在枚举倍数是枚举了元素，变成了 $n^2$，哈哈。

预计 $100+100+100+60=360$。

这不是 $\text{AK}$ 场吗
## $\text{Day 2}$

$\text A$ 等价于求 $i\in[3,n]$ 的数中，$(n-1)\bmod i\ne 0,1,i-1$ 的 $i$ 的数量，可以整除分块。还有对 $n-2,n-1,n$ 分别分解质因数的做法，不知道。

$\text B$ 可以发现返回是假的。考虑每个非叶子结点只会造成 $1$ 的贡献，叶子结点还要关掉。所以答案为 $n+$ 叶子数。

$\text C$ 大模拟出题人**。

$\text D$ 列出 dp 式子做最短路。

$\text D$ 赛时降智没想出来。

预计 $100+100+100+20=320$。
## $\text{Day 3}$
结果 $100+100+100+60+100+100+70+20=650$，$\text{rank 25}$。

流汗黄豆。
