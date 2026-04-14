from app.tools import (
    get_project_plan,
    get_project_plan_payload,
    lookup_quantum_term,
    lookup_quantum_term_payload,
)


def test_get_project_plan_contains_mvp_steps():
    result = get_project_plan.invoke({"project_name": "量子力学学习助手"})
    assert "最小可运行版本开发计划" in result
    assert "FastAPI" in result


def test_lookup_quantum_term_returns_known_term():
    result = lookup_quantum_term.invoke({"term": "叠加态"})
    assert "叠加态" in result
    assert "定义：" in result
    assert "开发者理解：" in result


def test_lookup_quantum_term_handles_unknown_term():
    result = lookup_quantum_term.invoke({"term": "量子纠缠"})
    assert "没有找到" in result


def test_lookup_quantum_term_payload_returns_structured_data():
    result = lookup_quantum_term_payload("叠加态")
    assert result is not None
    assert result["term"] == "叠加态"
    assert "线性组合" in result["definition"]


def test_get_project_plan_payload_returns_lists():
    result = get_project_plan_payload("量子力学学习助手")
    assert result["project_name"] == "量子力学学习助手"
    assert isinstance(result["steps"], list)
    assert isinstance(result["materials"], list)
