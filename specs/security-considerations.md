# Security Considerations – MCP Trust Framework

This document outlines security considerations for implementations of the MCP Trust Framework (MCPF), including registries, issuers, and hosts.

---

## 1. Key Management

### 1.1. Issuer Keys

Issuers (trust authorities) MUST:

- Store private keys securely (HSM, KMS, or equivalent).
- Rotate keys based on internal policies and best practices.
- Publish updated verification material via DID Documents or other agreed mechanisms.

Compromise of an issuer’s key may require:

- Revoking or re-issuing affected credentials.
- Updating trust policies and communicating with relying parties.

### 1.2. Server Keys

MCP servers that sign their own credentials or metadata SHOULD:

- Use dedicated keys for signing.
- Protect private keys with appropriate system protections.
- Rotate keys and update DID Documents accordingly.

---

## 2. Transport Security

All MCPF-related endpoints MUST use HTTPS with valid TLS certificates:

- MCP endpoints (the tool APIs)
- Registry APIs
- Credential hosting endpoints
- DID Document hosts
- `.well-known` metadata endpoints

Hosts SHOULD:

- Reject connections with invalid or self-signed certificates, unless explicitly configured otherwise for testing.
- Prefer modern TLS versions and cipher suites.

---

## 3. Revocation and Expiry

### 3.1. Credential Expiry

- `MCPServerCredential` includes `validUntil`.
- Hosts MUST check that the current time is within the validity window.
- Shorter validity periods reduce risk if a server or issuer becomes compromised.

### 3.2. Revocation

Registries and/or issuers SHOULD support revocation of:

- Specific MCP servers
- Specific credentials

Methods may include:

- Central revocation lists exposed via `GET /mcp/revocations`
- Status endpoints for individual credentials
- Updates to registry entries marking servers as `status: "revoked"` or `status: "inactive"`

Hosts SHOULD periodically refresh revocation information and apply it during verification.

---

## 4. Registry Compromise

If a registry is compromised, attackers may:

- Insert malicious registry entries
- Modify existing entries
- Remove entries to hide legit servers

Mitigations:

- Treat registries as **indexes**, not ultimate trust sources.
- Always verify credentials and signatures independently of the registry.
- Allow hosts to use multiple registries or direct credentials obtained from issuers.
- Log registry responses for audit and incident response.

---

## 5. Denial of Service

Registries and DID/VC endpoints may be subject to DoS attacks.

Implementations should:

- Apply rate limiting and resource throttling.
- Use caching of stable data (e.g., DID Documents) on the client side with reasonable TTL.
- Implement backoff strategies on repeated failures.

---

## 6. Privacy

Public registries may expose metadata about:

- Organizations
- Capabilities of MCP servers
- Geographical hints (e.g., `country` fields)

Where privacy is a concern:

- Limit fields in public registries to non-sensitive metadata.
- Use private registries or restricted access for sensitive environments.
- Provide minimal disclosure in credentials.

---

## 7. Policy Misconfiguration

Trust policies are powerful. Misconfiguration can cause:

- Overly permissive access to untrusted MCP servers.
- Overly strict policies that block legitimate operations.

Recommendations:

- Start with cautious defaults.
- Provide clear policy documentation.
- Log policy decisions (why a particular server was accepted or rejected).

---

## 8. Logging and Audit

Hosts and registries SHOULD log:

- Which MCP servers were used (by DID and endpoint).
- Which credentials were checked and their status.
- Policy decisions and revocation checks.

Logs aid:

- Forensic analysis
- Compliance reporting
- Security audits

Care must be taken not to log sensitive data beyond what is necessary.

---

## 9. Implementation Bugs

As with any new framework, early implementations may contain bugs.

Mitigations:

- Prefer simple, well-reviewed libraries.
- Keep crypto logic as isolated as possible.
- Add unit tests around:
  - Credential parsing and validation
  - Registry API interactions
  - Policy evaluation logic

Where practical, independent security review of critical components is recommended.
