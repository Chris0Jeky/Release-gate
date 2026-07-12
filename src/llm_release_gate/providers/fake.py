"""Deterministic fake provider (record/replay style).

Responses come from a committed fixture file, keyed by (model, item_id). This is
what lets the whole gate run in CI with no API key and byte-identical results.

Fixture file shape:

    {
      "version": "1",
      "responses": {
        "<model>": {
          "<item_id>": {
            "text": "...",                # required
            "prompt_tokens": 312,         # optional — omit to simulate a provider
            "completion_tokens": 45,      #   that reports no usage data
            "latency_ms": 820.0,          # optional recorded latency
            "error": "..."                # if present, the call raises ProviderError
          }
        }
      }
    }

A missing (model, item_id) entry raises ProviderError — the same path a real
provider outage takes — so provider-failure behavior is testable offline.
"""

from __future__ import annotations

import json
import os

from ..errors import GateConfigError, ProviderError
from ..hashing import file_sha256
from . import Provider, ProviderRequest, ProviderResult, register_provider


class FakeProvider(Provider):
    name = "fake"

    def __init__(self, options: dict, base_dir: str):
        fixtures = options.get("fixtures")
        if not fixtures:
            raise GateConfigError(
                "fake provider requires provider_options.fixtures (path to fixture JSON)"
            )
        path = fixtures if os.path.isabs(fixtures) else os.path.join(base_dir, fixtures)
        if not os.path.isfile(path):
            raise GateConfigError(f"fake provider fixture file not found: {path}")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise GateConfigError(f"fake provider fixtures not valid JSON: {path} ({exc})") from exc
        if not isinstance(data, dict) or not isinstance(data.get("responses"), dict):
            raise GateConfigError(f"fake provider fixtures {path}: expected {{'responses': {{...}}}}")
        self.fixtures_path = path
        self.fixtures_sha256 = file_sha256(path)
        self.responses: dict = data["responses"]

    def complete(self, request: ProviderRequest) -> ProviderResult:
        by_model = self.responses.get(request.model)
        if by_model is None:
            raise ProviderError(
                f"no fixtures for model '{request.model}' in {self.fixtures_path}"
            )
        entry = by_model.get(request.item_id)
        if entry is None:
            raise ProviderError(
                f"no fixture for item '{request.item_id}' under model "
                f"'{request.model}' in {self.fixtures_path}"
            )
        if "error" in entry:
            raise ProviderError(f"simulated provider failure: {entry['error']}")
        if "text" not in entry:
            raise ProviderError(
                f"fixture for item '{request.item_id}' has neither 'text' nor 'error'"
            )
        return ProviderResult(
            text=entry["text"],
            model=request.model,
            prompt_tokens=entry.get("prompt_tokens"),
            completion_tokens=entry.get("completion_tokens"),
            latency_ms=entry.get("latency_ms"),
            raw={"fixture": True},
        )

    def describe(self) -> dict:
        return {
            "name": self.name,
            "fixtures_path": self.fixtures_path,
            "fixtures_sha256": self.fixtures_sha256,
        }


register_provider("fake", FakeProvider)
