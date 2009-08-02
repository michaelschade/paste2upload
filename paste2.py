#!/usr/bin/python

# No www. because the Paste2 creator apparently dislikes the subdomain?
PASTE_URL = 'http://paste2.org/new-paste'

def paste(f, lang='text', description='', **kwargs):
    """The magic of the program that connects to the Paste2 servers and
    uploads the supplied information, printing to stdout the URL."""
    from urllib2 import Request, build_opener, install_opener, urlopen
    from urllib import urlencode
    postData = urlencode({
        'lang': lang,
        'description': description,
        'code': f.read(),
        'parent': '0',
    })
    headers = {
        'User-Agent': 'Paste2 Uploader/1.4 (Michael Schade)',
    }
    request = Request(PASTE_URL, postData, headers)
    opener = build_opener()
    install_opener(opener)
    response = urlopen(request)
    from sys import stdout
    stdout.write(response.url)

def __usage():
    """Aides the user along by providing information about how to properly use the paste2upload program."""
    from sys import argv, stdout
    stdout.write("""
    Copyright (c) 2009 Michael Schade. Distributed under the MIT License
    For more information see paste2's LICENSE file or visit
    http://www.mschade.me/projects/paste2upload/.
    
    Licensing and copyright information must stay with this code at
    all times. Notification via my website (http://www.mschade.me/)
    of your projects using this code is always appreciated but
    never required.
    
    Paste2 is an independent service not provided by Michael Schade.
    No service guarantees can be made on behalf of Paste2 or its
    dependencies by Michael Schade. Any issues, questions, comments,
    or concers regarding the service should be directed to Paste2 only.
    
    Usage %s [-h, --help] [-d, --description] [-l, --language syntax code] [file]:
    
        All arguments are optional.
        
        -h,         Outputs this information. Must be supplied as the first and only argument.
        --help
        -d desc,    A description to be displayed alongside the pasted content.
        --description desc
        -l code,    The language to use for syntax highlighting. See below for a list of available highlights.
        --language code
        
                    Language Code\tDescription
                    -------------\t-----------
                    text\t\tPlain Text / Other [Default]
                    actionscript\tActionscript
                    ada\t\t\tAda
                    apache\t\tApache Config
                    applescript\t\tAppleScript
                    asm\t\t\tAssembly
                    asp\t\t\tASP
                    bash\t\tBash
                    c\t\t\tC
                    cfm\t\t\tCold Fusion
                    cpp\t\t\tC++
                    csharp\t\tC#
                    css\t\t\tCSS
                    d\t\t\tD
                    delphi\t\tDelphi
                    diff\t\tUNIX Diff
                    eiffel\t\tEiffel
                    fortran\t\tFortran
                    html4strict\t\tHTML 4 Strict
                    ini\t\t\tIni
                    java\t\tJava
                    java5\t\tJava5
                    javascript\t\tJavascript
                    latex\t\tLaTeX
                    lisp\t\tLISP
                    lua\t\t\tLua
                    matlab\t\tMATLAB
                    mysql\t\tMySQL
                    perl\t\tPerl
                    php\t\t\tPHP
                    python\t\tPython
                    qbasic\t\tQBasic / QuickBASIC
                    robots\t\tRobots
                    ruby\t\tRuby
                    sql\t\t\tSQL
                    tcl\t\t\tTCL
                    vb\t\t\tVisual BASIC
                    vbnet\t\tVB.NET
                    winbatch\t\tWinbatch
                    xml\t\t\tXML
        
        [file, -],  Pastes supplied text to http://paste2.org/. Specify - for stdin.\n\n""" % argv[0])

def __main(argv):
    """Handles processing command line arguments and distributing them to the paste function appropriately."""
    from getopt import GetoptError, getopt
    try:
        opts, args = getopt(argv, "hvd:l:", ["help", "description", "language"])
    except GetoptError:
        __usage()
        from sys import exit
        exit(0)
    pArgs = {}
    for opt,arg in opts:
        if opt in ("-h", "--help"):
            __usage()
            from sys import exit
            exit(0)
        elif opt in ("-d", "--description"):
            pArgs['description'] = arg
        elif opt in ("-l", "--language"):
            pArgs['lang'] = arg
    try:
        f = open(args[0], 'r')
    except IOError:
        if args[0] == '-':
            from sys import stdin
            paste(stdin, **pArgs)
        else:
            from sys import stdout
            stdout.write("Error: Could not locate file.\r\n")
    except IndexError:
        __usage()
    else:
        paste(f, **pArgs)
        f.close()

if __name__ == '__main__':
    from sys import argv
    __main(argv[1:])
