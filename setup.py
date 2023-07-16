#!/usr/bin/env python3

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import glob
import os.path

from setuptools import setup, find_packages  # type: ignore

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
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob.glob("src/*.py")
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    python_requires=">= 3.8",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
    ],
)
