---
title: "题解：P12541 [APIO2025] Hack!"
date: 2025-05-19
category: "题解"
summary: "场外选手，做了一个下午做出来了！ Link 题意 这是一道交互题。 有一个未知的整数 n，你需要在若干次询问后猜出它。每一次询问你可以给出一个任意长的正整数序列 a1 k，交互"
math: true
top: 2
source: https://www.luogu.com.cn/article/tp7pzgqf
slug: tp7pzgqf
---

场外选手，做了一个下午做出来了！

[$\text{Link}$](https://www.luogu.com.cn/problem/P12541)
## 题意
这是一道交互题。

有一个未知的整数 $n$，你需要在若干次询问后猜出它。每一次询问你可以给出一个任意长的正整数序列 $a_{1\sim k}$，交互库会返回有多少对 $1\le i<j\le k$ 满足 $a_i\equiv a_j\pmod n$，花费的代价为给出的序列长度 $k$。

你需要在不超过 $1.1\times 10^5$ 的代价内返回 $n$。多组数据。

$T\le 10$，$n\le 10^9$。
## 思路

前两个子任务的做法没有什么拓展性，直接观察最大的档，不难猜测需要一个 $O(\sqrt n)$ 代价的算法。
### 算法模型
取模相关不妨考虑 BSGS 算法。设定阈值 $b$，构造两个序列 $F=\{1,2,\dots,b\},G=\{2b,3b,\dots,kb\}$，其中 $k=\left\lceil\dfrac{\max n}{b}\right\rceil$。

如果能找到 $x\in F,y\in G$ 满足询问 $\{x,y\}$ 返回 $1$ 且 $y$ 最小，那么我们就能确定 $n=y-x$。

寻找 $x,y$ 考虑二分，每次将 $|F|,|G|$ 分别减半。将 $F,G$ 分别对半划分为 $F_l,F_r,G_l,G_r$，一个朴素的想法为依次询问 $F_l\cup G_l,F_r\cup G_l,F_r\cup G_r$，若三次询问均不存在哈希冲突则保留 $F_l,G_r$，否则保留存在哈希冲突的一组，需要 $\frac32|F|+\frac32|G|$ 的代价。

注意到这样不是最优的，不妨询问 $F_l\cup G$，若成功存在冲突则询问 $F_l\cup G_l$，否则询问 $F_r\cup G_l$，这样只需要 $|F|+\frac32|G|$ 的代价。
### 细节处理

注意到如果 $F$ 或 $G$ 内部就存在哈希冲突，上述二分算法并不能正确运行，分别考虑处理 $F$ 与 $G$ 内部的问题。

对于 $F$ 的内部，若其存在哈希冲突则有 $n\le b$，这时可以用一次阈值为 $\sqrt b$ 的 BSGS 判断是否有 $n\le b$，若判断成功则直接使用子任务一的算法即可。

对于 $G$ 的内部，若其存在冲突则有 $ib\equiv jb\pmod n$，不妨要求 $b$ 为质数，这样只有 $n$ 是 $b$ 的倍数或者 $n\le \left\lceil\dfrac{\max n}{b}\right\rceil$ 时才可能冲突，后者与 $F$ 的处理方法相同，前者只需要选取一些不同的质数，在其中随机选取 $b$ 即可避免。

### 常数优化

上述算法的代价大致为 $2b+\dfrac{3\max n}{b}+O(\sqrt[4]{\max n})$，取 $b=O(\sqrt{3n/2})$ 得到次数 $2\sqrt{6n}$，约为 $1.5\times 10^5$，无法通过。

注意到我们只需要求出一个 $n$ 的倍数便可一个个试除其质因子得到正确的 $n$，于是我们无需要求求出的 $y$ 最小，并只保留 $G$ 中不小于 $\dfrac{\max n}2$ 的数，代价优化为 $2b+\dfrac{3\max n}{2b}+O(\sqrt[4]{\max n}+\log n)$，取 $b=O(\sqrt{3n/4})$ 得到次数 $2\sqrt{3n}$，约为 $1.09\times 10^5$，可以通过。

以下是一份通过代码：
```cpp
#include<bits/stdc++.h>
#include "grader.cpp"
using namespace std;
#define ll long long
#define vi vector<int>
#define vll vector<ll>
const int N=1e9+10;
int B,Bs[]={27329,27337,27361,27367,27397};
ll collisions(vll v);
ll calc(vi vc){
	vll v;
	for(auto x:vc)
		v.push_back(x);
	return collisions(v);
}
ll calc(vi L,vi R){
	vll v;
	for(auto x:L)
		v.push_back(x);
	for(auto x:R)
		v.push_back(x);
	return collisions(v);
}
inline bool chksub(){
	vi v;
	for(int i=1;i<200;i++)
		v.push_back(i);
	for(int i=1;i<=200;i++)
		v.push_back(i*200);
	return calc(v);
}
int hack(){
	B=Bs[rand()%5];
	if(chksub()){
		for(int i=1;i<=40000;i++)
			if(calc({1,i+1}))
				return i;
		exit(-1);
	}
	vi F,G;
	for(int i=1;i<=B;i++)
		F.push_back(i);
	for(int i=B*2;i<=N+B;i+=B)
		if(i>=N/2)
			G.push_back(i);
	while(F.size()>1||G.size()>1){
		int n=F.size(),m=G.size();
		int cl=n/2,dl=m/2;
		vi Fl,Fr,Gl,Gr;
		for(int i=0;i<cl;i++) Fl.push_back(F[i]);
		for(int i=cl;i<n;i++) Fr.push_back(F[i]);
		for(int i=0;i<dl;i++) Gl.push_back(G[i]);
		for(int i=dl;i<m;i++) Gr.push_back(G[i]);
		if(n==1){ G=calc(F,Gl)?Gl:Gr;continue; }
		if(calc(Fl,G)) F=Fl,G=calc(Fl,Gl)?Gl:Gr;
		else F=Fr,G=calc(Fr,Gl)?Gl:Gr;
	}
	int n=G[0]-F[0],d=n;
	for(int p=2;p*p<=d;p++){
		if(d%p) continue;
		while(d%p==0) d/=p;
		while(n%p==0){
			int np=n/p;
			if(!calc({1,np+1})) break;
			n/=p;
		}
	}
	if(d>1){
		int np=n/d;
		if(calc({1,np+1})) n=np;
	}
	return n;
}
```
