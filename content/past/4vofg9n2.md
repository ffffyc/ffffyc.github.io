---
title: "题解 CF807A 【Is it rated?】"
date: 2020-08-27
category: "题解"
summary: "CF807A Is it rated? 原题链接 思路 如果考前考后 rating 不一样，说明这场比赛肯定是 rating 的，直接输出即可。 unrating 的情况就取最"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/4vofg9n2
slug: 4vofg9n2
---

# CF807A Is it rated?
[原题链接](https://www.luogu.com.cn/problem/CF807A)
## 思路
如果考前考后 $rating$ 不一样，说明这场比赛肯定是 $rating$ 的，直接输出即可。 $unrating$ 的情况就取最小值，如果有 $rating$ 比目前最小的 $rating$ 大，就说明是 $unrating$ ，否则是 $maybe$。
```cpp
#include<bits/stdc++.h>
using namespace std;
#define LL long long
int main(){
	int n,a,b,minn=1<<30;//2^30
	bool flag=false;
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>a>>b;
		if(a!=b){//比赛前后rating不同
			cout<<"rated";
			return 0;
		}
		if(a<minn){
			minn=a;
		}
		if(a>minn){
			flag=true;//如果后面有rating变化则是rating，不能直接输出unrating
		}
	}
	if(flag){
		cout<<"unrated";
	}else{
		cout<<"maybe";
	}
    return 0;
}
```
每个数据点用时不超过 $31ms$ ，总用时 $1.78s$ ，排在最优解第五，做法还是较快的了。那就再见了qwq。
