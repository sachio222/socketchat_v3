"""Test setup.

The app reads and writes config, keys and the user dict relative to the
working directory, and a lot of it happens at import time. So the tests run
inside a throwaway copy of the repo, the way a fresh clone looks: no
config.json, no userDict.json, no config/prv. Nothing gets written into your
checkout.
"""
import atexit
import os
import shutil
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP = shutil.ignore_patterns(".git", "tests", "__pycache__", "*.pyc",
                              "config.json", "userDict.json", "prv", "venv",
                              ".venv", "downloads", "data")


def make_fresh_copy(dest: str) -> str:
    """Copies the repo into dest without any local state."""
    shutil.copytree(REPO, dest, ignore=SKIP)
    return dest


FRESH = make_fresh_copy(os.path.join(tempfile.mkdtemp(prefix="socketchat-"),
                                     "socketchat_v3"))
atexit.register(shutil.rmtree, os.path.dirname(FRESH), True)

os.chdir(FRESH)
sys.path.insert(0, FRESH)
