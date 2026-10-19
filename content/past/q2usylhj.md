---
title: "CSP-S2025 游记：没人告诉我 NOI Linux 有编译器 bug 啊？"
date: 2025-11-06
category: "游记"
tags: ["CSP-S 2025", "NOI 2025"]
summary: "初赛 100，复赛 400......390？？？？ replace 挂了 10 分，为什么呢？？ 好的，拿到代码了，赶紧交一下......所有民间数据都通过了啊？ 官方数据出"
math: true
top: 2
source: https://www.luogu.com.cn/article/q2usylhj
slug: q2usylhj
---

初赛 100，复赛 400......390？？？？

`replace` 挂了 $10$ 分，为什么呢？？

好的，拿到代码了，赶紧交一下......所有民间数据都通过了啊？

官方数据出了，赶紧交一下......怎么官方数据也过了？难道被卡常了？明明时间复杂度是正确的 $O((n+q)\log L+L)$ 啊。

放到 NOI Linux 上面跑一下......`replace13` 怎么爆空间了？实际空间 3G？？赛时测过静态空间才 `1G`，动态空间也只有 `eps`，并且各 OJ 都正常通过啊？

:::info[完整代码]
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long
#define gc() getchar()
#define putc(c) putchar(c)
inline int read(){
	int x=0,t=0;
	char c=gc();
	while(c<'0'||c>'9') t|=c=='-',c=gc();
	while(c>='0'&&c<='9') x=x*10+c-'0',c=gc();
	return t?-x:x;
}
inline void write(int x){
	if(x<0) putc('-'),x=-x;
	if(x>9) write(x/10);
	putc(x%10+'0');
}
inline int readstr(char *s){
	int l=0;
	char c=gc();
	while(c<'a'||c>'z') c=gc();
	while(c>='a'&&c<='z') s[++l]=c,c=gc();
	s[l+1]=0;
	return l;
}
#define mpr make_pair
#define pii pair<int,int>
#define fir first
#define sec second
//bool st;
using node=array<int,3>;
const int N=2e5+10,L=5e6+10;
const int bas=131,m1=998244853,m2=1e9+9;
int n,q,cd,ans[N],ls[N],lt[N],rs[N],rt[N],p;
char s[L],t[L],sp[L];
int son[L][26],cnt;
pii hsh[N];
vector<node>qr[L],md[L];
map<pii,int>id;
int dfn[L],low[L],tim;
inline void dfs0(int x){
	dfn[x]=++tim;
	for(int c=0;c<26;c++)
		if(son[x][c])
			dfs0(son[x][c]);
	low[x]=tim;
}
struct Segment_Tree{
	#define ls (a[rt].lson)
	#define rs (a[rt].rson)
	struct node{
		int lson,rson,tag;
	}a[N*60];
	int cnt;
	inline void add(int &rt,int l,int r,int L,int R,int v){
		if(!rt) rt=++cnt;
		if(L<=l&&r<=R){ a[rt].tag+=v;return ; }
		int mid=l+r>>1;
		if(L<=mid) add(ls,l,mid,L,R,v);
		if(R>mid) add(rs,mid+1,r,L,R,v);
	}
	inline int query(int rt,int l,int r,int p){
		if(!rt) return 0;
		if(l==r) return a[rt].tag;
		int mid=l+r>>1;
		if(p<=mid) return query(ls,l,mid,p)+a[rt].tag;
		else return query(rs,mid+1,r,p)+a[rt].tag;
	}
	#undef ls
	#undef rs
}T;
int rtp[N];
inline void dfs1(int x){
	for(auto tp:md[x]){
		int p=tp[1],id=tp[2];
		T.add(rtp[id],1,tim,dfn[p],low[p],1);
	}
	for(auto tp:qr[x]){
		int p=tp[1],id=tp[2];
		ans[tp[0]]=T.query(rtp[id],1,tim,dfn[p]);
	}
	for(int c=0;c<26;c++)
		if(son[x][c])
			dfs1(son[x][c]);
	for(auto tp:md[x]){
		int p=tp[1],id=tp[2];
		T.add(rtp[id],1,tim,dfn[p],low[p],-1);
	}
}
//bool ed;
int main(){
//	printf("%.2lfMB\n",(&st-&ed)/1024./1024.);
//	system("fc replace1.out replace1.ans /n");
//	system("fc replace2.out replace2.ans /n");
//	system("fc replace3.out replace3.ans /n");
//	system("fc replace4.out replace4.ans /n");
	freopen("replace.in","r",stdin);
	freopen("replace.out","w",stdout);
	n=read(),q=read();
	for(int i=1;i<=n;i++){
		int l=readstr(s),lp=readstr(t);
		assert(l==lp);
		bool fl=0;
		for(int j=1;j<=l;j++)
			fl|=s[j]!=t[j];
		if(!fl) continue;
		int lx=0,rx=0;
		for(int j=1;j<=l;j++)
			if(s[j]!=t[j])
				lx=(lx?lx:j),rx=j;
		ls[i]=p+1;
		for(int j=lx-1;j;j--)
			sp[++p]=s[j];
		lt[i]=p,rs[i]=p+1;
		for(int j=rx+1;j<=l;j++)
			sp[++p]=s[j];
		rt[i]=p;
		int hs1=0,hs2=0;
		for(int j=lx;j<=rx;j++)
			hs1=(1ll*hs1*bas+s[j])%m1,
			hs2=(1ll*hs2*bas+s[j])%m2,
			hs1=(1ll*hs1*bas+t[j])%m1,
			hs2=(1ll*hs2*bas+t[j])%m2;
		hsh[i]=mpr(hs1,hs2); 
	}
	for(int i=1;i<=q;i++){
		int l=readstr(s),lp=readstr(t);
		if(l!=lp) continue;
		int lx=0,rx=0;
		for(int j=1;j<=l;j++)
			if(s[j]!=t[j])
				lx=(lx?lx:j),rx=j;
		int hs1=0,hs2=0;
		for(int j=lx;j<=rx;j++)
			hs1=(1ll*hs1*bas+s[j])%m1,
			hs2=(1ll*hs2*bas+s[j])%m2,
			hs1=(1ll*hs1*bas+t[j])%m1,
			hs2=(1ll*hs2*bas+t[j])%m2;
		pii tp=mpr(hs1,hs2);
		if(!id.count(tp)) id[tp]=++cd;
		int pl=0,pr=0;
		for(int j=lx-1;j>=1;j--){
			int c=s[j]-'a';
			if(!son[pl][c]) son[pl][c]=++cnt;
			pl=son[pl][c];
		}
		for(int j=rx+1;j<=l;j++){
			int c=s[j]-'a';
			if(!son[pr][c]) son[pr][c]=++cnt;
			pr=son[pr][c];
		}
		qr[pl].push_back((node){i,pr,id[tp]});
	}
	for(int i=1;i<=n;i++){
		if(!ls[i]||!id.count(hsh[i])) continue;
		int pl=0,pr=0;
		for(int j=ls[i];j<=lt[i];j++){
			int c=sp[j]-'a';
			if(!son[pl][c]){ pl=-1;break; }
			pl=son[pl][c];
		}
		for(int j=rs[i];j<=rt[i];j++){
			int c=sp[j]-'a';
			if(!son[pr][c]){ pr=-1;break; }
			pr=son[pr][c];
		}
		if(pl==-1||pr==-1) continue;
		md[pl].push_back((node){i,pr,id[hsh[i]]});
	}
	dfs0(0),dfs1(0);
//	cerr<<cnt<<" "<<T.cnt<<endl;
	for(int i=1;i<=q;i++)
		write(ans[i]),putc('\n');
}
```
:::

怎么问题定位到线段树了？？

关闭 `O2`、使用高版本 `gcc`、给 `query` 函数加 `__attribute__((noinline))`，或者在里面定义任何临时变量都会让空间正常地变成 `1G`。

再怎么说 `O2` 也不会把我的空间翻三倍吧......

:::warning[AI 的回答]
大概率是错误的。

![](https://cdn.luogu.com.cn/upload/image_hosting/fyqfnng1.png)
:::

:::info[LA 群友的验证]
经检测是算入了栈空间，猜测编译器发现 `query` 函数递归层数只有 $20$ 层，就自动展开了，往栈里面放了一堆 `int`。

开启 `--param max-inline-recursive-depth=2` 编译选项也不会 MLE。

![](https://cdn.luogu.com.cn/upload/image_hosting/xxqhnxqw.png)

经检测，确实如此。
:::

警钟长鸣，但是不知道要鸣什么。可能是不要让自己代码太好看，给 `-O2` 优化掉吧。或者说加点东西让编译器不要给你内联。

CCF 用个老旧版本 `gcc`，考场又没有对应版本，根本无法查错。再怎样也不该用 `2G` 的空间给我做优化啊，老版本的 `gcc bug`......

本身就是考着玩，顺便看看能不能拿到 OI 生涯第一个 400 的。反正官方数据正常通过了，我认为自己拿了 400 不过分吧。

如果对这个问题有别的想法欢迎评论回复。
