# MCP Trust Registry API (MCPF)

This document defines a simple HTTP/JSON API for an **MCP Trust Registry** compatible with the MCP Trust Framework (MCPF).

The API is intentionally minimal, easy to implement, and suitable for both:

- Public registries (global trust authorities)
- Private registries (enterprise internal catalogs)

Base URL is implementation-specific. In examples below, we assume:

```text
https://registry.example.com
```

All responses are JSON and use standard HTTP status codes.

---

## 1. Data Model Overview

A Registry Entry represents one MCP server and has the structure:

```json
{
  "did": "did:web:example.com:mcp:myserver",
  "endpoint": "https://myserver.example.com/mcp",
  "manifest": "https://myserver.example.com/mcp/manifest.json",
  "credentials": [
    "https://registry.example.com/vc/myserver.json"
  ],
  "metadata": {
    "capabilities": ["telemetry", "alerts"],
    "organization": "Example Corp",
    "country": "US",
    "tags": ["security", "energy"],
    "status": "active"
  }
}
```

---

## 2. Endpoints

### 2.1. GET /mcp/servers

List all MCP servers known to the registry, optionally with pagination.

**Request:**

```
GET /mcp/servers?page=1&limit=50
```

**Query Parameters:**

- `page` – optional, default 1
- `limit` – optional, default 50, maximum implementation-defined

**Response 200:**

```json
{
  "page": 1,
  "limit": 50,
  "total": 1,
  "items": [
    {
      "did": "did:web:example.com:mcp:myserver",
      "endpoint": "https://myserver.example.com/mcp",
      "manifest": "https://myserver.example.com/mcp/manifest.json",
      "credentials": [
        "https://registry.example.com/vc/myserver.json"
      ],
      "metadata": {
        "capabilities": ["telemetry", "alerts"],
        "organization": "Example Corp",
        "country": "US",
        "tags": ["security", "energy"],
        "status": "active"
      }
    }
  ]
}
```

### 2.2. GET /mcp/servers/{did}

Retrieve a single registry entry by DID.

**Request:**

```
GET /mcp/servers/did:web:example.com:mcp:myserver
```

**Response 200:**

```json
{
  "did": "did:web:example.com:mcp:myserver",
  "endpoint": "https://myserver.example.com/mcp",
  "manifest": "https://myserver.example.com/mcp/manifest.json",
  "credentials": [
    "https://registry.example.com/vc/myserver.json"
  ],
  "metadata": {
    "capabilities": ["telemetry", "alerts"],
    "organization": "Example Corp",
    "country": "US",
    "tags": ["security", "energy"],
    "status": "active"
  }
}
```

**Response 404:**

```json
{
  "error": "not_found",
  "message": "No registry entry found for DID did:web:example.com:mcp:unknown"
}
```

### 2.3. GET /mcp/search

Search for MCP servers using simple filters.

**Request:**

```
GET /mcp/search?capability=telemetry&tag=security&assuranceLevel=verified
```

**Supported Query Parameters (all optional):**

- `capability` – string, match entries where `metadata.capabilities` contains this value.
- `tag` – string, match entries where `metadata.tags` contains this value.
- `organization` – string, match `metadata.organization` (case-insensitive).
- `country` – string, match `metadata.country`.
- `assuranceLevel` – string, filter by minimum assurance. Interpretation is registry-specific.
- `issuer` – string, filter by credential issuer DID (if registry maintains such index).

**Response 200:**

```json
{
  "items": [
    {
      "did": "did:web:example.com:mcp:myserver",
      "endpoint": "https://myserver.example.com/mcp",
      "manifest": "https://myserver.example.com/mcp/manifest.json",
      "credentials": [
        "https://registry.example.com/vc/myserver.json"
      ],
      "metadata": {
        "capabilities": ["telemetry", "alerts"],
        "organization": "Example Corp",
        "country": "US",
        "tags": ["security", "energy"],
        "status": "active"
      }
    }
  ]
}
```

### 2.4. POST /mcp/servers

Register or update a registry entry.

> Note: Authentication and authorization are implementation-specific. For an MVP, this may be open or protected by an API key; in production, stronger auth is recommended.

**Request:**

```
POST /mcp/servers
Content-Type: application/json

{
  "did": "did:web:example.com:mcp:myserver",
  "endpoint": "https://myserver.example.com/mcp",
  "manifest": "https://myserver.example.com/mcp/manifest.json",
  "credentials": [
    "https://registry.example.com/vc/myserver.json"
  ],
  "metadata": {
    "capabilities": ["telemetry", "alerts"],
    "organization": "Example Corp",
    "country": "US",
    "tags": ["security", "energy"],
    "status": "active"
  }
}
```

**Response 201 (created) or 200 (updated):**

```json
{
  "status": "ok",
  "did": "did:web:example.com:mcp:myserver"
}
```

**Response 400:**

```json
{
  "error": "invalid_entry",
  "message": "Missing required field 'did'."
}
```

### 2.5. GET /mcp/issuers

List recognized issuers (trust authorities) for credentials.

**Request:**

```
GET /mcp/issuers
```

**Response 200:**

```json
{
  "issuers": [
    {
      "id": "did:web:veritrust.vc",
      "name": "Veritrust",
      "documentation": "https://veritrust.vc/mcp-trust-framework"
    }
  ]
}
```

### 2.6. GET /mcp/revocations

Return a lightweight view of revoked MCP servers or credentials.

**Request:**

```
GET /mcp/revocations
```

**Response 200:**

```json
{
  "revokedServers": [
    {
      "did": "did:web:example.com:mcp:old-server",
      "revokedAt": "2025-10-01T12:00:00Z",
      "reason": "compromised_keys"
    }
  ],
  "revokedCredentials": [
    {
      "id": "https://registry.example.com/vc/old-credential.json",
      "revokedAt": "2025-10-01T12:00:00Z",
      "reason": "superseded"
    }
  ]
}
```

Implementations MAY provide more detailed partitioned revocation endpoints (e.g., `/mcp/revocations/servers`, `/mcp/revocations/credentials`) if needed.

---

## 3. Error Handling

Errors SHOULD use structured JSON:

```json
{
  "error": "string_code",
  "message": "Human-readable explanation"
}
```

Common error codes:

- `invalid_request`
- `not_found`
- `invalid_entry`
- `unauthorized`
- `internal_error`

---

## 4. Authentication and Authorization

The specification does not mandate a specific auth mechanism. Possible choices include:

- No auth (for public read-only endpoints)
- API keys
- OAuth 2.0 / OpenID Connect
- mTLS with client certificates

A common pattern:

- `GET` endpoints are public for read operations.
- `POST` (and any future mutation endpoints) require authenticated access.

---

## 5. Extensibility

Registries MAY add additional endpoints, fields, or indexes as long as:

- Core fields in this spec remain stable.
- Additional fields do not break clients that only rely on the core model.

Any extensions are clearly documented.

MCPF registry clients SHOULD ignore unknown fields.

---

## 6. Security Considerations

See `security-considerations.md` for general security guidance that also applies to registry implementations.
