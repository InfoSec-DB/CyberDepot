
# Password Reset Poisoning: Intercepting and Manipulating Email Links

## Overview

This tutorial demonstrates how to exploit vulnerabilities in the password reset process by intercepting and manipulating email links using BurpSuite. This can allow an attacker to reset a user’s password and gain unauthorized access to their account. This guide is intended for educational purposes to enhance your penetration testing skills as part of OSCP training.

## Step-by-Step Guide

### 1. Setting Up the Environment

#### Prerequisites

-   A vulnerable web application with a password reset feature.
-   BurpSuite installed and configured to intercept HTTP/HTTPS traffic.
-   An email client to receive password reset emails.

#### Configuring BurpSuite

1.  **Open BurpSuite**:
    
    -   Launch BurpSuite and navigate to the "Proxy" tab.
    -   Click on "Intercept" to ensure it is turned on.
2.  **Set Up Your Browser**:
    
    -   Open your browser settings and configure the proxy settings to use `127.0.0.1` and port `8080` (default BurpSuite settings).
    -   Ensure you have installed BurpSuite's CA certificate in your browser to avoid SSL/TLS issues. This can be done by going to BurpSuite's "Proxy" > "Options" > "Import / Export CA Certificate".

### 2. Initiating the Password Reset Process

#### Trigger Password Reset

1.  **Navigate to the Target Web Application's Password Reset Page**:
    
    -   Locate the "Forgot Password" or equivalent link on the login page.
2.  **Enter the Email Address**:
    
    -   Use the email address of the account you want to reset the password for.
3.  **Submit the Form**:
    
    -   Click on the "Reset Password" or equivalent button to submit the request.

#### Capture the Request

1.  **Intercept the Request in BurpSuite**:
    
    -   Ensure interception is turned on in BurpSuite. When you submit the form, BurpSuite will capture the HTTP request.
2.  **Analyze the Request**:
    
    -   Examine the request headers and parameters to understand how the password reset process works. For example:
       
    `POST /reset_password HTTP/1.1
    Host: example.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 40
    
    email=user@example.com&action=reset` 
        
    -   Look for parameters like `email` or `user_id`.
3.  **Forward the Request**:
    
    -   Forward the request to allow the email to be sent to the target's email address.

### 3. Intercepting the Password Reset Email

#### Receive the Email

1.  **Check the Email Account**:
    -   Log in to the email account used for the password reset request.
    -   Look for the password reset email. It typically contains a link or token for resetting the password, such as:
                
        `https://example.com/reset_password?token=abcd1234` 
        

#### Capture the Reset Link

1.  **Copy the Reset Link**:
    -   Copy the URL or token provided in the email.

### 4. Intercepting and Modifying the Reset Link Request

#### Prepare to Intercept the Reset Link Request

1.  **Paste the Reset Link into Your Browser**:
    
    -   Paste the copied URL into your browser but do not press Enter yet.
2.  **Turn On Interception in BurpSuite**:
    
    -   Ensure BurpSuite's interception is enabled to capture the request.

#### Intercept the Request

1.  **Navigate to the Reset Link**:
    -   Press Enter to navigate to the reset link.
    -   BurpSuite will capture the HTTP request containing the reset token or parameters, such as:
        
        
        `GET /reset_password?token=abcd1234 HTTP/1.1
        Host: example.com` 
        

#### Analyze and Modify the Request

1.  **Examine the Intercepted Request**:
    
    -   Look for parameters like `token`, `reset_token`, `email`, or `user_id`.
    -   Identify which parameter controls the reset functionality.
2.  **Modify the Parameters as Needed**:
    
    -   Example 1: Change the token to another valid token if you have multiple accounts. Let's assume you have another valid token `efgh5678`:
        
        
        `GET /reset_password?token=efgh5678 HTTP/1.1
        Host: example.com` 
        
    -   Example 2: Change the email parameter to another valid email. Suppose the original request was:
        

        
        `GET /reset_password?token=abcd1234&email=user@example.com HTTP/1.1
        Host: example.com` 
        
        You could change the email to an attacker-controlled email:
        
        
        `GET /reset_password?token=abcd1234&email=attacker@example.com HTTP/1.1
        Host: example.com` 
        
3.  **Understand the Application's Logic**:
    
    -   Analyze how the application validates the reset token. This can involve replaying the same request with slight modifications to see how the server responds.
    -   Check if the token is validated against the user's session or if it's independent. For example, some applications may bind the token to a specific IP address or session ID.

#### Forward the Modified Request

1.  **Forward the Modified Request**:
    -   Send the modified request to the server by clicking the "Forward" button in BurpSuite.
    -   Observe the server's response to confirm if the modification was successful.

### 5. Resetting the Password

#### Complete the Password Reset

1.  **Follow the Redirect**:
    
    -   If the modified request is accepted, you will typically be redirected to a page where you can set a new password.
2.  **Enter and Confirm the New Password**:
    
    -   Enter a new password and confirm it to complete the reset process.

#### Log In with the New Password

1.  **Use the Newly Set Password to Log In**:
    -   Log in to the account using the new password to verify that the reset was successful.

### Additional Examples and Advanced Techniques

#### Example: Exploiting Parameter Manipulation

-   Suppose the reset link contains multiple parameters including a user identifier:
    
    
    `https://example.com/reset_password?token=abcd1234&user_id=123` 
    
    You could change the `user_id` parameter to another valid user ID to see if the application allows resetting another user's password:
    
    
    `https://example.com/reset_password?token=abcd1234&user_id=456` 
    

#### Example: Using BurpSuite Repeater for Token Manipulation

-   Use BurpSuite's Repeater tool to resend and modify the reset token:
    1.  Intercept the reset link request.
    2.  Send the request to Repeater by right-clicking on the request and selecting "Send to Repeater".
    3.  In the Repeater tab, modify the token or other parameters as needed.
    4.  Send the modified request repeatedly with different values to test how the application responds.

### Mitigation Strategies

To prevent password reset poisoning attacks, consider implementing the following security measures:

1.  **Token Expiration**:
    
    -   Ensure that password reset tokens have a short expiration time to limit the window of opportunity for attacks.
2.  **Secure Token Generation**:
    
    -   Use cryptographically secure methods to generate unique and random tokens to prevent prediction or reuse.
3.  **Rate Limiting**:
    
    -   Implement rate limiting on password reset requests to prevent brute force attacks and token enumeration.
4.  **Email Confirmation**:
    
    -   Require users to confirm their email address or other personal information before allowing a password reset to ensure the request's legitimacy.
5.  **Logging and Monitoring**:
    
    -   Monitor and log password reset attempts and alert administrators of suspicious activity to detect and respond to potential attacks.
6.  **Use HTTPS**:
    
    -   Ensure all communication between the client and server is encrypted to prevent interception of sensitive data.
7.  **Bind Tokens to User Sessions**:
    
    -   Bind password reset tokens to the user’s session or IP address to prevent misuse by unauthorized parties.