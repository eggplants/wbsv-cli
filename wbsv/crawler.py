from typing import List, Iterable
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup as BS


class MissingURLSchemaWarning(UserWarning):
    pass


class Crawler:
    @staticmethod
    def from_parser_args(args):
        return Crawler.from_args(args.url, args.own, args.only_target, args.level)

    @staticmethod
    def from_args(urls: Iterable[str], own: bool, only_target: bool, level: int):
        normalized_urls = Crawler._normalize_urls_static_init(urls)
        target_domains = {urlparse(u).netloc for u in normalized_urls} if own else set()
        return Crawler(
            urls=normalized_urls,
            own=own,
            target_domains=target_domains,
            only_target=only_target,
            level=level
        )

    def __init__(self, urls, own, target_domains, only_target, level):
        """Init."""
        self.urls = urls
        self.own = own
        self.target_domains = target_domains
        self.only_target = only_target
        self.level = level
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
            extracted_urls = [
                urljoin(url, _.get("href")) for _ in set(data.find_all("a"))
            ]
            collecting_links |= set(
                Crawler._normalize_urls_static(extracted_urls, own=self.own, target_domains=self.target_domains)
            )
        self.queue.append(collecting_links - collected_links)

    @staticmethod
    def _normalize_urls_static(urls: Iterable[str], own: bool, target_domains: Iterable[str]):
        """Normalize url."""
        valid_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            if own:
                if parsed_url.netloc not in target_domains:
                    continue
            if Crawler._check_schema_is_valid(parsed_url):
                valid_urls.append(urldefrag(parsed_url.geturl()).url)
        return valid_urls

    @staticmethod
    def _normalize_urls_static_init(urls: Iterable[str]):
        valid_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            if Crawler._check_schema_is_valid(parsed_url):
                valid_urls.append(urldefrag(parsed_url.geturl()).url)
        return valid_urls

    @staticmethod
    def _check_schema_is_valid(parsed_url):
        """Judge if given url has a valid schema."""
        return parsed_url.scheme in {"http", "https", "ftp", "file"}
