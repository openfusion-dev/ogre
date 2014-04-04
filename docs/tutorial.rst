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
To find Tweets posted within 1km of Twitter headquarters, use::

 retriever.get(
     ('Twitter',),
     keyword='',
     what=('text',),
     where=(37.781157, -122.398720, 1, 'km')
 )

.. note:: Either a keyword or constraints are required.

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
