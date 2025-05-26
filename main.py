from textual.app import App

from views.DescriptionPromptView import DescriptionPromptView
from views.ProjectSelectorView import ProjectSelectorView
from views.TimerView import TimerView


class ProjectTimerApp(App):
    TITLE = "Project Tracker"
    CSS_PATH = "app.tcss"
    SCREENS = {
        "project-selector": ProjectSelectorView,
        "timer": TimerView,
        "description-prompt": DescriptionPromptView
    }

    def on_mount(self):
        self.push_screen(ProjectSelectorView())

if __name__ == "__main__":
    ProjectTimerApp().run()
