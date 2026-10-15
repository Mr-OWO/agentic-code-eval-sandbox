FROM python:3.12-slim

# Install Node.js for polyglot benchmark evaluation (Python + JS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY src/ ./src/

EXPOSE 8080

# Run with non-root user for security isolation
RUN useradd -u 1001 sandboxuser && chown -R sandboxuser:sandboxuser /app
USER sandboxuser

CMD ["uvicorn", "code_eval_sandbox.main:app", "--host", "0.0.0.0", "--port", "8080"]
