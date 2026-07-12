"""Report renderers + shared formatting.

Formatting rules all renderers obey:
- rates print counts next to the percentage: "7/8 (87.5%)" — never a bare rate
- heuristic scores are marked and footnoted as heuristics, never presented as
  probabilities or model-judged accuracy
- unavailable values print "unavailable" plus the reason; no substitution
"""

from __future__ import annotations

HEURISTIC_FOOTNOTE = (
    "heuristic rule-based score (keyword/pattern checks) — a proxy signal, "
    "not a probability or human-judged accuracy"
)


def fmt_value(m: dict) -> str:
    """Human formatting for one MetricValue dict."""
    if not m["available"]:
        return "unavailable"
    unit = m["unit"]
    if unit == "rate":
        return f"{m['numerator']}/{m['denominator']} ({m['value'] * 100:.1f}%)"
    if unit == "usd":
        return f"${m['value']:.6f}"
    if unit == "ms":
        return f"{m['value']:.0f} ms"
    if unit == "tokens":
        return f"{m['value']:,.0f}"
    return f"{m['value']:.6g}"


def fmt_delta(entry: dict) -> str:
    delta = entry.get("delta")
    if delta is None:
        return "—"
    m = entry["candidate"]
    abs_part = {
        "rate": lambda v: f"{v * 100:+.1f}pp",
        "usd": lambda v: f"{v:+.6f}",
        "ms": lambda v: f"{v:+.0f} ms",
        "tokens": lambda v: f"{v:+,.0f}",
    }.get(m["unit"], lambda v: f"{v:+.6g}")(delta["abs"])
    if delta["pct"] is not None and m["unit"] != "rate":
        return f"{abs_part} ({delta['pct']:+.1f}%)"
    return abs_part


def is_heuristic(m: dict) -> bool:
    return m.get("kind") == "heuristic_rate"


def verdict_word(verdict: str) -> str:
    return {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "skipped": "SKIPPED"}.get(
        verdict, verdict.upper()
    )
