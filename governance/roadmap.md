# MCP Trust Framework – Roadmap

This roadmap provides a high-level view of where the **MCP Trust Framework (MCPF)** and related components are headed.  
It is intentionally simple and may evolve based on community feedback and real-world deployments.

---

## Phase 1 – Foundation (MVP Spec + Registry)

**Goal:** Establish a working end-to-end baseline.

**Scope:**

- Publish core specifications:
  - `MCPF-1.0` (draft)
  - `registry-api.md`
  - `credential-schema.json`
  - `did-profile.md`
  - `security-considerations.md`
- Provide:
  - FastAPI-based reference registry (in-memory store)
  - Python and Node/TS SDKs (MVP)
- Include working examples:
  - Sample registry entry
  - Sample MCPServerCredential
  - Sample DID Document
  - Minimal verification guides (Python & Node)

**Exit Criteria:**

- Registry implementation running successfully against the spec.
- At least one real MCP server integrated via DID + registry.
- Basic documentation and examples available.

---

## Phase 2 – Persistence, Auth, and Policy Hooks

**Goal:** Make the registry practical for early production pilots.

**Potential Work Items:**

- Add persistent storage options:
  - SQLite or PostgreSQL backend for registry entries
  - Simple migration and configuration
- Introduce authentication / authorization:
  - API keys or OAuth2 / OIDC for `POST /mcp/servers`
  - Role concepts (e.g., admin, server-owner)
- Add policy hook points:
  - Allow registries to annotate entries with policy hints.
  - Ensure SDKs expose fields enough for host policies.

**Exit Criteria:**

- A small number of pilot deployments using persistent registry.
- Clear examples of policy integration with at least one MCP host.

---

## Phase 3 – Federation and Multi-Registry Support

**Goal:** Enable multiple registries and trust authorities to coexist.

**Potential Work Items:**

- Define a minimal pattern for registry federation:
  - Cross-referencing of registry entries
  - Optional upstream / downstream relationships
- Expand `.well-known` metadata format:
  - Advertise supported versions, trust domains, and capabilities.
- SDK enhancements:
  - Support querying multiple registries and merging results.
  - Handle conflicting or overlapping entries gracefully.

**Exit Criteria:**

- Demonstrated interoperability between at least two independent registries.
- Documented examples of federation topologies (e.g., local + global).

---

## Phase 4 – Deep VC / DID Integration and Security Hardening

**Goal:** Strengthen the trust layer for security-sensitive environments.

**Potential Work Items:**

- Enhance guidance on:
  - VC proof suites (e.g., Ed25519, ECDSA-based)
  - Recommended DID methods for different contexts (e.g., did:web, did:ebsi)
- Add concrete examples of:
  - Full cryptographic verification in SDKs (behind optional feature flags)
  - Integration with HSM/KMS for issuers
- Harden registry reference implementation:
  - Improved logging and audit trails
  - Rate limiting and basic abuse protection
  - Better error reporting and observability

**Exit Criteria:**

- At least one security-focused deployment in a regulated or critical setting.
- External review or audit of the security model for at least one implementation.

---

## Phase 5 – Ecosystem Integration and Standardization

**Goal:** Align MCPF with broader AI, security, and identity ecosystems.

**Potential Work Items:**

- Integration recipes for:
  - Specific MCP hosts / agents
  - AI frameworks and orchestration tools
- Mapping to:
  - Relevant standards or regulatory frameworks (where applicable)
  - Existing PKI / identity infrastructures (e.g., enterprise CAs, IAM systems)
- Consider forming:
  - A small working group or advisory board
  - A formal draft for external standards bodies if there is demand

**Exit Criteria:**

- Real-world multi-vendor deployments using MCPF.
- Recognition or alignment with at least one external community, consortium, or initiative.

---

## How to Influence the Roadmap

- Open GitHub issues with prefix:
  - `[ROADMAP]` for proposals or adjustments.
- Provide:
  - Use case descriptions
  - Impact analysis
  - Implementation estimates (if possible)
- Larger shifts (e.g., new phases) will be discussed in public issues and updated here.

This roadmap is deliberately high-level and does not promise specific dates.  
It is intended as a guide for contributors and adopters of the MCP Trust Framework.
