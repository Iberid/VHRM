from __future__ import annotations

import shlex
from dataclasses import dataclass


@dataclass(slots=True)
class PlannedCommand:
    title: str
    command: list[str]
    dangerous: bool = False

    def shell(self) -> str:
        return " ".join(shlex.quote(x) for x in self.command)


def build_repository_plan(device: str, mountpoint: str, username: str) -> list[PlannedCommand]:
    """Return a reviewable plan. VHRM intentionally does not auto-run destructive commands."""
    return [
        PlannedCommand("Create repository user", ["useradd", "--create-home", "--shell", "/bin/bash", username]),
        PlannedCommand("Create XFS filesystem", ["mkfs.xfs", "-f", device], dangerous=True),
        PlannedCommand("Create mountpoint", ["mkdir", "-p", mountpoint]),
        PlannedCommand("Mount repository", ["mount", device, mountpoint]),
        PlannedCommand("Set ownership", ["chown", f"{username}:{username}", mountpoint]),
        PlannedCommand("Set repository permissions", ["chmod", "0700", mountpoint]),
    ]
