import sys

import waybackpy


class SavepagenowFailureError(Exception):
    pass


class Archiver:
    def __init__(self, args):
        self.retry = args.retry
        self.UA = 'Mozilla/5.0 (Windows NT 5.1; rv:40.0) '\
                  'Gecko/20100101 Firefox/40.0'

    def archive(self, url):
        wp = waybackpy.Url(url, self.UA)
        for i in range(self.retry+1):
            if not self._try_savepagenow(wp):
                continue
            else:
                return (wp.archive_url, wp.cached_save)
        else:
            return False

    def _try_savepagenow(self, wp):
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
