---
title: "题解 P2197 【【模板】nim游戏】"
date: 2020-09-18
category: "题解"
summary: "P2197 【模板】nim游戏 传送门 思路 其实Nim取石子有自己的必胜态与必败态的公式。 就是如果有 N 堆石子，每堆为 a1,a2,a3...an ，则当 a1 xor "
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/qg56eyjk
slug: qg56eyjk
---

# P2197 【模板】nim游戏
[传送门](https://www.luogu.com.cn/problem/P2197)
## 思路
其实Nim取石子有自己的必胜态与必败态的公式。

就是如果有 $N$ 堆石子，每堆为 $a1,a2,a3...an$ ，则当 $a1\enspace xor\enspace a2\enspace xor\enspace a3...\enspace xor\enspace an>0$时，为必胜态，否则为必败态。

剩余的解释在代码注释中给出

上AC代码~
```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
	int t;
	scanf("%d",&t);
	while(t--){
		int n,w;
		bool first=true;
		scanf("%d",&n);
		while(n--){
			if(first){
				first=false;
				scanf("%d",&w);//输入第一个数
			}else{
				int q;
				scanf("%d",&q);
				w=w^q;//每个值xor一下
			}
		}
		if(w>0){//判断必胜态、必败态
			puts("Yes");
		}else{
			puts("No");
		}
	}
	return 0;
}
```
再见qwq
