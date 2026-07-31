FROM python:3.11-slim
WORKDIR /app
COPY tracker.py .
ENTRYPOINT ["python", "tracker.py"]
CMD ["list"]
