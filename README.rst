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

    $ socrates -i blog

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

    $ socrates -g blog

This will place all the generated files in ``blog/deploy``. You can then take
that directory and upload it to your server.

Installation
-------------------------------------------------------------------------------

First, set up your virtual environment and pip install Socrates.

::

    virtualenv env --no-site-packages
    source env/bin/activate
    pip install -e git://github.com/honza/socrates.git#egg=socrates

The next step is to install your templates. At the moment, you can choose
between `Django templates`_ and `Jinja2 templates`_. The default theme uses
Django.

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

By default, Socrates only installs the Markdown text processors. You can
install the others with pip::

    $ pip install textile
    $ pip install docutils

Development
-------------------------------------------------------------------------------

You can start a simple development server to aid you in development.::

    $ socrates -r blog

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

.. _Django templates: https://docs.djangoproject.com/en/1.3/#the-template-layer
.. _Jinja2 templates: http://jinja.pocoo.org/docs/
