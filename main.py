import requests
import time
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

ua = UserAgent()

# Generate a random user-agent string
random_user_agent = ua.random

def get_proxies():
    proxy_api_url = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000'
    response = requests.get(proxy_api_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print("Failed to retrieve proxies")
        return []

headers = {
    'user-agent': random_user_agent
}

string_to_check = "https://iws.lol"

print("=> Starting....")

# Read the URLs to check from a file
with open('data.txt', 'r', encoding='utf-8') as to_check:
    urls_to_check = to_check.read().splitlines()

def check_url(url, proxy):
    try:
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if string_to_check in r.text:
            return f"OK => {url} => {proxy}"
        else:
            return f"Fail => {url}"
    except requests.RequestException:
        return None

while True:
    proxies_list = get_proxies()  # Re-fetch proxies at the beginning of each iteration

    with ThreadPoolExecutor(max_workers=20000) as executor:
        futures = []
        proxy_index = 0

        for url in urls_to_check:
            proxy = proxies_list[proxy_index % len(proxies_list)]
            proxy_index += 1
            futures.append(executor.submit(check_url, url, proxy))
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)

    print("\n")
