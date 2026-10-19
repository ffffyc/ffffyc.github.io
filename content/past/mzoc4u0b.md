---
title: "简单多项式板子"
date: 2021-07-15
category: "个人记录"
tags: ["学习笔记"]
summary: "Inv(F) F G1( xn) F G'1( x n 2) F (G-G')0( x n 2) G-G'0( x n 2) (G-G')20( xn) G2+G'2-2GG'"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/mzoc4u0b
slug: mzoc4u0b
---

### [$\text{Inv}(F)$](https://www.luogu.com.cn/problem/P4238)
$$F\cdot G\equiv1(\bmod x^n)$$
$$F\cdot G'\equiv1(\bmod x^{\frac n 2})$$
$$F\cdot (G-G')\equiv0(\bmod x^{\frac n 2})$$
$$G-G'\equiv0(\bmod x^{\frac n 2})$$
$$(G-G')^2\equiv0(\bmod x^{n})$$
$$G^2+G'^2-2GG'\equiv0(\bmod x^n)$$
$$F(G^2+G'^2-2GG')\equiv0(\bmod x^n)$$
$$G+FG'^2-2G'\equiv0(\bmod x^n)$$
$$G\equiv 2G'-FG'^2(\bmod x^n)$$

$T(n)=T(\frac n 2)+O(n\log n)=O(n\log n)$
### [$\text{sqrt}(F)$](https://www.luogu.com.cn/problem/P5205)
$$F\equiv G^2(\bmod x^n)$$
$$F\equiv G'^2(\bmod x^{\frac n 2})$$
$$G^2-G'^2\equiv 0(\bmod x^{\frac n 2})$$
$$(G^2-G'^2)^2\equiv 0(\bmod x^n)$$
$$G^4+G'^4-2G^2G'^2\equiv 0(\bmod x^n)$$
$$G^4+G'^4+2G^2G'^2\equiv 4G^2G'^2(\bmod x^n)$$
$$G^2+G'^2\equiv 2GG'(\bmod x^n)$$
$$F+G'^2\equiv 2GG'(\bmod x^n)$$
$$G\equiv \dfrac{F+G'^2}{2G'}(\bmod x^n)$$

$T(n)=T(\frac n 2)+O(n\log n)=O(n\log n)$
### [$\ln(F)$](https://www.luogu.com.cn/problem/P4725)
$$f(x)=\ln x$$
$$G\equiv f(F)(\bmod x^n)$$
$$G'\equiv f(F)'(\bmod x^n)$$
$$G'\equiv f'(F)F'(\bmod x^n)$$
$$G'\equiv \frac {F'}{F}(\bmod x^n)$$
$$\int G'\equiv \int\frac {F'}{F}(\bmod x^n)$$
$$G\equiv \int\frac {F'}{F}(\bmod x^n)$$

$O(n\log n)$
### [$\exp (F)$](https://www.luogu.com.cn/problem/P4726)
$$G\equiv \exp F(\bmod x^n)$$
$$\ln G-F\equiv 0(\bmod x^n)$$
$$f(G)=\ln G-F$$
$$f'(G)\equiv\frac {1}{G}(\bmod x^n)$$
$$G\equiv G_0-\dfrac{f(G_0)}{f'(G_0)}(\bmod x^n)$$
$$G\equiv G_0-\dfrac{\ln G_0-F}{\frac 1 {G_0}}(\bmod x^n)$$
$$G\equiv G_0-G_0\ln G_0-F(\bmod x^n)$$
$$G\equiv G_0(1-\ln G_0+F)(\bmod x^n)$$

$T(n)=T(\frac n 2)+O(n\log n)=O(n\log n)$
### [$\text{pow}(F,k)$](https://www.luogu.com.cn/problem/P5273)
$$G\equiv F^k(\bmod x^n)$$
$$\ln G\equiv k\ln F(\bmod x^n)$$
$$\exp\ln G\equiv \exp (k\ln F)(\bmod x^n)$$
$$G\equiv e^{k\ln F}(\bmod x^n)$$

$O(n\log n)$
### [$\text{div}(F,G)$](https://www.luogu.com.cn/problem/P4512)
$$F(x)= Q(x)\cdot G(x)+R(x)$$
$$F(\frac 1x)= Q(\frac1x)\cdot G(\frac1x)+R(\frac1x)$$
$$F(\frac 1x)= Q(\frac1x)\cdot G(\frac1x)+R(\frac1x)$$
$$x^nF(\frac 1x)= x^{n-m}Q(\frac1x)\cdot x^mG(\frac1x)+x^{n-m+1}x^{m-1}R(\frac1x)$$
$$F_R(x)= Q_R(x)\cdot G_R(x)+x^{n-m+1}R_R(x)$$
$$F_R(x)\equiv Q_R(x)\cdot G_R(x)(\bmod x^{n-m+1})$$
$$Q_R(x)\equiv \frac{G_R(x)}{F_R(x)}(\bmod x^{n-m+1})$$
$$R(x)=F(x)-Q(x)\cdot G(x)$$

$O(n\log n)$
### [$\text{CZT}(F)$](https://www.luogu.com.cn/problem/P6800)
$$F(c^k)=\sum_{i=0}^{n-1}a_ic^{ik}$$
$$ik=\dfrac{2ik}{2}$$
$$=\dfrac{i^2+2ik+k^2-i-k-i^2+i-k^2+k}{2}$$
$$=\binom{i+k}{2}-\binom{i}{2}-\binom{k}{2}$$
$$F(c^k)=\sum_{i=0}^{n-1}a_ic^{ik}$$
$$=\sum_{i=0}^{n-1}a_ic^{\binom{i+k}{2}-\binom{i}{2}-\binom{k}{2}}$$
$$=c^{-\binom{k}{2}}\sum_{i=0}^{n-1}a_ic^{-\binom{i}{2}}c^{\binom{i+k}{2}}$$
### [$\sin F\text{ and }\cos F$](https://www.luogu.com.cn/problem/P5264)
$$e^{\text{i}x}=\cos x+\text{i }\sin x$$
$$e^{-\text{i}x}=\cos x-\text{i }\sin x$$
$$2\cos x=e^{\text{i} x}+e^{-\text{i} x}$$
$$2\text{i}\sin x=e^{\text{i} x}-e^{-\text{i} x}$$
$$\cos F=\frac{e^{\text{i} F}+e^{-\text{i} F}}2$$
$$\sin F=\frac{e^{\text{i} F}-e^{-\text{i} F}}{2\text{i}}$$

$O(n\log n)$
