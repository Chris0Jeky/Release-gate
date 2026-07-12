import json

import pytest

from llm_release_gate.hashing import canonical_json, content_hash, file_sha256


def test_key_order_does_not_change_hash():
    a = {"b": 1, "a": {"y": 2, "x": [1, 2, 3]}}
    b = {"a": {"x": [1, 2, 3], "y": 2}, "b": 1}
    assert content_hash(a) == content_hash(b)


def test_value_change_changes_hash():
    assert content_hash({"a": 1}) != content_hash({"a": 2})


def test_list_order_matters():
    assert content_hash({"a": [1, 2]}) != content_hash({"a": [2, 1]})


def test_unicode_stable():
    obj = {"vendor": "Café Lumière", "note": "über"}
    assert content_hash(obj) == content_hash(json.loads(canonical_json(obj)))


def test_nan_rejected():
    with pytest.raises(ValueError):
        canonical_json({"x": float("nan")})


def test_hash_format():
    digest = content_hash({})
    assert digest.startswith("sha256:") and len(digest) == 7 + 64


def test_file_sha256_matches_bytes(tmp_path):
    p = tmp_path / "f.json"
    p.write_bytes(b'{"a": 1}')
    import hashlib
    assert file_sha256(str(p)) == "sha256:" + hashlib.sha256(b'{"a": 1}').hexdigest()
