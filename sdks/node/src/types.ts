export interface Metadata {
  capabilities: string[];
  organization?: string;
  country?: string;
  tags: string[];
  status?: string;
}

export interface RegistryEntry {
  did: string;
  endpoint: string;
  manifest: string;
  credentials: string[];
  metadata: Metadata;
}

export interface Issuer {
  id: string;
  name: string;
  documentation?: string;
}

export interface RevokedServer {
  did: string;
  revokedAt: string;
  reason?: string;
}

export interface RevokedCredential {
  id: string;
  revokedAt: string;
  reason?: string;
}

export interface RevocationStatus {
  revokedServers: RevokedServer[];
  revokedCredentials: RevokedCredential[];
}

export interface PaginatedServers {
  page: number;
  limit: number;
  total: number;
  items: RegistryEntry[];
}

export interface SearchResults {
  items: RegistryEntry[];
}
