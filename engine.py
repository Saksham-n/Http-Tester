import asyncio
import time
import aiohttp
from typing import Optional
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn

from .config import PyLoadConfig
from .metrics import MetricsCollector
from .logger import logger

class PyLoadEngine:
    def __init__(self, config: PyLoadConfig, metrics: MetricsCollector):
        self.config = config
        self.metrics = metrics
        self.is_cancelled = False
        self._progress = None

    async def _make_request(self, session: aiohttp.ClientSession, task_id: int):
        retries = 0
        while retries <= self.config.retry_count and not self.is_cancelled:
            start_time = time.perf_counter()
            try:
                async with session.request(
                    method=self.config.method,
                    url=self.config.url,
                    headers=self.config.headers,
                    data=self.config.body,
                    allow_redirects=self.config.allow_redirects,
                ) as response:
                    # Read the response to ensure connection is freed
                    await response.read()
                    latency = time.perf_counter() - start_time
                    
                    if response.status >= 400:
                        logger.debug(f"Request failed with status {response.status}: {self.config.url}")
                        self.metrics.record_failure(f"HTTP_{response.status}", status_code=response.status)
                    else:
                        self.metrics.record_success(latency, status_code=response.status)
                    return
            except aiohttp.ClientError as e:
                logger.debug(f"ClientError on attempt {retries + 1}: {e}")
                error_type = type(e).__name__
            except asyncio.TimeoutError:
                logger.debug(f"TimeoutError on attempt {retries + 1}")
                error_type = "TimeoutError"
            except Exception as e:
                logger.debug(f"Unexpected error: {e}")
                error_type = type(e).__name__
            
            retries += 1
            if retries <= self.config.retry_count:
                await asyncio.sleep(0.1 * retries) # Simple exponential backoff
        
        # If we exhausted retries
        if not self.is_cancelled:
            self.metrics.record_failure(error_type)

    async def _worker(self, session: aiohttp.ClientSession, queue: asyncio.Queue, progress_task: Optional[int]):
        while not queue.empty() and not self.is_cancelled:
            request_index = await queue.get()
            try:
                await self._make_request(session, request_index)
            except asyncio.CancelledError:
                self.is_cancelled = True
                break
            finally:
                if self._progress and progress_task is not None:
                    self._progress.update(progress_task, advance=1)
                queue.task_done()

    async def run(self):
        logger.info(f"Starting load test on {self.config.url} with {self.config.concurrent_users} concurrent users.")
        
        connector = aiohttp.TCPConnector(
            limit=self.config.concurrent_users,
            verify_ssl=self.config.ssl_verify,
            keepalive_timeout=60 if self.config.keep_alive else 0
        )
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        
        queue = asyncio.Queue()
        for i in range(self.config.total_requests):
            queue.put_nowait(i)

        self.metrics.start()
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                self._progress = progress
                progress_task = progress.add_task("[cyan]Sending requests...", total=self.config.total_requests)
                
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    workers = [
                        asyncio.create_task(self._worker(session, queue, progress_task))
                        for _ in range(self.config.concurrent_users)
                    ]
                    
                    await asyncio.gather(*workers)
                    
        except asyncio.CancelledError:
            logger.warning("Test cancelled by user (Ctrl+C). Generating partial report...")
            self.is_cancelled = True
        finally:
            self.metrics.stop()
            self._progress = None
