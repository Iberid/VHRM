# Changelog

## 0.1.0 - 2026-09-07

### Added
- New Textual-based terminal UI.
- Dashboard for host, security and Veeam service state.
- Storage inventory using `lsblk`.
- Repository readiness audit for XFS, permissions, firewall and services.
- Current Ubuntu target awareness.
- Review-only provisioning plan API for high-risk storage operations.
- MIT license and explicit attribution to the original veeamhubrepo concept.

### Security design changes
- Destructive storage actions are not executed automatically.
- Audit and discovery are separated from provisioning logic.
- The UI is read-first by default.
