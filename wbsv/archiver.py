import re
import sys
import time

from random import random

from requests.exceptions import TooManyRedirects

from savepagenow import capture_or_cache
from savepagenow.api import WaybackRuntimeError


class AbstractArchiver():
    def __init__(self):
        self.save_count = 0
        self.fail_count = 0
    
    def parse_opt(self, opt):
        self.retry = opt["retry"]

    def try_archive(self, url):
        pass

    def archive(self, url):
        result = self.retry_ntimes( self.try_archive, [url] )
        self.add_result(result)
      
    def is_url(self, url):
        """Judge whether str is url or not."""
        return re.compile(r'\A(http|https)://').match(url)

    def wait_min(self):
        for t in range(60):
            print("%d/60s" % t, end="\r", file=sys.stderr)
            time.sleep(1)

    def retry_ntimes(self, func, args=()):
        for i in range(self.retry):
            if func(*args):
                return True
            else:
                print("failed: "+str(i))

        return False
    
    def add_result(self, result):
        if result:
            self.save_count += 1
        else:
            self.fail_count += 1
    
    def print_result(self):
        #print("[+]FIN!: %s" % pageurl)
        print("SAVE:", self.save_count, "FAIL:", self.fail_count)
    
class Archiver(AbstractArchiver):
    def try_archive(self, id_, dic_size, uri):
        pass

    def archive(self, url):
        pass

class RandomArchiver(AbstractArchiver):
    #def __init__(self):
        #super().__init__()

    def try_archive(self, url):
        if random() > 0.5 :
            print("Archived: "+url)
            return True
        else:
            print("Archive Failed: "+url)
            return False
        