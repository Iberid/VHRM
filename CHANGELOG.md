# Changelog

## Unreleased

### Added
- Multilingual documentation: English, Spanish, Brazilian Portuguese and Simplified Chinese.
- In-application language selector for English, Español, Português (Brasil) and 中文（简体）.
- Persistent language preference stored in `~/.config/vhrm/config.json`.
- Centralized translation layer in `src/vhrm/i18n.py` with English fallback for future languages.

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
