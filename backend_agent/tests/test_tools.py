from pathlib import Path

import app.tools as tools_module
from app.tools import (
    get_project_plan,
    get_project_plan_payload,
    lookup_quantum_term,
    lookup_quantum_term_payload,
    search_quantum_source,
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


def test_lookup_quantum_term_handles_empty_input():
    result = lookup_quantum_term.invoke({"term": ""})
    assert "请输入" in result


def test_lookup_quantum_term_payload_returns_structured_data():
    result = lookup_quantum_term_payload("叠加态")
    assert result is not None
    assert result["source"] == "local_json"
    assert result["found"] is True
    assert result["term"] == "叠加态"
    assert "线性组合" in result["definition"]


def test_get_project_plan_payload_returns_lists():
    result = get_project_plan_payload("量子力学学习助手")
    assert result["project_name"] == "量子力学学习助手"
    assert result["source"] == "local_plan"
    assert isinstance(result["steps"], list)
    assert isinstance(result["materials"], list)


def test_lookup_quantum_term_payload_supports_three_core_terms():
    for term in ("波函数", "叠加态", "测不准原理"):
        result = lookup_quantum_term_payload(term)
        assert result is not None
        assert result["term"] == term


def test_search_quantum_source_supports_exact_concept_match():
    result = search_quantum_source.invoke({"query": "波函数"})
    assert "波函数" in result
    assert "PDF" in result or "pdf" in result


def test_search_quantum_source_supports_partial_sentence_query():
    result = search_quantum_source.invoke({"query": "哪个 PDF 适合开发者理解量子比特？"})
    assert "量子比特" in result
    assert "Quantum Computing for the Quantum Curious" in result


def test_search_quantum_source_handles_empty_input():
    result = search_quantum_source.invoke({"query": ""})
    assert "请输入" in result


def test_search_quantum_source_handles_missing_file(monkeypatch, tmp_path):
    missing_path = tmp_path / "missing.jsonl"
    monkeypatch.setattr(tools_module, "SOURCE_DATA_PATH", missing_path)

    result = search_quantum_source.invoke({"query": "波函数"})
    assert "不存在" in result


def test_search_quantum_source_handles_invalid_jsonl(monkeypatch, tmp_path):
    invalid_path = tmp_path / "invalid.jsonl"
    invalid_path.write_text("{bad json}\n", encoding="utf-8")
    monkeypatch.setattr(tools_module, "SOURCE_DATA_PATH", invalid_path)

    result = search_quantum_source.invoke({"query": "波函数"})
    assert "格式有误" in result
