import os
import yaml
from libs.markdown import markdown
from django.template.defaultfilters import slugify


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
