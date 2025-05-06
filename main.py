from textual.app import App
from views.selector import ProjectSelectorView
from views.timer import TimerView

class ProjectTimerApp(App):
    TITLE = "Project Tracker"

    def on_mount(self):
        self.push_screen(ProjectSelectorView(), name="selector")

    def push_screen(self, screen, **kwargs):
        if isinstance(screen, str) and screen == "timer":
            project = kwargs.get("project")
            super().push_screen(TimerView(project))
        else:
            super().push_screen(screen)

if __name__ == "__main__":
    ProjectTimerApp().run()
