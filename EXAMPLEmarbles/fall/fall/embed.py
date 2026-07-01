"""Deterministic offline embeddings — spirit v1, no model download."""

from __future__ import annotations

import hashlib
import math
import struct


DIM = 64


def embed_text(text: str, dim: int = DIM) -> list[float]:
    """Hash n-grams into a unit vector. Review demo, not semantic truth."""
    vec = [0.0] * dim
    normalized = text.lower().strip()
    if not normalized:
        return vec

    for i in range(len(normalized) - 2):
        gram = normalized[i : i + 3]
        digest = hashlib.sha256(gram.encode()).digest()
        idx = int.from_bytes(digest[:4], "big") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vec[idx] += sign

    for token in normalized.split():
        digest = hashlib.sha256(token.encode()).digest()
        idx = int.from_bytes(digest[:4], "big") % dim
        vec[idx] += 1.0

    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


def embedding_to_blob(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def blob_to_embedding(blob: bytes) -> list[float]:
    n = len(blob) // 4
    return list(struct.unpack(f"{n}f", blob))


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    return sum(x * y for x, y in zip(a, b))
