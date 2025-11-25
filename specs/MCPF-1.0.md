# MCP Trust Framework (MCPF) – Version 1.0 (Draft)

**Status:** Public Draft  
**Maintainer:** Veritrust  
**Applies to:** Any MCP server and host implementation

---

## 1. Introduction

The **Model Context Protocol (MCP)** enables AI agents and hosts to interact with external tools and data sources in a structured way. MCP defines *how* tools are described and invoked.

However, MCP does **not** define:

- How to **identify** MCP servers and agents
- How to **discover** available MCP servers
- How to **express trust, provenance, and assurance** about MCP servers
- How to **apply policies** about which MCP servers a host is permitted to use

The **MCP Trust Framework (MCPF)** fills this gap by specifying:

- An **identity model** for MCP servers and agents based on Decentralized Identifiers (DIDs)
- A **verifiable credential** model for expressing trust and provenance
- A **registry model and API** for discovering MCP servers
- A **verification flow** for hosts before invoking MCP servers
- A **policy model** to decide whether a server is trusted enough to use

MCPF is compatible with existing MCP implementations and is transport- and vendor-agnostic.

---

## 2. Scope

MCPF:

- DOES NOT modify the MCP protocol or wire format.
- DOES define:
  - How MCP servers and agents identify themselves.
  - How registries can publish and expose trusted MCP servers.
  - How hosts can verify identity and trust information before invocation.
- Applies to:
  - Public MCP servers on the internet
  - Private/enterprise MCP deployments
  - Hybrid setups across organizational boundaries

---

## 3. Terminology

- **MCP Server**  \
  A tool or service that implements the Model Context Protocol and exposes capabilities to hosts/agents.

- **Host / Agent**  \
  An AI agent, application, or host runtime that initiates MCP calls to MCP servers.

- **Registry**  \
  A service that maintains a directory of MCP servers, indexed by decentralized identifiers (DIDs) and associated metadata and credentials.

- **DID (Decentralized Identifier)**  \
  A persistent identifier that can be resolved to a DID Document describing public keys and service endpoints. See W3C DID Core.

- **VC (Verifiable Credential)**  \
  A tamper-evident credential expressing claims about a subject, signed by an issuer. See W3C Verifiable Credentials.

- **Issuer**  \
  An entity that signs verifiable credentials (e.g., a trust authority such as Veritrust).

- **Trust Policy**  \
  A set of local rules that determine which MCP servers are acceptable to a given host or organization, based on DIDs, issuers, capabilities, and assurance levels.

- **Assurance Level**  \
  A coarse-grained indicator of how thoroughly an MCP server has been evaluated, e.g. `basic`, `verified`, `certified`.

---

## 4. Identity Model

Every MCP server that participates in MCPF SHOULD have a stable **DID** as its primary identifier.

Example using `did:web`:

```text
did:web:veritrust.vc:mcp:edgeguard-siem
```

### 4.1. DID Document

The DID MUST resolve to a DID Document that:

- Contains at least one `verificationMethod` with a public key used to sign credentials or metadata.
- Declares assertion methods (e.g., which keys can sign VCs).
- May include service entries referencing:
  - The MCP server endpoint
  - A registry entry URL
  - Documentation URLs

See `did-profile.md` for concrete recommendations and examples.

---

## 5. MCPServerCredential

MCPF defines a standard Verifiable Credential type called `MCPServerCredential`.

This credential expresses information about an MCP Server, such as:

- Its DID
- The organization operating it
- The primary MCP endpoint
- A URL to its MCP manifest
- Its capabilities
- An assurance level
- Validity period

### 5.1. Required Fields

An `MCPServerCredential` MUST include:

- `@context` – MUST include the W3C VC context and the MCP-specific context.
- `type` – MUST include `"VerifiableCredential"` and `"MCPServerCredential"`.
- `issuer` – Identifier (e.g., DID) of the issuer.
- `issuedAt` – Time the credential was issued (ISO 8601).
- `validUntil` – Time the credential expires (ISO 8601).
- `credentialSubject` – Object containing:
  - `id` (DID of the MCP server)
  - `operator` (string, organization name)
  - `endpoint` (URI for the MCP endpoint)
  - `manifest` (URI for MCP manifest JSON)
  - `capabilities` (array of strings)
  - `assuranceLevel` (one of: `basic`, `verified`, `certified`)

The full JSON Schema is defined in `credential-schema.json`.

---

## 6. Registry Model

A registry is a service that indexes MCP servers by DID, along with metadata and verifiable credentials.

A registry entry SHOULD at minimum contain:

- The server’s DID
- An endpoint URL
- A manifest URL
- A list of credentials (or credential URLs)
- Metadata describing capabilities and organizational context

Example structure:

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

The Registry API is described in detail in `registry-api.md`.

Registries MAY be:

- Publicly accessible (e.g., a global trust authority)
- Restricted to an organization (private enterprise registry)
- Federated (multiple registries with cross-references)

---

## 7. Verification Flow

Before a host invokes an MCP server under MCPF, it SHOULD perform the following steps:

1. **Resolve DID** – Obtain the DID Document for the MCP server’s DID.
2. **Validate DID Document**
   - Check structure and syntax.
   - Extract verification methods and service endpoints.
3. **Fetch Registry Entry** (optional but recommended) – Query a registry to retrieve metadata and credential references for the DID.
4. **Obtain MCPServerCredential** – Either from the registry or directly from the MCP server.
5. **Validate against the JSON Schema.**
6. **Verify Credential**
   - Check that the credential is issued by a trusted issuer.
   - Validate digital signature (implementation-specific).
   - Ensure `issuedAt` and `validUntil` are within acceptable range.
7. **Check Revocation** – Consult registry or issuer revocation lists or status endpoints.
8. **Apply Local Trust Policy** – Evaluate whether:
   - Issuer is allowed.
   - `assuranceLevel` meets minimum requirements.
   - Capabilities are acceptable.
   - Other metadata (country, tags, etc.) matches organizational policy.
9. **Fetch and Validate Manifest** – Retrieve MCP manifest from the URL in credential or registry. Optionally check hash/integrity if available.
10. **Establish TLS Connection** – Connect to the MCP endpoint using HTTPS. Validate TLS certificate as usual.

Only after these steps does the host proceed to use the MCP server in the normal MCP call flow.

---

## 8. Trust Policies

Each organization or host MAY define its own trust policy, for example:

- Only accept MCP servers with:
  - `assuranceLevel >= "verified"`
  - `issuer` in an approved list of trust authorities
  - capabilities restricted to a defined set
  - `country` not in a blocked list
- Reject or warn on:
  - Expired credentials
  - Revoked credentials
  - Unknown issuers

Trust policies are not standardized by MCPF; they are local configuration. MCPF only defines the information model to support such policies.

---

## 9. Registry Discovery

Trust authorities and registries MAY expose a `.well-known` document to advertise registry metadata.

Example:

```
GET https://veritrust.vc/.well-known/mcp-trust-registry.json
```

This document can contain:

- Registry base URL
- Issuer DID
- Public key references
- Documentation URLs
- Framework version supported

A sample structure is provided in the root README and examples.

---

## 10. Compatibility and Extensibility

MCPF is orthogonal to MCP versions. It can be used with any MCP-compliant server.

New credential types MAY be added in future versions (e.g., `MCPAgentCredential`).

Future DID methods MAY be adopted in addition to `did:web`.

Backward-compatible extensions SHOULD:

- Reuse existing fields where possible.
- Use additional fields under clearly namespaced keys.

---

## 11. Versioning

MCPF uses semantic versioning:

- **MAJOR** – breaking changes in the information model or required fields.
- **MINOR** – new optional fields or capabilities that are backward compatible.
- **PATCH** – corrections, clarifications, and documentation updates.

The version of this document is **1.0 (Draft)**.

---

## 12. References

- W3C Decentralized Identifiers (DIDs)
- W3C Verifiable Credentials Data Model
- Model Context Protocol (MCP) – official specification (vendor link)
- This repository’s:
  - `registry-api.md`
  - `credential-schema.json`
  - `did-profile.md`
  - `security-considerations.md`

---
