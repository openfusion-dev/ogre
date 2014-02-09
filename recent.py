#!/usr/bin/python

"""OGRe Time Query Handler"""

import json
from twython import Twython
from ogre.credentials import *


def get(sources, window, kinds=("any",), keyword=""):
    """Retrieve recent multimedia and return a JSON dictionary.

    sources -- tuple of sources to get content from
    window  -- 2-tuple of
    kinds   -- tuple of content mediums to get
    keyword -- term to search for

    """
    if len(window) is not 2:
        print "invalid window"
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
            source_dict[source](window[0], window[1], kinds, keyword)
    pass  # TODO Call the appropriate handler based on parameters.
    return


def _twitter(after, before, kinds=("any",), keyword=""):
    """Access tweets made in a given window of time from the Twitter API.

    after   -- number of seconds since the Epoch
               representing the maximum age of content to get
    before  -- number of seconds since the Epoch
               representing the minimum age of content to get
    kinds   -- tuple of content mediums to get
    keyword -- term to search for

    """
    twitter = Twython(TWITTER_CONSUMER_KEY, access_token=TWITTER_ACCESS_TOKEN)
    pass  # TODO Implement this function.
    return
