# `wbsv`

[![PyPI version](https://badge.fury.io/py/wbsv.svg)](https://badge.fury.io/py/wbsv) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/4914becc1f8f409dbc9f4a2020ab2e17)](https://www.codacy.com/manual/eggplants/wbsv-cli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eggplants/wbsv-cli&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/ce84fc17ef2b182eda26/maintainability)](https://codeclimate.com/github/eggplants/wbsv-cli/maintainability) [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Downloads](https://pepy.tech/badge/wbsv)](https://pepy.tech/project/wbsv) [![Downloads](https://pepy.tech/badge/wbsv/month)](https://pepy.tech/project/wbsv/month) [![Downloads](https://pepy.tech/badge/wbsv/week)](https://pepy.tech/project/wbsv/week)

## `wbsv`(stands for "WayBack machine SavepageNow") is…

CLI tool for saving webpage on Wayback Machine forever.
Enables you to **save all URIs** in a webpage forever on [Wayback Machine](https://archive.org/web/).

## Try now

You can try this tool on Google Cloud Shell. (First, `sudo python3 -m pip install -e .`)

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/eggplants/wbsv-cli&tutorial=README.md)

## DEMO

![demo.gif](https://raw.githubusercontent.com/eggplants/wbsv-cli/master/demo.gif)

## Install

```bash
$ python -m pip install wbsv # Python3.0+
```

## Run & Examples

### Help

```bash
$ wbsv -v
wbsv 0.2.0
$ wbsv -h
usage: wbsv [-h] [-v] [-r cnt] [-t] [-L lv] [url [url ...]]

CLI tool for save webpage on Wayback Machine forever.
Save webpage and one's all URI(s) on Wayback Machine.

positional arguments:
  url                  Saving pages in order.

optional arguments:
  -h, --help           show this help message and exit
  -v, --version        Show version and exit
  -r cnt, --retry cnt  Set a retry limit on failed save.
  -t, --only_target    Save just target webpage(s).
  -L lv, --level lv    Set maximum recursion depth.

additional information:
    If you don't give the URL,
    interactive mode will be launched.
    (To quit interactive mode,
     type "end", "exit", "exit()",
     "break", "bye", ":q" or "finish".)

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
$ wbsv https://programming-place.net/ppp/contents/c/index.html -L2
```

### Increase limit of retry

```bash
$ wbsv https://tsumanne.net --retry 10
```

## VERSION

`wbsv 0.2.0`

## LISENCE

MIT

## Author

eggplants (haruna)
