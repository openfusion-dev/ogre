"""
OpenFusion GeoJSON Retriever

:mod:`ogre.api` -- module for getting data from public APIs

:mod:`ogre.Twitter` -- module for getting data from Twitter

:mod:`ogre.validation` -- module for parameter validation and sanitation
"""

import importlib.metadata

from ogre.api import OGRe


__all__ = [
    "__version__",
    "OGRe",
]
__version__ = importlib.metadata.version("ogre")
