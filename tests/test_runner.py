import pytest
from code_eval_sandbox.models import ExecutionRequest
from code_eval_sandbox.runner import IsolatedSandboxRunner


@pytest.mark.asyncio
async def test_python_successful_execution():
    runner = IsolatedSandboxRunner()
    req = ExecutionRequest(
        language="python",
        code="print('Hello from sandbox!')\nx = 10 * 5\nprint(f'Result: {x}')",
    )
    result = await runner.execute(req)

    assert result.status == "success"
    assert result.exit_code == 0
    assert "Hello from sandbox!" in result.stdout
    assert "Result: 50" in result.stdout
    assert result.latency_ms > 0


@pytest.mark.asyncio
async def test_python_with_assertions_passed():
    runner = IsolatedSandboxRunner()
    req = ExecutionRequest(
        language="python",
        code="def add(a, b): return a + b",
        test_assertions="assert add(2, 3) == 5\nassert add(-1, 1) == 0",
    )
    result = await runner.execute(req)

    assert result.status == "success"
    assert result.all_tests_passed is True
    assert len(result.assertion_results) == 1
    assert result.assertion_results[0].passed is True


@pytest.mark.asyncio
async def test_python_with_assertions_failed():
    runner = IsolatedSandboxRunner()
    req = ExecutionRequest(
        language="python",
        code="def multiply(a, b): return a + b",  # Buggy implementation
        test_assertions="assert multiply(2, 3) == 6",
    )
    result = await runner.execute(req)

    assert result.status == "error"
    assert result.all_tests_passed is False
    assert "AssertionError" in result.stderr


@pytest.mark.asyncio
async def test_execution_timeout_enforcement():
    runner = IsolatedSandboxRunner()
    req = ExecutionRequest(
        language="python",
        code="import time\ntime.sleep(5.0)",
        timeout_seconds=0.8,
    )
    result = await runner.execute(req)

    assert result.status == "timeout"
    assert "timed out" in result.stderr
    assert result.exit_code == -9
