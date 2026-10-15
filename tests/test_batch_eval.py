import pytest
from code_eval_sandbox.batch_eval import BatchExecutionRunner
from code_eval_sandbox.models import ExecutionRequest


@pytest.mark.asyncio
async def test_batch_runner_success():
    runner = BatchExecutionRunner()
    req1 = ExecutionRequest(
        language="python",
        code="def solve(): return 42",
        test_assertions="assert solve() == 42",
    )
    req2 = ExecutionRequest(
        language="python",
        code="def greet(): return 'hello'",
        test_assertions="assert greet() == 'hello'",
    )
    summary = await runner.run_batch([req1, req2])
    assert summary.total_tasks == 2
    assert summary.successful_executions == 2
    assert summary.pass_rate == 1.0


@pytest.mark.asyncio
async def test_batch_runner_empty():
    runner = BatchExecutionRunner()
    summary = await runner.run_batch([])
    assert summary.total_tasks == 0
    assert summary.pass_rate == 0.0
