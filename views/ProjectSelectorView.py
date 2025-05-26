from dataclasses import dataclass

from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import DataTable, Button, Label
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets._data_table import RowKey, ColumnKey

from models import get_projects, ProjectEntry, format_time, LedgerTimeFileEnvNotSet
from views.CreateProjectView import CreateProjectView
from views.TimerView import TimerView


@dataclass
class SortedTableHeader:
    label: str
    sort_reversed: bool = False

class ProjectSelectorView(Screen):
    CSS = """
        #project-selector {
            width: 100;
            #title { margin-bottom: 1; }
            DataTable { max-width: 100%!important; margin-bottom: 1; } 
        }
    """

    errors = False
    table: DataTable
    create_new_project_button: Button = Button("Create new project", id="create_new_project")

    columns: list[ColumnKey]

    # used to manage sorting
    table_headers: list[SortedTableHeader] = [
        SortedTableHeader("Date"),
        SortedTableHeader("Client"),
        SortedTableHeader("Project"),
        SortedTableHeader("Hours"),
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
        with Vertical(id="project-selector", classes="auto-size"):
            yield Label(Text("Project tracking", style="bold"), id="title")
            yield self.table
            yield self.create_new_project_button

    def on_mount(self):
        try:
            projects = get_projects()
            max_length_name = 56
            max_length_client = 20

            # focus the "create new project" button if there are no projects in the ledger file
            if len(projects) == 0: self.create_new_project_button.focus()

            for p in projects:
                row_key = self.table.add_row(
                    p.date.strftime("%Y-%m-%d"),
                    p.client[:max_length_client] + (p.client[max_length_client:] and '…'),
                    p.name[:max_length_name] + (p.name[max_length_name:] and '…'),
                    format_time(p.get_time_spend())
                )

                self.table_rows[row_key] = p
        except LedgerTimeFileEnvNotSet as e:
            self.errors = True
            self.notify(message=e.__str__(), title="Critical error !", severity="error", timeout=30)

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
