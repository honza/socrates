Installation
============

First, set up your virtual environment and pip install Socrates.

.. code-block:: console

    virtualenv env --no-site-packages
    source env/bin/activate
    pip install -e git://github.com/honza/socrates.git#egg=socrates

The next step is to install your templates. At the moment, you can choose
between `Django templates`_ and `Jinja2 templates`_. The default theme uses
Django.

.. code-block:: console

    pip install django
    pip install jinja2

If you're going to use a processor other than Markdown, you have to install
that, too.

textile

.. code-block:: console

    pip install textile

reStructuredText

.. code-block:: console

    pip install docutils pygments

.. _Django templates: https://docs.djangoproject.com/en/1.3/#the-template-layer
.. _Jinja2 templates: http://jinja.pocoo.org/docs/
