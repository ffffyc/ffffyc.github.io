---
title: "莫比乌斯反演学习笔记"
date: 2021-07-07
category: "个人记录"
tags: ["学习笔记"]
summary: "以前都是抄的，现在重新学。很菜勿喷。 积性函数 f(ab)=f(a)f(b),gcd(a,b)=1 ,,,d 完全积性函数 f(ab)=f(a)f(b) I(x)=1,id(x"
math: true
top: 2
source: https://www.luogu.com.cn/article/fnmt9pcd
slug: fnmt9pcd
---

以前都是抄的，现在重新学。很菜勿喷。

**积性函数** $f(ab)=f(a)f(b),\gcd(a,b)=1$

$\varphi,\mu,\sigma,d$

**完全积性函数** $f(ab)=f(a)f(b)$

$I(x)=1,id(x)=x,\epsilon(x)=[x=1]$

设有两个函数 $f$ 和 $g$，他们的

**狄利克雷卷积** $(f*g)=\displaystyle\sum_{d|n}f(d)g(\frac n d)$
- $f*\epsilon=f$
- $\mu*I=\epsilon$
- $\varphi*I=id$
- $\mu*id=\varphi$

**莫比乌斯反演** $f(n)=\displaystyle\sum_{d|n}g(d)\to g(n)=\displaystyle\sum_{d|n}\mu(d)f(\frac n d)$

证明：$f*\mu=g*I*\mu=g*\epsilon=g$。
****
1.求
$$\sum_{i=1}^n\sum_{j=1}^n\gcd(i,j)$$

[$\text{Link}$](https://www.luogu.com.cn/problem/P2398)

**引理 1** $\displaystyle\sum_{d|n}\mu(d)=[n=1]$

证明：由 $\mu*I=\epsilon$ 易得。

**引理 2** $\displaystyle\sum_{i=1}^n\displaystyle\sum_{d|i}\mu(d)=\displaystyle\sum_{d=1}^n\left\lfloor\frac{n}{d}\right\rfloor\mu(d)$

显然。

**推论** $\displaystyle\sum_{i=1}^n\displaystyle\sum_{j=1}^m[\gcd(i,j)=1]=\displaystyle\sum_{d=1}^{\min(n,m)}\mu(d)\left\lfloor\frac{n}{d}\right\rfloor\left\lfloor\frac{m}{d}\right\rfloor$

证明：
$$\sum_{i=1}^n\sum_{j=1}^m[\gcd(i,j)=1]$$
由引理 1 知，
$$\sum_{i=1}^n\sum_{j=1}^m\sum_{d|\gcd(i,j)}\mu(d)$$
$$\sum_{i=1}^n\sum_{j=1}^m\sum_{d|i}\sum_{d|j}\mu(d)$$
$$\sum_{i=1}^n\sum_{d|i}\sum_{j=1}^m\sum_{d|j}\mu(d)$$
由引理 2 知，
$$\sum_{i=1}^n\sum_{d|i}\sum_{d=1}^m\left\lfloor\frac{m}{d}\right\rfloor\mu(d)$$
$$\sum_{d=1}^n\left\lfloor\frac{n}{d}\right\rfloor\sum_{d=1}^m\left\lfloor\frac{m}{d}\right\rfloor\mu(d)$$
$$\sum_{d=1}^{\min(n,m)}\left\lfloor\frac{n}{d}\right\rfloor\left\lfloor\frac{m}{d}\right\rfloor\mu(d)$$
证毕。

$$\sum_{i=1}^n\sum_{j=1}^n\gcd(i,j)$$
$$\sum_{d=1}^nd\sum_{i=1}^n\sum_{j=1}^n[\gcd(i,j)=d]$$
令 $s=\left\lfloor\frac{n}{d}\right\rfloor$

$$\sum_{d=1}^nd\sum_{i=1}^{s}\sum_{j=1}^{s}[\gcd(i,j)=1]$$
由推论得
$$\sum_{d=1}^nd\sum_{q=1}^s\mu(q)\left\lfloor\frac{s}{q}\right\rfloor^2$$
$$\sum_{d=1}^nd\sum_{q=1}^{\left\lfloor\frac{n}{d}\right\rfloor}\mu(q)\left\lfloor\frac{n}{dq}\right\rfloor^2$$
可以线性筛预处理 $\mu$ 的前缀和，枚举 $d$，对 $\left\lfloor\frac{s}{q}\right\rfloor$ 整除分块，时间复杂度 $O(n)$。
****
2.求
$$\sum_{i=1}^n\sum_{j=1}^m[\gcd(i,j)\in \text{prime}]$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P2257)

假设 $n\le m$

$$\sum_{k=1}^{k\le n,k\text{ is prime}}\sum_{i=1}^n\sum_{j=1}^m[\gcd(i,j)=k]$$
$$\sum_{k=1}^{k\le n,k\text{ is prime}}\sum_{i=1}^{\left\lfloor\frac{n}{k}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac{m}{k}\right\rfloor}[\gcd(i,j)=1]$$
$$\sum_{k=1}^{k\le n,k\text{ is prime}}\sum_{d=1}^n\mu(d)\left\lfloor\frac{n}{kd}\right\rfloor\left\lfloor\frac{m}{kd}\right\rfloor$$
令 $s=kd$

$$\sum_{k=1}^{k\le n,k\text{ is prime}}\sum_{d=1}^n\mu(d)\left\lfloor\frac{n}{s}\right\rfloor\left\lfloor\frac{m}{s}\right\rfloor$$
$$\sum_{s=1}^n\left\lfloor\frac{n}{s}\right\rfloor\left\lfloor\frac{m}{s}\right\rfloor\sum_{k|s}^{k\text{ is prime}}\mu(\frac s k)$$
右边那个可以预处理，就做完了，时间复杂度 $O(n+T\sqrt n)$。
****
3.求
$$\sum_{i=1}^n\sum_{j=1}^m\sigma(\gcd(i,j))[\sigma(\gcd(i,j))\le a]$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P3312)

假设 $n\le m$

先推
$$\sum_{i=1}^n\sum_{j=1}^m\sigma(\gcd(i,j))$$
$$\sum_{d=1}^n\sigma(d)\sum_{i=1}^{\left\lfloor\frac{n}{d}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac{m}{d}\right\rfloor}[\gcd(i,j)=1]$$
$$\sum_{d=1}^n\sigma(d)\sum_{p=1}^{\left\lfloor\frac{n}{d}\right\rfloor}\mu(p)\left\lfloor\frac{n}{dp}\right\rfloor\left\lfloor\frac{m}{dp}\right\rfloor$$
令 $s=dp$

$$\sum_{s=1}^n\sum_{d|s}\sigma(d)\mu(\frac s d)\left\lfloor\frac{n}{s}\right\rfloor\left\lfloor\frac{m}{s}\right\rfloor$$
$$\sum_{s=1}^n\left\lfloor\frac{n}{s}\right\rfloor\left\lfloor\frac{m}{s}\right\rfloor\sum_{d|s}\sigma(d)\mu(\frac s d)$$

令 $f(s)=\displaystyle\sum_{d|s}\sigma(d)\mu(\frac s d)[\sigma(d)\le a]$

现在要求 $\sigma(d)\le a$，则将询问离线，将 $a$ 从小到大排序，对新加入的 $\sigma(d)$ 枚举 $s$，对 $f(s)$ 加入 $\sigma(d)\mu(\frac s d)$ 的贡献。而进行整除分块是需要查询区间 $f(x)$ 和，于是采用树状数组维护 $f(x)$ 前缀和。时间复杂度 $O(n\log^2n+q\sqrt n\log n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/jc3kq7pc)
****
4.设 $f(n)=\displaystyle\sum_{d|n}[\sqrt d\in\Bbb N_+]$

求
$$k\text{ th number of }\{x|f(x)=0\}$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P4318)

即求
$$\min\{x|\sum_{i=1}^x\mu^2(i)=k\}$$

这个东西已经可以杜教筛了，但是我们讨论莫比乌斯反演。

可以二分答案，问题转为求 $[1,n]$ 内不含非 $1$ 完全平方数因子的数的个数。

考虑去掉所有质数的完全平方数的倍数，但是此时会有重复计算的，如 $36$ 被筛了三次。

所以需要容斥，我们发现只需容斥至 $\left\lfloor\sqrt n\right\rfloor$ 即可。

$$\sum_{i=1}^x\mu^2(i)$$
按照定义可以看为

>全体数 $-$ 为一个质因数的平方数的倍数的数的个数 $+$ 为两个不同质因数乘积的平方数的倍数的数的个数 $-$ 三个不同质数乘积的平方数的倍数的数的个数。

即可转化为
$$\sum_{i=1}^{\left\lfloor\sqrt n\right\rfloor}\mu(i)\left\lfloor\frac n{i^2}\right\rfloor$$
时间复杂度 $O(T\sqrt n\log n)$。
****
5.求
$$\sum_{i=1}^n\sum_{j=1}^m\text{lcm}(i,j)$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P1829)

假设 $n\le m$

$$\sum_{i=1}^n\sum_{j=1}^m\frac{ij}{\gcd(i,j)}$$
$$\sum_{i=1}^n\sum_{j=1}^m\sum_{d}\frac{ij}d[\gcd(i,j)=d]$$
$$\sum_{d=1}^nd\sum_{i=1}^{\left\lfloor\frac n{d}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac m{d}\right\rfloor}ij[\gcd(i,j)=1]$$

记 $f(n,m)=\displaystyle\sum_{i=1}^n\sum_{j=1}^mij[\gcd(i,j)=1],g(n,m)=\sum_{i=1}^n\sum_{j=1}^mij=\frac{n(n+1)}2\frac{m(m+1)}2$

**引理** $f(n,m)=\displaystyle\sum_{d=1}^n\mu(d)\cdot  d^2\cdot g(\left\lfloor\frac n{d}\right\rfloor,\left\lfloor\frac m{d}\right\rfloor)$

$$f(n,m)=\sum_{d=1}^n\sum_{d|i}^n\sum_{d|j}^m\mu(d)\cdot ij$$
记 $s=d\cdot i,t=d\cdot j$

$$f(n,m)=\sum_{d=1}^n\mu(d)\cdot  d^2\sum_{s=1}^{\left\lfloor\frac n{d}\right\rfloor}\sum_{t=1}^{\left\lfloor\frac m{d}\right\rfloor}ij$$
$$=\sum_{d=1}^n\mu(d)\cdot  d^2\frac{\left\lfloor\frac n{d}\right\rfloor(\left\lfloor\frac n{d}\right\rfloor+1)}2\cdot\frac{\left\lfloor\frac m{d}\right\rfloor(\left\lfloor\frac m{d}\right\rfloor+1)}2$$

即可前缀和搞定。

回到原式，

$$\sum_{d=1}^nd\cdot f(\left\lfloor\frac n{d}\right\rfloor,\left\lfloor\frac m{d}\right\rfloor)$$

时间复杂度 $O(n)=O(\sqrt n)\times O(\sqrt n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/orjaj2fw)

另解：
$$\sum_{d=1}^nd\sum_{i=1}^{\left\lfloor\frac n{d}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac m{d}\right\rfloor}ij[\gcd(i,j)=1]$$
$$\sum_{d=1}^nd\sum_{i=1}^{\left\lfloor\frac n{d}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac m{d}\right\rfloor}ij\sum_{q|\gcd(i,j)}\mu(q)$$
$$\sum_{d=1}^nd\sum_{q=1}^{\left\lfloor\frac n d\right\rfloor}q^2\mu(q)\cdot g(\left\lfloor\frac n {dq}\right\rfloor,\left\lfloor\frac m {dq}\right\rfloor)$$
令 $s=dq$

$$\sum_{s=1}^ng(\left\lfloor\frac n {s}\right\rfloor,\left\lfloor\frac m {s}\right\rfloor)\sum_{dq=s}dq^2\mu(q)$$
$$\sum_{s=1}^ng(\left\lfloor\frac n {s}\right\rfloor,\left\lfloor\frac m {s}\right\rfloor)\cdot s\sum_{q|s}q\mu(q)$$
右边那堆可以线性筛预处理。

于是现在询问的复杂度将至 $O(\sqrt n)$，可以出成多组数据，时间复杂度 $O(n+T\sqrt n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/q58v85vt)
****
6.给 $a_{1,2,...,n}$，求
$$\sum_{i=1}^n\sum_{j=1}^n\text{lcm}(a_i,a_j)$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P3911)

记 $c_i=\displaystyle\sum_{k=1}^n[a_k=i],v=\max_{k=1}^n(a_k)$

$$\sum_{i=1}^v\sum_{j=1}^v\text{lcm}(i,j)\cdot c_ic_j$$
$$\sum_{i=1}^v\sum_{j=1}^v\frac{ijc_ic_j}{\gcd(i,j)}$$
$$\sum_{i=1}^v\sum_{j=1}^v\sum_{d}\frac{ijc_ic_j}d[\gcd(i,j)=d]$$
$$\sum_{d=1}^vd\sum_{i=1}^{\left\lfloor\frac v{d}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac v{d}\right\rfloor}ijc_ic_j[\gcd(i,j)=1]$$
$$\sum_{d=1}^vd\sum_{i=1}^{\left\lfloor\frac v{d}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac v{d}\right\rfloor}ijc_ic_j\sum_{q|\gcd(i,j)}\mu(q)$$
$$\sum_{d=1}^vd\sum_{q=1}^{\left\lfloor\frac v{d}\right\rfloor}q^2\mu(q)\sum_{i=1}^{\left\lfloor\frac v{dq}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac v{dq}\right\rfloor}ijc_ic_j$$
令 $s=dq$

$$\sum_{s=1}^v(\sum_{i=1}^{\left\lfloor\frac v{s}\right\rfloor}c_{is}\cdot i)^2\cdot s\sum_{q|s}q\mu(q)$$

筛一下就能 $O(v\ln v)$ 了。
****
7.设 $f(x)$ 为 $n$ 所含质因子的最大幂指数，求
$$\sum_{i=1}^n\sum_{j=1}^mf(\gcd(i,j))$$
[$\text{Link}$](https://acm.taifua.com/bzoj/p/3309.html)

设 $n\le m$

$$\sum_{d=1}^nf(d)\sum_{i=1}^{\left\lfloor\frac n{d}\right\rfloor}\sum_{j=1}^{\left\lfloor\frac m{d}\right\rfloor}[\gcd(i,j)=1]$$
$$\sum_{d=1}^nf(d)\sum_{q=1}^{\left\lfloor\frac n{d}\right\rfloor}\mu(q)\left\lfloor\frac n{dq}\right\rfloor\left\lfloor\frac m{dq}\right\rfloor$$
令 $s=dq$

$$\sum_{s=1}^n\left\lfloor\frac n{s}\right\rfloor\left\lfloor\frac m{s}\right\rfloor\sum_{d|s}f(d)\mu(\frac s d)$$
写出 $s$ 的标准分解式 $s=\displaystyle\prod_{i=1}^kp_i^{q_i}$，因为 $\mu$ 不为 $0$ 当且仅当所有质因子指数为 $1$，所以只有 $2^k$ 个对应的 $d$。如果确定最高次幂 $p_x^{q_x-1}$，剩余的位都能选或不选，此时的 $\mu$ 也相对应地都为 $1,-1$，$f(d)$ 也均相等，和为 $0$。

若全部次幂完全相同，即 $s=\displaystyle\prod_{i=1}^kp_i^q$，则 $d=\displaystyle\prod_{i=1}^kp_i^{q-1}$ 时 $f(d)=q-1$，其余时候 $f(d)=q$。

由于有一情况 $f(d)=q-1$，其贡献为 $-1\times\mu(\displaystyle\prod_{i=1}^kp_i)=-1^{n+1}$.

时间复杂度 $O(n+T\sqrt n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/xg6canvg)
****
注意：以下题目的难度顺序可能不递增
****
8.求
$$\prod_{i=1}^n\prod_{j=1}^n\frac{\text{lcm}(i,j)}{\gcd(i,j)}$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P5221)
$$\prod_{i=1}^n\prod_{j=1}^n\frac{ij}{\gcd(i,j)^2}$$
$$\frac{\prod_{i=1}^n\prod_{j=1}^nij}{\prod_{i=1}^n\prod_{j=1}^n\gcd(i,j)^2}$$
考虑分开做，分子
$$\prod_{i=1}^n\prod_{j=1}^nij$$
$$\prod_{i=1}^ni^nn!$$
$$(n!)^{2n}$$
分母
$$\prod_{i=1}^n\prod_{j=1}^n\gcd(i,j)^2$$
$$\prod_{d=1}^nd^{2\sum_{i=1}^n\sum_{j=1}^n[\gcd(i,j)=d]}$$
$$\prod_{d=1}^nd^{2\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q)\lfloor\frac n {dq}\rfloor^2}$$

然后就可以整除分块了，时间复杂度 $O(n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/ej8oh1m2)
****
9.求
$$\sum_{i=1}^n\sum_{j=1}^md(ij)$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P3327)

**引理** $d(ij)=\displaystyle\sum_{x|i}\sum_{y|j}[\gcd(x,y)=1]$

留坑。
$$\sum_{i=1}^n\sum_{j=1}^m\sum_{x|i}\sum_{y|j}[\gcd(x,y)=1]$$
$$\sum_{x=1}^n\sum_{y=1}^m\left\lfloor\frac{n}{x}\right\rfloor\left\lfloor\frac{m}{y}\right\rfloor[\gcd(x,y)=1]$$
改写 $x,y$ 为 $i,j$

$$\sum_{i=1}^n\sum_{j=1}^m\left\lfloor\frac{n}{i}\right\rfloor\left\lfloor\frac{m}{j}\right\rfloor[\gcd(i,j)=1]$$
设
$$f(x)=\sum_{i=1}^n\sum_{j=1}^m\left\lfloor\frac{n}{i}\right\rfloor\left\lfloor\frac{m}{j}\right\rfloor[\gcd(i,j)=x]$$
$$g(x)=\sum_{x|d}^nf(d)$$
$$=\sum_{i=1}^n\sum_{j=1}^m\left\lfloor\frac{n}{i}\right\rfloor\left\lfloor\frac{m}{j}\right\rfloor[x|\gcd(i,j)]$$
$$=\sum_{i=1}^{\lfloor\frac n x\rfloor}\sum_{j=1}^{\lfloor \frac m x\rfloor}\left\lfloor\frac{n}{ix}\right\rfloor\left\lfloor\frac{m}{jx}\right\rfloor$$
根据**莫比乌斯反演公式**，有
$$f(x)=\sum_{x|d}^n\mu(d)g(\frac d x)$$
$$f(1)=\sum_{d=1}^n\mu(d)g(d)$$
$g(x)$ 可以通过预处理 $\displaystyle\sum_{i=1}^q\lfloor\frac q i\rfloor\;O(1)$ 得出。时间复杂度 $O(n\sqrt n+T\sqrt n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/boxwo62k)

另解：

此下令 $n=m$

$$\sum_{i=1}^n\sum_{j=1}^n\sum_{x|i}\sum_{y|j}[\gcd(x,y)=1]$$
$$\sum_{d=1}^n\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac n d\rfloor}\sum_{p=1}^{\lfloor\frac n {id}\rfloor}\sum_{q=1}^{\lfloor\frac n {jd}\rfloor}[\gcd(x,y)=1]$$
$$\sum_{d=1}^n\mu(d)(\sum_{i=1}^{\lfloor\frac n d\rfloor}\lfloor\frac n {id}\rfloor)^2$$

使用杜教筛，求 $\mu$ 的前缀和可以做到 $O(n^{\frac 2 3}+n^{\frac 3 4})$ 的时间复杂度。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/7p437hc4)
****
10.求
$$\sum_{i=1}^n i^k[\gcd(i,n)=1]$$
其中
$$n=\prod_{i=1}^wp_i^{q_i}$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P6271)

设
$$f(n)=\sum_{i=1}^ni^k$$
$$g(n)=\sum_{i=1}^n i^k[\gcd(i,n)=1]$$
$$f(n)=\sum_{d|n}d^kg(\frac  nd)$$
由**莫比乌斯反演公式**得 
$$g(n)=\sum_{d|n}\mu(d)d^kf(\frac n d)$$
众所周知，自然数幂和 $f(n)$ 是关于 $n$ 的 $k+1$ 次多项式，写成 $f(n)=\displaystyle\sum_{i=0}^{k+1}f_in^i$，代回得
$$g(n)=\sum_{d|n}\mu(d)d^k\sum_{i=0}^{k+1}f_i(\frac n d)^i$$
$$g(n)=\sum_{i=0}^{k+1}f_in^i\sum_{d|n}\mu(d)d^{k-i}$$
因为 $n=\displaystyle\prod_{i=1}^wp_i^{q_i}$，代入得
$$g(n)=\sum_{i=0}^{k+1}f_in^i\prod_{j=1}^w\sum_{q=1}^{q_j}\mu(p_j^q)p_j^{q(k-i)}$$
从 $\mu$ 的意义入手化简得
$$g(n)=\sum_{i=0}^{k+1}f_in^i\prod_{j=1}^w(1-p_j^{k-i})$$
现在只需求自然数 $k$ 次幂和的多项式即可，这个可以看 [$\text{Here}$](https://www.luogu.com.cn/problem/CF622F)，这里不讲.

时间复杂度可以做到 $O(k^2+kw)$ 或者 $O(k^3+kw)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/jsqwqjfi)

[$\text{Next}$](https://www.luogu.com.cn/blog/cyffff/mu-bi-wu-si-fan-yan-xue-xi-bi-ji-ii)
