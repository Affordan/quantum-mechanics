import json
from pathlib import Path

from langchain.tools import tool

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "quantum_terms.json"

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
    if not DATA_PATH.exists():
        return None

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    if term in data:
        item = data[term]
        return {
            "term": term,
            "source": "local_json",
            "found": True,
            "definition": item["definition"],
            "developer_view": item["developer_view"],
        }

    for key, item in data.items():
        if term in key or key in term:
            return {
                "term": key,
                "source": "local_json",
                "found": True,
                "definition": item["definition"],
                "developer_view": item["developer_view"],
            }

    return None


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
