from __future__ import annotations

from pathlib import Path

ALLOWED_COMMANDS = [
    "display interface {interface_name}",
    "display mac-address",
    "display vlan",
    "display arp",
    "display ip interface brief",
    "display version",
]


def build_allowed_commands(interface_name: str) -> list[str]:
    return [command.format(interface_name=interface_name) for command in ALLOWED_COMMANDS]


def command_is_allowed(command: str) -> bool:
    cmd = command.strip()
    allowed_prefixes = (
        "display interface",
        "display mac-address",
        "display vlan",
        "display arp",
        "display ip interface brief",
        "display version",
    )
    return cmd.startswith(allowed_prefixes)


def write_huawei_profile(path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "# Huawei read-only allowlist\n"
        + "\n".join(build_allowed_commands("GigabitEthernet 0/0/13"))
        + "\n",
        encoding="utf-8",
    )
