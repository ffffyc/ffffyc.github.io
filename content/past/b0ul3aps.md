---
title: "数据（备份）"
date: 2024-01-17
category: "杂项"
summary: "好像洛谷博客要爆了，备份一个。 cpp include using namespace std; namespace rad{ mt1993764 R(time(0)); in"
math: false
top: 1
hidden: true
source: https://www.luogu.com.cn/article/b0ul3aps
slug: b0ul3aps
---

好像洛谷博客要爆了，备份一个。

```cpp
#include<bits/stdc++.h>
using namespace std;
namespace rad{
	mt19937_64 R(time(0));
	inline int Rand(int l,int r){
		uniform_int_distribution<int> distribution(l,r);
	    return distribution(R);
	}
}
using namespace rad;
int main(){
	string in,out;
	for(int T=/*这里放起始数据编号*/;T<=/*这里放终止数据编号*/;T++){
		in.clear();
		int J=T;
		while(J){
			char m=J%10+'0';
			in=m+in;
			J/=10;
		}
		out=in;
		in+=".in";
		out+=".out";
		freopen(in.data(),"w",stdout);
        //这里放你的数据生成器
		fclose(stdout);
		string Str="/*这里放std文件名*/.exe < "+in+" > "+out;
		system(Str.data());
	}
}
```
