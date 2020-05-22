import time

from random import random, randint

from savepagenow import capture_or_cache
from savepagenow.api import WaybackRuntimeError


class AbstractArchiver():
    def __init__(self):
        """initialize."""
        self.save_count = 0
        self.fail_count = 0

    def parse_opt(self, opt):
        self.retry = opt["retry"]

    def try_archive(self, url):
        pass

    def archive(self, url, url_dic):
        print("[+]SAVING: " + url)
        result = self.retry_ntimes(self.try_archive, url, url_dic)
        self.add_result(result)

    def retry_ntimes(self, func, a1, a2):
        for i in range(self.retry):
            if func(a1, a2):
                return True
            else:
                print("fail: "+str(i+1))
                time.sleep(randint(2, 10))

        return False

    def add_result(self, result):
        if result:
            self.save_count += 1
        else:
            self.fail_count += 1

    def print_result(self, url):
        """Print result."""
        print("[+]FIN!: %s" % url)
        print("[+]SAVE:", self.save_count, "FAIL:", self.fail_count)


class Archiver(AbstractArchiver):
    def try_archive(self, url, url_dic):
        try:
            ind, size = list(url_dic).index(url) + 1, len(url_dic)
            print("[%d/%d]: Wait...    " % (ind, size), end="\r")
            archive_uri, exist_f = capture_or_cache(url)
            print("[%d/%d]:" % (ind, size), end=" ")
            print("<%s>" % "NOW" if exist_f else "PAST", archive_uri)
            return True

        except WaybackRuntimeError:
            return False


class RandomArchiver(AbstractArchiver):
    def try_archive(self, url, url_dic):
        if random() > 0.5:
            return True
        else:
            return False
