# Minimal image for running the MCP stdio server
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Default environment (override at runtime as needed)
ENV LLM_MODEL=gpt-5 \
    LLM_BASE_URL=https://api.openai.com/v1

# Expose stdio-based MCP server
CMD ["python", "-m", "src.mcp_server"]

