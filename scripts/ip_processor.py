import ipaddress
import requests
from pathlib import Path

def download_ip_data(url):
    """Download IP data from the given URL"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download data. Status code: {response.status_code}")

def ip_range_to_cidrs(start_ip, end_ip):
    """Convert an IP range to CIDR blocks"""
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    return [str(cidr) for cidr in ipaddress.summarize_address_range(start, end)]

def process_data(data, countries):
    """Process the raw data and return filtered CIDR blocks"""
    results = {country: [] for country in countries}
    
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(',')
        if len(parts) != 3:
            continue
            
        start_ip, end_ip, country = parts
        if country not in countries:
            continue
            
        try:
            cidrs = ip_range_to_cidrs(start_ip, end_ip)
            results[country].extend(cidrs)
        except:
            continue
            
    return results

def save_to_file(filename, cidr_list):
    """Save CIDR list to a file"""
    with open(filename, 'w') as f:
        for cidr in cidr_list:
            f.write(f"{cidr}\n")

def main():
    url = "https://raw.githubusercontent.com/sapics/ip-location-db/refs/heads/main/iplocate-country/iplocate-country-ipv4.csv"
    countries = ['IR']
    output_dir = Path.cwd()
    
    print("Downloading IP data...")
    data = download_ip_data(url)
    
    print("Processing data...")
    results = process_data(data, countries)
    
    print("Saving results to files...")
    save_to_file(output_dir / "ir.txt", results['IR'])
    
    print("Done! Files saved as ir.txt")

if __name__ == "__main__":
    main()
