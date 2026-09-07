# Architecture

VHRM separates presentation from privileged operating-system actions.

```text
Textual TUI
   |
   +-- core.system   -> read-only host/storage/security discovery
   |
   +-- core.plan     -> deterministic provisioning command plans
   |
   +-- future executor -> explicit privileged apply mode + audit log
```

## Design principles

1. Read-first: inspection must work without changing the host.
2. Explicit risk: destructive operations are visually and logically separated.
3. Deterministic plans: an operator can review commands before execution.
4. Least privilege: normal dashboard operation should not require root.
5. Observable changes: future apply mode must record what was changed.
6. Vendor-aware, not vendor-dependent: VHRM assists preparation and audit; Veeam remains the source of truth for product requirements.
