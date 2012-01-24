from setuptools import setup

description = 'Socrates is a simple static site generator.'
long_desc = open('README.rst').read()

setup(
    name='socrates',
    version='0.7.0',
    url='http://honza.github.com/socrates/',
    install_requires=[
        'pyYAML',
        'misaka',
        'django',
        'jinja2',
        'docutils',
        'pygments',
        'textile'
    ],
    description=description,
    long_description=long_desc,
    author='Honza Pokorny',
    author_email='me@honza.ca',
    maintainer='Honza Pokorny',
    maintainer_email='me@honza.ca',
    packages=['socrates'],
    include_package_data=True,
    scripts=['bin/socrates'],
)
