# Built-in Module
import re, random, sys, time
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from requests.exceptions import TooManyRedirects

# Third-parties' Module
from bs4 import BeautifulSoup
from savepagenow import capture_or_cache
from savepagenow.api import WaybackRuntimeError

# local Module
# from . import Version
# from . import Help

def is_url(url):
  """
  Judge whether str is url or not.
  """
  return re.compile(r'^(http|https)://').match(url)


def is_end(url):
  """
  Judge whether str is the fin command to quit interactive mode or not.
  """
  return re.compile(r'^(end|exit|exit\(\)|break|bye|:q|finish)$').match(url)

def is_page(url):
  """
  Judge whether str is webpage or not
  """
  exclude_suffixes = (".css", ".gif", ".jpeg", ".jpg", ".js", ".json", ".png", ".svg")
  url_parts = urlparse(url)
  return not url_parts.fragment and not url_parts.path.endswith(
             exclude_suffixes)

def is_valid_scheme(url):
  """
  Judge whether url is valid scheme or not
  """
  return urlparse(url).scheme in ["ftp", "gopher", "http", "https"]

def show_err():
  """
  Print error texts without stopping process when happening some error.
  """

  for err in list(sys.exc_info()):
    err_msg = "[!]%s"%str(err).strip("<>")
    print(err_msg, file=sys.stderr)

def find_uri(url):
    # remove not available data from list
    remove_useless = lambda l: {x for x in l if x != None and len(x) > 1}
    # extract elements containing of uri links in a page
    try:
      # print("->", url)
      html_source = urlopen(url)
    except HTTPError:
      return set()
    except URLError:
      return set()

    html_source_charset = html_source.headers.get_content_charset(failobj="utf-8")
    html_decoded = html_source.read().decode(
                     html_source_charset, 'ignore'
                   )
    uris_misc = BeautifulSoup(html_decoded, "html.parser").findAll(
                ["a"]
              )
    # extract uri link data
    uris_misc = sum([[i.get("href")] for i in uris_misc], [])
    # change "relative" uri into "absolute" one
    uris_misc = {urljoin(url, i) for i in uris_misc}
    # exclude mailto:// or javascript:// ...
    uris_misc = {i for i in uris_misc if is_valid_scheme(i)}
    return remove_useless(uris_misc)


# oldname: extract_uri
def extract_uri_recursive(url, rec):
  """
  Extract uri links from a page.
  """

  uri_dic = {url}
  search_queue = [[url]]
  if rec == 0:
    uri_dic=find_uri(url)
  for lev in range(rec):
    print("[+]LEVEL: %d" % lev)
    add_dic = set()
    remain_count = 1

    for url in search_queue[-1]:
      print("[+]REMAIN:%d/%d" % (remain_count, len(search_queue[-1])), end="\r")
      add_dic |= find_uri(url)
      remain_count += 1
    print("[+]LEVEL: %d FINISHED!" % lev)
    uri_dic |= add_dic
    search_queue.append([i for i in add_dic if is_page(i)])
  return uri_dic

def archive(uri_dic, pageurl, RETRY, ONLYPAGE):
  """
  Save URIs extracted from the target page.
  (by using Module savepagenow)
  """
  if ONLYPAGE:
    uri_dic = {i for i in uri_dic if is_page(i)}

  print("[+]Now: %s"%pageurl)
  print("[+]%d URI(s) found."%len(uri_dic))
  # try to throw each uri to API
  count, saves, fails = 0, 0, 0
  dic_size = len(uri_dic)

  for uri in uri_dic:
    count += 1

    id_ = str(count).zfill(len(str(len(uri_dic))))

    try:
      for j in range(1,RETRY+1):
        try:
          print("[%s/%d]: Wait..."%(id_, dic_size), end="\r")
          archived_uri, exist_flag = capture_or_cache(uri)  # use module of "savepagenow"
          print("[%s/%d]:"%(id_, dic_size),
                "<%s>"%"NOW" if exist_flag else "PAST", archived_uri)
          saves += 1
          break

        except WaybackRuntimeError:
          if j != RETRY:
            print("[%s/%d]: Retrying..."%(id_, dic_size), "COUNT:%d"%j, end="\r")
          else:
            print("[%s/%d]:"%(id_, dic_size), "<FAIL> %s"%uri)
            fails += 1
        finally:
            # wait retrying
            time.sleep(random.uniform(1,3))
    except KeyboardInterrupt:
      print("[!]Interrupted!", file=sys.stderr)
      print("[!]Halt.", file=sys.stderr)
      break

    except TooManyRedirects:
      print("[!]API says: TooManyRedirects!", file=sys.stderr)
      print("[!]Need a 1 min break...", file=sys.stderr)
      for t in range(60):
        print("%d/60s" % t,end="\r", file=sys.stderr)
        time.sleep(1)

  # after for-loop
  print("[+]FIN!: %s"%pageurl)
  print("[+]ALL:", count, "SAVE:", saves, "FAIL:", fails)
