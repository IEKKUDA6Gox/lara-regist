import requests
import argparse
import os
import concurrent.futures

def check_url(url):
    try:
        http_url = "http://" + url
        https_url = "https://" + url
        
        for url in [http_url, https_url]:
            response = requests.get(url)
            if 'name="csrf-token"' in response.text or 'uploadForm' in response.text:
                print(f"[+] {url} - Found")
                return url
        print(f"[-] {url} - Not Found")
    except requests.exceptions.RequestException as e:
        print(f"[-] {url} - Error: {e}")
    return None

def print_banner():
    banner = r"""
##################################################################################################
#  _                              _   _____ _ _                                                  #
# | |    __ _ _ __ __ ___   _____| | |  ___(_) | ___ _ __ ___   __ _ _ __   __ _  __ _  ___ _ __ #
# | |   / _` | '__/ _` \ \ / / _ \ | | |_  | | |/ _ \ '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \ '__|#
# | |__| (_| | | | (_| |\ V /  __/ | |  _| | | |  __/ | | | | | (_| | | | | (_| | (_| |  __/ |   #
# |_____\__,_|_|  \__,_| \_/ \___|_| |_|   |_|_|\___|_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|_|   #
#                                                                                |___/           #
#                                              https://github.com/IEKKUDA6Gox                    #
##################################################################################################
    """
    print(banner)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    parser = argparse.ArgumentParser(description="Path URL Scanner", formatter_class=argparse.RawTextHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", type=str, help="URL to scan")
    group.add_argument("-l", "--list", type=str, help="File containing list of URLs to scan")
    parser.add_argument("-o", "--output", type=str, help="Output file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    args = parser.parse_args()

    paths = [
        "/filemanager",
        "/laravel-filemanager",
        "/file-manager",
        "/files-manager",
        "/laravel/filemanager",
        "/laravel/laravel-filemanager",
        "/laravel/file-manager",
        "/laravel/files-manager",
        "/public/filemanager",
        "/public/laravel-filemanager",
        "/public/laravel/filemanager",
        "/public/laravel/laravel-filemanager",
        "/admin/uploads",
        "/admin/media",
        "/file-manager/index",
    ]

    urls = []

    if args.url:
        for path in paths:
            urls.append(args.url + path)
    elif args.list:
        with open(args.list, "r") as f:
            for line in f:
                line = line.strip()
                line_urls = []  
                for path in paths:
                    line_urls.append(line + path)
                urls.extend(line_urls)  

    print(f"\n[INF] Total URL target for scan: {len(line_urls)}")
    print("[INF] Start : ")

    found_urls = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = executor.map(check_url, urls)
        for result in results:
            if result:
                found_urls.append(result)

    if args.output:
        with open(args.output, "w") as f:
            for url in found_urls:
                f.write(f"{url}\n")

if __name__ == "__main__":
    main()
