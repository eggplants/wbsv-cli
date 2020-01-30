# Built-in Module
import re, random, sys, time
from urllib.parse import *
from urllib.request import urlopen

# Third-parties' Module
from bs4 import BeautifulSoup
from savepagenow import capture_or_cache
from savepagenow.api import WaybackRuntimeError

# local Module
from . import Version
from . import Help

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
  exclude_suffixes = (".png", ".jpg", ".jpeg", ".gif", ".js", ".css", ".svg")
  url_parts = urlparse(url)
  return not url_parts.fragment and not url_parts.path.endswith(
             exclude_suffixes)


def show_err():
  """
  Print error texts without stopping process when happening some error.
  """

  for err in list(sys.exc_info()):
    err_msg = "[!]%s"%str(err).strip("<>")
    print(err_msg, file=sys.stderr)

def find_uri(url):
    # remove not available data from list
    remove_useless=lambda l:{x for x in l if x != None and len(x) > 1}
    # extract elements containing of uri links in a page
    uris_misc=BeautifulSoup(urlopen(url), "html.parser").findAll(
                ["a", "img", "script", "link"]
              )
    # extract uri link data
    uris_misc=sum([[i.get("href"), i.get("src")] for i in uris_misc], [])
    # change "relative" uri into "absolute" one
    uris_misc={urljoin(url, i) for i in uris_misc}
    return remove_useless(uris_misc)


# oldname: extract_uri
def extract_uri_recursive(url,rec):
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

    for url in search_queue[-1]:
      add_dic |= find_uri(url)

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

  for uri in uri_dic:
    count += 1

    id_ = str(count).zfill(len(str(len(uri_dic))))

    try:
      for j in range(1,RETRY+1):
        try:
          print("[%s]: Wait...    "%id_, end="\r")
          archived_uri, exist_flag = capture_or_cache(uri)  # use module of "savepagenow"
          print("[%s]:"%id_,
                "<%s>"%"NOW" if exist_flag else "PAST", archived_uri)
          saves += 1
          break

        except WaybackRuntimeError:
          if j != RETRY:
            print("[%s]: Retrying..."%id_, "COUNT:%d"%j, end="\r")
          else:
            print("[%s]:"%id_, "<FAIL> %s"%uri)
            fails += 1
        finally:
            # wait retrying
            time.sleep(random.uniform(1,3))
    except KeyboardInterrupt:
      show_err()
      print("[!]Halt.", file=sys.stderr)
      break

    except:
      show_err()

  # after for-loop
  print("[+]FIN!: %s"%pageurl)
  print("[+]ALL:", count, "SAVE:", saves, "FAIL:", fails)
