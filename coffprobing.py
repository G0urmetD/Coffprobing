import sys
import json
import time
import argparse
import requests
import concurrent.futures

from colorama import Fore, Style
from pathlib import Path

# Constants
VERSION = "1.1.0"
BANNER = f"""

   ______      ________                 __    _            
  / ____/___  / __/ __/___  _________  / /_  (_)___  ____ _
 / /   / __ \/ /_/ /_/ __ \/ ___/ __ \/ __ \/ / __ \/ __ `/
/ /___/ /_/ / __/ __/ /_/ / /  / /_/ / /_/ / / / / / /_/ / 
\____/\____/_/ /_/ / .___/_/   \____/_.___/_/_/ /_/\__, /  
                  /_/                             /____/   {VERSION}
                                                           G0urmetD

"""
GITHUB_RELEASE_URL = "https://api.github.com/repos/G0urmetD/Coffprobing/releases/latest"  # Update this URL

# Check for latest version
def check_version():
    try:
        response = requests.get(GITHUB_RELEASE_URL, timeout=5)
        if response.status_code == 200:
            latest_version = response.json().get("tag_name")
            if latest_version == VERSION:
                print(f"{Fore.BLUE}[INF]{Style.RESET_ALL} Coffprobing has the [{Fore.GREEN}latest{Style.RESET_ALL}] version: {VERSION} ...")
            else:
                print(f"{Fore.BLUE}[INF]{Style.RESET_ALL} Coffprobing has an [{Fore.RED}old{Style.RESET_ALL}] version: {VERSION} ...")
        else:
            print(f"[{Fore.RED}WRN{Style.RESET_ALL}] Could not verify the latest version.")
    except Exception as e:
        print(f"[{Fore.RED}WRN{Style.RESET_ALL}] Version check failed: {e}")

# Helper to make requests
def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        return url, response.status_code
    except requests.exceptions.RequestException:
        return url, "Unreachable"

# Main tool functionality
def probe_urls(subdomains, rate_limit, filter_code):
    grouped_results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for subdomain in subdomains:
            for prefix in ["http://", "https://"]:
                futures.append(executor.submit(check_url, f"{prefix}{subdomain}"))

        start_time = time.time()
        for future in concurrent.futures.as_completed(futures):
            url, status_code = future.result()

            if filter_code and status_code != filter_code:
                continue

            if status_code not in grouped_results:
                grouped_results[status_code] = []
            grouped_results[status_code].append(url)

            # Rate limiting
            time.sleep(1 / rate_limit)
        end_time = time.time()

    return grouped_results, end_time - start_time

# Output results
def save_results(grouped_results):
    if 200 in grouped_results:
        with open("200er-results.txt", "w") as f:
            f.write("\n".join(grouped_results[200]))

    for code in [401, 403]:
        if code in grouped_results:
            with open("401and403-results.txt", "w") as f:
                f.write("\n".join(grouped_results.get(401, []) + grouped_results.get(403, [])))

# Print results
def print_results(grouped_results, scan_duration):
    for status_code, urls in grouped_results.items():
        if isinstance(status_code, int):  # Check if the status_code is an integer
            if status_code == 200:
                color = Fore.GREEN
            elif 300 <= status_code < 400:
                color = Fore.YELLOW
            elif 400 <= status_code < 500:
                color = Fore.RED
            elif 500 <= status_code < 600:
                color = Fore.MAGENTA
            else:
                color = Style.RESET_ALL
        else:  # For non-integer status codes (e.g., "Unreachable")
            color = Style.RESET_ALL

        print(f"[ HTTP-CODE = {status_code} ]")
        for url in urls:
            print(f"{color}{url}{Style.RESET_ALL}")
        print()

    print(f"[{Fore.YELLOW}INF{Style.RESET_ALL}] Scan duration: {scan_duration:.2f} seconds")

# Main function
def main():
    print(BANNER)
    check_version()

    parser = argparse.ArgumentParser(description="Coffprobing - Subdomain URL checker")
    parser.add_argument("-mt", "--mass-target", type=str, required=True, help="Path to file containing subdomains")
    parser.add_argument("-fc", "--filter-code", type=int, help="Filter specific HTTP codes in the output")
    parser.add_argument("-r", "--rate-limit", type=int, default=10, help="Requests per second (default: 10)")

    args = parser.parse_args()

    # Read subdomains from file
    subdomains_file = Path(args.mass_target)
    if not subdomains_file.exists():
        print(f"[{Fore.RED}ERR{Style.RESET_ALL}] File {args.mass_target} not found.")
        sys.exit(1)

    with open(subdomains_file, "r") as f:
        subdomains = [line.strip() for line in f if line.strip()]

    # Run URL probing
    grouped_results, scan_duration = probe_urls(subdomains, args.rate_limit, args.filter_code)

    # Save and display results
    save_results(grouped_results)
    print_results(grouped_results, scan_duration)

if __name__ == "__main__":
    main()
