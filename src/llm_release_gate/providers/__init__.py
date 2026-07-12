"""Provider interface + registry.

A provider turns one rendered request into one response. It reports what it
actually knows: token counts and latency are Optional — a provider that cannot
measure them returns None, and downstream cost/latency metrics become
"unavailable" rather than guessed.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Optional

from ..errors import GateConfigError


@dataclass
class ProviderRequest:
    model: str
    system: str
    prompt: str
    params: dict
    item_id: str          # replay key: lets record/replay providers look up fixtures
    metadata: dict = field(default_factory=dict)


@dataclass
class ProviderResult:
    text: str
    model: str
    prompt_tokens: Optional[int] = None      # None = provider did not report; never guessed
    completion_tokens: Optional[int] = None
    latency_ms: Optional[float] = None
    raw: dict = field(default_factory=dict)


class Provider(ABC):
    """One provider instance is built per run config from its provider_options."""

    name: str = "abstract"

    @abstractmethod
    def complete(self, request: ProviderRequest) -> ProviderResult:
        """Execute one request. Raise ProviderError on failure — the runner records
        the failure on the item and continues; it never invents a response."""

    def describe(self) -> dict:
        """Identity block recorded in the run manifest."""
        return {"name": self.name}


_REGISTRY: dict[str, Callable[[dict, str], Provider]] = {}


def register_provider(name: str, factory: Callable[[dict, str], Provider]) -> None:
    """factory(provider_options, base_dir) -> Provider. base_dir resolves relative paths
    in options against the config file's directory."""
    _REGISTRY[name] = factory


def build_provider(name: str, options: dict, base_dir: str) -> Provider:
    if name not in _REGISTRY:
        raise GateConfigError(
            f"unknown provider '{name}'; registered providers: {sorted(_REGISTRY)}"
        )
    return _REGISTRY[name](options, base_dir)


# Register built-ins on import.
from . import fake as _fake  # noqa: E402,F401
