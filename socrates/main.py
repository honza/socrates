#!/usr/bin/env python

import os
import shutil
from optparse import OptionParser
from socrates import Generator

def main():
    usage = "Socrates - static site generator\nUsage: socrates.py [options]"
    parser = OptionParser(usage=usage)
    parser.add_option('-i', '--init', action='store', 
        help="Create a new blog in DIR", metavar="DIR")
    parser.add_option('-g', '--generate', action='store',
        help="Generate a static site for a site in DIR.", metavar="DIR")
    parser.add_option('-r', '--run', action='store',
            help="Run a simple server in DIR.", metavar="DIR")

    options, args = parser.parse_args()

    if options.init:
        try:
            shutil.copytree('themes/default', options.init)
        except OSError:
            print "The '%s' directory already exists." % options.init

    if options.generate:
        Generator(options.generate)

    if options.run:
        import SimpleHTTPServer
        import SocketServer

        p = os.path.dirname(__file__)
        p = os.path.join(p, options.run, 'deploy')
        if os.path.exists(p):
            os.chdir('%s/deploy' % options.run)
            PORT = 8000
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(("", PORT), Handler)
            print "serving at port", PORT
            httpd.serve_forever()
        else:    
            print "The '%s' directory doesn't exist." % p
