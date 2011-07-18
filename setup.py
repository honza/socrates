from setuptools import setup

description =  'Socrates is a simple static site generator.'
long_desc = """
Socrates is a simple static site generator. It's geared towards blogs. You
write your posts in your favorite plain text to HTML language (e.g. Markdown,
textile) and save them as text files on your harddrive. Socrates then takes
them, and creates a full HTML site for you. For free, you will get a home page
which lists latest posts, single post pages, category pages, archive pages,
an about page and an atom feed.
"""

setup(
    name='socrates',
    version='0.4.0',
    install_requires=['django', 'pyYAML', 'jinja2', 'docutils'],
    description=description,
    long_description=long_desc,
    author='Honza Pokorny',
    maintainer='Honza Pokorny',
    maintainer_email='me@honza.ca',
    packages=['socrates'],
    entry_points={
        'console_scripts': [
            'socrates = socrates.main:main'
        ]
    }
)
