# **DNS Tunnel HTTP Proxy**

## **Overview**
This project demonstrates a **DNS Tunneling-based HTTP Proxy**, allowing a client behind a firewall to send HTTP requests over DNS queries. It mimics the behavior of **dnscat2** but is customized for HTTP traffic. This is useful in **environments where internet access is blocked but DNS queries are allowed**.

- **Client:** Encodes an HTTP request as a DNS query.
- **Server:** Receives the query, decodes it, fetches the requested HTTP resource, and returns the response in DNS TXT records.
- **Client:** Receives the DNS response, decodes it, and renders it in a web browser.

## **Attack Context**
Many **corporate, airport, and in-flight Wi-Fi networks** allow only DNS queries while blocking normal HTTP/HTTPS traffic until a user **pays for access**. However, **DNS traffic is usually unrestricted** for name resolution.

This setup exploits that by using DNS queries as a **covert channel** to bypass network restrictions and fetch web content.

## **How It Works**
1. **Client encodes an HTTP request** (URL) into a **Base64 string** and sends it inside a DNS query.
2. **DNS Tunnel Server** receives the query, extracts the URL, and makes an **HTTP request** to fetch the web page.
3. The server **encodes the response** into DNS TXT records and sends it back over DNS.
4. The **client decodes the response** and renders it in a web browser.

## **Installation & Setup**
### **Prerequisites**
- Python 3.x
- `dnslib` and `dnspython` libraries (for handling DNS queries)
- `requests` (for making HTTP requests)
- `webbrowser` (to render pages on the client side)

### **1️⃣ Install Dependencies**
Run the following command to install required packages:
```bash
pip install dnslib dnspython requests
```

### **2️⃣ Start the DNS Tunnel Server**
Run this on a **server or machine that can access the internet**:
```bash
sudo python3 dns_http_proxy_server.py
```
You should see:
```
[+] DNS HTTP Proxy Server Started on Port 53
[+] Your DNS Server IP: <Your Server IP>
```

### **3️⃣ Run the Client (Behind a Firewall)**
On a **restricted network**, run the client script:
```bash
python3 dns_http_proxy_client.py
```
Then enter a URL:
```
Enter URL: http://example.com
```
Expected output:
```
[+] HTTP Response:
<html><head>...</head><body>Example Domain</body></html>
```
A local HTML file will also open in a web browser.

## **Debugging & Troubleshooting**
### **🔹 Test If DNS Queries Reach the Server**
If the client is not receiving responses, check if the DNS server is reachable:
```bash
dig @127.0.0.1 example.com TXT
```
If you don’t get a response, ensure:
- The **DNS server is running**.
- The **firewall allows traffic on port 53** (`sudo ufw allow 53/udp`).
- The **DNS query format is correct**.

### **🔹 Capture DNS Traffic for Debugging**
On the server, check if queries are arriving:
```bash
sudo tcpdump -i eth0 port 53
```

## **Security & Ethical Considerations**
- **This tool is for educational and research purposes only.** Unauthorized use of this technique **may violate network policies**.
- Network administrators can **detect DNS tunneling** using **high query volumes, long subdomains, or unusual TXT records**.
- **Mitigation:** Enforce strict **DNS query rate limiting** and use **deep packet inspection (DPI)** to analyze DNS queries.

## **Potential Enhancements**
- **Compression**: Compress HTTP responses before sending them over DNS.
- **Encryption**: Use **AES encryption** to make the tunneling more stealthy.
- **Chunk Handling**: Implement **better chunked response handling** for large HTTP pages.
- **Support for POST requests**: Allow tunneling of data uploads.

## **License & Disclaimer**
- This project is released under the **MIT License**.
- The authors **do not encourage misuse** of this tool in real-world scenarios where it may violate legal or ethical guidelines.

---
**Now you have a working DNS-over-HTTP tunnel! 🚀**

