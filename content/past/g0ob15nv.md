---
title: "题解：P11160 機械生命体"
date: 2024-10-05
category: "题解"
summary: "Link Trie 树本质即为权值线段树。 本题解将会较为详细地讲述实现。 题意 维护一个可重集 S，初始为空。共有 q 次如下类型的操作： 1 x，向 S 中加入一个 x。 "
math: true
top: 2
source: https://www.luogu.com.cn/article/g0ob15nv
slug: g0ob15nv
---

[$\text{Link}$](https://www.luogu.com.cn/problem/P11160)

Trie 树本质即为权值线段树。

本题解将会较为详细地讲述实现。
## 题意
维护一个可重集 $S$，初始为空。共有 $q$ 次如下类型的操作：

- `1 x`，向 $S$ 中加入一个 $x$。
- `2 x`，从 $S$ 中删除一个 $x$。
- `3 x k v`，对 $S$ 中所有满足 $\operatorname{lowbit}(x\oplus y)\geq 2^k$ 的 $y$，将其替换为 $(y+v)\bmod 2^{32}$。
- `4 x`，求出 $\max\limits_{y\in S} \operatorname{lowbit}(x\oplus y)$。

$q\le 5\times 10^5$。
## 题解
想必各位对 Trie 树维护全局加一的做法都已经倒背如流了：从低位向高位建 Trie 树，将根的右链上所有结点的左右儿子交换。

本题的操作三相当于取出 Trie 树上的某个子树，对其进行加 $v$。同时此时的操作四所求的信息相当简单，允许我们由低位至高位求解。那么我们要从全局加一的做法类比一个全局加 $v$ 的做法出来。

对一个子树进行操作几乎已经明示了我们需要打标记处理该问题。我们对一个结点 $i$ 打上标记 $t_i$ 表示对将 $i$ 为根的子树看作独立的一颗 Trie 树，还需对全局加上 $t_i$。那么标记下传时只需如下操作：
- 如果 $t_i$ 为奇数，对 $i$ 子树做一次全局加一并将 $t_i$ 减去一；
- 将左右儿子的标记分别加上 $\dfrac{t_i}{2}$ 并清空 $t_i$。

由于每次下传都可能会做一次全局加一，单次操作时间复杂度为 $O(\log^2 v)$。但是注意到我们并不需要立即将此次全局加一进行完，只需将右儿子的标记加一再交换左右儿子即可避免，时间复杂度降为 $O(\log v)$。

接下来，考虑将全局加拓展到子树加。考虑一次操作三 $x,k,v$，不妨令 $x$ 仅保留后 $k$ 位。我们直接做完后 $k$ 位的加法，将剩余的部分标记给修改子树，再将修改子树与做完加法所得目标子树合并起来。其中合并即为线段树合并，复杂度均摊正确。

总时间复杂度 $O(q\log v)$，参考实现：
```cpp
#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define ui unsigned int
namespace IO{//by cyffff
    
}
const int N=5e5+10,B=32;
int rt;
struct Trie{
	#define ls son[rt][0]
	#define rs son[rt][1]
	int cnt,son[N*B][2],siz[N*B];
	ui tag[N*B];
	inline void pushup(int rt){
		siz[rt]=siz[ls]+siz[rs];
	}
	inline void pushtag(int rt,ui v){
		if(!rt) return ;
		tag[rt]+=v;
	}
	inline void pushdown(int rt){
		if(!tag[rt]) return ;
		if(tag[rt]&1) pushtag(rs,1),swap(ls,rs),tag[rt]--;
		pushtag(ls,tag[rt]>>1);
		pushtag(rs,tag[rt]>>1);
		tag[rt]=0;
	}
	inline void insert(int &rt,int d,ui x,int v){
		if(!rt) rt=++cnt;
		siz[rt]+=v;
		if(d==B) return ;
		pushdown(rt);
		int c=x>>d&1;
		insert(son[rt][c],d+1,x,v);
	}
	inline int merge(int x,int y,int d){
		if(!x||!y) return x+y;
		if(d==B){
			siz[x]+=siz[y];
			return x;
		}
		pushdown(x),pushdown(y);
		son[x][0]=merge(son[x][0],son[y][0],d+1);
		son[x][1]=merge(son[x][1],son[y][1],d+1);
		pushup(x);
		return x;
	}
	inline void solve(int &pr,int &nx,int d,ui x,ui v,int k){
		if(!pr) return ;
		if(!nx) nx=++cnt;
		if(d==k){
			int A=pr;
			pushtag(A,(x+v)>>k);
			pr=0,nx=merge(nx,A,k);
			return ;
		}
		pushdown(pr),pushdown(nx);
		int cp=x>>d&1,cn=x+v>>d&1;
		solve(son[pr][cp],son[nx][cn],d+1,x,v,k);
		pushup(pr),pushup(nx); 
	}
	inline int query(int rt,int d,ui x){
		if(d==B) return d;
		pushdown(rt);
		int c=x>>d&1;
		if(siz[son[rt][c]]) return query(son[rt][c],d+1,x);
		return d;
	}
}T;
int main(){
	int q=read();
	while(q--){
		int op=read();
		ui x=read();
		if(op==1){
			T.insert(rt,0,x,1);
		}else if(op==2){
			T.insert(rt,0,x,-1);
		}else if(op==3){
			int k=read();
			ui v=read();
			T.solve(rt,rt,0,x&((1ll<<k)-1),v,k); 
		}else{
			write(1ll<<T.query(rt,0,x)),putc('\n');
		}
	}
	flush();
}
```
