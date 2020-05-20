from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from http.client import IncompleteRead
from random import randint
import time

from bs4 import BeautifulSoup

from urllib.parse import urlparse, urljoin


class Finder:
    def __init__(self):
        """initialize."""
        self.urls = set()
        self.fetched_urls = set()

    def clean(self):
        self.urls = set()

    def print_result(self):
        print("Fetched:", len(self.fetched_urls), "URLs, ",
            "Found:", len(self.urls), "URLs")

    def parse_opt(self, opt):
        self.search_url_depth = opt["level"]
        if opt["only-target"] :
            self.search_url_depth = 0

    @staticmethod
    def is_page(url):
        """Judge whether str is webpage."""
        exclude_suffixes = (".css", ".gif", ".jpeg", ".jpg",
                            ".js", ".json", ".png", ".svg")
        url_parts = urlparse(url)
        return not url_parts.fragment and not url_parts.path.endswith(
            exclude_suffixes)

    @staticmethod
    def is_valid_scheme(url):
        """Judge whether url is valid scheme."""
        return urlparse(url).scheme in ["ftp", "gopher", "http", "https"]

    @staticmethod
    def remove_useless(l):
        """Remove not available data from list."""
        return {x for x in l if x is not None and len(x) > 1}

    def find_uri(self, url):
        """Find links in page."""
        # extract elements containing of uri links in a page
        if url in self.fetched_urls :
            return set()
        else:
            self.fetched_urls.add(url)

        try:
            print("Fetching: "+url)
            html_source = urlopen(url)
        except (HTTPError, URLError, UnicodeEncodeError):
            return set()

        html_source_charset = html_source.headers.get_content_charset(
            failobj="utf-8")

        try:
            html_decoded = html_source.read().decode(
                html_source_charset, 'ignore'
            )
            uris_misc = BeautifulSoup(html_decoded, "html.parser").findAll(
                ["a"]
            )
        except IncompleteRead:
            uris_misc = []

        # extract uri link data
        uris_misc = sum([[i.get("href")] for i in uris_misc], [])
        # change "relative" uri into "absolute" one
        uris_misc = {urljoin(url, i) for i in uris_misc}
        # exclude mailto:// or javascript:// ...
        uris_misc = {i for i in uris_misc if self.is_valid_scheme(i) and self.is_page(i)}
        return self.remove_useless(uris_misc)

    def extract_uri_recursive(self, url, depth):
        # to exit extracting URL, Listen KeyboardInterrupt arround this method.
        if depth==0 :
            self.urls.add(url)
            return
        elif depth==1 :
            self.urls |= self.find_uri(url)
            return
        else:
            included_urls = self.find_uri(url)
            for l in included_urls :
                self.extract_uri_recursive(l, depth-1)
                time.sleep(randint(2,5))

            self.urls |= included_urls

    def find_and_archive(self, url, archiver):
        try:
            self.extract_uri_recursive(url, self.search_url_depth)
        except KeyboardInterrupt:
            print("Interrupt: Stopped extracting url.")

        self.print_result()

        try:
            for l in self.urls :
                archiver.archive(l)
        except KeyboardInterrupt:
            print("Interrupt: Stopped saving pages.")
