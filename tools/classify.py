"""文章归类规则：把洛谷的新专栏分类与旧博客自定义标签统一成站内栏目。"""

import re

TRAVEL_WORDS = ["游记", "游寄", "邮寄", "寄记", "谢幕", "观光记", "回忆录", "简记", "问题记"]
TOOL_WORDS = ["黑盒", "创造数据"]
MISC_WORDS = ["闲话", "杂谈", "随想", "Phigros", "月考", "主页", "一周年", "问卷", "语录", "期末考"]
DIARY_WORDS = ["记录", "日志", "学习笔记", "反演", "板子", "摘抄", "Lucas", "模拟赛"]
COURSE_WORDS = ["信息数学", "计算理论", "文化课"]

CONTEST = re.compile(
    r"(联合省选|省选联考|THUWC|THUSC|THUPC|NOIWC|GDKOI|GDOI|NOIP|NOI|CSP-S|CSP-J|CSP|"
    r"CTT|CTS|APIO|WC|ZJOI|HNOI|ICPC|CCPC)\s*(\d{2,4})?"
)
ALIAS = {"NOIWC": "WC"}


def contest_tags(title: str) -> list[str]:
    """取出标题里全部比赛名与年份；只有一个年份时，把它补给没写年份的比赛。"""
    found: list[tuple[str, str]] = []
    for m in CONTEST.finditer(title):
        name = ALIAS.get(m.group(1), m.group(1))
        found.append((name, m.group(2) or ""))

    years = re.findall(r"(20\d{2})", title)
    only_year = years[0] if len(set(years)) == 1 else ""

    tags: list[str] = []
    for name, year in found:
        year = year or only_year
        tag = f"{name} {year}" if year else name
        if tag not in tags:
            tags.append(tag)
    return tags


def classify(title: str, old_tag: str, new_cat: str) -> str:
    """old_tag 为翻新前的自定义标签，new_cat 为洛谷现在的专栏分类编号。"""
    old = old_tag or ""
    cat = str(new_cat)

    if any(w in title for w in COURSE_WORDS):
        return "文化课"
    if title.lstrip().startswith("题解"):
        return "题解"
    if "tricks" in title:
        return "解题思路"
    if any(w in title for w in TRAVEL_WORDS) or cat == "5":
        return "游记"
    if any(w in title for w in TOOL_WORDS):
        return "工具"
    if any(w in title for w in MISC_WORDS):
        return "杂项"
    if any(w in title for w in DIARY_WORDS):
        return "个人记录"
    if old in ("学习笔记", "日报"):
        return "算法·理论"
    if old == "杂项":
        return "杂项"
    if old == "游记":
        return "游记"
    if old == "题解" or cat == "2":
        return "题解"
    if cat in ("4", "6"):
        return "算法·理论"
    if cat == "1":
        return "解题思路"
    return "杂项"
