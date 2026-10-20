"""Bug 1: a fresh clone has no config/config.json, so everything that reads
configs.dict["system"] blew up with KeyError: 'system'."""
import json
import os
import shutil
import subprocess
import sys

from conftest import FRESH, make_fresh_copy


def test_missing_config_seeds_from_defaults(tmp_path, monkeypatch):
    os.makedirs(tmp_path / "config")
    shutil.copy(os.path.join(FRESH, "config", "configDefaults.json"),
                tmp_path / "config" / "configDefaults.json")
    monkeypatch.chdir(tmp_path)

    from chatutils import utils
    configs = utils.JSONLoader()

    with open(tmp_path / "config" / "configDefaults.json") as f:
        defaults = json.load(f)

    assert configs.dict == defaults
    assert configs.dict["system"]["defaultHost"] == "127.0.0.1"
    with open(tmp_path / "config" / "config.json") as f:
        assert json.load(f) == defaults


def test_existing_config_is_left_alone(tmp_path, monkeypatch):
    os.makedirs(tmp_path / "config")
    shutil.copy(os.path.join(FRESH, "config", "configDefaults.json"),
                tmp_path / "config" / "configDefaults.json")
    with open(tmp_path / "config" / "config.json", "w") as f:
        json.dump({"cipher": "chacha"}, f)
    monkeypatch.chdir(tmp_path)

    from chatutils import utils
    assert utils.JSONLoader().dict == {"cipher": "chacha"}


def test_fresh_clone_imports_client_and_server(tmp_path):
    """Import both entry points from a clean copy, in a clean interpreter."""
    clone = make_fresh_copy(str(tmp_path / "clone"))
    for module in ("client", "server"):
        result = subprocess.run([sys.executable, "-c", f"import {module}"],
                                cwd=clone,
                                capture_output=True,
                                text=True,
                                timeout=60)
        assert result.returncode == 0, f"import {module}:\n{result.stderr}"
