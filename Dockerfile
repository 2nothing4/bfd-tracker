FROM python:3.11-slim
WORKDIR /app
COPY tracker.py .
RUN useradd -m -u 1000 appuser && chown appuser:appuser /app
USER appuser
ENTRYPOINT ["python", "tracker.py"]
CMD ["list"]
