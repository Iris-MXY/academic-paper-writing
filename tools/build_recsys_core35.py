from __future__ import annotations

import csv
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "论文主题分类总表.csv"


GROUPS: OrderedDict[str, list[tuple[str, str, str]]] = OrderedDict(
    [
        (
            "01 综述与总论",
            [
                ("AI人机协同相关主题文献1", "12", "算法厌恶与采纳"),
                ("AI人机协同相关主题文献1", "21", "机器学习与行为科学"),
                ("AI人机协同相关主题文献1", "22", "算法公平与商业分析"),
                ("AI人机协同相关主题文献1", "23", "可解释 AI 与运营研究"),
            ],
        ),
        (
            "02 推荐系统与个性化",
            [
                ("数字环境下的消费者决策 100篇UTD24", "031", "推荐与消费者评价"),
                ("数字环境下的消费者决策 100篇UTD24", "033", "推荐环境中的选择"),
                ("数字环境下的消费者决策 100篇UTD24", "034", "推荐与支付意愿"),
                ("数字环境下的消费者决策 100篇UTD24", "035", "偏好学习与推荐"),
                ("数字环境下的消费者决策 100篇UTD24", "037", "推荐位竞争"),
                ("数字环境下的消费者决策 100篇UTD24", "038", "个性化排序与福利"),
                ("数字环境下的消费者决策 100篇UTD24", "039", "推荐与消费者搜索"),
            ],
        ),
        (
            "03 搜索、排序与信息设计",
            [
                ("数字环境下的消费者决策 100篇UTD24", "003", "搜索成本与考虑集"),
                ("数字环境下的消费者决策 100篇UTD24", "005", "有限搜索与在线需求"),
                ("数字环境下的消费者决策 100篇UTD24", "008", "产品排序"),
                ("数字环境下的消费者决策 100篇UTD24", "010", "搜索疲劳与终止"),
                ("数字环境下的消费者决策 100篇UTD24", "067", "广告信息与搜索排序"),
            ],
        ),
        (
            "04 评价、口碑与文本挖掘",
            [
                ("数字环境下的消费者决策 100篇UTD24", "012", "评论与销售"),
                ("数字环境下的消费者决策 100篇UTD24", "013", "评价自选择"),
                ("数字环境下的消费者决策 100篇UTD24", "015", "评分方差"),
                ("数字环境下的消费者决策 100篇UTD24", "018", "社会学习与误学习"),
                ("数字环境下的消费者决策 100篇UTD24", "020", "评价的信息机制"),
            ],
        ),
        (
            "05 因果推断、实验与强化学习",
            [
                ("AI人机协同相关主题文献1", "05", "强化学习与序贯决策"),
                ("AI人机协同相关主题文献1", "31", "离线强化学习"),
                ("AI人机协同相关主题文献1", "47", "预测调整与现场实验"),
                ("AI人机协同相关主题文献1", "49", "人类决策与机器预测"),
                ("数字环境下的消费者决策 100篇UTD24", "046", "因果机器学习应用"),
            ],
        ),
        (
            "06 可信推荐、隐私与公平",
            [
                ("AI人机协同相关主题文献1", "30", "隐私保护推荐"),
                ("数字环境下的消费者决策 100篇UTD24", "051", "隐私监管与广告"),
                ("数字环境下的消费者决策 100篇UTD24", "056", "移动轨迹隐私"),
                ("数字环境下的消费者决策 100篇UTD24", "057", "个性化隐私偏好"),
            ],
        ),
        (
            "07 LLM、生成式推荐与 Agent",
            [
                ("数字环境下的消费者决策 100篇UTD24", "092", "LLM 与偏好建模"),
                ("数字环境下的消费者决策 100篇UTD24", "094", "生成式广告"),
                ("数字环境下的消费者决策 100篇UTD24", "095", "LLM 与赞助搜索"),
                ("数字环境下的消费者决策 100篇UTD24", "099", "LLM 流量与电商"),
                ("数字环境下的消费者决策 100篇UTD24", "100", "生成式 AI 研究方法"),
            ],
        ),
    ]
)


def load_rows() -> list[dict]:
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build_rows(source_rows: list[dict]) -> list[dict]:
    def normalized_id(folder: str, paper_id: str) -> str:
        if folder == "数字环境下的消费者决策 100篇UTD24" and paper_id.isdigit():
            return f"DCB{int(paper_id):03d}"
        if folder == "AI人机协同相关主题文献1" and paper_id.isdigit():
            return str(int(paper_id))
        return paper_id

    index = {
        (row["来源资料夹"], normalized_id(row["来源资料夹"], row["来源编号"])): row
        for row in source_rows
    }
    output: list[dict] = []
    for module, items in GROUPS.items():
        for folder, paper_id, subtopic in items:
            row = index.get((folder, normalized_id(folder, paper_id)))
            if row is None:
                raise RuntimeError(f"Missing paper: {folder} / {paper_id}")
            output.append(
                {
                    "精读模块": module,
                    "子方向": subtopic,
                    "来源编号": row["来源编号"],
                    "论文标题": row["论文标题"],
                    "来源资料夹": row["来源资料夹"],
                    "相对路径": row["相对路径"],
                }
            )
    return output


def write_csv(rows: list[dict]) -> None:
    fields = [
        "精读模块",
        "子方向",
        "来源编号",
        "论文标题",
        "来源资料夹",
        "相对路径",
    ]
    with (ROOT / "推荐系统与数据挖掘_精读35篇.csv").open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict]) -> None:
    lines = [
        "# 推荐系统与数据挖掘精读 35 篇",
        "",
        "这份清单面向高影响力核心文献，按 7 个模块细分。"
        "完整路径和可筛选字段见 `推荐系统与数据挖掘_精读35篇.csv`。",
        "",
        "## 阅读顺序",
        "",
        "1. 先读 01，理解算法采纳、公平、可解释和 ML 方法框架。",
        "2. 再读 02–04，建立推荐、搜索和信息挖掘的主线。",
        "3. 然后读 05–06，补齐因果、实验、强化学习和可信推荐。",
        "4. 最后读 07，进入 LLM、生成式推荐和 Agent 前沿。",
        "",
    ]

    for module in GROUPS:
        module_rows = [row for row in rows if row["精读模块"] == module]
        lines.extend(
            [
                f"## {module}",
                "",
                f"共 {len(module_rows)} 篇。",
                "",
                "| 子方向 | 编号 | 论文 |",
                "| --- | --- | --- |",
            ]
        )
        for row in module_rows:
            lines.append(
                f"| {row['子方向']} | {row['来源编号']} | {row['论文标题']} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 压缩建议",
            "",
            "- 时间有限时，每模块至少精读 1 篇代表作。",
            "- 如果重点做推荐系统，优先 02–07。",
            "- 如果重点做数据挖掘与因果推断，优先 03–06。",
            "- 如果重点做 LLM4Rec，优先 01、02、05、07。",
            "",
        ]
    )
    (ROOT / "推荐系统与数据挖掘_精读35篇.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    rows = build_rows(load_rows())
    write_csv(rows)
    write_markdown(rows)
    print(f"Generated {len(rows)} core papers.")
    for module in GROUPS:
        print(module, sum(row["精读模块"] == module for row in rows))


if __name__ == "__main__":
    main()

