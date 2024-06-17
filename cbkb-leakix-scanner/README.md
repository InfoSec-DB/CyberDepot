
# LeakIX Scanner 🚀

## Description

LeakIX Scanner is a powerful tool designed to interact with the LeakIX API, enabling red teamers and exploitation specialists to search for exposed and vulnerable configurations across the internet. This tool helps in identifying critical security issues by querying various plugins available on LeakIX and filtering the results based on specified severity levels.

## Features

- **Search LeakIX** 🔍: Query the LeakIX API for specific plugins and severity levels.
- **Pagination** 📄: Automatically handles pagination to fetch results across multiple pages.
- **Detailed Logging** 📝: Adjustable verbosity to provide insights into the scanning process.
- **Output Formats** 📂: Save results in JSON, CSV, or plain text formats.
- **Plugin Management** 🛠️: Lists available plugins and validates user-specified plugins against a predefined list.

## Screenshot
![LeakIX Scanner](https://colorblindkeybangers.com/imgs/cbkb-scanner1.png)
![LeakIX Scanner](https://colorblindkeybangers.com/imgs/cbkb-scanner2.png)

## Usage

1. **Clone the Repository** 🛒
    ```sh
    git clone https://github.com/InfoSec-DB/CyberDepot.git
    cd CyberDepot/cbkd-leakix-scanner
    ```

2. **Install Dependencies** 📦
    ```sh
    pip install requests argparse pyfiglet
    ```

3. **Get Your API Key** 🔑
    - Visit [LeakIX](https://leakix.net) and sign up for a free account.
    - Navigate to your profile settings and generate an API key.
    - Replace the `API_KEY` value in the `cbkb-leakix.py` file with your newly generated API key.
    ```python
    # Replace this value with your API key
    API_KEY = 'YOUR_API_KEY_HERE'
    ```

4. **Run the Tool** ▶️
    ```sh
    python cbkb-leakix.py -p ApacheStatusPlugin -s medium -o results.txt --format txt
    ```

## Arguments

- `-p, --plugins` 🎯: Specify the plugins to search for.
- `-s, --severity` ⚠️: Specify the severity level to filter results (`low`, `medium`, `high`, `critical`).
- `-o, --output` 💾: Specify the output file to save results.
- `--format` 📋: Specify the output format (`json`, `txt`, `csv`), default is `txt`.
- `-v, --verbosity` 🔊: Increase verbosity level (use `-v`, `-vv`, `-vvv`).
- `--list-plugins` 📜: List all available plugins.
- `--pages` 📑: Specify the number of pages to fetch (default: 5).

## Example Commands

- **Basic Search**:
    ```sh
    python cbkb-leakix.py -p ApacheStatusPlugin -o results.txt
    ```

- **GitHub Exposed Config's Targeting Severity**:
    ```sh
    python cbkb-leakix.py -p GitConfigHttpPlugin -s critical -o results.txt -vv
    ```

## Disclaimer

Explore our extensive collection of payloads and other resources for red teamers and exploitation specialists. These resources are curated to aid you in your penetration testing and vulnerability assessment tasks. We are not responsible for any damages or exploitation caused by scripts. Use at your own risk⚠️.
