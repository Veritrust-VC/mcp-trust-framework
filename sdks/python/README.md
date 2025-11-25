# mcpf-client (Python SDK)

A minimal Python SDK for interacting with an **MCP Trust Registry** that implements the **MCP Trust Framework (MCPF)**.

This SDK helps you:

- Query MCP registry endpoints
- Retrieve registry entries by DID
- Search for MCP servers by metadata
- Perform basic validation of MCPServerCredentials (time window, assurance level)

> ⚠️ This SDK does **not** implement full cryptographic verification of Verifiable Credentials.  
> It focuses on structure and simple policy checks.

---

## Installation

For local development (inside this monorepo), you can install in editable mode:

```bash
cd sdks/python
pip install -e .
```

This will install the package as `mcpf_client`.

## Quick Start

```python
from mcpf_client import RegistryClient
from mcpf_client.verification import is_credential_valid_now, check_assurance_level
import requests

REGISTRY_URL = "http://localhost:8080"
SERVER_DID = "did:web:veritrust.vc:mcp:edgeguard-siem"

client = RegistryClient(base_url=REGISTRY_URL)

# 1. Get registry entry by DID
entry = client.get_server(SERVER_DID)
print("Registry entry:", entry)

# 2. Fetch MCPServerCredential (first URL in entry.credentials)
if not entry.credentials:
    raise RuntimeError("No credentials listed for this server.")
cred_url = entry.credentials[0]
credential = requests.get(cred_url, timeout=5).json()

# 3. Simple validity checks
if not is_credential_valid_now(credential):
    raise RuntimeError("Credential is not within its validity period.")

if not check_assurance_level(credential, minimum_level="verified"):
    raise RuntimeError("Credential assurance level is below required minimum.")

print("Credential is current and meets assurance requirements.")
```

## API Overview

### RegistryClient

```python
from mcpf_client import RegistryClient

client = RegistryClient(base_url="http://localhost:8080")

# List servers
page = client.list_servers(page=1, limit=50)

# Get server by DID
entry = client.get_server("did:web:example.com:mcp:myserver")

# Search servers
results = client.search_servers(capability="telemetry", tag="security")
```

### Verification helpers

Located in `mcpf_client.verification`:

- `is_credential_valid_now(credential: dict, now: datetime | None = None) -> bool`
- `check_assurance_level(credential: dict, minimum_level: str = "basic") -> bool`
- `validate_credential_structure(credential: dict, schema: dict) -> None` (uses `jsonschema` if installed, otherwise raises `ImportError`)

## Limitations

- Does not perform VC signature verification.
- Does not manage caching or complex trust policies.
- Intended as a simple building block for hosts/agents that want to integrate with an MCP Trust Registry.

For production use, you should:

- Implement full VC proof verification.
- Integrate your organization’s trust policies.
- Add caching and error handling around network calls.

