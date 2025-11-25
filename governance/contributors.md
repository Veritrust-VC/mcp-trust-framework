# MCP Trust Framework – Contributors Guide

This document describes how to contribute to the **MCP Trust Framework (MCPF)** project at the governance level (spec design, roadmap, alignment), beyond regular code contributions.

For code and documentation contribution details, see also the root [`CONTRIBUTING.md`](../CONTRIBUTING.md).

---

## 1. Roles

The project recognizes several informal roles:

- **Maintainers**  
  Coordinate releases, approve changes to core specifications, and manage the repository.

- **Contributors**  
  Submit issues, pull requests, and proposals for improvements to specs, SDKs, and implementations.

- **Advisors / Reviewers**  
  External experts (e.g., from industry, academia, or standards bodies) who review documents and provide feedback on security, interoperability, and governance.

---

## 2. Areas of Contribution

You can contribute in several ways:

1. **Specifications**
   - Propose changes or extensions to:
     - `specs/MCPF-1.0.md`
     - `specs/registry-api.md`
     - `specs/credential-schema.json`
     - `specs/did-profile.md`
     - `specs/security-considerations.md`
   - Suggest clarifications or examples.
   - Help align with emerging standards and best practices.

2. **Reference Implementations**
   - Improve the FastAPI registry (`registry-reference-implementation/`).
   - Add persistence backends (e.g., PostgreSQL, SQLite).
   - Implement authentication / authorization options.
   - Harden security and logging.

3. **SDKs**
   - Enhance Python SDK (`sdks/python/`).
   - Enhance Node/TypeScript SDK (`sdks/node/`).
   - Add support for additional languages where appropriate.

4. **Use Cases and Examples**
   - Contribute example registry entries, credentials, and DID documents.
   - Write integration recipes for popular MCP hosts/agents.
   - Document real-world deployment patterns.

5. **Governance and Processes**
   - Help refine the roadmap.
   - Propose working groups or topic-focused task forces.
   - Align MCPF with regulatory or compliance frameworks where relevant.

---

## 3. How to Propose Changes

### 3.1. Specifications & Governance

1. Open an issue with a descriptive title, prefixed with:
   - `[SPEC]` – for changes to core spec documents.
   - `[GOV]` – for governance or process changes.
2. Clearly describe:
   - The problem you are solving.
   - The proposed change.
   - Any impact on existing implementations.
3. Be prepared to iterate on the proposal based on feedback.
4. Once there is broad agreement, submit a PR referencing the issue.

### 3.2. Code Contributions

1. Open a regular GitHub issue or PR.
2. Keep changes focused; avoid mixing spec and code changes in the same PR unless necessary.
3. Update relevant docs and READMEs when changing public APIs.

---

## 4. Decision Process

At the current stage:

- Maintainers review PRs and issues.
- For breaking changes in specs:
  - Discussion must take place in public issues.
  - A clear migration path or rationale must be documented.
  - The `versioning.md` rules must be followed.

When a broader steering group or advisory board is formed, this document may be updated to reflect more formal governance.

---

## 5. Communication

- Primary channel: GitHub Issues and Pull Requests.
- Additional communication channels (WG calls, mailing lists, etc.) may be introduced later and documented here.

---

## 6. Code of Conduct

All contributors are expected to:

- Treat others with respect.
- Keep discussions technical and constructive.
- Help maintain a welcoming environment for newcomers.

Behaviors inconsistent with these expectations may result in moderation actions by the maintainers.

---

Thank you for helping shape the MCP Trust Framework.
