from wbsv import crawler, main


def test_api_without_parser():
    args = {"urls": ["https://example.com"], "own": False, "only_target": False, "level": 1}
    c = crawler.Crawler.from_args(**args)
    urls = {"https://example.com", "https://www.iana.org/domains/example"}
    t = set().union(*c.run_crawl())
    if urls != t:
        raise AssertionError

def test1():
    args = main.parse_args(args_list=["https://example.com", "-l", "1"])
    c = crawler.Crawler.from_parser_args(args)
    urls = {"https://example.com", "https://www.iana.org/domains/example"}
    t = set().union(*c.run_crawl())
    if urls != t:
        raise AssertionError
