#!/usr/bin/env python3
"""Install the canonical Abandon Skill for supported local agent hosts."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "skills" / "abandon-slop"
TARGETS = {
    "claude": Path.home() / ".claude" / "skills" / "abandon-slop",
    "agents": Path.home() / ".agents" / "skills" / "abandon-slop",
    "codex": Path.home() / ".agents" / "skills" / "abandon-slop",
    "chatgpt": Path.home() / ".agents" / "skills" / "abandon-slop",
    "opencode": Path.home() / ".config" / "opencode" / "skills" / "abandon-slop",
}
ALL_TARGETS = ("claude", "agents")


def remove_destination(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def install(destination: Path, copy: bool, force: bool) -> str:
    destination = destination.expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() and destination.resolve() == SOURCE.resolve() and not copy:
            return "unchanged"
        if not force:
            raise FileExistsError(f"destination exists (use --force): {destination}")
        remove_destination(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if copy:
        shutil.copytree(SOURCE, destination)
        return "copied"
    destination.symlink_to(SOURCE, target_is_directory=True)
    return "linked"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["all", *TARGETS], default="all")
    parser.add_argument("--copy", action="store_true", help="copy instead of symlink")
    parser.add_argument("--force", action="store_true", help="replace an existing destination")
    parser.add_argument("--destination", type=Path, help="install to one custom Agent Skills directory")
    args = parser.parse_args()

    if args.destination:
        destinations = {"custom": args.destination / "abandon-slop"}
    elif args.target == "all":
        destinations = {name: TARGETS[name] for name in ALL_TARGETS}
    else:
        destinations = {args.target: TARGETS[args.target]}

    for host, destination in destinations.items():
        action = install(destination, args.copy, args.force)
        print(f"{host}: {action} {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
