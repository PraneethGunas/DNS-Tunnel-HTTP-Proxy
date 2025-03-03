import base64
import requests
import socket
from dnslib.server import DNSServer, BaseResolver
from dnslib import DNSRecord, QTYPE, RR, TXT

class DNSTunnelHTTPProxy(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname).strip('.')

        try:
            # Extract the encoded URL from the subdomain
            encoded_url = qname.split('.')[0]
            http_url = base64.urlsafe_b64decode(encoded_url).decode('utf-8')
            print(f"[+] Received HTTP Request: {http_url}")

            # Make the HTTP request on behalf of the client
            response = requests.get(http_url)
            response_text = response.text  # Limit response size

            # Encode response in Base64
            encoded_response = base64.urlsafe_b64encode(response_text.encode()).decode()
            chunks = [encoded_response[i:i+255] for i in range(0, len(encoded_response), 255)]
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            encoded_response = base64.urlsafe_b64encode(error_msg.encode()).decode()
            chunks = [encoded_response]

        # Create DNS TXT response
        reply = request.reply()
        for chunk in chunks:
            reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(chunk)))

        return reply

# Start the DNS Proxy Server
resolver = DNSTunnelHTTPProxy()
server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=True)

print("[+] DNS HTTP Proxy Server Started on Port 53")
local_ip = socket.gethostbyname(socket.gethostname())
print("[+] Your DNS Server IP:", local_ip)

server.start()
