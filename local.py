#!/usr/bin/python

"""OGRe Location Query Handler"""

import json
from twython import Twython
from ogre.credentials import *


def get(sources, coordinate, radius, unit="km", kinds=("any",), keyword=""):
    """Retrieve local multimedia and return a JSON dictionary.

    sources    -- tuple of sources to get content from
    coordinate -- 2-tuple containing a latitude and a longitude
    radius     -- number of units that defines "local"
    unit       -- metric used to measure distance
    kinds      -- tuple of content mediums to get
    keyword    -- term to search for

    """
    unit = unit.lower()
    valid_units = ("km", "mi")
    if unit not in valid_units:
        print "invalid unit", unit
        return
    if len(coordinate) is not 2:
        print "invalid coordinate"
        return

    valid_kinds = ("any", "image", "sound", "text", "video")
    for kind in kinds:
        if kind.lower() not in valid_kinds:
            print "invalid kind", kind
            return
    source_dict = {"twitter": _twitter}
    for source in sources:
        source = source.lower()
        if source not in source_dict.keys():
            print "invalid source", source
        else:
            source_dict[source](coordinate[0], coordinate[1], radius, unit,
                                kinds, keyword)

    # TODO Return concatenated results.


def _twitter(latitude, longitude, radius, unit="km",
             kinds=("any",), keyword=""):
    """Access tweets relative to a location from the Twitter API.

    latitude  -- number from -90.0 to 90.0
    longitude -- number from -180.0 to 180.0
    radius    -- max number of units from the coordinate
    unit      -- metric used to measure distance
    kinds     -- tuple of content mediums to get
    keyword   -- term to search for

    """
    twitter = Twython(TWITTER_CONSUMER_KEY, access_token=TWITTER_ACCESS_TOKEN)
    geocode = str(latitude)+","+str(longitude)+","+str(radius)+unit
    results = twitter.search(q=keyword, geocode=geocode)
    # TODO Narrow results by kind.
    print json.dumps(results, indent=4, separators=(",", ": "))
    # TODO Extract only desired information from the results.
