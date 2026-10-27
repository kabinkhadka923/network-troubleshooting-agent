import csv
import ipaddress
from pathlib import Path
from typing import Iterable

from .models import InventoryEntry


class InventoryManager:
    def __init__(self, inventory_path: str | Path):
        self.inventory_path = Path(inventory_path)
        self._entries = self._load_inventory()

    def _load_inventory(self) -> dict[str, InventoryEntry]:
        if not self.inventory_path.exists():
            raise FileNotFoundError(f"Inventory file not found: {self.inventory_path}")

        entries: dict[str, InventoryEntry] = {}
        with self.inventory_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            required_fields = {"hostname", "management_ip", "vendor", "os"}
            if not reader.fieldnames:
                raise ValueError("Inventory CSV is empty or missing a header row.")
            missing = required_fields - set(reader.fieldnames)
            if missing:
                raise ValueError(f"Inventory CSV is missing required columns: {sorted(missing)}")

            optional_fields = {"site", "interface", "paired_device", "paired_interface"}
            known_fields = set(reader.fieldnames)
            extra_fields = known_fields - required_fields - optional_fields
            # Keep extra fields ignored for safe compatibility with future inventory additions.

            for row_index, row in enumerate(reader, start=2):
                hostname = (row.get("hostname") or "").strip()
                if not hostname:
                    continue

                management_ip = (row.get("management_ip") or "").strip()
                vendor = (row.get("vendor") or "").strip()
                os_name = (row.get("os") or "").strip()
                site = (row.get("site") or "").strip()
                interface = (row.get("interface") or "").strip()
                paired_device = (row.get("paired_device") or "").strip()
                paired_interface = (row.get("paired_interface") or "").strip()

                try:
                    ipaddress.ip_address(management_ip)
                except ValueError as exc:
                    raise ValueError(f"Row {row_index}: invalid management_ip '{management_ip}'") from exc

                if hostname.lower() in entries:
                    raise ValueError(f"Duplicate hostname in inventory: {hostname}")

                entries[hostname.lower()] = InventoryEntry(
                    hostname=hostname,
                    management_ip=management_ip,
                    vendor=vendor,
                    os=os_name,
                    site=site,
                    interface=interface,
                    paired_device=paired_device,
                    paired_interface=paired_interface,
                )

        return entries

    def get_entry(self, hostname: str) -> InventoryEntry | None:
        return self._entries.get(hostname.lower())

    def list_entries(self) -> Iterable[InventoryEntry]:
        return self._entries.values()
