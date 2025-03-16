
# Nmap Cheat Sheet for Penetration Testing

  

Nmap (Network Mapper) is a free and open source utility for network discovery and security auditing. It is used to discover hosts and services on a computer network, thus building a "map" of the network. Here's how to use Nmap effectively in penetration testing:

  

## Basic Scanning Techniques

-  **Scan a single IP or host**

  `nmap 192.168.1.1`

-  **Scan a range of IPs**

  `nmap 192.168.1.1-20`

-  **Scan a subnet**

  `nmap 192.168.1.0/24`

-  **Scan for every TCP port (1-65535)**

  `nmap -p- 192.168.1.1`

-  **Perform a fast scan**

  `nmap -T4 -F 192.168.1.1`

  

## Service and OS Detection

-  **Detect OS and Services**

  `nmap -A 192.168.1.1`

-  **Standard service detection**

  `nmap -sV 192.168.1.1`

  

## Advanced Scanning

-  **Use TCP SYN scan (root only)**

  `nmap -sS 192.168.1.1`

-  **Use TCP connect scan (non-root)**

  `nmap -sT 192.168.1.1`

-  **UDP scan**

  `nmap -sU -p 123,161,162 192.168.1.1`

-  **SCTP INIT scan**

  `nmap -sY 192.168.1.1`

  

## Stealth and Evasion Techniques

-  **Fragment packets**

  `nmap -f 192.168.1.1`

-  **Specify a custom MTU**

  `nmap --mtu 24 192.168.1.1`

-  **Send bad checksums**

  `nmap --badsum 192.168.1.1`

-  **Decoy scan**

  `nmap -D RND:10 [target]`

  `nmap -D decoy1,decoy2,ME,decoy3,decoy4 [target]`

  

## Script Scanning

-  **Using default safe scripts**

  `nmap -sC 192.168.1.1`

-  **Script scanning with specific script**

  `nmap --script=ssl-heartbleed 192.168.1.1`

-  **Script scanning with script arguments**

  `nmap --script=smb-check-vulns --script-args=unsafe=1 192.168.1.1`

  

## Output Formats

-  **Save output to a file**

  `nmap -oN output.txt 192.168.1.1`

-  **Output in all formats**

  `nmap -oA output 192.168.1.1`

-  **Grepable output**

  `nmap -oG output.txt 192.168.1.1`

  

## Additional Useful Commands

-  **Aggressive timing template**

  `nmap -T5 192.168.1.1`

-  **Idle scan using a zombie host**

  `nmap -sI [zombie] 192.168.1.1`

-  **IPv6 scanning**

  `nmap -6 [IPv6 address]`

  

## Examples

-  **Basic host scan example**

  `nmap example.com`

-  **Service detection example**

  `nmap -sV example.com`

-  **OS and service detection example**

  `nmap -A example.com`

-  **Decoy scan example**

  `nmap -D decoy1,decoy2,ME,decoy3,decoy4 example.com`

  **Script scan using specific scripts example**

  `nmap --script=ssl-heartbleed example.com`

  

This cheat sheet provides a foundation for using Nmap in penetration testing and security assessments, with detailed commands for various scanning scenarios. These commands can help you discover network vulnerabilities, audit network security, and perform reconnaissance tasks effectively.