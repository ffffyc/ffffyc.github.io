---
title: "Ynoi 记录"
date: 2021-11-10
category: "个人记录"
summary: "写的挺少的。 有些加粗的是一些 trick。 1.P5309 [Ynoi2011] 初始化 讲个笑话，这题我 (n2) 过去的。 2.P5356 [Ynoi2017] 由乃打扑"
math: true
top: 1
hidden: true
source: https://www.luogu.com.cn/article/g1ti5cai
slug: g1ti5cai
---

写的挺少的。

有些加粗的是一些 trick。
****
1.P5309 [Ynoi2011] 初始化

讲个笑话，这题我 $\Theta(n^2)$ 过去的。
****
2.P5356 [Ynoi2017] 由乃打扑克

讲个笑话，这题我 $\Theta(n\sqrt n\log n\log v)$ 过去的。
****
3.P3934 [Ynoi2016] 炸脖龙 I

树状数组维护序列，拓展欧拉定理处理 power-tower。

时间复杂度应该是 $\Theta(n\log n\log p)$。
****
4.P5607 [Ynoi2013] 无力回天 NOI2017

这玩意直接差分然后线段树维护线性基就做完了。。。

时间复杂度 $\Theta(n\log n\log^2 v)$。
****
5.P4688 [Ynoi2016] 掉进兔子洞

把询问分一下组，每组跑莫队，然后 bitset 随便算一下。

时间复杂度 $\Theta(n\sqrt n+\dfrac{n^2} w)$。
****
6.P5072 [Ynoi2015] 盼君勿忘

令 $x=r-l+1$，你推一下式子，其实是求 $\sum 2^x-2^{x-cnt_i}$。

然后就是光速幂预处理、莫队维护双向链表就做完了。

时间复杂度 $\Theta(n\sqrt n)$。
****
7.P5355 [Ynoi2017] 由乃的玉米田

前三种比较简单。第四种考虑根号分治，对于 $x\le S$，找到距离 $i$ 最近的 $l_i$ 满足 $a_i$ 与 $a_{l_i}$ 商为 $x$。对于 $x\ge S$，可以直接枚举 $i$，看 $i$ 和 $ix$ 是否同时出现，莫队时判断即可。

$S=\Theta(\sqrt n)$，时间复杂度 $\Theta(n\sqrt v+\dfrac{n^2} w)$。
****
8.P5048 [Ynoi2019 模拟赛] Yuno loves sqrt technology III

相当简单，不过可以知道一个 trick。

序列分块，**维护块间答案**，散块暴力找答案，均摊是对的。

时间复杂度 $\Theta(n\sqrt n)$。
****
9.P5610 [Ynoi2013] 大学

每个数只会被除 $\Theta(\log v)$ 次。

听说约数个数接近 $O(a^{1/3})$，维护每个数的倍数，对每个数维护个数据结构存倍数。这里可以用**并查集**。

你卡卡常就过了/youl。

时间复杂度 $O(nv^{\frac 1 3}+v\log v+n\log n\alpha(n))$。
****
10.P5354 [Ynoi2017] 由乃的 OJ

一个位运算 trick：对于数据结构上一个结点，**维护 $0$、$2^k-1$ 从左向右、从右向左通过此结点（区间）后的值。**

然后可以 $\text{Link-Cut-Tree}$，时间复杂度 $\Theta(n\log n)$。
****
11.P7446 [Ynoi2007] rfplca

？？
****
12.P5071 [Ynoi2015] 此时此刻的光辉

Pollard-Rho 分解质因数，根号分值，莫队，$\le S$ 的质数暴力前缀和、$>S$ 的质数莫队。

时间复杂度玄学。
****
13.
