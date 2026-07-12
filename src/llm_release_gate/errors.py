"""Error taxonomy.

GateConfigError  -> the gate could not run (bad inputs, missing files). CLI exit 2.
ProviderError    -> a single provider call failed. Recorded per item; the run continues
                    and the failure surfaces as errors.error_rate (gate on it if you care).
"""


class GateConfigError(Exception):
    """The gate cannot run as configured. Maps to CLI exit code 2."""


class ProviderError(Exception):
    """A single provider call failed. Recorded on the item, never fabricated over."""
