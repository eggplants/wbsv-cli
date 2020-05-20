import sys
import re

class Interactive:
    def __init__(self, finder, archiver):
        """initialize."""
        self.finder = finder
        self.archiver = archiver

    def parse_opt(self, opt):
        self.only_target = opt["only-target"]

    @staticmethod
    def is_end(str):
        """Judge whether str is the fin cmd to quit interactive mode."""
        return re.compile(r'^(end|exit|exit\(\)|break|bye|:q|finish)$').match(str)

    @staticmethod
    def is_url(url):
        """Judge whether str is url or not."""
        return re.compile(r'\A(http|https)://').match(url)

    def judge_str(self, str):
        if self.is_end(str):
            print("[+]End.")
            exit(0)
        elif self.is_url(str):
            self.finder.find_and_archive(str, self.archiver)
            self.finder.print_result()
        else:
            print("[!]This input is invalid.", file=sys.stderr)

    def run(self):
        """Interactive mode like shell."""
        print("[+]To exit, use CTRL+C or type 'end'")

        while True:
            print("[[Input a target url (ex: https://google.com)]]")

            try:
                str = input(">>> ")
                self.judge_str(str)
            except(EOFError, KeyboardInterrupt):
                print("\n[+]End.")
                exit(0)
