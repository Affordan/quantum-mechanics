import json
from pathlib import Path

from langchain.tools import tool

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "quantum_terms.json"
SOURCE_DATA_PATH = ROOT / "data" / "quantum_sources.jsonl"

PROJECT_PLAN_STEPS = [
    "用 FastAPI 搭一个后端服务",
    "接入 Kimi API，先确认模型能正常返回",
    "用 LangChain create_agent 创建一个最简单的 agent",
    "添加两个工具：项目计划工具、本地术语查询工具",
    "准备本地 quantum_terms.json 资料文件",
    "打通 /chat 接口联调",
    "用 3 条测试输入验证输出是否符合预期",
]

PROJECT_PLAN_MATERIALS = [
    "项目目标的一句话描述",
    "5~10 个量子力学核心术语及解释",
    "一份你希望输出的开发计划模板",
    "输出风格要求：简洁 / 面向开发者 / 不空话",
    "后续若要增强，再补教材摘要或讲义内容",
]


def get_project_plan_payload(project_name: str) -> dict[str, object]:
    return {
        "project_name": project_name,
        "source": "local_plan",
        "steps": PROJECT_PLAN_STEPS,
        "materials": PROJECT_PLAN_MATERIALS,
    }


def lookup_quantum_term_payload(term: str) -> dict[str, object] | None:
    normalized_term = term.strip()
    if not normalized_term:
        return None

    if not DATA_PATH.exists():
        return None

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    if normalized_term in data:
        item = data[normalized_term]
        return {
            "term": normalized_term,
            "source": "local_json",
            "found": True,
            "definition": item["definition"],
            "developer_view": item["developer_view"],
        }

    for key, item in data.items():
        if normalized_term in key or key in normalized_term:
            return {
                "term": key,
                "source": "local_json",
                "found": True,
                "definition": item["definition"],
                "developer_view": item["developer_view"],
            }

    return None


def _normalize_text(value: str) -> str:
    return value.strip().lower()


def _contains_query(query: str, value: str) -> bool:
    normalized_query = _normalize_text(query)
    normalized_value = _normalize_text(value)
    if not normalized_query or not normalized_value:
        return False
    return normalized_query in normalized_value or normalized_value in normalized_query


def _load_source_records() -> tuple[list[dict[str, object]] | None, str | None]:
    if not SOURCE_DATA_PATH.exists():
        return None, "本地来源库文件不存在，请先准备 data/quantum_sources.jsonl。"

    records: list[dict[str, object]] = []
    for line_number, raw_line in enumerate(
        SOURCE_DATA_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            return None, f"本地来源库格式有误，无法读取第 {line_number} 行。"

        records.append(record)

    return records, None


def _format_source_record(record: dict[str, object]) -> str:
    concepts = ", ".join(str(item) for item in record.get("concepts", []))
    source_page_url = str(record.get("source_page_url") or "无")
    return (
        f"标题：{record.get('title', '未知来源')}\n"
        f"概念：{concepts}\n"
        f"摘要：{record.get('summary', '')}\n"
        f"开发者视角：{record.get('developer_view', '')}\n"
        f"PDF：{record.get('pdf_filename', '')}\n"
        f"PDF URL：{record.get('pdf_url', '')}\n"
        f"来源页：{source_page_url}"
    ).strip()


def search_quantum_source_text(query: str) -> str:
    normalized_query = query.strip()
    if not normalized_query:
        return "请输入想查找的概念、资料名或关键词。"

    records, error_message = _load_source_records()
    if error_message is not None:
        return error_message
    if not records:
        return "本地来源库为空，请先整理 quantum_sources.jsonl。"

    exact_matches: list[dict[str, object]] = []
    partial_matches: list[dict[str, object]] = []

    for record in records:
        concepts = [str(item) for item in record.get("concepts", [])]
        if any(_normalize_text(normalized_query) == _normalize_text(concept) for concept in concepts):
            exact_matches.append(record)
            continue

        haystacks = concepts + [
            str(record.get("title", "")),
            str(record.get("summary", "")),
            str(record.get("developer_view", "")),
        ]
        if any(_contains_query(normalized_query, haystack) for haystack in haystacks):
            partial_matches.append(record)

    matches = exact_matches or partial_matches
    if not matches:
        return f"没有找到和“{normalized_query}”相关的本地参考资料。"

    top_matches = matches[:3]
    formatted = "\n\n".join(_format_source_record(record) for record in top_matches)
    return f"找到 {len(matches)} 条相关来源，以下展示前 {len(top_matches)} 条：\n\n{formatted}"


@tool
def get_project_plan(project_name: str) -> str:
    """返回项目的最小开发计划和需要准备的资料。"""
    payload = get_project_plan_payload(project_name)
    steps = "\n".join(
        f"{index}. {step}" for index, step in enumerate(payload["steps"], start=1)
    )
    materials = "\n".join(
        f"{index}. {item}" for index, item in enumerate(payload["materials"], start=1)
    )
    return f"""
项目名称：{project_name}

最小可运行版本开发计划：
{steps}

当前需要补充的资料：
{materials}
""".strip()


@tool
def lookup_quantum_term(term: str) -> str:
    """查询本地量子力学术语资料。"""
    if not term.strip():
        return "请输入想查询的量子力学术语。"

    payload = lookup_quantum_term_payload(term)
    if payload is None and not DATA_PATH.exists():
        return "本地术语资料文件不存在，请先准备 data/quantum_terms.json。"
    if payload is None:
        return f"本地资料中没有找到“{term}”，请先把这个术语补充进 quantum_terms.json。"
    return (
        f"{payload['term']}\n"
        f"定义：{payload['definition']}\n"
        f"开发者理解：{payload['developer_view']}"
    )


@tool
def search_quantum_source(query: str) -> str:
    """查询本地量子力学来源库，适合回答参考资料、PDF、讲义、出处类问题。"""
    return search_quantum_source_text(query)
