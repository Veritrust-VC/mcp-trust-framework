# MCP Trust Framework – Versioning Policy

This document defines how versions are managed for:

1. **Specifications** (MCPF, registry API, schemas)
2. **Reference Implementations** (registry, tools)
3. **SDKs** (Python, Node/TS)

The goal is to keep changes predictable and transparent for implementers.

---

## 1. Semantic Versioning

All components use **semantic versioning** of the form:

```text
MAJOR.MINOR.PATCH


MAJOR – breaking changes

MINOR – new features with backward compatibility

PATCH – bug fixes and documentation-only changes

2. Specification Versioning

The main spec (MCPF-1.0.md, etc.) is versioned at the document level.

File naming convention:

MCPF-1.0.md

MCPF-1.1.md

MCPF-2.0.md

Each spec documents its own version in the header.

2.1. Patch-level Changes

Examples:

Clarifying text

Fixing typos

Adjusting examples without changing semantics

Patch-level changes:

May be applied in-place to the current spec file.

Should be noted in a change log or the spec’s “Change History” section.

2.2. Minor Changes (Backward Compatible)

Examples:

Adding optional fields

Adding new non-breaking endpoints in the registry API

Adding new credential types that do not invalidate existing ones

Minor changes:

Should update the minor version (e.g., 1.0 → 1.1).

Must preserve compatibility for existing implementations that follow the previous minor version.

2.3. Major Changes (Breaking)

Examples:

Removing or renaming required fields

Changing the meaning of existing fields

Removing or fundamentally altering endpoints

Any change that would cause a fully conformant implementation to break or misinterpret data

Major changes:

Require creating a new spec version, e.g., MCPF-2.0.md.

Existing implementations may need migration steps, which should be documented.

3. Registry Implementation Versioning

The reference registry (registry-reference-implementation/) follows semantic versioning in its release tags.

Its version is independent from the spec version, but:

Each release notes which spec version(s) it supports (e.g., MCPF 1.0).

A registry release may implement multiple spec versions or provide compatibility modes if needed.

Breaking changes (e.g., API behavior or config semantics) require a major version bump.

4. SDK Versioning

SDKs (sdks/python, sdks/node) each:

Use semantic versioning in their respective packaging metadata

Python: pyproject.toml

Node: package.json

Document which spec version(s) they target and support.

Examples:

Python: mcpf-client version 0.1.0

Node: @veritrust/mcpf-client version 0.1.0

4.1. Non-breaking SDK Changes

Examples:

Adding helper functions

Adding optional parameters

Improving error messages

Documentation updates

These should result in MINOR or PATCH version bumps.

4.2. Breaking SDK Changes

Examples:

Renaming or removing public methods

Changing method signatures incompatibly

Changing return types in ways that break existing code

These require a MAJOR version bump for that SDK.

5. Cross-Version Compatibility

The project aims to:

Keep spec changes incremental and backward-compatible where feasible.

Provide clear guidance when compatibility can’t be maintained.

Implementers should:

Pin to specific spec versions as needed.

Note which MCPF version their software supports in their own documentation.

Avoid mixing incompatible versions without explicit migration plans.

6. Change Communication

For significant changes:

A changelog entry SHOULD be added (either per module or as a central changelog).

Maintainers SHOULD describe:

What changed

Why it changed

Impact on existing implementations

Migration guidelines (for breaking changes)

This versioning policy may itself evolve. Any substantive modifications will be discussed publicly (e.g., via GitHub issues) and updated in this file.
