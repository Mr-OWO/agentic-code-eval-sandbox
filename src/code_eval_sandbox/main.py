from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ExecutionRequest, ExecutionResult
from .runner import IsolatedSandboxRunner

app = FastAPI(
    title="Agentic Code Execution Sandbox API",
    version="0.1.0",
    description="Containerized execution harness for LLM and AI agent code benchmark evaluations.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runner = IsolatedSandboxRunner()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "agentic-code-eval-sandbox"}


@app.post("/api/v1/execute", response_model=ExecutionResult)
async def execute_code(request: ExecutionRequest):
    try:
        return await runner.execute(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
