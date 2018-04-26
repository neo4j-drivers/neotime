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

import pytz

from neotime import DateTime


class DateTimeTestCase(TestCase):

    def test_zero_datetime(self):
        t = DateTime(0, 0, 0, 0, 0, 0)
        self.assertEqual(t.year, 0)
        self.assertEqual(t.month, 0)
        self.assertEqual(t.day, 0)
        self.assertEqual(t.hour, 0)
        self.assertEqual(t.minute, 0)
        self.assertEqual(t.second, 0)

    # TODO
    # def test_localization(self):
    #     eastern = pytz.timezone("US/Eastern")
    #     eastern.localize(DateTime.now_utc())
