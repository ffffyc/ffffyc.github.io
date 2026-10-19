---
title: "题解 UVA13287 【Shattered Cake】"
date: 2020-08-26
category: "题解"
summary: "UVA13287 Shattered Cake 原题链接 思路 给出了小矩形的长宽，就能求出它的面积，而原矩形的面积就是所有小矩形的面积之和，而要求的 L 就是 S/W ，上代"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/uwi7yzjx
slug: uwi7yzjx
---

# UVA13287 Shattered Cake
[原题链接](https://www.luogu.com.cn/problem/UVA13287)
## 思路
给出了小矩形的长宽，就能求出它的面积，而原矩形的面积就是所有小矩形的面积之和，而要求的 $L$ 就是 $S/W$ ，上代码。
```cpp
#include<bits/stdc++.h>
using namespace std;
#define LL long long
int main(){
	LL w,n,wi,li,sum=0;
	while(scanf("%lld %lld",&w,&n)!=EOF){//注意多组数据
		sum=0;//记得归0
		for(int i=1;i<=n;i++){
			scanf("%lld %lld",&wi,&li);
			sum+=wi*li;
		}
		printf("%lld\n",sum/w);
	}
	return 0;
}
```
这道蓝~~水~~题就做完了，不过本蒟蒻的做法有点慢，只排在了最优解第二页。
谢谢观看qwq
