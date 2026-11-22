FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY ctcc_mcp/ ./ctcc_mcp/

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "ctcc_mcp.server"]
