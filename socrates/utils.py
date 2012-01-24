import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def slugify(value):
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


_re_codeblock = re.compile(r'<pre(?: lang="([a-z0-9]+)")?><code'
    '(?: class="([a-z0-9]+).*?")?>(.*?)</code></pre>',
    re.IGNORECASE | re.DOTALL)


def highlight_code(html):
    def _unescape_html(html):
        html = html.replace('&lt;', '<')
        html = html.replace('&gt;', '>')
        html = html.replace('&amp;', '&')
        return html.replace('"', '"')
    def _highlight_match(match):
        language, classname, code = match.groups()
        if (language or classname) is None:
            return match.group(0)
        return highlight(_unescape_html(code),
            get_lexer_by_name(language or classname),
            HtmlFormatter())
    return _re_codeblock.sub(_highlight_match, html)
