#!/usr/bin/python3

import ipaddress

def save_ip_range():
    start_ip = input("Enter the start IP address: ")
    end_ip = input("Enter the end IP address: ")
    filename = input("Enter the file name to save IP addresses: ")

    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)

    with open(filename, 'w') as file:
        for ip_int in range(int(start_ip), int(end_ip) + 1):
            ip_address = ipaddress.IPv4Address(ip_int)
            file.write(str(ip_address) + '\n')

    print(f"IP addresses in the range have been saved to {filename}.")

# Call the function to execute the program
save_ip_range()
