Example posts
=============

Here is an example post written in reStructuredText.

.. code-block:: rst

    :title: `How to make a function in Python`
    :date: `2011-07-20 09:00`
    :categories: `Code, Python`

    How to make a function in Python
    ================================

    A function in Python starts with the keyword ``def``, followed by the
    function name and a set of parenthesis.

    .. code-block:: python

        def say_hello():
            ...

    You can read more about this in the `Python manual`_.

    .. _Python manual: http://docs.python.org/tutorial/controlflow.html#defining-functions

And here is the same post in Markdown.

.. code-block:: text

    --------------------------------------------------------------------------
    title: How to make a function in Python
    date: 2011-07-20 09:00:00
    categories:
        - Code
        - Python
    --------------------------------------------------------------------------

    How to make a function in Python
    ================================

    A function in Python starts with the keyword `def`, followed by the
    function name and a set of parenthesis.

        def say_hello():
            ...

    You can read more about this in the [Python manual][1].

    [1]: http://docs.python.org/tutorial/controlflow.html#defining-functions
