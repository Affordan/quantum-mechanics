from fastapi import FastAPI
from pydantic import BaseModel

from .agent import run_agent
from .tools import (
    get_project_plan,
    lookup_quantum_term,
    lookup_quantum_term_payload,
    search_quantum_source,
)

app = FastAPI(title="Quantum Agent Backend")


class ChatRequest(BaseModel):
    message: str


def _is_plan_query(message: str) -> bool:
    keywords = ("计划", "先做什么", "资料", "开发计划", "补充")
    return any(keyword in message for keyword in keywords)


def _is_source_query(message: str) -> bool:
    source_markers = ("资料", "来源", "出处", "参考", "pdf", "PDF", "讲义", "哪本", "哪个", "材料")
    physics_hints = (
        "量子",
        "波函数",
        "叠加态",
        "测不准",
        "薛定谔",
        "哈密顿",
        "本征",
        "纠缠",
        "量子比特",
        "量子门",
    )
    normalized = message.strip()
    return any(marker in normalized for marker in source_markers) and any(
        hint in normalized for hint in physics_hints
    )


def _is_term_query(message: str) -> bool:
    term_markers = ("解释", "什么是", "介绍", "术语", "原理")
    physics_hints = ("量子", "波函数", "叠加态", "测不准", "薛定谔", "哈密顿")
    normalized = message.strip()
    return any(marker in normalized for marker in term_markers) and any(
        hint in normalized for hint in physics_hints
    )


def _extract_term(message: str) -> str:
    normalized = message.strip()
    prefixes = ("请解释一下", "解释一下", "解释", "什么是", "请介绍一下", "介绍一下")
    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix) :].strip()
            break

    suffixes = ("是什么", "是啥", "?", "？")
    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)].strip()
            break
    return normalized


def _should_use_local_term_lookup(term: str) -> bool:
    normalized_term = term.strip()
    if not normalized_term:
        return False

    if lookup_quantum_term_payload(normalized_term) is not None:
        return True

    complex_markers = ("区别", "为什么", "如何", "怎么", "作用", "应用", "影响", "比较", "联系", "举例", "一句话")
    if any(marker in normalized_term for marker in complex_markers):
        return False

    return len(normalized_term) <= 12


def build_chat_answer(message: str) -> str:
    normalized = message.strip()
    if not normalized:
        return "请输入问题内容，例如“请解释一下叠加态”或“有哪些资料可以帮助我理解波函数？”。"

    if _is_source_query(normalized):
        return search_quantum_source.invoke({"query": normalized})

    if _is_plan_query(normalized):
        return get_project_plan.invoke({"project_name": "量子力学学习助手"})

    if _is_term_query(normalized):
        term = _extract_term(normalized)
        if _should_use_local_term_lookup(term):
            return lookup_quantum_term.invoke({"term": term})

    return run_agent(normalized)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest) -> dict[str, str]:
    return {"answer": build_chat_answer(req.message)}
