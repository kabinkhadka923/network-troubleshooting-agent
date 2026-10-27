from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class InventoryEntry:
    hostname: str
    management_ip: str
    vendor: str
    os: str
    site: str = ""
    interface: str = ""
    paired_device: str = ""
    paired_interface: str = ""


@dataclass(frozen=True)
class InterfaceRequest:
    raw_identifier: str
    prefix: str
    port: int
    hostname: str
    physical_interface: str


@dataclass(frozen=True)
class InspectionTarget:
    hostname: str
    management_ip: str
    vendor: str
    os: str
    physical_interface: str


@dataclass
class CommandResult:
    command: str
    stdout: str = ""
    stderr: str = ""
    success: bool = True
    error: str | None = None


@dataclass
class EvidenceRecord:
    evidence_type: str
    value: str
    status: str = "Confirmed"
    source: str = ""
    notes: str = ""


@dataclass
class InvestigationReport:
    interface_identifier: str
    hostname: str
    management_ip: str
    vendor: str
    os: str
    physical_interface: str
    findings: list[dict[str, Any]] = field(default_factory=list)
    command_results: list[CommandResult] = field(default_factory=list)
    report_path: str | None = None
    status: str = "pending"
