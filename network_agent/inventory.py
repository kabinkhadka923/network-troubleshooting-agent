import argparse
from pathlib import Path

from .huawei_profile import command_is_allowed
from .interface_parser import parse_interface_identifier
from .inventory import InventoryManager
from .models import CommandResult, InvestigationReport
from .reporting import write_csv_report, write_json_report, write_text_report

DEFAULT_INVENTORY_PATH = Path(__file__).resolve().parent.parent / "data" / "inventory.csv"
DEFAULT_REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"


def resolve_interface(interface_identifier: str, inventory_path: str | Path = DEFAULT_INVENTORY_PATH) -> InvestigationReport:
    prefix, port, hostname, physical_interface = parse_interface_identifier(interface_identifier)
    inventory = InventoryManager(inventory_path)
    matched = inventory.get_entry(hostname)
    if not matched:
        raise ValueError(f"Hostname '{hostname}' not found in inventory.")

    commands = [
        f"display interface {physical_interface}",
        "display mac-address",
        "display vlan",
        "display arp",
        "display ip interface brief",
    ]

    for command in commands:
        if not command_is_allowed(command):
            raise ValueError(f"Command is not in the approved Huawei allowlist: {command}")

    findings = [
        {
            "title": "Inventory resolution",
            "status": "Confirmed",
            "details": f"Resolved {hostname} to management IP {matched.management_ip} using the local inventory.",
        },
        {
            "title": "Interface parsing",
            "status": "Confirmed",
            "details": f"Parsed {interface_identifier} into prefix {prefix}, port {port}, and physical interface {physical_interface}.",
        },
        {
            "title": "Huawei command allowlist",
            "status": "Confirmed",
            "details": "Only read-only Huawei commands are allowed in the first implementation.",
        },
    ]

    command_results = [
        CommandResult(command=commands[0], success=True, stdout="Sample read-only output captured for Huawei interfaces.", stderr=""),
        CommandResult(command=commands[1], success=True, stdout="Sample MAC table captured for correlation.", stderr=""),
        CommandResult(command=commands[2], success=True, stdout="Sample VLAN table captured for correlation.", stderr=""),
    ]

    report = InvestigationReport(
        interface_identifier=interface_identifier,
        hostname=matched.hostname,
        management_ip=matched.management_ip,
        vendor=matched.vendor,
        os=matched.os,
        physical_interface=physical_interface,
        findings=findings,
        command_results=command_results,
        status="ready",
    )

    text_path = write_text_report(report, DEFAULT_REPORT_DIR)
    json_path = write_json_report(report, DEFAULT_REPORT_DIR)
    csv_path = write_csv_report(report, DEFAULT_REPORT_DIR)
    report.report_path = str(text_path)
    report.status = "report_generated"

    print(f"Resolved hostname: {report.hostname}")
    print(f"Management IP: {report.management_ip}")
    print(f"Vendor: {report.vendor}")
    print(f"OS: {report.os}")
    print(f"Physical interface: {report.physical_interface}")
    print(f"TXT report: {text_path}")
    print(f"JSON report: {json_path}")
    print(f"CSV report: {csv_path}")
    return report


def interactive_mode(inventory_path: str | Path = DEFAULT_INVENTORY_PATH) -> None:
    print("Network troubleshooting agent - interactive mode")
    print("Type 'quit' to exit.")
    while True:
        value = input("Interface identifier: ").strip()
        if value.lower() in {"quit", "exit", "q"}:
            print("Goodbye.")
            break
        try:
            resolve_interface(value, inventory_path)
        except ValueError as exc:
            print(f"Error: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Huawei-first network troubleshooting agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve", help="Resolve a single interface identifier")
    resolve_parser.add_argument("interface_identifier")

    interactive_parser = subparsers.add_parser("interactive", help="Run interactive mode")
    _ = interactive_parser
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "resolve":
        resolve_interface(args.interface_identifier)
    elif args.command == "interactive":
        interactive_mode()


if __name__ == "__main__":
    main()
