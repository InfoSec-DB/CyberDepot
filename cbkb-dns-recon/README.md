
# cbkb-dns-recon

This project provides a Python script for performing comprehensive DNS reconnaissance, including subdomain enumeration, DNS record retrieval, reverse DNS lookups, and DNS poisoning detection. The script integrates with `Sublist3r` for subdomain enumeration and supports output in CSV, JSON, and TXT formats.

![CBKB DNS Recon Scanner](https://colorblindkeybangers.com/imgs/cbkb-dns.png)
![CBKB DNS Recon Scanner](https://colorblindkeybangers.com/imgs/cbkb-dns1.png)
## Features


- 🌐 **Subdomain Enumeration:** Uses `Sublist3r` to retrieve subdomains if no input file is provided.
- 📜 **DNS Record Retrieval:** Queries A, CNAME, TXT, NS, and MX records.
- 🔐 **Zone Transfer Attempts:** Attempts to perform zone transfers.
- 🔍 **Reverse DNS Lookups:** Performs PTR record lookups for IP addresses.
- 🚨 **DNS Poisoning Detection:** Detects discrepancies in DNS records from multiple DNS servers.
- 📂 **Flexible Output:** Supports output in CSV, JSON, and TXT formats.
- 🛠️ **Verbose Debugging:** Provides detailed output when the verbose flag is enabled.
- ⏳ **Loading Bar:** Displays a loading bar while processing domains.
- 🎨 **ASCII Art Banner:** Displays a random ASCII art banner with a random phrase at the start.

## Prerequisites

- 🐍 Python 3.x
- 📦 Python packages:
  - `sublist3r`
  - `requests`
  - `argparse`
  - `dnspython`
  - `tqdm`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/InfoSec-DB/CyberDepot.git
    cd CyberDepot/cbkb-dns-recon
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Using a Domains File

If you have a file with a list of domains, you can use the `-f` option to specify the file:

    python cbkb-dns_recon.py -f domains.txt -b example.com -s 8.8.8.8 1.1.1.1 9.9.9.9 -bl blacklist.txt -o output.csv -v

This command will:

1.  📄 Read the domains from `domains.txt`.
2.  📡 Use the provided DNS servers for queries.
3.  🌐 Use `example.com` as the base domain for zone transfer attempts.
4.  🛑 Skip domains listed in `blacklist.txt`.
5.  💾 Save the output to `output.json`.
6.  🔍 Enable verbose debugging output.



### Using Sublist3r for Subdomain Enumeration
If you do not have a domains file, the script will use Sublist3r to retrieve subdomains:

    python cbkb-dns_recon.py -b example.com -s 8.8.8.8 1.1.1.1 9.9.9.9 -bl blacklist.txt -o output.json -v

This command will:

1.  🌐 Use `example.com` as the base domain for zone transfer attempts.
2.  📡 Use the provided DNS servers for queries.
3.  🛑 Skip domains listed in `blacklist.txt`.
4.  💾 Save the output to `output.json`.
5.  🔍 Enable verbose debugging output.


## Command Line Arguments

-   `-f`, `--file`: 📄 Input file with list of domains (optional).
-   `-b`, `--base-domain`: 🌐 Base domain for zone transfer attempts (required).
-   `-s`, `--dns-servers`: 📡 List of DNS servers to query (default: `8.8.8.8 1.1.1.1 9.9.9.9`).
-   `-bl`, `--blacklist`: 🛑 Input file with list of blacklisted domains (optional).
-   `-o`, `--output-file`: 💾 Output file to save the results (required).
-   `-v`, `--verbose`: 🔍 Enable verbose debugging output (optional).

## Output

The script supports output in CSV, JSON, and TXT formats. The output format is determined by the file extension of the output file specified with the `-o` option.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or new features.