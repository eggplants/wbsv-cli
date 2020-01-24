import sys
from . import Archive

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
    if Archive.is_url(url):
      try:
        if opt["only-page"]:
          Archive.archive([url], url, retry)
        else:
          Archive.archive(Archive.extract_uri(url), url, retry)
        print("[+]To exit, use CTRL+C or type 'end'")
      except:
        Archive.show_err()

    elif Archive.is_end(url):
      print("[+]End.")
      break

    elif url == '':
      continue

    else:
      print("[!]This input is invalid.", file=sys.stderr)
      continue

