import subprocess
import sys
from enum import Enum
from pathlib import Path


class VersionPart(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"

    def __str__(self):
        return self.value


def file_path(value):
    p = Path(value)
    if p.is_dir():
        p /= "__init__.py"
    if not p.exists():
        raise ValueError(f"File {value} doesn't exist")
    return p


def sh(*args, **kwargs):
    kwargs.setdefault("stdin", sys.stdin)
    kwargs.setdefault("stdout", sys.stdout)
    kwargs.setdefault("stderr", sys.stderr)
    kwargs.setdefault("check", True)
    return subprocess.run(args, **kwargs)
