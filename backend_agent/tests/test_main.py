from fastapi.testclient import TestClient

from app import main


def test_health_endpoint_returns_ok():
    client = TestClient(main.app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_returns_plain_answer_for_term_query():
    client = TestClient(main.app)

    response = client.post("/chat", json={"message": "解释一下叠加态"})

    assert response.status_code == 200
    assert set(response.json().keys()) == {"answer"}
    assert "叠加态" in response.json()["answer"]


def test_chat_endpoint_returns_plain_answer_for_project_plan():
    client = TestClient(main.app)

    response = client.post("/chat", json={"message": "请给我这个项目的最小开发计划和需要补充的资料"})

    assert response.status_code == 200
    assert set(response.json().keys()) == {"answer"}
    assert "开发计划" in response.json()["answer"]


def test_chat_endpoint_returns_plain_answer_for_general_query(monkeypatch):
    client = TestClient(main.app)

    monkeypatch.setattr(main, "run_agent", lambda message: f"stubbed: {message}")

    response = client.post("/chat", json={"message": "你好"})

    assert response.status_code == 200
    assert response.json() == {"answer": "stubbed: 你好"}


def test_chat_endpoint_keeps_non_physics_intro_query_as_general(monkeypatch):
    client = TestClient(main.app)

    monkeypatch.setattr(main, "run_agent", lambda message: f"stubbed: {message}")

    response = client.post("/chat", json={"message": "请用一句话介绍你自己"})

    assert response.status_code == 200
    assert response.json() == {"answer": "stubbed: 请用一句话介绍你自己"}


def test_chat_endpoint_keeps_long_physics_question_as_general(monkeypatch):
    client = TestClient(main.app)

    monkeypatch.setattr(main, "run_agent", lambda message: f"stubbed: {message}")

    response = client.post("/chat", json={"message": "请用一句话解释量子力学和经典力学的区别"})

    assert response.status_code == 200
    assert response.json() == {"answer": "stubbed: 请用一句话解释量子力学和经典力学的区别"}


def test_chat_endpoint_returns_local_message_for_unknown_term():
    client = TestClient(main.app)

    response = client.post("/chat", json={"message": "请解释一下量子纠缠"})

    assert response.status_code == 200
    assert "没有找到" in response.json()["answer"]


def test_chat_endpoint_returns_source_answer_for_source_query():
    client = TestClient(main.app)

    response = client.post("/chat", json={"message": "有什么资料可以帮助我理解波函数？"})

    assert response.status_code == 200
    assert set(response.json().keys()) == {"answer"}
    assert "PDF" in response.json()["answer"] or "pdf" in response.json()["answer"]
    assert "波函数" in response.json()["answer"]


def test_chat_endpoint_handles_empty_message():
    client = TestClient(main.app)

    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 200
    assert "请输入" in response.json()["answer"]
