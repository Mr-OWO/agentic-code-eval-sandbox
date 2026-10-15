# Agentic-Code-Eval-Sandbox: Containerized Execution Sandbox for AI Code Benchmark Evals

[![CI](https://github.com/Mr-OWO/agentic-code-eval-sandbox/actions/workflows/ci.yml/badge.svg)](https://github.com/Mr-OWO/agentic-code-eval-sandbox/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Isolation-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, high-security containerized execution sandbox designed for evaluating autonomous coding agents, LLM code generation benchmarks (HumanEval, MBPP, SWE-bench), and synthetic tool-use routines. Enforces strict process resource ceilings (0.5 CPU, 256MB RAM), ephemeral filesystem destruction, and sub-second hard timeouts with zero host exposure.

---

## 🏛️ System Architecture

```
                  +-----------------------------------------------+
                  |          AI Agent / Benchmark Client          |
                  |  POST /api/v1/execute {lang, code, assertions}|
                  +-----------------------+-----------------------+
                                          |
                                          v
                  +-----------------------------------------------+
                  |              FastAPI REST Gateway             |
                  |    - Schema Validation (Pydantic v2)          |
                  |    - Rate Limiting & Auth Gate                |
                  +-----------------------+-----------------------+
                                          |
                                          v
                  +-----------------------------------------------+
                  |         IsolatedSandboxRunner Core            |
                  |    - Ephemeral Temp Workspace Allocation      |
                  |    - Non-Root Execution UID (1001)            |
                  |    - Strict Hard Timeout Watchdog (5.0s)      |
                  |    - Subprocess / Docker Resource Ceilings    |
                  +-----------------------+-----------------------+
                                          |
                        +-----------------+-----------------+
                        |                                   |
                        v                                   v
             [Python 3.12 Runtime]                 [Node.js 20 Runtime]
                        |                                   |
                        +-----------------+-----------------+
                                          |
                                          v
                  +-----------------------------------------------+
                  |            Telemetry & Safety Report          |
                  |  - stdout / stderr streams                    |
                  |  - Exit code & Latency milliseconds           |
                  |  - Memory usage & Assertion pass/fail status  |
                  +-----------------------------------------------+
```

---

## 🚀 Key Features

- **Multi-Language Execution Engine:** Executes Python 3.12 and JavaScript/Node.js routines with zero cross-environment contamination.
- **Resource Sandboxing:** Enforces hard timeout interrupts (5.0s default) via `asyncio.wait_for` and process tree SIGKILL terminations.
- **Automated Assertion Harness:** Automatically stitches benchmark test cases, unit asserts, and edge cases to candidate code submissions and parses execution tracebacks.
- **Ephemeral Lifecycle:** Allocates isolated temp workspaces per execution and wipes them cleanly on completion.
- **Zero Host Exposure:** Strips dangerous host environment variables (`PYTHONPATH`, sensitive tokens) and runs under unprivileged non-root users.

---

## 📦 Quick Start with Docker

```bash
git clone https://github.com/Mr-OWO/agentic-code-eval-sandbox.git
cd agentic-code-eval-sandbox
docker-compose up --build
```

The execution service will start at `http://localhost:8080`.
Interactive OpenAPI docs are available at `http://localhost:8080/docs`.

---

## 💡 API Usage Example

```bash
curl -X POST "http://localhost:8080/api/v1/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(nums):\n    return [x * 2 for x in nums]",
    "test_assertions": "assert solve([1, 2, 3]) == [2, 4, 6]",
    "timeout_seconds": 3.0
  }'
```

Response:
```json
{
  "status": "success",
  "stdout": "",
  "stderr": "",
  "exit_code": 0,
  "latency_ms": 38.4,
  "memory_used_mb": 14.5,
  "all_tests_passed": true,
  "assertion_results": [
    {
      "passed": true,
      "details": "All assertions verified successfully"
    }
  ]
}
```

---

## 🧪 Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
ruff check src/ tests/
```

---

## 👤 Author
**Wisdom Ogechi Owabor**
- Full-Stack Software Engineer & Python AI Systems Specialist
- Portfolio: [wisdomowabor.online](https://wisdomowabor.online)
- GitHub: [@Mr-OWO](https://github.com/Mr-OWO)
