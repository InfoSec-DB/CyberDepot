
# Advanced 2FA Bypass via CSRF: Exploiting Two-Factor Authentication Vulnerabilities

## Overview

This tutorial demonstrates how to exploit vulnerabilities in the two-factor authentication (2FA) process using Cross-Site Request Forgery (CSRF). By manipulating 2FA requests, an attacker can potentially bypass 2FA and gain unauthorized access to a user’s account. This guide is intended for educational purposes to enhance your penetration testing skills as part of OSCP training.

## Step-by-Step Guide

### 1. Setting Up the Environment

#### Prerequisites

-   A vulnerable web application with 2FA and CSRF vulnerabilities.
-   BurpSuite installed and configured to intercept HTTP/HTTPS traffic.
-   An account on the target web application with 2FA enabled.

#### Configuring BurpSuite

1.  **Open BurpSuite**:
    
    -   Launch BurpSuite and navigate to the "Proxy" tab.
    -   Click on "Intercept" to ensure it is turned on.
2.  **Set Up Your Browser**:
    
    -   Open your browser settings and configure the proxy settings to use `127.0.0.1` and port `8080` (default BurpSuite settings).
    -   Ensure you have installed BurpSuite's CA certificate in your browser to avoid SSL/TLS issues. This can be done by going to BurpSuite's "Proxy" > "Options" > "Import / Export CA Certificate".

### 2. Understanding CSRF and 2FA

#### Cross-Site Request Forgery (CSRF)

CSRF is an attack that forces a user to execute unwanted actions on a web application where they are authenticated. By exploiting the trust that a web application has in the user’s browser, an attacker can trick the user into submitting requests unknowingly.

#### Two-Factor Authentication (2FA)

2FA adds an additional layer of security by requiring a second form of authentication (e.g., a code sent to a mobile device) in addition to the user’s password.

### 3. Identifying the Vulnerability

#### Analyze the 2FA Implementation

1.  **Log in to the Target Web Application**:
    
    -   Enter your username and password to log in.
    -   You will be prompted to enter a 2FA code.
2.  **Capture the 2FA Request in BurpSuite**:
    
    -   Ensure interception is turned on in BurpSuite.
    -   Enter the 2FA code and submit the form.
    -   BurpSuite will capture the HTTP request. For example:
                
        `POST /verify_2fa HTTP/1.1
        Host: example.com
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 40
        
        code=123456&session=abcdef123456` 
        
3.  **Analyze the Request**:
    
    -   Examine the request parameters. Look for the 2FA code and session identifiers.

### 4. Crafting the CSRF Attack

#### Create a Malicious HTML Form

1.  **Craft the CSRF Payload**:
    
    -   Create an HTML file with a form that mimics the 2FA request. For example:
                
        `<html>
        <body>
          <form action="http://example.com/verify_2fa" method="POST">
            <input type="hidden" name="code" value="123456">
            <input type="hidden" name="session" value="abcdef123456">
            <input type="submit" value="Submit request">
          </form>
          <script> document.forms[0].submit(); </script>
        </body>
        </html>` 
        
2.  **Host the HTML File**:
    
    -   Host this HTML file on a server controlled by the attacker or use a local web server.

#### Example of Hosting the Payload

You can use a simple Python HTTP server to host the HTML file:

`$ cd /path/to/html/file
$ python3 -m http.server 8080` 

### 5. Exploiting the CSRF Vulnerability

#### Deliver the Payload

1.  **Send the Link to the Victim**:
    
    -   Trick the victim into visiting the malicious HTML file. This can be done via email, social engineering, or other means. For example:
        
        `Hi,
        Please review the attached document by clicking the link below:
        http://attacker-server:8080` 
        
2.  **Victim Executes the CSRF Payload**:
    
    -   When the victim opens the link, the form is submitted automatically, sending the 2FA code and session information to the target web application.

### 6. Bypassing 2FA and Gaining Access

#### Verify the Attack

1.  **Check if the 2FA Was Bypassed**:
    
    -   If successful, the attack will bypass the 2FA check, and the attacker will gain access to the user’s account.
2.  **Log in as the Victim**:
    
    -   Use the victim's session information or credentials to log in to the account without needing the 2FA code.

### Additional Examples and Advanced Techniques

#### Example: Using BurpSuite to Automate the Attack

-   Use BurpSuite's Intruder tool to automate the attack by sending multiple requests with different 2FA codes:
    1.  Intercept the 2FA request.
    2.  Send the request to Intruder by right-clicking on the request and selecting "Send to Intruder".
    3.  Set the payload position for the `code` parameter.
    4.  Configure the payload set with possible 2FA codes (e.g., 000000 to 999999).
    5.  Start the attack and analyze the responses to identify valid 2FA codes.

#### Example: Understanding and Manipulating Session Identifiers

-   Examine how session identifiers are used in the 2FA process:
    1.  Capture a valid session identifier when logging in and during 2FA.
    2.  Manipulate the session identifier in the CSRF payload to see if the application accepts the modified session.

#### Example: Exploiting Weak 2FA Implementations

-   Identify and exploit weak 2FA implementations:
    1.  Test common default 2FA codes (e.g., 123456, 000000).
    2.  Check for predictable 2FA codes based on time or user patterns.

### Mitigation Strategies

To prevent 2FA bypass attacks via CSRF, consider implementing the following security measures:

1.  **Use Anti-CSRF Tokens**:
    
    -   Include unique, unpredictable tokens in all sensitive requests to prevent CSRF attacks.
2.  **Secure Cookie Attributes**:
    
    -   Set the `HttpOnly` and `Secure` flags on cookies to prevent them from being accessed via JavaScript and ensure they are only sent over HTTPS.
3.  **Implement SameSite Cookies**:
    
    -   Use the `SameSite` attribute for cookies to control how cookies are sent with cross-site requests.
4.  **Rate Limiting**:
    
    -   Implement rate limiting on 2FA verification attempts to prevent brute force attacks.
5.  **Monitor and Log 2FA Attempts**:
    
    -   Monitor and log all 2FA attempts and alert administrators of suspicious activity.


#### Response Manipulation

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#response-manipulation)

```
In response if "success":false
Change it to "success":true

```

#### Status Code Manipulation

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#status-code-manipulation)

```
If Status Code is 4xx
Try to change it to 200 OK and see if it bypass restrictions

```

#### 2FA Code Leakage in Response

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#2fa-code-leakage-in-response)

```
Check the response of the 2FA Code Triggering Request to see if the code is leaked.

```

#### JS File Analysis

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#js-file-analysis)

```
Rare but some JS Files may contain info about the 2FA Code, worth giving a shot

```

#### 2FA Code Reusability

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#2fa-code-reusability)

```
Same code can be reused

```

### Lack of Brute-Force Protection

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#lack-of-brute-force-protection)

```
Possible to brute-force any length 2FA Code

```

#### Missing 2FA Code Integrity Validation

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#missing-2fa-code-integrity-validation)

```
Code for any user acc can be used to bypass the 2FA

```

#### CSRF on 2FA Disabling

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#csrf-on-2fa-disabling)

```
No CSRF Protection on disabling 2FA, also there is no auth confirmation

```

#### Password Reset Disable 2FA

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#password-reset-disable-2fa)

```
2FA gets disabled on password change/email change

```

#### Backup Code Abuse

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#backup-code-abuse)

```
Bypassing 2FA by abusing the Backup code feature
Use the above mentioned techniques to bypass Backup Code to remove/reset 2FA restrictions

```

#### Clickjacking on 2FA Disabling Page

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#clickjacking-on-2fa-disabling-page)

```
Iframing the 2FA Disabling page and social engineering victim to disable the 2FA

```

#### Enabling 2FA doesn't expire Previously active Sessions

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#enabling-2fa-doesnt-expire-previously-active-sessions)

```
If the session is already hijacked and there is a session timeout vuln

```

#### Bypass 2FA with null or 000000

[](https://github.com/KathanP19/HowToHunt/blob/master/Authentication_Bypass/2FA_Bypasses.md#bypass-2fa-with-null-or-000000)

```
Enter the code 000000 or null to bypass 2FA protection.

```