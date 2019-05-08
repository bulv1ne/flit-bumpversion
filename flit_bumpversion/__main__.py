#!/usr/bin/env python
import argparse
import re
from pathlib import Path

import sh


def file_path(value):
    p = Path(value)
    if p.is_dir():
        p /= "__init__.py"
    if not p.exists():
        raise ValueError(f"File {value} doesn't exist")
    return p


def cli():
    parser = argparse.ArgumentParser(prog="flit-bumpversion")
    parser.add_argument("version_part", choices=["major", "minor", "patch"])
    parser.add_argument("base_file", type=file_path)
    args = parser.parse_args()
    re_version = re.compile(
        r"__version__\s*=\s*(?P<quote>\"|')(?P<version>\d+\.\d+(\.\d+)?)(\"|')"
    )
    file_text = args.base_file.read_text()
    match = re_version.search(file_text)
    if not match:
        print(f"Couldn't find __version__ in {args.base_file}")
        return

    quote = match.group("quote")
    old_version = match.group("version")
    version = list(map(int, old_version.split(".")))

    if len(version) == 2:
        version.append(0)
    if args.version_part == "patch":
        version[2] += 1
    elif args.version_part == "minor":
        version[1] += 1
        version[2] = 0
    elif args.version_part == "major":
        version[0] += 1
        version[1] = 0
        version[2] = 0

    version = ".".join(map(str, version))
    new_file_text = re_version.sub(f"__version__ = {quote}{version}{quote}", file_text)

    args.base_file.write_text(new_file_text)

    try:
        sh.git.commit(
            p=True, m=f"Bump version from v{old_version} to v{version}", _fg=True
        )
    except sh.ErrorReturnCode_1:
        return
    sh.git.tag(f"v{version}")


if __name__ == "__main__":
    cli()
