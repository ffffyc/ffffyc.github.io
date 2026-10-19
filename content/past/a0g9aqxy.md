---
title: "题解综述"
date: 2021-05-31
category: "题解"
tags: ["小记"]
summary: "对这个蒟蒻的题解整理一下，方便回顾。 此处仅限有意义的题解。 算法分类 数论：SP106（斯特林数）、UVA11526（整除分块）、P5107（矩阵快速幂）、UVA12396&"
math: true
top: 2
hidden: true
source: https://www.luogu.com.cn/article/a0g9aqxy
slug: a0g9aqxy
---

对这个蒟蒻的题解整理一下，方便回顾。

此处仅限有意义的题解。

## 算法分类
数论：[SP106](https://www.luogu.com.cn/blog/cyffff/solution-sp106)（斯特林数）、[UVA11526](https://www.luogu.com.cn/blog/cyffff/solution-uva11526)（整除分块）、[P5107](https://www.luogu.com.cn/blog/cyffff/solution-p5107)（矩阵快速幂）、[UVA12396](https://www.luogu.com.cn/blog/cyffff/solution-UVA-12396)&[SP10114](https://www.luogu.com.cn/blog/cyffff/solution-sp10114)（素数筛）、[P3868](https://www.luogu.com.cn/blog/cyffff/solution-p3868)（$\text{CRT}$）、[P5491](https://www.luogu.com.cn/blog/cyffff/solution-p5491)（二次剩余）、[P2529](https://www.luogu.com.cn/blog/cyffff/ti-xie-p2529shoi2001-ji-gu-zhuan-hua-post)&[SP2124](https://www.luogu.com.cn/blog/cyffff/solution-sp2124)、[P5071](https://www.luogu.com.cn/blog/cyffff/solution-p5071)（$\text{Pollard-Rho}$）、[UVA10023](https://www.luogu.com.cn/blog/cyffff/solution-uva10023)（高精度）

搜索：[CF877D](https://www.luogu.com.cn/blog/cyffff/solution-cf877d)（BFS）、[P7428](https://www.luogu.com.cn/blog/cyffff/solution-p7428)（BFS）、[P7472](https://www.luogu.com.cn/blog/cyffff/solution-p7472)（BFS）

$\text{DS}$：[P1383](https://www.luogu.com.cn/blog/cyffff/solution-p1383)&[P6166](https://www.luogu.com.cn/blog/cyffff/solution-p6166)（主席树）、[CF915E](https://www.luogu.com.cn/blog/cyffff/solution-cf915e)（珂朵莉树）、[CF86D](https://www.luogu.com.cn/blog/cyffff/solution-cf86d)（莫队）、[P7333](https://www.luogu.com.cn/blog/cyffff/ti-xie-t1-jfca)（ST表）、[P7334](https://www.luogu.com.cn/blog/cyffff/ti-xie-t2-diao-da-post)（分块）、[P7335](luogu.com.cn/blog/cyffff/ti-xie-t3-yi-huo-post)（$\text{01-Trie}$）、[P5607](https://www.luogu.com.cn/blog/cyffff/solution-p5607)（线性基+线段树）、[P5048](https://www.luogu.com.cn/blog/cyffff/solution-p5048)&[SP32900](https://www.luogu.com.cn/blog/cyffff/solution-sp32900)（分块（在线化莫队））、[P7424](https://www.luogu.com.cn/blog/cyffff/solution-p7424)（主席树）、[P5071](https://www.luogu.com.cn/blog/cyffff/solution-p5071)（莫队+根号分治）、[P5528](https://www.luogu.com.cn/blog/cyffff/solution-p5528)（$\text{CDQ}$ 分治+根号分治）、[P7602](https://www.luogu.com.cn/blog/cyffff/solution-p7602)（主席树）、[P7448](https://www.luogu.com.cn/blog/cyffff/ti-xie-p7448p7601ynoi2007-rpiq)&[P7601](https://www.luogu.com.cn/blog/cyffff/solution-p7601)（莫队二离+二维分块）、[P7549](https://www.luogu.com.cn/blog/cyffff/solution-p7549)（平衡树）、[CF666E](https://www.luogu.com.cn/blog/cyffff/solution-cf666e)（广义 $\text{SAM}$+线段树合并）、[P5494](https://www.luogu.com.cn/blog/cyffff/talk-about-segument-trees-split)（线段树分裂）

 _这里把分块当成一种数据结构_ 

结论：[P7078](https://www.luogu.com.cn/blog/cyffff/solution-p7078)、[P7291](https://www.luogu.com.cn/blog/cyffff/solution-p7291)

$\dfrac{}{w}$：[P4795](https://www.luogu.com.cn/blog/cyffff/solution-p4795)（$\text{bitset}$）、[P5670](https://www.luogu.com.cn/blog/cyffff/solution-p5670)（指令集）

$\text{DP}$：[P2285](https://www.luogu.com.cn/blog/cyffff/solution-p2285)

计算几何：[CF429D](https://www.luogu.com.cn/blog/cyffff/solution-cf429d)

图论：[UVA315](https://www.luogu.com.cn/blog/cyffff/solution-uva315)（Tarjan割点）、[P7338](https://www.luogu.com.cn/blog/cyffff/solution-p7338)（二分图最大匹配）、[P7245](https://www.luogu.com.cn/blog/cyffff/solution-p7425)（网络流）、[P4578](https://www.luogu.com.cn/blog/cyffff/solution-p4578)（差分约束）

$\text{Poly}$：[P7364](https://www.luogu.com.cn/blog/cyffff/solution-p7364)、[P6800](https://www.luogu.com.cn/blog/cyffff/solution-p6800)、[P6828](https://www.luogu.com.cn/blog/cyffff/solution-p6828)、[P5245](https://www.luogu.com.cn/blog/cyffff/solution-p5245)、[P5273](https://www.luogu.com.cn/blog/cyffff/ti-xie-p5273-mu-ban-duo-xiang-shi-mi-han-shuo-jia-qiang-ban-post)、[P5277](https://www.luogu.com.cn/blog/cyffff/solution-p5277)、[P4239](https://www.luogu.com.cn/blog/cyffff/solution-p4239)、[P7431](https://www.luogu.com.cn/blog/cyffff/solution-p7431)
