import os
import shutil
import yaml
from filesystem import Post
from django.conf import settings
from django.template.defaultfilters import slugify


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

        self.posts = []
        self.categories = {}

        for filename in os.listdir(self.POSTS):
            if filename.endswith('.md'):
                p = os.path.join(self.POSTS, filename)
                self.posts.append(Post(p, self.SETTINGS))

        self.posts.reverse()
        for post in self.posts:
            # Get categories
            self._get_post_cats(post)
        self.SETTINGS = dict(self.SETTINGS, **{'categories': self.categories})

        # Prepare post dirs
        self.years = {}
        for post in self.posts:
            date = post.config['date']
            if date.year not in self.years:
                self.years[str(date.year)] = []
        self.SETTINGS = dict(self.SETTINGS, **{'years': self.years})

        for post in self.posts:
            date = post.config['date']
            m = date.strftime("%m")
            y = self.years[str(date.year)]
            if m not in y:
                self.years[str(date.year)].append(m)

        # Make dirs
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

        # Save posts
        for post in self.posts:
            b = post.slug + '.html'
            m = os.path.join(self.DEPLOY, post.year, post.month, b)

            content = render_to_string(self.SINGLE, self._v({'post': post}))
            self._write_to_file(m, content)

        # Index file
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
        contents = render_to_string(self.INDEX, self._v({'posts': posts, 'extra':
            extra}))
        self._write_to_file(m, contents)

        # Save category pages
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
                contents = render_to_string(self.CATEGORY, self._v({'category': k, 'posts':
                    posts}))
                m = os.path.join(p, 'index.html')
                self._write_to_file(m, contents)

        self.archives = {}
        for post in self.posts:
            d = str(post.year)
            if d not in self.archives:
                self.archives[d] = [post]
            else:
                self.archives[d].append(post)

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
                contents = render_to_string(self.ARCHIVE, self._v({'year': k, 'posts':
                    posts}))
                m = os.path.join(p, 'index.html')
                self._write_to_file(m, contents)

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

            contents = render_to_string(self.PAGED, self._v(v))
            c = os.path.join(e, "index.html")
            self._write_to_file(c, contents)
            

        for p in self.posts:
            print p.filename

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

def main(directory):
    Generator(directory)
