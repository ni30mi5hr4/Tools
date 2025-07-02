import socket
import requests
import concurrent.futures
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            return True
    except (socket.timeout, socket.error):
        return False

def contains_env_variables(content):
    pattern = re.compile(
        r'\b(?:APP_NAME|APP_ENV|APP_KEY|APP_DEBUG|APP_URL|ASSET_URL|PUBLIC_ROOT|LOG_CHANNEL|'
        r'LOG_DEPRECATIONS_CHANNEL|LOG_LEVEL|DB_CONNECTION|DB_HOST|DB_PORT|DB_DATABASE|'
        r'DB_USERNAME|DB_PASSWORD|BROADCAST_DRIVER|CACHE_DRIVER|FILESYSTEM_DISK|QUEUE_CONNECTION|'
        r'SESSION_DRIVER|SESSION_LIFETIME|MEMCACHED_HOST|REDIS_HOST|REDIS_PASSWORD|REDIS_PORT|'
        r'SESSION_DOMAIN|MAIL_MAILER|MAIL_HOST|MAIL_PORT|MAIL_USERNAME|MAIL_PASSWORD|MAIL_ENCRYPTION|'
        r'MAIL_FROM_ADDRESS|MAIL_FROM_NAME|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_DEFAULT_REGION|'
        r'AWS_BUCKET|AWS_USE_PATH_STYLE_ENDPOINT|PUSHER_APP_ID|PUSHER_APP_KEY|PUSHER_APP_SECRET|'
        r'PUSHER_HOST|PUSHER_PORT|PUSHER_SCHEME|PUSHER_APP_CLUSTER|MIX_PUSHER_APP_KEY|'
        r'MIX_PUSHER_APP_CLUSTER|SCOUT_DRIVER|WORDPRESS_BASE_URL|WORDPRESS_API_KEY)=["\']?\w+'
    )
    return pattern.search(content) is not None

def check_endpoints(ip):
    endpoints = ["/.env"]
    for prefix in ["http://", "https://"]:
        for endpoint in endpoints:
            url = f"{prefix}{ip}{endpoint}"
            for _ in range(1):
                try:
                    print(f"Trying {url}")
                    response = requests.get(url, timeout=1, verify=False)
                    if response.status_code == 200 and contains_env_variables(response.text):
                        return url
                except requests.RequestException:
                    continue
            break
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

    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(scan_and_check_endpoints, ip, ports) for ip in ip_list]

    print("Scanning complete. Environment variable endpoints saved in envfound.txt.")

if __name__ == "__main__":
     main()
