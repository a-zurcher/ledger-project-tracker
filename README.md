# Ledger project tracker

Track your projects in the terminal using [ledger-cli](https://ledger-cli.org/) file format.

## Usage

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
