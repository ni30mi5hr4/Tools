import socket
import requests
import concurrent.futures

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            return True
    except (socket.timeout, socket.error):
        return False

def check_endpoints(ip):
    endpoints = ["/.git/HEAD"]
    for prefix in ["http://", "https://"]:
        for endpoint in endpoints:
            url = f"{prefix}{ip}{endpoint}"
            try:
                response = requests.get(url, timeout=1, verify=False)
                content_length = int(response.headers.get('Content-Length', 0))
                if response.status_code == 200 and 18 <= content_length <= 45:
                    return url
            except requests.RequestException:
                continue
    return None

def scan_and_check_endpoints(ip, ports):
    for port in ports:
        if is_port_open(ip, port):
            found_url = check_endpoints(f"{ip}:{port}")
            if found_url:
                with open('gitfound.txt', 'a') as file:
                    file.write(f"{found_url}\n")
                print(f"Endpoint found and saved: {found_url}")
                break

def main():
    ports = [80, 8080, 443]
    ip_list = []
    with open('ips.txt', 'r') as file:
        ip_list = [line.strip() for line in file]

    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(scan_and_check_endpoints, ip, ports) for ip in ip_list]

    print("Scanning complete. Endpoints saved in gitfound.txt.")

if __name__ == "__main__":
    main()
