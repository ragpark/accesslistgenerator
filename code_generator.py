"""Core code generation logic for access codes."""

from __future__ import annotations

import random
from typing import Iterable

# Avoid vowels so generated strings are unlikely to form words.
ALPHABET = "BCDFGHJKLMNPQRSTVWXYZ"
CODE_LENGTH = 5

# Extra guardrail against accidental rude content.
BLOCKED_SEQUENCES = {
    "ASS",
    "SEX",
    "FUK",
    "FUC",
    "CUM",
    "DCK",
    "CNT",
    "PNS",
    "TTS",
    "SHT",
    "FK",
}


def is_allowed(code: str, blocked: Iterable[str] = BLOCKED_SEQUENCES) -> bool:
    """Return True if code does not contain blocked sequences."""
    upper_code = code.upper()
    return not any(bad in upper_code for bad in blocked)


def generate_codes(count: int, *, seed: int | None = None) -> list[str]:
    """Generate `count` unique, safe-for-work codes."""
    if count < 1:
        raise ValueError("count must be at least 1")

    # Possible unique combinations with this alphabet + code length.
    max_codes = len(ALPHABET) ** CODE_LENGTH
    if count > max_codes:
        raise ValueError(f"count must be <= {max_codes}")

    rng = random.Random(seed)
    codes: set[str] = set()

    while len(codes) < count:
        candidate = "".join(rng.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if is_allowed(candidate):
            codes.add(candidate)

    return sorted(codes)
