from textual.screen import Screen
from textual.widgets import Static, Button, Input
from textual.reactive import reactive
from textual.timer import Timer
from textual.containers import Vertical, Center, Horizontal
from textual.app import ComposeResult
from models import ProjectEntry
import os

LEDGER_TIME_FILE = os.getenv("LEDGER_TIME_FILE")

class TimerView(Screen):
    BINDINGS = [("space", "toggle", "Start/Stop")]

    input: Input
    timer: Timer

    project_name: Static
    timer_display: Static
    select_project_button: Button
    toggle_timer_button: Button
    stop_button: Button

    elapsed: reactive[int] = reactive(0)
    running: reactive[bool] = reactive(True)

    def __init__(self, project: ProjectEntry):
        super().__init__()
        self.project = project

        # widgets
        self.project_name = Static(self.project.name)
        self.timer_display = Static("00:00")
        self.toggle_timer_button = Button(id="toggle_btn", variant="primary")
        self.toggle_timer_set_text()
        self.stop_button = Button("⏹ Stop tracking", id="stop_btn", variant="error")
        self.select_project_button = Button("Select another project", id="select_project_btn")

    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                self.project_name,
                self.timer_display,

                Horizontal(
                    self.toggle_timer_button,
                    self.stop_button
                ),

                self.select_project_button
            )
        )

    def on_mount(self):
        self.timer: Timer = self.set_interval(1.0, self.tick)

    def tick(self):
        if self.running:
            self.elapsed += 1
            m, s = divmod(self.elapsed, 60)
            self.timer_display.update(f"[bold green]{m:02}:{s:02}[/bold green]")

    def toggle_timer_set_text(self, **kwargs):
        self.toggle_timer_button.label = "▶ Resume" if not self.running else "⏸ Pause"

    def action_toggle(self, **kwargs):
        self.running = not self.running
        self.toggle_timer_set_text()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "toggle_btn":
            self.action_toggle()
        elif event.button.id == "stop_btn":
            self.ask_description()

    def ask_description(self):
        self.project.set_duration(f"{self.elapsed / 60:.2f}h")
        self.app.push_screen(DescriptionPromptView(self.project))


class DescriptionPromptView(Screen):
    input: Input

    def __init__(self, project: ProjectEntry):
        super().__init__()
        self.project = project

    def compose(self) -> ComposeResult:
        yield Static("Enter a description:")
        self.input = Input(placeholder="What did you do?")
        yield self.input
        yield Button("Save", id="save_btn")

    def on_mount(self):
        self.input.focus()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save_btn":
            self.project.set_description(self.input.value)
            self.save_project(self.project)
            self.app.pop_screen()  # Go back to selector or exit

    def save_project(self, project: ProjectEntry):
        if not LEDGER_TIME_FILE:
            self.app.exit("LEDGER_TIME_FILE not set")
        with open(LEDGER_TIME_FILE, "a") as f:
            f.write("\n" + project.to_ledger())
