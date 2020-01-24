from . import Archive
from . import Version
from . import Help
from . import ParseArgs
from . import Interact

def main():
  """
  main
  """

  opt = ParseArgs.parse_args()  # parse optional arguments and get `opt`(type:dict)

  if opt["version"]:
    Version.version()

  elif opt["help"]:
    Version.version()
    Help.help()

  elif len(opt["urls"]) == 0:
    Interact.interactive(opt)

  elif opt["only-page"]:
    for x in opt["urls"]:
      Archive.archive([x], x, opt["retry"])
  else:
    for x in opt["urls"]:
      Archive.archive(Archive.extract_uri(x), x, opt["retry"])

  # if no errors occurred ...
  exit(0)

if __name__ == "__main__":
  main()

