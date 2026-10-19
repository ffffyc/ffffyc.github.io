---
title: "信息数学"
date: 2021-09-10
category: "文化课"
tags: ["学习笔记"]
summary: "集合 1 集合的概念与表示 () 概念 定义：把一些确定的对象（元素）看做一个整体（集合）； 性质：确定性、互异性、无序性； 记号：a∈ A or a A； \\1,2,3,4,"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/kpl1k0cv
slug: kpl1k0cv
---

# 集合
## $1$ 集合的概念与表示 $(\blacksquare\blacksquare\square\square\square)$
### 概念
- 定义：把一些**确定的**对象（元素）看做一个整体（集合）；
- 性质：确定性、互异性、无序性；
- 记号：$a\in A\text{ or }a\notin A$；
- $\{1,2,3,4,5,...\}$，$\{x\in\mathbb R|1\le x\le 5\}$。

### 数集
- $\mathbb N$，自然数集
- $\mathbb N^+,\mathbb Z^+,\mathbb N^*$，正整数集
- $\mathbb Z$，整数集
- $\mathbb Q$，有理数集
- $\mathbb R$，实数集
- $\mathbb P$，质数集

### 例题
$(\blacksquare\square\square\square\square)$ $1$. 集合 $A=\{1,x,\sqrt{x^2-x}\}$，求 $x$ 取值范围。 
****
- $x^2-x\ge0$，$x\ge 1\text{ or } x\le0$
- $x\ne1$
- $\sqrt {x^2-x}\ne x$，$x^2-x\ne x^2$，$x\ne 0$
- $\sqrt{x^2-x}\ne 1$，$x^2-x-1\ne 0$，$x\ne \dfrac{1\pm\sqrt 5}2$

综上，$x<0\text{ or }x>1\text{ and }x\ne \dfrac{1\pm\sqrt 5}2$
****
$(\blacksquare\blacksquare\blacksquare\square\square)$ $2$. 设 $a_1,a_2,a_3,a_4\in\Bbb R$，$\{a_ia_j|1\le i<j\le 4\}=\{-24,-2,-\dfrac 2 3,-\dfrac 1 8,1,3\}$，求 $a_1+a_2+a_3+a_4$。 
****
显然 $\prod_{i=1}^4a_i=3$，考虑分为三组：$(-24,-\dfrac 1 8),(-2,-\dfrac 2 3),(1,3)$。

不妨设 $|a_1|<|a_2|<|a_3|<|a_4|$.

其中为定值的有 $\begin{cases}a_3a_4=-24\a_2a_4=3\a_1a_3=1\a_1a_2=-\dfrac 1 8\end{cases}$

$-24a_1^2=-\dfrac 3 2\text{ or } -2$，（$-2$ 舍去）。

$\to a_1=\pm\dfrac 1 4$

$\displaystyle(\frac 1 4,-\frac 1 2,4,-6)\text{ or }(-\frac 1 4,\frac 1 2,-4,6)$。

答案为 $\pm\dfrac 9 4$。
****
$(\blacksquare\blacksquare\blacksquare\blacksquare\square)$ $3$. 若集合 $A$ 由非 $0$、$1$ 实数组成，且满足若 $x\in A$ ，则 $\dfrac 1 {1-x}\in A$。 若 $A$ 中元素不超过 $8$ 个，所有元素和为 $\dfrac {14} 3$，且 $A$ 中有一个元素的平方为所有元素的积，求 $A$。
****
> $A$ 中至少有 $3$ 个元素

可证 $x,\dfrac1{1-x},\dfrac {x-1}x$ 互不相同，$\displaystyle\frac{1}{1-\frac {x-1}x}=x$。

> $|A|=3k$

$x\dfrac1{1-x}\dfrac {x-1}x=-1$，所以 $|A|=6$，所有元素的积为 $1$。

所以 $-1\in A$，不妨设 $A=\{a,\dfrac1{1-a},\dfrac {a-1}a,b,\dfrac1{1-b},\dfrac {b-1}b\},a=-1$。

$-1+\dfrac 1 2+2=\dfrac 3 2 $，所以 $b+1-\dfrac1{b-1}-\dfrac {1}b=\dfrac {19}6$，$b-\dfrac1{b-1}-\dfrac {1}b=\dfrac {13}6$.

$6b^3-19b^2+b+6=0$

$(b-3)(6b^2-b-2)=0$

$b-3=0$ 或 $6b^2-b-2=0$

所以 $b=3,\dfrac 2 3,-\dfrac 1 2$

$A=\{2,-1,\dfrac 1 2,3,\dfrac 2 3,-\dfrac 1 2\}$
## $2$ 集合的关系与运算 $(\blacksquare\blacksquare\square\square\square)$
### 关系
-  子集
	- $A\subseteq B$，$A$ 集合中所有元素都在 $B$ 集合中。
	- $\varnothing$ 是任意集合的子集。
- 相等
	- $A=B$，构成集合 $A$、$B$ 的元素相等。
	- 等价于 $A\subseteq B\land B\subseteq A$。
- 真子集
	- $A⫋ B$，$A$ 集合中所有元素都在 $B$ 集合中，且 $\exists x\in A,x\notin B$。
	- $\varnothing$ 是任意非空集合的子集。

### 运算
- 并集：$A\cup B=\{x|x\in A\lor x\in B\}$.
- 交集：$A\cap B=\{x|x\in A\land x\in B\}$.
- 补集：$C_U A=\{x|x\in U\land x\notin A\}=U\backslash A$.
- 差集：$A\backslash B=\{x|x\in A\land x\notin B\}$.

#### 运算性质
- 交换律：$A\cup B=B\cup A,A\cap B=B\cap A$.
- 结合律：$A\cup(B\cup C)=(A\cup B)\cup C,A\cap(B\cap C)=(A\cap B)\cap C$.
- 分配律：$A\cap(B\cup C)=(A\cap B)\cup (A\cap C),A\cup(B\cap C)=(A\cup B)\cap (A\cup C)$.
- 吸收率：$A\cup(A\cap B)=A,A\cap(A\cup B)=A$.
- 对偶率：$C_U(A\cup B)=C_U(A)\cap C_U(B),C_U(A\cap B)=C_U(A)\cup C_U(B)$
- 容斥原理：$\displaystyle B=\{x|1\le x\le n\}\cap \mathbb N,|\bigcup_{i=1}^n A_i|=\sum_{S\subseteq B}(-1)^{|S|-1}|\bigcap_{p\in S}A_p|$

## $3$ 逻辑联结词、全称与存在量词 $(\blacksquare\blacksquare\square\square\square)$
### 逻辑联结词
- 命题：能够判断真假的语句.
	- 真命题、假命题；简单命题、复合命题.
- 且 $\land$，或 $\lor$，非 $\lnot$.

### 全称量词与存在量词 
- 全称量词 $\forall$
	- 全称命题，$\forall x\in M,p(x)$;
- 存在量词 $\exists$
	- 特称命题，$\exists x\in M,p(x)$.


## $4$ 命题及其关系、充分必要条件$(\blacksquare\blacksquare\square\square\square)$
### 四种命题
- 原命题：$p\rArr q$；
- 逆命题：$q\rArr p$；
- 否命题：$\lnot p\rArr\lnot q$；
- 逆否命题：$\lnot q\rArr\lnot p$。

### 充分必要条件
- $p\Rarr q,A\sube B$ 充分条件；
- $p\Larr q,A\supe B$ 必要条件；
- $p\Harr q,A=B$ 充要条件；
- 都不满足，不充分也不必要。

# 函数
## $1$ 函数的基本概念 $(\blacksquare\square\square\square\square)$
### 集合的映射
$f:A\to B$ 表示 $\forall a\in A$，按照某一关系 $f$ 在 $B$ 中唯一对应一个元素 $b$。$b$ 为 $a$ 的像，$b=f(a)$，$a$ 为 $b$ 的原像，$\{b|b=f(a),a\in A\}$ 称为 $f$ 值域 $f(A)$。
### 函数的定义
设数集 $A,B$，映射 $f:A\to B$ 称为 $A$ 上的一个函数，记作 $y=f(x),x\in A$，$x$ 为自变量，$y$ 为因变量，记作 $y=f(x)$ 或 $y|_{x=a}$。$A$ 称为定义域，$\{y|y=f(x),x\in A\}$ 称为值域。

## $2$ 函数的单调性与最值 $(\blacksquare\blacksquare\square\square\square)$
### 函数单调性
设函数 $f$ 定义域为 $I$，若在区间 $D\sube I$ $,\forall x_1<x_2,x_1,x_2\in D,f(x_1)<f(x_2)$，则称函数 $f$ 在区间 $D$ 上的增函数。同理，若 $\forall x_1<x_2,x_1,x_2\in D,f(x_1)>f(x_2)$，则称函数 $f$ 在区间 $D$ 上的减函数。

若函数 $f$ 在区间 $D$ 上是增函数或减函数，则称这个函数在区间 $D$ 上具有单调性，$D$ 为单调区间。

增函数等价定义还有：
- $\forall x_1,x_2\in D,x_1\ne x_2,(x_1-x_2)[f(x_1)-f(x_2)]>0$.
- $\forall x_1,x_2\in D,x_1\ne x_2,\dfrac{f(x_1)-f(x_2)}{x_1-x_2}>0$.

减函数等价定义还有：
- $\forall x_1,x_2\in D,x_1\ne x_2,(x_1-x_2)[f(x_1)-f(x_2)]<0$.
- $\forall x_1,x_2\in D,x_1\ne x_2,\dfrac{f(x_1)-f(x_2)}{x_1-x_2}<0$.

###
