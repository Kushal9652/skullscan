import argparse
from termcolor import colored
import socket
import requests
from bs4 import BeautifulSoup

def get_subdomains(target_domain):
    subdomains = []

    print("Just a minute...")

    # Using subdomain enumeration service 1
    url1 = f"https://subdomainfinder.c99.nl/?q={target_domain}"
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    subdomains.extend([link.text for link in soup1.find_all('a', class_='text')])

    # Using subdomain enumeration service 2
    url2 = f"https://crt.sh/?q=%.{target_domain}&output=json"
    response2 = requests.get(url2)
    crtsh_data = response2.json()
    subdomains.extend(set(item['name_value'] for item in crtsh_data))

    return subdomains

def scan(target, ports):
    output_file = open("scan_results.txt", "w")
    print('\n' + 'Starting Scan For ' + str(target))
    for port in range(1, ports + 1):
        scan_port(target, port, output_file)
    output_file.close()

def scan_port(ipaddress, port, output_file):
    try:
        sock = socket.socket()
        sock.connect((ipaddress, port))
        result = f"[+] Port {port} Opened"
        print(colored(result, 'green'))
        output_file.write(result + "\n")
        sock.close()
    except (socket.error, OSError):
        result = f"[-] Port {port} Closed"
        print(colored(result, 'red'))
        output_file.write(result + "\n")

def main():
    parser = argparse.ArgumentParser(description="Port Scanner and Subdomain Enumeration Tool")
    parser.add_argument("--target", required=True, help="Target domain or IP address")
    parser.add_argument("--ports", type=int, help="Number of ports to scan")
    parser.add_argument("--sub", action="store_true", help="Perform subdomain enumeration")
    parser.add_argument("--o", "--output", dest="output_file", default=None, help="Output file for scan results")

    args = parser.parse_args()

    logo = """
    ██╗  ██╗██╗   ██╗███████╗██╗  ██╗ █████╗ ██╗     
    ██║ ██╔╝██║   ██║██╔════╝██║  ██║██╔══██╗██║     
    █████╔╝ ██║   ██║███████╗███████║███████║██║     
    ██╔═██╗ ██║   ██║╚════██║██╔══██║██╔══██║██║     
    ██║  ██╗╚██████╔╝███████║██║  ██║██║  ██║███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
    """
    print(colored(logo, 'green'))

    if args.output_file:
        try:
            output_file = open(args.output_file, "w")
        except Exception as e:
            print(f"Error opening output file: {e}")
            return
    else:
        output_file = None

    if args.sub:
        target_domain = args.target
        subdomains = get_subdomains(target_domain)
        print("Subdomains for", target_domain, ":")
        for subdomain in subdomains:
            print(subdomain)
            if output_file:
                output_file.write(subdomain + "\n")

    if args.ports:
        target = args.target
        ports = args.ports
        scan(target, ports)

    if output_file:
        output_file.close()
    print(f"Total subdomains found: {len(subdomains)}")


if __name__ == "__main__":
    main()
