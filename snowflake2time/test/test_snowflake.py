#!/usr/bin/env python
# Twitter Snowflake ID to timestamp (and back)
# https://github.com/client9/snowflake2time/
# Nick Galbreath @ngalbreath nickg@client9.com
# Public Domain -- no copyright -- but be kind and give credit
#

import unittest

import snowflake2time.snowflake as snowflake


class SnowflakeTest(unittest.TestCase):
    def test_str2utc(self):
        stamp = snowflake.str2utc("Mon May 21 22:16:35 +0000 2012")
        self.assertEquals(stamp, 1337638595)

    def test_snowflake2utc(self):
        utc = snowflake.snowflake2utc(204697221847986177)
        self.assertEquals(int(utc), int(1337638595.44))

    def test_snowflake2utcms(self):
        utc = snowflake.snowflake2utcms(204697221847986177)
        # danger floating point maths
        self.assertAlmostEqual(utc, 1337638595436)

    def test_diff(self):
        diff = snowflake.snowflake2utcms(204697221847986177) - snowflake.str2utcms(
            "Mon May 21 22:16:35 +0000 2012",
        )
        self.assertEquals(diff, 436)


if __name__ == "__main__":
    unittest.main()
