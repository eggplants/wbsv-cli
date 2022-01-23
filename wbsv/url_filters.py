import dataclasses
from abc import ABC, abstractmethod
from typing import Iterable, Set
from urllib.parse import ParseResult, urlparse


class UrlFilter(ABC):
    @abstractmethod
    def test_url(self, parsed_url: ParseResult) -> bool:
        pass


@dataclasses.dataclass
class SchemaFilter(UrlFilter):
    valid_schemas: Set[str] = dataclasses.field(
        default_factory=lambda: {"http", "https", "ftp", "file"}
    )

    def test_url(self, parsed_url: ParseResult) -> bool:
        return parsed_url.scheme in self.valid_schemas


@dataclasses.dataclass
class OwnDomainFilter(UrlFilter):
    own_domains: Set[str]

    @staticmethod
    def from_string_urls(urls: Iterable[str]) -> "OwnDomainFilter":
        return OwnDomainFilter({urlparse(url).netloc for url in urls})

    def test_url(self, parsed_url: ParseResult) -> bool:
        return parsed_url.netloc in self.own_domains


@dataclasses.dataclass
class CombinedFilter(UrlFilter):
    filters: Iterable[UrlFilter]

    def test_url(self, parsed_url: ParseResult) -> bool:
        return all(f.test_url(parsed_url) for f in self.filters)
