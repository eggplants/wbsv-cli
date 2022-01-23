from typing import Iterable, Set, TypedDict
from urllib.parse import urlparse

from wbsv import crawler, main

# UrlFilter unit tests
from wbsv.url_filters import OwnDomainFilter, SchemaFilter


class ArgDict(TypedDict):
    urls: Iterable[str]
    own: bool
    only_target: bool
    level: int


def test_schema_filter_should_reject_invalid_schema() -> None:
    schema_filter = SchemaFilter()
    invalid_schema_url = urlparse("data://test.txt")

    assert schema_filter.test_url(invalid_schema_url) is False


def test_schema_filter_should_accept_valid_schema() -> None:
    schema_filter = SchemaFilter()
    valid_schema_url = urlparse("https://example.com")

    assert schema_filter.test_url(valid_schema_url) is True


def test_own_domain_filter_should_reject_url_with_invalid_domain() -> None:
    own_domain_filter = OwnDomainFilter.from_string_urls(["https://example.com"])
    invalid_domain_url = urlparse("https://www.iana.org")

    assert own_domain_filter.test_url(invalid_domain_url) is False


def test_own_domain_filter_should_accept_url_with_valid_domain() -> None:
    own_domain_filter = OwnDomainFilter.from_string_urls(["https://example.com"])
    invalid_domain_url = urlparse("https://example.com")

    assert own_domain_filter.test_url(invalid_domain_url) is True


def test_api_without_parser() -> None:
    args: ArgDict = {
        "urls": ["https://example.com"],
        "own": False,
        "only_target": False,
        "level": 1,
    }
    c = crawler.Crawler.from_args(**args)
    urls = {"https://example.com", "https://www.iana.org/domains/example"}
    t: Set[str] = set()
    t = t.union(*c.run_crawl())
    if urls != t:
        raise AssertionError


def test1() -> None:
    args = main.parse_args(args_list=["https://example.com", "-l", "1"])
    c = crawler.Crawler.from_parser_args(args)
    urls = {"https://example.com", "https://www.iana.org/domains/example"}
    t: Set[str] = set()
    t = t.union(*c.run_crawl())
    if urls != t:
        raise AssertionError
