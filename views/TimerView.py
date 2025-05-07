import subprocess

from rich.text import Text
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Label, Header, Footer, Digits
from textual.reactive import reactive
from textual.timer import Timer
from textual.containers import Horizontal, Container, Vertical
from textual.app import ComposeResult

from models import ProjectEntry
from views.DescriptionPromptView import DescriptionPromptView


class TimerView(Screen):
    BINDINGS = [("space", "toggle", "Start/Stop")]

    CSS = """
        TimerView { align: center middle; }
        
        #project_name {
            margin-bottom: 1;
            max-width: 52;
        }
        
        #timer_controls { align: center middle; }
        
        Digits { margin-left: 2; margin-right: 2; }
        
        #project_client {
            width: 100%;
            text-align: right;
            margin-top: 1;
            max-width: 52;
        }
    """

    input: Input
    timer: Timer
    project_name: Static
    timer_display: Digits
    select_project_button: Button
    toggle_timer_button: Button
    stop_button: Button

    elapsed: reactive[float] = reactive(0)
    running: reactive[bool] = reactive(True)

    def __init__(self, project: ProjectEntry):
        super().__init__(name='timer')
        self.project = project

        # widgets
        self.timer_display = Digits(classes="auto-size")
        self.timer_display_update("00:00")

        self.toggle_timer_button = Button(id="toggle_btn", variant="default")
        self.toggle_timer_set_text()

        self.stop_button = Button("⏹ Stop", id="stop_btn", variant="error")

        self.select_project_button = Button("Select another project", id="select_project_btn")

    def compose(self) -> ComposeResult:
        with Container(classes="auto-size app-container"):
            yield Label(Text(self.project.name, style="bold"), id="project_name")

            with Horizontal(id="timer_controls", classes="auto-size"):
                yield self.toggle_timer_button
                yield self.timer_display
                yield self.stop_button

            yield Label(Text(self.project.client), id="project_client")

    def on_mount(self):
        self.timer: Timer = self.set_interval(1, self.tick)

    def tick(self):
        if self.running:
            # add one second to the elapsed total
            self.elapsed += 1 / 60
            m, s = divmod(self.elapsed, 60)
            self.timer_display_update(f"{int(m):02d}:{int(s):02d}")

    def toggle_timer_set_text(self, **kwargs):
        self.toggle_timer_button.label = "▶ Resume" if not self.running else "⏸ Pause"
        self.toggle_timer_button.variant = "primary" if not self.running else "default"

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

    def timer_display_update(self, text: str):
        figlet_output = subprocess.run(
            args=f'echo "" && figlet -w "$(tput cols)" -f "files/DOS_Rebel.flf" {text}',
            shell=True,
            capture_output=True,
        ).stdout.decode('utf-8')

        visual = Text(figlet_output)

        self.timer_display.update(text)
