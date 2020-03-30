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
          "only-target":False,
          "errout":sys.stderr,
          "out":sys.stdout,
          "level":0,
          "only-page":False,
        }
  args = sys.argv
  arg_str = "".join(args)

  # -h, --help
  if "-h" in args or "--help" in args:
    param["help"] = True

  # -v, --version
  if "-v" in args or "--version" in args:
    param["version"] = True

  # -t, --only-target
  if "-t" in args or "--only-target" in args:
    param["only-target"] = True

  # -r, --retry
  if re.compile(r'^.*-(-retry|r)[0-9]+[^.]*').match(arg_str):
    param["retry"] = int(re.search(r'^.*-(-retry|r)([0-9]+)', arg_str).group(2))
    if param["retry"] < 0:
      print("[!]Err: num of retry should be 0 or more.", file=sys.stderr)
      exit(1)
  elif re.compile(r'^.*-(-retry|r)').match(arg_str):
    print("[!]-r, --retry option needs int.", file=sys.stderr)
    exit(1)

  # -L, --level
  if re.compile(r'^.*-(-level|L)[0-9]+[^.]*').match(arg_str):
    param["level"] = int(re.search(r'^.*-(-level|L)([0-9]+)', arg_str).group(2))
    if param["level"] < 0:
      print("[!]Err: num of retry should be 0 or more.", file=sys.stderr)
      exit(1)
  elif re.compile(r'^.*-(-level|L)').match(arg_str):
    print("[!]-L, --level option needs int.", file=sys.stderr)
    exit(1)

  # -p, --only-page
  if "-p" in args or "--only-page" in args:
    param["only-page"] = True


  param["urls"] = [i for i in args if Archive.is_url(i)]
  return param
