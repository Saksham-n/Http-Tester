import pytest
from pyload.metrics import MetricsCollector

def test_metrics_initialization():
    metrics = MetricsCollector()
    assert metrics.total_requests == 0
    assert metrics.successful_requests == 0
    assert metrics.failed_requests == 0

def test_metrics_calculation_empty():
    metrics = MetricsCollector()
    metrics.start()
    metrics.stop()
    result = metrics.calculate()
    assert result["total_requests"] == 0
    assert result["error_percentage"] == 0.0

def test_metrics_calculation_success():
    metrics = MetricsCollector()
    metrics.start()
    metrics.record_success(0.1, 200)
    metrics.record_success(0.2, 200)
    metrics.record_success(0.3, 201)
    metrics.stop()
    
    result = metrics.calculate()
    assert result["total_requests"] == 3
    assert result["successful_requests"] == 3
    assert result["failed_requests"] == 0
    assert result["status_codes"][200] == 2
    assert result["status_codes"][201] == 1
    assert result["latency"]["min"] == 0.1
    assert result["latency"]["max"] == 0.3
    assert result["latency"]["avg"] == 0.2
    assert result["error_percentage"] == 0.0

def test_metrics_calculation_failure():
    metrics = MetricsCollector()
    metrics.start()
    metrics.record_success(0.1, 200)
    metrics.record_failure("TimeoutError")
    metrics.record_failure("HTTP_500", 500)
    metrics.stop()
    
    result = metrics.calculate()
    assert result["total_requests"] == 3
    assert result["successful_requests"] == 1
    assert result["failed_requests"] == 2
    assert result["status_codes"][200] == 1
    assert result["status_codes"][500] == 1
    assert result["errors"]["TimeoutError"] == 1
    assert result["errors"]["HTTP_500"] == 1
    assert round(result["error_percentage"], 2) == 66.67
