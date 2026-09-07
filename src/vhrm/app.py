from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import DataTable, Footer, Header, Static, TabbedContent, TabPane

from . import __version__
from .core.system import audit, block_devices, summary


CSS = """
Screen { background: #0b1017; }
Header { background: #111a24; color: #e9f2ff; }
Footer { background: #111a24; }
#hero { height: 7; padding: 1 2; background: #111a24; border: round #2f81f7; }
.brand { text-style: bold; color: #7ee787; }
.muted { color: #8b949e; }
.card { border: round #30363d; padding: 1 2; margin: 1 1; min-width: 28; background: #0d1520; }
.card-title { text-style: bold; color: #58a6ff; }
#cards { height: 10; }
DataTable { height: 1fr; border: round #30363d; }
TabPane { padding: 1; }
.good { color: #7ee787; }
.warn { color: #d29922; }
.info { color: #58a6ff; }
"""


class VHRMApp(App):
    TITLE = "VHRM — Veeam Hardened Repository Manager"
    SUB_TITLE = f"v{__version__}"
    CSS = CSS
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh_data", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll():
            yield Static(
                "[b #7ee787]VHRM[/]  Modern Linux Hardened Repository Manager\n"
                "[dim]Read-first dashboard · security audit · storage visibility · Veeam readiness[/]",
                id="hero",
            )
            with Horizontal(id="cards"):
                yield Static(id="card-system", classes="card")
                yield Static(id="card-security", classes="card")
                yield Static(id="card-veeam", classes="card")
            with TabbedContent(initial="audit"):
                with TabPane("Security audit", id="audit"):
                    yield DataTable(id="audit-table", zebra_stripes=True)
                with TabPane("Storage", id="storage"):
                    yield DataTable(id="disk-table", zebra_stripes=True)
                with TabPane("About", id="about"):
                    yield Static(
                        "VHRM is a community project for auditing and preparing Linux hosts used as "
                        "Veeam Hardened Repositories. It is not affiliated with or endorsed by Veeam Software.\n\n"
                        "Destructive storage actions are intentionally represented as reviewable plans. "
                        "The operator remains responsible for validating device names, backups and change control."
                    )
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_data()

    def action_refresh_data(self) -> None:
        s = summary()
        self.query_one("#card-system", Static).update(
            f"[b #58a6ff]SYSTEM[/]\n{s['host']}\n{s['os']}\nKernel {s['kernel']}"
        )
        checks = audit()
        pass_count = sum(c.status == "PASS" for c in checks)
        warn_count = sum(c.status == "WARN" for c in checks)
        self.query_one("#card-security", Static).update(
            f"[b #58a6ff]AUDIT[/]\n[green]{pass_count} pass[/] · [yellow]{warn_count} warnings[/]\n"
            "Press R to refresh"
        )
        veeam = [c for c in checks if c.name.startswith("Veeam")]
        vtext = "\n".join(f"{c.name.replace('Veeam ', '')}: {c.detail}" for c in veeam)
        self.query_one("#card-veeam", Static).update(f"[b #58a6ff]VEEAM[/]\n{vtext or 'Not detected'}")

        at = self.query_one("#audit-table", DataTable)
        at.clear(columns=True)
        at.add_columns("Status", "Check", "Detail")
        for c in checks:
            at.add_row(c.status, c.name, c.detail)

        dt = self.query_one("#disk-table", DataTable)
        dt.clear(columns=True)
        dt.add_columns("Device", "Size", "Type", "Filesystem", "Mount", "Model")
        for d in block_devices():
            dt.add_row(d["name"], d["size"], d["type"], d["fstype"], d["mount"], d["model"])


def main() -> None:
    VHRMApp().run()


if __name__ == "__main__":
    main()
