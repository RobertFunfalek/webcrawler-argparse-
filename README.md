Web Crawler with Adjustable Aggressiveness

This project is a multi-threaded web crawler implemented in Python, capable of traversing a website and determining the working status of the links it encounters. It allows users to adjust crawling depth, aggressiveness levels, and handles rate limiting. It is built using the requests, BeautifulSoup, and concurrent.futures libraries to ensure efficient performance across various platforms.

Features

Multi-threaded Crawling: Uses a thread pool to manage multiple link checks concurrently, improving efficiency.

Adjustable Aggressiveness: Control the rate of requests to avoid overwhelming target servers.

Depth Control: Set the maximum depth for crawling to determine how deep the crawler goes within the domain.

Link Classification: Stores working and non-working links in separate CSV files.

Domain Control: Only crawls links that belong to the same domain as the start URL.

Ignore Specific Links: Ability to ignore URLs that contain specified keywords.

How It Works

Rate Limiting

The crawler limits the rate of requests based on the aggressiveness level specified by the user. The rate limiting is implemented using a locking mechanism and time delays to ensure that requests are sent at an appropriate interval, preventing the crawler from overwhelming the target server. The following steps explain how rate limiting is managed:

Aggressiveness Levels: The user specifies an aggressiveness level from 1 to 5, where level 1 is the least aggressive (1 request per second) and level 5 is the most aggressive (full throttle with no delay).

Delay Management: The delay between requests is determined based on the aggressiveness level. For example, an aggressiveness level of 1 enforces a 1-second delay between requests, whereas level 5 has no enforced delay.

Thread Synchronization: A lock (rate_limit_lock) is used to ensure that only one thread can update the timing of the next request at a time, preventing race conditions. The time of the last request is tracked (last_request_time), and each thread checks the elapsed time since the last request before making a new one.

Multi-Threaded Crawling

The crawler uses the ThreadPoolExecutor from the concurrent.futures library to manage concurrent crawling tasks. The number of threads (MAX_WORKERS) is determined based on the available CPU cores to balance efficiency and resource usage. Each thread can:

Check Links: Make HEAD requests to verify if a link is working.

Get Links: Retrieve links from a webpage using BeautifulSoup to parse the HTML.

The thread pool allows multiple links to be processed simultaneously, significantly speeding up the crawling process.

Recursive Crawling

The crawler uses a recursive approach to explore links up to the specified depth:

Start URL: The crawling process begins with the specified domain (START_URL).

Link Extraction: Links are extracted from the current webpage and filtered to ensure they belong to the same domain.

Depth Control: The recursion continues until the maximum depth (MAX_DEPTH) is reached, allowing the user to control how deep the crawler goes into the domain.

Visited Links: A set (visited) is maintained to track the links that have already been crawled, preventing duplication and infinite loops.

Link Classification

Links are classified based on their status codes:

Working Links: URLs that return a status code of 200 or 302 are classified as working and are written to the working CSV file (WORKING_FILE).

Non-Working Links: URLs that return other status codes or encounter errors are classified as non-working and are written to the non-working CSV file (NOT_WORKING_FILE).

The status of each link is determined using a HEAD request to reduce the amount of data transferred, making the crawler more efficient.

Ignored Links

The crawler provides the ability to ignore specific links based on keywords. The user can specify a comma-separated list of keywords (--ignored_contains) that should be avoided during crawling. Any URL containing these keywords will be skipped, reducing unnecessary crawling and focusing only on relevant content.

Function Descriptions

rate_limited_request()

Controls the rate of requests based on the aggressiveness level. It uses a lock to ensure only one thread can update the timing of the next request, helping manage rate limiting.

check_link(url)

Checks if a URL is working by making a HEAD request. Returns the URL and the status code. Handles any request exceptions gracefully by returning an error status.

get_links(url)

Retrieves and parses links from a given URL using BeautifulSoup. Filters links to include only those belonging to the same domain and returns them as absolute URLs.

is_same_domain(base_url, link)

Determines whether a given link belongs to the same domain as the base URL. This helps ensure the crawler only stays within the target domain.

is_ignored(link)

Checks if a link should be ignored based on the presence of specified keywords. This helps skip unnecessary or irrelevant links during the crawling process.

crawl_and_check_links(start_url, max_depth)

The main function that initiates the crawling process. Opens CSV files to store working and non-working links, sets up the thread pool, and starts crawling from the given start URL.

crawl(url, depth, visited, current_level, working_writer, not_working_writer)

A recursive helper function that performs the crawling process. Extracts links, checks their status, and writes them to the appropriate CSV file. Recursively crawls deeper links up to the specified depth.

Prerequisites

Python 3.x

The following Python libraries are required:

requests

beautifulsoup4

concurrent.futures

You can install the dependencies using the following command:

pip install requests beautifulsoup4

Usage

To run the web crawler, use the following command:

python web_crawler.py <domain> [options]

Arguments

domain: The starting domain to crawl (e.g., https://example.com/).

Options

-d, --depth: Maximum crawling depth (default: 2).

-w, --working_file: CSV file to store working links (default: working.csv).

-n, --not_working_file: CSV file to store non-working links (default: not_working.csv).

-a, --aggressiveness: Aggressiveness level (1-5) to control request rate (default: 1).

--ignored_contains: Comma-separated list of URL parts to ignore (e.g., news,archive).

Example

To crawl https://example.com/ with a depth of 3 and an aggressiveness level of 2:

python web_crawler.py https://example.com/ -d 3 -a 2

Aggressiveness Levels

The aggressiveness level controls the rate of requests:

1: 1 request per second (least aggressive)

2: 2 requests per second

3: 5 requests per second

4: 10 requests per second

5: Full throttle (no delay)

Output

The crawler will create two CSV files:

Working Links: Contains URLs that responded with status codes 200 or 302.

Non-Working Links: Contains URLs that either responded with errors or other status codes.

Notes

The crawler uses a recursive approach to explore links up to the specified depth.

Rate limiting is enforced to avoid overwhelming servers, based on the aggressiveness level specified.

Multi-threading improves crawling speed by allowing multiple requests to be processed simultaneously.
