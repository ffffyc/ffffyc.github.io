---
title: "题解 P5073【[Ynoi2015] 世上最幸福的女孩】"
date: 2023-08-08
category: "题解"
summary: "Link 题意 全局加，区间最大子段和。 n≤ 3× 105，m≤ 6× 105。 思路 使用 KTT 通过。 对于每一次修改操作记录此时总共加了多少，记为 vi。对于每一次询"
math: true
top: 2
source: https://www.luogu.com.cn/article/pah0sw0w
slug: pah0sw0w
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P5073)
## 题意
全局加，区间最大子段和。

$n\le 3\times 10^5$，$m\le 6\times 10^5$。

## 思路

使用 [$\text{KTT}$](https://www.luogu.com.cn/problem/P5693) 通过。

对于每一次修改操作记录此时总共加了多少，记为 $v_i$。对于每一次询问将它放在其之前的最后一次修改操作后。

将操作按照 $v_i$ 排序，将序列中所有数都加上 $v_1$，$v_{1,\dots n}$ 减去 $v_1$。那么我们将问题转化为了全局加正数，区间最大子段和，可以使用 $\text{KTT}$。

显然全局加正数，最大前缀和、最大后缀和、最大子段和选择区间发生变化时均会变长，则总共变长 $O(n\log n)$ 次，每次花费 $O(\log n)$，总时间复杂度 $O(n\log^2n+m\log n)$，空间复杂度 $O(n+m)$。很难卡满。

我的实现直接写就能擦着时限空限通过，如果被卡常了可以用底层分块优化时空常数。
