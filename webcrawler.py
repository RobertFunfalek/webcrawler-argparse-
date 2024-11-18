import csv
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, unquote
import multiprocessing
import argparse
import time
from threading import Lock

# Argument parsing to configure the crawl
parser = argparse.ArgumentParser(description="Web Crawler with Adjustable Aggressiveness and Cross-Platform Support")
parser.add_argument("domain", help="The starting domain to crawl")
parser.add_argument("-d", "--depth", type=int, default=2, help="Maximum crawling depth")
parser.add_argument("-w", "--working_file", default="working.csv", help="CSV file to store working links")
parser.add_argument("-n", "--not_working_file", default="not_working.csv", help="CSV file to store non-working links")
parser.add_argument("-a", "--aggressiveness", type=int, choices=[1, 2, 3, 4, 5], default=1, help="Aggressiveness level (1-5)")
parser.add_argument("--ignored_contains", default="", help="Comma-separated list of URL parts to ignore (e.g., 'news,archive')")
args = parser.parse_args()

# Set configurations based on arguments
START_URL = args.domain
MAX_DEPTH = args.depth
WORKING_FILE = args.working_file
NOT_WORKING_FILE = args.not_working_file
AGGRESSIVENESS = args.aggressiveness
IGNORED_CONTAINS = args.ignored_contains.split(",") if args.ignored_contains else []

# Set delay based on aggressiveness level
AGGRESSIVENESS_DELAY = {
    1: 1,     # 1 request per second
    2: 0.5,   # 2 requests per second
    3: 0.2,   # 5 requests per second
    4: 0.1,   # 10 requests per second
    5: 0       # Full throttle (no delay)
}
TASK_DELAY = AGGRESSIVENESS_DELAY[AGGRESSIVENESS]

# Lock for rate limiting
rate_limit_lock = Lock()
last_request_time = [0]

# Set max workers for thread pool based on CPU availability
MAX_WORKERS = min(40, max(1, int(multiprocessing.cpu_count() * 0.8)))

def rate_limited_request():
    """Control the rate of requests based on aggressiveness level."""
    if TASK_DELAY > 0:
        with rate_limit_lock:
            current_time = time.time()
            elapsed = current_time - last_request_time[0]
            if elapsed < TASK_DELAY:
                time.sleep(TASK_DELAY - elapsed)
            last_request_time[0] = time.time()

def check_link(url):
    """Function to check if a URL is working using a HEAD request."""
    rate_limited_request()
    try:
        response = requests.head(url, timeout=0.5)
        if response.status_code in [200, 302]:
            return url, response.status_code
        else:
            return url, response.status_code
    except requests.RequestException as e:
        return url, "Error"

def get_links(url):
    """Retrieve and parse links from a given URL."""
    rate_limited_request()
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        absolute_links = [urljoin(url, link) for link in links if is_same_domain(url, link)]
        return absolute_links
    except requests.RequestException as e:
        print(f"Chyba pri načítaní stránky {url}: {e}")
        return []

def is_same_domain(base_url, link):
    """Check if a link is within the same domain as the base URL."""
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(urljoin(base_url, link)).netloc
    return base_domain == link_domain

def is_ignored(link):
    """Check if a link contains any of the ignored parts."""
    return any(ignored in link for ignored in IGNORED_CONTAINS)

def crawl_and_check_links(start_url, max_depth):
    """Main function to crawl and check links up to the specified depth."""
    visited = set()
    with open(WORKING_FILE, "w", newline="", encoding="utf-8-sig") as working_csv, \
         open(NOT_WORKING_FILE, "w", newline="", encoding="utf-8-sig") as not_working_csv:

        working_writer = csv.writer(working_csv)
        not_working_writer = csv.writer(not_working_csv)
        
        # Writing headers
        working_writer.writerow(["URL", "Status Code"])
        not_working_writer.writerow(["URL", "Status Code"])

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(crawl, start_url, max_depth, visited, 1, working_writer, not_working_writer): start_url}
            for future in as_completed(futures):
                future.result()

def crawl(url, depth, visited, current_level, working_writer, not_working_writer):
    """Recursive helper for crawling and checking links."""
    if url in visited or depth == 0 or is_ignored(url):
        return

    visited.add(url)
    print(f"Prehľadávam úroveň {current_level} pre URL: {url}")
    links = get_links(url)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(check_link, link): link for link in links}
        for future in as_completed(future_to_url):
            link = future_to_url[future]
            result = future.result()
            decoded_url = unquote(result[0])
            status_code = result[1]
            print(f"{decoded_url} - {status_code}")

            if status_code == 200 or status_code == 302:
                working_writer.writerow([decoded_url, status_code])
            else:
                not_working_writer.writerow([decoded_url, status_code])

    for link in links:
        if link not in visited and not is_ignored(link):
            crawl(link, depth - 1, visited, current_level + 1, working_writer, not_working_writer)

# Run the crawler with the specified configuration
crawl_and_check_links(START_URL, MAX_DEPTH)
