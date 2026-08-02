"""Hashing for JSON gate inputs and generated artifacts.

Reports use a canonical JSON encoding. JSON source files use a byte-level hash
after normalizing only physical line endings, so a CRLF checkout produces the
same audit identity as an LF checkout without collapsing meaningful JSON
formatting or value changes. ``file_sha256`` remains a standard raw-byte hash
for the generic CLI command.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

HASH_PREFIX = "sha256:"


def canonical_json(obj: Any) -> str:
    """Deterministic JSON encoding of ``obj``. Raises ValueError on NaN/Infinity."""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def content_hash(obj: Any) -> str:
    """sha256 over the canonical JSON encoding of ``obj``."""
    digest = hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()
    return HASH_PREFIX + digest


def json_source_sha256(source: bytes) -> str:
    """Hash valid JSON source bytes with physical line endings normalized.

    JSON cannot contain literal CR or LF inside a string, so normalizing CRLF
    and legacy lone-CR line endings affects only source layout. Escaped
    ``\\r`` and ``\\n`` remain distinct JSON values. Keeping this separate from
    :func:`file_sha256` preserves the generic CLI's standard byte checksum.
    """
    normalized = source.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    digest = hashlib.sha256(normalized).hexdigest()
    return HASH_PREFIX + digest


def file_sha256(path: str) -> str:
    """sha256 over raw file bytes (a standard byte-level checksum)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return HASH_PREFIX + h.hexdigest()
