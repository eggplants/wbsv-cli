# Built-in Module
from random import uniform
from re import compile
from re import search
from sys import exc_info
from sys import argv
from sys import stderr
from time import sleep
from urllib.parse import urljoin
from urllib.request import urlopen
# Third-parties' Module
from bs4 import BeautifulSoup
from savepagenow import capture_or_cache
from savepagenow.api import WaybackRuntimeError


def version():
  """
  show version info.
  """

  print("wbsv 0.0.5")


def help():
  """
  show usage.
  """

  print('''\
    CLI tool for save webpage on Wayback Machine forever.
    Save webpage and one's all URI(s) on Wayback Machine.

    Usage:
    wbsv [options] <url1> <url2> ... <urln>

    Args:
    <urls>                      Saving pages in order.
    no arg                      Launch Interactive mode.
                                (To quit interactive mode,
                                type "end", "exit", "exit()",
                                "break", "bye", ":q" or "finish".)

    Options:
    -h, --help                  Show help and exit.
    -v, --version               Show version and exit.
    -r, --retry <times>         Give the limit of retry when saving fails.
        --only-page             Save just target webpage(s).
    ''')


def is_url(url):
  """
  Judge whether str is url or not.
  """
  return compile(r'^(http|https)://').match(url)


def is_end(url):
  """
  Judge whether str is the fin command to quit interactive mode or not.
  """
  return compile(r'^(end|exit|exit\(\)|break|bye|:q|finish)$').match(url)


def show_err():
  """
  Print error texts without stopping process when happening some error.
  """

  for err in list(exc_info()):
    err_msg = "[!]%s"%str(err).strip("<>")
    print(err_msg, file=stderr)

def extract_uri(url):
  """
  Extract uri links from a page source.
  """

  # extract elements containing of uri links in a page
  uris_misc=BeautifulSoup(urlopen(url), "html.parser").findAll(["a", "img", "script", "link"])
  # extract uri link data
  uris_misc=sum([[i.get("href"), i.get("src")] for i in uris_misc], [])
  # change "relative" uri into "absolute" one
  uris_misc=[urljoin(url, i) for i in uris_misc]
  # remove not available data from list
  uri_list=set(list(filter(lambda x: x != None and len(x) > 1, uris_misc)))

  return uri_list

def archive(uri_list, pageurl, RETRY=3):
  """
  Save URIs extracted from the target page. (by using Module savepagenow)
  """
  print("[+]Now: %s"%pageurl)
  print("[+]%d URI(s) found."%len(uri_list))
  # try to throw each uri to API
  count, saves, fails = 0, 0, 0

  for uri in uri_list:
    count += 1

    id_ = str(count).zfill(len(str(len(uri_list))))

    try:
      for j in range(RETRY):
        try:
          print("[%s]: Wait...    "%id_, end="\r")
          archived_uri, exist_flag = capture_or_cache(uri)  # use module of "savepagenow"
          print("[%s]:"%id_,
                "<%s>"%"NOW" if exist_flag else "PAST", archived_uri)
          saves += 1
          break

        except WaybackRuntimeError:
          if j != RETRY-1:
            print("[%s]: Retrying..."%id_, "COUNT:%d"%(j+1), end="\r")
          else:
            print("[%s]:"%id_, "<FAIL> %s"%uri)
            fails += 1
        # wait retrying
        sleep(uniform(1,3))

    except KeyboardInterrupt:
      show_err()
      print("[!]Halt.", file=stderr)
      break

    except:
      show_err()

  # after for-loop
  print("[+]FIN!: %s"%pageurl)
  print("[+]ALL:", count, "SAVE:", saves, "FAIL:", fails)


def interactive(opt):
  """
  Interactive mode like shell.
  """

  retry = opt["retry"]

  while True:
    print("[[Input a target url (ex: https://google.com)]]")
    try:
      url = input(">>> ")
    except(EOFError, KeyboardInterrupt):
      print("\n[+]End.")
      break

    # if the input is succeeded ...
    if is_url(url):
      try:
        if opt["only-page"]:
          archive([url], url, retry)
        else:
          archive(extract_uri(url), url, retry)
        print("[+]To exit, use CTRL+C or type 'end'")
      except:
        show_err()

    elif is_end(url):
      print("[+]End.")
      break

    elif url == '':
      continue

    else:
      print("[!]This input is invalid.", file=stderr)
      continue


def parse_args():
  """
  Parse arguments.
  """

  # flags
  param={
          "help":False,
          "version":False,
          "retry":3,
          "urls":[],
          "only-page":False
        }
  args = argv
  arg_str = "".join(args)

  # -h, --help
  if "-h" in args or "--help" in args:
    param["help"] = True

  # -v, --version
  if "-v" in args or "--version" in args:
    param["version"] = True

  # --only-page
  if "--only-page" in args:
    param["only-page"] = True

  # -r, --retry
  if compile(r'^.*-(-retry|r)[0-9]+[^.]*').match(arg_str):
    param["retry"] = int(search(r'^.*-(-retry|r)([0-9]+)', arg_str).group(2))
    if param["retry"] < 0:
      print("[!]Err: num of retry should be 0 or more.", file=stderr)
      exit(1)
  elif compile(r'^.*-(-retry|r)').match(arg_str):
    print("[!]-r, --retry option needs int.", file=stderr)
    exit(1)

  param["urls"] = list(filter(lambda x: is_url(x), args))
  return param


def main():
  """
  main
  """

  opt = parse_args()  # parse optional arguments and get `opt`(type:dict)

  if opt["version"]:
    version()

  elif opt["help"]:
    version()
    help()

  elif len(opt["urls"]) == 0:
    interactive(opt)

  elif opt["only-page"]:
    for x in opt["urls"]:
      archive([x], x, opt["retry"])
  else:
    for x in opt["urls"]:
      archive(extract_uri(x), x, opt["retry"])

  # if no errors occurred ...
  exit(0)

if __name__ == "__main__":
  main()
