import logging
from prometheus_client import Counter, Histogram
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.core.config import settings

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

CONTEXT_COMMIT_COUNT = Counter(
    "context_commit_total",
    "Total number of context commits",
    ["type"],
)

CONTEXT_RETRIEVAL_COUNT = Counter(
    "context_retrieval_total",
    "Total number of context retrievals",
    ["type"],
)

def init_monitoring():
    # Set up logging
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Set up Sentry if DSN is provided
    if hasattr(settings, "SENTRY_DSN") and settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.APP_ENV,
            traces_sample_rate=1.0,
        )

def track_request(method: str, endpoint: str, status: int, duration: float):
    """Track HTTP request metrics."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

def track_context_commit(context_type: str):
    """Track context commit metrics."""
    CONTEXT_COMMIT_COUNT.labels(type=context_type).inc()

def track_context_retrieval(context_type: str):
    """Track context retrieval metrics."""
    CONTEXT_RETRIEVAL_COUNT.labels(type=context_type).inc() 