#!/usr/bin/env python
import argparse
import re
import shlex
import subprocess
import sys

from . import __version__
from .utils import (
    VersionPart,
    file_path,
    get_default_module_file,
    increase_version_number,
    sh,
)


def cli():
    parser = argparse.ArgumentParser(prog="flit-bumpversion")
    parser.add_argument(
        "version_part", choices=list(VersionPart), type=VersionPart,
    )
    parser.add_argument(
        "base_file",
        type=file_path,
        default=None,
        nargs="?",
        help="omitting this argument will look into the pyproject.toml file for the default module",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="don't change any files or execute any git commands, only show what would be done/changed",
    )

    args = parser.parse_args()

    base_file = args.base_file
    if base_file is None:
        base_file = get_default_module_file()

    re_version = re.compile(
        r"__version__\s*=\s*(?P<quote>\"|')(?P<version>\d+\.\d+(\.\d+)?)(\"|')"
    )
    file_text = base_file.read_text()
    match = re_version.search(file_text)
    if not match:
        print(f"Couldn't find __version__ in {base_file}")
        sys.exit(1)

    quote = match.group("quote")
    old_version = match.group("version")
    version = increase_version_number(old_version, args.version_part)

    print(f"Bumping version {old_version} to {version} in file {base_file}")
    if not args.dry_run:
        new_file_text = re_version.sub(
            f"__version__ = {quote}{version}{quote}", file_text
        )
        base_file.write_text(new_file_text)

    execute_command(
        "git",
        "commit",
        "-p",
        "-m",
        f"Bump version from v{old_version} to v{version}",
        dry_run=args.dry_run,
    )
    execute_command("git", "tag", f"v{version}", dry_run=args.dry_run)


def execute_command(*args, dry_run):
    # args = [shlex.quote(part) for part in args]
    print(" ".join(["$", *map(shlex.quote, args)]))
    if not dry_run:
        try:
            sh(*args)
        except subprocess.CalledProcessError:
            print("Aborted!")
            sys.exit(1)


if __name__ == "__main__":
    cli()
