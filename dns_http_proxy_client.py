import base64
import dns.resolver
import webbrowser
import os

# Set DNS Tunnel Proxy Server IP
DNS_SERVER = "127.0.0.1"  # Change to the remote server if needed

def send_http_request_over_dns(url):
    # Encode the URL in Base64
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode()
    dns_query = f"{encoded_url}.tunnel.com"

    # Send DNS TXT query
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [DNS_SERVER]

    try:
        response = resolver.resolve(dns_query, "TXT", tcp=True)

        # Collect all chunks
        full_encoded_response = []
        for txt_record in response:
            encoded_response = txt_record.to_text().strip('"')

            # # Fix padding for Base64 decoding
            # missing_padding = len(encoded_response) % 4
            # if missing_padding:
            #     encoded_response += '=' * (4 - missing_padding)
            
            full_encoded_response.append(encoded_response)

        # Decode full response
        full_encoded_string = ''.join(full_encoded_response)
        decoded_response = base64.urlsafe_b64decode(full_encoded_string).decode()

        # open in web browser (handle A DNS label is > 63 octets long)
        try:
            html = decoded_response
            path = os.path.abspath('/absolute/path/to/temp.html')
            file_url = 'file://' + path
            
            with open(path, 'w') as foo:
                foo.write(html)
            webbrowser.open(file_url)

        except Exception as e:
            print(f"[-] Error: {e}")

        print("[+] HTTP Response:\n", decoded_response)
        


    except dns.resolver.NXDOMAIN:
        print("[-] Error: NXDOMAIN - The DNS query name does not exist.")
    except dns.resolver.NoAnswer:
        print("[-] Error: No response received from the DNS server.")
    except Exception as e:
        print(f"[-] Error: {e}")

# Example usage
while True:
    url = input("Enter URL: ")
    if url.lower() in ["exit", "quit"]:
        break
    send_http_request_over_dns(url)
