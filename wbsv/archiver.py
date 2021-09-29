import sys

import waybackpy


class SavepagenowFailureError(Exception):
    pass


class Archiver:
    def __init__(self, args):
        """Init."""
        self.retry = args.retry
        self.UA = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) " "Gecko/20100101 Firefox/40.0"

    def archive(self, url):
        """Archive link."""
        wp = waybackpy.Url(url, self.UA)
        for _ in range(self.retry + 1):
            if not self._try_savepagenow(wp):
                continue
            else:
                return (wp.archive_url, wp.cached_save)
        return False

    @staticmethod
    def _try_savepagenow(wp):
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
