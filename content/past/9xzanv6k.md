---
title: "生成函数摘抄"
date: 2021-07-14
category: "个人记录"
tags: ["学习笔记"]
summary: "前置：微积分 导数的定义 y=f(x),f'(x0)= dydx = x→ 0 y x= x→0f(x0+ x)-f(x0) x 常见导数表 | f(x) | f'(x) | "
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/9xzanv6k
slug: 9xzanv6k
---

### 前置：微积分

**导数的定义**

$$y=f(x),f'(x_0)=\frac {\text{d}y}{\text{d}x} =\lim_{\Delta x\to 0}\dfrac{\Delta y}{\Delta x}=\lim_{\Delta x\to0}\dfrac{f(x_0+\Delta x)-f(x_0)}{\Delta x}$$

**常见导数表**

| $f(x)$ | $f'(x)$ |
| :----------: | :----------: |
| $c$ | $0$ |
| $x^n$ | $nx^{n-1}$ |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $a^x$ | $a^x\ln a$ |
| $e^x$ | $e^x$ |
| $\log_ax$ | $\frac 1 {x\ln a}$ |
| $\ln x$ | $\frac 1 x$ |

**导数四则运算**
- $[f(x)\pm g(x)]'=f'(x)\pm g'(x)$
- $[f(x)\times g(x)]'=f'(x)g(x)+f(x)g'(x)$
- $[\dfrac {f(x)}{g(x)}]'=\dfrac{f'(x)g(x)-f(x)g'(x)}{g^2(x)}$
- $[cf(x)]'=cf'(x)$

**复合函数求导**
$$u=g(x),y=f(u)$$
$$\to y=f(g(x))$$
$$y_x'=y_u'\times u_x'$$
**牛顿迭代公式** 

$$x_n=x_{n-1}-\dfrac{f(x_{n-1})}{f'(x_{n-1})}$$

**定积分的定义**
$$\int^b_af(x)\text{d}x=\lim_{n\to\infty}\sum_{i=1}^n\frac {b-a}{n}f(\xi_i)$$
**定积分运算**

- $\displaystyle\int_a^bcf(x)\text{d}x=c\int_a^bf(x)\text{d}x$
- $\displaystyle\int_a^b[f(x)\pm g(x)]\text{d}x=\int_a^bf(x)\text{d}x\pm\int_a^bg(x)\text{d}x$
- $\displaystyle\int_a^bf(x)\text{d}x=\int_a^cf(x)\text{d}x+\int_c^bf(x)\text{d}x\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\;\;\;\;(a<c<b)$

**不定积分的定义**
$$\int f(x)=F(x)\to F'(x)=f(x)$$

**不定积分运算**

- $\displaystyle\int cf(x)\text{d}x=c\int f(x)\text{d}x$
- $\displaystyle\int [f(x)\pm g(x)]\text{d}x=\int f(x)\text{d}x\pm\int g(x)\text{d}x$

**牛顿-莱布尼茨公式**
$$F'(x)=f(x)$$
$$\to\int_a^bf(x)\text{d}x=F(x)|_a^b=F(b)-F(a)$$

****
### 前置：组合数学
**广义二项式定理**

$$(1+x)^a=\sum_{i\ge0}\binom a ix^i$$
****
## 普通型生成函数 $\text{OGF}$
#### 定义
对于序列 $\{f_i\}$，其生成函数为 $F(x)=\sum_{n\ge0}f_nx^n$，即 $[x^n]F(x)=f_n$。
#### 三则运算
- $\displaystyle\left(\sum_{n\ge0}f_nx^n\right)\pm\left(\sum_{n\ge0}g_nx^n\right)=\sum_{n\ge0}\left(f_n\pm g_n\right)x^n$
- $\displaystyle c\times\left(\sum_{n\ge0}f_nx^n\right)=\sum_{n\ge0}cf_nx^n$
- $\displaystyle\left(\sum_{n\ge0}f_nx^n\right)\times\left(\sum_{n\ge0}g_nx^n\right)=\sum_{n\ge0}\left(\sum_{i=0}^nf_ig_{n-i}\right)x^n$

乘法法则中，得到的生成函数对应的序列 $\{h_n=\sum_{i=0}^nf_ig_{n-i}\}$ 称为 $f$ 序列与 $g$ 序列的**卷积**。
#### 移位
- $\displaystyle x^m\sum_{n\ge0}f_nx^n=\sum_{n\ge 0}f_{n}x^{n+m}=\sum_{n\ge m}f_{n-m}x^n$
- $\displaystyle \dfrac 1 {x^m}\left(\sum_{n\ge0}f_nx^n-\sum_{n=0}^{m-1}f_nx^n\right)=\sum_{n\ge0}f_{n+m}x^n$

#### 微积分
- $\displaystyle\dfrac{\text{d}}{\text{d}x}\left(\sum_{n\ge0}f_nx^n\right)=\sum_{n\ge1}nf_{n}x^{n-1}$
- $\displaystyle\int\left(\sum_{n\ge0}f_nx^n\right)\text{d}x=\sum_{n\ge0}\dfrac{f_{n-1}}{n}x^n+c$

#### 常见 $\text{OGF}$ 表
| $f_n=[n=m]$ | $\sum_{n\ge0}[n=m]x^n$ | $x^m$ |
| :----------: | :----------: | :----------: |
| $f_n=1$ | $\sum_{n\ge0}x^n$ | $\dfrac{1}{1-x}$ |
| $f_n=[n\ge m ]$ | $\sum_{n\ge m}x^n$ | $\dfrac {x^m} {1-x}$ |
| $f_n=c^n$ | $\sum_{n\ge0}c^nx^n$ | $\dfrac 1 {1-cx}$ |
| $f_n=\binom{n+k-1}{n}$ | $\sum_{n\ge0}\binom{n+k-1}nx^n$ | $\dfrac1{(1-x)^k}$ |
| $f_n=\dfrac{c^n}{n!}$ | $\sum_{n\ge0}\dfrac{c^nx^n}{n!}$ | $e^{cx}$ |
| $f_n=\dfrac{(-1)^{n-1}}n$ | $\sum_{n\ge0}\dfrac{(-1)^{n-1}}{n}x^n$ | $\ln(1+x)$ |
| $f_n=\dfrac 1 n$ | $\sum_{n\ge0}\dfrac 1 nx^n$ | $\ln\dfrac1{1-x}$ |

### 特殊数列
#### 斐波那契数列
$$F(x)=\sum_{n\ge0}f_nx^n$$
$$F(x)=\sum_{n\ge0}(f_{n-1}+f_{n-2})x^n$$
$$F(x)=1+xF(x)+x^2F(x)$$
$$F(x)-xF(x)-x^2F(x)=1$$
$$(1-x-x^2)F(x)=1$$
$$F(x)=\dfrac 1 {1-x-x^2}$$
#### 前缀和
$$s_n=\sum_{i=0}^nf_i$$
$$S(x)=\sum_{n\ge0}s_nx^n$$
$$S(x)=\sum_{n\ge0}\left(\sum_{i=0}^nf_i\right)x^n$$
$$S(x)=\sum_{i\ge0}f_i\sum_{n\ge i}x^n$$
$$S(x)=\sum_{i\ge0}f_i\dfrac {x^i}{1-x}$$
$$S(x)=\dfrac {1}{1-x}\sum_{i\ge0}f_ix^i$$
$$S(x)=\dfrac {1}{1-x}F(x)$$
### 例 [$\text{CF438E}$](https://www.luogu.com.cn/problem/CF438E)
$f_i$ 表示权值为 $i$ 的答案，$g_i=[i\in\{c_i\}]$

$$f_n=[n=0]+\sum_{i\ge1}g_i\sum_{j=1}^{n-i}f_jf_{n-i-j}$$

写出 $f$，$g$ 数列的生成函数

$$F(x)=\sum_{n\ge0}f_nx^n$$
$$F(x)=1+\sum_{n\ge0}\sum_{i\ge1}g_i\sum_{j=1}^{n-i}f_jf_{n-i-j}x^n$$
$$F(x)=1+G(x)F^2(x)$$
$$G(x)F^2(x)-F(x)+1=0$$
$$F(x)=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}=\dfrac{1\pm\sqrt{1-4G(x)}}{2G(x)}$$
$$2F(x)G(x)=1\pm\sqrt{1-4G(x)}$$
考虑取 $+$

$$[x^0]2F(x)G(x)=0,[x^0]1+\sqrt{1-4G(x)}\ne0$$
故不取 $+$，则有

$$F(x)=\dfrac{1-\sqrt{1-4G(x)}}{2G(x)}$$

$[x^0]G(x)=0$，无法对 $G(x)$ 求逆，考虑上下同乘 $1+\sqrt{1-4G(x)}$

$$F(x)=\dfrac{4G(x)}{2G(x)+2G(x)\sqrt{1-4G(x)}}$$
$$F(x)=\dfrac{2}{1+\sqrt{1-4G(x)}}$$
