
## OTP Bypass on Account Registration via Response Manipulation

### Overview

This article demonstrates several methods to bypass OTP (One-Time Password) verification during account registration or login processes using BurpSuite. These techniques can potentially lead to unauthorized access to user accounts, resulting in account takeover. This guide is intended for educational purposes to help you understand common vulnerabilities and improve your skills in penetration testing.

### Method 1: Response Manipulation During Registration

1.  **Register an Account**:
    -   Register an account with a mobile number and request an OTP.
2.  **Capture the Request**:
    -   Enter an incorrect OTP and capture the request in BurpSuite.
3.  **Intercept the Response**:
    
    -   In BurpSuite, go to the "Proxy" tab and intercept the response to the OTP verification request.
    -   The response will look like:
    
    `{"verificationStatus":false,"mobile":"9072346577","profileId":"84673832"}` 
    
4.  **Modify the Response**:
    
    -   Change the response to:
        
    `{"verificationStatus":true,"mobile":"9072346577","profileId":"84673832"}` 
    
    -   In BurpSuite, edit the intercepted response directly in the "HTTP history" tab.
5.  **Forward the Response**:
    -   Forward the modified response by clicking on the "Forward" button.
6.  **Outcome**:
    -   You will be logged into the account.

**Impact**: Account Takeover

### Method 2: Response Manipulation During Login

1.  **Initiate Login**:
    -   Go to the login page and request an OTP.
2.  **Capture the Request**:
    -   Enter an incorrect OTP and capture the request in BurpSuite.
3.  **Intercept the Response**:
    -   In BurpSuite, intercept the response to the OTP verification request.
    -   The response will indicate an error (e.g., incorrect OTP).
4.  **Modify the Response**:
    -   Change the response to indicate success (e.g., replace `{"status":"error"}` with `{"status":"success"}`).
5.  **Forward the Response**:
    -   Forward the modified response by clicking on the "Forward" button.
6.  **Outcome**:
    -   You will be logged into the account.

**Impact**: Account Takeover

### Method 3: Intercept and Modify Response Status

1.  **Register Two Accounts**:
    -   Register two accounts with any two mobile numbers, entering the correct OTP initially.
2.  **Capture the Request**:
    -   Intercept your request in BurpSuite.
3.  **Intercept the Response**:
    -   Click on "Action" -> "Do intercept" -> "Intercept response to this request".
4.  **Check the Response**:
    -   Check the response message for a status, e.g., `status:1`.
5.  **Repeat with Incorrect OTP**:
    -   Follow the same procedure with the other account but enter an incorrect OTP this time.
6.  **Capture and Modify**:
    -   Intercept the response to the request and note the message status, e.g., `status:0`.
    -   Change the status to `status:1`.
7.  **Forward the Response**:
    -   Forward the modified response by clicking on the "Forward" button.
8.  **Outcome**:
    -   If you are logged in, you have successfully bypassed authentication.

### Method 4: Bypass OTP in Registration Forms Using Repeater

1.  **Create an Account**:
    -   Create an account with a non-existent phone number.
2.  **Intercept the Request**:
    -   Intercept the request in BurpSuite.
3.  **Use Repeater**:
    -   Send the request to the repeater by right-clicking on the request and selecting "Send to Repeater".
4.  **Modify the Phone Number**:
    -   Go to the Repeater tab and change the non-existent phone number to your phone number.
5.  **Use Received OTP**:
    -   If you receive an OTP on your phone, use that OTP to register the non-existent number.

### Method 5: No Rate Limiting

1.  **Create an Account**:
    -   Create an account.
2.  **Capture the Request**:
    -   When the application asks for the OTP, enter an incorrect OTP and capture the request in BurpSuite.
3.  **Use Repeater**:
    -   Send this request to the Repeater by right-clicking on the request and selecting "Send to Repeater".
4.  **Check for Rate Limiting**:
    -   Set up a payload on the OTP value and repeat the request.
    -   If there is no rate limit, wait for a 200 OK or 302 Found status code.
5.  **Outcome**:
    -   If you receive a 200 OK or 302 Found status code, you have bypassed the OTP.

### Additional Test Cases for Bypassing OTP

1.  **Default OTPs**:
    -   Test common default OTPs like `111111`, `123456`, `000000`.
2.  **Leaked OTP in Response**:
    -   Capture the request in BurpSuite and check the response for any leaked OTP.
3.  **Old OTP Validity**:
    -   Check if an old OTP is still valid by attempting to reuse it.