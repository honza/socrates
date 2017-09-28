import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

register = template.Library()


def amp(text):
    """Wraps apersands in HTML with ``<span class="amp">`` so they can be
    styled with CSS. Apersands are also normalized to ``&amp;``. Requires
    ampersands to have whitespace or an ``&nbsp;`` on both sides.
    """
    text = force_unicode(text)
    # it kinda sucks but it fixes the standalone amps in attributes bug
    tag_pattern = \
        '</?\w+((\s+\w+(\s*=\s*(?:".*?"|\'.*?\'|[^\'">\s]+))?)+\s*|\s*)/?>'
    amp_finder = re.compile(r"(\s|&nbsp;)(&|&amp;|&\#38;)(\s|&nbsp;)")
    intra_tag_finder = re.compile(
        r'(?P<prefix>(%s)?)(?P<text>([^<]*))(?P<suffix>(%s)?)' %
        (tag_pattern, tag_pattern))

    def _amp_process(groups):
        prefix = groups.group('prefix') or ''
        text = amp_finder.sub(r"""\1<span class="amp">&amp;</span>\3""",
                              groups.group('text'))
        suffix = groups.group('suffix') or ''
        return prefix + text + suffix

    output = intra_tag_finder.sub(_amp_process, text)
    return mark_safe(output)


amp.is_safe = True


def caps(text):
    """Wraps multiple capital letters in ``<span class="caps">``
    so they can be styled with CSS.

    >>> caps("A message from KU")
    u'A message from <span class="caps">KU</span>'
    """
    text = force_unicode(text)
    try:
        from . import smartypants
    except ImportError:
        raise Exception("Error in {% caps %} filter: "
                        "The Python SmartyPants library isn't installed.")

    tokens = smartypants._tokenize(text)
    result = []
    in_skipped_tag = False

    cap_finder = re.compile(r"""(
                            (\b[A-Z\d]*
                            [A-Z]\d*[A-Z]
                            [A-Z\d']*\b)
                            | (\b[A-Z]+\.\s?
                            (?:[A-Z]+\.\s?)+)
                            (?:\s|\b|$))
                            """, re.VERBOSE)

    def _cap_wrapper(matchobj):
        """
        This is necessary to keep dotted cap strings to pick up extra spaces
        """
        if matchobj.group(2):
            return """<span class="caps">%s</span>""" % matchobj.group(2)
        else:
            if matchobj.group(3)[-1] == " ":
                caps = matchobj.group(3)[:-1]
                tail = ' '
            else:
                caps = matchobj.group(3)
                tail = ''
            return """<span class="caps">%s</span>%s""" % (caps, tail)

    tags_to_skip_regex = re.compile("<(/)?(?:pre|code|kbd|script|math)[^>]*>",
                                    re.IGNORECASE)

    for token in tokens:
        if token[0] == "tag":
            # Don't mess with tags.
            result.append(token[1])
            close_match = tags_to_skip_regex.match(token[1])
            if close_match and close_match.group(1) is None:
                in_skipped_tag = True
            else:
                in_skipped_tag = False
        else:
            if in_skipped_tag:
                result.append(token[1])
            else:
                result.append(cap_finder.sub(_cap_wrapper, token[1]))
    output = "".join(result)
    return mark_safe(output)


caps.is_safe = True


def initial_quotes(text):
    """Wraps initial quotes in ``class="dquo"`` for double quotes or
    ``class="quo"`` for single quotes. Works in these block tags
    ``(h1-h6, p, li, dt, dd)`` and also accounts for potential opening inline
    elements ``a, em, strong, span, b, i``
    """
    text = force_unicode(text)
    quote_finder = re.compile(r"""((<(p|h[1-6]|li|dt|dd)[^>]*>|^)
                                  \s*
                                  (<(a|em|span|strong|i|b)[^>]*>\s*)*)
                                  (("|&ldquo;|&\#8220;)|('|&lsquo;|&\#8216;))
                                  """, re.VERBOSE)

    def _quote_wrapper(matchobj):
        if matchobj.group(7):
            classname = "dquo"
            quote = matchobj.group(7)
        else:
            classname = "quo"
            quote = matchobj.group(8)
        return """%s<span class="%s">%s</span>""" % (
            matchobj.group(1), classname, quote)

    output = quote_finder.sub(_quote_wrapper, text)
    return mark_safe(output)


initial_quotes.is_safe = True


def smartypants(text):
    """Applies smarty pants to curl quotes.

    >>> smartypants('The "Green" man')
    u'The &#8220;Green&#8221; man'
    """
    text = force_unicode(text)
    try:
        from . import smartypants
    except ImportError:
        raise Exception("Error in {% smartypants %} filter: "
                        "The Python smartypants library isn't installed.")
    else:
        output = smartypants.smartyPants(text)
        return mark_safe(output)


smartypants.is_safe = True


def typogrify(text):
    """
    The super typography filter

    Applies the following filters: widont, smartypants, caps, amp,
    initial_quotes
    """
    text = force_unicode(text)
    text = amp(text)
    text = widont(text)
    text = smartypants(text)
    text = caps(text)
    text = initial_quotes(text)
    return text


def widont(text):
    """Replaces the space between the last two words in a string with ``&nbsp;``
    Works in these block tags ``(h1-h6, p, li, dd, dt)`` and also accounts for
    potential closing inline elements ``a, em, strong, span, b, i``

    >>> widont('A very simple test')
    u'A very simple&nbsp;test'

    Single word items shouldn't be changed
    >>> widont('Test')
    u'Test'
    >>> widont(' Test')
    u' Test'
    >>> widont('<ul><li>Test</p></li><ul>')
    u'<ul><li>Test</p></li><ul>'
    >>> widont('<ul><li> Test</p></li><ul>')
    u'<ul><li> Test</p></li><ul>'

    >>> widont('<p>In a couple of paragraphs</p><p>paragraph two</p>')
    u'<p>In a couple of&nbsp;paragraphs</p><p>paragraph&nbsp;two</p>'

    >>> widont('<h1><a href="#">In a link inside a heading</i> </a></h1>')
    u'<h1><a href="#">In a link inside a&nbsp;heading</i> </a></h1>'

    >>> widont('<h1><a href="#">In a link</a> followed by other text</h1>')
    u'<h1><a href="#">In a link</a> followed by other&nbsp;text</h1>'

    Empty HTMLs shouldn't error
    >>> widont('<h1><a href="#"></a></h1>')
    u'<h1><a href="#"></a></h1>'

    >>> widont('<div>Divs get no love!</div>')
    u'<div>Divs get no love!</div>'

    >>> widont('<pre>Neither do PREs</pre>')
    u'<pre>Neither do PREs</pre>'

    >>> widont('<div><p>But divs with paragraphs do!</p></div>')
    u'<div><p>But divs with paragraphs&nbsp;do!</p></div>'
    """
    text = force_unicode(text)
    widont_finder = re.compile(r"""((?:</?(?:a|em|span|strong|i|b)[^>]*>)|[^<>\s])
                                   \s+
                                   ([^<>\s]+
                                   \s*
                                   (</(a|em|span|strong|i|b)>\s*)*
                                   ((</(p|h[1-6]|li|dt|dd)>)|$))
                                   """, re.VERBOSE)
    output = widont_finder.sub(r'\1&nbsp;\2', text)
    return mark_safe(output)


widont.is_safe = True

register.filter('amp', amp)
register.filter('caps', caps)
register.filter('initial_quotes', initial_quotes)
register.filter('smartypants', smartypants)
register.filter('typogrify', typogrify)
register.filter('widont', widont)
