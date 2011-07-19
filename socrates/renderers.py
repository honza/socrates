import os


class DjangoRenderer(object):

    def __init__(self, path):
        try:
            from django.conf import settings
            from django.template.loader import render_to_string
        except ImportError:
            import sys
            print "You have to install django to continue."
            print "Run: pip install django"
            sys.exit(1)
        path = os.path.abspath(path)
        settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
                TEMPLATE_DIRS=[path])
        self._render = render_to_string

    def render(self, template, values):
        return self._render(template, values)


class Jinja2Renderer(object):

    def __init__(self, path):
        try:
            from jinja2 import Environment, FileSystemLoader
        except ImportError:
            import sys
            print "You have to install jinja2 to continue."
            print "Run: pip install jinja2"
            sys.exit(1)
        self.env = Environment(loader=FileSystemLoader(path))

    def render(self, template, values):
        t = self.env.get_template(template)
        return t.render(values)
