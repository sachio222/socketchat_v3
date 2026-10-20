"""Bug 2: config/prv/keys/hashes.json is no longer in the repo, and passtools
tried to write it into a folder that doesn't exist at import time."""
import importlib
import json
import os

import pytest

from handlers.routers import DefaultCmds


@pytest.fixture
def empty_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def fresh_passtools():
    from chatutils import passtools
    return importlib.reload(passtools)


def feed_input(monkeypatch, answers):
    answers = iter(answers)
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(answers))


def test_passtools_imports_without_keys_folder(empty_dir):
    assert not os.path.exists(empty_dir / "config" / "prv")
    passtools = fresh_passtools()
    assert passtools.hash_json.dict == {}


def test_hackmyserver_without_hash_says_so(empty_dir, monkeypatch, capsys):
    fresh_passtools()

    feed_input(monkeypatch, ["n"])
    DefaultCmds.cli(sock=None, msg_parts=["/hackmyserver"])

    out = capsys.readouterr().out
    assert "No password set" in out


def test_hackmyserver_without_hash_can_set_one(empty_dir, monkeypatch):
    passtools = fresh_passtools()

    feed_input(monkeypatch, ["y", "opensesame", "opensesame"])
    DefaultCmds.cli(sock=None, msg_parts=["/hackmyserver"])

    with open(empty_dir / "config" / "prv" / "keys" / "hashes.json") as f:
        stored = json.load(f)
    assert stored["cli"].startswith("$argon2")
    assert passtools.password_verify("cli", "opensesame")
    assert not passtools.password_verify("cli", "wrong")
