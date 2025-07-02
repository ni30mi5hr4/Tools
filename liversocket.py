import socket
import concurrent.futures

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Adjust the timeout as needed
            s.connect((ip, port))
            return True
    except socket.timeout:
        print(f"Timeout when attempting to connect to {ip}:{port}")
        return False
    except socket.error as e:
        print(f"Error when attempting to connect to {ip}:{port}: {e}")
        return False

def scan_ip(ip, ports):
    for port in ports:
        if is_port_open(ip, port):
            with open('aliveip.txt', 'a') as file:
                file.write(f"{ip}\n")
            print(f"Live IP found and saved: {ip}")
            return

def main():
    ports = [80, 8080, 443]
    ip_list = []
    with open('ips.txt', 'r') as file:
        ip_list = [line.strip() for line in file]

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_ip, ip, ports) for ip in ip_list]

    print("Scanning complete. Live IPs saved in aliveip.txt.")

if __name__ == "__main__":
    main()

