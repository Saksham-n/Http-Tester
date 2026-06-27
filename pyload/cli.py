import argparse
import yaml
from pathlib import Path
from typing import Dict, Any, List

from .config import PyLoadConfig
from .utils import parse_headers

def load_yaml_config(file_path: str) -> Dict[str, Any]:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PyLoad - Asynchronous HTTP Load Testing and API Performance Analyzer (FYP)"
    )
    
    parser.add_argument("-u", "--url", type=str, help="Target URL for load testing")
    parser.add_argument("-m", "--method", type=str, default="GET", help="HTTP Method (GET, POST, etc.)")
    parser.add_argument("-H", "--header", action="append", help="HTTP Headers (e.g., -H 'Accept: application/json')")
    parser.add_argument("-d", "--data", type=str, help="Request body (JSON string)")
    parser.add_argument("-n", "--requests", type=int, default=100, help="Total number of requests to send")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Number of concurrent users")
    parser.add_argument("-t", "--timeout", type=float, default=10.0, help="Request timeout in seconds")
    parser.add_argument("-r", "--retry", type=int, default=0, help="Number of retries per request")
    parser.add_argument("-f", "--file", type=str, help="Path to YAML configuration file")
    
    # Flags
    parser.add_argument("--no-ssl", action="store_false", dest="ssl_verify", help="Disable SSL verification")
    parser.add_argument("--no-redirect", action="store_false", dest="allow_redirects", help="Disable following redirects")
    parser.add_argument("--no-keepalive", action="store_false", dest="keep_alive", help="Disable HTTP Keep-Alive")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("-o", "--output", type=str, default="reports", help="Output directory for reports")
    
    return parser

def parse_args(args: List[str] = None) -> PyLoadConfig:
    parser = build_parser()
    parsed = parser.parse_args(args)
    
    config_data = {}
    if parsed.file:
        config_data = load_yaml_config(parsed.file)
        
    # CLI args override YAML config
    url = parsed.url or config_data.get("url")
    if not url:
        parser.error("URL is required either via CLI (-u) or YAML config (-f)")
        
    method = config_data.get("method", parsed.method)
    
    headers_list = parsed.header if parsed.header else config_data.get("headers", [])
    headers = parse_headers(headers_list) if isinstance(headers_list, list) else headers_list
    
    body = parsed.data or config_data.get("body")
    total_requests = parsed.requests if parsed.requests != 100 else config_data.get("requests", 100)
    concurrency = parsed.concurrency if parsed.concurrency != 10 else config_data.get("concurrency", 10)
    timeout = parsed.timeout if parsed.timeout != 10.0 else config_data.get("timeout", 10.0)
    retry_count = parsed.retry if parsed.retry != 0 else config_data.get("retry", 0)
    
    ssl_verify = parsed.ssl_verify if not config_data.get("no_ssl") else False
    allow_redirects = parsed.allow_redirects if not config_data.get("no_redirect") else False
    keep_alive = parsed.keep_alive if not config_data.get("no_keepalive") else False
    debug = parsed.debug or config_data.get("debug", False)
    output_dir = parsed.output if parsed.output != "reports" else config_data.get("output", "reports")
    
    return PyLoadConfig(
        url=url,
        method=method,
        headers=headers,
        body=body,
        total_requests=total_requests,
        concurrent_users=concurrency,
        timeout=timeout,
        retry_count=retry_count,
        ssl_verify=ssl_verify,
        allow_redirects=allow_redirects,
        keep_alive=keep_alive,
        debug=debug,
        output_dir=output_dir
    )
