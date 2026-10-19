---
title: "题解 P7243 【最大公约数】"
date: 2021-01-03
category: "题解"
summary: "P7243 最大公约数 传送门 刚拿到这道题可能没有什么思路，但是想一会就想通了。 首先，我们设 gcd(ax,y,aq,p)=1 .如果 q,p 不存在，则 ax,y 一定不"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/xxjj691n
slug: xxjj691n
---

# P7243 最大公约数
#### [_传送门_](https://www.luogu.com.cn/problem/P7243)
刚拿到这道题可能没有什么思路，但是想一会就想通了。

首先，我们设 $\gcd(a_{x,y},a_{q,p})=1$ .如果 $q,p$ 不存在，则 $a_{x,y}$ 一定不为 $1$ ，因为它会保留所有数最后的 $gcd$.

如果 $q,p$ 存在，则答案不超过 $|q-x|+|p-y|$ ，即为点 $(x,y)$ 与点 $(q,p)$ 之间的曼哈顿距离.所以答案一定小于 $\displaystyle\min_{\gcd(a_{x,y},a_{q,p})=1}|q-x|+|p-y|$.

这样为什么正确呢？在变化 $d$ 天后，与格子 $(q,p)$ 曼哈顿距离为 $d$ 的格子就只剩下自己与 $a_{q,p}$ 的因数了，$|q-x|+|p-y|$ 天后，$a_{x,y}$ 就只剩下与 $a_{q,p}$ 的共同因素了。

可以想到广搜，存当前曼哈顿距离以内的数与$a_{x,y}$的最大公因数，当它变为1，输出目前曼哈顿距离即可


$Code$:
[Here](https://www.luogu.com.cn/paste/jezusxcz)
