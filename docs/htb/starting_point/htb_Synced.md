# HTB Synced Exploit Documentation

Welcome to the documentation for the **HTB Synced Exploit**. This site is generated with MkDocs and provides detailed instructions and information about the tool.

## Overview

The HTB Synced Exploit is a Python-based tool designed for use in Capture The Flag (CTF) challenges—specifically targeting systems with anonymous Rsync access. It automates the process of scanning for the Rsync service, listing available modules, downloading data, and retrieving the flag file if available.

## Features

- **Port Scanning:** Checks if Rsync is active on port 873.
- **Module Extraction:** Automatically lists available Rsync modules.
- **Anonymous Access:** Attempts to connect without credentials.
- **Data Download:** Saves files from accessible modules.
- **Flag Retrieval:** Reads and displays the contents of the `flag.txt` file.
- **Verbose Output:** Provides detailed, SLMap-style colored output.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/HTB-Synced.git
   ```

2. **Install Dependencies:**

   The tool requires Python 3 and the `pyfiglet` package. Install it with:

   ```bash
   pip install pyfiglet
   ```

3. **Setup MkDocs (Optional):**

   To build this documentation as a static site, install MkDocs:

   ```bash
   pip install mkdocs
   ```

   Then start the MkDocs server:

   ```bash
   mkdocs serve
   ```

   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Usage

Run the tool by executing:

```bash
python htb_synced.py
```

Follow the prompts to input the target IP. The tool then scans for Rsync, extracts modules, downloads available data, and attempts to read the flag.

## License

This documentation and tool are provided for educational and authorized penetration testing purposes only. Use responsibly and ethically.

---
*Made by #AfterDark*
