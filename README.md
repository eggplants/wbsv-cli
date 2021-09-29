# `wbsv`

[![PyPI version](https://badge.fury.io/py/wbsv.svg)](https://badge.fury.io/py/wbsv) [![Maintainability](https://api.codeclimate.com/v1/badges/ce84fc17ef2b182eda26/maintainability)](https://codeclimate.com/github/eggplants/wbsv-cli/maintainability)

## `wbsv`(stands for "WayBack machine SavepageNow") is…

CLI tool for saving webpage on Wayback Machine forever.
Enables you to **save all URIs** in a webpage forever on [Wayback Machine](https://archive.org/web/).

## Install

```bash
pip install wbsv
```

## DEMO

![demo.gif](https://raw.githubusercontent.com/wiki/eggplants/wbsv-cli/demo.gif)

## Run & Examples

### Help

```bash
$ wbsv -h
usage: wbsv [-h] [-r times] [-t] [-l level] [-V] [url [url ...]]

CLI tool for save webpage on Wayback Machine forever.
Save webpage and one 's all URI(s) on Wayback Machine.

positional arguments:
  url                   Saving pages in order.

optional arguments:
  -h, --help            show this help message and exit
  -r times, --retry times
                        Set a retry limit on failed save.(>=0
  -t, --only_target     Save just target webpage(s).
  -l level, --level level
                        Set maximum recursion depth. (>0)
  -V, --version         show program's version number and exit

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
[+]Target: ['https://www.u.tsukuba.ac.jp']
[+]61 URI(s) found.
[01/60]: <NOW> https://web.archive.org/web/20200412020015/https://www.u.tsukuba.ac.jp/password/
[02/60]: <FAIL> https://www.u.tsukuba.ac.jp/info_lit/tebiki.html
[03/60]: <NOW> https://web.archive.org/web/20200412020026/https://www.u.tsukuba.ac.jp/account/
...
[58/60]: <NOW> https://web.archive.org/web/20200412022608/https://www.u.tsukuba.ac.jp/phishing/
[59/60]: <FAIL> https://www.u.tsukuba.ac.jp/wordpress/wp-content/uploads/note_usingcomputerrooms.png
[60/60]: <NOW> https://web.archive.org/web/20200412022640/https://www.u.tsukuba.ac.jp/
[+]FIN!: ['https://www.u.tsukuba.ac.jp']
[+]ALL: 60, SAVE: 57, PAST: 0, FAIL: 3
>>>
```

### From stdin

```bash
$ wbsv https://tsumanne.net
[+]Target: ['https://tsumanne.net']
[+]4 URI(s) found.
[1/4]: <NOW> https://web.archive.org/web/20200412022931/https://tsumanne.net/si/
[2/4]: <NOW> https://web.archive.org/web/20200412022935/https://tsumanne.net/
[3/4]: <NOW> https://web.archive.org/web/20200412022938/https://tsumanne.net/my/
[4/4]: <NOW> https://web.archive.org/web/20200412022949/https://tsumanne.net/ct/
[+]FIN!: ['https://tsumanne.net']
[+]ALL: 4, SAVE: 4, PAST: 0, FAIL: 0
$
```

### Search links recurcively

```bash
wbsv https://programming-place.net/ppp/contents/c/index.html -l 2
```

### Increase limit of retry

```bash
wbsv https://tsumanne.net -r 10
```

## LISENCE

MIT

## Author

eggplants (haruna)
