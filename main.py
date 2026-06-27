import sys
import asyncio
from rich.console import Console

from pyload.cli import parse_args
from pyload.logger import setup_logger
from pyload.engine import PyLoadEngine
from pyload.metrics import MetricsCollector
from pyload.reporter import Reporter
from pyload.utils import is_valid_url

def main():
    console = Console()
    
    try:
        config = parse_args()
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        sys.exit(1)

    if not is_valid_url(config.url):
        console.print(f"[bold red]Error:[/bold red] Invalid URL provided: {config.url}")
        sys.exit(1)

    logger = setup_logger(debug=config.debug)
    
    # Print welcome banner
    console.print("[bold blue]PyLoad - High Performance HTTP Load Tester[/bold blue]")
    console.print(f"Target: [cyan]{config.url}[/cyan] ({config.method})")
    console.print(f"Concurrency: {config.concurrent_users} | Total Requests: {config.total_requests}")
    console.print("-" * 50)

    metrics = MetricsCollector()
    engine = PyLoadEngine(config=config, metrics=metrics)

    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        asyncio.run(engine.run())
        
        metrics_data = metrics.calculate()
        reporter = Reporter(metrics_data, config.output_dir)
        reporter.generate_all()
        
    except KeyboardInterrupt:
        # Graceful exit already handled in engine, but just in case
        console.print("\n[bold yellow]Forced Exit by User[/bold yellow]")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Fatal error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
