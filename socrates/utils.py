import re


def slugify(value):
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


def ligatures(text):
    # TODO: Georgia doesn't like the following three.
    # text = text.replace('ft', '&#xFB05;')
    # text = text.replace('ffl', '&#xFB04;')
    # text = text.replace('ffi', '&#xFB03;')
    text = text.replace('fl', '&#xFB02;')
    text = text.replace('fi', '&#xFB01;')
    return text
