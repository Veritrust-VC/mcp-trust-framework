from __future__ import annotations

from typing import Optional, Dict, Any
import requests

from .models import (
    RegistryEntry,
    PaginatedServers,
    SearchResults,
    RevocationStatus,
    Issuer,
)


class RegistryClient:
    """
    Client for interacting with an MCP Trust Registry that implements
    the MCP Trust Framework (MCPF) API.
    """

    def __init__(self, base_url: str, session: Optional[requests.Session] = None) -> None:
        """
        :param base_url: Base URL of the registry, e.g. "http://localhost:8080"
        :param session: Optional requests.Session for connection pooling and custom config.
        """
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    # --- Low-level request helper ---

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params, timeout=10)
        if not resp.ok:
            try:
                detail = resp.json()
            except Exception:
                detail = {"error": resp.text}
            raise RuntimeError(
                f"Registry GET {path} failed: {resp.status_code} {resp.reason} – {detail}"
            )
        return resp.json()

    def _post(self, path: str, json_body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = self.session.post(url, json=json_body, timeout=10)
        if not resp.ok:
            try:
                detail = resp.json()
            except Exception:
                detail = {"error": resp.text}
            raise RuntimeError(
                f"Registry POST {path} failed: {resp.status_code} {resp.reason} – {detail}"
            )
        return resp.json()

    # --- High-level API methods ---

    def list_servers(self, page: int = 1, limit: int = 50) -> PaginatedServers:
        """
        List MCP servers known to the registry.

        :param page: page number, starting at 1
        :param limit: number of items per page
        """
        data = self._get("/mcp/servers", params={"page": page, "limit": limit})
        return PaginatedServers.from_dict(data)

    def get_server(self, did: str) -> RegistryEntry:
        """
        Get a single MCP server registry entry by DID.

        :param did: DID of the MCP server
        """
        data = self._get(f"/mcp/servers/{did}")
        return RegistryEntry.from_dict(data)

    def search_servers(
        self,
        capability: Optional[str] = None,
        tag: Optional[str] = None,
        organization: Optional[str] = None,
        country: Optional[str] = None,
    ) -> SearchResults:
        """
        Search for MCP servers by simple metadata filters.
        """
        params: Dict[str, Any] = {}
        if capability:
            params["capability"] = capability
        if tag:
            params["tag"] = tag
        if organization:
            params["organization"] = organization
        if country:
            params["country"] = country

        data = self._get("/mcp/search", params=params)
        return SearchResults.from_dict(data)

    def upsert_server(self, entry: RegistryEntry) -> Dict[str, Any]:
        """
        Register or update a registry entry.

        NOTE: In real deployments, this would typically require authentication.
        """
        body = {
            "did": entry.did,
            "endpoint": entry.endpoint,
            "manifest": entry.manifest,
            "credentials": entry.credentials,
            "metadata": {
                "capabilities": entry.metadata.capabilities,
                "organization": entry.metadata.organization,
                "country": entry.metadata.country,
                "tags": entry.metadata.tags,
                "status": entry.metadata.status,
            },
        }
        return self._post("/mcp/servers", json_body=body)

    def list_issuers(self) -> Dict[str, Any]:
        """
        Return raw issuer information from the registry.
        Caller can cast to Issuer objects if desired.
        """
        data = self._get("/mcp/issuers")
        issuers_raw = data.get("issuers", [])
        issuers = [Issuer.from_dict(d) for d in issuers_raw]
        return {"issuers": issuers}

    def get_revocations(self) -> RevocationStatus:
        """
        Get revoked servers and credentials as reported by the registry.
        """
        data = self._get("/mcp/revocations")
        return RevocationStatus.from_dict(data)

