import re


def slugify(value):
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


def ligatures(text):
    text = text.replace('ft', '&#xFB05;')
    text = text.replace('ffl', '&#xFB04;')
    text = text.replace('ffi', '&#xFB03;')
    text = text.replace('fl', '&#xFB02;')
    text = text.replace('fi', '&#xFB01;')
    text = text.replace('ff', '&#xFB00;')
    return text
