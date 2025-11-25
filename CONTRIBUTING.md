# Contributing to MCP Trust Framework (MCPF)

Thank you for your interest in contributing to the MCP Trust Framework.

There are two main contribution areas:

1. **Specification & Governance**
2. **Code & Implementations** (registry, SDKs, tools)

---

## Issues and Discussions

- Use GitHub Issues to:
  - Report bugs
  - Propose enhancements
  - Suggest clarifications to the specification
- For significant spec changes, please open an issue with the prefix **`[SPEC]`** in the title.

---

## Specification Changes

1. Open an issue describing:
   - The problem
   - The proposed change
   - Impact on existing implementations
2. Discuss and refine in the issue thread.
3. Once accepted, create a PR against `specs/`:
   - Update `MCPF-1.x.md` as needed.
   - Update related schemas or API docs if applicable.
4. Specification versions follow semantic versioning:
   - `MAJOR.MINOR.PATCH`
   - Breaking changes require a major bump.

---

## Code Contributions

### General Guidelines

- Follow existing code style:
  - Python: PEP 8 style, type hints where reasonable.
  - Node/TypeScript: idiomatic ES modules, basic types, no framework lock-in.
- Include minimal tests for new features or bug fixes where applicable.
- Keep changes focused; avoid mixing unrelated modifications in a single PR.

### Reference Registry (FastAPI)

- Located in `registry-reference-implementation/`.
- New features should:
  - Align with `specs/registry-api.md`.
  - Preserve backwards compatibility when possible.
- If adding storage backends or auth layers, keep configuration-driven design.

### SDKs

- Python SDK: `sdks/python/`
- Node SDK: `sdks/node/`

When changing SDK APIs:
- Update README examples.
- Note any breaking changes in the PR description.

---

## Governance

See [`governance/versioning.md`](governance/versioning.md) and [`governance/roadmap.md`](governance/roadmap.md) for details about how the framework evolves over time.

---

## Code of Conduct

By participating in this project, you agree to:
- Treat all contributors with respect.
- Focus on technical arguments, not personal attacks.
- Help keep the project useful and interoperable.

Thank you for helping build a trustworthy MCP ecosystem.
