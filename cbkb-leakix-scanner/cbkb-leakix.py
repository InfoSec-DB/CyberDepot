import requests
import argparse
import csv
import json
from collections import defaultdict
import pyfiglet
import re
import logging
import sys

API_KEY = 'MIHSAb5UEEwGVKUVt80IB5Notk_Hj_R2XFmKTpXPkWH5ARuN'
BASE_URL = 'https://leakix.net'

def setup_logging(verbosity):
    log_level = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
    logging.basicConfig(level=log_level.get(verbosity, logging.DEBUG))
    logging.debug(f"Logging set to {logging.getLevelName(logging.getLogger().level)}")

def search_leaks(query, scope='leak', page=0):
    headers = {
        'api-key': API_KEY,
        'accept': 'application/json'
    }
    params = {
        'scope': scope,
        'q': query,
        'page': page
    }
    logging.debug(f"Querying LeakIX with params: {params}")
    response = requests.get(f'{BASE_URL}/search', headers=headers, params=params)
    logging.debug(f"Received response with status code {response.status_code}")
    
    if response.status_code == 204:
        logging.debug("No content found for the query")
        return []
    
    response.raise_for_status()
    return response.json()

def extract_info(url):
    match = re.search(r'(https?|http)://(.*):(.*)@', url)
    if match:
        username, password = match.groups()[1], match.groups()[2]
        return username, password
    return 'N/A', 'N/A'

def format_result(results, verbose):
    formatted_results = []
    for result in results:
        host = result.get('host', 'N/A')
        ip = result.get('ip', 'N/A')
        summary = result.get('summary', 'N/A')
        severity = result.get('leak', {}).get('severity', 'N/A')
        country = result.get('geoip', {}).get('country_name', 'N/A')
        city = result.get('geoip', {}).get('city_name', 'N/A')
        organization = result.get('network', {}).get('organization_name', 'N/A')
        url_match = re.search(r'url = (https?://\S+)', summary)
        branch_match = re.search(r'\[branch "(.*?)"\]', summary)

        if url_match:
            url = url_match.group(1)
            username, password = extract_info(url)
        else:
            url = 'N/A'
            username, password = 'N/A', 'N/A'

        branch_name = branch_match.group(1) if branch_match else 'N/A'

        domains = re.findall(r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', summary)
        domain_list = ', '.join(set(domains))

        formatted_result = {
            "Host": host,
            "IP": ip,
            "Summary": summary,
            "URL": url,
            "Username": username,
            "Password": password,
            "Branch": branch_name,
            "Severity": severity,
            "Location": f"{city}, {country}",
            "Organization": organization,
            "Domains": domain_list
        }
        
        if verbose:
            tags = result.get('tags', [])
            if not isinstance(tags, list):
                tags = []
            formatted_result.update({
                "Event Type": result.get('event_type', 'N/A'),
                "Event Source": result.get('event_source', 'N/A'),
                "Transport": ', '.join(result.get('transport', [])),
                "Protocol": result.get('protocol', 'N/A'),
                "Port": result.get('port', 'N/A'),
                "Tags": ', '.join(tags),
                "Time": result.get('time', 'N/A')
            })
        
        formatted_results.append(formatted_result)
    return formatted_results

def list_plugins():
    with open('plugins.txt') as f:
        plugins = f.read().splitlines()
        print("Available Plugins:")
        for plugin in plugins:
            print(f"  - {plugin}")

def validate_plugin(plugin):
    with open('plugins.txt') as f:
        valid_plugins = [p.split('=')[0].strip() for p in f.read().splitlines()]
        logging.debug(f"Valid plugins: {valid_plugins}")
        if plugin not in valid_plugins:
            print(f"Error: The plugin '{plugin}' is not in the list of available plugins.")
            print("Here are some available plugins:")
            for p in valid_plugins[:10]:  # Show only the first 10 plugins
                print(f"  - {p}")
            print("Use --list-plugins to see the full list of available plugins.")
            exit(1)

def save_results(results, output, format):
    if format == 'json':
        with open(output, 'w') as f:
            json.dump(results, f, indent=4)
    elif format == 'csv':
        keys = results[0].keys()
        with open(output, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
    else:  # raw text
        with open(output, 'w') as f:
            for result in results:
                for key, value in result.items():
                    f.write(f"{key}: {value}\n")
                f.write('-' * 40 + '\n')

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        print(f"\nError: {message}")
        self.exit(2)

    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        self._print_message(self.format_help(), file)

    def format_help(self):
        formatter = self._get_formatter()
        formatter.add_text(self.description)
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        formatter.add_arguments(self._actions)
        return formatter.format_help()

def main():
    # Generate the banner with the smmono12 font
    banner = pyfiglet.figlet_format("CBKB-LEAKIX", font="smmono12")
    spider_art = """
             uu$:$:$:$:$:$uu
          uu$$$$$$$$$$$$$$$$$uu
         u$$$$$$$$$$$$$$$$$$$$$u
         u$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$*   *$$$*   *$$$$$$u
       *$$$$*      u$u       $$$$*
        $$$u   CB  u$u   KB  u$$$
        $$$u      u$$$u      u$$$
         *$$$$uu$$$   $$$uu$$$$*
          *$$$$$$$*   *$$$$$$$*
            u$$$$$$$u$$$$$$$u
             u$*$*$*$*$*$*$u
  uuu        $$u$ $ $ $ $u$$       uuu
 u$$$$        $$u$u$u$u$u$$       u$$$$
  $$$$$uu      *$$$$$$$$$*     uu$$$$$$
u$$$$$$$$$$$      *****    uuuu$$$$$$$$$
$$$$***$$$$$$$$$$uuu   uu$$$$$$$$$***$$$*
 ***      **$$$$$$$$$$$uu **$***
          uuuu **$$$$$$$$$$uuu
 u$$$uuu$$$$$$$$$uu **$$$$$$$$$$$uuu$$$
 $$$$$$$$$$****           **$$$$$$$$$$$*
   *$$$$$*                      **$$$$**
     $$$*                         $$$$*

---------------------------------------------
	     -HACK THE PLANET-
---------------------------------------------

    """

    print(spider_art)
    print(banner)

    parser = CustomArgumentParser(description='Interact with LeakIX API for bug bounty results.')
    parser.add_argument('-p', '--plugins', type=str, help='Specify the plugins to search for.')
    parser.add_argument('-s', '--severity', type=str, choices=['low', 'medium', 'high', 'critical'], help='Specify the severity level to filter results.')
    parser.add_argument('-o', '--output', type=str, help='Specify the output file to save results.')
    parser.add_argument('--format', type=str, choices=['json', 'txt', 'csv'], default='txt', help='Specify the output format (default: txt)')
    parser.add_argument('-v', '--verbosity', action='count', default=0, help='Increase verbosity level (use -v, -vv, -vvv)')
    parser.add_argument('--list-plugins', action='store_true', help='List all available plugins.')
    parser.add_argument('--pages', type=int, default=5, help='Specify the number of pages to fetch (default: 5)')
    args = parser.parse_args()

    setup_logging(args.verbosity)

    if args.list_plugins:
        list_plugins()
        return

    if not args.plugins or not args.output:
        parser.print_help()
        if not args.plugins:
            print("\nError: You must specify a plugin using the -p option.")
        if not args.output:
            print("Error: You must specify an output file using the -o option.")
        exit(1)

    validate_plugin(args.plugins)

    query = f'+plugin:"{args.plugins}"'
    
    if args.severity:
        query += f' +severity:"{args.severity}"'

    results = []
    try:
        for page in range(args.pages):
            print(f"Searching Page {page + 1}")
            logging.info(f"Fetching page {page}")
            response = search_leaks(query, page=page)
            if not response:
                break
            results.extend(response)
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error occurred: {err}")
    except ValueError as err:
        logging.error(f"JSON parsing error: {err}")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")

    if not results:
        logging.warning("No results found.")
        return

    formatted_results = format_result(results, args.verbosity > 1)
    total_results = len(results)
    print(f"Total Results Found: {total_results}")

    save_results(formatted_results, args.output, args.format)
    print(f"Results saved to {args.output}")

if __name__ == '__main__':
    main()
