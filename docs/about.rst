About
=====
OGRe is a component of a larger project called OpenFusion that aims at gathering
crowdsourced data to produce useful visualizations.

OpenFusion
----------
Development began for a "Geotagged Sensor Fusion" idea in late 2013 as a
Senior Design project at the University of California at Santa Cruz with
sponsorship from Lawrence Livermore National Laboratory. There are currently 3
other components to the project including an iOS application, a visualizer, and
a web application to unify each piece.

Mobile Data Logger
~~~~~~~~~~~~~~~~~~
The mobile data collection suite consists of a series of sensors. To supplement
the sensors in the iPhone such as the camera, microphone, and GPS receiver,
students developed a pluggable device with an onboard temperature sensor,
humidity sensor, and barometric pressure sensor.

.. note:: The iOS application uses OpenCV to detect people and faces in photos.

The external sensors connect to an iPhone via the 3.5mm headset jack, and relay
measurements with the help of a microcontroller. So far, an iPhone 4S and an
iPhone 5S have been used to upload gathered data to the OpenFusion web
application via a publicly-accessible API.

.. seealso:: https://github.com/mbaptist23/open-fusion-iOS

User Interface
~~~~~~~~~~~~~~
Mobile devices upload geotagged data to the web application where it
is stored in a database for later retrieval. OpenFusion coordinates uploads and
programmatic downloads through a public REST API.

.. seealso:: https://github.com/bkeyoumarsi/open-fusion-webapp

Users may access the project online using their favorite browser or mobile
device. There they can query the database of measurements and use it to create
fusions with data from other sources such as Twitter. Some examples queries
include:

 - What images were posted in Times Square when the temperature was 50 degrees?
 - What was posted within 1 kilometer of any Tweet mentioning Barack Obama?
 - What posts mentioning the Super Bowl were posted within 5 minutes of a
   humidity measurement of 50%?

.. seealso:: https://gsf.soe.ucsc.edu/

Visualizer
~~~~~~~~~~
After a query is run, the web application uses OGRe to collect relevant data
from public sources. It hands off the results it receives to a client-side
visualizer called Vizit which plots points on a map or timeline.

.. note:: Vizit uses OpenStreetMap and Leaflet to create map visualizations,
          and it creates timelines with D3.

Vizit is capable of rendering any GeoJSON file that it retrieves via AJAX;
however, it was designed to specialize in GeoJSON files specifically made by the
OpenFusion project.

.. seealso:: https://github.com/dmtucker/vizit
