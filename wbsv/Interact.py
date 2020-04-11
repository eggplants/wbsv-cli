import sys
from . import Archive

def interactive(opt):
  """
  Interactive mode like shell.
  """
  #print(opt) #show flags for debugging...

  while True:
    print("[[Input a target url (ex: https://google.com)]]")
    try:
      url = input(">>> ")
    except(EOFError, KeyboardInterrupt):
      print("\n[+]End.")
      break

    # if the input is succeeded ...
    if Archive.is_url(url):
      if opt["only-target"]:
        Archive.archive([url], url, opt["retry"])
      else:
        Archive.archive(Archive.extract_uri_recursive(
            url,opt["level"]),
            url, opt["retry"])
        print("[+]To exit, use CTRL+C or type 'end'")

    elif Archive.is_end(url):
      print("[+]End.")
      break

    elif url == '':
      continue

    else:
      print("[!]This input is invalid.", file=sys.stderr)
      continue

