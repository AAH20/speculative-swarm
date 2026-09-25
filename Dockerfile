FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY speculative_swarm/ ./speculative_swarm/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["speculative-swarm"]
CMD ["race"]
