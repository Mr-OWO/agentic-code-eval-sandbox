from fastapi.testclient import TestClient
from code_eval_sandbox.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "agentic-code-eval-sandbox"}


def test_api_execute_python_code():
    payload = {
        "language": "python",
        "code": "print('API Execution Test')\nval = sum([1, 2, 3, 4])\nprint(f'Sum: {val}')",
        "test_assertions": "assert val == 10",
        "timeout_seconds": 3.0,
    }
    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["all_tests_passed"] is True
    assert "Sum: 10" in data["stdout"]
