# PyLoad - High-Performance Asynchronous HTTP Load Testing & API Analyzer

**Final Year Project (FYP)**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

**PyLoad** is a production-grade, asynchronous HTTP load testing and API performance analysis tool. Designed as a lightweight, modern alternative to tools like `k6` and `ApacheBench`, it evaluates the scalability, reliability, and network fundamentals of robust API endpoints under heavy concurrency.

Built entirely in Python, PyLoad leverages `asyncio` and `aiohttp` to maximize throughput using non-blocking I/O and connection pooling. It incorporates enterprise-grade software engineering best practices, emphasizing modular OOP design, SOLID principles, testing, and comprehensive logging.

### Key Features
- **Asynchronous Execution:** High concurrency utilizing `asyncio` and `aiohttp` connection pooling.
- **Advanced Metrics:** Computes standard statistics including total throughput, error percentages, and latency percentiles (P95, P99, Median, Min, Max).
- **Enterprise Networking:** Supports HTTP Keep-Alive, connection reuse, DNS resolution failure handling, SSL verification, and custom headers.
- **Reporting:** Generates detailed reports in JSON, CSV, and TXT formats for post-test analysis.
- **Graceful Degradation:** Robust timeout handling, retry mechanisms with exponential backoff, and graceful cancellation handling (Ctrl+C).

---

## Architecture

PyLoad's architecture separates concerns strictly for maintainability and extensibility:

```text
+-------------------+       +-------------------+       +--------------------+
|                   |       |                   |       |                    |
|   CLI interface   +------->   Configuration   +------->   Execution Engine |
|   (argparse)      |       |   (dataclass)     |       |   (aiohttp pool)   |
|                   |       |                   |       |                    |
+-------------------+       +-------------------+       +---------+----------+
                                                                  |
                                                                  |
+-------------------+       +-------------------+       +---------v----------+
|                   |       |                   |       |                    |
|   File / Console  <-------+     Reporting     <-------+  Metrics Collector |
|   Outputs         |       |  (JSON/CSV/TXT)   |       |  (Aggregations)    |
|                   |       |                   |       |                    |
+-------------------+       +-------------------+       +--------------------+
```

---

## Installation

Ensure you have Python 3.12+ installed.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pyload
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage Examples

PyLoad provides a robust CLI interface. Run `python -m pyload.main --help` to see all available options.

### Basic GET Request Load Test
Simulate 100 concurrent users sending a total of 1000 requests to an endpoint:
```bash
python -m pyload.main -u https://jsonplaceholder.typicode.com/posts -c 100 -n 1000
```

### POST Request with Custom Headers & JSON Payload
```bash
python -m pyload.main -u https://api.example.com/data \
  -m POST \
  -H "Authorization: Bearer my-token" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  -c 50 -n 500
```

### YAML Configuration File Support
Instead of passing numerous CLI flags, PyLoad supports YAML configurations:
```yaml
# config.yaml
url: https://jsonplaceholder.typicode.com/users
method: GET
headers:
  - "Accept: application/json"
requests: 2000
concurrency: 200
timeout: 5.0
retry: 2
```
Execute with:
```bash
python -m pyload.main -f config.yaml
```

---

## Output and Reports

Upon test completion, PyLoad renders a beautiful Rich-formatted terminal summary and automatically exports reports to the `reports/` directory.

---

## Testing

PyLoad uses `pytest` for unit testing, employing `aioresponses` to mock network requests and ensure tests are fast and deterministic.

```bash
pytest tests/
```

---

## Containerization

A `Dockerfile` is provided for containerized deployment, ensuring the tool runs consistently across environments.

```bash
docker build -t pyload .
docker run --rm pyload -u https://example.com -c 10 -n 100
```

## Continuous Integration

A GitHub Actions workflow is included (`.github/workflows/pytest.yml`) to automatically run the test suite on every push.

---
**Developed as part of a Final Year Project aimed at mastering high-performance networking and backend systems engineering.**
