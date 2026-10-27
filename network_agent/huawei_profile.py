import re

VALID_PREFIXES = {
    "et": "Ethernet",
    "gi": "GigabitEthernet",
}


def parse_interface_identifier(raw_identifier: str) -> tuple[str, int, str, str]:
    if not raw_identifier or not isinstance(raw_identifier, str):
        raise ValueError("Interface identifier is required.")

    normalized = raw_identifier.strip()
    match = re.fullmatch(r"(?P<prefix>et|gi)-(?P<port>\d+)\.(?P<hostname>[A-Za-z0-9.-]+)", normalized, re.IGNORECASE)
    if not match:
        raise ValueError("Invalid interface format. Expected et-N.hostname or gi-N.hostname")

    prefix = match.group("prefix").lower()
    port = int(match.group("port"))
    hostname = match.group("hostname").lower()

    if port < 1:
        raise ValueError("Port number must be greater than zero.")

    physical_interface = f"{VALID_PREFIXES[prefix]} 0/0/{port}"
    return prefix, port, hostname, physical_interface
