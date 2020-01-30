# `wbsv`

[![PyPI version](https://badge.fury.io/py/wbsv.svg)](https://badge.fury.io/py/wbsv) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3721b14865f34217ab912c9afd364b9b)](https://www.codacy.com/manual/eggplants/wbsv-cli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eggplants/wbsv-cli&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/ce84fc17ef2b182eda26/maintainability)](https://codeclimate.com/github/eggplants/wbsv-cli/maintainability) [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Downloads](https://pepy.tech/badge/wbsv)](https://pepy.tech/project/wbsv) [![Downloads](https://pepy.tech/badge/wbsv/month)](https://pepy.tech/project/wbsv/month) [![Downloads](https://pepy.tech/badge/wbsv/week)](https://pepy.tech/project/wbsv/week)

- `wbsv`("Wabisavi", "わびさび", stands for "WayBack machine SavepageNow") is...

  - CLI tool for saving webpage on Wayback Machine forever.
  - Enables you to **save all URIs** in a webpage forever on [Wayback Machine](https://archive.org/web/).

# DEMO

![demo.gif](https://raw.githubusercontent.com/eggplants/wbsv-cli/master/demo.gif)

# Install

```bash
$ pip install wbsv # Python3.0+
```

# Run & Examples

## Help

```bash
$ wbsv -h
wbsv 0.0.7
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
    -r, --retry <times>         Set a retry limit on failed save.
        --only-target           Save just target webpage(s).
    -l, --log-to-file <file>    Write STDOUT to a specified file.
    -L, --recursive <level>     Set maximum recursion depth.
        --only-page             Get only URIs of type web page.
```

## Interactive mode

```bash
$ wbsv
[[Input a target url (ex: https://google.com)]]
>>> https://tsukuba.ac.jp
[!]Now: https://tsukuba.ac.jp
[!]class 'urllib.error.URLError'
[!]urlopen error [Errno -2] Name or service not known
[!]traceback object at 0x7eff0d207188
[[Input a target url (ex: https://google.com)]]
>>> https://www.u.tsukuba.ac.jp
[+]Now: https://www.u.tsukuba.ac.jp
87 URI(s) found.
[01]: <NOW> https://web.archive.org/web/20200123135244/https://www.u.tsukuba.ac.jp/20180622terminals/
[02]: <NOW> https://web.archive.org/web/20200123135247/https://www.u.tsukuba.ac.jp/
[03]: <NOW> https://web.archive.org/web/20200123135250/https://www.u.tsukuba.ac.jp/anti-virus/
...
[85]: <NOW> https://web.archive.org/web/20200123140917/https://www.u.tsukuba.ac.jp/snapshot/
[86]: <FAIL> https://www.u.tsukuba.ac.jp/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww.u.tsukuba.ac.jp%2F&format=xml
[87]: <FAIL> https://www.u.tsukuba.ac.jp/info_lit/tebiki.html
[+]FIN!: https://www.u.tsukuba.ac.jp
[+]ALL: 87 SAVE: 61 FAIL: 21
[+]To exit, use CTRL+C or type 'end'
[[Input a target url (ex: https://google.com)]]
>>> exit
$
```

## From stdin

```bash
$ wbsv https://tsumanne.net https://tsumanne.net/ct
[+]Now: https://tsumanne.net
9 URI(s) found.
[1]: <NOW> https://web.archive.org/web/20200123194439/https://tsumanne.net
...
[9]: <FAIL> https://tsumanne.net/src/iphone.png
[+]FIN!: https://tsumanne.net
[+]ALL: 9 SAVE: 5 FAIL: 4
[+]Now: https://tsumanne.net/ct
7 URI(s) found.
[1]: <NOW> https://web.archive.org/web/20200123194602/https://tsumanne.net/ct/?cat=&of=25
...
[7]: <FAIL> https://tsumanne.net/src/site.js
[+]FIN!: https://tsumanne.net/ct
[+]ALL: 7 SAVE: 5 FAIL: 2
$
```

## Increase limit of retry
```bash
$ wbsv https://tsumanne.net --retry 10
```

# VERSION

`wbsv 0.0.7`

# LISENCE
MIT

# Author
eggplants (haruna)
