from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional


def _parse_iso8601(dt_str: str) -> datetime:
    """
    Minimal ISO 8601 parser that understands 'Z' and timezone offsets.
    """
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00")).astimezone(timezone.utc)


def is_credential_valid_now(credential: Dict[str, Any], now: Optional[datetime] = None) -> bool:
    """
    Check if the MCPServerCredential is within its validity window.

    :param credential: Credential dict containing 'issuedAt' and 'validUntil'
    :param now: Optional datetime. If None, uses current UTC time.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    issued_at_str = credential.get("issuedAt")
    valid_until_str = credential.get("validUntil")

    if not issued_at_str or not valid_until_str:
        return False

    try:
        issued_at = _parse_iso8601(issued_at_str)
        valid_until = _parse_iso8601(valid_until_str)
    except Exception:
        return False

    return issued_at <= now <= valid_until


def check_assurance_level(
    credential: Dict[str, Any],
    minimum_level: str = "basic",
) -> bool:
    """
    Check if the credential's assuranceLevel meets or exceeds the given minimum.

    Levels (from lowest to highest):
      - basic
      - verified
      - certified
    """
    levels = ["basic", "verified", "certified"]

    subject = credential.get("credentialSubject", {})
    level = subject.get("assuranceLevel", "basic")

    try:
        min_index = levels.index(minimum_level)
        level_index = levels.index(level)
    except ValueError:
        return False

    return level_index >= min_index


def validate_credential_structure(credential: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """
    Validate the credential against the given JSON Schema.

    This uses the 'jsonschema' library if available. If the library is not installed,
    this function will raise an ImportError.

    :param credential: Credential dictionary to validate.
    :param schema: JSON Schema dictionary.
    :raises ValueError: if the credential does not conform to the schema.
    :raises ImportError: if jsonschema is not installed.
    """
    try:
        from jsonschema import Draft202012Validator  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "jsonschema is required for validate_credential_structure. "
            "Install it via 'pip install jsonschema'."
        ) from exc

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(credential), key=lambda e: e.path)
    if errors:
        msg_lines = [
            f"- {'/'.join(map(str, err.path))}: {err.message}" for err in errors
        ]
        msg = "\n".join(msg_lines)
        raise ValueError(f"Credential does not conform to schema:\n{msg}")

