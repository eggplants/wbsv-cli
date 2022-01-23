import sys
from argparse import Namespace
from typing import Union, Tuple, Literal

import waybackpy


class SavepagenowFailureError(Exception):
    pass


class Archiver:

    @staticmethod
    def from_parser_args(args: Namespace) -> 'Archiver':
        return Archiver(args.retry)

    def __init__(self, retry: int):
        """Init."""
        self.retry: int = retry
        self.UA: str = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) " "Gecko/20100101 Firefox/40.0"

    def archive(self, url: str) -> Union[Literal[False], Tuple[str, bool]]:
        """Archive link."""
        wp = waybackpy.Url(url, self.UA)
        for _ in range(self.retry + 1):
            if not self._try_savepagenow(wp):
                continue
            else:
                return wp.archive_url, wp.cached_save
        return False

    @staticmethod
    def _try_savepagenow(wp: waybackpy.Url) -> bool:
        """Error handler for saving with savepagenow."""
        try:
            wp.save()
        except waybackpy.exceptions.RedirectSaveError as e:
            print(e, file=sys.stderr)
            return False
        except waybackpy.exceptions.WaybackError as e:
            print(e, file=sys.stderr)
            return False
        except AttributeError as e:
            print(e, file=sys.stderr)
            return False
        else:
            return True
