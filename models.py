import os
import re
import subprocess
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'
projects_root_account = "Projets"
ledger_time_file = os.getenv("LEDGER_TIME_FILE")
time_account = "Temps"

class InvalidProjectEntry(Exception): pass

class LedgerTimeFileEnvNotSet(Exception):
    def __init__(self):
        # Call the base class constructor with the parameters it needs
        message = "The $LEDGER_TIME_FILE environmental variable is not set ! Please declare it before using this app."
        super().__init__(message)

class ProjectEntry:
    name: str
    client: str
    date: datetime.date
    description: str
    duration: str

    def __init__(self, client: str, name: str, date: datetime.date):
        self.client = client
        self.name = name
        self.date = date
        self.description = ""
        self.duration = ""

    def __str__(self) -> str:
        return f"{self.name} ({self.client})"

    def set_description(self, description: str):
        self.description = description

    def set_duration(self, duration: str):
        self.duration = duration

    def get_ledger_project_name(self) -> str:
        date_str = self.date.strftime(DATE_FORMAT)
        return f"{projects_root_account}:{self.client}:{date_str} {self.name}"

    def to_ledger_entry(self):
        today = datetime.today().strftime(DATE_FORMAT)
        ledger_project = self.get_ledger_project_name()

        return (
            f"{today} {self.description}\n"
            f"    {ledger_project}\t\t{self.duration}\n"
            f"    {time_account}\n"
        )

    def get_time_spend(self) -> int:
        """Returns the time spent on this project in seconds, or 0 if the project doesn't exist in the ledger file."""
        ledger_format = "%(to_int(amount(scrub(display_amount))))\n"

        result = subprocess.run(
            args=f'ledger -f {ledger_time_file} balance --format "{ledger_format}" "{self.get_ledger_project_name()}"',
            shell=True, capture_output=True, text=True
        )

        try:
            return int(result.stdout)
        except ValueError:
            return 0

def format_time(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}"


def parse_project(query: str) -> ProjectEntry:
    matches = re.findall(r'(.+):(\d{4}-\d{2}-\d{2})\s(.+)', query)
    if len(matches) != 1:
        raise InvalidProjectEntry(f"Invalid project entry: {query}")
    client, date_str, project = matches[0]

    return ProjectEntry(client, project, datetime.strptime(date_str, DATE_FORMAT))


def get_projects() -> list[ProjectEntry]:
    if ledger_time_file is None: raise LedgerTimeFileEnvNotSet()

    # create the file if it doesn't exist yet
    if not os.path.isfile(ledger_time_file):
        with open(ledger_time_file, "w") as f:
            f.write("")

    result = subprocess.run(
        args=f"ledger -f {ledger_time_file} accounts {projects_root_account} --uncleared",
        shell=True, capture_output=True, text=True
    )

    lines = filter(None, result.stdout.splitlines())
    return [parse_project(line.replace(f"{projects_root_account}:", "")) for line in lines]
