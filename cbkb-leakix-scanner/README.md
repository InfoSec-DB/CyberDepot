
# LeakIX Scanner 🚀

## Description

LeakIX Scanner is a powerful tool designed to interact with the LeakIX API, enabling security researchers and bug bounty hunters to search for exposed and vulnerable configurations across the internet. This tool helps in identifying critical security issues by querying various plugins available on LeakIX and filtering the results based on specified severity levels.

## Features

- **Search LeakIX** 🔍: Query the LeakIX API for specific plugins and severity levels.
- **Pagination** 📄: Automatically handles pagination to fetch results across multiple pages.
- **Detailed Logging** 📝: Adjustable verbosity to provide insights into the scanning process.
- **Output Formats** 📂: Save results in JSON, CSV, or plain text formats.
- **Plugin Management** 🛠️: Lists available plugins and validates user-specified plugins against a predefined list.

## Usage

1. **Clone the Repository** 🛒

    ```sh
    git clone https://github.com/yourusername/leakix-scanner.git
    cd leakix-scanner
    ```

2. **Install Dependencies** 📦

    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Tool** ▶️

    ```sh
    python search_exposed_git_configs2.py -p ApacheStatusPlugin -s medium -o results.json --format json
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
  python search_exposed_git_configs2.py -p ApacheStatusPlugin -o results.txt
    ```

- **Github Exposed Config's Targeting Severity**: 
 ```sh
 python search_exposed_git_configs2.py -p GitConfigHttpPlugin -s critical -o results.txt -vv
     ```