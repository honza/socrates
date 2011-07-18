===============================================================================
Socrates
===============================================================================

Socrates is a simple static site generator. It's geared towards blogs. You
write your posts in your favorite plain text to HTML language (e.g. Markdown,
textile) and save them as text files on your harddrive. Socrates then takes
them, and creates a full HTML site for you. For free, you will get a home page
which lists latest posts, single post pages, category pages, archive pages,
an about page and an atom feed.

Usage
-------------------------------------------------------------------------------

First, you need to create a new blog::

    python socrates.py -i blog

This will create a ``blog`` directory with a simple blog structure::

    blog
        posts
            2010-your-post.md
        layout
            index.html
            single.html
            category.html
            ...
        media
            style.css
        config.yaml
        about.md

The ``posts`` directory is where you will place your posts files. Anything
prefixed with ``_`` or ``.`` will be ignored. ``layout`` is your basic theme or
a template. ``config.yaml`` is a site-wide configuration file. Don't forget to
update the about file with relevant information.

When you are ready to generate your site, you run::

    python socrates.py -g blog

This will place all the generated files in ``blog/deploy``. You can then take
that directory and upload it to your server.

Installation
-------------------------------------------------------------------------------

::

    git clone https://github.com/honza/socrates.git
    cd socrates
    virtualenv env --no-site-packages
    source env/bin/activate
    pip install -r requirements.txt
    # If you want to use Django templates...
    pip install django
    # If you want to use Jinja2 templates...
    pip install jinja2

Config.yaml
-------------------------------------------------------------------------------

In the pre-generated ``config.yaml`` all the values are required. You can add
as many values to that file and they will be available in the templates'
context.

Themes
-------------------------------------------------------------------------------

Socrates supports Django templates and Jinja2 templates. You can specify which
templating engine you wish to use in the ``config.yaml`` file. There are two
basic themes in the ``themes`` directory to get you started.

Text to HTML
-------------------------------------------------------------------------------

Socrates will attemp to convert your text files into HTML using a text
processor. You should specify the name of the text processor in
``config.yaml``. It should be all lowercase. Currently supported processors:

  - Markdown
  - Textile
  - reStructuredText
  - HTML (unmodified text)

To install a text processor, run one of the following::

    $ pip install markdown
    $ pip install textile
    $ pip install docutils # reStructuredText

Development
-------------------------------------------------------------------------------

You can start a simple development server to aid you in development.::

    python socrates.py -r blog

License
-------------------------------------------------------------------------------

Socrates is licensed under the terms of the 3-clause BSD license.

Contribute
-------------------------------------------------------------------------------

All contributions are welcome. 

Bugs & Issues
-------------------------------------------------------------------------------

Please report all bugs on Github.

Authors
-------------------------------------------------------------------------------

Socrates was originally written by Honza Pokorny.
