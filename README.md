# `wbsv`

[![PyPI version](https://badge.fury.io/py/wbsv.svg)](https://badge.fury.io/py/wbsv) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3721b14865f34217ab912c9afd364b9b)](https://www.codacy.com/manual/eggplants/wbsv-cli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eggplants/wbsv-cli&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/ce84fc17ef2b182eda26/maintainability)](https://codeclimate.com/github/eggplants/wbsv-cli/maintainability) [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Downloads](https://pepy.tech/badge/wbsv)](https://pepy.tech/project/wbsv) [![Downloads](https://pepy.tech/badge/wbsv/month)](https://pepy.tech/project/wbsv/month) [![Downloads](https://pepy.tech/badge/wbsv/week)](https://pepy.tech/project/wbsv/week)

## `wbsv`("Wabisavi", "わびさび", stands for "WayBack machine SavepageNow") is…

CLI tool for saving webpage on Wayback Machine forever.
Enables you to **save all URIs** in a webpage forever on [Wayback Machine](https://archive.org/web/).

## Try now

You can try this tool on Google Cloud Shell. (First, `sudo python3 -m pip install -e .`)

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/eggplants/wbsv-cli&tutorial=README.md)

## DEMO

![demo.gif](https://raw.githubusercontent.com/eggplants/wbsv-cli/master/demo.gif)

## Install

```bash
$ pip install wbsv # Python3.0+
```

## Run & Examples

### Help

```bash
$ wbsv -h
wbsv 0.1.6
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
    -t, --only-target           Save just target webpage(s).
    -L, --level <depth>          Set maximum recursion depth.
```

### Interactive mode

```bash
$ wbsv
[[Input a target url (ex: https://google.com)]]
>>> https://www.u.tsukuba.ac.jp
[+]Now: https://www.u.tsukuba.ac.jp
[+]60 URI(s) found.
[01/60]: <NOW> https://web.archive.org/web/20200412020015/https://www.u.tsukuba.ac.jp/password/
[02/60]: <FAIL> https://www.u.tsukuba.ac.jp/info_lit/tebiki.html
[03/60]: <NOW> https://web.archive.org/web/20200412020026/https://www.u.tsukuba.ac.jp/account/
...
[58/60]: <NOW> https://web.archive.org/web/20200412022608/https://www.u.tsukuba.ac.jp/phishing/
[59/60]: <FAIL> https://www.u.tsukuba.ac.jp/wordpress/wp-content/uploads/note_usingcomputerrooms.png
[60/60]: <NOW> https://web.archive.org/web/20200412022640/https://www.u.tsukuba.ac.jp/
[+]FIN!: https://www.u.tsukuba.ac.jp
[+]ALL: 60 SAVE: 57 FAIL: 3
[+]To exit, use CTRL+C or type 'end'
[[Input a target url (ex: https://google.com)]]
>>> exit
[+]End.
$
```

### From stdin

```bash
$ wbsv https://tsumanne.net https://tsumanne.net/ct
[+]Now: https://tsumanne.net
[+]4 URI(s) found.
[1/4]: <NOW> https://web.archive.org/web/20200412022931/https://tsumanne.net/si/
[2/4]: <NOW> https://web.archive.org/web/20200412022935/https://tsumanne.net/
[3/4]: <NOW> https://web.archive.org/web/20200412022938/https://tsumanne.net/my/
[4/4]: <NOW> https://web.archive.org/web/20200412022949/https://tsumanne.net/ct/
[+]FIN!: https://tsumanne.net
[+]ALL: 4 SAVE: 4 FAIL: 0
[+]Now: https://tsumanne.net/ct
[+]3 URI(s) found.
[1/3]: <NOW> https://web.archive.org/web/20200412022958/https://tsumanne.net/
[2/3]: <NOW> https://web.archive.org/web/20200412023000/https://tsumanne.net/oa_login.php
[3/3]: <NOW> https://web.archive.org/web/20200412023012/https://tsumanne.net/ct/?cat=&of=25
[+]FIN!: https://tsumanne.net/ct
[+]ALL: 3 SAVE: 3 FAIL: 0
$
```

### Search links recurcively
```bash
$ wbsv -L2 https://programming-place.net/ppp/contents/c/index.html
```

### Increase limit of retry
```bash
$ wbsv https://tsumanne.net --retry 10
```

## VERSION

`wbsv 0.1.6`

## LISENCE
MIT

## Author
eggplants (haruna)
