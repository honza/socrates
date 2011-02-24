from socrates.main import main
from socrates.bootstrap import run
from optparse import OptionParser


parser = OptionParser()
parser.add_option('-i', '--init', action='store_true', help='Some help')
parser.add_option('-g', '--generate', action='store_true', help='Some help')
parser.add_option('-r', '--run', action='store_true', help='Some help')

options, args = parser.parse_args()

if options.init:
    run()

if options.generate:
    main()

if options.run:
    import SimpleHTTPServer
    import SocketServer
    import os

    os.chdir('blog/deploy')

    PORT = 8000

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print "serving at port", PORT
    httpd.serve_forever()
        
