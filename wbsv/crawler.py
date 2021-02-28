from urllib import parse
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup as BS


class MissingURLSchemaError(Exception):
    pass


class Clawler:
    def __init__(self, args):
        self.urls = self._normalize_url(args.url)
        self.only_target = args.only_target
        self.level = args.level
        self.queue = []
        self.UA = 'Mozilla/5.0 (Windows NT 5.1; rv:40.0) '\
                  'Gecko/20100101 Firefox/40.0'

    def run_crawl(self):
        if self.only_target:
            return [set(self.urls)]
        for now_level in range(self.level):
            collecting_links = set()
            collected_links = set().union(*self.queue)
            if now_level == 0:
                self.queue.append(set(self.urls))
            for url in self.queue[-1]:
                source = requests.get(
                    url, headers={'User-Agent': self.UA}).content
                data = BS(source, parser="html.parser", features="lxml")
                extracted_url = [urljoin(url, _.get('href'))
                                 for _ in set(data.find_all('a'))]
                collecting_links |= set(self._normalize_url(extracted_url))
            self.queue.append(collecting_links - collected_links)

        return self.queue

    def _normalize_url(self, urls):
        valid_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            if self._check_schema(parsed_url):
                raise MissingURLSchemaError(
                    '{}: schema {} is not valid.'.format(url, parsed_url.scheme))
            valid_urls.append(parsed_url.geturl())
        return valid_urls

    def _check_schema(self, parsed_url):
        return parsed_url.scheme == '' or not parsed_url.scheme in ('http', 'https', 'ftp', 'file')