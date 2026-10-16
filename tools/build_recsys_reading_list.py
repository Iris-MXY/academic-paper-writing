from __future__ import annotations

import csv
import re
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "论文主题分类总表.csv"


GROUPS: OrderedDict[str, dict] = OrderedDict(
    [
        (
            "01 推荐系统与个性化",
            {
                "priority": "A",
                "why": "最直接对应推荐系统、排序、个性化与消费者选择。",
                "ids": [f"DCB{i:03d}" for i in range(31, 41)],
            },
        ),
        (
            "02 搜索、排序与信息获取",
            {
                "priority": "A",
                "why": "搜索引擎、排序、考虑集和产品发现的算法与实证问题。",
                "ids": [f"DCB{i:03d}" for i in range(1, 11)],
            },
        ),
        (
            "03 在线评价、口碑与文本挖掘",
            {
                "priority": "A",
                "why": "用户生成内容、评论、评分、社会学习和文本分析的经典数据挖掘场景。",
                "ids": [f"DCB{i:03d}" for i in range(11, 31)]
                + ["DCB085", "DCB058", "DCB077", "DCB020"],
            },
        ),
        (
            "04 个性化、定价、广告与用户行为",
            {
                "priority": "B",
                "why": "个性化推荐、定向广告、选择架构、定价和用户行为建模的交叉场景。",
                "ids": [f"DCB{i:03d}" for i in range(41, 51)]
                + [f"DCB{i:03d}" for i in range(61, 71)]
                + ["DCB082", "DCB083", "DCB084", "DCB086", "DCB087", "DCB088", "DCB089", "DCB090"],
            },
        ),
        (
            "05 生成式 AI 与算法决策（应用型）",
            {
                "priority": "A",
                "why": "把 LLM/GenAI 用于推荐、广告、搜索、评价和行为研究，适合做交叉创新。",
                "ids": [f"DCB{i:03d}" for i in range(91, 101)],
            },
        ),
        (
            "06 因果、预测与决策支持",
            {
                "priority": "B",
                "why": "预测模型、因果实验、算法建议和人在回路决策，适合数据科学与应用算法交叉。",
                "ids": ["12", "21", "23", "25", "29", "30", "31", "38", "40", "47", "49", "50", "56", "58", "62", "64", "65", "66", "68", "70"],
                "folder": "AI人机协同相关主题文献1",
            },
        ),
        (
            "07 可信推荐、公平与隐私",
            {
                "priority": "B",
                "why": "隐私、公平、解释、安全和合规是推荐与数据挖掘最稳定的差异化方向。",
                "ids": [f"DCB{i:03d}" for i in range(51, 61)]
                + ["DCB093", "DCB098"],
                "extra": {
                    "AI人机协同相关主题文献1": ["22", "33", "42", "54", "55", "61", "69"],
                },
            },
        ),
        (
            "08 算法与数据挖掘基础",
            {
                "priority": "C",
                "why": "模型、强化学习、Agent、多模态、异常检测与图/文本数据结构基础。",
                "folder": "AI相关学术论文文献汇总2",
                "title_patterns": [
                    "multi-agent",
                    "multi ai agent",
                    "agentic ai",
                    "ai agents",
                    "an llm-lvlm",
                    "agile-a-novel-reinforcement-learning",
                    "agentic reinforcement learning",
                    "infrastructure for ai agents",
                    "governing ai agents",
                    "characterizing ai agents",
                    "economy of ai agents",
                    "multi-agent risks",
                    "can chatgpt forecast",
                    "large_language_models__foundation_models",
                    "lora",
                    "tnsorflow",
                    "internvl",
                    "video understanding",
                    "toward agentic ai",
                    "evaluating the robustness of multimodal agents",
                    "towards autonomous sustainability assessment",
                ],
            },
        ),
        (
            "09 平台、治理与数字化交叉",
            {
                "priority": "C",
                "why": "推荐和数据分析在组织、平台、治理与数字化转型中的管理交叉。",
                "ids": [f"DTF{i:03d}" for i in range(51, 61)],
                "extra": {
                    "129篇文献": ["2", "4", "17", "22", "23", "27", "31", "38", "56", "60", "63", "65", "68", "87", "97", "98", "99", "104", "109", "113"],
                },
            },
        ),
    ]
)


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def load_rows() -> list[dict]:
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def select_rows(rows: list[dict]) -> list[dict]:
    selected: list[dict] = []
    used: set[tuple[str, str, str]] = set()

    for group, config in GROUPS.items():
        candidates = rows
        if config.get("folder"):
            candidates = [
                row
                for row in candidates
                if row["来源资料夹"] == config["folder"]
            ]

        group_rows: list[dict] = []
        ids = {str(value) for value in config.get("ids", [])}
        if ids:
            group_rows.extend(
                row
                for row in candidates
                if row["来源编号"] in ids
            )

        patterns = config.get("title_patterns", [])
        if patterns:
            group_rows.extend(
                row
                for row in candidates
                if any(pattern in normalize(row["论文标题"]) for pattern in patterns)
            )

        for folder, extra_ids in config.get("extra", {}).items():
            extra_set = {str(value) for value in extra_ids}
            group_rows.extend(
                row
                for row in rows
                if row["来源资料夹"] == folder and row["来源编号"] in extra_set
            )

        for row in group_rows:
            key = (row["来源资料夹"], row["来源编号"], row["论文标题"])
            if key in used:
                continue
            used.add(key)
            selected.append(
                {
                    **row,
                    "清单分类": group,
                    "推荐级别": config["priority"],
                    "入选理由": config["why"],
                }
            )
    folder_order = {
        "数字环境下的消费者决策 100篇UTD24": 0,
        "AI人机协同相关主题文献1": 1,
        "AI相关学术论文文献汇总2": 2,
        "企业数字化转型 100篇UTD24": 3,
        "129篇文献": 4,
    }

    def row_key(row: dict) -> tuple:
        source_id = row["来源编号"]
        number = int(source_id) if source_id.isdigit() else 9999
        return (
            row["清单分类"],
            folder_order.get(row["来源资料夹"], 99),
            number,
            row["论文标题"],
        )

    return sorted(selected, key=row_key)


def write_csv(rows: list[dict]) -> None:
    fields = [
        "清单分类",
        "推荐级别",
        "统一主题",
        "来源资料夹",
        "来源主题",
        "来源编号",
        "论文标题",
        "入选理由",
        "相对路径",
    ]
    with (ROOT / "推荐系统与数据挖掘_相关论文.csv").open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            {field: row.get(field, "") for field in fields}
            for row in rows
        )


def write_markdown(rows: list[dict]) -> None:
    lines = [
        "# 推荐系统与数据挖掘相关论文",
        "",
        "这份清单面向“推荐系统/数据挖掘为主、AI 为工具或交叉变量”的选题路线。"
        "A 为核心阅读，B 为交叉拓展；完整路径见同目录 CSV。",
        "",
    ]

    for group in GROUPS:
        group_rows = [row for row in rows if row["清单分类"] == group]
        if not group_rows:
            continue
        config = GROUPS[group]
        lines.extend(
            [
                f"## {group}",
                "",
                f"- 推荐级别：{config['priority']}",
                f"- 入选理由：{config['why']}",
                f"- 论文数：{len(group_rows)}",
                "",
                "| 编号 | 论文 | 来源资料夹 |",
                "| --- | --- | --- |",
            ]
        )
        for row in group_rows:
            paper_id = row["来源编号"] or "-"
            lines.append(
                f"| {paper_id} | {row['论文标题']} | {row['来源资料夹']} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 使用建议",
            "",
            "1. 先读 01–07 组，建立推荐、搜索、用户行为和可信算法的基本盘。",
            "2. 08 组用于补 Agent、强化学习、多模态和数据结构基础，不必全部精读。",
            "3. 09 组适合把算法问题放回平台、组织和治理情境，形成交叉贡献。",
            "4. 选题时优先组合一个算法问题和一个业务情境，例如“因果排序 × 电商”“隐私推荐 × 平台治理”“LLM 评价摘要 × 消费者决策”。",
            "",
        ]
    )
    (ROOT / "推荐系统与数据挖掘_相关论文.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    rows = select_rows(load_rows())
    write_csv(rows)
    write_markdown(rows)
    print(f"Generated {len(rows)} related papers.")
    for group in GROUPS:
        print(group, sum(row["清单分类"] == group for row in rows))


if __name__ == "__main__":
    main()

