import os


class BaseRenderer(object):

    def render(self, template, values):
        raise NotImplementedError


class DjangoRenderer(BaseRenderer):

    def __init__(self, path):
        from django.conf import settings
        from django.template.loader import render_to_string

        path = os.path.abspath(path)
        settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
                TEMPLATE_DIRS=[path])
        self._render = render_to_string

    def render(self, template, values):
        return self._render(template, values)


class Jinja2Renderer(BaseRenderer):

    def __init__(self, path):
        from jinja2 import Environment, FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(path))

    def render(self, template, values):
        t = self.env.get_template(template)
        return t.render(values)
