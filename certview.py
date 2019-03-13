#!/usr/bin/python3
# vim:fileencoding=utf-8:tabstop=4:shiftwidth=4

############################################ 
#  Certificate viewer
#
#  Author: Martin Horak
#  Version: 0.1
#  Date: 13. 3. 2019
#
############################################
import sys, subprocess, re

## Environment ## ==========================
################# ==========================


## Functions ## ============================
############### ============================
## Usage ## --------------------------------
def Usage():
    '''Usage help'''

    usage = """
Usage:
    {script_name} [-h] [-vq]

View certificate important data

Parametry:
    -h  ... help - this help
    -v  ... verbose
    -q  ... quiet

"""
    print(usage.format(script_name = sys.argv[0]))
    return

## Usage end ## ----------------------------

## Main ## =================================
########## =================================
def main():
    '''Main program'''

## Variables ## ============================
############### ============================
    verbose = 1
    log = ''
    subject = False;

## Getparam ## -----------------------------
    argn = []
    args = sys.argv;
    i = 1
    try:
        while(i < len(args)):
            if(args[i][0] == '-'):
                for j in args[i][1:]:
                    if j == 'h':
                        Usage()
                        return
                    elif j == 't':
                        test = True
                    elif j == 'v':
                        verbose += 1
                    elif j == 'q':
                        verbose -= 1
                    elif j == 's':
                        subject = True
                    elif j == 'l':
                        i += 1
                        log = args[i]
            else:
                argn.append(args[i])
            i += 1
    except IndexError:
        print("Chyba cteni parametru.")
        Usage()
        return
## Getparam end ## -------------------------

    for s in argn:
        with open(s, 'r') as infile:
            f_incert = False;
            for line in infile:
                if f_incert:
                    cert += line
                    if '--END CERTIFICATE--' in line:
                        crtparse = subprocess.run(['openssl', 'x509', '-text', '-noout'], input=bytes(cert, 'ascii'), stdout=subprocess.PIPE)
                        crtxt = crtparse.stdout.decode('ascii')
                        if subject:
                            for ln in crtxt.splitlines():
                                res = re.search(r'    Subject: (.*)', ln)
#                                pat = re.compile(r'    Subject:(.*)')
#                                res = pat.search(l)
                                if res:
                                    print(res.group(1))

                        f_incert = False
                else:
                    if '--BEGIN CERTIFICATE--' in line:
                        cert = line
                        f_incert = True



    return
## Main end =================================
########### =================================

## Spusteni main ============================
########### =================================
if __name__ == '__main__': 
    main()
