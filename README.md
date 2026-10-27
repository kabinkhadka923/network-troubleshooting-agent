# network-troubleshooting-agent

Local network troubleshooting agent for Huawei switches with inventory lookup, SSH-ready architecture, and evidence correlation groundwork.

This project is designed to:

- accept interface identifiers like `et-48.mkamaladi-sw4` and `gi-13.mchandragadi-dls-sw1`
- validate the hostname and interface format exactly as specified
- resolve the switch management IP from a local inventory CSV
- support a Huawei-first command profile with room for Juniper and Cisco later
- produce structured investigation reports
- remain safe by using read-only, allowlisted commands only

Quick start

1. Create a virtual environment and install dependencies:
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt

2. Resolve an interface:
   python -m network_agent.cli resolve gi-13.mchandragadi-dls-sw1

3. Run interactive mode:
   python -m network_agent.cli interactive

Example interface mappings

- `et-48.mkamaladi-sw4` -> hostname `mkamaladi-sw4`, physical interface `Ethernet 0/0/48`
- `gi-13.mchandragadi-dls-sw1` -> hostname `mchandragadi-dls-sw1`, physical interface `GigabitEthernet 0/0/13`

The project intentionally does not guess a management IP or vendor. It resolves both from a trusted inventory file.
