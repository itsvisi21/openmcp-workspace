from typing import Dict, Any, Optional
from prometheus_client import Counter, Gauge, Histogram
import sentry_sdk

class MonitoringClient:
    def __init__(self, enable_monitoring: bool = True):
        self.enable_monitoring = enable_monitoring
        self.metrics = {}
        self._initialize_metrics()

    def _initialize_metrics(self):
        """Initialize default metrics."""
        self.metrics["request_count"] = Counter(
            "request_count_total",
            "Total number of requests"
        )
        self.metrics["request_latency"] = Histogram(
            "request_latency_seconds",
            "Request latency in seconds"
        )
        self.metrics["active_connections"] = Gauge(
            "active_connections",
            "Number of active connections"
        )

    async def record_metric(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a metric value."""
        if not self.enable_monitoring:
            return

        if name not in self.metrics:
            raise ValueError(f"Unknown metric: {name}")

        if isinstance(self.metrics[name], Counter):
            self.metrics[name].inc(value)
        elif isinstance(self.metrics[name], Gauge):
            self.metrics[name].set(value)
        elif isinstance(self.metrics[name], Histogram):
            self.metrics[name].observe(value)

    async def record_event(self, event_type: str, data: Dict[str, Any]):
        """Record an event."""
        if not self.enable_monitoring:
            return

        sentry_sdk.capture_event({
            "type": event_type,
            "data": data
        }) 