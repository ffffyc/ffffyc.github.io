---
title: "题解 CF39H 【Multiplication Table】"
date: 2020-08-27
category: "题解"
summary: "CF39H Multiplication Table 原题链接 输入进制 $k(2 using namespace std; string zh(int n,int l){//"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/8p2fo2ep
slug: 8p2fo2ep
---

# CF39H Multiplication Table
[原题链接](https://www.luogu.com.cn/problem/CF39H)

输入进制 $k(2<=k<=10)$,输出k进制下的乘法表。
## 思路
第 $i$ 行 $j$ 的数就是 $i$ × $j$ ，只需要转化为 $k$ 进制就行了。

把一个数转化为十以内的进制只需使用短除法：
*  每次用原数 $n$ 除以 $k$ 
*  取余数
*  $n$ 就变为商
*  重复以上操作直至 $n=0$ 
*  从最后一个余数开始，把所有余数连起来
*  得到的结果就是 $n$ 的 $k$ 进制了。

PS：[ADay](https://aday526.blog.luogu.org/solution-cf39h) dalao已经使用过字符串解过这道题了，不过不需要定一个char数组存'0'~'9'，直接+'0'就行了（希望不算重复解法）

```cpp
#include<bits/stdc++.h>
using namespace std;
string zh(int n,int l){//短除法
	string a;
	char b;
    while(n>0){
    	b=n%l+'0';//余数整形转字符
    	a=b+a;//倒取余数，把最新的余数插入到字符串尾
    	n/=l;
	}
	return a;//最后的结果
}
int main(){
	int n;
	string a;
	scanf("%d",&n);
	for(int i=1;i<=n-1;i++){
		for(int j=1;j<=n-1;j++){
			a=zh(i*j,n);//把i*j转换为n进制
			cout<<a<<" ";
		}
		puts("");
	}
	return 0;
	/*数据点用时最高30ms，总用时150ms，最优解第七*/
}
```
再见qwq
