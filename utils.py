import json
from typing import Dict, Any, Optional
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """Check if the provided string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def parse_headers(headers_list: Optional[list[str]]) -> Dict[str, str]:
    """Parse a list of 'Key: Value' strings into a dictionary."""
    headers = {}
    if not headers_list:
        return headers
    
    for header in headers_list:
        if ':' in header:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def load_json_body(body_str: Optional[str]) -> Any:
    """Load JSON from string, returning None if invalid or empty."""
    if not body_str:
        return None
    try:
        return json.loads(body_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON body: {e}")
