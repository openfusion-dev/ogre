"""OGRe Query Handler Test"""

import base64
import json
import os
import unittest
import urllib
from datetime import datetime
from mock import MagicMock, call
from snowflake2time import snowflake
from ogre import OGRe


class OGReTest (unittest.TestCase):

    """Create objects that test the OGRe module."""

    def setUp(self):
        """Prepare to run tests on OGRe.

        Since OGRe requires API keys to run and they cannot be stored
        conveniently, this test module retrieves them from the OS environment.
        Also, to prevent OGRe from actually querying the APIs
        (and subsequently retrieving unpredictable data), a MagicMock object
        is used to do a dependency injection, and predictable results are
        stored in the data directory to be read during these tests.

        """
        self.retriever = OGRe({
            "Twitter": {
                "consumer_key": os.environ.get("TWITTER_CONSUMER_KEY"),
                "access_token": os.environ.get("TWITTER_ACCESS_TOKEN")
            }
        })
        self.api = MagicMock()
        with open("ogre/test/data/Twitter-response-example.json") as tweets:
            self.tweets = json.load(tweets)

    def test_get(self):
        """Test the main entry point to OGRe.

        These tests should make sure all input in validated correctly,
        and they should ensure that the retrieved results are packaged
        in a GeoJSON FeatureCollection object properly.

        """
        with self.assertRaises(TypeError):
            self.retriever.get()
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",))
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"nonexistent": "invalid"})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"what": ("invalid",)})
        with self.assertRaises(AttributeError):
            self.retriever.get(("Twitter",), "", {"what": (1,)})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"when": ("malformed",)})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"when": "xx"})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"when": (-1, 1)})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"when": (1, -1)})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": ("malformed",)})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": "four"})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": (-100, 0, 0, "km")})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": (100, 0, 0, "km")})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": (0, -200, 0, "km")})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": (0, 200, 0, "km")})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": (0, 0, -1, "km")})
        with self.assertRaises(ValueError):
            self.retriever.get(("Twitter",), "", {"where": (0, 0, 0, "ly")})
        with self.assertRaises(AttributeError):
            self.retriever.get(("Twitter",), "", {"where": (0, 0, 0, 0)})
        with self.assertRaises(ValueError):
            self.retriever.get(("invalid",), "test")
        self.assertEqual(self.retriever.get((), "test"), {
            "type": "FeatureCollection",
            "features": []
        })

        self.api.reset_mock()
        self.api().search.return_value = self.tweets
        self.assertEqual(
            self.retriever.get(
                sources=("Twitter",),
                keyword="test",
                constraints={
                    "what": ("image", "text"),
                    "when": (4, 3),  # Verify OGRe switches these automatically.
                    "where": (0, 1, 2, "km")
                },
                api=self.api
            )["features"],
            OGRe._twitter(
                self.retriever.keychain["Twitter"],
                keyword="test",
                locale=(0, 1, 2, "km"),
                period=(3, 4),
                medium=("image", "text"),
                api=self.api
            )
        )
        self.api.reset_mock()

    def test__twitter(self):
        """Test OGRe's access point to the Twitter API.

        These tests should verify any validation that is double-checked
        (assuming that users always access this function through OGRe.get),
        and it should make sure that any relevant Twitter data is extracted
        and packaged in GeoJSON format correctly.

        The first two Tweets in the example Twitter response data
        must be geotagged, and the first one must contain an image.
        If any other geotagged data is included, this test will fail;
        however, it is a good idea to include non-geotagged Tweets
        to ensure that OGRe omits them in the returned results.

        """
        with self.assertRaises(ValueError):
            self.assertEqual(
                OGRe._twitter(self.retriever.keychain["Twitter"]),
                None
            )
        self.assertEqual(
            OGRe._twitter(self.retriever.keychain["Twitter"], medium=()),
            []
        )

        self.api.reset_mock()
        self.assertEqual(
            OGRe._twitter(
                self.retriever.keychain["Twitter"],
                keyword="test",
                locale=(0, 1, 2, "km"),
                period=(3, 4),
                medium=("image", "text"),
                api=self.api
            ),
            []
        )
        self.api.assert_called_once_with(
            self.retriever.keychain["Twitter"]["consumer_key"],
            access_token=self.retriever.keychain["Twitter"]["access_token"]
        )
        self.api().search.assert_called_once_with(
            q="test",
            count=100,
            geocode="0,1,2km",
            since_id=-5405765676960841728,
            max_id=-5405765672766537728
        )
        self.api.reset_mock()
        self.api().search.return_value = self.tweets
        self.assertEqual(
            OGRe._twitter(
                self.retriever.keychain["Twitter"],
                keyword="test",
                locale=(0, 1, 2, "km"),
                period=(3, 4),
                medium=("image", "text"),
                api=self.api
            ),
            [
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            self.tweets["statuses"][0]
                                ["coordinates"]["coordinates"][0],
                            self.tweets["statuses"][0]
                                ["coordinates"]["coordinates"][1],
                        ]
                    },
                    "type": "Feature",
                    "properties": {
                        "source": "Twitter",
                        "text": self.tweets["statuses"][0]["text"],
                        "image": base64.b64encode(urllib.urlopen(
                            self.tweets["statuses"][0]
                                ["entities"]["media"][0]["media_url"]
                        ).read()),
                        "timestamp": datetime.utcfromtimestamp(
                            snowflake.snowflake2utc(
                                self.tweets["statuses"][0]["id"]
                            )
                        ).isoformat()+"Z"
                    }
                },
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            self.tweets["statuses"][1]
                                ["coordinates"]["coordinates"][0],
                            self.tweets["statuses"][1]
                                ["coordinates"]["coordinates"][1],
                        ]
                    },
                    "type": "Feature",
                    "properties": {
                        "source": "Twitter",
                        "text": self.tweets["statuses"][1]["text"],
                        "timestamp": datetime.utcfromtimestamp(
                            snowflake.snowflake2utc(
                                self.tweets["statuses"][1]["id"]
                            )
                        ).isoformat()+"Z"
                    }
                }
            ]
        )
        self.api.reset_mock()


if __name__ == "__main__":
    unittest.main()
