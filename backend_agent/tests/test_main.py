from fastapi.testclient import TestClient

from app import main


def test_health_endpoint_returns_ok():
    client = TestClient(main.app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_returns_agent_answer(monkeypatch):
    client = TestClient(main.app)

    monkeypatch.setattr(main, "run_agent", lambda message: f"stubbed: {message}")

    response = client.post("/chat", json={"message": "解释一下叠加态"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "quantum_term"
    assert payload["data"]["term"] == "叠加态"
    assert "线性组合" in payload["data"]["definition"]
    assert "叠加态" in payload["answer"]


def test_chat_endpoint_returns_structured_project_plan():
    client = TestClient(main.app)

    response = client.post("/chat", json={"message": "请给我这个项目的最小开发计划和需要补充的资料"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "project_plan"
    assert isinstance(payload["data"]["steps"], list)
    assert isinstance(payload["data"]["materials"], list)


def test_chat_endpoint_returns_structured_general_answer(monkeypatch):
    client = TestClient(main.app)

    monkeypatch.setattr(main, "run_agent", lambda message: f"stubbed: {message}")

    response = client.post("/chat", json={"message": "你好"})

    assert response.status_code == 200
    assert response.json() == {
        "intent": "general",
        "answer": "stubbed: 你好",
        "data": {"source": "model"},
    }
