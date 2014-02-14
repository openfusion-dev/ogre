#!/usr/bin/python

"""OGRe Location Query Handler"""

import json
from twython import Twython
from ogre.credentials import TWITTER_CONSUMER_KEY, TWITTER_ACCESS_TOKEN


def get(sources, keyword="", constraints=None, kinds=("any",)):
    """Retrieve multimedia from a public source and return a JSON dictionary.

    sources     -- tuple of sources to get content from
    keyword     -- term to search for
    constraints -- dictionary of search parameters
        The following keys are currently supported:
        "location": 4-tuple containing latitude, longitude, radius, and unit,
                    respectively. "km" and "mi" are supported unit metrics.
        "time"    : 2-tuple containing earliest and latest times, respectively
                    (specified in seconds from Epoch)
    kinds       -- tuple of content mediums to get

    """
    if keyword is "" and constraints is None:
        print "Either a keyword or constraints must be specified."
        return
    for kind in kinds:
        if kind.lower() not in ("any", "image", "sound", "text", "video"):
            print kind, "is an invalid kind."
            return
    coordinate = None
    window = None
    for constraint in constraints.keys():
        if constraint.lower() == "location":
            if len(constraints[constraint]) is not 4:
                print "The location constraint is malformed."
                return
            elif (constraints[constraint][0] < -90 or
                  constraints[constraint][0] > 90):
                print constraints[constraint][0], "is an invalid latitude."
                return
            elif (constraints[constraint][1] < -180 or
                  constraints[constraint][1] > 180):
                print constraints[constraint][0], "is an invalid longitude."
                return
            elif constraints[constraint][2] < 0:
                print constraints[constraint][2], "is an invalid radius."
                return
            elif constraints[constraint][3] not in ("km", "mi"):
                print constraints[constraint][3], "is an invalid unit."
                return
            else:
                coordinate = constraints[constraint]
        elif constraint.lower() == "time":
            if len(constraints[constraint]) is not 2:
                print "The time constraint is malformed."
                return
            elif constraints[constraint][0] < 0:
                print constraints[constraint][0], "is an invalid window start."
                return
            elif constraints[constraint][1] < 0:
                print constraints[constraint][1], "is an invalid window end."
                return
            else:
                if constraints[constraint][0] > constraints[constraint][1]:
                    window = (constraints[constraint][1],
                              constraints[constraint][0])
                else:
                    window = constraints[constraint]
        else:
            print constraint, "is an invalid constraint."
            return

    source_map = {"twitter": _twitter}
    for source in sources:
        source = source.lower()
        if source not in source_map.keys():
            print source, "is an invalid source."
            return
        else:
            source_map[source](keyword, coordinate, window, kinds)
    # TODO Concatenate results and return them.


def _twitter(keyword="", coordinate=None, window=None, kinds=("any",)):
    """Access tweets relative to a location from the Twitter API.

    keyword    -- term to search for
    coordinate -- 4-tuple containing latitude, longitude, radius, and unit,
                  respectively. "km" and "mi" are supported unit metrics.
    window     -- 2-tuple containing earliest and latest times, respectively
                  (specified in seconds from Epoch)
    kinds      -- tuple of content mediums to get

    """
    twitter = Twython(TWITTER_CONSUMER_KEY, access_token=TWITTER_ACCESS_TOKEN)
    location =\
        str(coordinate[0])+"," +\
        str(coordinate[1])+"," +\
        str(coordinate[2])+coordinate[3]
    # TODO Figure out how Twitter does time-relative searches.
    # TODO Convert window to Twitter query format.
    results = twitter.search(q=keyword, geocode=location)
    # TODO Narrow results by kind.
    print json.dumps(results, indent=4, separators=(",", ": "))
    # TODO Extract only desired information from the results.
