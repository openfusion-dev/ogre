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

.. _easy_install: https://pythonhosted.org/setuptools/easy_install.html

.. code-block:: bash

   $ easy_install ogre

3. git_

.. _git: http://git-scm.com/

.. code-block:: bash

   $ git clone http://github.com/dmtucker/ogre.git
   $ cd ogre
   $ python setup.py install

.. note:: This method requires separate installation(s) for dependencies!

Usage
-----
To use OGRe, you must import it into your module::

 from ogre import OGRe

Next, create an OGRe instance with your API credentials::

 retriever = OGRe(
     keys={
         'Twitter': {
             'consumer_key': 'xxxxxxxxxxxxxxxxxxxxxx',
             'access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' +
                             'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' +
                             'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' +
                             'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
         }
     }
 )

Finally, make queries using the `.get` method.

.. note:: "The [Twitter] Search API is not complete index of all Tweets,
          but instead an index of recent Tweets.
          At the moment that index includes between 6-9 days of Tweets."

OGRe may be also be executed directly as shown below.

.. code-block:: bash

   $ python -m ogre

or (if OGRe was installed with pip)

.. code-block:: bash

   $ ogre

As one would expect, API keys are necessary whenever OGRe is run, and they may
be passed one of two ways: the `keys` parameter or via environment variables.
If the latter is preferred, the following table shows what variables are
needed for each source:

+---------+----------------------+
| Source  | Key Variable(s)      |
+=========+======================+
| Twitter | TWITTER_CONSUMER_KEY |
|         | TWITTER_ACCESS_TOKEN |
+---------+----------------------+

Examples
~~~~~~~~
To find 50 image-less Tweets posted within 1km of Twitter headquarters, use::

 retriever.fetch(
     sources=('Twitter',),
     media=('text',),
     keyword='',
     quantity=50,
     location=(37.781157, -122.398720, 1, 'km'),
     interval=None
 )

.. note:: Either a keyword or location are required.

To issue the same query directly from the command line, use the following:

.. code-block:: bash

   $ python -m ogre --keys "{\
   >   'Twitter': {\
   >     'consumer_key': '<Insert Twitter Consumer Key.>',\
   >     'access_token': '<Insert Twitter Access Token.>'\
   >   }\
   > }\
   > --sources Twitter \
   > --media text \
   > --quantity 50 \
   > --location 37.781157 -122.398720 1 km

Alternatively, environment variables are checked when keys are unspecified.

.. code-block:: bash

   $ export TWITTER_CONSUMER_KEY='<Insert Twitter Consumer Key.>'
   $ export TWITTER_ACCESS_TOKEN='<Insert Twitter Access Token.>'
   $ python -m ogre --sources Twitter --media text \
   > --quantity 50 --location 37.781157 -122.398720 1 km

Results return as a single GeoJSON FeatureCollection.
So, the example above could return::

 {
     "type": "FeatureCollection",
     "features": [
         {
             "geometry": {
                 "type": "Point",
                 "coordinates": [
                     -122.3970807,
                     37.77541704
                 ]
             },
             "type": "Feature",
             "properties": {
                 "source": "Twitter",
                 "text": "Sending good thoughts to my babe @annecurtissmith...",
                 "timestamp": "2014-04-04T02:03:28.431000Z"
             }
         },
         {
             "geometry": {
                 "type": "Point",
                 "coordinates": [
                     -122.41160509,
                     37.78093192
                 ]
            },
              "type": "Feature",
             "properties": {
                 "source": "Twitter",
                 "text": "I'm at Huckleberry Bicycles...",
                 "timestamp": "2014-04-04T02:03:13.190000Z"
             }
         },
         ...
     ]
 }

Say we wanted to run the same query and possibly have images returned too.
Additional mediums can be specified with subsequent `media` flags like this:

.. code-block:: bash

   $ python -m ogre \
   > --sources Twitter \
   > --media text --media image \
   > --quantity 50 \
   > --location 37.781157 -122.398720 1 km
