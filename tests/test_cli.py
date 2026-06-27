import pytest
from pyload.cli import parse_args

def test_parse_args_basic():
    args = ["-u", "http://test.com", "-n", "50", "-c", "5"]
    config = parse_args(args)
    
    assert config.url == "http://test.com"
    assert config.total_requests == 50
    assert config.concurrent_users == 5
    assert config.method == "GET"

def test_parse_args_headers():
    args = ["-u", "http://test.com", "-H", "Authorization: Bearer token", "-H", "Accept: application/json"]
    config = parse_args(args)
    
    assert config.headers["Authorization"] == "Bearer token"
    assert config.headers["Accept"] == "application/json"

def test_parse_args_missing_url():
    with pytest.raises(SystemExit):
        parse_args(["-n", "50"])
