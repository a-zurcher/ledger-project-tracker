# Ledger project tracker

Track your projects in the terminal using [ledger-cli](https://ledger-cli.org/) file format.

## Usage

### [ledger-cli](https://ledger-cli.org/) format

To use this program, declare a new environmental variable `LEDGER_TIME_FILE` pointing to a file that will store your project's different tasks.

Each project can have multiple entries that reflect a project's task. Here's the example of an entry saved to the `LEDGER_TIME_FILE`:

```ledger
2025-05-02 Refactored the code base
    Projects:Company 1:2025-05-01 Ledger project tracker        0.35h
    Time
```

You can then use ledger to see how much time you've worked for a company, or a particular project:

```bash
ledger -f "$LEDGER_TIME_FILE" balance "Projects:Company 1"
#               2.36h  Projects:Company 1:2025-05-01 Ledger project tracker
```

## Installation

1. Create a new virtual environment for this project
    ```bash
    python -m venv venv
    ```
2.  Activate it
    - On macOS/Linux : 
      ```bash
      source venv/bin/activate
      ```
    - On Windows :
      ```powershell
      venv\Scripts\activate
      ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
4. Run the app :
    ```bash
    python main.py
    ```

5. (Optional Linux step) Add an entry in your bashrc for access from anywhere:
    ```bash
    # run this from this project root
    echo "alias track=\"source $(pwd)/venv/bin/activate && python $(pwd)/main.py && deactivate\"" >> ~/.bashrc
    ```