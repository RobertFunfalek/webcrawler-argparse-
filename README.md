Web Crawler with Adjustable Aggressiveness

This project is a multi-threaded web crawler implemented in Python, capable of traversing a website and determining the working status of the links it encounters. It allows users to adjust crawling depth, aggressiveness levels, and handles rate limiting. It is built using the requests, BeautifulSoup, and concurrent.futures libraries to ensure efficient performance across various platforms.

Features

Multi-threaded Crawling: Uses a thread pool to manage multiple link checks concurrently, improving efficiency.

Adjustable Aggressiveness: Control the rate of requests to avoid overwhelming target servers.

Depth Control: Set the maximum depth for crawling to determine how deep the crawler goes within the domain.

Link Classification: Stores working and non-working links in separate CSV files.

Domain Control: Only crawls links that belong to the same domain as the start URL.

Ignore Specific Links: Ability to ignore URLs that contain specified keywords.

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

To crawl https://uniag.sk/ with a depth of 3 and an aggressiveness level of 2:

python web_crawler.py https://uniag.sk/ -d 3 -a 2

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
