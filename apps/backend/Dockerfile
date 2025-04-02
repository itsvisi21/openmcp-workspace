# Base stage with common dependencies
FROM python:3.11-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development
ENV PYTHONPATH=/app
ENV ENVIRONMENT=development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Test stage
FROM base as test
ENV PYTHONPATH=/app
ENV ENVIRONMENT=test
COPY . .
CMD ["pytest", "-v", "--cov=app", "--cov-report=term-missing"]

# Production stage
FROM base as production
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 