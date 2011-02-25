from socrates.main import main
from optparse import OptionParser


parser = OptionParser()
parser.add_option('-i', '--init', action='store', help='Some help')
parser.add_option('-g', '--generate', action='store', help='Some help')
parser.add_option('-r', '--run', action='store', help='Some help')

options, args = parser.parse_args()

if options.init:
    import shutil
    try:
        shutil.copytree('socrates/themes/default', options.init)
    except OSError:
        print "The '%s' directory already exists." % options.init

if options.generate:
    main(options.generate)

if options.run:
    import SimpleHTTPServer
    import SocketServer
    import os

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
