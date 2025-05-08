from dataclasses import dataclass

from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import DataTable, Button, Label
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets._data_table import RowKey, ColumnKey

from models import get_projects, ProjectEntry
from views.CreateProjectView import CreateProjectView
from views.TimerView import TimerView


@dataclass
class SortedTableHeader:
    label: str
    sort_reversed: bool = False

class ProjectSelectorView(Screen):
    CSS = """
        #project-selector { width: 100%; }
        #title { margin-bottom: 1; }
        DataTable { max-width: 100%!important; margin-bottom: 1; } 
    """

    table: DataTable
    create_new_project_button: Button = Button("Create new project", id="create_new_project")

    columns: list[ColumnKey]

    # used to manage sorting
    table_headers: list[SortedTableHeader] = [
        SortedTableHeader("Date"),
        SortedTableHeader("Client"),
        SortedTableHeader("Project")
    ]

    # stores all the projects in a dict as values with RowKey as keys
    table_rows: dict[RowKey, ProjectEntry] = {}



    def __init__(self):
        super().__init__(name='project_selector')

        table = DataTable(zebra_stripes=True)
        table.cursor_type = "row"
        self.columns = table.add_columns(*[x.label for x in self.table_headers])
        self.table = table

    def compose(self) -> ComposeResult:
        with Vertical(id="project-selector", classes="auto-size app-container"):
            yield Label(Text("Project tracking", style="bold"), id="title")
            yield self.table
            yield self.create_new_project_button

    def on_mount(self):
        projects = get_projects()

        for p in projects:
            row_key = self.table.add_row(p.date.strftime("%Y-%m-%d"), p.client, p.name)
            self.table_rows[row_key] = p

        # sort by date, then company, then project name
        self.table.sort(*self.columns, reverse=True)
        self.table.focus()

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected):
        """Sort the table by the selected column header"""
        header: SortedTableHeader = self.table_headers[event.column_index]
        header.sort_reversed = not header.sort_reversed
        column = self.columns[event.column_index]
        self.table.sort(column, reverse=header.sort_reversed)

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        project = self.table_rows.get(event.row_key)
        self.app.push_screen(TimerView(project))

    def on_button_pressed(self):
        self.app.push_screen(CreateProjectView())
