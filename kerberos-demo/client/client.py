import socket
import gssapi
import sys

def main(server_host):
    print(f"Initiating connection to {server_host}...")
    
    # 1. Specify the service we want to talk to
    target_name = gssapi.Name(f"host@{server_host}", gssapi.NameType.hostbased_service)
    
    # 2. Create a security context
    sec_ctx = gssapi.SecurityContext(name=target_name, usage='initiate')
    
    # 3. Generate the token (This secretly uses your TGT in /tmp/krb5cc_* to get a service ticket)
    out_token = sec_ctx.step()
    print(f"Generated Kerberos token ({len(out_token)} bytes)")
    
    # 4. Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_host, 9999))
    
    # 5. Send the token length, then the token
    sock.sendall(len(out_token).to_bytes(4, 'big'))
    sock.sendall(out_token)
    print("Token sent to server.")
    
    # 6. Receive response
    response = sock.recv(1024)
    print(f"\nServer Response: {response.decode()}")
    sock.close()

if __name__ == "__main__":
    server_host = sys.argv[1] if len(sys.argv) > 1 else "fake-hive.lab.local"
    main(server_host)
