Tutorial
========
Follow this simple guide to quickly get started using OGRe.

Installation
------------
To get OGRe, use one of the following methods:

1. pip_ *(recommended)*

.. _pip: http://www.pip-installer.org/en/latest/

.. code-block:: bash

   $ pip install ogre

2. easy_install_

.. _easy_install: https://pypi.python.org/pypi/setuptools

.. code-block:: bash

   $ easy_install ogre

3. git_

.. _git: http://git-scm.com/

.. code-block:: bash

   $ git clone http://github.com/dmtucker/ogre.git
   $ cd ogre
   $ python setup.py install

Usage
-----
To use OGRe, you must import it into your module::

 from ogre import OGRe

Next, create an OGRe instance with your API credentials::

 retriever = OGRe({
     'Twitter': {
         'consumer_key': 'xxxxxxxxxxxxxxxxxxxxxx',
         'access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' +
                         'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' +
                         'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' +
                         'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
     }
 })

Finally, make queries using the `.get` method.

Example
~~~~~~~
To find Tweets with images posted within 1km of Twitter headquarters, use::

 retriever.get(
     ('Twitter',),
     keyword='',
     constraints={
         'what': ('image',),
         'where': (37.781157, -122.398720, 1, 'km')
     }
 )

.. note:: Either a keyword or constraints are required.
