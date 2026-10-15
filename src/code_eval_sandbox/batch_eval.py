"""Batch execution harness for concurrent agent code evaluations."""

import asyncio
from typing import List, Optional
from pydantic import BaseModel
from .models import ExecutionRequest, ExecutionResult
from .runner import IsolatedSandboxRunner


class BatchBenchmarkSummary(BaseModel):
    total_tasks: int
    successful_executions: int
    timed_out_executions: int
    error_executions: int
    mean_latency_ms: float
    pass_rate: float


class BatchExecutionRunner:
    """Executes multiple benchmark evaluation requests asynchronously and aggregates metrics."""

    def __init__(self, runner: Optional[IsolatedSandboxRunner] = None):
        self.runner = runner or IsolatedSandboxRunner()

    async def run_batch(self, requests: List[ExecutionRequest]) -> BatchBenchmarkSummary:
        total = len(requests)
        if total == 0:
            return BatchBenchmarkSummary(
                total_tasks=0,
                successful_executions=0,
                timed_out_executions=0,
                error_executions=0,
                mean_latency_ms=0.0,
                pass_rate=0.0,
            )

        results: List[ExecutionResult] = await asyncio.gather(
            *(self.runner.execute(req) for req in requests)
        )
        success_count = sum(1 for r in results if r.status == "success" and r.all_tests_passed)
        timeout_count = sum(1 for r in results if r.status == "timeout")
        error_count = sum(1 for r in results if r.status == "error")
        mean_lat = sum(r.latency_ms for r in results) / total

        return BatchBenchmarkSummary(
            total_tasks=total,
            successful_executions=success_count,
            timed_out_executions=timeout_count,
            error_executions=error_count,
            mean_latency_ms=round(mean_lat, 2),
            pass_rate=round(success_count / total, 4),
        )
