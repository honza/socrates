Configuration
=============

This is a reference for your blog's main configuration file. Any values that
you add in there will be made available in your templates' context.

.. option:: author

    Blog author. Defaults to `author`.

.. option:: site_name

    Site name. Defaults to `Socrates site`.

.. option:: posts_per_page

    Number of posts displayed per page. Used for pagination. Defaults to `10`.
    Setting this to `0` will display all posts on one page.

.. option:: url

    Your site's URL. Defaults to `http://example.com`.

.. option:: date_format

    Python strftime formatted date format. Defaults to `%B %d, %Y`.

.. option:: text_processor

    Which X to html processor to use; *markdown*, *textile*, *rst*, *html*,
    *extension*. Defaults to `markdown`. The 'extension' setting will decide on
    the processor to be used based on the post's file extension:

    * Markdown
        + .md
        + .markdown
        + .mkdn
    * reStructuredText
        + .rst
    * HTML
        + .html
        + .htm
        + .txt
    * Textile
        + .textile

.. option:: templates

    'django' or 'jinja2'. Defaults to `django`.

.. option:: append_slash

    Whether a slash should be appended to post urls. Defaults to `true`.

.. option:: url_include_day

    Whether to include the day with the month and year in the generated
    directories and urls. Defaults to `false`.

.. option:: initial_header_level

    By default, the first heading in your document will be ``<h2>``. Only
    available for reStructuredText posts. Defaults to `2`.

.. option:: skip_archives

    If set to `true`, it won't bother generating archives. Defaults to `false`.

.. option:: skip_categories

    If set to `true`, it won't bother generating categories. Defaults to
    `false`.

.. option:: pygments

    Additional settings for the Pygments HTML Parser. It passes the arguments
    directly to the ``HtmlFormatter`` class when it's instanciated, so these
    settings include all of the available settings for ``HtmlFormatter``

    sample:

    .. code-block:: yaml

        pygments:
            linenos: true
            noclasses: false
            style: 'pastie'


    .. option:: style
        
        The style option has many default built in styles for your code blocks.
        The ones that ship with Pygments are: ``monokai``, ``manni``, ``perldoc``,
        ``borland``, ``colorful``, ``default``, ``murphy``, ``vs``, ``trac``, 
        ``tango``, ``fruity``, ``autumn``, ``bw``, ``emacs``, ``vim``, 
        ``pastie``, ``friendly``, ``native``

.. option:: inline_css

    Whether or not you want pygments to output a ``pygments.css`` file in your
    build directory for css. If set to ``false`` it will output the file.

