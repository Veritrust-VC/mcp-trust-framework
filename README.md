![Status](https://img.shields.io/badge/status-draft-blue)
![Spec](https://img.shields.io/badge/MCPF-1.0--draft-important)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/sdk-python-blue)
![TypeScript](https://img.shields.io/badge/sdk-typescript-blueviolet)
![FastAPI](https://img.shields.io/badge/registry-FastAPI-009688)

# MCP Trust Framework (MCPF)

The **Model Context Protocol (MCP)** defines how AI agents and hosts call external tools and data sources.  
However, MCP does **not** define:

- How to **identify** MCP servers and agents
- How to **discover** available MCP servers
- How to **express trust, provenance, and assurance**
- How to **govern** which MCP servers a host may safely use

The **MCP Trust Framework (MCPF)** fills this gap.

It provides:

- A **specification** for MCP identity and trust (`specs/`)
- A **reference registry implementation** (`registry-reference-implementation/`)
- **Client SDKs** for Python and Node.js (`sdks/`)
- **Examples** of registry entries, credentials, and DID documents (`examples/`)
- **Governance** and roadmap documents (`governance/`)

MCPF is compatible with any existing MCP server or host. It does not change the MCP protocol; it adds a **trust and discovery layer** on top.


## Repository Structure

- `specs/`  
  Core specifications, JSON schemas, and security considerations for MCPF.

- `examples/`  
  Example registry entries, MCP server credentials, DID documents, and verification guides.

- `registry-reference-implementation/`  
  A minimal MCP Trust Registry implemented with FastAPI (Python).

- `sdks/python/`  
  Python client SDK for querying and verifying MCP registry entries.

- `sdks/node/`  
  Node.js/TypeScript client SDK for querying and verifying MCP registry entries.

- `governance/`  
  Versioning, roadmap, and contributor guidelines at the framework level.


## Quick Start

1. **Read the spec**

   See [`specs/MCPF-1.0.md`](specs/MCPF-1.0.md) for the core MCP Trust Framework definition.

2. **Run the reference registry**

   See [`registry-reference-implementation/README.md`](registry-reference-implementation/README.md) for instructions to run a local MCP Trust Registry.

3. **Use an SDK**

   - Python: [`sdks/python/`](sdks/python/)
   - Node.js: [`sdks/node/`](sdks/node/)

4. **Explore examples**

   See [`examples/`](examples/) for sample registry entries, MCP server credentials, and DID documents.


## .well-known discovery

A registry operator can expose discovery metadata at:

```text
https://<domain>/.well-known/mcp-trust-registry.json
```

An example structure is:

```json
{
  "mcpfVersion": "1.0",
  "registry": {
    "name": "Veritrust MCP Trust Registry",
    "baseUrl": "https://ans.veritrust.vc/mcp"
  },
  "issuer": {
    "did": "did:web:veritrust.vc",
    "name": "Veritrust"
  }
}
```

Clients can fetch this file first and use `registry.baseUrl` to configure a `RegistryClient`.


## Status

- Specification: **Draft 1.0**
- Reference implementation: **MVP**
- SDKs: **MVP**

This project is intended to be open, interoperable, and suitable for enterprise deployment.


## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
