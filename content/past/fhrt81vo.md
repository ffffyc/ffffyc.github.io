---
title: "快速创造数据"
date: 2021-01-13
category: "工具"
summary: "想批量生产数据？下面的数据生成器能满足你的愿望。 cpp include using namespace std; namespace rad{ mt1993764 R(chr"
math: false
top: 2
source: https://www.luogu.com.cn/article/fhrt81vo
slug: fhrt81vo
---

想批量生产数据？下面的数据生成器能满足你的愿望。
```cpp
#include<bits/stdc++.h>
using namespace std;
namespace rad{
	mt19937_64 R(chrono::system_clock::now().time_since_epoch().count());
	inline int Rand(int l,int r){
		uniform_int_distribution<int> distribution(l,r);
	    return distribution(R);
	}
}using namespace rad;
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
快去造数据吧！
