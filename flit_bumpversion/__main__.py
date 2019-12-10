#!/usr/bin/env python
import argparse
import re
import subprocess
import sys

from . import __version__
from .utils import VersionPart, file_path, sh


def cli():
    parser = argparse.ArgumentParser(prog="flit-bumpversion")
    parser.add_argument(
        "version_part", choices=list(VersionPart), type=VersionPart,
    )
    parser.add_argument("base_file", type=file_path)
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()
    re_version = re.compile(
        r"__version__\s*=\s*(?P<quote>\"|')(?P<version>\d+\.\d+(\.\d+)?)(\"|')"
    )
    file_text = args.base_file.read_text()
    match = re_version.search(file_text)
    if not match:
        print(f"Couldn't find __version__ in {args.base_file}")
        sys.exit(1)

    quote = match.group("quote")
    old_version = match.group("version")
    version = list(map(int, old_version.split(".")))

    if len(version) == 2:
        version.append(0)
    if args.version_part is VersionPart.PATCH:
        version[2] += 1
    elif args.version_part is VersionPart.MINOR:
        version[1] += 1
        version[2] = 0
    elif args.version_part is VersionPart.MAJOR:
        version[0] += 1
        version[1] = 0
        version[2] = 0

    version = ".".join(map(str, version))
    new_file_text = re_version.sub(f"__version__ = {quote}{version}{quote}", file_text)

    args.base_file.write_text(new_file_text)

    try:
        sh(
            "git",
            "commit",
            "-p",
            "-m",
            f"Bump version from v{old_version} to v{version}",
        )
    except subprocess.CalledProcessError:
        print("Aborted!")
        sys.exit(1)
    sh("git", "tag", f"v{version}")


if __name__ == "__main__":
    cli()
