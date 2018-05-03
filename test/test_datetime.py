#!/usr/bin/env python
# coding: utf-8

# Copyright 2018, Nigel Small & Neo4j Sweden AB
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

from neotime import DateTime, MIN_YEAR, MAX_YEAR, Duration
from neotime.clock_implementations import Clock, ClockTime


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
        return ClockTime()

    def utc_time(self):
        return ClockTime(45296, 789000000)


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

    def test_year_lower_bound(self):
        with self.assertRaises(ValueError):
            _ = DateTime(MIN_YEAR - 1, 1, 1, 0, 0, 0)

    def test_year_upper_bound(self):
        with self.assertRaises(ValueError):
            _ = DateTime(MAX_YEAR + 1, 1, 1, 0, 0, 0)

    def test_month_lower_bound(self):
        with self.assertRaises(ValueError):
            _ = DateTime(2000, 0, 1, 0, 0, 0)

    def test_month_upper_bound(self):
        with self.assertRaises(ValueError):
            _ = DateTime(2000, 13, 1, 0, 0, 0)

    def test_day_zero(self):
        with self.assertRaises(ValueError):
            _ = DateTime(2000, 1, 0, 0, 0, 0)

    def test_day_30_of_29_day_month(self):
        with self.assertRaises(ValueError):
            _ = DateTime(2000, 2, 30, 0, 0, 0)

    def test_day_32_of_31_day_month(self):
        with self.assertRaises(ValueError):
            _ = DateTime(2000, 3, 32, 0, 0, 0)

    def test_day_31_of_30_day_month(self):
        with self.assertRaises(ValueError):
            _ = DateTime(2000, 4, 31, 0, 0, 0)

    def test_day_29_of_28_day_month(self):
        with self.assertRaises(ValueError):
            _ = DateTime(1999, 2, 29, 0, 0, 0)

    def test_last_day_of_month(self):
        t = DateTime(2000, 1, -1, 0, 0, 0)
        self.assertEqual(t.year, 2000)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 31)

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

    def test_utc_now(self):
        t = DateTime.utc_now()
        self.assertEqual(t.year, 1970)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 1)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789)
        self.assertIsNone(t.tzinfo)

    def test_from_timestamp(self):
        t = DateTime.from_timestamp(0)
        self.assertEqual(t.year, 1970)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 1)
        self.assertEqual(t.hour, 0)
        self.assertEqual(t.minute, 0)
        self.assertEqual(t.second, 0.0)
        self.assertIsNone(t.tzinfo)

    def test_from_overflowing_timestamp(self):
        with self.assertRaises(ValueError):
            _ = DateTime.from_timestamp(999999999999999999)

    def test_from_timestamp_with_tz(self):
        t = DateTime.from_timestamp(0, eastern)
        self.assertEqual(t.year, 1969)
        self.assertEqual(t.month, 12)
        self.assertEqual(t.day, 31)
        self.assertEqual(t.hour, 19)
        self.assertEqual(t.minute, 0)
        self.assertEqual(t.second, 0.0)
        self.assertEqual(t.utcoffset(), timedelta(seconds=-18000))
        self.assertEqual(t.dst(), timedelta())
        self.assertEqual(t.tzname(), "EST")

    def test_conversion_to_t(self):
        dt = DateTime(2018, 4, 26, 23, 0, 17.914390409)
        t = dt.to_clock_time()
        self.assertEqual(t, ClockTime(63660380417, 914390409))

    def test_add_timedelta(self):
        dt1 = DateTime(2018, 4, 26, 23, 0, 17.914390409)
        delta = timedelta(days=1)
        dt2 = dt1 + delta
        self.assertEqual(dt2, DateTime(2018, 4, 27, 23, 0, 17.914390409))

    def test_subtract_datetime_1(self):
        dt1 = DateTime(2018, 4, 26, 23, 0, 17.914390409)
        dt2 = DateTime(2018, 1, 1, 0, 0, 0.0)
        t = dt1 - dt2
        self.assertEqual(t, Duration(months=3, days=25, hours=23, seconds=17.914390409))

    def test_subtract_datetime_2(self):
        dt1 = DateTime(2018, 4, 1, 23, 0, 17.914390409)
        dt2 = DateTime(2018, 1, 26, 0, 0, 0.0)
        t = dt1 - dt2
        self.assertEqual(t, Duration(months=3, days=-25, hours=23, seconds=17.914390409))

    def test_subtract_native_datetime_1(self):
        dt1 = DateTime(2018, 4, 26, 23, 0, 17.914390409)
        dt2 = datetime(2018, 1, 1, 0, 0, 0)
        t = dt1 - dt2
        self.assertEqual(t, timedelta(days=115, hours=23, seconds=17.914390409))

    def test_subtract_native_datetime_2(self):
        dt1 = DateTime(2018, 4, 1, 23, 0, 17.914390409)
        dt2 = datetime(2018, 1, 26, 0, 0, 0)
        t = dt1 - dt2
        self.assertEqual(t, timedelta(days=65, hours=23, seconds=17.914390409))

    def test_normalization(self):
        ndt1 = eastern.normalize(DateTime(2018, 4, 27, 23, 0, 17, tzinfo=eastern))
        ndt2 = eastern.normalize(datetime(2018, 4, 27, 23, 0, 17, tzinfo=eastern))
        self.assertEqual(ndt1, ndt2)

    def test_localization(self):
        ldt1 = eastern.localize(datetime(2018, 4, 27, 23, 0, 17))
        ldt2 = eastern.localize(DateTime(2018, 4, 27, 23, 0, 17))
        self.assertEqual(ldt1, ldt2)
