import os
import shutil
import yaml
from django.conf import settings
from django.template.defaultfilters import slugify
from libs.markdown import markdown


class Post(object):
    """
    Post object. Exposes the following attributes:
        - filename (e.g. 2010-cool-post.md)
        - path (e.g. /home/user/2010-cool-post.md)
        - contents (post content)
        - config (post front config)
        - year, month, date (in the format specified in config.yaml)
        - title
        - url (e.g. /2010/02/cool-post/)
        - categories (list)
        - author (from config.yaml or from front config)

    All attributes are calculated on init.
    """

    def __init__(self, path, context):

        self.context = context # site wide config
        self.path = path

        self.filename = os.path.basename(path)
        self.contents, self.config = self.get_contents()

        self.year = str(self.config['date'].year)
        self.month = self.config['date'].strftime("%m")
        self.date = self.config['date'].strftime(self.context['date_format'])

        self.slug = slugify(self.config['title'])
        self.url = "%s/%s/%s/" % (self.year, self.month, self.slug,)
        self.title = self.config['title']
        self.categories = self.config['categories']
        if 'author' not in self.config:
            self.author = self.context['author']
        else:
            self.author = self.config['author']

    def get_contents(self):
        """
        Read file contents. Extract yaml config. Return post contents and
        parsed config.
        """
        f = open(self.path, 'r')

        c = ""
        start = False
        end = False
        conf = ""
        for x in f:
            if x.startswith('-'*80):
                if not start:
                    start = True
                else:
                    end = True
                continue

            if start and not end:
                conf += x
            else:
                c += x
        f.close()

        config = yaml.load(conf)
        try:
            pr = self.context['text_processor']
            if pr == 'markdown':
                c = markdown(c)
        except KeyError:
            pass
        return c, config


class Generator(object):

    # Templates
    SINGLE = 'single.html'
    INDEX = 'index.html'
    CATEGORY = 'category.html'
    ARCHIVE = 'archive.html'
    PAGED = 'index_paged.html'

    # Directories
    ROOT = None
    DEPLOY = None
    POSTS = None

    # Global, site-wide settings
    SETTINGS = None


    def __init__(self, directory):
        m = os.path.dirname(os.path.dirname(__file__))
        self.ROOT = os.path.join(m, directory)

        if not os.path.exists(self.ROOT):
            print "The '%s' directory doesn't exist." % directory
            return
        self.DEPLOY = os.path.join(self.ROOT, 'deploy')
        if not os.path.exists(self.DEPLOY):
            os.mkdir(self.DEPLOY)
        # TODO: This needs a better solution. Simlinks perhaps?
        if os.path.exists(os.path.join(self.DEPLOY, 'media')):
            shutil.rmtree(os.path.join(self.DEPLOY, 'media'))
        shutil.copytree(os.path.join(self.ROOT, 'layout', 'media'),
                os.path.join(self.DEPLOY, 'media'))

        self.POSTS = os.path.join(self.ROOT, 'posts')
        self.SETTINGS = self._get_settings()

        # django boiler plate
        x = (os.path.join(self.ROOT, 'layout'),)
        settings.configure(DEBUG=True, TEMPLATE_DEBUG=True, TEMPLATE_DIRS=x)
        from django.template.loader import render_to_string
        # Remap a django function to a method
        self.render = render_to_string

        self.posts = []
        self.categories = {}
        self.years = {}
        self.archives = {}

        self.load_posts()
        self.process_posts()

        self.SETTINGS = dict(self.SETTINGS, **{'categories': self.categories})
        self.SETTINGS = dict(self.SETTINGS, **{'years': self.years})

        self.make_index_page()
        self.make_category_pages()
        self.make_archive_pages()
        self.make_pagination()

        print "Success!"

    def _get_page_str(self, current, total):
        current += 1
        if total < 10:
            return str(current)
        elif 10 <= total < 100:
            if total < 10:
                return '0%d' % current
            else:
                return str(current)

    def _get_post_cats(self, post):
        cats = post.config['categories']
        for c in cats:
            if c not in self.categories:
                self.categories[c] = [post]
            else:
                self.categories[c].append(post)

    def _get_settings(self):
        s = os.path.join(self.ROOT, 'config.yaml')
        if not os.path.exists(s):
            raise Exception('No config file.')
        f = open(s, 'r')
        c = f.read()
        f.close()
        return yaml.load(c)

    def _write_to_file(self, path, contents):
        """
        Create a file (path) with contents
        """
        f = open(path, 'w')
        f.write(contents)
        f.close()

    def _v(self, vals):
        return dict(self.SETTINGS, **vals)

    def load_posts(self):
        """
        Get all files from the posts directory, create Post instances and add
        them to the self.posts list.
        """
        # TODO: Allow different file extensions
        for filename in os.listdir(self.POSTS):
            if filename.endswith('.md'):
                p = os.path.join(self.POSTS, filename)
                self.posts.append(Post(p, self.SETTINGS))
        self.posts.reverse()

    def process_posts(self):
        """
        Collect all the necessary information about posts.
        """
        print 'Processing posts...'
        self.make_post_directories()
        for post in self.posts:
            # Get categories
            self._get_post_cats(post)
            # Post dirs
            #   years
            date = post.config['date']
            if date.year not in self.years:
                self.years[str(date.year)] = []
            #   months
            m = date.strftime("%m")
            y = self.years[str(date.year)]
            if m not in y:
                self.years[str(date.year)].append(m)
            # Archives
            d = str(post.year)
            if d not in self.archives:
                self.archives[d] = [post]
            else:
                self.archives[d].append(post)
            # Save the thing
            b = post.slug + '.html'
            m = os.path.join(self.DEPLOY, post.year, post.month, b)

            content = self.render(self.SINGLE, self._v({'post': post}))
            print post.filename
            self._write_to_file(m, content)

    def make_post_directories(self):
        """
        If they don't exist, create post directories.
            2011
                01
                03
                12
            2010
                04
                07
        """
        print 'Creating directories...'
        keys = self.years.keys()
        for k in keys:
            m = os.path.join(self.DEPLOY, k)
            if not os.path.exists(m):
                os.mkdir(m)
            months = self.years[k]
            for month in months:
                m = os.path.join(self.DEPLOY, k, month)
                if not os.path.exists(m):
                    os.mkdir(m)

    def make_index_page(self):
        """
        Create an index page
        """
        m = os.path.join(self.DEPLOY, 'index.html')
        if len(self.posts) > self.SETTINGS['posts_per_page']:
            # Cut off unnecessary posts
            n = len(self.posts)
            n = self.SETTINGS['posts_per_page']
            posts = self.posts[:n]
            extra = True
        else:
            posts = self.posts
            extra = False
        contents = self.render(self.INDEX, self._v({'posts': posts, 'extra':
            extra}))
        self._write_to_file(m, contents)


    def make_category_pages(self):
        """
        Make category pages. They go into the 'category' directory.
        """
        keys = self.categories.keys()
        if len(keys) != 0:
            # Make category dir
            self.CATEGORIES = os.path.join(self.DEPLOY, 'category')
            if not os.path.exists(self.CATEGORIES):
                os.mkdir(self.CATEGORIES)
            for k in keys:
                p = os.path.join(self.CATEGORIES, slugify(k))
                if not os.path.exists(p):
                    os.mkdir(p)
                posts = self.categories[k]
                contents = self.render(self.CATEGORY, self._v({'category': k, 'posts':
                    posts}))
                m = os.path.join(p, 'index.html')
                self._write_to_file(m, contents)

    def make_archive_pages(self):
        print 'Creating archives...'
        keys = self.archives.keys()
        if len(keys) != 0:
            # Make category dir
            self.ARCHIVES = os.path.join(self.DEPLOY, 'archive')
            if not os.path.exists(self.ARCHIVES):
                os.mkdir(self.ARCHIVES)
            for k in keys:
                p = os.path.join(self.ARCHIVES, slugify(k))
                if not os.path.exists(p):
                    os.mkdir(p)
                posts = self.archives[k]
                contents = self.render(self.ARCHIVE, self._v({'year': k, 'posts':
                    posts}))
                m = os.path.join(p, 'index.html')
                self._write_to_file(m, contents)

    def make_pagination(self):
        """
        Make pagination.
            /page/2/
            /page/3/
        Uses posts per page setting
        """
        print 'Creating pagination...'
        num = len(self.posts)
        per = int(self.SETTINGS['posts_per_page'])
        pages = num/per

        m = os.path.join(self.DEPLOY, 'page')
        if not os.path.exists(m):
            os.mkdir(m)
        for x in range(1, pages + 1):
            if x == 1:
                prev = '/'
            else:
                prev = '/page/%d/' % x

            if x < pages:
                next = '/page/%d/' % int(x+1)
            else:
                next = None

            n = per*x
            p = self.posts[n:n+per]

            v = {
                'page': x+1,
                'posts': p,
                'prev': prev,
                'total': pages+1,
                'next': next
            }

            folder = self._get_page_str(x, pages+1)

            e = os.path.join(m, folder)
            if not os.path.exists(e):
                os.mkdir(e)

            contents = self.render(self.PAGED, self._v(v))
            c = os.path.join(e, "index.html")
            self._write_to_file(c, contents)
            


if __name__ == '__main__':
    from optparse import OptionParser
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
