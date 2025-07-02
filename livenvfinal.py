import socket
import requests
import concurrent.futures
import re

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            return True
    except (socket.timeout, socket.error):
        return False

def contains_env_variables(content):
    # Define the pattern for environment variables
    pattern = re.compile(r'\b(?:APP_NAME|APP_ENV|APP_KEY|DB_CONNECTION|DB_HOST|DB_DATABASE|DB_USERNAME|DB_PASSWORD|MAIL_HOST|MAIL_USERNAME|MAIL_PASSWORD)=["\']?\w+')
    return pattern.search(content) is not None

def check_endpoints(ip):
    endpoints = ["/env", "/.env"]
    for prefix in ["http://", "https://"]:
        for endpoint in endpoints:
            url = f"{prefix}{ip}{endpoint}"
            try:
                response = requests.get(url, timeout=1, verify=False)
                if response.status_code == 200 and contains_env_variables(response.text):
                    return url
            except requests.RequestException:
                continue
    return None

def scan_and_check_endpoints(ip, ports):
    for port in ports:
        if is_port_open(ip, port):
            found_url = check_endpoints(f"{ip}:{port}")
            if found_url:
                with open('envfound.txt', 'a') as file:
                    file.write(f"{found_url}\n")
                print(f"Environment variable endpoint found and saved: {found_url}")
                break

def main():
    ports = [80, 8080, 443]
    ip_list = []
    with open('ips.txt', 'r') as file:
        ip_list = [line.strip() for line in file]

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_and_check_endpoints, ip, ports) for ip in ip_list]

    print("Scanning complete. Environment variable endpoints saved in envfound.txt.")

if __name__ == "__main__":
    main()
