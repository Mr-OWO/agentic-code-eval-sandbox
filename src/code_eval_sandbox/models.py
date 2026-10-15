from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class AssertionResult(BaseModel):
    passed: bool
    details: str


class ExecutionRequest(BaseModel):
    """Payload to be executed inside the isolated sandbox."""
    language: Literal["python", "javascript"] = Field(default="python", description="Target programming language")
    code: str = Field(..., min_length=1, description="Source code snippet to execute")
    test_assertions: Optional[str] = Field(None, description="Optional unit test assertion script to append")
    timeout_seconds: float = Field(default=5.0, ge=0.5, le=30.0, description="Hard timeout ceiling")
    memory_limit_mb: int = Field(default=256, ge=32, le=1024, description="Memory limit ceiling in megabytes")


class ExecutionResult(BaseModel):
    """Captured telemetry and stdout/stderr output from sandbox execution."""
    status: Literal["success", "timeout", "error", "memory_limit_exceeded"]
    stdout: str
    stderr: str
    exit_code: int
    latency_ms: float
    memory_used_mb: float
    all_tests_passed: bool
    assertion_results: List[AssertionResult] = Field(default_factory=list)
