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


from unittest import TestCase

from neotime import Duration, Date


class DateTestCase(TestCase):

    def test_zero_date(self):
        t = Date(0, 0, 0)
        self.assertEqual(t.year_month_day, (0, 0, 0))
        self.assertEqual(t.year, 0)
        self.assertEqual(t.month, 0)
        self.assertEqual(t.day, 0)

    def test_all_positive_days_of_month_for_31_day_month(self):
        for day in range(1, 32):
            t = Date(1976, 1, day)
            self.assertEqual(t.year_month_day, (1976, 1, day))
            self.assertEqual(t.year, 1976)
            self.assertEqual(t.month, 1)
            self.assertEqual(t.day, day)
        with self.assertRaises(ValueError):
            _ = Date(1976, 1, 32)

    def test_all_positive_days_of_month_for_30_day_month(self):
        for day in range(1, 31):
            t = Date(1976, 6, day)
            self.assertEqual(t.year_month_day, (1976, 6, day))
            self.assertEqual(t.year, 1976)
            self.assertEqual(t.month, 6)
            self.assertEqual(t.day, day)
        with self.assertRaises(ValueError):
            _ = Date(1976, 6, 31)

    def test_all_positive_days_of_month_for_29_day_month(self):
        for day in range(1, 30):
            t = Date(1976, 2, day)
            self.assertEqual(t.year_month_day, (1976, 2, day))
            self.assertEqual(t.year, 1976)
            self.assertEqual(t.month, 2)
            self.assertEqual(t.day, day)
        with self.assertRaises(ValueError):
            _ = Date(1976, 2, 30)

    def test_all_positive_days_of_month_for_28_day_month(self):
        for day in range(1, 29):
            t = Date(1977, 2, day)
            self.assertEqual(t.year_month_day, (1977, 2, day))
            self.assertEqual(t.year, 1977)
            self.assertEqual(t.month, 2)
            self.assertEqual(t.day, day)
        with self.assertRaises(ValueError):
            _ = Date(1977, 2, 29)

    def test_last_but_2_day_for_31_day_month(self):
        t = Date(1976, 1, -3)
        self.assertEqual(t.year_month_day, (1976, 1, 29))
        self.assertEqual(t.year, 1976)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 29)

    def test_last_but_1_day_for_31_day_month(self):
        t = Date(1976, 1, -2)
        self.assertEqual(t.year_month_day, (1976, 1, 30))
        self.assertEqual(t.year, 1976)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 30)

    def test_last_day_for_31_day_month(self):
        t = Date(1976, 1, -1)
        self.assertEqual(t.year_month_day, (1976, 1, 31))
        self.assertEqual(t.year, 1976)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 31)

    def test_last_but_1_day_for_30_day_month(self):
        t = Date(1976, 6, -2)
        self.assertEqual(t.year_month_day, (1976, 6, 29))
        self.assertEqual(t.year, 1976)
        self.assertEqual(t.month, 6)
        self.assertEqual(t.day, 29)

    def test_last_day_for_30_day_month(self):
        t = Date(1976, 6, -1)
        self.assertEqual(t.year_month_day, (1976, 6, 30))
        self.assertEqual(t.year, 1976)
        self.assertEqual(t.month, 6)
        self.assertEqual(t.day, 30)

    def test_day_28_for_29_day_month(self):
        t = Date(1976, 2, 28)
        self.assertEqual(t.year_month_day, (1976, 2, 28))
        self.assertEqual(t.year, 1976)
        self.assertEqual(t.month, 2)
        self.assertEqual(t.day, 28)

    def test_last_day_for_29_day_month(self):
        t = Date(1976, 2, -1)
        self.assertEqual(t.year_month_day, (1976, 2, 29))
        self.assertEqual(t.year, 1976)
        self.assertEqual(t.month, 2)
        self.assertEqual(t.day, 29)

    def test_last_day_for_28_day_month(self):
        t = Date(1977, 2, -1)
        self.assertEqual(t.year_month_day, (1977, 2, 28))
        self.assertEqual(t.year, 1977)
        self.assertEqual(t.month, 2)
        self.assertEqual(t.day, 28)

    def test_cannot_use_year_lower_than_one(self):
        with self.assertRaises(ValueError):
            _ = Date(0, 2, 1)

    def test_cannot_use_year_higher_than_9999(self):
        with self.assertRaises(ValueError):
            _ = Date(10000, 2, 1)

    def test_can_add_years(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(years=2)
        self.assertEqual(d2, Date(1978, 6, 13))

    def test_can_add_negative_years(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(years=-2)
        self.assertEqual(d2, Date(1974, 6, 13))

    def test_can_add_years_and_months(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(years=2, months=3)
        self.assertEqual(d2, Date(1978, 9, 13))

    def test_can_add_negative_years_and_months(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(years=-2, months=-3)
        self.assertEqual(d2, Date(1974, 3, 13))

    def test_can_retain_offset_from_end_of_month(self):
        d = Date(1976, 1, -1)
        self.assertEqual(d, Date(1976, 1, 31))
        d += Duration(months=1)
        self.assertEqual(d, Date(1976, 2, 29))
        d += Duration(months=1)
        self.assertEqual(d, Date(1976, 3, 31))
        d += Duration(months=1)
        self.assertEqual(d, Date(1976, 4, 30))
        d += Duration(months=1)
        self.assertEqual(d, Date(1976, 5, 31))
        d += Duration(months=1)
        self.assertEqual(d, Date(1976, 6, 30))

    def test_can_roll_over_end_of_year(self):
        d = Date(1976, 12, 1)
        self.assertEqual(d, Date(1976, 12, 1))
        d += Duration(months=1)
        self.assertEqual(d, Date(1977, 1, 1))

    def test_can_add_months_and_days(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(months=1, days=1)
        self.assertEqual(d2, Date(1976, 7, 14))

    def test_can_add_months_then_days(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(months=1) + Duration(days=1)
        self.assertEqual(d2, Date(1976, 7, 14))

    def test_can_add_days_then_months(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(days=1) + Duration(months=1)
        self.assertEqual(d2, Date(1976, 7, 14))

    def test_can_add_months_and_days_for_last_day_of_short_month(self):
        d1 = Date(1976, 6, 30)
        d2 = d1 + Duration(months=1, days=1)
        self.assertEqual(d2, Date(1976, 8, 1))

    def test_can_add_months_then_days_for_last_day_of_short_month(self):
        d1 = Date(1976, 6, 30)
        d2 = d1 + Duration(months=1) + Duration(days=1)
        self.assertEqual(d2, Date(1976, 8, 1))

    def test_can_add_days_then_months_for_last_day_of_short_month(self):
        d1 = Date(1976, 6, 30)
        d2 = d1 + Duration(days=1) + Duration(months=1)
        self.assertEqual(d2, Date(1976, 8, 1))

    def test_can_add_months_and_days_for_last_day_of_long_month(self):
        d1 = Date(1976, 1, 31)
        d2 = d1 + Duration(months=1, days=1)
        self.assertEqual(d2, Date(1976, 3, 1))

    def test_can_add_months_then_days_for_last_day_of_long_month(self):
        d1 = Date(1976, 1, 31)
        d2 = d1 + Duration(months=1) + Duration(days=1)
        self.assertEqual(d2, Date(1976, 3, 1))

    def test_can_add_days_then_months_for_last_day_of_long_month(self):
        d1 = Date(1976, 1, 31)
        d2 = d1 + Duration(days=1) + Duration(months=1)
        self.assertEqual(d2, Date(1976, 3, 1))

    def test_can_add_negative_months_and_days(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(months=-1, days=-1)
        self.assertEqual(d2, Date(1976, 5, 12))

    def test_can_add_negative_months_then_days(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(months=-1) + Duration(days=-1)
        self.assertEqual(d2, Date(1976, 5, 12))

    def test_can_add_negative_days_then_months(self):
        d1 = Date(1976, 6, 13)
        d2 = d1 + Duration(days=-1) + Duration(months=-1)
        self.assertEqual(d2, Date(1976, 5, 12))

    def test_can_add_negative_months_and_days_for_first_day_of_month(self):
        d1 = Date(1976, 6, 1)
        d2 = d1 + Duration(months=-1, days=-1)
        self.assertEqual(d2, Date(1976, 4, 30))

    def test_can_add_negative_months_then_days_for_first_day_of_month(self):
        d1 = Date(1976, 6, 1)
        d2 = d1 + Duration(months=-1) + Duration(days=-1)
        self.assertEqual(d2, Date(1976, 4, 30))

    def test_can_add_negative_days_then_months_for_last_day_of_month(self):
        d1 = Date(1976, 6, 1)
        d2 = d1 + Duration(days=-1) + Duration(months=-1)
        self.assertEqual(d2, Date(1976, 4, 30))

    def test_can_add_negative_month_for_last_day_of_long_month(self):
        d1 = Date(1976, 5, 31)
        d2 = d1 + Duration(months=-1)
        self.assertEqual(d2, Date(1976, 4, 30))

    def test_date_difference(self):
        new_year = Date(2000, 1, 1)
        christmas = Date(1999, 12, 25)
        self.assertEqual(new_year - christmas, Duration(days=7))

    def test_date_less_than(self):
        new_year = Date(2000, 1, 1)
        christmas = Date(1999, 12, 25)
        self.assertLess(christmas, new_year)

    def test_date_greater_than(self):
        new_year = Date(2000, 1, 1)
        christmas = Date(1999, 12, 25)
        self.assertGreater(new_year, christmas)

    def test_date_equal(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 1)
        self.assertEqual(d1, d2)

    def test_date_not_equal(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 2)
        self.assertNotEqual(d1, d2)
