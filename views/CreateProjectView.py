from datetime import datetime

from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.validation import Validator, ValidationResult
from textual.widgets import Input, Button, Label

from models import ProjectEntry
from views.TimerView import TimerView


class ValidateNotEmpty(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value == "":
            return self.failure("Field cannot be empty")
        else:
            return self.success()


class ValidateDate(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value == "":
            return self.failure("Field cannot be empty")
        else:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return self.success()
            except Exception:
                return self.failure("Wrong date format, should be YYYY-MM-DD")



class CreateProjectView(Screen):
    BINDINGS = [("submit", "start_timer_with_new_project", "Create a new project")]

    CSS = """
        #form { margin-bottom: 1; }
        Label { height: auto; }
        Input { width: 52; }
        #submit_btn { margin-right: 1; }
    """

    date_input: Input
    client_input: Input
    project_name_input: Input
    submit_button: Button
    cancel_button: Button

    def __init__(self):
        super().__init__(name="create_project")

        self.date_input = Input(placeholder="Enter a date", validators=[ValidateDate()])
        self.date_input.action_submit = self.action_start_timer_with_new_project

        self.client_input = Input(placeholder="Enter a client name", validators=[ValidateNotEmpty()])
        self.client_input.action_submit = self.action_start_timer_with_new_project

        self.project_name_input = Input(placeholder="Enter a project name", validators=[ValidateNotEmpty()])
        self.project_name_input.action_submit = self.action_start_timer_with_new_project

        self.submit_button = Button("Start timer", id="submit_btn", variant="primary")

        self.cancel_button = Button("Cancel", id="cancel_btn", variant="error")


    def compose(self):
        with Vertical(id="form", classes="auto-size"):
            with Vertical(classes="form-group"):
                yield Label("Date (YYYY-MM-DD format):")
                yield self.date_input

            with Vertical(classes="form-group"):
                yield Label("Client:")
                yield self.client_input

            with Vertical(classes="form-group"):
                yield Label("Project name:")
                yield self.project_name_input

        with Horizontal(id="buttons", classes="auto-size"):
            yield self.submit_button
            yield self.cancel_button

    def action_start_timer_with_new_project(self):
        all_inputs_valid = True

        for input_widget in [self.date_input, self.client_input, self.project_name_input]:
            result = input_widget.validate(input_widget.value)
            if not result.is_valid: all_inputs_valid = False

        if not all_inputs_valid: return

        project = ProjectEntry(
            client=self.client_input.value,
            project=self.project_name_input.value,
            date=datetime.strptime(self.date_input.value, "%Y-%m-%d").date(),
        )

        self.app.push_screen(TimerView(project))


    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "submit_btn":
            self.action_start_timer_with_new_project()
        elif event.button.id == "cancel_btn":
            self.app.pop_screen()
