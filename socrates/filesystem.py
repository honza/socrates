import os
import yaml
from libs.markdown import markdown
from django.template.defaultfilters import slugify


class File(object):

    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(path)
        self.contents, self.config = self.get_contents()
        self.year = str(self.config['date'].year)
        self.month = self.config['date'].strftime("%m")
        self.slug = slugify(self.config['title'])
        self.url = "%s/%s/%s/" % (self.year, self.month, self.slug,)
        self.title = self.config['title']

    def vals(self):
        """
        Return django template values
        """
        self.config['content'] = self.contents
        return self.config

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

        c = markdown(c)
        return c, yaml.load(conf)
