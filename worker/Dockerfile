FROM python:3.11-slim AS build
WORKDIR /build
COPY worker.py .

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --system --uid 10001 appuser && mkdir -p /data/results && chown -R appuser:appuser /data
COPY --from=build --chown=appuser:appuser /build/worker.py .
USER 10001
CMD ["python", "worker.py"]
