---
title: "计算理论复习集"
kind: review
order: 0
date: 2026-10-24
math: true
unlisted: true
tags: []
---

## 1. Pumping Lemma（正则语言）

对于正则语言 $L$，存在长度 $p$，使得对任意 $s\in L$ 且 $|s|\ge p$，都存在划分 $s=xyz$ 满足：

- $|y|>0$，$|xy|\le p$；
- $\forall i\ge 0$，$xy^iz\in L$。

## 2. Pumping Lemma（上下文无关语言）

对于上下文无关语言 $L$，存在长度 $p$，使得对任意 $s\in L$ 且 $|s|\ge p$，都存在划分 $s=uvxyz$ 满足：

- $|vy|>0$，$|vxy|\le p$；
- $\forall i\ge 0$，$uv^ixy^iz\in L$。

## 3. 经典不可判定语言

- $A_{TM}$、$HALT_{TM}$；
- $SOME_{TM}$：至少接受一个输入的 TM $M$；
- $E_{TM}$：拒绝所有输入的 TM $M$；
- 所有 $L(M)$ 是正则语言的 TM $M$；
- $ALL_{CFG}$：接受所有输入的 CFG $G$；
- $AMBIG_{CFG}$：所有有歧义的 CFG $G$；
- $PCP$：给定一组骨牌，每个骨牌上下各有一个字符串，能否通过有限个骨牌的拼接，使得上下拼接后的字符串完全相同。

## 4. 规约方法

- 图灵规约：若有 $B$ Oracle 的 TM 可判定 $A$，则 $A\le_T B$；
- 映射规约：若有 $f$ 使得 $w\in A$ 当且仅当 $f(w)\in B$，则 $A\le_m B$。

## 5. 递归定理

对于任意递归函数 $t:\N\to\N$，存在 TM $F$ 使得 $t(\langle F\rangle)$ 是一个与 $F$ 等价的图灵机编码。

- **构造方法**：
    - 构造 TM $D$：输入 $\langle M\rangle$，输出 $\langle G\rangle$，其中 TM $G$ 的行为为：输入字符串 $y$，用输入 $y$ 模拟编码为 $M(\langle M\rangle)$ 的图灵机。
    - 构造 TM $V$：输入 $\langle M\rangle$，输出 $t(D(\langle M\rangle))$。
    - 构造 TM $F$：令 $\langle F\rangle=D(\langle V\rangle)$，那么 $F$ 的行为为：输入字符串 $y$，用输入 $y$ 模拟编码为 $V(\langle V\rangle)=t(D(\langle V\rangle))=t(\langle F\rangle)$ 的图灵机。
- **本质**：
    - 考虑表格 $M_i(\langle M_j\rangle)$，则 $D$ 同时是其中的对角线与一行，$V=t\circ D$ 对应其中另外一行。
    - 显然，$D$ 对应的行与对角线是一一等价的；
    - 考虑对角线与 $V$ 行的交点，与这一列上 $D$ 行是等价的，令 $D$ 行这一列的结果为 $\langle F\rangle$，那么 $V$ 行这一列的结果就是 $t(\langle F\rangle)$。
- **Kleene's s-n-m 定理**：
    - 对于 $n+m$ 个输入的 TM $M(x_{1,\dots,n},y_{1,\dots,m})$，存在递归函数 $t$ 使得 $T(\langle M\rangle,y_{1,\dots,m})=\langle M'\rangle$，其中 $M'(y_{1,\dots,m})=M(x_{1,\dots,n},y_{1,\dots,m})$。
    - 相当于把 $x$ 硬编码。
- **Kleene's 递归定理**：
    - 对于递归函数 $t:\N\times\N\to\N$，存在 TM $R$ 使得 $R(x)=t(\langle R\rangle,x)$。

## 6. Kolmogorov 复杂度

$K(x)$：能输出二进制串 $x$ 的最短「图灵机 + 输入」的长度。

- 基础上界：$K(x)\le |x|+c$，$K(x^n)\le |x|+c\log n$。
- 任意长度的不可压缩字符串都存在，大多数字符串是高度不可压缩的：随机串是 $c$-compressible 的概率不超过 $1/2^c$。
- $COMPRESS=\{(x,c) \mid K(x)\leq c\}$ 不可判定。

## 7. 空间复杂度

$\text{L}=\text{SPACE}(\log n)$，$\text{NL}=\text{NSPACE}(\log n)$，$\text{PSPACE}=\bigcup_k\text{SPACE}(n^k)$。

- $\text{L}\subseteq\text{NL}\subseteq\text{P}\subseteq\text{NP}\subseteq\text{PSPACE}=\text{NPSPACE}\subseteq\text{EXPTIME}$。
- **NL-complete PATH**：给定有向图 $G$，判断是否有 $s\to t$ 的路径。
    - PATH $\in$ NL：非确定性猜路径，记录当前节点和步数计数。
    - PATH 是 NL-C：对于任意的 $A\in\text{NL}$，构造 $M$ 在输入 $x$ 上的配置图，结点数为 $|\Sigma|^{O(\log n)}=O(\text{poly}(n))$，判定是否有边可以做到对数空间。
    - PATH $\in$ P：$\text{NL}\sube\text{P}$。
- **Savitch 定理**：
    - $\text{NL}\sube\text{L}^2$：分治求解 PATH 问题。
    - 若 $S(n)\ge\log n$，则 $\text{NSPACE}(S(n))\sube\text{SPACE}(S(n)^2)$：填充论证。
    - $\text{NPSPACE}=\text{PSPACE}$。
- **Immerman–Szelepcsényi 定理**：$\text{NL}=\text{coNL}$，$\text{NSPACE}(S(n))=\text{coNSPACE}(S(n))$。
- **PSPACE-complete TQBF**：全量化布尔公式 $Q_1x_1\dots Q_kx_k\phi(x_1,\dots,x_k)$。
    - TQBF $\in$ PSPACE：递归枚举。
    - TQBF 是 PSPACE-C：对于 PSPACE 语言定义布尔公式，从配置 $C_1$ 到 $C_2$ 在 $t$ 步内可达：$\Phi(C_1,C_2,t)=\exists C_m\forall(A,B)\in\{(C_1,C_m),(C_m,C_2)\}\Phi(A,B,t/2)$，可以进一步修改成 $\forall A\forall B\,(A=C_1\land B=C_m)\lor(A=C_m\land B=C_2)$。
    - TQBF 可化为 3-CNF，3-CNF 可规约至广义地理游戏 GG，故 GG 也是 PSPACE-complete 的。

## 8. 层次定理

- **时间层次定理**：对于时间可构造函数 $f(n)$，一定存在语言 $L$ 使得 $L$ 可以在 $O(f(n))$ 时间判定，但不能在 $o(f(n)/\log n)$ 时间内判定；故 $\text{P}\ne\text{EXPTIME}$。
- **空间层次定理**：对于空间可构造函数 $f(n)$，一定存在语言 $L$ 使得 $L$ 可以在 $O(f(n))$ 空间判定，但不能在 $o(f(n))$ 空间内判定；故 $\text{L}\ne\text{PSPACE}$。

## 9. 多项式层次 PH

- **基本定义与性质**：
    - 语言 $L$ 在 $\Sigma_i^p$ 中当且仅当存在多项式时间复杂度 TM $M$ 使得 $x\in L$ 等价于 $\exists u_1\in\{0,1\}^{q(|x|)}\forall u_2\in\{0,1\}^{q(|x|)}\dots Q_iu_i\in\{0,1\}^{q(|x|)}\,(M(x,u_1,\dots,u_i)=1)$；
    - $\Pi_i^p=\text{co}\Sigma_i^p$，即从 $\forall$ 量词开始。
    - $\Sigma_0^p=\Pi_0^p=\text{P}$，$\Sigma_1^p=\text{NP}$，$\Pi_1^p=\text{coNP}$。
    - $\Sigma_i^p\sube\Sigma_{i+1}^p$，$\Pi_i^p\sube\Pi_{i+1}^p$，$\Sigma_i^p\sube\Pi_{i+1}^p\sube\Sigma_{i+2}^p$。
    - $\text{PH}=\bigcup_k\Sigma_k^p=\bigcup_k\Pi_k^p$。
    - $\Sigma_{i+1}^p=\text{NP}^{\Sigma_i^p}$，$\Pi_{i+1}^p=\text{coNP}^{\Pi_i^p}$。
    - $\text{PH}\sube\text{PSPACE}$：枚举。
- **层次塌缩**：
    - 如果 $\Sigma_i^p=\Sigma_{i+1}^p$，那么 $\text{PH}=\Sigma_i^p=\Pi_i^p$。
    - 如果 $\text{P}=\text{NP}$，那么 $\text{PH}=\text{P}$；
    - 如果 $\text{NP}=\text{coNP}$，那么 $\text{PH}=\text{NP}$。

## 10. 相对化

如果一个证明在引入任意 oracle $A$ 的情况下都成立，那么这个证明是相对化的。

- 停机问题、层次定理、Savitch 定理、Immerman–Szelepcsényi 定理都是相对化的。
- 任意相对化的证明都无法解决 $\text{P}=\text{NP}$。
    - 构造 $A$ 使得 $\text{P}^A=\text{NP}^A$：令 $A=\text{TQBF}$，那么有 $\text{NP}^{\text{TQBF}}\sube\text{NPSPACE}$，且 $\text{PSPACE}\sube\text{P}^{\text{TQBF}}$。
    - 构造 $B$ 使得 $\text{P}^B\ne\text{NP}^B$：
        - 根据 $B$ 构造另一语言 $L=\{1^k:\exists x\in B,|x|=k\}$。
        - 那么 $L\in\text{NP}^B$，只需要枚举可能的 $x$。
        - 枚举所有多项式时间复杂度的 oracle TM $M_1,\dots$。枚举 $i=1,\dots$，令 $X$ 为 $B$ 的补集：
        - 选择足够大的 $n$ 使得所有长度为 $n$ 的字符串都未确定结果，模拟 $M_i(1^n)$；
        - 对于每次 $M_i$ 调用的 oracle 查询 $x$，我们都拒绝并确定 $x\in X$；
        - 如果最终 $M_i$ 接受，则将所有长度为 $n$ 的字符串放入 $X$ 中；
        - 如果最终 $M_i$ 拒绝，则将所有长度为 $n$ 的未确定字符串放入 $B$ 中；
        - 故 $M_i$ 正确不能判定 $1^n$，$L\notin\text{P}^B$。

## 11. 概率复杂性类

- 概率 TM：只读输入带，只读随机带，工作带；
- $\text{BPP}$：存在多项式时间概率 TM $M$，使得
    - 若 $x\in L$，则 $\Pr[M\text{ accepts }x]\ge 2/3$；
    - 若 $x\notin L$，则 $\Pr[M\text{ rejects }x]\ge 2/3$；
- $\text{RP}$：存在 $M$，使得一定能拒绝不在 $L$ 中的 $x$：
    - 若 $x\in L$，则 $\Pr[M\text{ accepts }x]\ge 1/2$；
    - 若 $x\notin L$，则 $\Pr[M\text{ rejects }x]=1$；
- $\text{coRP}$：存在 $M$，使得一定能接受在 $L$ 中的 $x$：
    - 若 $x\in L$，则 $\Pr[M\text{ accepts }x]=1$；
    - 若 $x\notin L$，则 $\Pr[M\text{ rejects }x]\ge 1/2$；
- $\text{ZPP}$：存在 $M$，使得一定能正确判断：
    - 若 $x\in L$，则 $\Pr[M\text{ accepts }x]=1$；
    - 若 $x\notin L$，则 $\Pr[M\text{ rejects }x]=1$；
- **复杂度类关系**：
    - $\text{ZPP}=\text{RP}\cap\text{coRP}$：同时运行 $\text{RP}$ 算法和 $\text{coRP}$ 算法，期望运行多项式时间。
    - $\text{P}\subseteq\text{ZPP}\subseteq\text{RP}\subseteq\text{BPP}$。
    - $\text{RP}\sube\text{NP}$：枚举所有使用到的随机位结果，如果 $x\in L$ 一定会找到接受的结果，否则不可能接受。
    - $\text{BPP}\sube\Sigma_2^p\cap\Pi_2^p\sube\text{PH}$：令 $L\in\text{BPP}$，则存在 $M(x,y)$，其中 $|y|=m$ 为随机位，满足
        - 若 $x\in L$，则 $\Pr_y[M\text{ accept }x]\ge 1-1/2m$；
        - 若 $x\notin L$，则 $\Pr_y[M\text{ accept }x]\le 1/2m$。
    - **引理**：$x\in L$ 当且仅当 $\exists y_{1\dots m}\in\{0,1\}^m\forall z\in\{0,1\}^m\bigvee_{i=1}^m(M(x,y_i\oplus z)\text{ accepts})$。
        - 从左至右：对于固定的 $z$，所有 $y_i\oplus z$ 都拒绝的概率 $\le 1/(2m)^m$，由 Union Bound 得到存在这样的 $z$ 的概率不超过 $1/m^m<1$，即一定有一组 $y_{1\dots m}$ 不存在这样的 $z$；
        - 从右至左：假设满足有边，且 $x\notin L$，则对于任意 $y_i$，要让 $y_i\oplus z$ 接受的 $z$ 的数量最多是 $2^m/2m$，所以存在 $y_i\oplus z$ 接受的 $z$ 不超过 $2^m/2$ 个，那么一定有 $z$ 使得所有 $y_i\oplus z$ 不接受，这并不满足右半部分的条件。
    - 这就说明了 $\text{BPP}\sube\Sigma_2^p$，由于 $\text{coBPP}=\text{BPP}$，我们也有 $\text{BPP}\sube\Pi_2^p$。

## 12. 随机素性测试

- Fermat 小定理：若 $p$ 是素数，则 $a^{p-1}\equiv 1\pmod p$。
- Carmichael 数：若 $p$ 是合数且对于所有 $(a,p)=1$ 的 $a$ 都有 $a^{p-1}\equiv1\pmod p$，那么 $p$ 是 Carmichael 数。
- 引理：设 $p$ 是奇素数，$k$ 为偶数，若 $a^k\equiv 1\pmod p$，则 $a^{k/2}\equiv \pm1\pmod p$。
- **Miller–Rabin 算法**：
    - 令 $k\gets N-1$，当 $2\mid k$ 时不断重复：
        - 计算 $a^k\bmod N$；
        - 如果结果是 $N-1$，接受；
        - 否则如果结果不是 $1$，拒绝；
    - 接受。
    - 如果 $N$ 是奇素数，必然会在某次降次后得到 $-1$ 或者降至奇数；
    - 如果 $N$ 是合数，则至少以 $1/2$ 概率拒绝。

## 13. 交互式证明

无限强大计算能力的 Prover P 和 Verifier V 进行交互，要求交互轮数与信息长度为多项式，V 提问，P 回答，V 最终决定是否接受。

- $\text{dIP}$：V 为多项式时间 TM。
    - $\text{dIP}=\text{NP}$：若 $x\in L$，则 $\exists P,\langle V,P\rangle(x)=1$。
- $\text{IP}$：V 为多项式时间随机 TM。
    - 若 $x\in L$，则 $\exists P,\Pr[V\text{ accepts in }(P,V)(x)]\ge 2/3$；
    - 若 $x\notin L$，则 $\forall P^*,\Pr[V\text{ accepts in }(P^*,V)(x)]\le 1/3$。
    - V 的随机位不对 P 公开。
    - $\text{NP}\sube\text{IP}$。
    - $\text{GNI}\in\text{IP}$：图非同构问题。
        - V 随机选取一张图，随机打乱编号，要求 P 判断其属于哪一张图；
        - 通过多项式次交互可将错误率缩减至指数小。
    - $\text{coNP}\sube\text{IP}$：$\#\text{SAT}\in\text{IP}$。
        - 算术化：$\lnot \phi\to 1-p_\phi$，$\phi\land\psi\to p_\phi\cdot p_{\psi}$，$\phi\lor\psi\to1-(1-p_{\phi})(1-p_\psi)$，取质数 $q>2^n$，在 $\bmod q$ 意义下运算。
        - P 声称 $k=\sum_{x_1,\dots,x_n\in\{0,1\}}p_{\phi}(x_1,\dots,x_n)$；
        - P 发送字符串 $s(z)=k_z=\sum_{x_2,\dots,x_n\in\{0,1\}}p_{\phi}(z,x_2,\dots,x_n)$；
        - V 验证 $s(0)+s(1)=k$；
        - V 随机选取 $a\in\text{GF}(q)$，递归验证 $s(a)$。
        - 若 P 作弊，则至少有 $1-\text{poly}(n)/2^n$ 的概率被发现。
    - $\text{IP}=\text{PSPACE}$：$\text{TQBF}\in\text{IP}$。
        - 算术化：$\exists x\phi\to\sum_{x\in\{0,1\}}p_\phi(x,\dots)$，$\forall x\phi\to\prod_{x\in\{0,1\}}p_\phi(x,\dots)$。
        - 避免次数爆炸：$Rx_i\phi(x_1,\dots,x_i,\dots,x_n)\to(1-x_i)\cdot p_\phi(x_1,\dots,x_{i-1},0,x_{i+1},\dots,x_n)+x_i\cdot p_\phi(x_1,\dots,x_{i-1},1,x_{i+1},\dots,x_n)$，将所有 $x_i^k$ 替换为 $x_i$。
        - 将 TQBF 化作 $\forall x_1Rx_1\exists x_2Rx_1Rx_2\dots$。
        - P 声称 $k=p_\phi$，其中 $\phi=(Ox_1)\phi'(x_1)$，$O\in\{\exists,\forall,R\}$；
        - P 发送字符串 $s(x_1)=p_{\phi'}(x_1)$；
        - 若 $O=\exists$，V 检查 $s(0)+s(1)=k$；
        - 若 $O=\forall$，V 检查 $s(0)\cdot s(1)=k$；
        - 若 $O=R$，V 检查 $(1-a_1)s(0)+a_1s(1)=k$，其中 $a_1$ 是已经在外层被量词 $Q_1x_1$ 赋值的 $x_1$（取最后一次赋值）；
        - 若通过，则 V 随机选取 $a\in\text{GF}(q)$，递归验证 $p_{\phi'}(a)$。
        - 若 P 作弊，则至少有 $1-\text{poly}(n)/2^n$ 的概率被发现。
- **Arthur–Merlin 游戏**：Arthur 的随机数对 Merlin 公开。
    - $\text{IP}=\text{Arthur–Merlin}$：在 TQBF 协议中事实上只使用了公共随机数，所以 $\text{PSPACE}\sube\text{Arthur–Merlin}\sube\text{IP}=\text{PSPACE}$。

## 14. 决策树模型

- 决策树：二叉树，每个结点查询 $x_i$ 并依此递归至某一子树，叶子结点输出函数值 $f(x)$。
- **决策树复杂度** $D(f)$：最坏情况下的最少查询次数，即深度的最小值。
- 0/1-证书：为了证明 $f(x)=0/1$，需要的最少信息。即定义 $x|_S$ 表示取出 $x$ 在 $S$ 中的位，则 $f(x)=0\iff x|_S=x_0$ 是一个 0-证书。
- **证书复杂度** $C(f)$：最小的整数 $k$，使得所有输入均有一个 $\le k$ 大小的证书。
- $C(f)\le D(f)\le C(f)^2$：
    - 决策树的一条根到叶子的路径是一个证书。
    - 如果 $f$ 不是常数，则存在 0-证书 $S$；
    - 查询所有 $S$ 内的变量；
    - 所有 1-证书必须与 $S$ 相交，否则存在 $x$ 同时满足 0-证书与 1-证书；
    - 故查询后，所有还符合条件的 1-证书的位数至少减去 1；
    - 故最多查询 $C(f)$ 次，每次取一 0-证书查询，查询总次数 $\le C(f)^2$。

## 15. 电路复杂度类

- **电路族**：$\{C_n\}$，其中 $C_n$ 处理长为 $n$ 的输入；
- $\text{SIZE}(T(n))$：大小不超过 $T(n)$ 的电路族可判定的语言；
- $\text{P/poly}$：多项式大小电路族可判定的语言类。
    - $\text{P}\sube\text{P/poly}$：计算历史；
    - 甚至可判定不可判定语言：将 $n$ 相关信息编码入电路族；
    - 一致性：一致性要求存在对数空间图灵机，对输入 $n$ 输出 $C_n$；
    - 对数空间一致、多项式大小的电路族可判定的语言类恰好 $=\text{P}$。
- **带建议 Advice 的 TM**：多一条只读建议带，内容依赖于输入长度 $|x|$。
    - $\text{TIME}(T(n))/f(n)$：建议长度为 $O(f(n))$，运行时间为 $T(n)$；
    - $\text{P/poly}=\bigcup_k\text{TIME}(n^k)/n^k$。
- **Karp–Lipton 定理**：如果 SAT 有多项式大小电路，则 $\text{PH}\sube\Sigma_2$。
    - 对于 $L\in\Pi_2$，可表述为 $L=\{x:\forall y\exists z\,(x,y,z)\in R\}$，其中 $R\in\text{P}$。
    - $\exists z\,(x,y,z)\in R$ 是 $\text{NP}$ 问题，可以用 SAT 解决。
    - 若 $\text{SAT}\in\text{P/poly}$，则 $L$ 可重写为 $\{x:\exists C\forall y,\text{use }C\text{ to find }z\text{ for }\exists z\,(x,y,z)\in R,\text{ accept iff }(x,y,z)\in R\}$，判定部分是 $\text{P}$ 的，故 $L\in\Sigma_2$。
    - 普遍认为 $\text{NP}\subsetneq\text{P/poly}$。
- **Shannon 计数论证**：在至少 $1-o(1)$ 的概率下，随机函数 $f:\{0,1\}^n\to\{0,1\}$ 需要一个大小至少为 $\Omega(2^n/n)$ 的电路判定。
    - 大小为 $s$ 的 $n$ 输入电路只有 $\le(3(s+n)^2)^s$ 个；
    - $C(n,c2^n/n)\le(c'2^{2n}/n^2)^{c2^n/n}=O(1/n^2)2^{2c\cdot2^{n}}=o(1)2^{2^n}$。
- 电路大小层次定理：若 $T(n)\log T(n)=o(T'(n))$，则 $\text{SIZE}(T(n))\subsetneq\text{SIZE}(T'(n))$。
- **复杂度类关系**：
    - $\text{EXPSPACE}\not\subset\text{P/poly}$：对于每个 $n$，找到 $f_n$ 为第一个需要 $\Omega(2^n/n)$ 规模的函数，对应电路族不属于 $\text{P/poly}$；
    - $\text{EXP}^{\Sigma_2}\not\subset\text{P/poly}$：通过二分寻找上述 $f_n$，判断 $g$ 可以通过 $\le s$ 的电路计算是 $\Sigma_2$ 语句 $\exists C\forall x,(\text{size}(C)\le s)\land (C(x)=g(x))$。
    - $\text{NEXP}^{\text{NP}}\not\subset\text{P/poly}$：如果 $\text{NEXP}^{\text{NP}}\subseteq\text{P/poly}$，则 $\text{PH}=\Sigma_2$，所以 $\text{P}^{\Sigma_2}=\text{NP}^{\text{NP}}$；由填充论证有 $\text{EXP}^{\Sigma_2}=\text{NEXP}^{\text{NP}}$，与已知结论矛盾。
- $\text{NC}$：$\text{NC}^k$ 表示 $O(\log^kn)$ 深度，多项式大小，对数空间一致的电路，$\text{NC}=\bigcup_k\text{NC}^k$。
    - $\text{NC}^1$ 等价于多项式大小的均匀布尔公式族。
    - $\text{NC}\sube\text{P}$：$\text{P}$ 等于多项式大小均匀电路类；
    - $\text{NC}^1\sube\text{L}$：电路求值只需要深度大小空间；
    - $\text{NL}\sube\text{NC}^2$：布尔矩阵乘法在 $\text{NC}^1$ 中，$\text{PATH}$ 只需要做矩阵快速幂。
- P-complete CIRCUIT-VALUE：给定电路和输入，判定是否输出 1。
- $\text{AC}$：$\text{AC}^k$ 表示 $O(\log^kn)$ 深度，多项式大小，对数空间一致的无界扇入电路，$\text{AC}=\bigcup_k\text{AC}^k$。
    - 二进制加法器在 $\text{AC}^0$ 中；
    - 奇偶性判断器 Parity 不在 $\text{AC}^0$ 中：多项式方法。
        - 任何 $\text{AC}^0$ 电路可以在 $\mathbb Z_3$ 上被低次多项式 $99\%$ 概率近似；
        - $x_1\lor\dots\lor x_n$ 用随机变量 $a_1,\dots,a_n$ 近似为 $a_1x_1+\dots+a_nx_n$，若结果为 $0$ 必定正确，否则有 $1/3$ 概率错误；
        - 用 $\Theta(\log s)$ 组随机向量 $A$，可控制错误率至 $\le 1/100s$。
        - 用 $(\log s)^{O(d)}$ 次多项式做到错误率 $<1\%$。
    - Parity 不可以在 $\mathbb Z_3$ 上被低次多项式近似；
        - 转化为 $x_1\cdot x_2\cdot\dots\cdot x_n$；
        - 不存在次数为 $c\cdot\sqrt n$ 的多项式能够 $99\%$ 近似 $n$ 元乘积函数；
        - 假设存在这样的 $Q(y)$ 在集合 $S\sube\{-1,1\}^n,|S|\ge 0.99\cdot 2^n$ 上有 $Q(y)-y_1\cdots y_n=0$；
        - 对于任意高次多项式，由于 $y_i^2=1$，我们可以将其转化为 $y_1\cdots y_n$ 乘上其补集；
        - 那么在 $S$ 上，高次多项式等价于其补集乘上 $Q(y)$；
        - 任意定义在 $S$ 上的函数都可以唯一地表示成多线性多项式，也就可以表示成 $\le n/2+D$ 次多项式，其中 $D=\text{degree}(Q)$；
        - 计数论证：$S$ 上函数有 $\ge 2^{0.99\cdot2^n}$ 个；
        - 单项式个数为 $\sum_{i\le K}\binom ni$ 个，故多项式次数为 $3^{\sum_{i\le K}\binom ni}$ 个，取 $K=n/2+c\sqrt n$，那么多项式次数为 $3^{2^{n-1}+\delta\cdot2^n}$；
        - 当 $\delta$ 足够小时 $2^{n-1}\log 3<0.99\cdot 2^n$。
- $\text{ACC}$：$\text{AC}^0[p]$ 表示 $\text{AC}^0$ 加上 $\bmod p$ 计数门，返回是否是 $p$ 的倍数，$\text{ACC}^0=\bigcup_p\text{AC}^0[p]$。
    - Parity $\notin\text{AC}^0[3]$，若 $p,q$ 为不同质数，则 $\text{MOD}_q\notin\text{AC}^0[p]$；
    - $\text{NEXP}\not\subset\text{ACC}^0$。

## 16. APSP 猜想

- 猜想：APSP 全源最短路不存在 $O(n^{3-\delta})$ 算法；
- **APSP 与距离乘积等价**：
    - 距离乘积：$(\min,+)$ 矩阵乘法；
    - 距离乘积 → APSP：构造双层图；
    - APSP → 距离乘积：矩阵快速幂；
- **距离乘积、距离乘积比较、距离乘积验证与负三角形等价**：
    - 距离乘积比较：确认 $(A\times B)_{i,j}\le C_{i,j}$，可通过整体二分解决距离乘积；
    - 距离乘积验证：确认 $A\times B=C$；
    - 负三角形 → 距离乘积：显然；
    - 距离乘积比较 → 负三角形：假设负三角形可在 $T(n)=O(n^{3-\delta})$ 内判定；
        - 构造三分图 $I,J,K$，每一部分 $n$ 个结点，连边 $I\to K\to J$，边权为 $A_{i,k},B_{k,j},-C_{i,j}$；
        - 需要所有边 $(i,j)$ 都在负三角形中；
        - 每次找一个负三角形，然后删去其中的边 $(i,j)$，时间复杂度 $O(n^2T(n))$；
        - 分块，将每一部分分为 $n/s$ 个大小为 $s$ 的块，每组 $I_x,J_y,K_z$ 间运行上述算法；
        - 时间复杂度 $O(((n/s)^3+n^2)T(s))$，取 $s=n^{1/3}$ 有时间复杂度 $O(n^{3-\delta/3})$。
    - 负三角形 → 距离乘积验证：给定邻接矩阵 $A$，负三角形不存在当且仅当

$$\begin{bmatrix}-A&\infty\\\infty&\infty\end{bmatrix}=\begin{bmatrix}A^\top&I\\\infty&\infty\end{bmatrix}\times\begin{bmatrix}A^\top&\infty\\-A&\infty\end{bmatrix}.$$

        - 负三角形存在即为 $\min_k(A_{k,i}+A_{j,k})<-A_{i,j}$；
        - 即 $\min\bigl(\min_k(A_{k,i}+A_{j,k}),-A_{i,j}\bigr)\ne -A_{i,j}$；
- **最小权环、替代路径、次短路径的 APSP 复杂性**：
    - 替代路径：有向图删边最短路；
    - 负三角形 → 最小权环：将所有边权增加 $8M$，则原先的负权三角形 $<24M$，任何四元环 $\ge 24M$。
    - 替代路径 → APSP：线段树。
    - 最小权三角形 → 次短路径：构造三分图 $I,J,K$，再拉一条路径对应 $K$，建边 $(s,k_1,0),(k_1,(k+1)_1,0),(n_1,t,0)$，以及 $(k_0,k_1,4kM)$，$(k_1,i,w(k,i)+4(n-k)M)$，$(i,j,w(i,j))$，$(j,k_0,w(j,k))$。

## 17. OV 与 SETH 复杂性

- **正交向量 OV**：给定 $d$ 维向量集合 $S$，求其中是否存在正交向量 $u\cdot v=0$，其中 $d=O(\log n)$；
    - OV 猜想：OV 不存在 $O(n^{2-\delta})$ 的算法。
- 指数时间假说 ETH：存在常数 $\delta$ 使得 3-SAT 需要 $2^{\delta n}$ 的时间复杂度。Schöning 算法证伪：
    - 随机指定初值 $x$；
    - 重复至多 $n$ 次，每次判断是否满足条件，若不满足则任意取一个不满足条件的子句，随机翻转其中一个变量。
    - 概率分析：相差 $k$ 位的概率为 $\binom nk2^{-n}$，正确修正的概率为 $3^{-k}$，即正确率为 $(2/3)^n$，重复执行 $O(1.5^n)$ 次即可。
- **强指数时间假说 SETH**：对任意常数 $\epsilon>0$，存在 $k$ 使得 $k$-SAT 不能在 $2^{(1-\epsilon)n}\cdot\text{poly}(m)$ 的时间内解决。
    - SETH → OV：给定 $k$-CNF，将变量集划分为两半，分别枚举每一部分的变量，构造出大小为 $2^{n/2}$ 的 $m+2$ 维向量集合，其中前两维为 $01/10$ 用于分组，后 $m$ 维为每一子句满足情况，满足则为 $0$。那么如果 OV 能 $O(n^{2-\delta})$ 完成，则 $k$-SAT 可 $O(2^{(1-\delta/2)n})$ 时间解决。
    - **图的直径问题**：
        - 2/3 近似算法：
            - 流程：
                - 以 $1/\sqrt n$ 概率独立选择顶点，记作集合 $S$；
                - 从 $S$ 的每个顶点运行 BFS，得到 $d(x,S)$；
                - 找到 $w=\argmax d(u,S)$；
                - 定义 $T=\{v:d(w,v)<d(v,S)\}$，即距离 $w$ 比距离 $S$ 更近的点，$T$ 的大小高概率为 $O(\sqrt n)$；
                - 从 $S\cup T$ 的点出发运行 BFS，返回最远的距离 $D'$；
            - 近似分析：
                - 假设真实直径为 $d(a,b)=3h$；
                - 如果存在 $u\in S$ 使得 $d(u,a)\ge 2h$ 或 $d(u,b)\ge 2h$，直接满足；
                - 剩余情况下 $h\le d(u,a)\le 2h$，那么 $d(w,S)\ge h$。考虑 $w\to b$ 最短路径上 $d(w,y)=h$ 的点 $y$，有 $y\in T$。由于 $d(y,b)\le h$，故 $d(y,a)\ge 2h$。
        - 近似的 OV 难解下界：
            - OV → 区分直径 2/3：判断是否有分别来自 $A,B$ 集合的向量正交，构造三层各 $n,d,n$ 个结点，按照向量连边，再加上一条特殊边沟通一三层，如果存在 $u\cdot v=0$，则必须进过特殊边，距离为 $3$，否则距离为 $2$。
            - 故若能够在 $O(m^{2-\delta})$ 的时间复杂度内做到优于 2/3 近似，则 OV 猜想错误。
    - **动态单源可达性 #SSR 的难解性**：给定图与源点，动态加边删边并询问 $s$ 的可达点数。
        - OV → #SSR：固定 $[d]\to B$ 的边，逐个加上 $A\to[d]$ 的边，查看可达点数再撤回；

## 18. Were-you-last 游戏

$m$ 名玩家独立地进入房间，房间中有若干格子。每个玩家可打开至多 $t$ 个格子，读/写相应格子并放/取石子。玩家离开时需回答自己是否是最后一个。

- 平凡上界：$t=\Theta(\log m)$，直接使用计数器；
- 块表示法：$t=\Theta(\log\log m)$，维护 $m$ 的二进制表示，将其中每一段连续段压缩为一位，再维护段数，可以直接跳转至末尾块内存位。
- 下界：当 $t\le 0.4\log\log m$ 时，玩家一定无法获胜。
    - 向日葵：集合族 $S_1,\dots,S_p$ 称为向日葵当且仅当任意 $S_i\cap S_j$ 均相同；
    - 向日葵引理：对于集合族 $S_1,\dots,S_m$ 且 $|S_i|\le l$，如果 $m>(p-1)^{l+1}l!$，那么其中必定存在一个大小为 $p$ 的子集为向日葵。
        - 对于 $l$ 归纳，$l=1$ 显然。
        - 找到最大的子集 $A_1,\dots,A_t$ 互不相交，如果 $t\ge p$ 那么这就是合法向日葵；
        - 当 $t<p$ 时，令 $B=A_1\cup\dots\cup A_t$，则 $|B|\le(p-1)l$，且 $B$ 与任意 $S_i$ 相交，那么一定存在 $B$ 中元素 $x$ 被包含在 $>\frac{(p-1)^{l+1}l!}{(p-1)l}=(p-1)^l(l-1)!$ 个 $S_i$ 中。
        - 从这些集合中删去 $x$，可得到一个向日葵，再加入 $x$ 即可。
    - 令 $S_i$ 为第 $i$ 个人查看的位，则 $|S_i|\le l=2^t-1\le(\log m)^{0.4}$。
    - 找到一个向日葵 $S_1,\dots,S_p$，先让其余人进入，再让这 $p$ 人进入，只有这个向日葵的中心区域是对这 $p$ 人有用的，可能的状态只有 $\le 2^l$ 个。
    - $(2^l)^{l+1}l^l=2^{l^2+l+l\log l}<m$，故我们可以找到 $p>2^l$ 的向日葵，导致存在两个人进入时状态相同。

## 19. 催化计算

- 催化 TM：多一条长度为 $O(c(n))$ 的辅助带，其中内容在计算完毕后必须恢复原状；
- **催化类** $\text{CSPACE}[s(n),c(n)]$：工作带空间为 $O(s(n))$，辅助带空间为 $O(c(n))$ 的催化 TM 类；
- $\text{CL}=\text{CSPACE}[\log n,\text{poly}(n)]$。
- 直线程序：无分支、循环、跳转的程序，等价于电路；
    - 任意 $t(n)$ 时间的 TM 等价于长度为 $O(t(n)^2)$ 的直线程序；
    - 可逆程序：每一步都是可逆的；
    - 透明计算：将 $f(x)$ 的值加到寄存器 $R_i$ 上，其余寄存器可以改变；
    - 干净计算：将 $f(x)$ 的值加到寄存器 $R_i$ 上，其余寄存器必须恢复。
        - 任何代数公式 $f$ 均可用 $3$ 个寄存器干净计算。
- **复杂度类关系**：
    - $\text{NC}^1\sube\text{L}\sube\text{NL}\sube\text{AC}^1\sube\text{ACC}^1\sube\text{TC}^1\sube\text{CL}$；
    - $\text{TC}^1$：$\text{AC}^1$ + Majority 门；
    - $\text{CL}\sube\text{P}$ 是开放问题；
    - $\text{CL}\sube\text{ZPP}$：
        - 不同初始辅助带内容 $a,a'$ 不能进入相同格局，否则不可能恢复原状。
        - 总格局数为 $O(2^{s(n)+c(n)})$；
        - 记 $T(x,a)$ 为辅助带初始为 $a$ 时的运行时间，那么 $\sum_aT(x,a)=O(2^{s(n)+c(n)})$，故 $\mathbb E[T(x,a)]=O(2^{s(n)})=\text{poly}(n)$，随机选取辅助带内容即可。
