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

from neotime import Time


class TimeTestCase(TestCase):

    def test_simple_time(self):
        t = Time(12, 34, 56.789)
        self.assertEqual(t.hour_minute_second, (12, 34, 56.789))
        self.assertEqual(t.ticks, 45296.789)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789)

    def test_midnight(self):
        t = Time(0, 0, 0)
        self.assertEqual(t.hour_minute_second, (0, 0, 0))
        self.assertEqual(t.ticks, 0)
        self.assertEqual(t.hour, 0)
        self.assertEqual(t.minute, 0)
        self.assertEqual(t.second, 0)

    def test_nanosecond_precision(self):
        t = Time(12, 34, 56.789123456)
        self.assertEqual(t.hour_minute_second, (12, 34, 56.789123456))
        self.assertEqual(t.ticks, 45296.789123456)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.minute, 34)
        self.assertEqual(t.second, 56.789123456)
