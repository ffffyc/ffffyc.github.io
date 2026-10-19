---
title: "Lucas"
date: 2021-07-06
category: "个人记录"
tags: ["学习笔记"]
summary: "重新学数论。 有时会省略 \\,p。 Lucas 描述：求 Cmn p，p 是质数。O(logpn)。 Cmn=m!n!(m-n)! 引理 Cpi p iCp-1i-1. 二项式"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/uhzxfoms
slug: uhzxfoms
---

重新学数论。

有时会省略 $\bmod\,p$。

## $\text{Lucas}$
描述：求 $C_m^n\bmod p$，$p$ 是质数。$O(\log_pn)$。

$C_m^n=\frac{m!}{n!(m-n)!}$

**引理** $C_p^i\equiv\frac p iC_{p-1}^{i-1}$.

**二项式定理** $(x+y)^n=\sum_{k=0}^nC_n^ka^kb^{n-k}$.

$\to (x+1)^p\equiv x^p+1+\sum_{i=1}^{p-1}C_p^ix^i\equiv x^p+1+p\sum_{i=1}^{p-1}\frac{1}{i}C_{p-1}^{i-1}x^i\equiv 0$.

令 $n=ap+b,m=cp+d(0\le b,d<p)$

$(x+1)^{n}=(x+1)^{ap+b}=(x+1)^{ap}(x+1)^b=(x^p+1)^a(x+1)^b=(\sum_{i=0}^aC_a^ix^{ip})(\sum_{i=0}^bC_b^ix^i)$.

$(x+1)^{ap+b}\equiv \sum_{i=0}^{ap+b}C_{ap+b}^ix^i$.

同时观察两边的 $x^{m}$ 项：

$C_{ap+b}^{cp+d}x^{cp+d}\equiv C_a^{c}x^{cp}\times C_b^{d}x^d$.

$\to C_{ap+b}^{cp+d}\equiv C_a^{c}C_b^d$
即得

**卢卡斯定理** $C_m^n=C^{\frac n p}_{\frac m p}C^{n\text{ mod } p}_{m\text{ mod } p}$。
## $\text{exLucas}$
描述：求 $C_m^n\bmod p$。最优 $O(\sqrt p+\sum_{i=1}^kp_i^{q_i})=O(p)$。
