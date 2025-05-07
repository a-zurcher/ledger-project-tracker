import os
import re
import subprocess
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'
projects_root_account = "Projets"
ledger_time_file = os.getenv("LEDGER_TIME_FILE")
time_account = "Temps"

class InvalidProjectEntry(Exception):
    pass

class ProjectEntry:
    name: str
    client: str
    date: datetime.date
    description: str
    duration: str

    def __init__(self, client: str, project: str, date: datetime.date):
        self.client = client
        self.name = project
        self.date = date
        self.description = ""
        self.duration = ""

    def __str__(self) -> str:
        return f"{self.name} ({self.client})"

    def set_description(self, description: str):
        self.description = description

    def set_duration(self, duration: str):
        self.duration = duration

    def to_ledger(self):
        today = datetime.today().strftime(DATE_FORMAT)
        date_str = self.date.strftime(DATE_FORMAT)
        return (
            f"{today} {self.description}\n"
            f"    {projects_root_account}:{self.client}:{date_str} {self.name}\t\t{self.duration}\n"
            f"    {time_account}\n"
        )


def parse_project(query: str) -> ProjectEntry:
    matches = re.findall(r'(.+):(\d{4}-\d{2}-\d{2})\s(.+)', query)
    if len(matches) != 1:
        raise InvalidProjectEntry(f"Invalid project entry: {query}")
    client, date_str, project = matches[0]

    return ProjectEntry(client, project, datetime.strptime(date_str, DATE_FORMAT))


def get_projects() -> list[ProjectEntry]:
    result = subprocess.run(
        args=f"ledger -f {ledger_time_file} accounts {projects_root_account} --uncleared",
        shell=True, capture_output=True, text=True
    )

    lines = filter(None, result.stdout.splitlines())
    return [parse_project(line.replace(f"{projects_root_account}:", "")) for line in lines]
