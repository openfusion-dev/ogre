About
=====
OGRe is a component of a larger project called OpenFusion that aims to gather
crowdsourced data and produce useful visualizations from it.

OpenFusion
----------
Development began for a "Geotagged Sensor Fusion" idea in late 2013 as a
Senior Design project at the University of California at Santa Cruz with
sponsorship from Lawrence Livermore National Laboratory.
There are currently 4 components to the project including
a mobile data logger, a web application, a retriever, and a visualizer.
Some examples of questions this project tries to answer are listed below.

 - What images were posted in Times Square when the temperature was 50 degrees?
 - What was posted within 1 kilometer of any Tweet mentioning Barack Obama?
 - What posts mentioning the Super Bowl were created within 5 minutes of a
   humidity measurement of 50%?

.. seealso:: https://gsf.soe.ucsc.edu/

Mobile Data Logger
~~~~~~~~~~~~~~~~~~
The mobile data collection suite consists of a series of sensors and
a mobile application. In addition to utilizing sensors common in mobile devices
(i.e. the camera, microphone, and GPS receiver), students developed a
pluggable device with onboard sensors. The external sensors connect to via a
3.5mm headset jack and relay measurements using a microcontroller.
Gathered data then gets transmitted to the OpenFusion web application.

.. note:: Currently, only the iPhone 4S and 5S are officially supported.

.. seealso:: https://github.com/mbaptist23/open-fusion-iOS

Web Application
~~~~~~~~~~~~~~~
Mobile devices upload geotagged data to the web application where it is stored
in a database for later retrieval. OpenFusion coordinates programmatic uploads
and downloads through a public REST API. Users may access a deployment of the
web application online using their favorite browser. There, they can query the
database of measurements and use it to create fusions with data from other
sources.

.. seealso:: https://github.com/bkeyoumarsi/open-fusion-webapp

Retriever
~~~~~~~~~
The web application uses a retriever called OGRe to collect relevant data from
public sources such as Twitter. It merges the results with gathered data and
writes the combined set to a GeoJSON file that gets handed off to the
visualizer.

.. seealso:: https://github.com/openfusion-dev/ogre

Visualizer
~~~~~~~~~~
After a query is run, a client-side visualizer called Vizit fetches data from
the web application via AJAX and plots it on a map or timeline.
Vizit is capable of rendering any GeoJSON file, and it supports a number of
special properties to affect the resulting visualization.

.. seealso:: https://github.com/openfusion-dev/vizit
