# Simple Certificate Viewer

(Hopefully) well arranged view of certificate data.

From help:
```
Usage:
    certview [options] [certificate_file... ]

options:
  -h ... help - this help
  +c ... do not use colors

  Print info:
    -S ... Subject [printed by default]
    -s ... Subject CN
    -A ... Issuer (CA)
    -a ... Issuer CN
    -d ... Validity dates
    -n ... Alternative names
    -i ... Subject key identifier
    -I ... Issuer key identifier
    -u ... Key usage
    -N ... Serial number
    -H ... Key hash

  Do not print info:
    +S ... Subject

When no option is specified, default is [-SNAdiInu].
When no certificate_file is specified, stdin is read.
When stdout is not a tty, colors are disabled.

Prerequisites:
    Python3
    Openssl installed in $PATH (program doesn't check).
```
