from argparse import Namespace
from typing import Literal, Tuple, Union

import requests
import waybackpy  # type: ignore

from wbsv.utils import log_exception


class SavepagenowFailureError(Exception):
    pass


class Archiver:
    @staticmethod
    def from_parser_args(args: Namespace) -> "Archiver":
        return Archiver(args.retry)

    def __init__(self, retry: int):
        """Init."""
        self.retry: int = retry
        self.UA: str = (
            "Mozilla/5.0 (Windows NT 5.1; rv:40.0) " "Gecko/20100101 Firefox/40.0"
        )

    def archive(self, url: str) -> Union[Literal[False], Tuple[str, bool]]:
        """Archive link."""
        wp = waybackpy.WaybackMachineSaveAPI(url, self.UA, max_tries=self.retry)
        if self._try_savepagenow(wp):
            return wp.archive_url, wp.cached_save
        return False

    @staticmethod
    def _try_savepagenow(wp: waybackpy.WaybackMachineSaveAPI) -> bool:
        """Error handler for saving with savepagenow."""
        try:
            wp.save()
        except (
            waybackpy.exceptions.MaximumSaveRetriesExceeded,
            waybackpy.exceptions.WaybackError,
            requests.exceptions.TooManyRedirects,
            AttributeError,
        ) as e:
            log_exception(e)
            return False
        else:
            return True
