import pytest
from aioresponses import aioresponses
from pyload.config import PyLoadConfig
from pyload.metrics import MetricsCollector
from pyload.engine import PyLoadEngine

@pytest.mark.asyncio
async def test_engine_successful_requests():
    config = PyLoadConfig(url="http://example.com", total_requests=5, concurrent_users=2)
    metrics = MetricsCollector()
    engine = PyLoadEngine(config, metrics)
    
    with aioresponses() as m:
        m.get('http://example.com/', status=200, repeat=True)
        await engine.run()
        
    result = metrics.calculate()
    assert result["total_requests"] == 5
    assert result["successful_requests"] == 5
    assert result["failed_requests"] == 0
    assert result["status_codes"][200] == 5

@pytest.mark.asyncio
async def test_engine_failed_requests():
    config = PyLoadConfig(url="http://example.com", total_requests=3, concurrent_users=1, retry_count=0)
    metrics = MetricsCollector()
    engine = PyLoadEngine(config, metrics)
    
    with aioresponses() as m:
        m.get('http://example.com/', status=500, repeat=True)
        await engine.run()
        
    result = metrics.calculate()
    assert result["total_requests"] == 3
    assert result["successful_requests"] == 0
    assert result["failed_requests"] == 3
    assert result["status_codes"][500] == 3
