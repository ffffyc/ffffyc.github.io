"""给有课件但缺「涉及内容」的三门课补上主题（依据课件标题整理）。"""

from __future__ import annotations

from pathlib import Path

import yaml

NOTES = Path(__file__).resolve().parent.parent / "content" / "notes"

TOPICS: dict[str, dict[int, str]] = {
    "sys-intro": {
        1: "课程总览与核心原则：计算机系统的抽象层次、性能度量与 Amdahl 定律",
        2: "处理器与汇编代码：指令集、寄存器、函数调用与栈帧",
        3: "存储层次：缓存、局部性与存储性能",
        4: "进程与线程：进程模型、上下文切换、线程与并发",
        5: "实用工具：Shell、版本控制、调试与性能剖析",
        6: "并发与同步（一）：竞态条件、互斥锁与条件变量",
        7: "并发与同步（二）：信号量、死锁与并发编程模式",
        8: "虚拟内存与内存管理：地址转换、分页、malloc 与碎片",
        9: "I/O 设备：总线、中断、DMA 与磁盘",
        10: "文件系统与保护：inode、目录、权限与访问控制",
        11: "计算机网络与 RPC：多路复用、寻址、可靠传输、分层与远程过程调用",
        12: "数据库与事务：关系模型、SQL、ACID 与隔离级别",
        13: "分布式系统：RPC、分布式文件系统与故障处理",
        14: "系统设计原则：抽象、模块化、权衡与可扩展性",
    },
    "theory-of-computation": {
        1: "引言与数理逻辑：课程概览、命题逻辑与可判定性",
        2: "有限自动机：DFA/NFA、正则表达式与泵引理",
        3: "上下文无关文法：CFG、下推自动机与语法分析",
        4: "图灵机与停机问题：图灵机模型、丘奇-图灵论题、不可判定性",
        5: "图灵机进阶：非确定性、枚举器与归约",
        6: "空间复杂性：Savitch 定理、PSPACE 与 NL",
        7: "对角化与交替：时间层次定理与多项式层次",
        8: "随机计算与素性测试：BPP、RP 与 Miller–Rabin",
        9: "交互式证明与决策树：IP、AM 与决策树下界",
        10: "电路复杂性与多项式方法：电路下界与多项式方法",
        11: "计数复杂性：#P 与 Toda 定理",
        12: "P 内困难性：细粒度复杂性与 SETH",
        13: "单元探测模型：cell-probe 下界与数据结构",
        14: "催化计算与时间-空间复杂性",
    },
    "introduction-to-cs": {
        1: "AI 的能力与局限：从理论视角看机器学习的边界",
        2: "图算法：BFS/DFS、最短路与最小生成树",
        3: "计算机体系结构：过去与未来",
        5: "Grothendieck 拓扑：局部视角到整体一致",
        6: "量子计算：算法与纠错",
    },
}

for subject, topics in TOPICS.items():
    folder = NOTES / subject
    lines = ["# 每周/每讲涉及的课程内容，键是周次或讲次；留空则不显示"]
    for n in sorted(topics):
        text = topics[n].replace("'", "''")
        lines.append(f"{n}: '{text}'")
    (folder / "_syllabus.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    meta_path = folder / "_subject.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    meta.pop("show_text", None)  # 默认 true
    meta_path.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(subject, "写入", len(topics), "行，show_text 打开")
