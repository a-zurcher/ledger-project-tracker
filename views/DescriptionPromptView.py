import os

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Input, Static, Button

from models import ProjectEntry, ledger_time_file


class DescriptionPromptView(Screen):
    BINDINGS = [("submit", "save_project", "Save to ledger file")]

    CSS = """
        Input { width: 52; }
    """

    input: Input
    save_button: Button

    def __init__(self, project: ProjectEntry):
        super().__init__(name='description_prompt')
        self.project = project

        # widgets
        self.input = Input()
        self.input.action_submit = self.action_save_project

        self.save_button = Button("Save", id="save_btn")
        self.save_button.action_submit = self.action_save_project


    def compose(self) -> ComposeResult:
        with Container(classes="auto-size app-container"):
            yield Static("Enter a description for this task:")
            yield self.input
            yield self.save_button

    def on_mount(self):
        self.input.focus()

    def action_save_project(self):
        self.project.set_description(self.input.value)

        if not ledger_time_file:
            self.app.exit("LEDGER_TIME_FILE not set")
        with open(ledger_time_file, "a") as f:
            f.write("\n" + self.project.to_ledger())
        self.app.exit()
