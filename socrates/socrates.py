"""
Socrates
Static site generator
(c) 2011 - Honza Pokorny <me@honza.ca> <http://github.com/honza/socrates>
BSD licensed
"""
import os
import shutil
import yaml
from datetime import datetime

from renderers import DjangoRenderer, Jinja2Renderer
from models import Post, Page
from utils import slugify


class Generator(object):

    # Templates
    SINGLE = 'single.html'
    PAGE = 'page.html'
    INDEX = 'index.html'
    CATEGORY = 'category.html'
    ARCHIVE = 'archive.html'
    PAGED = 'index_paged.html'
    ATOM = 'atom.html'

    # Directories
    ROOT = None
    DEPLOY = None
    POSTS = None

    # Global, site-wide settings
    SETTINGS = None

    def __init__(self, directory):
        m = os.getcwd()
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
        self.init_template_renderer()

        self.posts = []
        self.categories = {}
        self.years = {}
        self.archives = {}

        self.load_posts()
        self.process_posts()

        self.SETTINGS = dict(self.SETTINGS, **{'categories': self.categories})
        self.SETTINGS = dict(self.SETTINGS, **{'years': self.years})

        self.make_index_page()
        self.make_atom()
        self.make_category_pages()
        self.make_archive_pages()
        self.make_pagination()
        self.make_about_page()

        print "Success!"

    def init_template_renderer(self):
        t = self.SETTINGS['templates']
        layout = os.path.join(self.ROOT, 'layout')
        if t == 'jinja2':
            self.template = Jinja2Renderer(layout)
        elif t == 'django':
            self.template = DjangoRenderer(layout)
        else:
            raise NotImplementedError("I don't know this template type.")

    def render(self, template, values):
        return self.template.render(template, values)

    def _get_page_str(self, current, total):
        """
        Return page number as a string for pagination.
        """
        current += 1
        if total < 10:
            return str(current)
        elif 10 <= total < 100:
            if total < 10:
                return '0%d' % current
            else:
                return str(current)

    def _get_post_cats(self, post):
        """
        Extract and save post's categories
        """
        cats = post.config['categories']
        for c in cats:
            if c not in self.categories:
                self.categories[c] = [post]
            else:
                self.categories[c].append(post)

    def _get_settings(self):
        """
        Read main config file. Return dict.
        """
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
        """
        Create a joint dict of global config and local template vals
        """
        return dict(self.SETTINGS, **vals)

    def load_posts(self):
        """
        Get all files from the posts directory, create Post instances and add
        them to the self.posts list.
        """
        for filename in os.listdir(self.POSTS):
            if not filename.startswith('.') and not filename.startswith('_'):
                p = os.path.join(self.POSTS, filename)
                self.posts.append(Post(p, self.SETTINGS))
        self.posts.reverse()

    def process_posts(self):
        """
        Collect all the necessary information about posts.
        """
        print 'Processing posts...'
        for post in self.posts:
            # Get categories
            self._get_post_cats(post)

            # Post dirs
            #   years
            date = post.config['date']
            year = str(date.year)
            if year not in self.years:
                self.years[year] = []
            #   months
            m = date.strftime("%m")
            y = self.years[year]
            if m not in y:
                self.years[year].append(m)

            # Archives
            d = year
            if d not in self.archives:
                self.archives[d] = [post]
            else:
                self.archives[d].append(post)

        self.make_post_directories()
        self.save_posts()

    def save_posts(self):
        print 'Saving posts...'
        for post in self.posts:
            # Save the thing
            b = post.slug + '.html'
            m = os.path.join(self.DEPLOY, post.year, post.month, b)

            if 'template' in post.config.keys():
                t = post.config['template']
            else:
                t = self.SINGLE

            content = self.render(t, self._v({'post': post}))

            # Print filename to show progress
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
        if self.SETTINGS['posts_per_page'] == 0:
            # List all posts on the index page
            posts = self.posts
            extra = False
        elif len(self.posts) > self.SETTINGS['posts_per_page']:
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

    def make_atom(self):
        """
        Create an atom feed 
        """
        m = os.path.join(self.DEPLOY, 'atom.xml')
        if self.SETTINGS['posts_per_page'] == 0:
            # List all posts on the index page
            posts = self.posts
        elif len(self.posts) > self.SETTINGS['posts_per_page']:
            # Cut off unnecessary posts
            n = len(self.posts)
            n = self.SETTINGS['posts_per_page']
            posts = self.posts[:n]
        else:
            posts = self.posts
        contents = self.render(self.ATOM, self._v({'posts': posts, 'now':
            self._get_atom_date()}))
        self._write_to_file(m, contents)

    def _get_atom_date(self):
        date = datetime.utcnow()
        d = date.strftime('%Y-%m-%dT%H:%M:%S%z')
        return d[:-2] + ':' + d[-2:]



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
        """
        Make archive pages. Only by year.
        """
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
        per = int(self.SETTINGS['posts_per_page'])
        if per == 0:
            # Skip pagination if all posts are on index page
            return
        print 'Creating pagination...'
        num = len(self.posts)
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
            
    def make_about_page(self):
        print 'Creating about page...'
        files = os.listdir(self.ROOT)
        path = ""
        for f in files:
            if f.startswith('about.'):
                path = f
                break
        path = os.path.join(self.ROOT, path)
        about = Page(path, self.SETTINGS)
        v = {'page': about}

        c = os.path.join(self.DEPLOY, 'about.html')

        contents = self.render(self.PAGE, self._v(v))
        self._write_to_file(c, contents)
