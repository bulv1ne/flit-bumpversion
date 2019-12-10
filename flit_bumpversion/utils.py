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


def increase_version_number(version_number: str, version_part: VersionPart) -> str:
    version_split = list(map(int, version_number.split(".")))

    if len(version_split) == 2:
        version_split.append(0)

    if version_part is VersionPart.PATCH:
        version_split[2] += 1
    elif version_part is VersionPart.MINOR:
        version_split[1] += 1
        version_split[2] = 0
    elif version_part is VersionPart.MAJOR:
        version_split[0] += 1
        version_split[1] = 0
        version_split[2] = 0

    return ".".join(map(str, version_split))


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
