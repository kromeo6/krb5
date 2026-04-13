import socket
import gssapi
import os

def main():
    # Load the service keytab 
    # GSSAPI looks for KRB5_KTNAME environment variable by default
    os.environ['KRB5_KTNAME'] = '/shared/hive.keytab'
    
    server_creds = gssapi.Credentials(usage='accept')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable address reuse so we can restart easily
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 9999))
    sock.listen(1)
    print("Fake Hive Server listening on port 9999...")

    while True:
        conn, addr = sock.accept()
        print(f"\n--- Incoming connection from {addr} ---")
        
        try:
            # 1. Receive token length
            length_bytes = conn.recv(4)
            if not length_bytes:
                continue
            token_len = int.from_bytes(length_bytes, 'big')
            
            # 2. Receive token
            in_token = conn.recv(token_len)
            print(f"Received Kerberos token ({token_len} bytes)")
            
            # 3. Validate token using GSSAPI
            sec_ctx = gssapi.SecurityContext(creds=server_creds)
            sec_ctx.step(in_token)
            
            if sec_ctx.complete:
                client_name = str(sec_ctx.initiator_name)
                print(f"SUCCESS: Authenticated client as {client_name}")
                conn.sendall(f"Welcome to Fake Hive, {client_name}!".encode())
            else:
                print("FAILURE: Authentication incomplete.")
                conn.sendall(b"Authentication failed.")
                
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
