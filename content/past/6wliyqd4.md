---
title: "题解 P9663【[ICPC2021 Macao R] Permutation on Tree】"
date: 2024-02-17
category: "题解"
summary: "Link 题意 给定一颗叶向树，求所有合法拓扑序 p 的 Σi=2n|pi-pi-1| 之和，对 109+7 取模。 n≤200。 思路 考虑求一颗树的拓扑序数量，定义 gx "
math: true
top: 2
source: https://www.luogu.com.cn/article/6wliyqd4
slug: 6wliyqd4
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P9663)

## 题意

给定一颗叶向树，求所有合法拓扑序 $p$ 的 $\sum_{i=2}^n|p_i-p_{i-1}|$ 之和，对 $10^9+7$ 取模。

$n\le200$。

## 思路

考虑求一颗树的拓扑序数量，定义 $g_x$ 为 $x$ 子树内拓扑序的数量，$sz_x$ 为 $x$ 子树大小。考虑 $x$ 不同子树之间无限制，而 $x$ 必须摆在第一位，显然有

$$g_x=\binom{sz_x-1}{sz_{t_1},sz_{t_2},\dots,sz_{t_k}}\prod_{i=1}^kg_{t_i}$$

其中 $t_{1\sim k}$ 为 $x$ 的儿子，多重组合数 $\binom{n}{s_1,s_2,\dots.s_k}$ 意义为把 $n$ 个数划分成 $k$ 个大小给定集合的方案数。

根据此式，我们可以算出 $\text{reduce}(x,p_1,\dots)$ 表示求 $x$ 子树去掉 $p_1,\dots$ 子树后合法拓扑序数量，其中 $p_{1\sim k}$ 均为 $x$ 的儿子，此函数时间复杂度为 $O(k)$，预处理 $g_x$ 逆元即可。

考虑枚举 $a,b$，计算它们在所有合法拓扑序中相邻的次数。
- $a,b$ 有祖先后代关系。那么此时 $a$ 一定是 $b$ 的父亲，考虑 $a$ 子树内所有拓扑序，那么 $b$ 一定在第二位，方案数为 $\text{reduce}(a,b)\cdot\binom{sz_a-2}{sz_b-1}\cdot g_b$。
- $a,b$ 无祖先后代关系。设 $c=\text{LCA}(a,b)$，$a',b'$ 分别为 $c$ 的 $a,b$ 方向的儿子。由于 $a,b$ 相邻，不妨先把 $a,b$ 子树拓扑序合并，方案数为 $\binom{sz_a+sz_b-2}{sz_a-1}\cdot g_ag_b$。考虑令 $f(u,v)$ 表示 $u,v$ 子树拓扑序拼起来有几个是 $a,b$ 相邻的，则 $f(fa_u,v)\gets f(u,v)\cdot\text{reduce}(fa_u,u)\cdot\binom{sz_{fa_u}+sz_v-2}{sz_u+sz_v-1}$，$f(u,v)\to f(u,fa_v)$ 同理。最后 $c$ 子树内 $a,b$ 相邻方案数就是 $f(a',b')\cdot\text{reduce}(c,a',b')\cdot\binom{c-2}{sz_{a'}+sz_{b'}-1}$。

子树内方案数容易推至全树方案数，总时间复杂度 $O(n^4)$。

考虑 $a,b$ 在 $f$ 转移式中无体现，考虑令原来 $a,b$ 时的 $f(u,v)$ 记作 $f'(a,b,u,v)$，新定义 $f(u,v)$ 为 $\sum_{a\in S_u}\sum_{b\in S_v}|a-b|f'(a,b,u,v)$，转移式不变，在 $fa_u=fa_v$ 时统计贡献，注意不能转移至 $u,v$ 有祖先后代关系的状态。子树方案数也可加起来一起推至全树，总时间复杂度 $O(n^2)$。
