"""Canonical hashing.

Every artifact the gate consumes (dataset, configs, scorer config, thresholds,
pricing table) and the comparison result itself are identified by a sha256 over
a canonical JSON encoding, so a manifest pins exactly what produced a verdict.

Canonical form: sorted keys, compact separators, UTF-8, NaN/Infinity rejected.
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


def file_sha256(path: str) -> str:
    """sha256 over raw file bytes (for pinning files exactly as committed)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return HASH_PREFIX + h.hexdigest()
