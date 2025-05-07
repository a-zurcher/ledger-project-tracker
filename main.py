from textual.app import App
from views.ProjectSelectorView import ProjectSelectorView

class ProjectTimerApp(App):
    TITLE = "Project Tracker"
    CSS_PATH = "app.tcss"

    def on_mount(self):
        self.push_screen(ProjectSelectorView())

if __name__ == "__main__":
    ProjectTimerApp().run()
