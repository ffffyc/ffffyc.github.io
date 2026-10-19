---
title: "题解 P7425【[THUPC2017] 机场】"
date: 2021-03-14
category: "题解"
summary: "传送门 传统异能网络流建图题。 题意 说不清楚，得去题面看。 思路 可以发现这是费用流的题，于是开始思考建图。 考虑用时间做点，于是先离散化掉时间，并顺便判走非法情况（某一时刻"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/d6eb0aoz
slug: d6eb0aoz
---

#### [_传送门_](https://www.luogu.com.cn/problem/P7425)
传统异能网络流建图题。
## 题意
说不清楚，得去题面看。
## 思路
可以发现这是费用流的题，于是开始思考建图。

考虑用时间做点，于是先离散化掉时间，并顺便判走非法情况（某一时刻飞机数比机场限制飞机数打）。

将源点设为 $1$，汇点设为 $3n+1$，首先从源点向 $2$ 号点连边，流量限制为 $a$，费用为 $0$，再将所有 $i\in(1,2n)$，从 $i$ 号点连向 $i+1$，流量限制为 $a$，费用为 $0$。再连一条 $2n$ 向 $t$ 的边，流量限制、费用同上。

再对于第 $i$ 架飞机，设登记时间为 $s_i$，起飞时间为 $t_i$，人数 $u_i$，则连 $(s_i,2n+i,1,0),(s_i+1,2n+i,1,-u_i+u_i\times p),(t_i,2n+i,1,-u_i)$ 三条边，其中 $(a,b,c,d)$ 表示 $a$ 向 $b$，流量限制为 $c$，费用为 $d$ 的边。

如这组数据
```cpp
input:
1
3 2 3
0.5
2 3 100
3 4 6
3 5 7
output:
1
```
建图为：

![qwq](https://cdn.luogu.com.cn/upload/image_hosting/st25haxc.png?x-oss-process=image/resize,m_lfit,h_170,w_225)

（可能有亿点丑，也可以在[这个网站](https://csacademy.com/app/graph_editor/)输入下面这些东西查看）
```cpp
1 2 2,0
2 3 2,0
3 4 2,0
4 5 2,0
5 6 2,0
6 10 2,0
1 7 1,0
7 2 1,-1
7 6 1,-2
2 8 1,0
8 3 1,-2
8 4 1,-3
3 9 1,0
9 4 1,-2
9 5 1,-3

```
建出来的图跑 `dinic` 即可。

再见 qwq~
