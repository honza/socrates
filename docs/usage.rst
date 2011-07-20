Usage
=====

First, you need to create a new blog:

.. code-block:: console

    $ socrates -i blog

This will create a ``blog`` directory with a simple blog structure:

.. code-block:: console

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

You can also create a new blog in the current working directory::

    $ socrates -i

When you are ready to generate your site, you run:

.. code-block:: console

    $ socrates -g blog

Or, ::

    $ socrates -g

for current directory.

This will place all the generated files in ``blog/deploy``. You can then take
that directory and upload it to your server.
