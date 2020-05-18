from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from http.client import IncompleteRead
import sys

from bs4 import BeautifulSoup

from urllib.parse import urlparse, urljoin


def is_page(url):
    """Judge whether str is webpage."""
    exclude_suffixes = (".css", ".gif", ".jpeg", ".jpg",
                        ".js", ".json", ".png", ".svg")
    url_parts = urlparse(url)
    return not url_parts.fragment and not url_parts.path.endswith(
        exclude_suffixes)


def is_valid_scheme(url):
    """Judge whether url is valid scheme."""
    return urlparse(url).scheme in ["ftp", "gopher", "http", "https"]


def remove_useless(l):
    """Remove not available data from list."""
    return {x for x in l if x is not None and len(x) > 1}


def find_uri(url):
    """Find links in page."""
    # extract elements containing of uri links in a page
    try:
        html_source = urlopen(url)

    except (HTTPError, URLError, UnicodeEncodeError) as e:
        print("[!]" + str(type(e)), file=sys.stderr)
        return set()

    html_source_charset = html_source.headers.get_content_charset(
        failobj="utf-8")

    try:
        html_decoded = html_source.read().decode(
            html_source_charset, 'ignore')
        uris_misc = BeautifulSoup(html_decoded, "html.parser").findAll(
            ["a"])

    except IncompleteRead:
        uris_misc = []

    # extract uri link data
    uris_misc = sum([[i.get("href")] for i in uris_misc], [])
    # change "relative" uri into "absolute" one
    uris_misc = {urljoin(url, i) for i in uris_misc}
    # exclude mailto:// or javascript:// ...
    uris_misc = {i for i in uris_misc if is_valid_scheme(i) and is_page(i)}
    return remove_useless(uris_misc)


def extract_uri_recursive(url, rec):
    """Extract uri links from a page."""
    uri_dic = {url}
    search_queue = [[url]]
    if rec == 0:
        uri_dic = find_uri(url)

    for lev in range(rec):
        print("[+]LEVEL: %d" % (lev + 1))
        add_dic = set()
        remain_count = 1
        for url in search_queue[-1]:
            print("[+]REMAIN:%d/%d" %
                  (remain_count, len(search_queue[-1])), end="\r")
            add_dic |= find_uri(url)
            remain_count += 1

        print("[+]LEVEL: %d FINISHED!" % (lev + 1))
        uri_dic |= add_dic
        search_queue.append(add_dic)

    return uri_dic
