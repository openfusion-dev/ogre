#!/usr/bin/env python

from distutils.core import setup
from ogre.__init__ import __version__

setup(
    name="OGRe",
    version=__version__,
    description="OpenFusion GIS Retriever",
    author="David Tucker",
    author_email="dmtucker@ucsc.edu",
    url="https://github.com/dmtucker/ogre",
    packages=["ogre"],
    requires=["twython>=3.1.2"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
    ]
)
