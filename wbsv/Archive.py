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

  print("wbsv 0.0.2")

def help():
  """
  show this command's usage.
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
  -r, --retry <times>         Give the limit of retry when saving fails.\
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

def err_show():
  """
  Print error texts without stopping process when happening some error.
  """

  [print("[!]%s"%str(i).strip("<>"),file=stderr) for i in list(exc_info())]

def archive(url,RETRY=3):
  """
  Save URIs extracted from the target page. (by using Module savepagenow)
  """

  print("[+]Now: %s"%url)
  # extract uris
  uri_list=set(
             list(
               filter(
                 lambda x:x!=None and len(x)>1,
                 [
                   urljoin(url,i) for i in sum(
                   [[i.get("href"),i.get("src")] for i in BeautifulSoup(urlopen(url),"html.parser").findAll(["a","img","script","link"])],[]
                   )
                 ]
               )
             )
           )
  # input url appends to extracted uris' list
  uri_list.add(url)
  # try to throw each uri to API
  count,saves,fails=0,0,0
  for uri in uri_list:
    if count==0:
      print("%d URI(s) found."%len(uri_list))
    count+=1
    id=str(count).zfill(len(str(len(uri_list))))
    try:
      for _ in range(RETRY):
        try:
          print("[%s]: Wait...    "%id,end="\r")
          archived_uri,exist_flag=capture_or_cache(uri)
          print("[%s]:"%id,
                "<%s>"%"NOW" if exist_flag else "PAST",archived_uri)
          saves+=1
          break
        except WaybackRuntimeError:
          if _!=RETRY-1:
            print("[%s]: Retrying..."%id,"COUNT:%d"%(_+1),end="\r")
            sleep(uniform(_+1,_+2))
          else:
            print("[%s]:"%id,"<FAIL> %s"%uri)
            fails+=1
        sleep(uniform(1,3))
    except KeyboardInterrupt:
      err_show()
      print("[!]Halt.",file=stderr)
      break
    except:
      err_show()
  print("[+]FIN!: %s"%url)
  print("[+]ALL:",count,"SAVE:",saves,"FAIL:",fails)

def interactive(retry=3):
  """
  Interactive mode like shell.
  """

  while 1:
    print("[[Input a target url (ex: https://google.com)]]")
    try:
      url=input(">>> ")
    except(EOFError,KeyboardInterrupt):
      print("\n[+]End.")
      break
    if is_url(url):
      try:
        archive(url,retry)
        print("[+]To exit, use CTRL+C or type 'end'")
      except:
        err_show()
    elif is_end(url):
      print("[+]End.")
      break
    elif url=='':
      continue
    else:
      print("[!]This input is invalid.",file=stderr)
      continue

def opt_parse():
  """
  Parse arguments.
  """

  # flags
  param={"help":False, "version":False, "retry":3, "urls":[]}
  args=argv
  arg_str="".join(args)
  if "-h" in args or "--help" in args:
    param["help"]=True
  if "-v" in args or "--version" in args:
    param["version"]=True
  if compile(r'^.*-(-retry|r)[0-9]+[^.]*').match(arg_str):
    param["retry"]=int(search(r'^.*-(-retry|r)([0-9]+)',arg_str).group(2))
    if param["retry"]<0:
      print("[!]Err: num of retry should be 0 or more.",file=stderr)
      exit(1)
  elif compile(r'^.*-(-retry|r)').match(arg_str):
    print("[!]-r, --retry option needs int.",file=stderr)
    exit(1)
  param["urls"]=list(filter(lambda λ: is_url(λ), args))
  return param

def main():
  """
  main
  """

  opt=opt_parse()
  if opt["version"]:
    version()
  elif opt["help"]:
    version()
    help()
  elif len(opt["urls"])==0:
    interactive(opt["retry"])
  else:
    for i in opt["urls"]:
      archive(i,opt["retry"])
  exit(0)
if __name__ == "__main__":
  main()
