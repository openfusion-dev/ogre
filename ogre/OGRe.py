"""OGRe Query Handler

:class:`OGRe` -- retriever object template

    The following methods are currently exported:
     - :func:`OGRe.get` : method for making a retriever fetch data

"""

import base64
import urllib
from datetime import datetime
from warnings import warn
from twython import Twython
from snowflake2time.snowflake import *


class OGRe:

    """Create objects that contain API keys and API access points.

    A class is necessary here to avoid requiring API keys with every API call.
    Since this is a library meant for developers, it didn't seem appropriate to
    use a configuration file. Also, importing the keys from the OS environment
    subjects them to data leak to other processes. This way developers are
    responsible for keeping their keys safe. Twython, the Twitter API wrapper,
    also uses this scheme.

    :func:`get` -- method for retrieving data from a public source

    """

    def __init__(self, keys):
        """Instantiate an OGRe.

        keys -- dictionary of dictionaries containing
                API keys for supported public sources
                supported sources: Twitter

        """
        self.keychain = keys

    def get(self, sources, keyword="", constraints=None, api=None):

        """Retrieve multimedia from a public API and return a JSON dictionary.

        :param sources: public APIs to get content from (required)
        :type sources: tuple

        :param keyword: term to search for
        :type keyword: str

        :param constraints: search parameters
        :type constraints: dict

        .. versionchanged:: 4.0.0
           These will soon be kwargs instead of keys!

        The following keys are currently supported:

         - "where" : 4-tuple containing latitude, longitude, radius, and unit.
             - "km" and "mi" are supported units.
         - "when"  : 2-tuple containing earliest and latest moments.
             - Moments must be specified in Unix time.
         - "what"  : tuple of content mediums to get
             - supported mediums: "image", "sound", "text", and "video"

        .. versionadded:: 4.0.0

        :param what: content mediums to get ("image", "sound", "text", or "video")
        :type what: tuple

        :param when: earliest and latest moments (POSIX timestamps)
        :type when: tuple

        :param where: latitude, longitude, radius, and unit ("km" or "mi")
        :type where: tuple

        Those will replace the `constraints` parameter.

        :param api: API access point (used for testing)
        :type api: callable

        :raises: AttributeError, ValueError

        :returns: GeoJSON FeatureCollection
        :rtype: dict

        """

        # TODO Verify Twitter accepts any constraint instead of a keyword.
        if keyword is "" and constraints is None:
            raise ValueError("Specify either a keyword or constraints.")

        locale = None
        period = None
        medium = []
        if constraints is not None:
            for constraint in constraints.keys():
                if constraints[constraint] is None:
                    continue
                elif constraint.lower() == "what":
                    for kind in constraints[constraint]:
                        if kind.lower() not in (
                            "image",
                            "sound",
                            "text",
                            "video"
                        ):
                            raise ValueError(
                                "Medium may be " +
                                '"image", "sound", "text", or "video".'
                            )
                        if kind.lower() not in medium:
                            medium.append(kind.lower())
                elif constraint.lower() == "when":
                    if len(constraints[constraint]) != 2:
                        raise ValueError('usage: {"when": (earliest, latest)}')
                    since = float(constraints[constraint][0])
                    until = float(constraints[constraint][1])
                    if since < 0 or until < 0:
                        raise ValueError("Moments must be POSIX timestamps.")
                    if since > until:
                        since, until = until, since
                    period = (since, until)
                elif constraint.lower() == "where":
                    if len(constraints[constraint]) != 4:
                        raise ValueError(
                            "usage:" +
                            '{"where": (latitude, longitude, radius, unit)}'
                        )
                    latitude = float(constraints[constraint][0])
                    if latitude < -90 or latitude > 90:
                        raise ValueError("Latitude must be -90 to 90.")
                    longitude = float(constraints[constraint][1])
                    if longitude < -180 or longitude > 180:
                        raise ValueError("Longitude must be -180 to 180.")
                    radius = float(constraints[constraint][2])
                    if radius < 0:
                        raise ValueError("Radius must be positive.")
                    unit = constraints[constraint][3].lower()
                    if unit not in ("km", "mi"):
                        raise ValueError('Unit must be "km" or "mi".')
                    locale = (latitude, longitude, radius, unit)
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
        source_map = {"twitter": OGRe._twitter}
        for source in sources:
            source = source.lower()
            if source not in source_map.keys():
                raise ValueError('Source may be "Twitter".')
            else:
                for feature in source_map[source](
                    self.keychain["Twitter"],
                    keyword,
                    locale,
                    period,
                    medium,
                    api
                ):
                    feature_collection["features"].append(feature)
        return feature_collection

    @staticmethod
    def _twitter(
            keys,
            keyword="",
            locale=None,
            period=None,
            medium=("image", "text"),
            api=None
    ):

        """Access Tweets from the Twitter API and return a list.

        keys    -- dictionary containing an API key and an access token
                   required keys: "consumer_key" and "access_token"
        keyword -- term to search for
        locale  -- 4-tuple containing latitude, longitude, radius, and unit.
                   "km" and "mi" are supported units.
        period  -- 2-tuple containing earliest and latest moments.
                   Moments must be specified in Unix time.
        medium  -- tuple of content mediums to get
                   "image" and "text" are supported mediums.
        api     -- API access point (used for dependency injection)

        """

        media = []
        for kind in medium:
            if kind.lower() in ("image", "text"):
                media.append(kind.lower())
        if not media:
            return []
        media = list(set(media))
        if media == ["image"]:
            keyword += "  pic.twitter.com"
        elif media == ["text"]:
            keyword += " -pic.twitter.com"

        # TODO Verify Twitter accepts keyword="", medium=(text,) with a period.
        if keyword is "" and locale is None and period is None:
            raise ValueError("Specify either a keyword or constraints.")

        coordinate = None
        if locale is not None:
            coordinate =\
                str(locale[0])+","+str(locale[1])+","+str(locale[2])+locale[3]

        since = None
        until = None
        if period is not None:
            since = utc2snowflake(period[0])
            until = utc2snowflake(period[1])

        if api is None:
            api = Twython
        twitter = api(
            keys["consumer_key"],
            access_token=keys["access_token"]
        )
        results = twitter.search(
            q=keyword.strip(),
            count=100,
            geocode=coordinate,
            since_id=since,
            max_id=until
        )

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
