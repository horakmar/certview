#!/usr/bin/python3
# vim:fileencoding=utf-8:tabstop=4:shiftwidth=4

############################################ 
#  Certificate viewer
#
#  Author: Martin Horak
#  Version: 0.1
#  Date: 15. 3. 2019
#
############################################
import sys, subprocess, re

## Variables   ## ==========================
################# ==========================

clr = None

inf = {
    'serial': [False],
    'subject': [True],
    'ca': [False],
    'hash': [False],
    'dates': [False],
    'subcn': [False, r'CN = (.*?)(,|$)'],
    'cacn': [False, r'CN = (.*?)(,|$)'],
    'names': [False, r'Subject Alternative Name:'],
    'subid': [False, r'Subject Key Identifier:'],
    'caid': [False, r'Authority Key Identifier:'],
    'usage': [False, r'X509v3 Key Usage:', r'X509v3 Extended Key Usage:']
}

class colors:
    none   = '[0m'
    red    = '[01;31m'
    green  = '[01;32m'
    yellow = '[01;33m'
    blue   = '[01;34m'
    white  = '[01;37m'

    def __init__(self, use_colors):
        if not use_colors:
            self.none = ''
            self.red  = ''
            self.green = ''
            self.yellow = ''
            self.blue = ''
            self.white = ''

## Functions ## ============================
############### ============================
## Usage ## --------------------------------
def Usage():
    '''Usage help'''

    usage = """
Usage:
    {script_name} [Options] [certificate_file... ]

Well arranged view of certificate data

Options:
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

"""
    print(usage.format(script_name = sys.argv[0]))
    return
## Usage end ## ----------------------------

## Color print helper ## -------------------
def lprint(header, text):
    print(clr.yellow + header + clr.none, text)

## Certificate parser ## -------------------
def crtparse(infile):
    'Certificate data parser'
    f_incert = False;
    for line in infile:
        if f_incert:
            cert += line
            if '--END CERTIFICATE--' in line:
                crt1 = subprocess.run(['openssl', 'x509', '-nameopt', 'oneline', '-serial', '-subject', '-issuer', '-hash',  '-dates'], \
                       input=bytes(cert, 'ascii'), stdout=subprocess.PIPE)
                crt1lns = crt1.stdout.decode('ascii').splitlines()
                crt2 = subprocess.run(['openssl', 'x509', '-text', '-noout', '-certopt', \
                       'no_header,no_version,no_serial,no_signame,no_validity,no_issuer,no_pubkey,no_sigdump,no_aux,no_subject'], \
                       input=bytes(cert, 'ascii'), stdout=subprocess.PIPE)
                crt2lns = iter(crt2.stdout.decode('ascii').splitlines())

                print(clr.green + '----------------------------------------------------' + clr.none)
                if inf['subject'][0]:
                    lprint('Subject:', crt1lns[1].split('=', 1)[1].strip())
                if inf['serial'][0]:
                    lprint('Serial:', crt1lns[0].split('=', 1)[1])
                if inf['ca'][0]:
                    lprint('Issuer:', crt1lns[2].split('=', 1)[1].strip())
                if inf['hash'][0]:
                    lprint('Hash:', crt1lns[3])
                if inf['dates'][0]:
                    lprint('From:',crt1lns[4].split('=', 1)[1])
                    lprint('To:  ', crt1lns[5].split('=', 1)[1])
                if inf['subcn'][0]:
                    r = re.search(inf['subcn'][1], crt1lns[1].split('=', 1)[1]) 
                    if r:
                        lprint('Subject CN:', r.group(1))
                if inf['cacn'][0]:
                    r = re.search(inf['cacn'][1], crt1lns[2].split('=', 1)[1]) 
                    if r:
                        lprint('Issuer CN:', r.group(1))

                crtusg = [];
                crtextusg = [];
                for ln in crt2lns:
                    if inf['names'][0] and inf['names'][1] in ln:
                        names = next(crt2lns).strip().split(', ')
                        print(clr.yellow + 'Names: |' + clr.none)
                        print('  ' + '\n  '.join(names))
                    if inf['subid'][0] and inf['subid'][1] in ln:
                        lprint('Subject ID:', next(crt2lns).lstrip())
                    if inf['caid'][0] and inf['caid'][1] in ln:
                        a = next(crt2lns).lstrip()
                        if a.startswith('keyid:'): a = a[6:]
                        lprint('Issuer ID:', a)
                    if inf['usage'][0] and inf['usage'][1] in ln:
                        crtusg = next(crt2lns).strip().split(", ")
                    if inf['usage'][0] and inf['usage'][2] in ln:
                        crtextusg = next(crt2lns).strip().split(", ")
                if inf['usage'][0]:
                    print(clr.yellow + 'Usage: |' + clr.none)
                    print('  ' + '\n  '.join(crtusg + crtextusg))
                f_incert = False
        else:
            if '--BEGIN CERTIFICATE--' in line:
                cert = line
                f_incert = True
    print(clr.green + '----------------------------------------------------' + clr.none)
    return

## Main ## =================================
########## =================================
def main():
    '''Main program'''
    global clr

    use_colors = sys.stdout.isatty()
## Getparam ## -----------------------------
    argn = []
    args = sys.argv;
    havearg = filter(lambda x: x[0] == '-' or x[0] == '+', args)
    if not next(havearg, None):
        args.append('-SNAdiInu')
    i = 1
    try:
        while(i < len(args)):
            if(args[i][0] == '-'):
                for j in args[i][1:]:
                    if j == 'h':
                        Usage()
                        return
                    elif j == 'S':
                        inf['subject'][0] = True
                    elif j == 's':
                        inf['subcn'][0] = True
                    elif j == 'N':
                        inf['serial'][0] = True
                    elif j == 'A':
                        inf['ca'][0] = True
                    elif j == 'a':
                        inf['cacn'][0] = True
                    elif j == 'd':
                        inf['dates'][0] = True
                    elif j == 'H':
                        inf['hash'][0] = True
                    elif j == 'n':
                        inf['names'][0] = True
                    elif j == 'i':
                        inf['subid'][0] = True
                    elif j == 'I':
                        inf['caid'][0] = True
                    elif j == 'u':
                        inf['usage'][0] = True
            elif(args[i][0] == '+'):
                for j in args[i][1:]:
                    if j == 'S':
                        inf['subject'][0] = False
                    if j == 'c':
                        use_colors = False
            else:
                argn.append(args[i])
            i += 1
    except IndexError:
        print("Parameter reading error. Use -h for help.")
        Usage()
        return
## Getparam end ## -------------------------
    
    clr = colors(use_colors)

    if len(argn) > 0:
        for s in argn:
            with open(s, 'r') as infile:
                crtparse(infile)
    else:
        crtparse(sys.stdin)

## Main end =================================
########### =================================

## Spusteni main ============================
########### =================================
if __name__ == '__main__': 
    main()
