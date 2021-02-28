import pytest

from wbsv import crawler, main


def test1():
    args = main.parse_args(test=['https://example.com', '-l', '1'])
    c = crawler.Clawler(args)
    assert {'https://example.com',
            'https://www.iana.org/domains/example'} == set().union(*c.run_crawl())
