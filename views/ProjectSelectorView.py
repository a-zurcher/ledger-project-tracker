from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import DataTable, Header, Footer, Button, Label
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets._data_table import RowKey

from models import get_projects, ProjectEntry
from views.CreateProjectView import CreateProjectView


class ProjectSelectorView(Screen):
    CSS = """
        Vertical { max-width: 100; }
        #title { margin-bottom: 1; }
        DataTable { margin-bottom: 1; }
    """

    table: DataTable
    projects_rows: dict[RowKey, ProjectEntry] = {}
    create_new_project_button: Button = Button("Create new project", id="create_new_project")

    def __init__(self):
        super().__init__(name='project_selector')

        table = DataTable(zebra_stripes=True)
        table.cursor_type = "row"
        table.add_columns("Date", "Project", "Client")
        self.table = table

    def compose(self) -> ComposeResult:
        with Vertical(classes="auto-size"):
            yield Label(Text("Project tracking", style="bold"), id="title")
            yield self.table
            yield self.create_new_project_button

    def on_mount(self):
        projects = get_projects()

        for p in projects:
            row_key = self.table.add_row(p.date.strftime("%Y-%m-%d"), p.name, p.client)
            self.projects_rows[row_key] = p

        self.table.focus()

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        from views.TimerView import TimerView

        project = self.projects_rows.get(event.row_key)
        self.app.push_screen(TimerView(project))

    def on_button_pressed(self):
        self.app.push_screen(CreateProjectView())
