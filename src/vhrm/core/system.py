from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import psutil


@dataclass(slots=True)
class Check:
    name: str
    status: str
    detail: str


def _run(*cmd: str) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=8, check=False)
        return p.returncode, (p.stdout or p.stderr).strip()
    except Exception as exc:
        return 1, str(exc)


def os_release() -> dict[str, str]:
    data: dict[str, str] = {}
    try:
        for line in Path("/etc/os-release").read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                data[k] = v.strip().strip('"')
    except OSError:
        pass
    return data


def summary() -> dict[str, str]:
    rel = os_release()
    vm = psutil.virtual_memory()
    root = psutil.disk_usage("/")
    return {
        "host": platform.node() or "unknown",
        "os": rel.get("PRETTY_NAME", platform.platform()),
        "kernel": platform.release(),
        "cpu": f"{psutil.cpu_count(logical=True) or 0} logical CPUs",
        "ram": f"{vm.total / (1024**3):.1f} GiB",
        "root": f"{root.free / (1024**3):.1f} GiB free / {root.total / (1024**3):.1f} GiB",
    }


def block_devices() -> list[dict[str, str]]:
    rc, out = _run("lsblk", "-J", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL,UUID")
    if rc:
        return []
    import json

    try:
        raw = json.loads(out)
    except json.JSONDecodeError:
        return []

    devices: list[dict[str, str]] = []
    for d in raw.get("blockdevices", []):
        devices.append({
            "name": str(d.get("name") or ""),
            "size": str(d.get("size") or ""),
            "type": str(d.get("type") or ""),
            "fstype": str(d.get("fstype") or "-"),
            "mount": ", ".join(d.get("mountpoints") or []) or "-",
            "model": str(d.get("model") or "-").strip(),
            "uuid": str(d.get("uuid") or "-"),
        })
    return devices


def service_state(name: str) -> str:
    if not shutil.which("systemctl"):
        return "n/a"
    rc, out = _run("systemctl", "is-active", name)
    return out if out else ("active" if rc == 0 else "inactive")


def firewall_backend() -> str:
    for cmd in ("ufw", "firewall-cmd", "iptables"):
        if shutil.which(cmd):
            return cmd
    return "none"


def audit(repo_path: str = "/mnt/veeamrepo") -> list[Check]:
    rel = os_release()
    ubuntu_version = rel.get("VERSION_ID", "")
    supported = rel.get("ID") == "ubuntu" and ubuntu_version in {"20.04", "22.04", "24.04", "26.04"}

    checks = [
        Check("Supported Ubuntu target", "PASS" if supported else "WARN", rel.get("PRETTY_NAME", "Unknown OS")),
        Check("Firewall manager", "PASS" if firewall_backend() != "none" else "WARN", firewall_backend()),
        Check("SSH service", "INFO", service_state("ssh")),
        Check("Veeam transport", "INFO", service_state("veeamtransport")),
        Check("Veeam immutability service", "INFO", service_state("veeamimmureposvc")),
    ]

    path = Path(repo_path)
    if path.exists():
        st = path.stat()
        mode = oct(st.st_mode & 0o777)
        checks.append(Check("Repository path", "PASS", str(path)))
        checks.append(Check("Repository permissions", "PASS" if mode == "0o700" else "WARN", mode))
        rc, out = _run("findmnt", "-no", "FSTYPE", "--target", str(path))
        fs = out.strip() if rc == 0 else "unknown"
        checks.append(Check("Repository filesystem", "PASS" if fs == "xfs" else "WARN", fs))
    else:
        checks.append(Check("Repository path", "WARN", f"{path} does not exist"))

    return checks
