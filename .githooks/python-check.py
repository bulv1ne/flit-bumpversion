#!/usr/bin/env python
import asyncio
import sys


async def cli_async():
    returncodes = await asyncio.gather(
        run("isort", "--check-only", "--diff", "--quiet"),
        run("black", "--check", "--exclude", "node_modules", "."),
        run("flake8"),
    )
    sys.exit(max(returncodes))


async def run(*args, **kwargs):
    kwargs.setdefault("stdout", asyncio.subprocess.PIPE)
    kwargs.setdefault("stderr", asyncio.subprocess.PIPE)
    proc = await asyncio.create_subprocess_exec(*args, **kwargs)

    stdout, stderr = await proc.communicate()

    print(f"[{' '.join(args)!r} exited with {proc.returncode}]")
    if proc.returncode:
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
    return proc.returncode


if __name__ == "__main__":
    asyncio.run(cli_async())
