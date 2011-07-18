import os
import yaml

from utils import slugify


class File(object):

    def __init__(self, path, context):

        self.context = context # site wide config
        self.path = path

        self.filename = os.path.basename(path)
        self.contents, self.config = self.get_contents()
        self.title = self.config['title']

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
        c = self._process_contents(c)
        return c, config

    def _process_contents(self, text):
        """
        Run contents through a text processor.
        Options:
            - markdown
            - textile
            - restructuredtext
            - html
        """
        p = self.context['text_processor']
        p = p.lower()

        if p == 'markdown':
            from markdown import markdown
            html = markdown(text)
        elif p == 'textile':
            from textile import textile
            html = textile(text)
        elif p == 'restructuredtext':
            from docutils.core import publish_parts
            parts = publish_parts(source=text, writer_name="html4css1")
            html = parts.get('fragment')
        elif p == 'pygmentedmarkdown':
            from pygmentedmarkdown import markdown
            html = markdown(text)
        elif p == 'html':
            html = text
        else:
            raise Exception("Unknown text processor")

        return html


class Post(File):
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
        super(Post, self).__init__(path, context)

        self.year = str(self.config['date'].year)
        self.month = self.config['date'].strftime("%m")
        self.date = self.config['date'].strftime(self.context['date_format'])
        self.atom_date = self._get_atom_date(self.config['date'])

        self.slug = slugify(self.config['title'])
        self.url = "%s/%s/%s/" % (self.year, self.month, self.slug,)

        categories = self.config['categories']
        self.categories = []
        for c in categories:
            v = {
                'name': c,
                'slug': slugify(c)
            }
            self.categories.append(v)

        if 'author' not in self.config:
            self.author = self.context['author']
        else:
            self.author = self.config['author']

    def _get_atom_date(self, date):
        d = date.strftime('%Y-%m-%dT%H:%M:%S%z')
        return d[:-2] + ':' + d[-2:]


class Page(File):

    def __init__(self, path, context):
        super(Page, self).__init__(path, context)
