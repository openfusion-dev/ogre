#!/usr/bin/env python
# coding: utf-8

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    README = readme_file.read()

setup(
    name="OGRe",
    version='4.5.1',
    description='OpenFusion GeoJSON Retriever',
    long_description=README,
    author='David Tucker',
    author_email='dmtucker@ucsc.edu',
    license='GPL',
    url='https://github.com/dmtucker/ogre',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    test_suite="ogre.test",
    tests_require=['mock==1.0.1'],
    install_requires=['twython'],
    entry_points={'console_scripts': ['ogre = ogre.__main__:main']},
    keywords='OpenFusion Twitter GeoJSON geotag',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
    ],
)
