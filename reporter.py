import json
import csv
from pathlib import Path
from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .logger import logger

class Reporter:
    def __init__(self, metrics_data: Dict[str, Any], output_dir: str):
        self.data = metrics_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.console = Console()

    def generate_json(self):
        file_path = self.output_dir / "report.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            logger.info(f"JSON report generated: {file_path}")
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")

    def generate_csv(self):
        file_path = self.output_dir / "report.csv"
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Metric", "Value"])
                writer.writerow(["Total Execution Time (s)", self.data["execution_time_sec"]])
                writer.writerow(["Total Requests", self.data["total_requests"]])
                writer.writerow(["Successful Requests", self.data["successful_requests"]])
                writer.writerow(["Failed Requests", self.data["failed_requests"]])
                writer.writerow(["Requests / sec", self.data["requests_per_sec"]])
                writer.writerow(["Error %", self.data["error_percentage"]])
                
                lat = self.data.get("latency", {})
                for k, v in lat.items():
                    writer.writerow([f"Latency {k.upper()}", v])
                
            logger.info(f"CSV report generated: {file_path}")
        except Exception as e:
            logger.error(f"Failed to generate CSV report: {e}")

    def generate_txt(self):
        file_path = self.output_dir / "summary.txt"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("PyLoad Load Test Summary\n")
                f.write("========================\n\n")
                f.write(f"Total Execution Time (s): {self.data['execution_time_sec']}\n")
                f.write(f"Total Requests: {self.data['total_requests']}\n")
                f.write(f"Successful Requests: {self.data['successful_requests']}\n")
                f.write(f"Failed Requests: {self.data['failed_requests']}\n")
                f.write(f"Requests / sec: {self.data['requests_per_sec']}\n")
                f.write(f"Error %: {self.data['error_percentage']}\n\n")
                
                f.write("Latency Distribution:\n")
                lat = self.data.get("latency", {})
                for k, v in lat.items():
                    f.write(f"  {k.upper()}: {v}s\n")
                    
                f.write("\nStatus Codes:\n")
                for k, v in self.data.get("status_codes", {}).items():
                    f.write(f"  {k}: {v}\n")
                    
                if self.data.get("errors"):
                    f.write("\nErrors:\n")
                    for k, v in self.data["errors"].items():
                        f.write(f"  {k}: {v}\n")
            logger.info(f"TXT report generated: {file_path}")
        except Exception as e:
            logger.error(f"Failed to generate TXT report: {e}")

    def print_summary(self):
        table = Table(title="PyLoad Metrics Summary")
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Execution Time", f"{self.data['execution_time_sec']}s")
        table.add_row("Total Requests", str(self.data['total_requests']))
        table.add_row("Successful Requests", f"[green]{self.data['successful_requests']}[/green]")
        table.add_row("Failed Requests", f"[red]{self.data['failed_requests']}[/red]")
        table.add_row("Req/Sec", str(self.data['requests_per_sec']))
        table.add_row("Error Rate", f"{self.data['error_percentage']}%")
        
        lat = self.data.get("latency", {})
        table.add_row("Latency Min", f"{lat.get('min', 0)}s")
        table.add_row("Latency Max", f"{lat.get('max', 0)}s")
        table.add_row("Latency Avg", f"{lat.get('avg', 0)}s")
        table.add_row("Latency Median", f"{lat.get('median', 0)}s")
        table.add_row("Latency P95", f"{lat.get('p95', 0)}s")
        table.add_row("Latency P99", f"{lat.get('p99', 0)}s")

        self.console.print(Panel(table, title="[bold]Test Completed[/bold]", expand=False))

    def generate_all(self):
        self.generate_json()
        self.generate_csv()
        self.generate_txt()
        self.print_summary()
