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
    -l, --log-to-file <file>    Write STDOUT to a specified file.
    ''')

