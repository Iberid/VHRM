from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import DataTable, Footer, Header, Select, Static, TabbedContent, TabPane

from . import __version__
from .core.system import audit, block_devices, summary
from .i18n import SUPPORTED_LANGUAGES, load_language, save_language, tr


CSS = """
Screen { background: #0b1017; }
Header { background: #111a24; color: #e9f2ff; }
Footer { background: #111a24; }
#hero { height: 7; padding: 1 2; background: #111a24; border: round #2f81f7; }
#language-row { height: 5; padding: 0 2; align: right middle; }
#language-label { width: auto; padding: 1 1; color: #8b949e; }
#language-select { width: 28; }
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
    CSS = CSS
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh_data", "Refresh"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.language = load_language()
        self.TITLE = tr(self.language, "app_title")
        self.SUB_TITLE = f"v{__version__}"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll():
            yield Static(id="hero")
            with Horizontal(id="language-row"):
                yield Static(id="language-label")
                yield Select(
                    [(label, code) for code, label in SUPPORTED_LANGUAGES.items()],
                    value=self.language,
                    allow_blank=False,
                    id="language-select",
                )
            with Horizontal(id="cards"):
                yield Static(id="card-system", classes="card")
                yield Static(id="card-security", classes="card")
                yield Static(id="card-veeam", classes="card")
            with TabbedContent(initial="audit"):
                with TabPane(tr(self.language, "security_audit"), id="audit"):
                    yield DataTable(id="audit-table", zebra_stripes=True)
                with TabPane(tr(self.language, "storage"), id="storage"):
                    yield DataTable(id="disk-table", zebra_stripes=True)
                with TabPane(tr(self.language, "about"), id="about"):
                    yield Static(id="about-text")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_localized_ui()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id != "language-select" or event.value is Select.BLANK:
            return
        language = str(event.value)
        if language == self.language:
            return
        self.language = language
        save_language(language)
        self.TITLE = tr(language, "app_title")
        self.refresh_localized_ui()
        self.notify(SUPPORTED_LANGUAGES[language])

    def action_refresh_data(self) -> None:
        self.refresh_localized_ui()

    def refresh_localized_ui(self) -> None:
        language = self.language

        self.query_one("#hero", Static).update(
            f"[b #7ee787]VHRM[/]  {tr(language, 'manager_title')}\n"
            f"[dim]{tr(language, 'hero_subtitle')}[/]"
        )
        self.query_one("#language-label", Static).update(f"{tr(language, 'language')}:")
        self.query_one("#about-text", Static).update(tr(language, "about_text"))

        s = summary()
        self.query_one("#card-system", Static).update(
            f"[b #58a6ff]{tr(language, 'system')}[/]\n{s['host']}\n{s['os']}\nKernel {s['kernel']}"
        )

        checks = audit()
        pass_count = sum(c.status == "PASS" for c in checks)
        warn_count = sum(c.status == "WARN" for c in checks)
        self.query_one("#card-security", Static).update(
            f"[b #58a6ff]{tr(language, 'audit')}[/]\n"
            f"[green]{pass_count} {tr(language, 'pass')}[/] · "
            f"[yellow]{warn_count} {tr(language, 'warnings')}[/]\n"
            f"{tr(language, 'refresh_hint')}"
        )

        veeam = [c for c in checks if c.name.startswith("Veeam")]
        vtext = "\n".join(f"{c.name.replace('Veeam ', '')}: {c.detail}" for c in veeam)
        self.query_one("#card-veeam", Static).update(
            f"[b #58a6ff]{tr(language, 'veeam')}[/]\n{vtext or tr(language, 'not_detected')}"
        )

        at = self.query_one("#audit-table", DataTable)
        at.clear(columns=True)
        at.add_columns(tr(language, "status"), tr(language, "check"), tr(language, "detail"))
        for c in checks:
            at.add_row(c.status, c.name, c.detail)

        dt = self.query_one("#disk-table", DataTable)
        dt.clear(columns=True)
        dt.add_columns(
            tr(language, "device"),
            tr(language, "size"),
            tr(language, "type"),
            tr(language, "filesystem"),
            tr(language, "mount"),
            tr(language, "model"),
        )
        for d in block_devices():
            dt.add_row(d["name"], d["size"], d["type"], d["fstype"], d["mount"], d["model"])


def main() -> None:
    VHRMApp().run()


if __name__ == "__main__":
    main()
