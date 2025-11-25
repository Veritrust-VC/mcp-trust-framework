from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Metadata:
    capabilities: List[str] = field(default_factory=list)
    organization: Optional[str] = None
    country: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    status: Optional[str] = "active"


@dataclass
class RegistryEntry:
    did: str
    endpoint: str
    manifest: str
    credentials: List[str] = field(default_factory=list)
    metadata: Metadata = field(default_factory=Metadata)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RegistryEntry":
        meta_data = data.get("metadata") or {}
        metadata = Metadata(
            capabilities=meta_data.get("capabilities") or [],
            organization=meta_data.get("organization"),
            country=meta_data.get("country"),
            tags=meta_data.get("tags") or [],
            status=meta_data.get("status"),
        )
        return cls(
            did=data["did"],
            endpoint=data["endpoint"],
            manifest=data["manifest"],
            credentials=data.get("credentials") or [],
            metadata=metadata,
        )


@dataclass
class Issuer:
    id: str
    name: str
    documentation: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Issuer":
        return cls(
            id=data["id"],
            name=data["name"],
            documentation=data.get("documentation"),
        )


@dataclass
class RevokedServer:
    did: str
    revokedAt: str
    reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RevokedServer":
        return cls(
            did=data["did"],
            revokedAt=data["revokedAt"],
            reason=data.get("reason"),
        )


@dataclass
class RevokedCredential:
    id: str
    revokedAt: str
    reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RevokedCredential":
        return cls(
            id=data["id"],
            revokedAt=data["revokedAt"],
            reason=data.get("reason"),
        )


@dataclass
class RevocationStatus:
    revokedServers: List[RevokedServer] = field(default_factory=list)
    revokedCredentials: List[RevokedCredential] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RevocationStatus":
        servers = [RevokedServer.from_dict(d) for d in data.get("revokedServers", [])]
        creds = [RevokedCredential.from_dict(d) for d in data.get("revokedCredentials", [])]
        return cls(revokedServers=servers, revokedCredentials=creds)


@dataclass
class PaginatedServers:
    page: int
    limit: int
    total: int
    items: List[RegistryEntry]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PaginatedServers":
        items = [RegistryEntry.from_dict(d) for d in data.get("items", [])]
        return cls(
            page=data.get("page", 1),
            limit=data.get("limit", len(items)),
            total=data.get("total", len(items)),
            items=items,
        )


@dataclass
class SearchResults:
    items: List[RegistryEntry]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResults":
        items = [RegistryEntry.from_dict(d) for d in data.get("items", [])]
        return cls(items=items)

