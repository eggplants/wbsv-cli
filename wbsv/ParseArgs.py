import sys, re
from . import Archive

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
          "only-page":False,
          "errout":sys.stderr,
          "out":sys.stdout
        }
  args = sys.argv
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
  if re.compile(r'^.*-(-retry|r)[0-9]+[^.]*').match(arg_str):
    param["retry"] = int(re.search(r'^.*-(-retry|r)([0-9]+)', arg_str).group(2))
    if param["retry"] < 0:
      print("[!]Err: num of retry should be 0 or more.", file=sys.stderr)
      exit(1)
  elif re.compile(r'^.*-(-retry|r)').match(arg_str):
    print("[!]-r, --retry option needs int.", file=sys.stderr)
    exit(1)

  param["urls"] = list(filter(lambda x: Archive.is_url(x), args))
  return param

