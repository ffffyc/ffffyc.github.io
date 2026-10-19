---
title: "莫比乌斯反演学习笔记 II"
date: 2021-07-12
category: "个人记录"
tags: ["学习笔记"]
summary: "Prod 如无特殊说明，n≤ m。 狄利克雷卷积 (fg)=Σd|nf(d)g( n d) f=f I= I=id id= 莫比乌斯反演 f(n)=Σd|ng(d)→ g(n)"
math: true
top: 2
source: https://www.luogu.com.cn/article/rfimhsac
slug: rfimhsac
---

[$\text{Prod}$](https://www.luogu.com.cn/blog/cyffff/mu-bi-wu-si-fan-yan-xue-xi-bi-ji)

如无特殊说明，$n\le m$。

**狄利克雷卷积** $(f*g)=\displaystyle\sum_{d|n}f(d)g(\frac n d)$
- $f*\epsilon=f$
- $\mu*I=\epsilon$
- $\varphi*I=id$
- $\mu*id=\varphi$

**莫比乌斯反演** $f(n)=\displaystyle\sum_{d|n}g(d)\to g(n)=\displaystyle\sum_{d|n}\mu(d)f(\frac n d)$

$\displaystyle\sum_{d|n}\mu(d)=[n=1]$

$\displaystyle\sum_{i=1}^n\displaystyle\sum_{j=1}^m[\gcd(i,j)=1]=\displaystyle\sum_{d=1}^{n}\mu(d)\left\lfloor\frac{n}{d}\right\rfloor\left\lfloor\frac{m}{d}\right\rfloor$

$\displaystyle\sum_{i=1}^n\sum_{j=1}^mf(\gcd(i,j))=\sum_{s=1}^n\left\lfloor\frac n{s}\right\rfloor\left\lfloor\frac m{s}\right\rfloor\sum_{d|s}f(d)\mu(\frac s d)$
****
11.求
$$\sum_{i=1}^n\sum_{j=1}^nij\gcd(i,j)$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P3768)
$$\sum_{d=1}^nd^3\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac n d\rfloor}ij[\gcd(i,j)=1]$$
$$\sum_{d=1}^nd^3\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac n d\rfloor}ij\sum_{q|i}\sum_{q|j}\mu(q)$$
$$\sum_{d=1}^nd^3\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q)q^2\sum_{i=1}^{\lfloor\frac n {dq}\rfloor}\sum_{j=1}^{\lfloor\frac n {dq}\rfloor}ij$$
例 $5$ 中有
$$g(n)=\sum_{i=1}^n\sum_{j=1}^nij=\frac{n^2(n+1)^2}4$$
$$\sum_{d=1}^nd^3\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q)q^2g(\lfloor\frac n {dq}\rfloor)$$
令 $t=dq$

$$\sum_{t=1}^ng(\lfloor\frac n {t}\rfloor)\sum_{d|t}d^3\mu(\frac t d)(\frac t d)^2$$
$$\sum_{t=1}^ng(\lfloor\frac n {t}\rfloor)\sum_{d|t}d\mu(\frac t d) t^2$$
$$\sum_{t=1}^ng(\lfloor\frac n {t}\rfloor) t^2\sum_{d|t}d\mu(\frac t d)$$
可以看出，后面是狄利克雷卷积的形式，即有 $\mu*id=\varphi$

$$\sum_{t=1}^ng(\lfloor\frac n {t}\rfloor) t^2\varphi(t)$$
记 $f(x)=x^2\varphi(x)$，显然为积性函数，于是考虑 $h(x)$ 使得 $(f*h)(x)$ 可以快速计算
$$(f*h)(x)=\sum_{d|x}d^2\varphi(d)h(\frac x d)$$
想要约去 $d^2$，则可设计函数 $h(x)=x^2$

$$(f*h)(x)=x^2\sum_{d|x}\varphi(d)$$
欧拉反演得
$$(f*h)(x)=x^3$$
接下来考虑杜教筛，记 
$$S(n)=\sum_{i=1}^nf(i)$$
$$h(1)S(n)=\sum_{i=1}^nh(i)S(\lfloor\frac n i\rfloor)-\sum_{i=2}^nh(i)S(\lfloor\frac n i\rfloor)$$
$$S(n)=\sum_{i=1}^nh(i)S(\lfloor\frac n i\rfloor)-\sum_{i=2}^nh(i)S(\lfloor\frac n i\rfloor)$$
先算前面的
$$\sum_{i=1}^nh(i)S(\lfloor\frac n i\rfloor)$$
$$\sum_{i=1}^nh(i)\sum_{j=1}^{\lfloor\frac n i\rfloor}f(j)$$
$$\sum_{j=1}^n\sum_{i|j}f(j)h(\frac j i)$$
$$\sum_{j=1}^n(f*h)(j)$$

$$\sum_{j=1}^nj^3$$
$$g(n)$$
$$S(n)=g(n)-\sum_{i=2}^nh(i)S(\lfloor\frac n i\rfloor)$$
为了达到 $O(n^{\frac 2 3})$ 的时间复杂度，需要预处理 $S(1)$ 至 $S(\lfloor n^{\frac 2 3}\rfloor)$ 的值，可以用 $S(n)=S(n-1)+n^2\varphi(n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/lwv0wnqm)
****
12.求
$$\sum_{i=1}^n\sum_{j=1}^n(i+j)^k\gcd(i,j)\mu^2(\gcd(i,j)))$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P6222)
$$\sum_{d=1}^n\mu^2(d)d^{k+1}\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac n d\rfloor}(i+j)^k[\gcd(i,j)=1]$$
$$\sum_{d=1}^n\mu^2(d)d^{k+1}\sum_{q=1}^{\lfloor\frac n {d}\rfloor}\mu(q)q^k\sum_{i=1}^{\lfloor\frac n {dq}\rfloor}\sum_{j=1}^{\lfloor\frac n {dq}\rfloor}(i+j)^k$$
记 $\displaystyle f_k(x)=\sum_{i=1}^{x}\sum_{j=1}^{x}(i+j)^k,s=dq$

$$\sum_{d=1}^n\mu^2(d)d^{k+1}\sum_{q=1}^{\lfloor\frac n {d}\rfloor}\mu(q)q^kf_k(\lfloor\frac n {s}\rfloor)$$
$$\sum_{s=1}^nf_k(\lfloor\frac n {s}\rfloor)\sum_{d|s}\mu^2(d)d^{k+1}\mu(\frac s d)(\frac s d)^k$$
$$\sum_{s=1}^nf_k(\lfloor\frac n {s}\rfloor)s^k\sum_{d|s}\mu^2(d)d\mu(\frac s d)$$
令
$$g(x)=\sum_{i=1}^xi^k$$
$$h(x)=\sum_{i=1}^xg(i)$$
$$f_k(n)=\sum_{i=n+1}^{2n}\sum_{j=1}^i j^k-\sum_{i=1}^n\sum_{j=1}^i j^k$$
$$f_k(n)=\sum_{i=n+1}^{2n}g(i)-\sum_{i=1}^ng(i)$$
$$f_k(n)=h(2n)-2h(n)$$
就可以线性筛预处理了。

$$F(x)=\sum_{d|x}\mu^2(d)\mu(\frac x d)d$$
是 $(x)=\mu^2(x)x$ 与 $(x)=\mu(x)$ 的狄利克雷卷积，为积性函数。

于是只需考虑 $F(p^k)$ 即可。

- $k=0$，$F(1)=1$；
- $k=1$，$F(p)=\mu(p)+\mu^2(p)p=p-1$；
- $k=2$，$F(p^2)=\mu^3(p)p=-p$；
- $k\ge3$，$\mu(p^c)=0\text{ or }\mu(p^{k-c})=0,F(p^k)=0$。

推完了，时间复杂度 $O(n+T\sqrt n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/pwfy2aqi)
****
13.求
$$\sum_{i=1}^n\sum_{j=1}^m\gcd(i,j)^k$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P4449)

$$\sum_{d=1}^nd^k\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac m d\rfloor}\sum_{q|\gcd(i,j)}\mu(q)$$
$$\sum_{d=1}^nd^k\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q)\lfloor\frac n {dq}\rfloor\lfloor\frac m {dq}\rfloor$$
令 $s=dq$

$$\sum_{s=1}^n\lfloor\frac n {s}\rfloor\lfloor\frac m {s}\rfloor\sum_{d|s}d^k\mu(\frac s d)$$
只需求 $f(x)=\displaystyle\sum_{d|x}d^k\mu(\frac x d)$ 的前缀和即可，注意到 $f$ 是积性函数，设
$$x=\prod_{i=1}^yp_i^{q_i}$$
$$f(x)=\prod_{i=1}^yf(p_i^{q_i})$$
$$\prod_{i=1}^yp_i^{k(q_i-1)}\mu(p_i)+p_i^{kq_i}\mu(1)$$
$$\prod_{i=1}^yp_i^{k(q_i-1)}(p_i^{k}-1)$$
就可以线性筛了，时间复杂度 $O(n+T\sqrt n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/ddwecn35)
****
14.求
$$\sum_{i=1}^n\sum_{j=1}^n\gcd(i,j)^{i+j}$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P6825)

$$\sum_{d=1}^n\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac n d\rfloor}[\gcd(i,j)=1]d^{id+jd}$$
$$\sum_{d=1}^n\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac n d\rfloor}d^{id+jd}\sum_{q|\gcd(i,j)}\mu(q)$$
$$\sum_{d=1}^n\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q)\sum_{i=1}^{\lfloor\frac n {dq}\rfloor}\sum_{j=1}^{\lfloor\frac n {dq}\rfloor}d^{idq+jdq}$$
令 $s=dq$

$$\sum_{d=1}^n\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q)\sum_{i=1}^{\lfloor\frac n {s}\rfloor}\sum_{j=1}^{\lfloor\frac n {s}\rfloor}d^{is+js}$$
$$\sum_{d=1}^n\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q)\sum_{i=1}^{\lfloor\frac n {s}\rfloor}d^{is}\sum_{j=1}^{\lfloor\frac n {s}\rfloor}d^{js}$$
$$\sum_{d=1}^n\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q){\left(\sum_{i=1}^{\lfloor\frac n {s}\rfloor}{(d^{s})}^i\right)}^2$$

设 $S_n$ 为等比数列前 $n$ 项和，$a$ 为共商。

$$S_n=S_{\lfloor\frac 2 n\rfloor}(1+a^{\lfloor\frac 2 n\rfloor})+a^n[2\nmid n]$$

即可 $O(\log n)$ 求解。

最终时间复杂度为 $O(n\log n)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/o6rpsk6f)
****
15.设 $f_x$ 表示斐波那契数列第 $x$ 项，求
$$\prod_{i=1}^n\prod_{j=1}^mf_{\gcd(i,j)}$$

[$\text{Link}$](https://www.luogu.com.cn/problem/P3704)
$$\prod_{d=1}^nf_d^{\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac m d\rfloor}[\gcd(i,j)=1]}$$
考虑指数
$$\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac m d\rfloor}[\gcd(i,j)=1]$$
$$\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q){\lfloor\frac n {dq}\rfloor}{\lfloor\frac m {dq}\rfloor}$$
令 $s=dq$

$$\prod_{d=1}^nf_d^{\sum_{q=1}^{\lfloor\frac n d\rfloor}\mu(q){\lfloor\frac n {s}\rfloor}{\lfloor\frac m {s}\rfloor}}$$
$$\prod_{s=1}^n\prod_{d|s}f_d^{\mu(\frac s d){\lfloor\frac n {s}\rfloor}{\lfloor\frac m {s}\rfloor}}$$
$$\prod_{s=1}^n{\left(\prod_{d|s}f_d^{\mu(\frac s d)}\right)}^{{\lfloor\frac n {s}\rfloor}{\lfloor\frac m {s}\rfloor}}$$

时间复杂度 $O(n\ln n+n\log\bmod+T\sqrt n\log\bmod)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/0r4tpit5)
****
16.
$$\sum_{i=1}^n\sum_{j=1}^m[\gcd(i,j)=1][\gcd(j,k)=1]$$
[$\text{Link}$](https://www.luogu.com.cn/problem/P1587)
$$\sum_{i=1}^n\sum_{j=1}^m[\gcd(i,j)=1][\gcd(j,k)=1]$$
$$\sum_{i=1}^n\sum_{j=1}^m\sum_{d|\gcd(i,j)}\mu(d)[\gcd(j,k)=1]$$
$$\sum_{d=1}^n\mu(d)\sum_{d|i}^n\sum_{d|j}^m[\gcd(j,k)=1]$$
$$\sum_{d=1}^n\mu(d)\sum_{i=1}^{\lfloor\frac n d\rfloor}\sum_{j=1}^{\lfloor\frac m d\rfloor}[\gcd(jd,k)=1]$$
$$\sum_{d=1}^n\mu(d)[\gcd(d,k)=1]\lfloor\frac n d\rfloor\sum_{j=1}^{\lfloor\frac m d\rfloor}[\gcd(j,k)=1]$$
$$\begin{aligned}g(n)&=\sum_{i=1}^n[\gcd(i,k)=1]\\
&=\lfloor\frac n k\rfloor\sum_{i=1}^k[\gcd(i,k)=1]+g(n\bmod k)\\
&=\lfloor\frac n k\rfloor\varphi(k)+g(n\bmod k)\end{aligned}$$
$$\sum_{d=1}^n\mu(d)[\gcd(d,k)=1]\lfloor\frac n d\rfloor g\left(\lfloor\frac m d\rfloor\right)$$
$$\begin{aligned}f(n)&=\sum_{i=1}^n\mu(i)[\gcd(i,k)=1]\\
&=\sum_{i=1}^n[\gcd(i,k)=1]f\left(\lfloor\frac n d\rfloor\right)-\sum_{i=2}^n[\gcd(i,k)=1]f\left(\lfloor\frac n d\rfloor\right)\\
&=\sum_{i=1}^n\sum_{j=1}^{\lfloor\frac n i\rfloor}\mu(j)[\gcd(ij,k)=1]-\sum_{i=2}^n[\gcd(i,k)=1]f\left(\lfloor\frac n d\rfloor\right)\\
&=\sum_{q=1}^n[\gcd(q,k)=1]\sum_{d|q}\mu(d)-\sum_{i=2}^n[\gcd(i,k)=1]f\left(\lfloor\frac n d\rfloor\right)\\
&=\sum_{q=1}^n[\gcd(q,k)=1][q=1]-\sum_{i=2}^n[\gcd(i,k)=1]f\left(\lfloor\frac n d\rfloor\right)\\
&=1-\sum_{i=2}^n[\gcd(i,k)=1]f\left(\lfloor\frac n d\rfloor\right)\end{aligned}$$
时间复杂度 $O(n^{\frac 2 3}+k\log k)$。

代码：[$\text{Here}$](https://www.luogu.com.cn/paste/jcsnwdok)
