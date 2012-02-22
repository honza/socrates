import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def slugify(value):
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


def highlight_code(language, code):
    return highlight(code, get_lexer_by_name(language), HtmlFormatter())
