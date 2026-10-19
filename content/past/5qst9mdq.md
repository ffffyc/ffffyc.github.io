---
title: "题解 CF675A 【Infinite Sequence】"
date: 2020-08-26
category: "题解"
summary: "CF675A Infinite Sequence 原题链接 题目描述 给出三个整数 a,b,c(-109 using namespace std; define LL long"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/5qst9mdq
slug: 5qst9mdq
---

# CF675A Infinite Sequence
[原题链接](https://www.luogu.com.cn/problem/CF675A)
#### 题目描述
给出三个整数 a,b,c($-10^9$<=a , b , c<=$10^9$)，求 $b$ 是否在以 $a$ 为第一个数，公差为 $c$ 的等差数列中。
###### 
例如第一个样例，等差数列为1,4,7,10……，7在这个等差数列中，输出 $YES$。（注意，这个等差数列是无限长的）。
#### 思路
来推导一波：如果 $b$ 在以 $a$ 为开头，以 $c$ 为公差的等差数列里，则 $b=a+dc$ ，这样只需要判断 $(b-a)%c$ 是否为 $0$ 就行了。
###### 
注意：当 $c$ 为 $0$ 时注意特判，否则会 $mod 0 $会 $RE$。
###### 
~~这也是黄题？~~
****
接下来贴上C++AC代码~
###### 
~~我才不会告诉你我因为少了2个等于号WA了四次#7。~~
```cpp
#include<bits/stdc++.h>
using namespace std;
#define LL long long
int main(){
	LL a,b,c;
	cin>>a>>b>>c;
	if(c==0){ //特判c=0
		if(a==b){
			cout<<"YES";
		}else{
			cout<<"NO";
		}
		return 0;
	}
	if((b-a)%c==0&&((a<=b&&c>0)||(a>=b&&c<0))){
		cout<<"YES";
	}else{
		cout<<"NO";
	}
	//当c>0时，若b要在等差数列里，b一定>a，c<0时同理，b一定<a
	return 0;
}
```
好了，成功AC~
###### 
本蒟蒻第一次交题解，使用$\LaTeX$还不太熟练qwq。
