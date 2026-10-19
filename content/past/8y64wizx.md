---
title: "题解：P8299 [COCI2012-2013#2] INFORMACIJE"
date: 2025-01-08
category: "题解"
summary: "Link 题意 构造一个长为 n 的排列 p1 n，使得其满足给出的 m 条限制，每条限制形如： 1 l r v，要求 pl r 的最大值为 v。 2 l r v，要求 pl "
math: true
top: 2
source: https://www.luogu.com.cn/article/8y64wizx
slug: 8y64wizx
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P8299)
## 题意
构造一个长为 $n$ 的排列 $p_{1\sim n}$，使得其满足给出的 $m$ 条限制，每条限制形如：
- `1 l r v`，要求 $p_{l\sim r}$ 的最大值为 $v$。
- `2 l r v`，要求 $p_{l\sim r}$ 的最小值为 $v$。

无解输出 `-1`。

$n\le200$。

Bonus：$n\le 2\times 10^4$。
## 思路
记 $p_{1\sim n}$ 的逆排列为 $q_{1\sim n}$，则题目的要求可转化为 $2n$ 条限制：$p_i\in[l_i,r_i]$，$q_v\in[a_v,b_v]$，不难看出可转化为二分图匹配问题，可以通过本题。

在平面直角坐标系上画出水平线段与竖直线段各 $n$ 条，分别为：
- $x=i$，$l_i\le y\le r_i$；
- $y=v$，$a_v\le x\le b_v$。

则水平线段 $i$ 与竖直线段 $v$ 连边当且仅当两条线段相交，可以使用主席树优化建图，对横坐标做扫描线，在端点出插入删除水平线段，扫到一个横坐标时将该竖直线段与当前区间内存在的水平线段连边。

点数与边数均为 $O(n\log n)$。

考虑一个点 $i$ 能连向哪些值 $v$，若值 $v$ 未在任意限制中出现，则可直接建出这类值的线段树，对每个位置 $i$ 使用普通线段树优化建图连向区间内的这类值。

否则注意到对于一个 $p_i\in[l,r]$，位置 $i$ 可取且覆盖位置 $i$ 的限制的值只可能为 $l$ 或者 $r$，我们只需要根据 $q_l,q_r$ 的条件判断 $p_i$ 是否可取到值 $l,r$ 便可。

点数为 $O(n)$，边数为 $O(n\log n)$。

使用 Dinic 算法即可通过 $n\le 2\times 10^4$ 版本。
