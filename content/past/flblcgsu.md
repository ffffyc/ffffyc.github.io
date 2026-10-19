---
title: "题解：P10998 Tuple+"
date: 2024-08-27
category: "题解"
summary: "Link 有意思，记录一下。 题意 给出 m 个互不相同的无序三元组 (u,v,w)，求有多少无序四元组 (a,b,c,d) 使得三元组 (a,b,c),(a,b,d),(a,"
math: true
top: 2
source: https://www.luogu.com.cn/article/flblcgsu
slug: flblcgsu
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P10998)

有意思，记录一下。
## 题意

给出 $m$ 个互不相同的无序三元组 $(u,v,w)$，求有多少无序四元组 $(a,b,c,d)$ 使得三元组 $(a,b,c),(a,b,d),(a,c,d),(b,c,d)$ 均存在。

$m\le 3\times 10^5$。

Bonus：$m\le 2\times 10^6$。
## 题解

回忆无向图三元环计数的做法，使所有边从度数小的点指向度数大的点，其中度数相同的比较编号。此时图形成 DAG，三元环中一个点指向另外两个点，枚举该点 $u$，标记其所有出点，枚举 $u\to v\to w$ 即可。

考虑计算复杂度，令定向后每个点的出度为 $\text{deg}'(u)$：
- 如果 $\text{deg}(u)\le m^{1/2}$，显然 $\text{deg}'(u)\le \text{deg}(u)\le m^{1/2}$。
- 如果 $\text{deg}(u)\ge m^{1/2}$，那么定向后每一个 $u\to v$ 均有 $\text{deg}(v)\ge \text{deg}(u)\ge m^{1/2}$，所以 $\text{deg}'(u)\le m^{1/2}$。

所以 $\text{deg}'(u)\le m^{1/2}$。我们在 $O(m^{3/2})$ 的时间复杂度内枚举到了每一个三元环，同时这也说明了三元环数量的上界。

回到本题，限制为三元组，相对难以处理，我们考虑强制满足一维的限制以化为二维的问题。假如枚举 $a$，则对于所有的三元组 $(a,x,y)$，我们在 $x,y$ 间连边，枚举建出的图上的所有三元环并检查这三点是否包含在同一三元组内即可。时间复杂度 $O(m^{3/2})$。

考虑类似三元环计数的优化：我们令 $\text{deg}(i)$ 表示包含 $i$ 的三元组数量，则我们将每个三元组内部重排使得其 $\text{deg}(u)\le \text{deg}(v)\le \text{deg}(w)$，其中度数相同的比较编号。

考虑计算复杂度，令 $\text{deg}'(u)$ 表示重排后三元组 $(u,x,y)$ 的数量：
- 如果 $\text{deg}(u)\le m^{2/3}$，显然 $\text{deg}'(u)\le \text{deg}(u)\le m^{2/3}$。
- 如果 $\text{deg}(u)\ge m^{2/3}$，那么重排后每一个 $(u,v,w)$ 均有 $\text{deg}(w)\ge\text{deg}(v)\ge \text{deg}(u)\ge m^{2/3}$，所以 $\text{deg}'(u)\le m^{2/3}$。

那么 $\text{deg}'(u)\le m^{2/3}$ 且 $\sum\text{deg}'(u)=m$，复杂度为 $\sum(\text{deg}'(u))^{3/2}$，这在 $\forall i\in[1,m^{1/3}],\text{deg}'(i)=m^{2/3}$ 时取得最大值 $O(m^{4/3})$。

如果本题中三元组变为 $k$ 元组，我们仍可依照类似的方式将其变为 $k-1$ 元组的子问题，时间复杂度可做到 $O(m^{1/k+1})$。
