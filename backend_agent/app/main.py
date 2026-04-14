from fastapi import FastAPI
from pydantic import BaseModel

from .agent import run_agent
from .tools import get_project_plan_payload, lookup_quantum_term_payload

app = FastAPI(title="Quantum Agent Backend")


class ChatRequest(BaseModel):
    message: str


def _is_plan_query(message: str) -> bool:
    keywords = ("计划", "先做什么", "资料", "开发计划", "补充")
    return any(keyword in message for keyword in keywords)


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


def build_chat_response(message: str) -> dict[str, object]:
    if _is_plan_query(message):
        data = get_project_plan_payload("量子力学学习助手")
        answer = "最小开发计划已整理完成，可直接查看步骤和资料清单。"
        return {"intent": "project_plan", "answer": answer, "data": data}

    term = _extract_term(message)
    term_data = lookup_quantum_term_payload(term)
    if term_data is not None:
        answer = (
            f"{term_data['term']}：{term_data['definition']} "
            f"开发者理解：{term_data['developer_view']}"
        )
        return {"intent": "quantum_term", "answer": answer, "data": term_data}

    answer = run_agent(message)
    return {"intent": "general", "answer": answer, "data": {"source": "model"}}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest) -> dict[str, object]:
    return build_chat_response(req.message)
