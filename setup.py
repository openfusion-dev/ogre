#!/usr/bin/env python3

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    README = readme_file.read()

setup(
    name="OGRe",
    description="OpenFusion GeoJSON Retriever",
    long_description=README,
    long_description_content_type="text/x-rst",
    author="David Tucker",
    author_email="dmtucker@ucsc.edu",
    license="LGPLv2+",
    url="https://github.com/openfusion-dev/ogre",
    packages=find_packages(exclude=["docs"]),
    include_package_data=True,
    python_requires=">= 3.6",
    install_requires=[
        "twython >= 3.4",
    ],
    options={"bdist_wheel": {"universal": True}},
    entry_points={"console_scripts": ["ogre = ogre.cli:main"]},
    keywords="OpenFusion Twitter GeoJSON geotag",
    classifiers=[
        "License :: OSI Approved"
        " :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 5 - Production/Stable",
    ],
)
