# VHRM — Veeam Hardened Repository Manager

A modern, open-source terminal interface for auditing and preparing Linux systems used as **Veeam Hardened Repositories**.

> **Status:** early community release / technical preview. Use in labs first. Storage changes must always be validated by an administrator.

## Why this project exists

VHRM is inspired by the workflow of [`tdewin/veeamhubrepo`](https://github.com/tdewin/veeamhubrepo), an MIT-licensed project created to quickly prepare Linux immutable repositories for Veeam lab environments.

Instead of extending its 2021 `dialog`-based implementation, VHRM is an **independent reimplementation** focused on a current, maintainable UX and a read-first security model.

## What is improved

| Area | veeamhubrepo approach | VHRM approach |
|---|---|---|
| Interface | classic dialog wizard | modern Textual TUI dashboard |
| Target baseline | Ubuntu 20.04 / Veeam V11 era | Ubuntu 20.04/22.04/24.04/26.04 awareness |
| Safety | setup wizard performs changes | read-first audit; destructive commands are plans |
| Visibility | menus and dialogs | live system/security/storage dashboard |
| Architecture | large procedural script | UI separated from system/audit/planning logic |
| Repository checks | setup-oriented | XFS, permissions, SSH/firewall and Veeam service audit |
| Maintenance | pinned 2020-era dependencies | modern Python packaging (`pyproject.toml`) |

## Current features

- Modern keyboard-driven terminal dashboard.
- Linux distribution, kernel, CPU, RAM and root filesystem summary.
- Block-device inventory through `lsblk`.
- Security/readiness audit for:
  - supported Ubuntu target awareness;
  - firewall manager presence;
  - SSH service state;
  - Veeam transport and immutability service state;
  - repository directory presence;
  - `0700` repository permissions;
  - XFS filesystem detection.
- Reviewable repository provisioning plan generator.
- No automatic formatting of disks in v0.1.0.

## Install

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip xfsprogs
python3 -m venv .venv
source .venv/bin/activate
pip install .
vhrm
```

## Recommended operating model

VHRM does **not** replace the Veeam documentation or the Veeam Infrastructure Appliance. For manually configured Linux repositories, validate the host against the current Veeam Backup & Replication requirements before production use.

For a hardened repository, use dedicated block storage and prefer XFS where Fast Clone is required. Repository ownership/permissions, single-use credentials, firewall policy, SSH lifecycle and Veeam services should be reviewed as part of change control.

## Roadmap

- [ ] Guided repository provisioning with an explicit two-step destructive confirmation.
- [ ] Device fingerprinting (serial/WWN) before format operations.
- [ ] XFS/Reflink validation.
- [ ] UFW/firewalld policy inspector.
- [ ] SSH exposure timer and post-onboarding lockdown helper.
- [ ] Veeam component/port diagnostics.
- [ ] Repository capacity and inode trends.
- [ ] JSON audit export for RMM/SIEM ingestion.
- [ ] Debian/RHEL/Rocky profiles where supported by current Veeam releases.
- [ ] `.deb` packaging and GitHub Actions release pipeline.

## Attribution

The original idea and workflow inspiration came from:

- **veeamhubrepo** by Thomas De Win (`tdewin`) — https://github.com/tdewin/veeamhubrepo

VHRM does not copy the original Python implementation. It is a clean, independently structured implementation inspired by the same operational problem.

## Disclaimer

Veeam® is a trademark of Veeam Software Group GmbH. This community project is not affiliated with, sponsored by, or endorsed by Veeam Software.

Disk formatting, filesystem creation, firewall changes and account changes can cause data loss or loss of access. Validate all commands and test in a non-production environment first.

## License

MIT. See [LICENSE](LICENSE).
