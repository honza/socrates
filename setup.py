from setuptools import setup

description = 'Socrates is a simple static site generator.'
long_desc = open('README.rst').read()

setup(
    name='socrates',
    version='0.9.1',
    url='http://honza.github.com/socrates/',
    install_requires=[
        'PyYAML==3.11',
        'misaka==2.0.0',
        'Django==1.8.6',
        'Jinja2==2.8',
        'docutils==0.12',
        'Pygments==2.0.2',
        'textile==2.2.2'
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
