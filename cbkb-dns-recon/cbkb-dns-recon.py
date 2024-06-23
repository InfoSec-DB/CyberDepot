import argparse
import subprocess
import re
import csv
import json
import os
import random
import logging
import sys
from tqdm import tqdm

def print_banner():
    banner_folder = "ASCIArt"
    if os.path.isdir(banner_folder):
        banners = [f for f in os.listdir(banner_folder) if os.path.isfile(os.path.join(banner_folder, f))]
        if banners:
            with open(os.path.join(banner_folder, random.choice(banners)), 'r') as f:
                banner = f.read()
                phrase = get_random_phrase()
                banner_lines = banner.split('\n')
                max_length = max(len(line) for line in banner_lines)
                
                if phrase:
                    # Calculate the position to place the phrase in the middle-right
                    middle_index = len(banner_lines) // 2
                    phrase_offset = max_length - len(phrase) - 1  # Offset from the right
                    if len(banner_lines[middle_index]) > phrase_offset:
                        banner_lines[middle_index] = banner_lines[middle_index][:phrase_offset] + phrase
                    else:
                        banner_lines[middle_index] = banner_lines[middle_index].ljust(phrase_offset) + phrase

                banner_with_phrase = "\n".join(banner_lines)
                print(banner_with_phrase)
                return banner_with_phrase
        else:
            print("No ASCII art banners found in ASCIArt folder.")
            return ""
    else:
        print("ASCIArt folder not found.")
        return ""

def get_random_phrase():
    phrases_file = "ASCIText/phrases.txt"
    if os.path.isfile(phrases_file):
        with open(phrases_file, 'r') as f:
            phrases = f.readlines()
        if phrases:
            phrase = random.choice([phrase.strip() for phrase in phrases])
            logging.debug(f"Selected phrase: {phrase}")
            return phrase
        else:
            logging.debug(f"No phrases found in {phrases_file}.")
            return "No phrases found in ASCIText file."
    else:
        logging.debug("ASCIText file not found.")
        return "ASCIText file not found."

def dig_query(server, record_type, domain, verbose=False):
    try:
        if verbose:
            print(f"Querying {record_type} records for {domain} on {server}")
        result = subprocess.check_output(['dig', f'@{server}', domain, record_type, '+short'], text=True)
        return result.strip().split('\n')
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"Error querying {record_type} records for {domain} on {server}: {e}")
        return []

def attempt_zone_transfer(ns_server, base_domain, verbose=False):
    try:
        if verbose:
            print(f"Attempting zone transfer for {base_domain} on {ns_server}")
        result = subprocess.check_output(['dig', f'@{ns_server}', base_domain, 'AXFR'], text=True)
        if "Transfer failed." in result or "connection timed out" in result:
            return None
        return result.strip()
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"Zone transfer failed for {base_domain} on {ns_server}: {e}")
        return None

def reverse_dns_lookup(ip, verbose=False):
    try:
        if verbose:
            print(f"Performing reverse DNS lookup for {ip}")
        result = subprocess.check_output(['dig', '-x', ip, '+short'], text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"Error performing reverse DNS lookup for {ip}: {e}")
        return None

def normalize_results(result):
    return ' '.join(sorted(result.split()))

def check_dns_poisoning(domain, dns_servers, verbose=False):
    results = {}
    discrepancies = False

    for server in dns_servers:
        result = dig_query(server, 'A', domain, verbose)
        normalized_result = normalize_results('\n'.join(result))
        results[server] = normalized_result

    reference_result = results[dns_servers[0]]

    for server in dns_servers:
        if results[server] != reference_result:
            discrepancies = True
            print(f"[!] Discrepancy detected on DNS Server {server}:")
            print(f"Expected: {reference_result}")
            print(f"Got: {results[server]}")

    if not discrepancies:
        print(f"[*] No DNS poisoning/domain hijacking detected for {domain}.")
    else:
        print(f"[!] Potential DNS poisoning/domain hijacking detected for {domain}!")

    return results

def perform_dns_recon(domains, base_domain, dns_servers, blacklist, verbose=False):
    results = []
    for domain in tqdm(domains, desc="Processing domains"):
        if domain in blacklist:
            print(f"[*] Skipping blacklisted domain: {domain}")
            continue

        print(f"\n### Querying DNS information for {domain} ###")

        domain_result = {
            'domain': domain,
            'A': [],
            'CNAME': [],
            'TXT': [],
            'NS': [],
            'MX': [],
            'zone_transfer': None,
            'PTR': [],
            'dns_poisoning': {}
        }

        # Query A records
        print("[*] A records:")
        for server in dns_servers:
            a_records = dig_query(server, 'A', domain, verbose)
            if a_records:
                domain_result['A'] = a_records
                print('\n'.join(a_records))
                break

        # Query CNAME records
        print("[*] CNAME records:")
        for server in dns_servers:
            cname_records = dig_query(server, 'CNAME', domain, verbose)
            if cname_records:
                domain_result['CNAME'] = cname_records
                print('\n'.join(cname_records))
                break

        # Query TXT records
        print("[*] TXT records:")
        for server in dns_servers:
            txt_records = dig_query(server, 'TXT', domain, verbose)
            if txt_records:
                domain_result['TXT'] = txt_records
                print('\n'.join(txt_records))
                break

        # Query NS records
        print("[*] NS records:")
        for server in dns_servers:
            ns_records = dig_query(server, 'NS', domain, verbose)
            if ns_records:
                domain_result['NS'] = ns_records
                print('\n'.join(ns_records))
                break

        # Query MX records
        print("[*] MX records:")
        for server in dns_servers:
            mx_records = dig_query(server, 'MX', domain, verbose)
            if mx_records:
                domain_result['MX'] = mx_records
                print('\n'.join(mx_records))
                break

        # Attempt Zone Transfer
        print("[*] Attempting Zone Transfer:")
        for ns in domain_result['NS']:
            zone_transfer_result = attempt_zone_transfer(ns, base_domain, verbose)
            if zone_transfer_result:
                domain_result['zone_transfer'] = zone_transfer_result
                print(zone_transfer_result)
                break
            else:
                print(f"Zone transfer failed for {domain} on {ns}")

        # Reverse DNS Lookups
        print("[*] Reverse DNS (PTR records):")
        for ip in domain_result['A']:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip):
                ptr_record = reverse_dns_lookup(ip, verbose)
                if ptr_record:
                    domain_result['PTR'].append({'ip': ip, 'ptr': ptr_record})
                    print(f"{ip} -> {ptr_record}")

        # Check DNS Poisoning/Domain Hijacking
        domain_result['dns_poisoning'] = check_dns_poisoning(domain, dns_servers, verbose)
        results.append(domain_result)

    return results

def output_results(results, output_file):
    _, file_extension = os.path.splitext(output_file)
    output_format = file_extension.lower().replace('.', '')

    if output_format == 'csv':
        keys = results[0].keys()
        with open(output_file, 'w', newline='') as output_csv:
            dict_writer = csv.DictWriter(output_csv, keys)
            dict_writer.writeheader()
            for result in results:
                row = {key: json.dumps(value) if isinstance(value, list) or isinstance(value, dict) else value for key, value in result.items()}
                dict_writer.writerow(row)
    elif output_format == 'json':
        with open(output_file, 'w') as output_json:
            json.dump(results, output_json, indent=4)
    elif output_format == 'txt':
        with open(output_file, 'w') as output_txt:
            for result in results:
                output_txt.write(json.dumps(result, indent=4))
                output_txt.write('\n\n')
    else:
        print(f"Unsupported output format: {output_format}")

def retrieve_subdomains_with_sublist3r(domain, verbose=False):
    try:
        if verbose:
            print(f"Retrieving subdomains for {domain} using Sublist3r")
        subprocess.check_output(['sublist3r', '-d', domain, '-o', 'subdomains.txt'], text=True)
        with open('subdomains.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving subdomains for {domain} using Sublist3r: {e}")
        return []

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Perform DNS reconnaissance.")
    parser.add_argument('-f', '--file', help="Input file with list of domains.")
    parser.add_argument('-b', '--base-domain', required=True, help="Base domain for zone transfer attempts.")
    parser.add_argument('-s', '--dns-servers', nargs='+', default=['8.8.8.8', '1.1.1.1', '9.9.9.9'], help="List of DNS servers to query.")
    parser.add_argument('-bl', '--blacklist', help="Input file with list of blacklisted domains.")
    parser.add_argument('-o', '--output-file', required=True, help="Output file to save the results.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose debugging output.")

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    else:
        domains = retrieve_subdomains_with_sublist3r(args.base_domain, args.verbose)

    blacklist = []
    if args.blacklist:
        if os.path.exists(args.blacklist):
            with open(args.blacklist, 'r') as bl_file:
                blacklist = [line.strip() for line in bl_file if line.strip()]
        else:
            print(f"Blacklist file {args.blacklist} not found. Continuing without a blacklist.")
    
    results = perform_dns_recon(domains, args.base_domain, args.dns_servers, blacklist, args.verbose)
    output_results(results, args.output_file)

if __name__ == "__main__":
    main()
