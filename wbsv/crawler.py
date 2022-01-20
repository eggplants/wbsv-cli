from typing import List
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup as BS


class MissingURLSchemaWarning(UserWarning):
    pass


class Crawler:
    def __init__(self, args):
        """Init."""
        self.urls = self._normalize_url(args.url, skip=True)
        self.own = args.own
        self.target_domains = [urlparse(u).netloc for u in self.urls]
        self.only_target = args.only_target
        self.level = args.level
        self.queue: List = []
        self.UA: str = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) " "Gecko/20100101 Firefox/40.0"

    def run_crawl(self):
        """Execute crawler."""
        if self.only_target:
            return [set(self.urls)]
        for now_level in range(self.level):
            self._crawl(now_level)

        return self.queue

    def _crawl(self, now_level):
        """Helper for crawling."""
        collecting_links = set()
        collected_links = set().union(*self.queue)
        if now_level == 0:
            self.queue.append(set(self.urls))
        for url in self.queue[-1]:
            source = requests.get(url, headers={"User-Agent": self.UA}).content
            data = BS(source, features="lxml")
            extracted_url = [
                urljoin(url, _.get("href")) for _ in set(data.find_all("a"))
            ]
            collecting_links |= set(self._normalize_url(extracted_url))
        self.queue.append(collecting_links - collected_links)

    def _normalize_url(self, urls, skip: bool = False):
        """Normalize url."""
        valid_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            if not skip and self.own and parsed_url.netloc not in self.target_domains:
                continue
            if not self._check_schema_is_invalid(parsed_url):
                valid_urls.append(urldefrag(parsed_url.geturl()).url)
        return valid_urls

    @staticmethod
    def _check_schema_is_invalid(parsed_url):
        """Judge if given url has a valid schema."""
        is_invalid = parsed_url.scheme not in ("http", "https", "ftp", "file")
        return parsed_url.scheme == "" or is_invalid
