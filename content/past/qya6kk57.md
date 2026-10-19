---
title: "题解 CF153D 【Date Change】"
date: 2020-09-08
category: "题解"
summary: "CF153D Date Change 传送门 ~~emmm由于提交了5次一直wating还没AC~~ 思路 分类讨论 x 。 如果 x0 ，循环 x 次，每次把日期 +1 ，如"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/qya6kk57
slug: qya6kk57
---

# CF153D Date Change
[传送门](https://www.luogu.com.cn/problem/CF153D)

~~emmm由于提交了5次一直wating还没AC~~
## 思路
分类讨论 $x$ 。

如果 $x>0$ ，循环 $x$ 次，每次把日期 $+1$ ，如果当前日期比当前月份的天数多了，就把月份 $+1$，日期设为 $1$ ，如果月份 $>12$ ，设定月份为 $1$ ，年份 $+1$ 。

如果 $x<0$ ，同理，减到 $1$ 以下就设定为上一个月的月份天数。

注意：每次改变年份都要判断以下是不是闰年。

上代码~
```cpp
#include<bits/stdc++.h>
using namespace std;
#define LL long long
int y,m,d,q[]={0,31,28,31,30,31,30,31,31,30,31,30,31};//各月天数
inline int read(){//快读
	char ch=getchar();
	int x=0,f=1;
	while(ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9') x=x*10+(ch^48),ch=getchar();
	return x*f;
}
inline void year(int x){//判断闰年
	if((x%4==0&&x%100!=0)||x%400==0){
		q[2]=29;
	}else{
		q[2]=28;
	}
}
inline int f(int x){//判断位数
	int y=x,ans=0;
	while(y){
		y/=10;
		ans++;
	}
	return ans;
}
int x;
int main(){
	d=read(),m=read(),y=read(),x=read();//快读可以直接省去终止符'.'
	year(y);//判断这一年是闰年还是平年
	if(x>0){//分类讨论
		for(int i=1;i<=x;i++){
			d++;
			if(d>q[m]){//日期溢出
				d-=q[m];
				m++;
			}
			if(m>12){//月份溢出
				m-=12;
				y++;
				year(y);
			}
		}
	}else if(x<0){
		for(int i=1;i<=abs(x);i++){
			d--;
			if(d<=0){
				d=q[m-1+12*(m-1==0)];//注意当m=1时m-1=0
				m--;
			}
			if(m<=0){
				m=12;
				y--;
				year(y);
			}
		}
	}
	if(f(d)!=2){//补全两位日期
		printf("0%d.",d);
	}else{
		printf("%d.",d);
	}
	if(f(m)!=2){
		printf("0%d.",m);
	}else{
		printf("%d.",m);
	}
	for(int i=4;i>f(y);i--){//补全四位年份
		printf("0");
	}
	printf("%d",y);
	return 0;
}
```
下次再见qwq
