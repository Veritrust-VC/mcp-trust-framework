# Verifying an MCP Server with the MCP Trust Registry (Node.js / TypeScript)

This guide shows how a Node.js / TypeScript host or agent can:

1. Query an MCP Trust Registry for a server by DID  
2. Fetch its MCPServerCredential  
3. Validate the credential structure with a JSON schema validator  
4. Perform basic validity checks (time window, assurance level)

> Note: This example does **not** perform real cryptographic signature verification.

---

## 1. Setup

Install dependencies:

```bash
npm install node-fetch ajv ajv-formats
# or
pnpm add node-fetch ajv ajv-formats
```

Assume:

```
Registry: https://registry.example.com
DID:      did:web:veritrust.vc:mcp:edgeguard-siem
```

In Node 18+, you can use the built-in fetch.
If you’re on older Node, configure node-fetch as needed.

## 2. Fetch Registry Entry

Example TypeScript file, verify-mcp-server.ts:

```typescript
import fetch from "node-fetch";

const REGISTRY_BASE_URL = "https://registry.example.com";
const SERVER_DID = "did:web:veritrust.vc:mcp:edgeguard-siem";

async function fetchRegistryEntry(did: string): Promise<any> {
  const url = `${REGISTRY_BASE_URL}/mcp/servers/${encodeURIComponent(did)}`;
  const resp = await fetch(url, { method: "GET" });

  if (resp.status === 404) {
    throw new Error(`No registry entry found for DID ${did}`);
  }
  if (!resp.ok) {
    throw new Error(`Registry error: ${resp.status} ${resp.statusText}`);
  }

  return resp.json();
}

(async () => {
  const entry = await fetchRegistryEntry(SERVER_DID);
  console.log("Registry entry:", entry);
})();
```

## 3. Fetch MCPServerCredential

```typescript
async function fetchCredential(entry: any): Promise<any> {
  const creds: string[] = entry.credentials || [];
  if (!creds.length) {
    throw new Error("Registry entry has no 'credentials' URLs");
  }

  const credUrl = creds[0];
  const resp = await fetch(credUrl, { method: "GET" });
  if (!resp.ok) {
    throw new Error(`Failed to fetch credential: ${resp.status} ${resp.statusText}`);
  }

  return resp.json();
}

(async () => {
  const entry = await fetchRegistryEntry(SERVER_DID);
  const credential = await fetchCredential(entry);
  console.log("Credential:", credential);
})();
```

## 4. Validate Credential Structure with AJV

Place credential-schema.json (from specs/) where it can be imported or loaded.
For simplicity here, assume we load it from a file.

```typescript
import Ajv from "ajv";
import addFormats from "ajv-formats";
import { readFileSync } from "fs";
import { resolve } from "path";

function loadSchema(): any {
  const schemaPath = resolve(__dirname, "../specs/credential-schema.json");
  const raw = readFileSync(schemaPath, "utf-8");
  return JSON.parse(raw);
}

function validateCredentialStructure(credential: any, schema: any): void {
  const ajv = new Ajv({ allErrors: true });
  addFormats(ajv);
  const validate = ajv.compile(schema);
  const valid = validate(credential);
  if (!valid) {
    const errors = (validate.errors || [])
      .map((e) => `- ${e.instancePath || "/"} ${e.message}`)
      .join("\n");
    throw new Error(`Credential does not conform to schema:\n${errors}`);
  }
}
```

## 5. Basic Validity Checks

```typescript
function parseIsoDateTime(value: string): Date {
  // Node Date supports ISO 8601 with Z or offset
  const d = new Date(value);
  if (isNaN(d.getTime())) {
    throw new Error(`Invalid date-time: ${value}`);
  }
  return d;
}

function isCredentialValidNow(credential: any, now: Date = new Date()): boolean {
  const issuedAt = parseIsoDateTime(credential.issuedAt);
  const validUntil = parseIsoDateTime(credential.validUntil);

  return issuedAt <= now && now <= validUntil;
}

function checkAssuranceLevel(credential: any, minimumLevel: string = "basic"): boolean {
  const levels = ["basic", "verified", "certified"];
  const subject = credential.credentialSubject || {};
  const level = subject.assuranceLevel || "basic";

  const minIndex = levels.indexOf(minimumLevel);
  const levelIndex = levels.indexOf(level);

  if (minIndex === -1 || levelIndex === -1) {
    return false;
  }
  return levelIndex >= minIndex;
}
```

## 6. Putting It All Together

```typescript
(async () => {
  try {
    const entry = await fetchRegistryEntry(SERVER_DID);
    const credential = await fetchCredential(entry);

    const schema = loadSchema();
    validateCredentialStructure(credential, schema);

    const now = new Date();
    if (!isCredentialValidNow(credential, now)) {
      throw new Error("Credential is not within its validity period.");
    }

    if (!checkAssuranceLevel(credential, "verified")) {
      throw new Error("Credential assurance level is below required minimum.");
    }

    console.log("Credential is structurally valid, current, and meets assurance requirements.");
    console.log("MCP server can be considered trusted according to this basic policy.");

    // TODO: integrate this result into your MCP host's tool enablement logic.
  } catch (err: any) {
    console.error("Verification failed:", err.message || err);
    process.exit(1);
  }
})();
```
