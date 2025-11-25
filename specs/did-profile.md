# DID Profile for MCP Trust Framework

This document describes recommendations for using Decentralized Identifiers (DIDs) within the MCP Trust Framework (MCPF).

MCPF is DID-method agnostic, but early implementations are expected to use `did:web` due to simplicity and compatibility with existing web PKI.

---

## 1. DID Method Recommendation

### 1.1. `did:web`

For initial deployments, MCP servers SHOULD use `did:web` because:

- It can be hosted on existing HTTPS domains.
- It leverages established DNS and TLS infrastructure.
- It is easy to deploy for organizations already managing web resources.

Example:

```text
did:web:veritrust.vc:mcp:edgeguard-siem
```

The corresponding DID Document would be served from a URL derived from the DID method specification.

---

## 2. DID Document Structure

A typical DID Document for an MCP server might include:

- One or more `verificationMethod` entries with the server’s public keys.
- An `assertionMethod` referencing which keys can be used for VCs.
- `service` entries describing MCP-related endpoints.

Example (simplified):

```json
{
  "@context": ["https://www.w3.org/ns/did/v1"],
  "id": "did:web:veritrust.vc:mcp:edgeguard-siem",
  "verificationMethod": [
    {
      "id": "did:web:veritrust.vc:mcp:edgeguard-siem#key-1",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:web:veritrust.vc:mcp:edgeguard-siem",
      "publicKeyMultibase": "zABCDEFG1234567890"
    }
  ],
  "assertionMethod": [
    "did:web:veritrust.vc:mcp:edgeguard-siem#key-1"
  ],
  "service": [
    {
      "id": "#mcp-endpoint",
      "type": "MCPServerEndpoint",
      "serviceEndpoint": "https://edgeguard.cyberfort.lv/mcp"
    },
    {
      "id": "#mcp-registry-entry",
      "type": "MCPRegistryEntry",
      "serviceEndpoint": "https://ans.veritrust.vc/mcp/servers/did:web:veritrust.vc:mcp:edgeguard-siem"
    }
  ]
}
```

---

## 3. Key Management

Issuers and MCP Servers SHOULD:

- Use modern key types (e.g., Ed25519 or secp256k1, depending on the VC proof suite).
- Rotate keys periodically and update the DID Document accordingly.
- Keep private keys secured in appropriate key management systems (HSM, KMS, or equivalent).

Hosts verifying credentials and DID Documents MUST be prepared to:

- Refresh DID Documents to pick up key rotations.
- Handle the case where a DID is no longer resolvable or is intentionally removed.

---

## 4. Other DID Methods

MCPF allows for the use of other DID methods, for example:

- `did:key` for lightweight, self-contained identifiers.
- `did:ion`, `did:ebsi`, or others for more advanced or regulatory-compliant settings.

Implementations that support multiple DID methods should:

- Clearly document which methods are supported.
- Allow policy-based control over which DID methods are trusted.

---

## 5. Relationship to MCP

MCP itself does not require or define DIDs. MCPF adds DIDs as an identity layer on top of MCP:

- MCP servers are referenced by their DID at the trust layer.
- MCP manifests and endpoints are linked from either:
  - the DID Document, or
  - the `MCPServerCredential`, or
  - the registry entry.

This separation keeps MCP simple while enabling a richer trust and governance model where needed.
