import pytest

from wbsv import wbsv


def test1():
    args = {
        'url': ['https://example.com'],
        'only_target': False,
        'level': 1,
        'retry': 3
        }
    c = wbsv.crawler.Clawler(args)
test1()
