# Shodan Cheat Sheet for Penetration Testing

Shodan is a search engine for Internet-connected devices. It can be used to discover which of your devices are connected to the Internet, where they are located, and who is using them. Here’s how to use Shodan for penetration testing:

## Basic Commands
- **Search for devices using a simple query**
  - `shodan search apache`
- **Count the number of results for a query**
  - `shodan count microsoft iis 6.0`

## Searching by Filters
Use filters to refine your searches:
- **City**
  - `shodan search city:"Las Vegas" apache`
- **Country**
  - `shodan search country:"US" camera`
- **Geo (latitude/longitude)**
  - `shodan search geo:"50.3,8.25"`
- **Hostname**
  - `shodan search hostname:"example.com"`
- **Net (network range)**
  - `shodan search net:192.168.0.0/24`
- **OS (operating system)**
  - `shodan search os:"windows 7"`
- **Port**
  - `shodan search port:80`

## Advanced Search Techniques
- **Combine filters**
  - `shodan search country:"DE" port:21 "anonymous ftp"`
- **Search for vulnerabilities**
  - `shodan search vuln:cve-2019-11510`

## Using Shodan to Monitor Specific Systems or Assets
- **Set up alerts for specific terms**
  - `shodan alert create "Name of Alert" "port:22 country:US"`
- **List all your created alerts**
  - `shodan alert list`
- **Remove an alert**
  - `shodan alert remove [ALERT ID]`

## Command-line Interface (CLI) Features
- **Download search results**
  - `shodan download myresults apache`
- **View downloaded data**
  - `shodan parse --fields ip_str,port,org,hostnames myresults.json.gz`
- **Generate a report from downloaded data**
  - `shodan stats --facets port:top10 myresults.json.gz`

## Reconnaissance on Companies for Bug Bounties
- **Identify technology footprint**
  - `shodan search org:"Example Company"`
- **Find exposed databases**
  - `shodan search org:"Example Company" product:"MongoDB"`
- **Locate vulnerable systems**
  - `shodan search org:"Example Company" vuln:cve-2022-0001`
- **Monitor for new devices**
  - `shodan alert create "New Devices at Example Company" "org:'Example Company'"`

## Examples
- **Basic device search example**
  - `shodan search webcam`
- **Search for default passwords**
  - `shodan search "default password"`
- **Search for specific CVE vulnerabilities**
  - `shodan search cve:2021-44228`
- **Monitor network for new SSH services**
  - `shodan alert create "New SSH" "port:22"`

## Tips for Advanced Shodan Queries
- **Filter by SSL info**
  - `shodan search ssl.cert.subject.cn:google`
- **Find devices based on their banner**
  - `shodan search "Server: Apache"`

This cheat sheet provides a foundation for using Shodan in penetration testing and security assessments, with specific strategies for conducting company-specific reconnaissance for bug bounties.
