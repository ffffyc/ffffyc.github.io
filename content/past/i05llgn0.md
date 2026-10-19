---
title: "常用黑盒"
date: 2024-02-26
category: "工具"
summary: "扫描线维护区间 mex cpp define pii pair define mpr makepair define fir first define sec second c"
math: true
top: 2
source: https://www.luogu.com.cn/article/i05llgn0
slug: i05llgn0
---

# 扫描线维护区间 mex

```cpp
#define pii pair<int,int>
#define mpr make_pair
#define fir first
#define sec second
const int N=;
struct Segment_Tree1{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	int mn[N<<2];
	inline void pushup(int rt){
		mn[rt]=min(mn[ls],mn[rs]);
	}
	inline void build(int rt,int l,int r){
		mn[rt]=0;
		if(l==r) return ;
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r); 
	}
	inline void modify(int rt,int l,int r,int p,int v){
		if(l==r){
			mn[rt]=v;
			return ;
		}
		int mid=l+r>>1;
		if(p<=mid) modify(ls,l,mid,p,v);
		else modify(rs,mid+1,r,p,v);
		pushup(rt);
	}
	inline pii query(int rt,int l,int r,int v){
		if(mn[rt]>v) return mpr(-1,-1);
		if(l==r) return mpr(l,mn[rt]);
		int mid=l+r>>1;
		pii tmp=query(ls,l,mid,v);
		if(tmp.fir!=-1) return tmp;
		return query(rs,mid+1,r,v);
	}
}T1;
struct Segment_Tree2{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	int mx[N<<2],tag[N<<2];
	inline void pushup(int rt){
		mx[rt]=max(mx[ls],mx[rs]);
	}
	inline void pushtag(int rt,int v){
		mx[rt]=tag[rt]=v;
	}
	inline void pushdown(int rt){
		if(tag[rt]==-1) return ;
		pushtag(ls,tag[rt]);
		pushtag(rs,tag[rt]);
		tag[rt]=-1;
	}
	inline void build(int rt,int l,int r){
		mx[rt]=0,tag[rt]=-1;
		if(l==r) return ;
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r); 
	}
	inline void modify(int rt,int l,int r,int L,int R,int v){
		if(L<=l&&r<=R){
			pushtag(rt,v);
			return ;
		}
		pushdown(rt);
		int mid=l+r>>1;
		if(L<=mid) modify(ls,l,mid,L,R,v);
		if(R>mid) modify(rs,mid+1,r,L,R,v);
		pushup(rt);
	}
	inline int query(int rt,int l,int r,int v){
		if(mx[rt]<v) return -1;
		if(l==r) return l;
		pushdown(rt);
		int mid=l+r>>1;
		int tmp=query(rs,mid+1,r,v);
		if(tmp==-1) tmp=query(ls,l,mid,v);
		pushup(rt);
		return tmp;
	}
	#undef ls
	#undef rs
}T2;
struct node{
	mutable int l,r,v;
	node(int V=0){ l=r=n+1,v=V; }
	node(int L,int R,int V){ l=L,r=R,v=V; }
	inline friend bool operator<(const node &a,const node &b){
		return a.v<b.v||(a.v==b.v&&a.l>b.l);
	}
};
set<node>st;
int main(){
	/*
	...
	*/ 
	for(int i=1;i<=n;i++){
		int x=b[i];
		st.insert(node(i,i,0));
		T1.modify(1,0,n+1,x,i);
		T2.modify(1,1,n,i,i,0);
		auto it=st.lower_bound(node(x));
		for(;it!=st.end()&&(it->v==x);){
			int l=(*it).l,r=(*it).r;
			auto itr=it;
			for(++itr;itr!=st.end();++itr)
				if(itr->v==x&&itr->r==l-1) l=itr->l;
				else break;
			st.erase(it,itr);
			while(r>=l){
				pii tmp=T1.query(1,0,n+1,r-1);
				int y=tmp.fir,L=max(l,tmp.sec+1);
				st.insert(node(L,r,y));
				T2.modify(1,1,n,L,r,y);
				r=L-1;
			}
			it=st.lower_bound(node(x));
		}
	}
	/*
	...
	*/ 
}
```
时间复杂度 $O(n\log n)$。

# FHQ-Treap 维护凸分段一次函数
```cpp
const int N=;
const ll INF=1e16;
namespace FHQ_Func{
	//下凸壳 
	//(len,v) 长为 len，斜率为 v 
	mt19937_64 R(time(0));
	struct node{
		ll len,siz,v,tag;
		int pr,cnt,son[2];
	}a[N*10];
	#define ls (a[rt].son[0])
	#define rs (a[rt].son[1])
	int stk[N*10],top,siz;
	namespace Opers{
		inline void del(int rt){
			stk[++top]=rt;
		}
		inline int newnode(ll len,ll v){
			if(!len) return 0;
			int rt=top?stk[top--]:++siz;
			ls=rs=0,a[rt].pr=R(),a[rt].len=a[rt].siz=len;
			a[rt].v=v,a[rt].tag=0,a[rt].cnt=1;
			return rt;
		}
		inline void pushup(int rt){
			a[rt].siz=a[ls].siz+a[rs].siz+a[rt].len;
			a[rt].cnt=a[ls].cnt+a[rs].cnt+1;
		}
		inline void pushtag(int rt,ll v){
			if(!rt) return ;
			a[rt].v+=v,a[rt].tag+=v;
		}
		inline void pushdown(int rt){
			if(!a[rt].tag) return ;
			if(ls) pushtag(ls,a[rt].tag);
			if(rs) pushtag(rs,a[rt].tag);
			a[rt].tag=0;
		}
		inline void split0(int rt,int &x,int &y,ll k){
			if(!rt){
				x=y=0;
				return ;
			}
			pushdown(rt);
			if(a[ls].siz+a[rt].len<=k)
				x=rt,split0(rs,rs,y,k-a[ls].siz-a[rt].len);
			else
				y=rt,split0(ls,x,ls,k);
			pushup(rt);
		}
		inline int merge1(int x,int y){//min +
			if(!x||!y) return x+y;
			pushdown(x),pushdown(y);
			if(a[x].pr<a[y].pr){
				a[x].son[1]=merge1(a[x].son[1],y);
				pushup(x);
				return x;
			}else{
				a[y].son[0]=merge1(x,a[y].son[0]);
				pushup(y);
				return y;
			}
		}
		inline int cut(int rt,ll k){
			if(ls){
				pushdown(rt);
				int tmp=cut(ls,k);
				pushup(rt);
				return tmp;
			}
			a[rt].len-=k,a[rt].siz-=k;
			return newnode(k,a[rt].v);
		}
		inline void split1(int rt,int &x,int &y,ll k){//[0,k]
			if(!k){
				x=0,y=rt;
				return ;
			}
			if(k>=a[rt].siz){
				x=rt,y=0;
				return ;
			}
			split0(rt,x,y,k);
			if(k>a[x].siz) x=merge1(x,cut(y,k-a[x].siz));
		}
		inline void split2(int rt,int &x,int &y,ll v){//<=v
			if(!rt){
				x=y=0;
				return ;
			}
			pushdown(rt);
			if(a[rt].v<=v)
				x=rt,split2(rs,rs,y,v);
			else
				y=rt,split2(ls,x,ls,v);
			pushup(rt);
		}
		inline int merge1s(int x,int y){//min +(值域相交)
			if(!x||!y) return x+y;
			if(a[x].cnt>a[y].cnt) swap(x,y);
			pushdown(x);
			int A,B,C,lp=a[x].son[0],rp=a[x].son[1];
			split2(y,A,B,a[x].v-1);
			split2(B,B,C,a[x].v);
			if(B) a[B].len+=a[x].len,a[B].siz+=a[x].len;
			else B=newnode(a[x].len,a[x].v);
			del(x);
			return merge1(merge1(merge1s(lp,A),B),merge1s(rp,C));
		}
		inline int merge2(int x,int y){//+
			if(!x||!y) return x+y;
			if(a[x].cnt>a[y].cnt) swap(x,y);
			pushdown(x);
			int A,B,C,lp=a[x].son[0],rp=a[x].son[1];
			split1(y,A,B,a[lp].siz);
			split1(B,B,C,a[x].len);
			pushtag(B,a[x].v);
			del(x);
			return merge1(merge1(merge2(lp,A),B),merge2(rp,C));
		}
		inline void insert(int &rt,ll len,ll v){
			int A,B,C;
			split2(rt,A,B,v-1);
			split2(B,B,C,v);
			if(B) a[B].len+=len,a[B].siz+=len;
			else B=newnode(len,v);
			rt=merge1(merge1(A,B),C);
		}
		inline ll query(int rt){
			if(!rt) return 0;
			pushdown(rt);
			return a[rt].v*a[rt].len+query(ls)+query(rs);
		}
		inline void dfs1(int rt){
			if(!rt) return ;
			pushdown(rt);
			dfs1(ls);
			printf("(%lld,%lld) %d\n",a[rt].v,a[rt].len,a[rt].siz);
			dfs1(rs);
		}
	}
	#undef ls
	#undef rs
}
using namespace FHQ_Func::Opers;
```

维护差分序列，设定义域为 $[l,r]$。

`split1` 将分裂出 $[l,l+k]$，`split2` 将把差分序列中 $\le v$ 的前缀分裂出。`merge1` 将对两个值域不交的凸分段函数做 $(\min,+)$ 卷积，即归并差分序列，`merge1s` 将对两个值域相交的凸分段函数做 $(\min,+)$ 卷积，`merge2` 将对两个定义域相同的凸分段函数做加法。

如要求值，需要手动维护定义域左端点处值。

时间复杂度未知，不超过 $O(n\log^2 n)$，常数较小。

# KTT 维护直线

```cpp
const ll INF=1e18;
struct Func{
	int k;
	ll b;
	inline friend Func operator+(const Func &a,const Func &b){ return (Func){a.k+b.k,a.b+b.b}; }
	inline void add(ll v){ b+=k*v; }
};
inline auto max(Func a,Func b){
	if(a.k<b.k||a.k==b.k&&a.b<b.b) swap(a,b);
	if(a.b>=b.b) return mpr(a,INF);
	return mpr(b,(b.b-a.b)/(a.k-b.k));
}
struct node{
	Func mx;
	ll x;
	inline friend node operator+(const node &a,const node &b){
		auto tp=max(a.mx,b.mx);
		return {tp.fir,min({a.x,b.x,tp.sec})};
	}
};
struct KTT{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	node a[N<<2];
	ll tag[N<<2];
	inline void pushup(int rt){
		a[rt]=a[ls]+a[rs];
	}
	inline void pushtag(int rt,ll v){
		tag[rt]+=v,a[rt].x-=v,a[rt].mx.add(v);
	}
	inline void pushdown(int rt){
		if(!tag[rt]) return ;
		pushtag(ls,tag[rt]),pushtag(rs,tag[rt]);
		tag[rt]=0;
	}
	inline void build(int rt,int l,int r){
		a[rt]={{0,0},INF},tag[rt]=0;
		if(l==r) return ;
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r);
	}
	inline void modify(int rt,int l,int r,int p,int k,ll b){
		if(l==r){ a[rt]={{k,b-tag[rt]*k},INF};return ; }
		pushdown(rt);
		int mid=l+r>>1;
		if(p<=mid) modify(ls,l,mid,p,k,b);
		else modify(rs,mid+1,r,p,k,b);
		pushup(rt);
	}
	inline void defeat(int rt,int l,int r,ll v){
		if(v<=a[rt].x) return pushtag(rt,v);
		int mid=l+r>>1;
		ll tp=tag[rt]+v;
		defeat(ls,l,mid,tp),defeat(rs,mid+1,r,tp);
		pushup(rt),tag[rt]=0;
	}
	inline void update(int rt,int l,int r,int L,int R,int k){
		if(L<=l&&r<=R) return defeat(rt,l,r,k);
		pushdown(rt);
		int mid=l+r>>1;
		if(L<=mid) update(ls,l,mid,L,R,k);
		if(R>mid) update(rs,mid+1,r,L,R,k);
		pushup(rt);
	}
	inline node query(int rt,int l,int r,int L,int R){
		if(L>R) return {{0,0},INF};
		if(L<=l&&r<=R) return a[rt];
		pushdown(rt);
		int mid=l+r>>1;
		if(R<=mid) return query(ls,l,mid,L,R);
		if(L>mid) return query(rs,mid+1,r,L,R);
		return query(ls,l,mid,L,mid)+query(rs,mid+1,r,mid+1,R);
	}
}T;
```

有 $n$ 条直线 $f_i(x)=k_ix+b_i$，有序列 $x_{1\sim n}$。

`update` 令 $\forall i\in[l,r],x_i\gets x_i+k(k>0)$，`query` 求 $\max_{i=l}^r f_i(x_i)$。

支持单点修改直线。

时间复杂度 $O(n\log^2n+m\log^3 n+q\log n)$。

# 区间加区间历史和
```cpp
const int N=;
struct Line{
	ll k,b;
	Line(ll K=0,ll B=0){ k=K,b=B; }
	inline friend Line operator+(const Line &a,const Line &b){ return Line(a.k+b.k,a.b+b.b); }
	inline void operator+=(const Line &a){ k+=a.k,b+=a.b; }
	inline friend Line operator*(const Line &a,const ll &b){ return Line(a.k*b,a.b*b); }
	inline ll getv(ll x){ return k*x+b; }
};
int n,q,a[N];
struct Segment_Tree{
	#define ls (rt<<1)
	#define rs (rt<<1|1)
	Line sum[N<<2],tag[N<<2];
	inline void pushup(int rt){
		sum[rt]=sum[ls]+sum[rs];
	}
	inline void pushtag(int rt,int l,int r,Line v){
		sum[rt]+=v*(r-l+1);
		tag[rt]+=v;
	}
	inline void pushdown(int rt,int l,int r){
		if(tag[rt].k||tag[rt].b){
			int mid=l+r>>1;
			pushtag(ls,l,mid,tag[rt]);
			pushtag(rs,mid+1,r,tag[rt]);
			tag[rt]=Line();
		}
	}
	inline void build(int rt,int l,int r){
		if(l==r){
			sum[rt]=Line(a[l],a[l]);
			return ;
		}
		int mid=l+r>>1;
		build(ls,l,mid),build(rs,mid+1,r);
		pushup(rt); 
	}
	inline void modify(int rt,int l,int r,int p,Line v){
		if(l==r){
			sum[rt]+=v;
			return ;
		}
		pushdown(rt,l,r);
		int mid=l+r>>1;
		if(p<=mid) modify(ls,l,mid,p,v);
		else modify(rs,mid+1,r,p,v);
		pushup(rt);
	}
	inline void modify(int rt,int l,int r,int L,int R,Line v){
		if(L<=l&&r<=R){
			pushtag(rt,l,r,v);
			return ;
		}
		pushdown(rt,l,r);
		int mid=l+r>>1;
		if(L<=mid) modify(ls,l,mid,L,R,v);
		if(R>mid) modify(rs,mid+1,r,L,R,v);
		pushup(rt);
	}
	inline ll query(int rt,int l,int r,int L,int R,ui x){
		if(L<=l&&r<=R)
			return sum[rt].getv(x);
		pushdown(rt,l,r);
		int mid=l+r>>1;
		ll ans=0;
		if(L<=mid) ans+=query(ls,l,mid,L,R,x);
		if(R>mid) ans+=query(rs,mid+1,r,L,R,x);
		pushup(rt);
		return ans;
	}
}T;
```

# 哈希表

```cpp
template<class P,class Q>
class HashTable{
	static const int mod=5e5+9,L=mod+10;
	int head[L],nxt[N],siz;
	P val[N];
	Q sav[N],z;
	public:
	inline void clear(){
		for(int i=1;i<=siz;i++){
			head[val[i]%mod]=0,nxt[i]=val[i]=0;
			Q tmp=z;
			swap(sav[i],tmp);
		}
		siz=0;
	}
	inline void insert(P y){
		val[++siz]=y;
		nxt[siz]=head[y%mod];
		head[y%mod]=siz;
	}
	inline Q &operator[](const P y){
		int x=y%mod;
		for(int i=head[x];i;i=nxt[i])
			if(val[i]==y)
				return sav[i];
		insert(y);
		return sav[siz];
	}
	inline bool count(const P y){
		int x=y%mod;
		for(int i=head[x];i;i=nxt[i])
			if(val[i]==y)
				return 1;
		return 0;
	}
};
template<class P>
class HashSet{
	static const int mod=5e5+9,L=mod+10;
	int head[L],nxt[N],siz;
	P val[N];
	public:
	inline void clear(){
		for(int i=1;i<=siz;i++)
			head[val[i]%mod]=0,nxt[i]=val[i]=0;
		siz=0;
	}
	inline void ins(P y){
		val[++siz]=y;
		nxt[siz]=head[y%mod];
		head[y%mod]=siz;
	}
	inline void insert(const P y){
		int x=y%mod;
		for(int i=head[x];i;i=nxt[i])
			if(val[i]==y)
				return ;
		ins(y);
	}
	inline bool count(const P y){
		int x=y%mod;
		for(int i=head[x];i;i=nxt[i])
			if(val[i]==y)
				return 1;
		return 0;
	}
};
```

# 矩阵乘法

```cpp
struct Matrix{
	vector<vector<int>>a;
	int n,m;
	inline void init(int N,int M){
		n=N,m=M;
		a.resize(n);
		for(int i=0;i<n;i++)
			a[i].resize(m,0);
	}
	inline vector<int>& operator[](int x){ return a[x]; }
	inline friend Matrix operator*(Matrix a,Matrix b){
		Matrix c;
		c.init(a.n,b.m);
		for(int k=0;k<a.m;k++){
			int pos[V],top=0;
			for(int j=0;j<b.m;j++)
				if(b[k][j])
					pos[++top]=j;
			for(int i=0;i<c.n;i++)
				if(a[i][k])
					for(int j=1;j<=top;j++)
						inc(c[i][pos[j]],1ll*a[i][k]*b[k][pos[j]]%mod);
		}
		return c;
	}
};
struct Matrix{
	int a[2][2];
	int n,m;
	inline void init(int N,int M){
		n=N,m=M;
		for(int i=0;i<n;i++)
			for(int j=0;j<m;j++)
				a[i][j]=0;
	}
	inline void Einit(int N){
		n=m=N;
		for(int i=0;i<n;i++)
			for(int j=0;j<n;j++)
				a[i][j]=i==j;
	}
	inline int* operator[](int x){ return a[x]; }
	inline friend Matrix operator*(Matrix a,Matrix b){
		Matrix c;
		c.init(a.n,b.m);
		for(int k=0;k<a.m;k++)
			for(int i=0;i<c.n;i++)
				for(int j=0;j<b.m;j++)
					inc(c[i][j],1ll*a[i][k]*b[k][j]%mod);
		return c;
	}
}; 
struct Matrix{
	ll a[V][V];
	int n,m;
	inline void init(int N,int M){
		n=N,m=M;
		for(int i=0;i<n;i++)
			for(int j=0;j<m;j++)
				a[i][j]=-INF;
	}
	inline void Einit(int N){
		n=m=N;
		for(int i=0;i<n;i++)
			for(int j=0;j<n;j++)
				a[i][j]=i==j?0:-INF;
	}
	inline ll* operator[](int x){ return a[x]; }
	inline friend Matrix operator*(Matrix a,Matrix b){
		Matrix c;
		c.init(a.n,b.m);
		for(int k=0;k<a.m;k++)
			for(int i=0;i<c.n;i++)
				for(int j=0;j<b.m;j++)
					upd(c[i][j],a[i][k]+b[k][j]);
		return c;
	}
};
struct Matrix{
    bitset<N>a[N],b[N];
    int n,m;
    inline void init(int N){
        n=m=N;
        for(int i=0;i<n;i++)
            a[i].reset(),b[i].reset();
    }
    inline void Einit(int N){
        n=m=N;
        for(int i=0;i<n;i++)
            a[i].reset(),b[i].reset();
        for(int i=0;i<n;i++)
            a[i][i]=b[i][i]=1;
    }
    inline friend Matrix operator*(Matrix a,Matrix b){
        Matrix c;
        c.init(a.n);
        for(int i=0;i<a.n;i++)
            for(int j=0;j<a.n;j++)
                c.a[i][j]=c.b[j][i]=(a.a[i]&b.b[j]).any();
        return c;
    }
};
```
# 定值矩阵光速幂

```cpp
Matrix P0[Bc],P1[Bc],P2[Bc],P3[Bc];
inline void init(Matrix C){
	P0[0].Einit(C.n),P1[0].Einit(C.n),P2[0].Einit(C.n),P3[0].Einit(C.n);
	for(int i=1;i<=B;i++) P0[i]=P0[i-1]*C;C=P0[B];
	for(int i=1;i<=B;i++) P1[i]=P1[i-1]*C;C=P1[B];
	for(int i=1;i<=B;i++) P2[i]=P2[i-1]*C;C=P2[B];
	for(int i=1;i<=B;i++) P3[i]=P3[i-1]*C;
}
inline void MulP(Matrix &S,ll c){
	S=S*P3[c/B3]*P2[(c%B3)/B2]*P1[(c%B2)/B]*P0[c%B];
}
```

# 反射容斥

```cpp
inline int Calc(int n,int m,int l,int r){
	int ans=0;
	for(int k=0;n-k*(r-l)>=0;k++) ans=add(ans,C(n+m,n-k*(r-l)));
	for(int k=0;n-k*(r-l)+r>=0;k++) ans=dec(ans,C(n+m,n-k*(r-l)+r));
	for(int k=-1;n-k*(r-l)<=n+m;k--) ans=add(ans,C(n+m,n-k*(r-l)));
	for(int k=-1;n-k*(r-l)+r<=n+m;k--) ans=dec(ans,C(n+m,n-k*(r-l)+r));
	return ans;
}
inline int Cp(int n,int m){
	return n+m&1?0:C(n,(n+m)/2);
}
inline int Calc(int n,int m,int l,int r){
    int ans=0;
    l*=2,r*=2;
    for(int k=0;m-k*(r-l)>=-n;k++) ans=add(ans,Cp(n,m-k*(r-l)));
    for(int k=-1;m-k*(r-l)<=n;k--) ans=add(ans,Cp(n,m-k*(r-l)));
    for(int k=0;m-k*(r-l)-r>=-n;k++) ans=dec(ans,Cp(n,m-k*(r-l)-r));
    for(int k=-1;m-k*(r-l)-r<=n;k--) ans=dec(ans,Cp(n,m-k*(r-l)-r));
    return ans;
}
```
允许向右或向上走，计算从 $(0,0)$ 到达 $(n,m)$ 且不**触碰** $y=x+l$ 和 $y=x+r$ 的路径数。


允许向右上或向右下走，计算从 $(0,0)$ 到达 $(n,m)$ 且不**触碰** $y=l$ 和 $y=r$ 的路径数。

时间复杂度 $O(\dfrac{n+m}{r-l})$。
# 最近公共祖先


```cpp
struct ST_table{
	int dep[N],dfn[N],tim,st[19][N];
	inline void dfs(int x,int fa){
		dep[x]=dep[fa]+1;
		st[0][dfn[x]=++tim]=fa;
		for(int i=head[x];i;i=a[i].nxt){
			int t=a[i].to;
			if(t==fa) continue;
			dfs(t,x);
		}
	}
	inline int cmp(int x,int y){
		return dep[x]<dep[y]?x:y;
	}
	inline void init(){
		dfs(1,0);
		for(int i=1;(1<<i)<=n;i++)
			for(int j=1;j+(1<<i)-1<=n;j++)
				st[i][j]=cmp(st[i-1][j],st[i-1][j+(1<<i-1)]);
	}
	inline int LCA(int x,int y){
		if(x==y) return x;
		x=dfn[x],y=dfn[y];
		if(x>y) swap(x,y);
		x++;
		int i=__lg(y-x+1),p=1<<i;
		return cmp(st[i][x],st[i][y-p+1]);
	}
	inline int dis(int u,int v){
		return dep[u]+dep[v]-2*dep[LCA(u,v)];
	}
}st;
```
# 虚树

```cpp
namespace FT{
	inline bool cmp(int u,int v){
		return st.dfn[u]<st.dfn[v];
	}
	int head[N],cnt;
	struct EdgeT{
		int to,nxt;
	}a[N];
	inline void adde(int u,int v){
		cnt++;
		a[cnt].to=v;
		a[cnt].nxt=head[u];
		head[u]=cnt;
	}
	vector<int>c;
	inline void build(){
		sort(c.begin(),c.end(),cmp);
		c.erase(unique(c.begin(),c.end()),c.end());
		int s=c.size();
		for(int i=1;i<s;i++)
			c.push_back(st.LCA(c[i-1],c[i]));
		sort(c.begin(),c.end(),cmp);
		c.erase(unique(c.begin(),c.end()),c.end());
		for(int i=1;i<c.size();i++){
			int l=st.LCA(c[i-1],c[i]);
			adde(l,c[i]);
		}
	}
	inline int solve(vector<int>t){
		c=t;
		build();
		
		cnt=0;
		for(auto tmp:c)
			head[tmp]=0;
		return tmp;
	}
}
```
# 范围随机数生成


```cpp
namespace rad{
	mt19937_64 R(chrono::system_clock::now().time_since_epoch().count());
	inline int Rand(int l,int r){
		uniform_int_distribution<int> distribution(l,r);
		return distribution(R);
	}
}
using namespace rad;
```
# 拉格朗日插值


```cpp
namespace PolyC{
    #define Poly vector<int>
    inline int qpow(int x,int y){
        int res=1;
        while(y){
            if(y&1) res=1ll*res*x%mod;
            x=1ll*x*x%mod;
            y>>=1;
        }
        return res;
    }
    inline int add(int a,int b){
        return a+b>=mod?a+b-mod:a+b;
    }
    inline int dec(int a,int b){
        return a>=b?a-b:a+mod-b;
    }
    inline Poly operator+(const Poly &a,const Poly &b){
        Poly F=a;
        F.resize(max(a.size(),b.size()));
        for(int i=0;i<b.size();i++)
            F[i]=add(F[i],b[i]);
        return F;
    }
    inline Poly operator-(const Poly &a,const Poly &b){
        Poly F=a;
        F.resize(max(a.size(),b.size()));
        for(int i=0;i<b.size();i++)
            F[i]=dec(F[i],b[i]);
        return F;
    }
    inline Poly operator+(const Poly &a,const int &b){
        Poly F=a;
        F[0]=add(F[0],b);
        return F;
    }
    inline Poly operator-(const Poly &a,const int &b){
        Poly F=a;
        F[0]=dec(F[0],b);
        return F;
    }
    inline Poly operator*(const Poly &a,const int &b){
        Poly F=a;
        for(int i=0;i<F.size();i++)
            F[i]=1ll*F[i]*b%mod;
        return F;
    }
    inline Poly Mulx(const Poly &a,int c=1){
        Poly F(max(c,0),0);
        for(int i=max(-c,0);i<a.size();i++)
            F.push_back(a[i]);
        return F;
    }
}
using namespace PolyC;
int iv[N];
inline Poly Lagrange(Poly R){
    int n=R.size()-1;
    Poly F(1,1),G(n,0);
    for(int i=1;i<=n;i++)
        iv[i]=qpow(mod-i,mod-2),F=Mulx(F)-F*i;
    for(int i=1;i<=n;i++){
        int k=1;
        for(int j=1;j<=n;j++)
            if(i!=j)
                k=1ll*k*(i-j+mod)%mod;
        k=1ll*R[i]*qpow(k,mod-2)%mod;
        for(int j=0,t=0;j<n;j++){
            int tmp=1ll*(F[j]-t+mod)*iv[i]%mod;
            G[j]=(G[j]+1ll*k*tmp)%mod,t=tmp;
        } 
    }
    return G;
}
inline Poly Lagrange(Poly X,Poly R){
    int n=R.size();
    Poly F(1,1),G(n,0);
    for(int i=0;i<n;i++)
        iv[i]=qpow(mod-X[i],mod-2),F=Mulx(F)-F*X[i];
    for(int i=0;i<n;i++){
        int k=1;
        for(int j=0;j<n;j++)
            if(i!=j)
                k=1ll*k*(X[i]-X[j]+mod)%mod;
        k=1ll*R[i]*qpow(k,mod-2)%mod;
        for(int j=0,t=0;j<n;j++){
            int tmp=1ll*(F[j]-t+mod)*iv[i]%mod;
            G[j]=(G[j]+1ll*k*tmp)%mod,t=tmp;
        } 
    }
    return G;
}
inline int calc(Poly F,int x){
    int s=0;
    for(int i=F.size()-1;i>=0;i--)
        s=(F[i]+1ll*s*x)%mod;
    return s;
}
inline int Lagrange(Poly R,int v){
    int n=R.size()-1,s=0;
    for(int i=1;i<=n;i++){
        int p=1,q=1;
        for(int j=1;j<=n;j++)
            if(i!=j)
            	p=1ll*p*dec(v,j)%mod,
            	q=1ll*q*dec(i,j)%mod;
    	s=(s+1ll*p*qpow(q,mod-2)%mod*R[i])%mod;
    }
    return s;
}
int pr[N],sf[N];
inline int Lagrange(int x0,int x,Poly R){
    int n=R.size()-1;
    if(x<=x0+n) return R[x-x0];
    pr[0]=dec(x,x0),sf[n+1]=1;
    for(int i=1;i<=n;i++)
    	pr[i]=1ll*pr[i-1]*dec(x,add(x0,i))%mod;
    for(int i=n;i>=0;i--)
    	sf[i]=1ll*sf[i+1]*dec(x,add(x0,i))%mod;
    int s=0;
    for(int i=0;i<=n;i++){
    	int u=sf[i+1];
    	if(i) u=1ll*u*pr[i-1]%mod;
    	u=1ll*u*ifac[i]%mod*ifac[n-i]%mod;
    	if(n-i&1) u=dec(0,u);
    	inc(s,1ll*R[i]*u%mod);
	}
    return s;
}
```
# 压位布尔数组

```cpp
struct Bitset{
	ull v[S];
	int n,N;
	Bitset(int s=0){ N=s,n=(s>>6)+2; }
	inline int size(){ return N; }
	inline void set(){ fill(v,v+n,-1); }
	inline void reset(){ fill(v,v+n,0); }
	inline void resize(int s){ N=s,n=(s>>6)+2;reset(); }
	inline bool operator[](const int &x){ return (v[x>>6]>>(x&63))&1; }
	inline void set(int p){ v[p>>6]|=1ull<<(p&63); }
	inline void reset(int p){ v[p>>6]&=~(1ull<<(p&63)); }
	inline friend Bitset operator &(const Bitset &a,const Bitset &b){
		Bitset c(a.N);
		for(int i=0;i<a.n;i++) c.v[i]=a.v[i]&b.v[i];
		return c;
	}
	inline friend Bitset operator |(const Bitset &a,const Bitset &b){
		Bitset c(a.N);
		for(int i=0;i<a.n;i++) c.v[i]=a.v[i]|b.v[i];
		return c;
	}
	inline friend Bitset operator ^(const Bitset &a,const Bitset &b){
		Bitset c(a.N);
		for(int i=0;i<a.n;i++) c.v[i]=a.v[i]^b.v[i];
		return c;
	}
	inline void operator |=(const Bitset &b){ for(int i=0;i<n;i++) v[i]|=b.v[i]; }
	inline void operator &=(const Bitset &b){ for(int i=0;i<n;i++) v[i]&=b.v[i]; }
	inline void operator ^=(const Bitset &b){ for(int i=0;i<n;i++) v[i]^=b.v[i]; }
	inline int Find_first(){
		for(int i=0;i<n;i++)
			if(v[i])
				return __builtin_ctzll(v[i])+(i<<6);
		return (n+1)<<6;
	} 
	inline int Find_next(int p){
		if((p&63)!=63){
			ull vt=v[p>>6]>>((p&63)+1);
			if(vt) return p+__builtin_ctzll(vt)+1;
		}
		for(int i=(p>>6)+1;i<n;i++)
			if(v[i])
				return __builtin_ctzll(v[i])+(i<<6);
		return (n+1)<<6;
	}
};
```
# 可删堆

```cpp
template<class ND>
struct Set{
	priority_queue<ND>p,q;
	inline void upd(){ while(!q.empty()&&p.top()==q.top()) p.pop(),q.pop(); }
	public:
	inline int size(){ return p.size()-q.size(); }
	inline bool empty(){ return p.size()==q.size(); }
	inline void ins(ND v){ p.push(v); }
	inline void del(ND v){ q.push(v); }
	inline ND top(){ upd();return p.top(); }
	inline void pop(){ upd();p.pop(); }
};
```
# zkw 线段树

```cpp
struct Segment_Tree{
    #define ls (rt<<1)
    #define rs (rt<<1|1)
    int m,t,len[M];
    ll tag[M],sum[M];
    bool cl[M];
    inline void pushup(int rt){
        sum[rt]=sum[ls]+sum[rs];
    }
    inline void pushtag(int rt,ll v){
        tag[rt]+=v,sum[rt]+=v*len[rt];
    }
    inline void pushclr(int rt){
        sum[rt]=tag[rt]=0,cl[rt]=1;
    }
    inline void pushdown(int rt){
        if(cl[rt]) pushclr(ls),pushclr(rs),cl[rt]=0;
        if(tag[rt]) pushtag(ls,tag[rt]),pushtag(rs,tag[rt]),tag[rt]=0;
    }
    inline void build(int n){
        for(m=1;m<=n;m<<=1,t++);
        //printf("%d %d\n",m,t);
        for(int i=m+1;i<=m+n;i++)
            len[i]=1,sum[i]=a[i-m];
        for(int i=m;i;i--)
            len[i]=len[i<<1]+len[i<<1|1],
            sum[i]=sum[i<<1]+sum[i<<1|1];
    }
    inline void modify(int l,int r,int v){
        l+=m-1,r+=m+1;
        for(int i=t;i;i--) pushdown(l>>i),pushdown(r>>i);
        for(;l^r^1;){
            if(~l&1) pushtag(l^1,v);
            if(r&1) pushtag(r^1,v);
            l>>=1,r>>=1;
            pushup(l),pushup(r);
        }
        for(l>>=1;l;l>>=1) pushup(l);
    }
    inline void clear(int l,int r){
        l+=m-1,r+=m+1;
        for(int i=t;i;i--) pushdown(l>>i),pushdown(r>>i);
        for(;l^r^1;){
            if(~l&1) pushclr(l^1);
            if(r&1) pushclr(r^1);
            l>>=1,r>>=1;
            pushup(l),pushup(r);
        }
        for(l>>=1;l;l>>=1) pushup(l);
    }
    inline ll query(int l,int r){
        ll v=0;
        l+=m-1,r+=m+1;
        for(int i=t;i;i--) pushdown(l>>i),pushdown(r>>i);
        for(;l^r^1;){
            if(~l&1) v+=sum[l^1];
            if(r&1) v+=sum[r^1];
            l>>=1,r>>=1;
        }
        return v;
    }
}T;
```
这是下传标记版的区间加区间清零区间求和。


```cpp
struct Segment_Tree{
    #define ls (rt<<1)
    #define rs (rt<<1|1)
    int m,mx[N<<2];
    inline void pushup(int rt){
    	mx[rt]=max(mx[ls],mx[rs]);
    }
    inline void build(int n,int *v){
        for(m=1;m<=n;m<<=1);
        for(int i=m+1;i<=m+n;i++)
            mx[i]=v[i-m];
        for(int i=m;i;i--)
        	mx[i]=max(mx[i<<1],mx[i<<1|1]);
    }
    inline void modify(int p,int v){
        p+=m,mx[p]=v;
        for(p>>=1;p;p>>=1) pushup(p);
    }
    inline int query(int l,int r){
        l+=m-1,r+=m+1;
        int v=0;
        for(;l^r^1;){
            if(~l&1) v=max(v,mx[l^1]);
            if(r&1) v=max(v,mx[r^1]);
            l>>=1,r>>=1;
        }
        return v;
    }
}T;
```
这是单点修改区间最大值。

```cpp
struct Segment_Tree{
    #define ls (rt<<1)
    #define rs (rt<<1|1)
    int m;
	ll tag[N<<2],mx[N<<2];
    inline void pushup(int rt){
    	mx[rt]=max(mx[ls],mx[rs])+tag[rt];
    }
    inline void build(int n){
        for(m=1;m<=n;m<<=1);
        for(int i=1;i<=n+m;i++)
        	mx[i]=-INF;
    }
    inline void modify(int p,int v){
        p+=m,mx[p]=v;
        for(p>>=1;p;p>>=1) pushup(p);
    }
    inline void modify(int l,int r,int v){
        l+=m-1,r+=m+1;
        for(;l^r^1;){
            if(~l&1) tag[l^1]+=v,mx[l^1]+=v;
            if(r&1) tag[r^1]+=v,mx[r^1]+=v;
            l>>=1,r>>=1;
            pushup(l),pushup(r);
        }
        for(l>>=1;l;l>>=1) pushup(l);
    }
    inline ll query(){
    	return mx[1];
	}
    inline ll query(int l,int r){
        l+=m-1,r+=m+1;
        ll vl=-INF,vr=-INF;
        for(;l^r^1;){
        	vl+=tag[l],vr+=tag[r];
            if(~l&1) vl=max(vl,mx[l^1]);
            if(r&1) vr=max(vr,mx[r^1]);
            l>>=1,r>>=1;
        }
        ll v=max(vl+tag[l],vr+tag[r]);
        for(l>>=1;l;l>>=1) v+=tag[l];
        return v;
    }
}T;
```
区间加区间最大值。
# 颜色段均摊

```cpp
struct node{
	int l;
	mutable int r,v;
	node(int L=0,int R=-1,int V=0){ l=L,r=R,v=V; }
	inline friend bool operator<(const node &a,const node &b){
		return a.l<b.l;
	}
};
set<node>tr;
inline auto split(int p){
	auto it=tr.lower_bound(node(p));
	if(it!=tr.end()&&it->l==p)
	    return it;
	--it;
	int mr=it->r,mv=it->v;
	it->r=p-1;
	return tr.insert(node(p,mr,mv)).first;
}
inline void cover(int l,int r,int v){
	auto itr=split(r+1),itl=split(l);
	tr.erase(itl,itr),tr.insert(node(l,r,v));
}
```
# 迭代分块

```cpp
struct BLK1{
    int n,v1[N+256],v2[(N>>6)+256],v3[(N>>12)+256];
    inline void init(int N){
        for(int i=0;i<=N;i++) v1[i]=0;
        for(int i=0;i<=(N>>6)+1;i++) v2[i]=0;
        for(int i=0;i<=(N>>12)+1;i++) v3[i]=0;
        n=(N>>12)+1; 
    }
    inline void add(int x,int v){
        for(;x&63;x++) v1[x]+=v;
        for(x>>=6;x&63;x++) v2[x]+=v;
        for(x>>=6;x<=n;x++) v3[x]+=v;
    }
    inline int query(int x){
        return v1[x]+v2[x>>6]+v3[x>>12];
    }
    inline int query(int l,int r){
        return query(r)-query(l-1);
    }
}T1;
struct BLK2{
    int n,v1[N+256],v2[(N>>6)+256],v3[(N>>12)+256];
    inline void init(int N){
        for(int i=0;i<=N;i++) v1[i]=0;
        for(int i=0;i<=(N>>6)+2;i++) v2[i]=0;
        for(int i=0;i<=(N>>12)+2;i++) v3[i]=0;
        n=(N>>12)+2;
    }
    inline void add(int x,int v){
        v1[x]+=v,v2[x>>6]+=v,v3[x>>12]+=v;
    }
    inline int query(int x){
        int s=0;
        for(;x&63;x++) s+=v1[x];
        for(x>>=6;x&63;x++) s+=v2[x];
        for(x>>=6;x<=n;x++) s+=v3[x];
        return s;
    }
    inline void add(int l,int r,int v){
        add(l-1,-v),add(r,v);
    }
}T2;
```
# 强连通分量

```cpp
int tim,dfn[N],low[N],bel[N],stk[N],top,blk;
bool inc[N];
inline void Tarjan(int x){
	dfn[x]=low[x]=++tim,inc[x]=1,stk[++top]=x;
	for(auto t:a[x]){
		if(!dfn[t]) Tarjan(t),low[x]=min(low[x],low[t]);
		else if(inc[t]) low[x]=min(low[x],low[t]);
	}
	if(dfn[x]==low[x]){
		++blk;
		while(1){
			int p=stk[top--];
			inc[p]=0,bel[p]=blk;
			if(p==x) break;
		}
	}
}
```
# 斜率优化

```cpp
inline pii operator-(const pii &a,const pii &b){ return mpr(a.fir-b.fir,a.sec-b.sec); }
inline ll operator*(const pii &a,const pii &b){ return a.fir*b.sec-a.sec*b.fir; }
struct Convex_Hull{
	deque<pii>d;
	inline void clear(){ d.clear(); }
	inline bool check(pii a,pii b,pii c){ return (b-a)*(c-a)>0; }
	inline ll f(pii p,ll k){ return p.sec-k*p.fir; }
	inline void ins(pii p){
		while(d.size()>1&&!check(d[d.size()-2],d.back(),p)) d.pop_back();
		d.push_back(p);
	}
	inline ll query(ll k){
		if(!d.size()) return INF;
		while(d.size()>1&&f(d[0],k)>=f(d[1],k)) d.pop_front();
		return f(d[0],k);
	}
};
```
# 组合数

```cpp
inline int add(int x,int y){ return x+y>=mod?x+y-mod:x+y; }
inline int dec(int x,int y){ return x>=y?x-y:x-y+mod; }
inline void inc(int &x,int y){ x=add(x,y); }
inline int qpow(int x,int y){
	int res=1;
	while(y){
		if(y&1) res=1ll*res*x%mod;
		x=1ll*x*x%mod;
		y>>=1;
	}
	return res;
}
int fac[N],ifac[N];
inline void Prefix(int n){
	fac[0]=1;
	for(int i=1;i<=n;i++)
		fac[i]=1ll*fac[i-1]*i%mod;
	ifac[n]=qpow(fac[n],mod-2);
	for(int i=n;i;i--)
		ifac[i-1]=1ll*ifac[i]*i%mod;
}
inline int C(int n,int m){
	return n<m?0:1ll*fac[n]*ifac[m]%mod*ifac[n-m]%mod;
}
```
