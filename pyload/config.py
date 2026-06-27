from dataclasses import dataclass, field
from typing import Dict, Optional, Any

@dataclass
class PyLoadConfig:
    url: str
    method: str = "GET"
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    total_requests: int = 100
    concurrent_users: int = 10
    timeout: float = 10.0
    retry_count: int = 0
    ssl_verify: bool = True
    allow_redirects: bool = True
    keep_alive: bool = True
    debug: bool = False
    output_dir: str = "reports"

    def __post_init__(self):
        self.method = self.method.upper()
        if self.concurrent_users <= 0:
            raise ValueError("Concurrent users must be greater than 0")
        if self.total_requests <= 0:
            raise ValueError("Total requests must be greater than 0")
