import os
from datetime import datetime

import yaml

from processors import Processor
from utils import slugify, highlight_code
from exceptions import ConfigurationError

EXTENSIONS = {
    '.md': 'markdown',
    '.markdown': 'markdown',
    '.mkdn': 'markdown',
    '.rst': 'rst',
    '.html': 'html',
    '.htm': 'html',
    '.txt': 'html',
    '.textile': 'textile'
}


class File(object):

    def __init__(self, path, context):

        self.context = context  # site wide config
        self.path = path

        self.filename = os.path.basename(path)
        self.parse()

        # The file should have at least a title
        try:
            self.title = self.config['title']
        except KeyError:
            raise ConfigurationError

    def _get_type(self):
        name, extension = os.path.splitext(self.path)
        try:
            self.file_type = EXTENSIONS[extension]
            return self.file_type
        except KeyError:
            raise Exception('Unknown extension')

    def parse(self):
        """
        Decide what file type the current file is.
        """
        is_rst = False
        if self.context['text_processor'] == 'extension':
            file_type = self._get_type()
            is_rst = file_type == 'rst'

        if self.context['text_processor'] in ['markdown', 'textile', 'html']:
            is_rst = False
            self.file_type = self.context['text_processor']

        if is_rst:
            self._parse_rst()
        else:
            self._parse()

    def _parse(self):
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
            if x.startswith('-' * 79):
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

        self.config = yaml.load(conf)
        self.contents = self._process_contents(c)

    def _parse_rst(self):
        try:
            h = self.context['initial_header_level']
        except KeyError:
            h = 2
        p = Processor(self.path, self.context, 'html', h)
        self.contents = p.content
        self.config = p.metadata

        try:
            d = datetime.strptime(self.config['date'], '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                d = datetime.strptime(self.config['date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ConfigurationError

        self.year = d.year
        self.month = d.strftime("%m")
        self.date = d.strftime(self.context['date_format'])
        try:
            self.config['categories'] = self.config['categories'].split(', ')
        except KeyError:
            pass

        self.config['date'] = d

    def _process_contents(self, text):
        """
        Run contents through a text processor.
        Options:
            - markdown
            - textile
            - html
        """
        p = self.file_type
        p = p.lower()

        if p == 'markdown':
            import misaka
            html = misaka.html(unicode(text, "utf-8"),
                render_flags=misaka.HTML_GITHUB_BLOCKCODE,
                extensions=misaka.EXT_FENCED_CODE)
            html = highlight_code(html)
        elif p == 'textile':
            try:
                from textile import textile
            except ImportError:
                import sys
                print 'Please install textile to continue'
                sys.exit(1)
            html = textile(text)
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
        self.day = self.config['date'].strftime("%d")
        self.date = self.config['date'].strftime(self.context['date_format'])
        self.atom_date = self._get_atom_date(self.config['date'])
        if self.config.get('slug'):
            self.slug = self.config['slug']
        else:
            self.slug = slugify(self.config['title'])

        if context['append_slash']:
            url_template = '%s/%s/%s/'
        else:
            url_template = '%s/%s/%s'

        if context['url_include_day']:
            url_template = '%s/' + url_template
            self.url = url_template % (self.year, self.month, self.day,
                    self.slug,)
        else:
            self.url = url_template % (self.year, self.month, self.slug,)

        categories = self.config.get('categories', ['Uncategorized'])
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
        return d + "Z"


class Page(File):

    def __init__(self, path, context):
        super(Page, self).__init__(path, context)
