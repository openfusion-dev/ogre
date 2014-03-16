"""OGRe Location Query Handler"""

import base64
import urllib
from datetime import datetime
from warnings import warn

from twython import Twython
from snowflake2time.snowflake import *
from ogre.credentials import TWITTER_CONSUMER_KEY, TWITTER_ACCESS_TOKEN


def get(sources, keyword="", constraints=None):
    """Retrieve multimedia from a public source and return a JSON dictionary.

    sources     -- tuple of sources to get content from
    keyword     -- term to search for
    constraints -- dictionary of search parameters
        The following keys are currently supported:
        "where" : 4-tuple containing latitude, longitude, radius, and unit.
                  "km" and "mi" are supported units.
        "when"  : 2-tuple containing earliest and latest moments.
                  Moments must be specified in Unix time.
        "what"  : tuple of content mediums to get
                  "image", "sound", "text", and "video" are supported mediums.

    """
    if keyword is "" and constraints is None:
        raise ValueError("Either a keyword or constraints must be specified.")

    locale = None
    period = None
    medium = []
    if constraints is not None:
        for constraint in constraints.keys():

            if constraint.lower() == "where":
                if len(constraints[constraint]) != 4:
                    raise ValueError(
                        'usage: {"where": (latitude, longitude, radius, unit)}'
                    )
                latitude = float(constraints[constraint][0])
                if latitude < -90 or latitude > 90:
                    raise ValueError("Latitude must be between -90 and 90.")
                longitude = float(constraints[constraint][0])
                if longitude < -180 or longitude > 180:
                    raise ValueError("Longitude must be between -180 and 180.")
                radius = float(constraints[constraint][2])
                if radius < 0:
                    raise ValueError("Radius must be positive.")
                unit = constraints[constraint][3].lower()
                if unit not in ("km", "mi"):
                    raise ValueError('Unit must be "km" or "mi".')
                locale = constraints[constraint]

            elif constraint.lower() == "when":
                if len(constraints[constraint]) != 2:
                    raise ValueError(
                        'usage: {"when": (earliest, latest)}'
                    )
                since = float(constraints[constraint][0])
                until = float(constraints[constraint][1])
                if since < 0 or until < 0:
                    raise ValueError("Moments must be specified in Unix time.")
                if since > until:
                    period = (until, since)
                else:
                    period = constraints[constraint]

            elif constraint.lower() == "what":
                for kind in constraints[constraint]:
                    if kind.lower() not in ("image", "sound", "text", "video"):
                        raise ValueError(
                            "Medium may be " +\
                            '"image", "sound", "text", or "video".'
                        )
                    medium.append(kind.lower())

            else:
                raise ValueError(
                    'Constraint may be "where", "when", or "what".'
                )
    if not medium:
        medium = ("image", "sound", "text", "video")

    feature_collection = {
        "type": "FeatureCollection",
        "features": []
    }
    source_map = {"twitter": _twitter}
    for source in sources:
        source = source.lower()
        if source not in source_map.keys():
            print source, "is an invalid source."
            print "Twitter is currently the only supported source."
            return
        else:
            for feature in source_map[source](keyword, locale, period, medium):
                feature_collection["features"].append(feature)
    return feature_collection


def _twitter(keyword="", locale=None, period=None, medium=("image", "text")):
    """Access Tweets from the Twitter API and return a list.

    keyword -- term to search for
    locale  -- 4-tuple containing latitude, longitude, radius, and unit.
               "km" and "mi" are supported units.
    period  -- 2-tuple containing earliest and latest moments.
               Moments must be specified in Unix time.
    medium  -- tuple of content mediums to get
               "image" and "text" are supported mediums.

    """
    media = []
    for kind in medium:
        if kind.lower() in ("image", "text"):
            media.append(kind.lower())
    if not media:
        return None
    media = list(set(media))
    if media == ["image"]:
        keyword += "  pic.twitter.com"
    elif media == ["text"]:
        keyword += " -pic.twitter.com"

    coordinate = None
    if locale is not None:
        coordinate =\
            str(locale[0])+","+str(locale[1])+","+str(locale[2])+locale[3]

    since = None
    until = None
    if period is not None:
        since = utc2snowflake(period[0])
        until = utc2snowflake(period[1])

    twitter = Twython(TWITTER_CONSUMER_KEY, access_token=TWITTER_ACCESS_TOKEN)
    results = twitter.search(q=keyword.strip(),
                             count=100,
                             geocode=coordinate,
                             since_id=since,
                             max_id=until)

    collection = []
    for tweet in results["statuses"]:
        if tweet["coordinates"] is None:
            continue
        feature = {
            "type": "Feature",
            "geometry": tweet["coordinates"],
            "properties": {
                "source": "Twitter",
                "timestamp": datetime.utcfromtimestamp(
                    snowflake2utc(tweet["id"])
                ).isoformat()+"Z"
            }
        }

        if "text" in media:
            feature["properties"]["text"] = tweet["text"]
        if "image" in media:
            if ("media" in tweet["entities"] and
                    tweet["entities"]["media"] is not None):
                for entity in tweet["entities"]["media"]:
                    if entity["type"] == "photo":
                        feature["properties"]["image"] = base64.b64encode(
                            urllib.urlopen(entity["media_url"]).read()
                        )
                    else:
                        warn('New type "'+entity["type"]+'" detected.')
        collection.append(feature)

    return collection
