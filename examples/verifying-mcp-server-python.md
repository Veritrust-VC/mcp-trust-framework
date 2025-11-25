# Verifying an MCP Server with the MCP Trust Registry (Python)

This guide shows how a Python host or agent can:

1. Query an MCP Trust Registry for a server by DID
2. Fetch its MCPServerCredential
3. Validate the credential structure
4. Perform basic validity checks (time window, assurance level)

> Note: This example does **not** perform real cryptographic signature verification.  
> That is left as an exercise for production environments.

---

## 1. Setup

Install dependencies (using `pip`):

```bash
pip install requests jsonschema
```

Assume the registry is running at:

```
https://registry.example.com
```

and the MCP server DID is:

```
did:web:veritrust.vc:mcp:edgeguard-siem
```

## 2. Fetch Registry Entry

```python
import requests

REGISTRY_BASE_URL = "https://registry.example.com"
SERVER_DID = "did:web:veritrust.vc:mcp:edgeguard-siem"


def fetch_registry_entry(did: str) -> dict:
    url = f"{REGISTRY_BASE_URL}/mcp/servers/{did}"
    resp = requests.get(url, timeout=5)
    if resp.status_code == 404:
        raise ValueError(f"No registry entry found for DID {did}")
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    entry = fetch_registry_entry(SERVER_DID)
    print("Registry entry:")
    print(entry)
```

## 3. Fetch MCPServerCredential

The registry entry contains a credentials array with URLs to credentials.

```python
def fetch_credential(entry: dict) -> dict:
    creds = entry.get("credentials") or []
    if not creds:
        raise ValueError("Registry entry has no 'credentials' URLs")

    # Use the first credential URL for this example
    cred_url = creds[0]
    resp = requests.get(cred_url, timeout=5)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    entry = fetch_registry_entry(SERVER_DID)
    credential = fetch_credential(entry)
    print("Credential:")
    print(credential)
```

## 4. Validate Credential Structure with JSON Schema

Use the credential-schema.json from specs/ to validate basic structure.

```python
import json
from jsonschema import Draft202012Validator
from pathlib import Path


def load_schema() -> dict:
    schema_path = Path(__file__).resolve().parent.parent / "specs" / "credential-schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_credential_structure(credential: dict, schema: dict) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(credential), key=lambda e: e.path)
    if errors:
        msg = "\n".join(f"- {'/'.join(map(str, err.path))}: {err.message}" for err in errors)
        raise ValueError(f"Credential does not conform to schema:\n{msg}")


if __name__ == "__main__":
    entry = fetch_registry_entry(SERVER_DID)
    credential = fetch_credential(entry)
    schema = load_schema()
    validate_credential_structure(credential, schema)
    print("Credential structure is valid according to schema.")
```

## 5. Basic Validity Checks (Time Window, Assurance Level)

```python
from datetime import datetime, timezone


def parse_iso8601(dt_str: str) -> datetime:
    # Minimal parser assuming 'Z' or full offset
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00")).astimezone(timezone.utc)


def is_credential_valid_now(credential: dict, now: datetime | None = None) -> bool:
    if now is None:
        now = datetime.now(timezone.utc)

    issued_at = parse_iso8601(credential["issuedAt"])
    valid_until = parse_iso8601(credential["validUntil"])

    return issued_at <= now <= valid_until


def check_assurance_level(credential: dict, minimum_level: str = "basic") -> bool:
    levels = ["basic", "verified", "certified"]
    min_index = levels.index(minimum_level)

    subject = credential.get("credentialSubject", {})
    level = subject.get("assuranceLevel", "basic")
    try:
        level_index = levels.index(level)
    except ValueError:
        return False

    return level_index >= min_index


if __name__ == "__main__":
    entry = fetch_registry_entry(SERVER_DID)
    credential = fetch_credential(entry)
    schema = load_schema()
    validate_credential_structure(credential, schema)

    now = datetime.now(timezone.utc)

    if not is_credential_valid_now(credential, now):
        raise ValueError("Credential is not within its validity period.")

    if not check_assurance_level(credential, minimum_level="verified"):
        raise ValueError("Credential assurance level is below required minimum.")

    print("Credential is structurally valid, current, and meets assurance requirements.")
```

## 6. Next Steps

In a production implementation, you SHOULD:

- Implement full cryptographic proof verification.
- Enforce your organization’s trust policy (allowed issuers, DID methods, countries, etc.).
- Add caching for registry responses and credentials.
- Integrate with actual MCP host logic to decide whether to enable the server as a tool.
