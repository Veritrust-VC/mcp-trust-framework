# @veritrust/mcpf-client (Node.js / TypeScript SDK)

A minimal Node.js / TypeScript client SDK for interacting with **MCP Trust Registry** implementations of the **MCP Trust Framework (MCPF)**.

This SDK helps you:

- Query MCP registry endpoints
- Retrieve registry entries by DID
- Search for MCP servers by metadata
- Perform basic validation of MCPServerCredentials (time window, assurance level, optional JSON Schema validation)

> ⚠️ This SDK does **not** implement full cryptographic verification of Verifiable Credentials.  
> It focuses on structure and simple policy checks.

---

## Installation

From within this subdirectory for local development:

```bash
cd sdks/node
npm install
npm run build


If published as a package, you would install it like:

npm install @veritrust/mcpf-client

Quick Start
import { RegistryClient } from "./dist"; // or "@veritrust/mcpf-client" after publishing
import { isCredentialValidNow, checkAssuranceLevel } from "./dist/verification";

const REGISTRY_URL = "http://localhost:8080";
const SERVER_DID = "did:web:veritrust.vc:mcp:edgeguard-siem";

async function main() {
  const client = new RegistryClient(REGISTRY_URL);

  // 1. Get registry entry
  const entry = await client.getServer(SERVER_DID);
  console.log("Registry entry:", entry);

  // 2. Fetch MCPServerCredential from first credential URL
  if (!entry.credentials.length) {
    throw new Error("No credentials listed for this server.");
  }

  const credUrl = entry.credentials[0];
  const credResp = await fetch(credUrl);
  if (!credResp.ok) {
    throw new Error(`Failed to fetch credential: ${credResp.status} ${credResp.statusText}`);
  }
  const credential = await credResp.json();

  // 3. Basic checks
  if (!isCredentialValidNow(credential)) {
    throw new Error("Credential is not within its validity period.");
  }

  if (!checkAssuranceLevel(credential, "verified")) {
    throw new Error("Credential assurance level is below required minimum.");
  }

  console.log("Credential is current and meets assurance requirements.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});


This example assumes Node.js 18+ where fetch is available globally.
If you’re on an older Node version, you can polyfill it (e.g., with node-fetch).

API Overview
RegistryClient
import { RegistryClient } from "@veritrust/mcpf-client";

const client = new RegistryClient("http://localhost:8080");

// List servers
const page = await client.listServers(1, 50);

// Get server by DID
const entry = await client.getServer("did:web:example.com:mcp:myserver");

// Search servers
const results = await client.searchServers({ capability: "telemetry", tag: "security" });

// Upsert (register/update) a server
await client.upsertServer(entry);

Types

All main data structures are defined in src/types.ts and exported from the package:

Metadata

RegistryEntry

PaginatedServers

SearchResults

Issuer

RevokedServer

RevokedCredential

RevocationStatus

Verification Helpers

In src/verification.ts (also exported):

isCredentialValidNow(credential: any, now?: Date): boolean

checkAssuranceLevel(credential: any, minimumLevel?: string): boolean

validateCredentialStructure(credential: any, schema: any): void
(uses ajv and ajv-formats for JSON Schema validation)

Limitations

VC crypto proof verification is out of scope for this SDK.

No caching or advanced trust policy features are included.

Intended as a simple building block for hosts/agents integrating with an MCP Trust Registry.


---
