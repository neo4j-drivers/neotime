#!/usr/bin/env python
# coding: utf-8

# Copyright 2018, Nigel Small & Neo4j
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from datetime import datetime, timedelta
from unittest import TestCase

import pytz

from neotime import DateTime
from neotime.clock import Clock, T


eastern = pytz.timezone("US/Eastern")


class FixedClock(Clock):

    @classmethod
    def available(cls):
        return True

    @classmethod
    def precision(cls):
        return 12

    @classmethod
    def local_offset(cls):
        return T(0)

    def utc_time(self):
        return T((45296, 789000000))


class DateTimeTestCase(TestCase):

    def test_zero(self):
        t = DateTime(0, 0, 0, 0, 0, 0)
        self.assertEqual(t.year, 0)
        self.assertEqual(t.month, 0)
        self.assertEqual(t.day, 0)
        self.assertEqual(t.hour, 0)
        self.assertEqual(t.minute, 0)
        self.assertEqual(t.second, 0)

    def test_non_zero_naive(self):
        t = DateTime(2018, 4, 26, 23, 0, 17.914390409)
        self.assertEqual(t.year, 2018)
        self.assertEqual(t.month, 4)
        self.assertEqual(t.day, 26)
        self.assertEqual(t.hour, 23)
        self.assertEqual(t.minute, 0)
        self.assertEqual(t.second, 17.914390409)

    def test_today(self):
        t = DateTime.today()
        self.assertEqual(t.year, 1970)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 1)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789)

    def test_now_without_tz(self):
        t = DateTime.now()
        self.assertEqual(t.year, 1970)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 1)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789)
        self.assertIsNone(t.tzinfo)

    def test_now_with_tz(self):
        t = DateTime.now(eastern)
        self.assertEqual(t.year, 1970)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 1)
        self.assertEqual(t.hour, 7)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789)
        self.assertEqual(t.utcoffset(), timedelta(seconds=-18000))
        self.assertEqual(t.dst(), timedelta())
        self.assertEqual(t.tzname(), "EST")

    def test_conversion_to_t(self):
        dt = DateTime(2018, 4, 26, 23, 0, 17.914390409)
        t = T(dt)
        self.assertEqual(t, T((63660380417, 914390409)))

    def test_add_timedelta(self):
        dt1 = DateTime(2018, 4, 26, 23, 0, 17.914390409)
        delta = timedelta(days=1)
        dt2 = dt1 + delta
        self.assertEqual(dt2, DateTime(2018, 4, 27, 23, 0, 17.914390409))

    def test_normalization(self):
        ndt1 = eastern.normalize(DateTime(2018, 4, 27, 23, 0, 17, tzinfo=eastern))
        ndt2 = eastern.normalize(datetime(2018, 4, 27, 23, 0, 17, tzinfo=eastern))
        self.assertEqual(ndt1, ndt2)

    def test_localization(self):
        ldt1 = eastern.localize(datetime(2018, 4, 27, 23, 0, 17))
        ldt2 = eastern.localize(DateTime(2018, 4, 27, 23, 0, 17))
        self.assertEqual(ldt1, ldt2)
