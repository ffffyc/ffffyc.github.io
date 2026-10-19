---
title: "题解 CF1285C 【Fadi and LCM】"
date: 2020-08-27
category: "题解"
summary: "CF1285C Fadi and LCM 原题链接 思路 要求使 lcm(a,b)=X 成立时 max(a,b) 最小的 a,b ，可从 n 开始向下枚举，直到枚举到 i 满足"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/ay1bv18l
slug: ay1bv18l
---

# CF1285C Fadi and LCM
[原题链接](https://www.luogu.com.cn/problem/CF1285C)
## 思路
要求使 $\operatorname{lcm}(a,b)=X$ 成立时 $\max(a,b)$ 最小的 $a,b$ ，可从 $\sqrt n$ 开始向下枚举，直到枚举到 $i$ 满足 $X\mod i=0$ ，则 $a=i,b=X/i$ 。此时 $\max(a,b)$ 必定最小，因为 $a<=b,b=X/a$ ，则 $a$ 越大， $b$ 就越小， $\max(a,b)$ 就最小。
```cpp
#include<bits/stdc++.h>
using namespace std;
#define LL long long
LL lcm(LL x,LL y){
	LL a=x,b=y;
	LL z=x%y;
	while(z!=0){
		x=y;
		y=z;
		z=x%y;
	}
	return a*b/y;
}
int main(){
	LL x;
	cin>>x;
	for(LL i=sqrt(x);i>=1;i--){
		LL j=x/i;
		if(j*i==x){
			if(lcm(i,j)==x){
				cout<<min(i,j)<<" "<<max(i,j);
				return 0;
			}
		}
	}
	return 0;
	//数据点$31ms$，总用时$1.33s$，最优解第八名
}
```
再见qwq
