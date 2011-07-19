Writing posts
=============

All of your posts will typically be contained in the ``posts`` directory in
your main blog directory. Your post file can be called anything you want, and
as long as you're not mixing and matching different text processors, the
file extension can be anything, too. I use the following naming convetion:

.. code-block:: console

    2011-07-29-name-of-post.rst

This way my posts are automatically ordered by publish date when I run ``ls``
in the ``posts`` directory.

Markdown, textile and HTML
--------------------------

When you're writing your posts in Markdown (or textile or HTML), you need to
add a bit of text to the top of your file to provide Socrates with some
metadata about your post.

.. code-block:: text

    ----------------------------------------------------------------------  
    title: Title of your post
    date: 2011-07-29 13:00:00
    categories:
        - Photos
        - Vacation
    ----------------------------------------------------------------------  

The text between the two horizontal line is written in `YAML`_ syntax. Note
that the horizontal line should have at least 79 characters.

reStructuredText
----------------

If you want to write your post in reStructuredText, you should use the rst
native way to specify document metadata. Include this at the top of your post
file:

.. code-block:: rst

    :title: Title of your post
    :date: 2011-07-29 13:00:00
    :categories: Photos, Vacation

This way, your posts can be processed by the native `Docutils`_ utility
functions such as ``rst2html.py`` or ``rst2latex.py``.

.. _YAML: http://www.yaml.org/ 
.. _Docutils: http://docutils.sourceforge.net/
