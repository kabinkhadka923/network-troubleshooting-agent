import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from .models import InvestigationReport


def generate_report_summary(report: InvestigationReport) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "interface_identifier": report.interface_identifier,
        "hostname": report.hostname,
        "management_ip": report.management_ip,
        "vendor": report.vendor,
        "os": report.os,
        "physical_interface": report.physical_interface,
        "status": report.status,
        "findings": report.findings,
    }


def write_text_report(report: InvestigationReport, output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = output_path / f"{report.hostname}-{timestamp}.txt"

    lines = [
        "Network Troubleshooting Investigation",
        f"Timestamp: {datetime.now(timezone.utc).isoformat()}",
        f"Interface: {report.interface_identifier}",
        f"Hostname: {report.hostname}",
        f"Management IP: {report.management_ip}",
        f"Vendor: {report.vendor}",
        f"OS: {report.os}",
        f"Physical interface: {report.physical_interface}",
        "",
        "Findings:",
    ]
    if report.findings:
        for finding in report.findings:
            lines.append(f"- {finding.get('title')}: {finding.get('status')} :: {finding.get('details')}")
    else:
        lines.append("- No findings captured.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_json_report(report: InvestigationReport, output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = output_path / f"{report.hostname}-{timestamp}.json"

    payload = generate_report_summary(report)
    payload["command_results"] = [
        {
            "command": item.command,
            "success": item.success,
            "stdout": item.stdout,
            "stderr": item.stderr,
            "error": item.error,
        }
        for item in report.command_results
    ]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_csv_report(report: InvestigationReport, output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = output_path / f"{report.hostname}-{timestamp}.csv"

    rows = report.findings
    if rows:
        fieldnames = sorted({key for row in rows for key in row.keys()})
    else:
        fieldnames = ["title", "status", "details"]

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return path
