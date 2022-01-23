from argparse import Namespace
from typing import Iterable, List, Set
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup as BS  # type: ignore

from wbsv.url_filters import CombinedFilter, OwnDomainFilter, SchemaFilter, UrlFilter


class MissingURLSchemaWarning(UserWarning):
    pass


class Crawler:
    @staticmethod
    def from_parser_args(args: Namespace) -> "Crawler":
        return Crawler.from_args(args.url, args.own, args.only_target, args.level)

    @staticmethod
    def from_args(
        urls: Iterable[str], own: bool, only_target: bool, level: int
    ) -> "Crawler":
        schema_filter = SchemaFilter()
        normalized_urls = Crawler._normalize_urls(urls, schema_filter)
        domain_filters = (
            [schema_filter, OwnDomainFilter.from_string_urls(set(normalized_urls))]
            if own
            else [schema_filter]
        )
        return Crawler(
            urls=normalized_urls,
            domain_filter=CombinedFilter(domain_filters),
            only_target=only_target,
            level=level,
        )

    def __init__(
        self, urls: List[str], domain_filter: UrlFilter, only_target: bool, level: int
    ):
        """Init."""
        self.urls = urls
        self.domain_filter = domain_filter
        self.only_target = only_target
        self.level = level
        self.queue: List[Set[str]] = []
        self.UA: str = (
            "Mozilla/5.0 (Windows NT 5.1; rv:40.0) " "Gecko/20100101 Firefox/40.0"
        )

    def run_crawl(self) -> List[Set[str]]:
        """Execute crawler."""
        if self.only_target:
            return [set(self.urls)]
        for now_level in range(self.level):
            self._crawl(now_level)

        return self.queue

    def _crawl(self, now_level: int) -> None:
        """Helper for crawling."""
        collecting_links = set()
        collected_links: Set[str] = set()
        collected_links = collected_links.union(*self.queue)
        if now_level == 0:
            self.queue.append(set(self.urls))
        for url in self.queue[-1]:
            source = requests.get(url, headers={"User-Agent": self.UA}).content
            data = BS(source, features="lxml")
            extracted_urls = [
                urljoin(url, _.get("href")) for _ in set(data.find_all("a"))
            ]
            collecting_links |= set(
                Crawler._normalize_urls(extracted_urls, url_filter=self.domain_filter)
            )
        self.queue.append(collecting_links - collected_links)

    @staticmethod
    def _normalize_urls(urls: Iterable[str], url_filter: UrlFilter) -> List[str]:
        """Normalize parsed_url."""
        valid_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            if url_filter.test_url(parsed_url):
                valid_urls.append(urldefrag(parsed_url.geturl()).url)
        return valid_urls
