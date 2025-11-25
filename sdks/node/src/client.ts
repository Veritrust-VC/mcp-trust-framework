import {
  RegistryEntry,
  PaginatedServers,
  SearchResults,
  RevocationStatus,
  Issuer
} from "./types";

export interface RegistryClientOptions {
  fetchImpl?: typeof fetch;
}

/**
 * Client for interacting with an MCP Trust Registry that implements
 * the MCP Trust Framework (MCPF) API.
 */
export class RegistryClient {
  private readonly baseUrl: string;
  private readonly fetchImpl: typeof fetch;

  constructor(baseUrl: string, options: RegistryClientOptions = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.fetchImpl = options.fetchImpl ?? (globalThis.fetch as typeof fetch);

    if (!this.fetchImpl) {
      throw new Error(
        "No fetch implementation available. Use Node.js 18+ or provide fetchImpl in options."
      );
    }
  }

  // --- internal helpers ---

  private async get(path: string, params?: Record<string, string>): Promise<any> {
    const url = new URL(this.baseUrl + path);

    if (params) {
      for (const [key, value] of Object.entries(params)) {
        url.searchParams.set(key, value);
      }
    }

    const resp = await this.fetchImpl(url.toString());
    if (!resp.ok) {
      let detail: any;
      try {
        detail = await resp.json();
      } catch {
        detail = await resp.text();
      }
      throw new Error(
        `Registry GET ${path} failed: ${resp.status} ${resp.statusText} – ${JSON.stringify(
          detail
        )}`
      );
    }

    return resp.json();
  }

  private async post(path: string, body: any): Promise<any> {
    const url = this.baseUrl + path;
    const resp = await this.fetchImpl(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    if (!resp.ok) {
      let detail: any;
      try {
        detail = await resp.json();
      } catch {
        detail = await resp.text();
      }
      throw new Error(
        `Registry POST ${path} failed: ${resp.status} ${resp.statusText} – ${JSON.stringify(
          detail
        )}`
      );
    }

    return resp.json();
  }

  // --- public API ---

  /**
   * List MCP servers known to the registry.
   */
  async listServers(page = 1, limit = 50): Promise<PaginatedServers> {
    const data = await this.get("/mcp/servers", {
      page: String(page),
      limit: String(limit)
    });

    const items = (data.items || []) as any[];
    return {
      page: data.page ?? page,
      limit: data.limit ?? limit,
      total: data.total ?? items.length,
      items: items.map((raw) => this.toRegistryEntry(raw))
    };
  }

  /**
   * Get a single MCP server registry entry by DID.
   */
  async getServer(did: string): Promise<RegistryEntry> {
    const data = await this.get(`/mcp/servers/${encodeURIComponent(did)}`);
    return this.toRegistryEntry(data);
  }

  /**
   * Search for MCP servers by simple metadata filters.
   */
  async searchServers(filters: {
    capability?: string;
    tag?: string;
    organization?: string;
    country?: string;
  }): Promise<SearchResults> {
    const params: Record<string, string> = {};
    if (filters.capability) params.capability = filters.capability;
    if (filters.tag) params.tag = filters.tag;
    if (filters.organization) params.organization = filters.organization;
    if (filters.country) params.country = filters.country;

    const data = await this.get("/mcp/search", params);
    const items = (data.items || []) as any[];
    return {
      items: items.map((raw) => this.toRegistryEntry(raw))
    };
  }

  /**
   * Register or update a registry entry.
   *
   * NOTE: In real deployments, this should be authenticated.
   */
  async upsertServer(entry: RegistryEntry): Promise<{ status: string; did: string }> {
    const body = {
      did: entry.did,
      endpoint: entry.endpoint,
      manifest: entry.manifest,
      credentials: entry.credentials,
      metadata: {
        capabilities: entry.metadata.capabilities,
        organization: entry.metadata.organization,
        country: entry.metadata.country,
        tags: entry.metadata.tags,
        status: entry.metadata.status
      }
    };

    return this.post("/mcp/servers", body);
  }

  /**
   * List recognized issuers.
   */
  async listIssuers(): Promise<{ issuers: Issuer[] }> {
    const data = await this.get("/mcp/issuers");
    const rawIssuers = (data.issuers || []) as any[];
    const issuers: Issuer[] = rawIssuers.map((d) => ({
      id: d.id,
      name: d.name,
      documentation: d.documentation
    }));
    return { issuers };
  }

  /**
   * Get revoked servers and credentials as reported by the registry.
   */
  async getRevocations(): Promise<RevocationStatus> {
    const data = await this.get("/mcp/revocations");
    const revokedServers = ((data.revokedServers || []) as any[]).map((d) => ({
      did: d.did,
      revokedAt: d.revokedAt,
      reason: d.reason
    }));
    const revokedCredentials = ((data.revokedCredentials || []) as any[]).map((d) => ({
      id: d.id,
      revokedAt: d.revokedAt,
      reason: d.reason
    }));
    return {
      revokedServers,
      revokedCredentials
    };
  }

  // --- helpers ---

  private toRegistryEntry(raw: any): RegistryEntry {
    const metadata = raw.metadata || {};
    return {
      did: raw.did,
      endpoint: raw.endpoint,
      manifest: raw.manifest,
      credentials: raw.credentials || [],
      metadata: {
        capabilities: metadata.capabilities || [],
        organization: metadata.organization,
        country: metadata.country,
        tags: metadata.tags || [],
        status: metadata.status
      }
    };
  }
}
