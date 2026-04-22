import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from .prompts import SYSTEM_PROMPT
from .tools import get_project_plan, lookup_quantum_term, search_quantum_source

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


@lru_cache(maxsize=1)
def build_agent():
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key or api_key == "your_moonshot_api_key":
        raise RuntimeError("未配置有效的 MOONSHOT_API_KEY，请先更新 backend_agent/.env。")

    model = ChatOpenAI(
        model="kimi-k2.5",
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1",
        max_completion_tokens=2048,
        extra_body={"thinking": {"type": "disabled"}},
    )

    return create_agent(
        model=model,
        tools=[get_project_plan, lookup_quantum_term, search_quantum_source],
        system_prompt=SYSTEM_PROMPT,
    )


def _normalize_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(str(item))
            else:
                text = getattr(item, "text", None)
                parts.append(str(text if text is not None else item))
        return "\n".join(part for part in parts if part).strip()

    return str(content).strip()


def run_agent(user_input: str) -> str:
    try:
        agent = build_agent()
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    except Exception as exc:
        return f"Agent 调用失败：{exc}"

    messages = result.get("messages", [])
    if not messages:
        return "Agent 没有返回内容。"

    last_message = messages[-1]
    content = getattr(last_message, "content", last_message)
    answer = _normalize_content(content)
    return answer or "Agent 没有返回可读文本。"
