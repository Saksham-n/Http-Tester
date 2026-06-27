import statistics
import time
from collections import defaultdict
from typing import List, Dict, Any, Optional

class MetricsCollector:
    def __init__(self):
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.total_requests: int = 0
        self.successful_requests: int = 0
        self.failed_requests: int = 0
        self.latencies: List[float] = []
        self.status_codes: Dict[int, int] = defaultdict(int)
        self.errors: Dict[str, int] = defaultdict(int)

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    def record_success(self, latency: float, status_code: int):
        self.total_requests += 1
        self.successful_requests += 1
        self.latencies.append(latency)
        self.status_codes[status_code] += 1

    def record_failure(self, error_type: str, status_code: Optional[int] = None):
        self.total_requests += 1
        self.failed_requests += 1
        self.errors[error_type] += 1
        if status_code is not None:
            self.status_codes[status_code] += 1

    def calculate(self) -> Dict[str, Any]:
        duration = self.end_time - self.start_time
        if duration <= 0:
            duration = 0.0001 # Prevent division by zero

        req_per_sec = self.total_requests / duration

        if self.latencies:
            sorted_latencies = sorted(self.latencies)
            min_latency = sorted_latencies[0]
            max_latency = sorted_latencies[-1]
            avg_latency = statistics.mean(sorted_latencies)
            median_latency = statistics.median(sorted_latencies)
            
            # Calculate percentiles manually or using statistics (Python 3.8+)
            try:
                p95_latency = statistics.quantiles(sorted_latencies, n=100)[94]
                p99_latency = statistics.quantiles(sorted_latencies, n=100)[98]
            except statistics.StatisticsError:
                # Fallback for very few data points
                p95_latency = max_latency
                p99_latency = max_latency
        else:
            min_latency = max_latency = avg_latency = median_latency = p95_latency = p99_latency = 0.0

        error_percentage = (self.failed_requests / self.total_requests * 100) if self.total_requests > 0 else 0.0

        return {
            "execution_time_sec": round(duration, 4),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "requests_per_sec": round(req_per_sec, 2),
            "error_percentage": round(error_percentage, 2),
            "latency": {
                "min": round(min_latency, 4),
                "max": round(max_latency, 4),
                "avg": round(avg_latency, 4),
                "median": round(median_latency, 4),
                "p95": round(p95_latency, 4),
                "p99": round(p99_latency, 4),
            },
            "status_codes": dict(self.status_codes),
            "errors": dict(self.errors)
        }
