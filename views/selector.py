from textual.app import ComposeResult
from textual.widgets import DataTable, Header, Footer
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets._data_table import RowKey

from models import get_projects, ProjectEntry
from views.timer import TimerView


class ProjectSelectorView(Screen):
    table: DataTable
    projects_rows: dict[RowKey, ProjectEntry] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            table = DataTable(zebra_stripes=True)
            table.cursor_type = "row"
            table.add_columns("Date", "Project", "Client")
            self.table = table
            yield table
        yield Footer()

    def on_mount(self):
        projects = get_projects()

        for p in projects:
            row_key = self.table.add_row(p.date.strftime("%Y-%m-%d"), p.name, p.client)
            self.projects_rows[row_key] = p

        self.table.focus()

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        project = self.projects_rows.get(event.row_key)
        self.app.push_screen(TimerView(project))
