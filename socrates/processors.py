try:
    import docutils
except ImportError:
    import sys
    print 'You must install docutils to use reStructuredText'
    print 'pip install docutils'
    sys.exit(1)

import docutils.core
from docutils.writers.html4css1 import HTMLTranslator
from docutils.writers.latex2e import LaTeXTranslator
from docutils import nodes
from docutils.parsers.rst import directives, Directive

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, TextLexer
    from pygments.formatters import HtmlFormatter
    from pygments.formatters import LatexFormatter
except ImportError:
    import sys
    print 'You must install pygments to use reStructuredText'
    print 'pip install pygments'
    sys.exit(1)

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = False

# The default formatter
DEFAULT = LatexFormatter()
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)

# Add name -> formatter pairs for every variant you want to use
VARIANTS = {
    # 'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}

def raw_html(name, args, options, content, lineno, contentOffset, blockText, state, stateMachine):
    """
    Simply render the input html as html.
    """
    if content == "":
        return
    return [nodes.raw(text='\n'.join(content), format='html')]
raw_html.content = True
directives.register_directive('raw_html', raw_html)

class Pygments(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True
    formatter = DEFAULT

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        if self.options and VARIANTS[self.options.keys()[0]]:
            self.formatter = VARIANTS[self.options.keys()[0]]

        parsed = highlight(u'\n'.join(self.content), lexer, self.formatter)
        return [nodes.raw('', parsed, format='html')]


class Processor(object):

    allowed_types = ['html', 'latex', 'xetex']

    class HtmlTranslator(HTMLTranslator):
        def astext(self):
            return ''.join(self.body)

        def visit_field_body(self, node):
            pass

        def depart_field_body(self, node):
            pass

    class LatexTranslator(LaTeXTranslator):
        def astext(self):
            return ''.join(self.body)

        def visit_field_body(self, node):
            pass

        def depart_field_body(self, node):
            pass

    def __init__(self, filename, global_settings, output='html',
            header_level=2):

        self.settings = global_settings
        self.pygments_builder()

        directives.register_directive('sourcecode', self.pygmenter)
        directives.register_directive('code-block', self.pygmenter)

        self.filename = filename
        if output not in self.allowed_types:
            raise NotImplementedError("Can't render '%s'." % output)
        self.header_level = str(header_level)
        self.output = output
        self.metadata = None
        self.get_publisher()
        self.get_metadata()
        self.run()

    def pygments_builder(self):

        self.pygmenter = Pygments
        if self.settings['pygments']:
            print self.settings['pygments']
            self.pygmenter.formatter = HtmlFormatter(
                **self.settings['pygments'])

    def render_node_to_html(self, document, node):
        if self.output == 'html':
            visitor = self.HtmlTranslator(document)
        elif self.output == 'latex' or self.output == 'xetex':
            visitor = self.LatexTranslator(document)
        else:
            pass

        node.walkabout(visitor)
        return visitor.astext()

    def get_metadata(self):
        self.metadata = {}
        for docinfo in self.pub.document.traverse(docutils.nodes.docinfo):
            for element in docinfo.children:
                if element.tagname == 'field':
                    name_elem, body_elem = element.children
                    name = name_elem.astext()
                    value = self.render_node_to_html(self.pub.document,
                            body_elem)
                else:
                    name = element.tagname
                    value = element.astext()
                self.metadata[name] = value

    def get_publisher(self):
        extra_params = {
            'initial_header_level': self.header_level
        }
        pub = docutils.core.Publisher(
            destination_class=docutils.io.StringOutput)
        pub.set_components('standalone', 'restructuredtext', self.output)
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=self.filename)
        pub.publish()
        self.pub = pub

    def run(self):
        parts = self.pub.writer.parts
        if self.output == 'html':
            content = parts.get('body')
        elif self.output == 'latex' or self.output == 'xetex':
            content = parts.get('body')
            content = parts.get('whole')
        else:
            pass

        self.content = content
